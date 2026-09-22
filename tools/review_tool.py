# -*- coding: utf-8 -*-
"""Winds of Change 中文化 : 翻译校对工作流 (纯标准库, Python 3.8+)

流程
----
    stats                 看进度
    scan                  规则预筛 -> review/findings.md + review/candidates.tsv
    export                导出校对清单 -> review/sheet_*.tsv (含 source/target/revised)
    terms [--apply]       术语统一 (blade=剑 之类), 默认 dry-run 只出差异
    apply [--build]       把清单里填好的 revised 写回 chunks, 可选重新 build

目录约定
--------
    tl_work/chunks/dialogue/*.tsv   对白: seq block idx speaker source target
    tl_work/chunks/strings/*.tsv    界面: seq file key target
    review/terms.tsv                术语规则表
    review/                         所有校对产物

术语规则表 review/terms.tsv 列:
    en <TAB> cn <TAB> variants <TAB> protect <TAB> mode <TAB> note
        en       英文词 (source 匹配, mode=word 按词边界, mode=phrase 按子串)
        cn       规定译法
        variants 该词的其他译法, 用 | 分隔; 统一时会被替换成 cn
        protect  保护子串, 用 | 分隔; 这些片段内的字不参与替换
        mode     word | phrase
"""
import argparse, collections, glob, io, json, os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TL_DEFAULT = os.path.join(ROOT, "tl_work")
REVIEW = os.path.join(ROOT, "review")
TERMS = os.path.join(REVIEW, "terms.tsv")
FIXUPS = os.path.join(REVIEW, "fixups.tsv")
TL_TOOL = os.path.join(TL_DEFAULT, "tl_tool.py")

KINDS = {
    "dialogue": {"folder": "chunks/dialogue", "scol": 4, "tcol": 5, "sample": "dialogue_0001.tsv"},
    "strings":  {"folder": "chunks/strings",  "scol": 2, "tcol": 3, "sample": "strings_0001.tsv"},
}

# ---------------------------------------------------------------- 基础读写

def read_text(p):
    return io.open(p, encoding="utf-8-sig").read()


def write_text(p, text):
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(p, "w", encoding="utf-8-sig", newline="\n").write(text)


def iter_rows(tl_dir):
    """逐行读出可翻译条目。"""
    for kind, cfg in KINDS.items():
        folder = os.path.join(tl_dir, cfg["folder"].replace("/", os.sep))
        for path in sorted(glob.glob(os.path.join(folder, "*.tsv"))):
            lines = read_text(path).split("\n")
            for i, ln in enumerate(lines):
                if not ln or ln.startswith("#"):
                    continue
                parts = ln.split("\t")
                if len(parts) <= cfg["tcol"]:
                    continue
                yield {
                    "kind": kind, "chunk": os.path.basename(path), "line": i,
                    "seq": parts[0], "speaker": parts[3] if kind == "dialogue" else "",
                    "src": parts[cfg["scol"]], "tgt": parts[cfg["tcol"]],
                    "parts": parts,
                }


def write_row(path, line_no, parts):
    lines = read_text(path).split("\n")
    lines[line_no] = "\t".join(parts)
    write_text(path, "\n".join(lines))


# ---------------------------------------------------------------- 文本工具

ESC = "\x01"          # [[ 的占位符, 避免被当成插值标签
LITERAL_NL = "\\n"    # 字面量反斜杠+n, 代表换行
TAG_RE = re.compile(r"\{[^{}]*\}")
INT_RE = re.compile(r"\[[^\[\]]*\]")
WORD_RE = re.compile(r"[A-Za-z]{3,}")
HALF_RE = re.compile(r"[,;:!?]")
KEY_LEAK_RE = re.compile(r"\bz\d{4,}\b")
# Ren'Py 引擎内置串: 按键名/占位符/调试串/游戏标题, 通常就该保留英文
ENGINE_HINT_RE = re.compile(
    r"^(\{#|\()|^(Escape|Ctrl|Tab|Shift|Alt|Enter|Return|Space|Page Up|Page Down|NPOT"
    r"|Winds of Change)$|[<>]|\[name\] \[attributes\]")
NAME_LEAK_RE = re.compile(r"\b[A-Z][a-z]{2,}\s*:")
REPEAT_RE = re.compile(r"(我我|的的|了了|是是|你你|他他|们们)")


def mask(s):
    return s.replace("[[", ESC)


def unmask(s):
    return s.replace(ESC, "[[")


def tags(s):
    return TAG_RE.findall(mask(s))


