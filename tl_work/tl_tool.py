"""Round-trip tooling for the Winds of Change Chinese translation.

Layout
------
<gameroot>/tl_work/
    tl_tool.py                this script
    template/                 frozen engine-generated skeleton (.rpy)
    chunks/dialogue/*.tsv     editable translation chunks (dialogue)
    chunks/strings/*.tsv      editable translation chunks (UI / choice strings)

Usage
-----
    python tl_tool.py extract [--chunk-size N] [--force]
    python tl_tool.py build
    python tl_tool.py status

Editing
-------
Each TSV row is one line of dialogue.  Columns:

    dialogue : seq  block  idx  speaker  source  target
    strings  : seq  file   key  target

Only the last column (`target`) is meant to be edited.  `source` is the
original English kept for reference.  Keep the literal escapes `\\\\n` and the
text tags `{w}`, `{i}`, `[name]`, etc.  An empty `target` falls back to English.

After editing run `build`, then recompile the game:

    WindsofChange.exe <gameroot> compile
"""

import io
import os
import re
import sys
import glob
import shutil
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
GAMEROOT = os.path.dirname(HERE)
TL_DIR = os.path.join(GAMEROOT, "game", "tl", "chinese")
WORK = os.path.join(HERE)
TEMPLATE = os.path.join(WORK, "template")
CHUNK_DIALOGUE = os.path.join(WORK, "chunks", "dialogue")
CHUNK_STRINGS = os.path.join(WORK, "chunks", "strings")
TARGETS_DIALOGUE = os.path.join(WORK, "targets", "dialogue")
TARGETS_STRINGS = os.path.join(WORK, "targets", "strings")

FILES = ["script", "screens", "options", "common"]

BLOCK_RE = re.compile(r"^translate\s+chinese\s+(\S+):\s*$")
IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")

# Statement keywords that carry a quoted argument but are not translatable.
NON_TRANSLATABLE = {
    "voice", "play", "queue", "stop", "show", "hide", "scene", "pause",
    "window", "with", "nvl", "image", "define", "default", "jump", "call",
    "set",
}


def read_text(path):
    return io.open(path, encoding="utf-8-sig").read()


def write_text(path, text):
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(path, "w", encoding="utf-8-sig", newline="\n").write(text)


def find_literal(line, start=0):
    """Return (quote_index, inner, end_index) for the first quoted literal."""
    i = line.find('"', start)
    if i < 0:
        return None
    j = i + 1
    while j < len(line):
        c = line[j]
        if c == "\\":
            j += 2
            continue
        if c == '"':
            return i, line[i + 1:j], j
        j += 1
    return None


def split_say(line):
    """Return (prefix, inner, suffix) if the line is a translatable Say statement."""
    lit = find_literal(line)
    if not lit:
        return None
    qi, inner, end = lit
    prefix = line[:qi]
    suffix = line[end + 1:]
    head = prefix.strip()
    if head == "":
        return prefix, inner, suffix
    if IDENT_RE.match(head) and head not in NON_TRANSLATABLE:
        return prefix, inner, suffix
    return None


