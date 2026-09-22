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