def interps(s):
    return INT_RE.findall(mask(s))


def plain(s):
    """去掉标签/插值/转义标记后的纯文本 (用于标点与英文残留检查)。"""
    s = mask(s)
    s = TAG_RE.sub("", s)
    s = INT_RE.sub("", s)
    return unmask(s)


def has_letters(s):
    return bool(re.search(r"[A-Za-z]{2,}", s))


# ---------------------------------------------------------------- 规则

def load_terms(path=TERMS):
    rules = []
    if not os.path.isfile(path):
        return rules
    for ln in read_text(path).split("\n"):
        if not ln or ln.startswith("#"):
            continue
        p = ln.split("\t")
        while len(p) < 7:
            p.append("")
        rules.append({"en": p[0].strip(), "cn": p[1].strip(),
                      "variants": [x for x in p[2].split("|") if x],
                      "protect": [x for x in p[3].split("|") if x],
                      "mode": (p[4].strip() or "word"),
                      "exclude_en": p[5].strip(), "note": p[6].strip()})
    return rules


def load_fixups(path=FIXUPS):
    """一次性润色表: old <TAB> new <TAB> note, 对所有译文生效。"""
    out = []
    if not os.path.isfile(path):
        return out
    for ln in read_text(path).split("\n"):
        if not ln or ln.startswith("#"):
            continue
        p = ln.split("\t")
        if len(p) >= 2 and p[0]:
            out.append((p[0], p[1], p[2] if len(p) > 2 else ""))
    return out


def rule_applies(src, rule):
    """规则是否作用于该行: 先匹配 en, 再排除 exclude_en 命中的行。"""
    if not rule["cn"] or not src_matches(src, rule):
        return False
    ex = rule.get("exclude_en")
    if ex and re.search(r"\b" + re.escape(ex) + r"\b", src, re.I):
        return False
    return True


def src_matches(src, rule):
    if rule["mode"] == "phrase":
        return rule["en"].lower() in src.lower()
    return bool(re.search(r"\b" + re.escape(rule["en"]) + r"\b", src, re.I))


def scan_rows(rows, rules):
    """返回候选问题列表 (severity, rule, kind, chunk, seq, speaker, src, tgt, note)。"""
    out = []

    def add(sev, rule, r, note):
        out.append({"sev": sev, "rule": rule, "kind": r["kind"], "chunk": r["chunk"],
                    "seq": r["seq"], "speaker": r["speaker"], "src": r["src"],
                    "tgt": r["tgt"], "note": note})

    for r in rows:
        src, tgt = r["src"], r["tgt"]
        p = plain(tgt)

        if KEY_LEAK_RE.search(tgt) or NAME_LEAK_RE.search(plain(tgt)):
            add("high", "key-leak", r, "译文里混入了内部键号或英文角色名")
        if tags(src) != tags(tgt):
            add("high", "tag-mismatch", r, "{} 标签集合与原文不一致")
        if interps(src) != interps(tgt):
            add("high", "interp-mismatch", r, "[] 插值集合与原文不一致")
        if has_letters(src) and tgt.strip() == src.strip():
            if ENGINE_HINT_RE.search(src.strip()):
                add("info", "engine-string", r, "引擎内置字符串, 通常保留原文")
            else:
                add("high", "untranslated", r, "译文与原文相同, 可能未翻译")

        for rule in rules:
            if not rule_applies(src, rule):
                continue
            if rule["cn"] in tgt:
                continue
            hit = [v for v in rule["variants"] if v in tgt]
            note = "术语 %s 应为「%s」" % (rule["en"], rule["cn"])
            if hit:
                note += ", 现用「%s」" % "/".join(hit)
            add("term", "term-%s" % rule["en"].lower().replace(" ", "-"), r, note)

        if HALF_RE.search(p):
            add("low", "halfwidth-punct", r, "中文里出现半角 , ; : ! ?")
        m = WORD_RE.findall(p)
        if m:
            add("low", "ascii-residue", r, "残留英文单词: " + ",".join(sorted(set(m))[:4]))
        if REPEAT_RE.search(p):
            add("low", "repeated-char", r, "可能重复用字: " + REPEAT_RE.search(p).group(1))
        if src.strip() and len(src) > 20:
            ratio = len(tgt) / float(len(src))
            if ratio > 0.9 or ratio < 0.15:
                add("low", "length-ratio", r, "长度比 %.2f 偏离常规" % ratio)
    return out