def escape_quotes(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            out.append(s[i:i + 2])
            i += 2
            continue
        if c == '"':
            out.append('\\"')
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def flatten(s):
    return s.replace("\t", "\\t").replace("\r", "").replace("\n", "\\n")


def parse_template(name):
    """Parse one skeleton file into (lines, dialogue_entries, string_entries)."""
    path = os.path.join(TEMPLATE, name + ".rpy")
    text = read_text(path)
    lines = text.split("\n")

    blocks = []          # (block_id, header_line_index)
    for i, ln in enumerate(lines):
        m = BLOCK_RE.match(ln)
        if m:
            blocks.append((m.group(1), i))

    dialogue = []
    strings = []

    for bi, (bid, hline) in enumerate(blocks):
        end = blocks[bi + 1][1] if bi + 1 < len(blocks) else len(lines)
        seg = lines[hline + 1:end]
        base = hline + 1

        if bid == "strings":
            key = None
            for k, ln in enumerate(seg):
                s = ln.strip()
                lit = find_literal(s)
                if not lit:
                    continue
                if s.startswith("old "):
                    key = lit[1]
                elif s.startswith("new ") and key is not None:
                    strings.append({
                        "file": name,
                        "key": key,
                        "target": lit[1],
                        "line": base + k,
                    })
                    key = None
            continue

        if bid in ("python", "early"):
            continue

        idx = 0
        comment_inner = None
        for k, ln in enumerate(seg):
            s = ln.strip()
            if s.startswith("#"):
                lit = find_literal(s)
                comment_inner = lit[1] if lit else None
                continue
            if s == "":
                continue
            say = split_say(ln)
            if say is None:
                continue
            prefix, inner, suffix = say
            dialogue.append({
                "block": bid,
                "idx": idx,
                "speaker": prefix.strip(),
                "source": comment_inner if comment_inner is not None else inner,
                "target": inner,
                "line": base + k,
                "prefix": prefix,
                "suffix": suffix,
            })
            idx += 1
            comment_inner = None

    return lines, dialogue, strings


def cmd_extract(args):
    existing = glob.glob(os.path.join(CHUNK_DIALOGUE, "*.tsv"))
    if existing and not args.force:
        print("chunks already exist (%d files). Use --force to regenerate (translations lost)." % len(existing))
        return 1

    if args.force:
        shutil.rmtree(os.path.join(WORK, "chunks"), ignore_errors=True)

    os.makedirs(CHUNK_DIALOGUE, exist_ok=True)
    os.makedirs(CHUNK_STRINGS, exist_ok=True)
    os.makedirs(TEMPLATE, exist_ok=True)

    for name in FILES:
        src = os.path.join(TL_DIR, name + ".rpy")
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(TEMPLATE, name + ".rpy"))

    all_dialogue = []
    all_strings = []
    for name in FILES:
        if not os.path.exists(os.path.join(TEMPLATE, name + ".rpy")):
            continue
        _, d, s = parse_template(name)
        all_dialogue.extend(d)
        all_strings.extend(s)

    size = args.chunk_size
    for ci, start in enumerate(range(0, len(all_dialogue), size)):
        part = all_dialogue[start:start + size]
        out = ["# dialogue chunk %04d  entries %d-%d of %d" %
               (ci + 1, start + 1, start + len(part), len(all_dialogue)),
               "# seq\tblock\tidx\tspeaker\tsource\ttarget"]
        for off, r in enumerate(part):
            out.append("\t".join([
                str(start + off + 1), r["block"], str(r["idx"]), r["speaker"],
                flatten(r["source"]), flatten(r["target"]),
            ]))
        write_text(os.path.join(CHUNK_DIALOGUE, "dialogue_%04d.tsv" % (ci + 1)),
                   "\n".join(out) + "\n")

    for ci, start in enumerate(range(0, len(all_strings), size)):
        part = all_strings[start:start + size]
        out = ["# strings chunk %04d  entries %d-%d of %d" %
               (ci + 1, start + 1, start + len(part), len(all_strings)),
               "# seq\tfile\tkey\ttarget"]
        for off, r in enumerate(part):
            out.append("\t".join([
                str(start + off + 1), r["file"],
                flatten(r["key"]), flatten(r["target"]),
            ]))
        write_text(os.path.join(CHUNK_STRINGS, "strings_%04d.tsv" % (ci + 1)),
                   "\n".join(out) + "\n")

    nd = len(glob.glob(os.path.join(CHUNK_DIALOGUE, "*.tsv")))
    ns = len(glob.glob(os.path.join(CHUNK_STRINGS, "*.tsv")))
    print("template dir :", TEMPLATE)
    print("dialogue     : %d entries -> %d chunk files" % (len(all_dialogue), nd))
    print("strings      : %d entries -> %d chunk files" % (len(all_strings), ns))
    return 0


def load_chunk_rows(folder):
    rows = []
    for path in sorted(glob.glob(os.path.join(folder, "*.tsv"))):
        for ln in read_text(path).split("\n"):
            if not ln or ln.startswith("#"):
                continue
            rows.append(ln.split("\t"))
    return rows


