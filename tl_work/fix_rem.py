# -*- coding: utf-8 -*-
"""Fix the 4 remaining audit items."""
import io
import os
import glob

WORK = r"C:\SteamLibrary\steamapps\common\winds-of-change\tl_work"
LQ, RQ = u"\u201c", u"\u201d"
SLQ, SRQ = u"\u2018", u"\u2019"

# 1) trailing lone open-quote rows (delete the stray)
STRIP_OPEN = {
    "strings_0001.tsv": {"99"},
    "strings_0002.tsv": {"420", "425", "444", "466"},
}
# 2) 神像 -> 灵像
IDOL_ROWS = {
    "strings_0001.tsv": {"198", "372"},
    "strings_0002.tsv": {"476", "477", "539", "697", "698"},
    "dialogue_0023.tsv": {"9194"},
}
# 3) half-width single quotes
SQ_ROWS = {"strings_0002.tsv": {"418", "624", "743"}}
SQ_SPECIAL = {"strings_0002.tsv": {"733": (u"'"+u"\u6d41\u4ea1"+u"'"+u"\u7a81\u88ad", u"\u6d41\u4ea1\u7a81\u88ad")}}


def tcol(isstr):
    return 3 if isstr else 5


stats = {}
report = []

for folder, isstr in ((os.path.join(WORK, "chunks", "dialogue"), False),
                      (os.path.join(WORK, "chunks", "strings"), True)):
    col = tcol(isstr)
    for path in sorted(glob.glob(os.path.join(folder, "*.tsv"))):
        name = os.path.basename(path)
        rows = io.open(path, encoding="utf-8-sig").read().split("\n")
        n = 0
        for i, ln in enumerate(rows):
            if not ln or ln.startswith("#"):
                continue
            c = ln.split("\t")
            if len(c) <= col:
                continue
            seq = c[0].strip()
            t = c[col]
            o = t

            # 1) backslash before curly quote (dialogue_0022)
            t = t.replace("\\" + LQ, LQ).replace("\\" + RQ, RQ)
            t = t.replace("\\" + '"', "")

            # 2) trailing lone open quote
            if seq in STRIP_OPEN.get(name, ()) and t.endswith(LQ):
                t = t[:-1].rstrip()

            # 3) 神像 -> 灵像
            if seq in IDOL_ROWS.get(name, ()) and u"\u795e\u50cf" in t:
                t = t.replace(u"\u795e\u50cf", u"\u7075\u50cf")

            # 4) half-width single quotes
            if seq in SQ_ROWS.get(name, ()):
                out = []
                opening = True
                for ch in t:
                    if ch == "'":
                        out.append(SLQ if opening else SRQ)
                        opening = not opening
                    else:
                        out.append(ch)
                t = "".join(out)
            for seq2, (a, b) in SQ_SPECIAL.get(name, {}).items():
                if seq == seq2 and a in t:
                    t = t.replace(a, b)

            if t != o:
                c[col] = t
                rows[i] = "\t".join(c)
                n += 1
                stats[name] = stats.get(name, 0) + 1
        if n:
            io.open(path, "w", encoding="utf-8-sig", newline="\n").write("\n".join(rows))
            report.append("%-22s %d" % (name, n))

print("\n".join(report))
print("STATS:", stats)

# diagnostics: any target ending with a lone open quote?
bad = []
for folder, isstr in ((os.path.join(WORK, "chunks", "dialogue"), False),
                      (os.path.join(WORK, "chunks", "strings"), True)):
    col = tcol(isstr)
    for path in sorted(glob.glob(os.path.join(folder, "*.tsv"))):
        for ln in io.open(path, encoding="utf-8-sig").read().split("\n"):
            if not ln or ln.startswith("#"):
                continue
            c = ln.split("\t")
            if len(c) > col and c[col].rstrip().endswith(LQ):
                bad.append((os.path.basename(path), c[0], c[col][:90]))
print("targets ending with open quote (after fix): %d" % len(bad))
for b in bad[:10]:
    print("   ", b)