def term_diff(rows, rules, fixups=None):
    """术语统一 + 润色: 返回需要改写的行与改后文本。"""
    out = []
    fixups = fixups or []
    for r in rows:
        src, tgt = r["src"], r["tgt"]
        new = tgt
        notes = []
        for rule in rules:
            if not rule_applies(src, rule):
                continue
            if not rule["variants"]:
                continue
            cur = new
            for v in rule["variants"]:
                if v not in cur:
                    continue
                # 先保护专名片段, 再替换
                marks = {}
                for i, ph in enumerate(rule["protect"]):
                    key = "\x02%d\x03" % i
                    while ph in cur:
                        marks[key] = ph
                        cur = cur.replace(ph, key, 1)
                cur = cur.replace(v, rule["cn"])
                for key, ph in marks.items():
                    cur = cur.replace(key, ph)
            if cur != new:
                notes.append("%s -> %s" % (rule["en"], rule["cn"]))
                new = cur
        for old, new_s, note in fixups:
            if old and old in new:
                new = new.replace(old, new_s)
                notes.append("润色: " + (note or ("%s -> %s" % (old, new_s))))
        if new != tgt:
            out.append((r, new, "; ".join(notes)))
    return out


# ---------------------------------------------------------------- 命令

# ---- 语域标记表 ----------------------------------------------------------
# 对话里出现这些 = 念台词风险 (书面/文言腔)
WRITTEN_MARKS = ["亦然", "意欲何为", "乃至", "皆", "乃", "岂", "尚且", "何况", "予以",
                 "加以", "从而", "因而", "故而", "由此可见", "极为", "甚为", "颇为",
                 "亦", "遂", "并非如此", "何须"]
# 奇幻语境里的现代职场/技术词 (独白或对话出现都不自然)
MODERN_MARKS = ["团队", "优先级", "进度", "效率", "资源", "管理员", "失业",
                "制度", "流程", "反馈", "沟通", "管理"]
# 内心独白里出现这些 = 旁白过于口语/网络化
COLLOQ_MARKS = ["稳了", "溜了", "咋", "咱", "绝了", "上头", "破防", "哥们", "老铁",
                "大佬", "牛逼", "事儿", "味儿", "搞定", "没辙"]


def classify(r):
    """内心独白 (speaker 空) / 人物对话 / 界面串。"""
    if r["kind"] == "strings":
        return "ui"
    return "dialogue" if r["speaker"] else "monologue"


