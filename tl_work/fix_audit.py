# -*- coding: utf-8 -*-
"""Apply the audit fixes to tl_work/chunks/**/*.tsv (target columns only)."""
import io
import os
import glob
from collections import defaultdict, Counter

WORK = os.path.dirname(os.path.abspath(__file__))
CAND = r"C:\Users\Fractal\Documents\Codex\2026-09-22\jia\outputs\zh_fix_candidates.tsv"
DIA = os.path.join(WORK, "chunks", "dialogue")
STR = os.path.join(WORK, "chunks", "strings")


def read(p):
    return io.open(p, encoding="utf-8-sig").read().split("\n")


def write(p, rows):
    io.open(p, "w", encoding="utf-8-sig", newline="\n").write("\n".join(rows))


# ---- explicit row edits: file -> seq -> [(old, new), ...] ----
STR_EDITS = {
    "strings_0001.tsv": {
        "3": [("[[Sad]", "[[悲伤]")],
        "4": [("[[Happy]", "[[开心]")],
        "5": [("[[Neutral]", "[[中立]")],
        "9": [("[[Aggressive]", "[[强硬]")],
        "84": [("[[Joking]", "[[玩笑]")],
        "85": [("[[Flirty]", "[[调情]")],
    },
    "strings_0003.tsv": {
        "820": [("View Parallel Chronicle", "查看平行编年史")],
        "831": [("View Parallel Chronicle", "查看平行编年史")],
        "832": [("View Parallel Chronicle", "查看平行编年史")],
        "870": [("View Parallel Chronicle", "查看平行编年史")],
        "871": [("View Parallel Chronicle", "查看平行编年史")],
        "890": [("View Parallel Chronicle", "查看平行编年史")],
        "833": [("Access Sovy Heart-to-Heart", "进入索维的谈心")],
    },
}

DIA_EDITS = {
    "dialogue_0011.tsv": {
        "4110": [("我希望你对他们所有人一视同仁。", "我希望你对他们所有人{i}一视同仁{/i}。")],
        "4171": [("但如果他真的为薇薇安效力", "但如果他{i}真的{/i}为薇薇安效力")],
    },
    "dialogue_0021.tsv": {
        "8192": [("这大大阻碍了社会的进步。", "这{i}大大{/i}阻碍了社会的进步。")],
    },
}

# ---- source-filtered term unification ----
SRC_TERMS = [
    ("idol", [("灵魂灵像", "灵像"), ("灵魂神像", "灵像"), ("神灵像", "灵像"),
              ("灵魂偶像", "灵像"), ("灵偶", "灵像"), ("神像", "灵像")]),
    ("inquisition", [("宗教裁判所", "审判庭"), ("宗教审判庭", "审判庭")]),
    ("monarchy", [("君主团", "王室"), ("君主制", "王室")]),
    ("champion", [("救世主", "斗士"), ("勇士", "斗士"), ("冠军", "斗士")]),
    ("exodus", [("大迁徙", "出埃及")]),
]

# ---- load audit candidates ----
cands = defaultdict(lambda: defaultdict(list))
for line in io.open(CAND, encoding="utf-8-sig").read().split("\n"):
    if not line or line.startswith("#"):
        continue
    p = line.split("\t")
    if len(p) < 8:
        continue
    cands[p[1]][p[2].strip()].append(dict(kind=p[0], col=int(p[3]), find=p[4], repl=p[5]))


def pair_quotes(s):
    out = []
    opening = True
    for ch in s:
        if ch == '"':
            out.append(u"\u201c" if opening else u"\u201d")
            opening = not opening
        else:
            out.append(ch)
    return "".join(out)


def pair_escaped_quotes(s):
    out = []
    opening = True
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s) and s[i + 1] == '"':
            out.append(u"\u201c" if opening else u"\u201d")
            opening = not opening
            i += 2
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


stats = Counter()
report = []

for folder, is_dia in ((DIA, True), (STR, False)):
    tcol = 5 if is_dia else 3
    for path in sorted(glob.glob(os.path.join(folder, "*.tsv"))):
        name = os.path.basename(path)
        rows = read(path)
        n = 0
        for i, ln in enumerate(rows):
            if not ln or ln.startswith("#"):
                continue
            c = ln.split("\t")
            if len(c) <= tcol:
                continue
            seq = c[0].strip()

            # 1) audit candidates
            for cd in cands.get(name, {}).get(seq, []):
                col = cd["col"]
                if col >= len(c):
                    continue
                if cd["kind"] == "quote":
                    newv = pair_quotes(c[col])
                else:
                    if cd["find"] not in c[col]:
                        report.append("MISS %s seq=%s %s->%s" % (name, seq, cd["find"], cd["repl"]))
                        continue
                    newv = c[col].replace(cd["find"], cd["repl"])
                if newv != c[col]:
                    c[col] = newv
                    n += 1
                    stats["cand_" + cd["kind"]] += 1

            # 2) explicit edits
            edits = (DIA_EDITS if is_dia else STR_EDITS).get(name, {}).get(seq)
            if edits:
                for old, new in edits:
                    if old in c[tcol]:
                        c[tcol] = c[tcol].replace(old, new)
                        n += 1
                        stats["explicit"] += 1
                    else:
                        report.append("MISS-EDIT %s seq=%s %r" % (name, seq, old))

            # 3) source-filtered term unification
            if is_dia and len(c) > 5:
                src = c[4].lower()
                for key, subs in SRC_TERMS:
                    if key in src:
                        t = c[5]
                        for a, b in subs:
                            if a in t:
                                t = t.replace(a, b)
                        if t != c[5]:
                            c[5] = t
                            n += 1
                            stats["term_" + key] += 1

            # 4) strings: escaped quotes -> full-width
            if not is_dia and len(c) > 3 and "\\\"" in c[3]:
                t = pair_escaped_quotes(c[3])
                if t != c[3]:
                    c[3] = t
                    n += 1
                    stats["strquote"] += 1

            # 5) trailing spaces
            if c[tcol] != c[tcol].rstrip():
                c[tcol] = c[tcol].rstrip()
                n += 1
                stats["rstrip"] += 1

            rows[i] = "\t".join(c)

        if n:
            write(path, rows)
            report.append("%-24s %d changes" % (name, n))

print("\n".join(report))
print()
print("STATS:", dict(stats))
