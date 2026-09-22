# Winds of Change 中文补丁

把《Winds of Change》的中文翻译（含改过的图片、对话框、语言切换与标题粒子）打包成一个可独立安装、可完整还原的补丁项目。

- 补丁版本：1.1.0（构建于 2026-09-22）
- 适用游戏：Steam《Winds of Change》(appid 594130)，基线 `game/script.rpy` sha256 已写入 `manifest.json`
- 引擎兼容：Ren'Py 7.1.1（PC 现状）与 Ren'Py 8.6.0（安卓构建现状）均可，见下节

## 快速开始

Windows 下双击：

| 文件 | 作用 |
| --- | --- |
| `安装补丁.cmd` | 备份原文件并安装 |
| `卸载补丁.cmd` | 从备份还原并清除新增文件 |
| `检查补丁.cmd` | 体检：引擎版本、文件完整性、与安卓工程的同步状态 |

命令行等价形式（纯标准库，Python 3.8+）：

```
python tools/patch_tool.py install    [--game-dir PATH] [--force] [--backup-dir PATH]
python tools/patch_tool.py uninstall  [--game-dir PATH] [--force] [--keep-backup]
python tools/patch_tool.py verify     [--game-dir PATH]
python tools/patch_tool.py check      [--game-dir PATH] [--android-dir PATH] [--no-android]
python tools/patch_tool.py backup     [--game-dir PATH]
python tools/patch_tool.py find
python tools/fetch_renpy_sdk.py --list
```

不加 `--game-dir` 时会自动扫描 Steam 库和注册表定位游戏。

## 目录结构

```
payload/game/     补丁内容：56 个修改文件 + 16 个新增文件
tools/            patch_tool.py（安装器）、fetch_renpy_sdk.py（引擎依赖获取）
deps/             renpy.json（引擎版本、下载地址、sha256；不含二进制）
docs/             renpy8-migration.md（Ren'Py 8 迁移现状与注意事项）
manifest.json     文件清单：路径、类型、双方 sha256、基线校验、编译版本
originals/game/   原版文件副本，仅本地保留，不入仓库
```

## 备份机制（不依赖 originals）

安装时，会先把游戏目录内即将被覆盖的 56 个原文件复制到 `<游戏目录>/woc_zh_patch_backup/`，再写入补丁内容。卸载时优先从这个备份还原，因此：

- 补丁包被删除或移动后，依然可以完整还原；
- 仓库里不需要分发游戏原文件（`originals/` 只在本地作为兜底，已被 `.gitignore` 排除）；
- 安装后你自己改动过的文件，卸载时会跳过而不是覆盖（会打印跳过原因）；
- 卸载默认删除备份目录，加 `--keep-backup` 可保留。

还原准确性已做过验证：在仿造的干净游戏目录上安装再卸载，56 个文件与原版逐字节一致。

彻底兜底：Steam → 游戏属性 → 已安装文件 → 验证游戏文件完整性。

## 引擎版本兼容（Ren'Py 7 / 8）

`patch_tool.py` 会读取 `renpy/vc_version.py`、`renpy/__init__.py` 或 `log.txt` 判断引擎版本，并据此决定 `.rpyc` 的处理方式：

- `payload` 里每个 `.rpyc` 都有配套的 `.rpy`（`check` 会核对这一点）；
- `.rpyc` 由 PC 端 Ren'Py 7.1.1（Python 2）编译，记录在 `manifest.json` 的 `compiled_with`；
- 目标引擎主版本与编译版本不同时，安装器**跳过 `.rpyc`**，只放 `.rpy`，由引擎在首次启动时自行编译（首次启动稍慢，属正常）；
- 引擎主版本相同时照常投放 `.rpyc`，启动最快；
- `verify` 会读取安装状态，不会把被跳过的 `.rpyc` 误报为缺失。

`check` 还会扫描补丁内 `.rpy` 的 Python 块，报告 Python 2 专有写法（`.iteritems()`、`has_key()`、`print` 语句等）。当前结果：未发现。

## 与安卓工程的关系

安卓包在 `C:/renpy8/renpy-8.6.0-sdk/winds-of-change` 上构建（Ren'Py 8.6.0，Python 3.12）。`check` 会把 `payload` 与该工程逐文件比对：

- 源文件（`.rpy`、图片等）必须一致，不一致会计为问题；
- `.rpyc` 差异属正常（两边引擎的 Python 版本不同，各自编译），只提示不计错。

最近一次核对结果：源文件一致 64，分叉 0，缺失 0，`.rpyc` 编译产物差异 8（正常）。

## 依赖

引擎二进制不入库，改由 `deps/renpy.json` 固定版本与校验和，`tools/fetch_renpy_sdk.py` 负责下载或校验：

```
python tools/fetch_renpy_sdk.py --list                                  # 查看清单
python tools/fetch_renpy_sdk.py --local C:/renpy8/renpy-8.6.0-sdk.zip   # 校验本地已有包并登记
python tools/fetch_renpy_sdk.py                                         # 下载并解包
```

清单内容：安卓构建实际使用的 8.6.0.25112108（master 预发布快照，来自 renpy.org/dl/8.6.0/）、当前官方稳定版 8.5.3.26051504（来自 GitHub release，sha256 取自官方 `checksums.txt`），以及对应的 RAPT 包。JDK 需求：Ren'Py 8 的 RAPT 需要 JDK 17+，本机为 `C:/renpy-android/jdk-21.0.12.1+1`。

## 更新流程

1. 在 `tl_work/` 里改翻译，`python tl_tool.py build` 生成 `game/tl/chinese/*.rpy`；
2. 用游戏自带引擎重新编译：`WindsofChange.exe <游戏根目录> compile`；
3. 重跑构建脚本刷新 `payload/`、`manifest.json`；
4. `python tools/patch_tool.py check` 体检，通过后打包发布，并同步安卓工程。

## 说明

游戏本体、美术与音频版权归原开发者所有。本仓库只包含汉化改动内容与安装工具，不含游戏原始文件；引擎依赖需使用者按 `deps/renpy.json` 自行获取（Ren'Py 为 MIT 许可）。
