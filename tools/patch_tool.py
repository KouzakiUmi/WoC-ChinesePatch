# -*- coding: utf-8 -*-
"""Winds of Change 中文补丁安装器 (纯标准库, Python 3.8+)

用法:
  python patch_tool.py install [--game-dir PATH] [--force]
  python patch_tool.py uninstall [--game-dir PATH] [--force]
  python patch_tool.py verify [--game-dir PATH]
  python patch_tool.py backup [--game-dir PATH] [--backup-dir PATH]
  python patch_tool.py find

安装:  先把游戏内将被覆盖的原文件备份到 <游戏目录>/woc_zh_patch_backup/,
       再复制 payload/ 中的文件; 安装状态写入 game/woc_zh_patch.json
卸载:  modified 文件优先用备份还原 (无备份时回退到随包的 originals/),
       new 文件删除, 并清理对应 .rpyc 与 game/cache
备份:  不安装, 只单独执行一次原文件备份
"""
import argparse, hashlib, io, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
# PyInstaller --onefile extracts bundled data beside sys._MEIPASS. In a source
# checkout this remains the repository root above tools/.
ROOT = getattr(sys, "_MEIPASS", os.path.dirname(HERE))
STATE_NAME = "woc_zh_patch.json"
BACKUP_DIRNAME = "woc_zh_patch_backup"
CACHE_DIRS = ("game/cache", "game/saves/../cache")


def _read_ver(path):
    try:
        return io.open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


def _eng(version, source, script_version=None):
    return {"version": version, "source": source,
            "script_version": script_version}


def detect_engine(game):
    """读取游戏引擎版本, 返回 dict(version, source, script_version) 或 None。

    读取 PC 版 Ren'Py 7.1.1 的 version_tuple 与 vc_version。
    """
    def dotted(s):
        return bool(s) and s[0].isdigit() and "." in s

    vc = _read_ver(os.path.join(game, "renpy", "vc_version.py"))
    ini = _read_ver(os.path.join(game, "renpy", "__init__.py"))

    # version_tuple = (7, 1, 1, vc_version) + vc_version = 929
    vcnum = None
    for line in vc.splitlines():
        s = line.strip()
        if s.startswith("vc_version") and "=" in s:
            t = s.split("=", 1)[1].strip()
            if t.isdigit():
                vcnum = t
    sv = None
    for line in ini.splitlines():
        s = line.strip()
        if s.startswith("script_version") and "=" in s:
            t = s.split("=", 1)[1].strip()
            if t.isdigit():
                sv = int(t)
        if s.startswith("version_tuple") and "(" in s and ")" in s:
            body = s[s.index("(") + 1:s.index(")")]
            parts = [t.strip() for t in body.split(",")]
            nums = [t for t in parts if t.isdigit()]
            if nums:
                v = ".".join(nums)
                if any(t == "vc_version" for t in parts) and vcnum:
                    v = v + "." + vcnum
                return _eng(v, "renpy/__init__.py", sv)

    # log.txt fallback
    p = os.path.join(game, "log.txt")
    if os.path.isfile(p):
        for line in _read_ver(p).splitlines():
            if "Py " in line:
                for tok in line.split():
                    if dotted(tok.strip()):
                        return _eng(tok.strip(), "log.txt", sv)
    if sv:
        return _eng("unknown", "renpy/__init__.py", sv)
    return None


def engine_label(game):
    e = detect_engine(game)
    if not e:
        return "未知 (找不到 renpy 版本信息)", None
    return "Ren'Py %s" % e["version"], e


def rpyc_orphans(man):
    """列出没有配套 .rpy 的 .rpyc。
    源码配对可在清缓存或编译文件失效后重新生成字节码。"""
    paths = set(e["path"] for e in man["files"])
    return sorted(c for c in paths if c.endswith(".rpyc") and c[:-1] not in paths)


def backup_dir_for(game, override=None):
    """备份目录: 默认放在游戏根目录下, 跟随游戏安装走, 补丁包被删也能还原。"""
    if override:
        return os.path.abspath(override)
    return os.path.join(game, BACKUP_DIRNAME)