def cmd_register(args):
    """按 内心独白 / 人物对话 分层, 分别检查语域 (书面腔、现代词、口语网络词)。"""
    rows = list(iter_rows(args.tl_dir))
    bucket = collections.Counter()
    hits = collections.defaultdict(list)
    for r in rows:
        kind = classify(r)
        bucket[kind] += 1
        t = plain(r["tgt"])
        if kind == "dialogue":
            for m in WRITTEN_MARKS:
                if m in t:
                    hits[("dialogue", "书面/文言腔", m)].append(r); break
            for m in MODERN_MARKS:
                if m in t:
                    hits[("dialogue", "现代职场词", m)].append(r); break
        elif kind == "monologue":
            for m in COLLOQ_MARKS:
                if m in t:
                    hits[("monologue", "口语/网络词", m)].append(r); break
            for m in MODERN_MARKS:
                if m in t:
                    hits[("monologue", "现代职场词", m)].append(r); break
    os.makedirs(REVIEW, exist_ok=True)
    with io.open(os.path.join(REVIEW, "register.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# 语域分层检查 (内心独白 / 人物对话)\n\n生成时间: %s\n\n" % time.strftime("%Y-%m-%d %H:%M"))
        f.write("| 层 | 行数 |\n| --- | --- |\n")
        for k in ("monologue", "dialogue", "ui"):
            f.write("| %s | %d |\n" % ({"monologue": "内心独白", "dialogue": "人物对话", "ui": "界面串"}[k], bucket[k]))
        f.write("\n---\n\n")
        for (kind, cat, mark), items in sorted(hits.items(), key=lambda kv: (kv[0][0], kv[0][1], -len(kv[1]))):
            f.write("## [%s] %s — 标记「%s」 %d 条\n\n" %
                    ({"monologue": "内心独白", "dialogue": "人物对话"}[kind], cat, mark, len(items)))
            for r in items[:args.show]:
                f.write("- `%s#%s` %s\n  - EN: %s\n  - CN: %s\n"
                        % (r["chunk"], r["seq"], r["speaker"] or "旁白",
                           r["src"].replace("\n", " ")[:110], r["tgt"].replace("\n", " ")[:110]))
            if len(items) > args.show:
                f.write("- ... 其余 %d 条\n" % (len(items) - args.show))
            f.write("\n")
    print("分层: 内心独白 %d, 人物对话 %d, 界面串 %d" % (bucket["monologue"], bucket["dialogue"], bucket["ui"]))
    print("报告 -> review/register.md")
    for (kind, cat, mark), items in sorted(hits.items(), key=lambda kv: -len(kv[1]))[:14]:
        print("   [%-4s] %-10s %-8s %d" % ({"monologue": "独白", "dialogue": "对话"}[kind], cat, mark, len(items)))
    return 0


def cmd_dedupe(args):
    """同一句英文(同一说话人)在全篇出现多次时, 统一为用得最多的那种译法。"""
    rows = list(iter_rows(args.tl_dir))
    groups = collections.defaultdict(list)
    for r in rows:
        if r["kind"] != "dialogue" or len(r["src"].strip()) <= 25:
            continue
        groups[(r["src"].strip(), r["speaker"])].append(r)
    diff = []
    for key, items in groups.items():
        tgts = collections.Counter(r["tgt"].strip() for r in items)
        if len(tgts) < 2:
            continue
        best = tgts.most_common(1)[0][0]
        for r in items:
            if r["tgt"].strip() != best:
                diff.append((r, best, "重复句统一 (同句出现 %d 次)" % len(items)))
    print("重复句组: %d, 需要统一的译法: %d 行" % (sum(1 for v in groups.values() if len(v) > 1), len(diff)))
    for r, new, note in diff[:args.show]:
        print("  %-20s #%-6s %s" % (r["chunk"], r["seq"], note))
        print("     - %s" % r["tgt"].replace("\n", " ")[:100])
        print("     + %s" % new.replace("\n", " ")[:100])
    if len(diff) > args.show:
        print("  ... 其余 %d 行省略" % (len(diff) - args.show))
    if not diff or not args.apply:
        print("\n(dry-run, 加 --apply 才会写回)")
        return 0
    return apply_changes(args, diff, "dedupe")


def apply_changes(args, diff, label):
    """把 (row, new_target, note) 列表写回 chunks, 先备份。"""
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = os.path.join(REVIEW, "backup_chunks_%s_%s" % (label, stamp))
    touched = collections.defaultdict(list)
    for r, new, note in diff:
        touched[r["kind"]].append((r, new))
    for kind in touched:
        src_folder = os.path.join(args.tl_dir, KINDS[kind]["folder"].replace("/", os.sep))
        dst_folder = os.path.join(backup, KINDS[kind]["folder"].replace("/", os.sep))
        os.makedirs(dst_folder, exist_ok=True)
        for f in glob.glob(os.path.join(src_folder, "*.tsv")):
            shutil.copy2(f, os.path.join(dst_folder, os.path.basename(f)))
    n = 0
    for kind, items in touched.items():
        for r, new in items:
            path = os.path.join(args.tl_dir, KINDS[kind]["folder"].replace("/", os.sep), r["chunk"])
            parts = list(r["parts"])
            parts[KINDS[kind]["tcol"]] = new
            write_row(path, r["line"], parts)
            n += 1
    print("已写回 %d 行 (%s); chunks 备份 -> %s" % (n, label, backup))
    if args.build:
        return build(args)
    return 0


TAIL_MARKS = ["啊", "吧", "呢", "吗", "嘛", "呀", "哦", "哈", "嗯", "啦", "哟", "欸", "唉"]
ADDRESS_MARKS = ["大人", "阁下", "长官", "先生", "女士", "小姐", "兄弟", "姐妹们", "同胞们",
                 "朋友", "孩子", "小子", "老家伙", "头儿", "陛下", "君主", "长老", "先知"]


def cmd_chars(args):
    """按说话人统计语气证据, 输出 docs/character-stats.md (供人工写角色档案)。"""
    rows = list(iter_rows(args.tl_dir))
    spk = collections.defaultdict(list)
    for r in rows:
        if r["kind"] == "dialogue":
            spk[r["speaker"] or "(旁白/内心独白)"].append(r)
    stats = {}
    for name, items in spk.items():
        tgts = [r["tgt"] for r in items]
        blob = "".join(tgts)
        lens = [len(t) for t in tgts if t]
        stats[name] = {
            "n": len(items),
            "avg": sum(lens) / max(1, len(lens)),
            "nin": blob.count("您"), "ni": blob.count("你"),
            "written": sum(blob.count(m) for m in WRITTEN_MARKS),
            "modern": sum(blob.count(m) for m in MODERN_MARKS),
            "colloq": sum(blob.count(m) for m in COLLOQ_MARKS),
            "tails": sorted(((m, blob.count(m)) for m in TAIL_MARKS if blob.count(m)), key=lambda x: -x[1])[:4],
            "addr": sorted(((m, blob.count(m)) for m in ADDRESS_MARKS if blob.count(m)), key=lambda x: -x[1])[:4],
            "samples": [items[len(items) // 5]["tgt"], items[len(items) // 2]["tgt"], items[-len(items) // 5]["tgt"]],
        }
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    out = os.path.join(ROOT, "docs", "character-stats.md")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 角色语气证据表 (自动生成, 勿手改)\n\n生成时间: %s\n\n" % time.strftime("%Y-%m-%d %H:%M"))
        f.write("由 `review_tool.py chars` 生成, 供 `docs/characters.md` 人工定稿参考。\n\n")
        f.write("| 说话人 | 行数 | 平均句长 | 您/你 | 书面腔 | 现代词 | 口语词 | 常见句末 | 称呼 |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for name, s in sorted(stats.items(), key=lambda kv: -kv[1]["n"]):
            f.write("| %s | %d | %.0f | %d/%d | %d | %d | %d | %s | %s |\n" % (
                name, s["n"], s["avg"], s["nin"], s["ni"], s["written"], s["modern"], s["colloq"],
                " ".join("%s%d" % t for t in s["tails"]) or "-",
                " ".join("%s%d" % t for t in s["addr"]) or "-"))
        f.write("\n---\n\n")
        for name, s in sorted(stats.items(), key=lambda kv: -kv[1]["n"]):
            f.write("## %s (%d 行)\n\n" % (name, s["n"]))
            for x in s["samples"]:
                f.write("- %s\n" % x.replace("\n", " ")[:120])
            f.write("\n")
    print("证据表 -> docs/character-stats.md (%d 个说话人)" % len(stats))
    return 0


def cmd_worklist(args):
    """按 chunk 生成精校工单与进度清单。"""
    rows = list(iter_rows(args.tl_dir))
    cand = scan_rows(rows, load_terms())
    per = collections.defaultdict(list)
    for c in cand:
        per[c["chunk"]].append(c)
    counts = collections.Counter()
    for r in rows:
        counts[(r["chunk"], classify(r))] += 1
    chunks = sorted(set(list(per) + [k[0] for k in counts]))
    os.makedirs(REVIEW, exist_ok=True)
    order = {"high": 0, "term": 1, "low": 2, "info": 3}
    with io.open(os.path.join(REVIEW, "worklist.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# 精校工单 (按 chunk)\n\n生成时间: %s\n\n" % time.strftime("%Y-%m-%d %H:%M"))
        f.write("逐个 chunk 精校: 先读 `docs/characters.md` 确认该角色语气, 处理完本页候选后在 checklist.csv 标记。\n\n")
        for ch in chunks:
            items = sorted(per.get(ch, []), key=lambda c: (order.get(c["sev"], 9), int(c["seq"] or 0)))
            kinds = " ".join("%s=%d" % (k, counts[(ch, k)]) for k in ("monologue", "dialogue", "ui") if counts[(ch, k)])
            f.write("## %s\n\n行数: %s | 候选: %d\n\n" % (ch, kinds or "-", len(items)))
            if not items:
                f.write("无候选, 可直接人工通读一遍。\n\n"); continue
            for c in items[:args.show]:
                f.write("- **%s** `%s#%s` %s\n  - EN: %s\n  - CN: %s\n  - %s\n"
                        % (c["sev"], c["chunk"], c["seq"], c["speaker"] or "旁白",
                           c["src"].replace("\n", " ")[:110], c["tgt"].replace("\n", " ")[:110], c["note"]))
            if len(items) > args.show:
                f.write("- ... 其余 %d 条见 review/candidates.tsv\n" % (len(items) - args.show))
            f.write("\n")
    ck = os.path.join(REVIEW, "checklist.csv")
    old = {}
    if os.path.isfile(ck):
        for ln in read_text(ck).split("\n"):
            p = ln.split(",")
            if len(p) >= 2 and p[0] != "chunk":
                old[p[0]] = p
    with io.open(ck, "w", encoding="utf-8", newline="\n") as f:
        f.write("chunk,rows,candidates,status,reviewer,date,note\n")
        for ch in chunks:
            prev = old.get(ch)
            n = sum(v for (c, k), v in counts.items() if c == ch)
            f.write("%s,%d,%d,%s,%s,%s,%s\n" % (ch, n, len(per.get(ch, [])),
                    prev[3] if prev else "未开始", prev[4] if prev and len(prev) > 4 else "",
                    prev[5] if prev and len(prev) > 5 else "", prev[6] if prev and len(prev) > 6 else ""))
    print("工单 -> review/worklist.md (%d 个 chunk)" % len(chunks))
    print("进度清单 -> review/checklist.csv")
    return 0


def cmd_mark(args):
    """更新 checklist.csv 中某个 chunk 的校对状态。"""
    ck = os.path.join(REVIEW, "checklist.csv")
    if not os.path.isfile(ck):
        sys.exit("先运行 worklist 生成 review/checklist.csv")
    lines = read_text(ck).rstrip("\n").split("\n")
    hit = False
    for i, ln in enumerate(lines):
        p = ln.split(",")
        if p and p[0] == args.chunk:
            while len(p) < 7:
                p.append("")
            p[3] = args.status
            if args.reviewer:
                p[4] = args.reviewer
            p[5] = time.strftime("%Y-%m-%d")
            if args.note:
                p[6] = args.note.replace(",", ";")
            lines[i] = ",".join(p)
            hit = True
    if not hit:
        sys.exit("checklist.csv 里没有: " + args.chunk)
    write_text(ck, "\n".join(lines) + "\n")
    print("已标记 %s = %s" % (args.chunk, args.status))
    return 0


def cmd_stats(args):
    rows = list(iter_rows(args.tl_dir))
    for kind in KINDS:
        sub = [r for r in rows if r["kind"] == kind]
        done = sum(1 for r in sub if r["tgt"].strip() and r["tgt"] != r["src"])
        print("%-9s %5d / %5d  (%.1f%%)" % (kind, done, len(sub), 100.0 * done / max(1, len(sub))))
    cand = scan_rows(rows, load_terms())
    cnt = collections.Counter(c["rule"] for c in cand)
    print("预筛候选: %d 条" % len(cand))
    for k, v in cnt.most_common():
        print("   %-22s %d" % (k, v))
    return 0


def cmd_scan(args):
    rows = list(iter_rows(args.tl_dir))
    cand = scan_rows(rows, load_terms())
    os.makedirs(REVIEW, exist_ok=True)
    ts = time.strftime("%Y-%m-%d %H:%M")
    order = {"high": 0, "term": 1, "low": 2, "info": 3}
    cand.sort(key=lambda c: (order.get(c["sev"], 3), c["rule"], c["chunk"], int(c["seq"] or 0)))

    with io.open(os.path.join(REVIEW, "candidates.tsv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# severity\trule\tkind\tchunk\tseq\tspeaker\tsource\ttarget\tnote\n")
        for c in cand:
            f.write("\t".join(x.replace("\t", " ") for x in
                              (c["sev"], c["rule"], c["kind"], c["chunk"], c["seq"],
                               c["speaker"], c["src"], c["tgt"], c["note"])) + "\n")

    groups = collections.defaultdict(list)
    for c in cand:
        groups[(c["sev"], c["rule"])].append(c)
    with io.open(os.path.join(REVIEW, "findings.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("# 翻译校对预筛报告\n\n生成时间: %s\n\n" % ts)
        f.write("扫描条目: %d; 候选问题: %d\n\n" % (len(rows), len(cand)))
        f.write("| 等级 | 规则 | 数量 | 说明 |\n| --- | --- | --- | --- |\n")
        desc = {
            "key-leak": "译文混入内部键号/英文角色名", "tag-mismatch": "{} 标签不一致",
            "interp-mismatch": "[] 插值不一致", "untranslated": "疑似未翻译",
            "halfwidth-punct": "半角标点", "ascii-residue": "残留英文单词",
            "repeated-char": "重复用字", "length-ratio": "长度异常",
            "engine-string": "引擎内置串 (正常)",
        }
        for (sev, rule), items in sorted(groups.items(), key=lambda kv: (order.get(kv[0][0], 3), kv[0][1])):
            f.write("| %s | %s | %d | %s |\n" % (sev, rule, len(items), desc.get(rule, "术语不一致")))
        f.write("\n---\n\n")
        for (sev, rule), items in sorted(groups.items(), key=lambda kv: (order.get(kv[0][0], 3), kv[0][1])):
            f.write("## [%s] %s — %d 条\n\n" % (sev, rule, len(items)))
            for c in items[:args.show]:
                f.write("- `%s#%s` %s\n  - 原文: %s\n  - 现译: %s\n  - 说明: %s\n"
                        % (c["chunk"], c["seq"], c["speaker"] or "", c["src"][:120],
                           c["tgt"][:120], c["note"]))
            if len(items) > args.show:
                f.write("- ... 其余 %d 条见 candidates.tsv\n" % (len(items) - args.show))
            f.write("\n")
    print("候选 %d 条 -> review/candidates.tsv" % len(cand))
    print("报告 -> review/findings.md")
    for (sev, rule), items in sorted(groups.items(), key=lambda kv: (order.get(kv[0][0], 3), -len(kv[1]))):
        print("   [%-4s] %-22s %d" % (sev, rule, len(items)))
    return 0


def cmd_export(args):
    os.makedirs(REVIEW, exist_ok=True)
    n = 0
    buckets = collections.defaultdict(list)
    for r in iter_rows(args.tl_dir):
        buckets[(r["kind"], r["chunk"])].append(r)
    for (kind, chunk), rows in sorted(buckets.items()):
        out = ["# review sheet  %s  %s  (%d rows)" % (kind, chunk, len(rows)),
               "# chunk\tkind\tseq\tspeaker\tsource\ttarget\tverdict\trevised\tnote"]
        for r in rows:
            out.append("\t".join(x.replace("\t", " ") for x in
                                 (r["chunk"], r["kind"], r["seq"], r["speaker"],
                                  r["src"], r["tgt"], "", "", "")))
        write_text(os.path.join(REVIEW, "sheet_%s" % chunk), "\n".join(out) + "\n")
        n += len(rows)
    print("导出 %d 行 -> review/sheet_*.tsv" % n)
    return 0


def cmd_terms(args):
    rows = list(iter_rows(args.tl_dir))
    rules = load_terms()
    if args.rule:
        rules = [r for r in rules if r["en"].lower() == args.rule.lower()]
        if not rules:
            sys.exit("terms.tsv 里没有规则: " + args.rule)
    diff = term_diff(rows, rules, load_fixups())
    print("待改写: %d 行" % len(diff))
    for r, new, note in diff[:args.show]:
        print("  %-20s #%-6s %s" % (r["chunk"], r["seq"], note))
        print("     - %s" % r["tgt"].replace("\n", " ")[:110])
        print("     + %s" % new.replace("\n", " ")[:110])
    if len(diff) > args.show:
        print("  ... 其余 %d 行省略" % (len(diff) - args.show))
    if not args.apply:
        print("\n(dry-run, 加 --apply 才会写入 chunks)")
        return 0

    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = os.path.join(REVIEW, "backup_chunks_%s" % stamp)
    touched = collections.defaultdict(list)
    for r, new, note in diff:
        touched[r["kind"]].append((r, new))
    for kind, items in touched.items():
        src_folder = os.path.join(args.tl_dir, KINDS[kind]["folder"].replace("/", os.sep))
        dst_folder = os.path.join(backup, KINDS[kind]["folder"].replace("/", os.sep))
        os.makedirs(dst_folder, exist_ok=True)
        for f in glob.glob(os.path.join(src_folder, "*.tsv")):
            shutil.copy2(f, os.path.join(dst_folder, os.path.basename(f)))
    for kind, items in touched.items():
        for r, new in items:
            path = os.path.join(args.tl_dir, KINDS[kind]["folder"].replace("/", os.sep), r["chunk"])
            parts = list(r["parts"])
            parts[KINDS[kind]["tcol"]] = new
            write_row(path, r["line"], parts)
    print("已写回 %d 行; chunks 备份 -> %s" % (len(diff), backup))
    if args.build:
        return build(args)
    return 0


def cmd_apply(args):
    pattern = args.sheet or os.path.join(REVIEW, "sheet_*.tsv")
    files = sorted(glob.glob(pattern))
    if not files:
        sys.exit("找不到校对清单: " + pattern)
    changes = collections.defaultdict(list)
    for path in files:
        for ln in read_text(path).split("\n"):
            if not ln or ln.startswith("#"):
                continue
            p = ln.split("\t")
            if len(p) < 9:
                continue
            chunk, kind, seq, spk, src, tgt, verdict, revised, note = p[:9]
            if revised.strip() and revised != tgt:
                changes[kind].append((chunk, seq, tgt, revised, verdict, note))
    total = sum(len(v) for v in changes.values())
    print("清单中已修改行: %d" % total)
    for kind, items in changes.items():
        for chunk, seq, old, new, verdict, note in items[:args.show]:
            print("  %-20s #%-6s %s" % (chunk, seq, (verdict or "-")))
            print("     - %s" % old.replace("\n", " ")[:110])
            print("     + %s" % new.replace("\n", " ")[:110])
    if not total:
        return 0
    if not args.write:
        print("\n(dry-run, 加 --write 才会写回 chunks)")
        return 0
    for kind, items in changes.items():
        cfg = KINDS[kind]
        folder = os.path.join(args.tl_dir, cfg["folder"].replace("/", os.sep))
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup = os.path.join(REVIEW, "backup_chunks_%s" % stamp, cfg["folder"].replace("/", os.sep))
        os.makedirs(backup, exist_ok=True)
        for f in glob.glob(os.path.join(folder, "*.tsv")):
            shutil.copy2(f, os.path.join(backup, os.path.basename(f)))
        for chunk, seq, old, new, verdict, note in items:
            path = os.path.join(folder, chunk)
            for r in iter_rows(args.tl_dir):
                if r["kind"] == kind and r["chunk"] == chunk and r["seq"] == seq:
                    parts = list(r["parts"])
                    parts[cfg["tcol"]] = new
                    write_row(path, r["line"], parts)
                    break
        print("写回 %d 行 (%s), 备份 -> %s" % (len(items), kind, backup))
    if args.build:
        return build(args)
    return 0


def build(args):
    """调用 tl_tool.py 重新生成 game/tl/chinese/*.rpy。"""
    tl_tool = os.path.join(HERE, "tl_tool.py")
    if not os.path.isfile(tl_tool):
        tl_tool = os.path.join(args.tl_dir, "tl_tool.py")
    cmd = [sys.executable, tl_tool, "build", "--tl-dir", args.tl_dir]
    if args.game_root:
        cmd += ["--game-root", args.game_root]
    print("执行:", " ".join(cmd))
    rc = subprocess.call(cmd)
    if rc == 0 and args.game_root:
        print('重新编译游戏: WindsofChange.exe "%s" compile' % args.game_root)
    return rc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tl-dir", default=TL_DEFAULT, help="tl_work 目录")
    sub = ap.add_subparsers(dest="cmd")

    st = sub.add_parser("stats"); st.set_defaults(fn=cmd_stats)
    sc = sub.add_parser("scan"); sc.add_argument("--show", type=int, default=6); sc.set_defaults(fn=cmd_scan)
    ex = sub.add_parser("export"); ex.set_defaults(fn=cmd_export)
    tm = sub.add_parser("terms")
    tm.add_argument("--rule", help="只处理某条规则 (英文词)")
    tm.add_argument("--apply", action="store_true", help="真正写回 chunks")
    tm.add_argument("--build", action="store_true", help="写回后重新 build")
    tm.add_argument("--game-root", help="游戏根目录")
    tm.add_argument("--show", type=int, default=12)
    tm.set_defaults(fn=cmd_terms)
    rg = sub.add_parser("register")
    rg.add_argument("--show", type=int, default=6)
    rg.set_defaults(fn=cmd_register)
    dd = sub.add_parser("dedupe")
    dd.add_argument("--apply", action="store_true")
    dd.add_argument("--build", action="store_true")
    dd.add_argument("--game-root")
    dd.add_argument("--show", type=int, default=6)
    dd.set_defaults(fn=cmd_dedupe)
    ch = sub.add_parser("chars"); ch.set_defaults(fn=cmd_chars)
    wl = sub.add_parser("worklist"); wl.add_argument("--show", type=int, default=8); wl.set_defaults(fn=cmd_worklist)
    mk = sub.add_parser("mark")
    mk.add_argument("chunk")
    mk.add_argument("status", choices=["未开始", "进行中", "已完成", "待确认"])
    mk.add_argument("--reviewer"); mk.add_argument("--note")
    mk.set_defaults(fn=cmd_mark)
    ap_ = sub.add_parser("apply")
    ap_.add_argument("--sheet", help="指定清单文件 (默认 review/sheet_*.tsv)")
    ap_.add_argument("--write", action="store_true", help="真正写回 chunks")
    ap_.add_argument("--build", action="store_true")
    ap_.add_argument("--game-root")
    ap_.add_argument("--show", type=int, default=10)
    ap_.set_defaults(fn=cmd_apply)

    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return 1
    args.tl_dir = os.path.abspath(args.tl_dir)
    if not os.path.isdir(args.tl_dir):
        sys.exit("tl_work 目录不存在: " + args.tl_dir)
    return args.fn(args) or 0


if __name__ == "__main__":
    sys.exit(main())
