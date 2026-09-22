# -*- coding: utf-8 -*-
"""按 deps/renpy.json 获取并校验 Ren'Py 引擎依赖 (纯标准库, 无需联网也能用 --local)。

仓库内不包含引擎二进制: 体积大, 且应由使用者从官方渠道获取。
本脚本把这件事变成一条可复现、可校验的命令。

用法:
  python fetch_renpy_sdk.py --list
  python fetch_renpy_sdk.py --local C:/renpy8/renpy-8.6.0-sdk.zip     # 校验本地已有包并登记
  python fetch_renpy_sdk.py                                            # 下载并解包安卓构建用 SDK
  python fetch_renpy_sdk.py --channel stable --artifact renpy-8.5.3-sdk.zip
  python fetch_renpy_sdk.py --artifact renpy-8.6.0-rapt.zip --no-extract
"""
import argparse, hashlib, io, json, os, sys, time, urllib.request, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEPS = os.path.join(ROOT, "deps")
DOWN = os.path.join(DEPS, "downloads")
LOCK = os.path.join(DEPS, "renpy.lock.json")


def load_spec():
    p = os.path.join(DEPS, "renpy.json")
    if not os.path.isfile(p):
        sys.exit("找不到 deps/renpy.json")
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def human(n):
    n = float(n)
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return "%.1f %s" % (n, u)
        n /= 1024.0
    return "%.1f TB" % n


def pick(spec, name=None, channel=None):
    arts = spec["artifacts"]
    if name:
        a = next((x for x in arts if x["name"] == name), None)
        if not a:
            sys.exit("清单里没有 %s, 用 --list 查看" % name)
        return a
    ch = channel or "android-build"
    cands = [x for x in arts if x.get("channel") == ch and x["name"].endswith("-sdk.zip")]
    if not cands:
        sys.exit("channel=%s 下没有默认 SDK 构件, 请用 --artifact 指定" % ch)
    return cands[0]


def download(url, dst, want, want_size=None):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isfile(dst) and sha256(dst) == want:
        print("已存在且校验通过:", os.path.basename(dst))
        return True
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (woc-patch-fetch)"})
    print("下载:", url)
    t0 = time.time()
    got = 0
    try:
        with urllib.request.urlopen(req, timeout=120) as r, open(dst + ".part", "wb") as f:
            total = r.headers.get("Content-Length")
            total = int(total) if total and str(total).isdigit() else want_size
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                f.write(b)
                got += len(b)
                msg = ("  %s / %s (%.0f%%)" % (human(got), human(total), got * 100.0 / total)) if total else ("  %s" % human(got))
                sys.stdout.write("\r" + msg)
                sys.stdout.flush()
    except Exception as e:
        print("")
        print("下载失败:", e)
        print("可手动从官方地址下载后用 --local 登记:", url)
        return False
    print("")
    os.replace(dst + ".part", dst)
    return verify(dst, want)


def verify(path, want):
    h = sha256(path)
    if h != want:
        print("校验失败! 期望 %s" % want)
        print("          实际 %s" % h)
        print("文件保留在 %s" % path)
        return False
    print("sha256 校验通过:", h)
    return True


def extract(zpath, destdir):
    os.makedirs(destdir, exist_ok=True)
    print("解包到:", destdir)
    with zipfile.ZipFile(zpath) as z:
        bad = z.testzip()
        if bad:
            sys.exit("压缩包损坏: " + str(bad))
        z.extractall(destdir)
    print("解包完成:", len(os.listdir(destdir)), "个顶层条目")


def write_lock(spec, art, path):
    lock = {}
    if os.path.isfile(LOCK):
        try:
            with io.open(LOCK, encoding="utf-8") as f:
                lock = json.load(f)
        except Exception:
            lock = {}
    lock[art["name"]] = {"version": art.get("version"), "channel": art.get("channel"),
                         "sha256": art["sha256"], "size": os.path.getsize(path),
                         "url": art.get("url"),
                         "path": os.path.relpath(path, ROOT).replace(os.sep, "/"),
                         "registered_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    with io.open(LOCK, "w", encoding="utf-8", newline="\n") as f:
        json.dump(lock, f, ensure_ascii=False, indent=2)
    print("已登记到 deps/renpy.lock.json")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--artifact", help="构件名, 如 renpy-8.6.0-sdk.zip")
    ap.add_argument("--channel", choices=["android-build", "stable"], help="按渠道选默认 SDK")
    ap.add_argument("--local", help="不下载, 直接校验并登记这个本地 zip")
    ap.add_argument("--no-extract", action="store_true", help="只校验, 不解包")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    spec = load_spec()
    if args.list:
        cur = spec.get("current", {})
        for k in ("pc_steam_copy", "android_build", "android_legacy_sdk"):
            if k in cur:
                print("%-20s Ren'Py %-18s Python %s" % (k, cur[k].get("engine"), cur[k].get("python")))
        print("")
        for a in spec["artifacts"]:
            print("  [%s] %-24s %s" % (a.get("channel"), a["name"], a.get("role", "")))
            print("      %s" % a.get("url"))
            print("      sha256 %s" % a.get("sha256"))
        return 0

    art = pick(spec, args.artifact, args.channel)
    if not art.get("sha256"):
        sys.exit("%s 缺少 sha256, 拒绝使用 (请先更新 deps/renpy.json)" % art["name"])

    if args.local:
        path = os.path.abspath(args.local)
        if not os.path.isfile(path):
            sys.exit("本地文件不存在: " + path)
        print("校验本地包:", path, human(os.path.getsize(path)))
        if not verify(path, art["sha256"]):
            return 1
    else:
        path = art.get("local_copy")
        if path and os.path.isfile(path):
            print("清单里记录了本地副本:", path)
            if not verify(path, art["sha256"]):
                return 1
        else:
            path = os.path.join(DOWN, art["name"])
            if not download(art["url"], path, art["sha256"], art.get("size")):
                return 1

    if not args.no_extract and zipfile.is_zipfile(path):
        stem = art["name"][:-4] if art["name"].endswith(".zip") else art["name"]
        extract(path, os.path.join(DEPS, stem))
    write_lock(spec, art, path)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