def read_state(sp):
    try:
        with io.open(sp, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def backup_one(bdir, rel, src_file):
    """把游戏里的原文件复制进备份目录, 保留相对路径。已备份过则跳过。"""
    bp = os.path.join(bdir, rel)
    if os.path.isfile(bp):
        return bp, False
    os.makedirs(os.path.dirname(bp), exist_ok=True)
    shutil.copy2(src_file, bp)
    return bp, True

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def load_manifest():
    with open(os.path.join(ROOT, "manifest.json"), encoding="utf-8") as f:
        return json.load(f)

def check_game_dir(path):
    if not os.path.isdir(path):
        return "目录不存在"
    if not os.path.isfile(os.path.join(path, "WindsofChange.exe")):
        return "找不到 WindsofChange.exe (不是游戏根目录)"
    if not os.path.isfile(os.path.join(path, "game", "script.rpy")):
        return "找不到 game/script.rpy"
    return None

def find_game():
    cands = []
    for lib in (r"C:\Program Files (x86)\Steam\steamapps", r"C:\SteamLibrary\steamapps",
                r"D:\SteamLibrary\steamapps", r"D:\Steam\steamapps", r"E:\SteamLibrary\steamapps"):
        vdf = os.path.join(lib, "libraryfolders.vdf")
        roots = [lib]
        if os.path.isfile(vdf):
            import re
            txt = open(vdf, encoding="utf-8", errors="ignore").read()
            roots += re.findall(r'"path"\s+"([^"]+)"', txt)
        for r in roots:
            g = os.path.join(r, "steamapps" if not r.lower().endswith("steamapps") else "", "common", "winds-of-change")
            g = os.path.normpath(g)
            if g not in cands:
                cands.append(g)
    # 也检查注册表 Steam Path
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
        sp = winreg.QueryValueEx(k, "InstallPath")[0]
        g = os.path.join(sp, "steamapps", "common", "winds-of-change")
        if g not in cands:
            cands.append(g)
    except Exception:
        pass
    ok = [c for c in cands if not check_game_dir(c)]
    return ok

def state_path(game):
    return os.path.join(game, "game", STATE_NAME)

def cmd_find(args):
    ok = find_game()
    if not ok:
        print("未自动找到游戏目录。请用 --game-dir 指定 (游戏根目录, 含 WindsofChange.exe)。")
        return 1
    for g in ok:
        print("找到:", g)
    return 0

def resolve_game(args, need_state=False):
    if args.game_dir:
        game = os.path.abspath(args.game_dir)
    else:
        ok = find_game()
        if not ok:
            sys.exit("未找到游戏目录, 请用 --game-dir 指定。")
        game = ok[0]
        if len(ok) > 1:
            print("提示: 找到多个安装, 使用第一个:", game)
    err = check_game_dir(game)
    if err:
        sys.exit("游戏目录无效 (%s): %s" % (game, err))
    print("游戏目录:", game)
    return game

def do_install(args):
    game = resolve_game(args)
    man = load_manifest()
    sp = state_path(game)
    if os.path.isfile(sp) and not args.force:
        sys.exit("检测到补丁已安装 (game/%s)。如需覆盖安装请加 --force。" % STATE_NAME)

    # 基线校验
    bc = man.get("base_check")
    if bc:
        p = os.path.join(game, bc["path"].replace("/", os.sep))
        if os.path.isfile(p):
            h = sha256(p)
            if h != bc["sha256"]:
                msg = ("警告: %s 与本补丁构建时的基线不一致 (游戏版本可能不同或已被其他补丁修改)。\n"
                       "继续安装可能覆盖他人修改。加 --force 强制安装。" % bc["path"])
                if not args.force:
                    sys.exit(msg)
                print(msg)

    label, eng = engine_label(game)
    print("游戏引擎:", label)
    cw = man.get("compiled_with") or {}
    if not eng or eng.get("version") != cw.get("engine"):
        sys.exit("本补丁只适用于 Ren'Py %s PC 版。" % cw.get("engine", "7.1.1.929"))
    orphan = rpyc_orphans(man)
    if orphan:
        print("警告: %d 个 .rpyc 没有配套 .rpy:" % len(orphan))
        for o in orphan:
            print("   ", o)

    bdir = backup_dir_for(game, getattr(args, "backup_dir", None))
    n_new = n_mod = n_bak = 0
    backed = []
    total = len(man["files"])
    for index, e in enumerate(man["files"], 1):
        rel = e["path"].replace("/", os.sep)
        src = os.path.join(ROOT, "payload", rel)
        dst = os.path.join(game, rel)
        if not os.path.isfile(src):
            sys.exit("payload 缺失: " + e["path"])
        # payload 与 manifest 一致性校验（防止"源已损坏/清单未同步"就直接写入游戏）
        if sha256(src) != e["sha256"]:
            msg = "payload 与 manifest 不一致: %s（请先修复 payload 或更新 manifest）" % e["path"]
            if not args.force:
                sys.exit(msg)
            print("警告: " + msg)
        # 覆盖前备份游戏内现有文件 (仅 modified 条目, 且不重复备份已打过补丁的内容)
        if e["type"] == "modified" and os.path.isfile(dst):
            cur = sha256(dst)
            if cur != e["sha256"]:
                bp, created = backup_one(bdir, rel, dst)
                backed.append(e["path"])
                if created: n_bak += 1
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print("写入文件 [%d/%d]: %s" % (index, total, e["path"]))
        if e["type"] == "new": n_new += 1
        else: n_mod += 1
    state = {"manifest_version": man["version"], "installed": man["built"],
             "files": len(man["files"]), "backup_dir": bdir,
             "backup_files": sorted(set(backed)),
             "engine": eng}
    with io.open(sp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    print("已备份 %d 个原文件到: %s" % (n_bak, bdir))
    print("安装完成: 修改 %d 个文件, 新增 %d 个文件。" % (n_mod, n_new))
    print("直接启动游戏即为中文。若显示异常, 删除 game/cache 后重试。")
    return 0

def do_uninstall(args):
    game = resolve_game(args)
    man = load_manifest()
    sp = state_path(game)
    if not os.path.isfile(sp) and not args.force:
        sys.exit("未找到安装状态 (game/%s), 该目录可能未安装本补丁。加 --force 仍要卸载请重试。" % STATE_NAME)
    st = read_state(sp)
    bdir = backup_dir_for(game, getattr(args, "backup_dir", None) or st.get("backup_dir"))
    have_backup = os.path.isdir(bdir)
    print("备份目录:", bdir if have_backup else "(未找到, 将回退到随包 originals/)")
    restored = removed = skipped = from_backup = 0
    touched_dirs = set()
    total = len(man["files"])
    for index, e in enumerate(man["files"], 1):
        rel = e["path"].replace("/", os.sep)
        dst = os.path.join(game, rel)
        rpyc = dst + "c"
        if e["type"] == "modified":
            src = os.path.join(bdir, rel)
            used_backup = os.path.isfile(src)
            if not used_backup:
                src = os.path.join(ROOT, "originals", rel)
            if not os.path.isfile(src):
                print("跳过(缺备份且缺原版):", e["path"]); skipped += 1; continue
            cur = sha256(dst) if os.path.isfile(dst) else None
            ok_hashes = [e["sha256"], e["original"]["sha256"], sha256(src)]
            if cur and cur not in ok_hashes:
                print("跳过(文件在安装后被改动过):", e["path"]); skipped += 1; continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            if os.path.isfile(rpyc): os.remove(rpyc)
            restored += 1
            if used_backup: from_backup += 1
        else:
            if os.path.isfile(dst): os.remove(dst); removed += 1
            if os.path.isfile(rpyc): os.remove(rpyc); removed += 1
            touched_dirs.add(os.path.dirname(dst))
        print("卸载检查 [%d/%d]: %s" % (index, total, e["path"]))
    # 删除新增文件后留下的空目录 (只删空的, 从深到浅)
    for d in sorted(touched_dirs, key=lambda x: -len(x)):
        cur = d
        while os.path.isdir(cur) and not os.listdir(cur) and cur != game:
            try:
                os.rmdir(cur)
            except OSError:
                break
            cur = os.path.dirname(cur)

    # 清理缓存目录内容
    cache = os.path.join(game, "game", "cache")
    if os.path.isdir(cache):
        shutil.rmtree(cache, ignore_errors=True)
        print("已清理 game/cache (下次启动自动重建)。")
    if os.path.isfile(sp): os.remove(sp)
    if os.path.isdir(bdir) and not getattr(args, "keep_backup", False):
        shutil.rmtree(bdir, ignore_errors=True)
        print("已删除备份目录。")
    elif os.path.isdir(bdir):
        print("已保留备份目录:", bdir)
    print("卸载完成: 还原 %d (其中来自备份 %d), 删除 %d, 跳过 %d。"
          % (restored, from_backup, removed, skipped))
    return 0


def do_backup(args):
    """只备份, 不安装: 把 manifest 中所有 modified 条目对应的游戏内文件存进备份目录。"""
    game = resolve_game(args)
    man = load_manifest()
    bdir = backup_dir_for(game, getattr(args, "backup_dir", None))
    n_new = n_skip = n_miss = 0
    for e in man["files"]:
        if e["type"] != "modified":
            continue
        rel = e["path"].replace("/", os.sep)
        dst = os.path.join(game, rel)
        if not os.path.isfile(dst):
            print("游戏内缺失, 无法备份:", e["path"]); n_miss += 1; continue
        _, created = backup_one(bdir, rel, dst)
        if created: n_new += 1
        else: n_skip += 1
    print("备份目录:", bdir)
    print("备份完成: 新增 %d, 已存在跳过 %d, 缺失 %d。" % (n_new, n_skip, n_miss))
    return 1 if n_miss else 0

def do_verify(args):
    game = resolve_game(args)
    man = load_manifest()
    bad = ok = 0
    for e in man["files"]:
        rel = e["path"].replace("/", os.sep)
        p = os.path.join(game, rel)
        if not os.path.isfile(p):
            print("缺失:", e["path"]); bad += 1; continue
        if sha256(p) != e["sha256"]:
            print("不一致:", e["path"]); bad += 1; continue
        ok += 1
    total = len(man["files"])
    print("校验完成: %d / %d 个文件正确。" % (ok, total))
    return 1 if bad else 0

def do_check(args):
    """Check the PC payload and its Ren'Py 7.1.1 source/bytecode pairs."""
    man = load_manifest()
    problems = 0
    expected = (man.get("compiled_with") or {}).get("engine")

    if not args.no_game:
        try:
            game = resolve_game(args)
            label, eng = engine_label(game)
            print("Game engine:", label)
            if not eng or eng.get("version") != expected:
                problems += 1
                print("Expected Ren'Py %s." % expected)
        except SystemExit:
            print("Game engine: not found (skipped)")

    orphan = rpyc_orphans(man)
    if orphan:
        problems += len(orphan)
        print(".rpyc without matching .rpy:", len(orphan))
        for path in orphan:
            print("   ", path)
    else:
        print(".rpyc/.rpy pairs: OK")

    missing = [e["path"] for e in man["files"]
               if not os.path.isfile(os.path.join(ROOT, "payload", e["path"].replace("/", os.sep)))]
    if missing:
        problems += len(missing)
        print("Missing payload files:", len(missing))
        for path in missing[:20]:
            print("   ", path)
    else:
        print("Payload files: OK (%d)" % len(man["files"]))

    # payload 完整性: 逐个比对 manifest 记录的 sha256（README 承诺的"payload 完整性"）
    bad_hash = []
    for e in man["files"]:
        p = os.path.join(ROOT, "payload", e["path"].replace("/", os.sep))
        if os.path.isfile(p) and sha256(p) != e["sha256"]:
            bad_hash.append(e["path"])
    if bad_hash:
        problems += len(bad_hash)
        print("Payload hash mismatch: %d" % len(bad_hash))
        for path in bad_hash[:20]:
            print("   ", path)
    else:
        print("Payload hashes: OK (%d)" % len(man["files"]))

    print("Check result:", ("%d problem(s)" % problems) if problems else "OK")
    return 1 if problems else 0

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("install", do_install), ("uninstall", do_uninstall), ("verify", do_verify)):
        s = sub.add_parser(name)
        s.add_argument("--game-dir")
        s.add_argument("--force", action="store_true")
        s.add_argument("--backup-dir", help="备份目录 (默认 <游戏目录>/%s)" % BACKUP_DIRNAME)
        if name == "uninstall":
            s.add_argument("--keep-backup", action="store_true", help="卸载后保留备份目录")
        s.set_defaults(fn=fn)
    b = sub.add_parser("backup")
    b.add_argument("--game-dir")
    b.add_argument("--force", action="store_true")
    b.add_argument("--backup-dir")
    b.set_defaults(fn=do_backup)
    c = sub.add_parser("check")
    c.add_argument("--game-dir")
    c.add_argument("--force", action="store_true")
    c.add_argument("--no-game", action="store_true", help="只检查补丁包本身, 不定位游戏")
    c.set_defaults(fn=do_check)
    f = sub.add_parser("find"); f.set_defaults(fn=cmd_find)
    args = ap.parse_args()
    sys.exit(args.fn(args) or 0)

if __name__ == "__main__":
    main()