def cmd_build(args):
    dtarget = {}
    for parts in load_chunk_rows(CHUNK_DIALOGUE):
        if len(parts) < 6:
            continue
        try:
            seq = int(parts[0])
        except ValueError:
            continue
        dtarget[seq] = parts[5]

    starget = {}
    for parts in load_chunk_rows(CHUNK_STRINGS):
        if len(parts) < 4:
            continue
        starget[(parts[1], parts[2])] = parts[3]

    total_d = changed_d = 0
    total_s = changed_s = 0

    for name in FILES:
        tpath = os.path.join(TEMPLATE, name + ".rpy")
        if not os.path.exists(tpath):
            continue
        lines, dialogue, strings = parse_template(name)

        for k, r in enumerate(dialogue):
            total_d += 1
            tgt = dtarget.get(k + 1)
            if not tgt:
                continue
            new_line = r["prefix"] + '"' + escape_quotes(tgt) + '"' + r["suffix"]
            if lines[r["line"]] != new_line:
                changed_d += 1
            lines[r["line"]] = new_line

        for r in strings:
            total_s += 1
            tgt = starget.get((r["file"], r["key"]))
            if not tgt:
                continue
            old = lines[r["line"]]
            lit = find_literal(old)
            if not lit:
                continue
            new_line = old[:lit[0] + 1] + escape_quotes(tgt) + old[lit[2]:]
            if new_line != old:
                changed_s += 1
            lines[r["line"]] = new_line

        write_text(os.path.join(TL_DIR, name + ".rpy"), "\n".join(lines))

    print("dialogue : %d changed of %d" % (changed_d, total_d))
    print("strings  : %d changed of %d" % (changed_s, total_s))
    print('recompile: WindsofChange.exe "%s" compile' % GAMEROOT)
    return 0


def cmd_status(args):
    rows = load_chunk_rows(CHUNK_DIALOGUE)
    d_total = len(rows)
    d_done = sum(1 for p in rows if len(p) >= 6 and p[5].strip() and p[5] != p[4])
    srows = load_chunk_rows(CHUNK_STRINGS)
    s_total = len(srows)
    s_done = sum(1 for p in srows if len(p) >= 4 and p[3].strip() and p[3] != p[2])
    print("dialogue : %5d / %5d  (%.1f%%)" % (d_done, d_total, 100.0 * d_done / max(1, d_total)))
    print("strings  : %5d / %5d  (%.1f%%)" % (s_done, s_total, 100.0 * s_done / max(1, s_total)))
    return 0


def apply_group(label, chunk_dir, targets_dir, target_col):
    """Merge every seq->target row found in targets_dir into the chunk files.

    Target files may be split into any number of parts; rows are matched by the
    global `seq` column, so file names do not need to match chunk names.
    """
    tmap = {}
    tfiles = sorted(glob.glob(os.path.join(targets_dir, "*.tsv")))
    for tp in tfiles:
        for ln in read_text(tp).split("\n"):
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if len(parts) >= 2 and parts[0].strip():
                tmap[parts[0].strip()] = parts[1]

    total = 0
    for path in sorted(glob.glob(os.path.join(chunk_dir, "*.tsv"))):
        rows = read_text(path).split("\n")
        n = 0
        for i, ln in enumerate(rows):
            if not ln or ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if len(parts) <= target_col:
                continue
            seq = parts[0].strip()
            if seq in tmap:
                if parts[target_col] != tmap[seq]:
                    n += 1
                parts[target_col] = tmap[seq]
                rows[i] = "\t".join(parts)
        if n:
            write_text(path, "\n".join(rows))
            print("  %s: %d rows" % (os.path.basename(path), n))
        total += n

    if tfiles:
        done_dir = os.path.join(targets_dir, "done")
        os.makedirs(done_dir, exist_ok=True)
        for tp in tfiles:
            shutil.move(tp, os.path.join(done_dir, os.path.basename(tp)))

    print("%s: applied %d rows" % (label, total))
    return total


def cmd_apply(args):
    apply_group("dialogue", CHUNK_DIALOGUE, TARGETS_DIALOGUE, 5)
    apply_group("strings", CHUNK_STRINGS, TARGETS_STRINGS, 3)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    ex = sub.add_parser("extract")
    ex.add_argument("--chunk-size", type=int, default=400)
    ex.add_argument("--force", action="store_true")
    sub.add_parser("apply")
    sub.add_parser("build")
    sub.add_parser("status")
    args = ap.parse_args()
    if args.cmd == "extract":
        return cmd_extract(args)
    if args.cmd == "apply":
        return cmd_apply(args)
    if args.cmd == "build":
        return cmd_build(args)
    if args.cmd == "status":
        return cmd_status(args)
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
