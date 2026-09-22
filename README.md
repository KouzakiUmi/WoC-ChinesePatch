# Winds of Change 中文补丁

把《Winds of Change》的中文翻译（含改过的图片、语言切换与标题粒子）打包成一个可独立安装、可完整还原的补丁项目。

**本补丁只面向 PC（Steam）版游戏。**

- 补丁版本：1.1.1（构建于 2026-09-22）
- 适用游戏：Steam《Winds of Change》(appid 594130)，基线 `game/script.rpy` sha256 已写入 `manifest.json`
- 引擎兼容：Ren'Py 7.1.1（PC 现状）与 Ren'Py 8.6.0（安卓构建现状）均可，见下节

## 快速开始

Windows 下双击：

| 文件 | 作用 |
| --- | --- |
| `安装补丁.cmd` | 备份原文件并安装 |
| `卸载补丁.cmd` | 从备份还原并清除新增文件 |
| `检查补丁.cmd` | 体检：引擎版本、payload 完整性、`.rpyc`/`.rpy` 配对、Python 2 残留 |

命令行等价形式（纯标准库，Python 3.8+）：

```
python tools/patch_tool.py install    [--game-dir PATH] [--force] [--backup-dir PATH]
python tools/patch_tool.py uninstall  [--game-dir PATH] [--force] [--keep-backup]
python tools/patch_tool.py verify     [--game-dir PATH]
python tools/patch_tool.py check      [--game-dir PATH] [--android]   # --android 为维护者选项
python tools/patch_tool.py backup     [--game-dir PATH]
python tools/patch_tool.py find
python tools/fetch_renpy_sdk.py --list
```

不加 `--game-dir` 时会自动扫描 Steam 库和注册表定位游戏。

## 目录结构

```
payload/game/     补丁内容：54 个修改文件 + 16 个新增文件
tools/            patch_tool.py（安装器）、fetch_renpy_sdk.py（维护者用）
deps/             renpy.json（维护者用：引擎版本、下载地址、sha256；不含二进制）
docs/             renpy8-migration.md（维护者用：个人安卓构建笔记）
manifest.json     文件清单：路径、类型、双方 sha256、基线校验、编译版本
tl_work/          翻译审查工作区（分块 TSV、tl_tool.py）；仅本地使用，不入仓库
originals/game/   原版文件副本，仅本地保留，不入仓库
```

## 备份机制（不依赖 originals）

安装时，会先把游戏目录内即将被覆盖的 54 个原文件复制到 `<游戏目录>/woc_zh_patch_backup/`，再写入补丁内容。卸载时优先从这个备份还原，因此：

- 补丁包被删除或移动后，依然可以完整还原；
- 仓库里不需要分发游戏原文件（`originals/` 只在本地作为兜底，已被 `.gitignore` 排除）；
- 安装后你自己改动过的文件，卸载时会跳过而不是覆盖（会打印跳过原因）；
- 卸载默认删除备份目录，加 `--keep-backup` 可保留。

还原准确性已做过验证：在仿造的干净游戏目录上安装再卸载，54 个文件与原版逐字节一致。

彻底兜底：Steam → 游戏属性 → 已安装文件 → 验证游戏文件完整性。

## 引擎版本兼容（Ren'Py 7 / 8）

`patch_tool.py` 会读取 `renpy/vc_version.py`、`renpy/__init__.py` 或 `log.txt` 判断引擎版本，并据此决定 `.rpyc` 的处理方式：

- `payload` 里每个 `.rpyc` 都有配套的 `.rpy`（`check` 会核对这一点）；
- `.rpyc` 由 PC 端 Ren'Py 7.1.1（Python 2）编译，记录在 `manifest.json` 的 `compiled_with`；
- 目标引擎主版本与编译版本不同时，安装器**跳过 `.rpyc`**，只放 `.rpy`，由引擎在首次启动时自行编译（首次启动稍慢，属正常）；
- 引擎主版本相同时照常投放 `.rpyc`，启动最快；
- `verify` 会读取安装状态，不会把被跳过的 `.rpyc` 误报为缺失。

`check` 还会扫描补丁内 `.rpy` 的 Python 块，报告 Python 2 专有写法（`.iteritems()`、`has_key()`、`print` 语句等）。当前结果：未发现。

## 引擎版本兼容

安装器会读取引擎版本（`renpy/vc_version.py`、`renpy/__init__.py` 或 `log.txt`）。`.rpyc` 由 PC 端 Ren'Py 7.1.1（Python 2）编译，版本记录在 `manifest.json` 的 `compiled_with`；如果目标引擎主版本不同，安装器会跳过 `.rpyc`，只放 `.rpy`，由引擎在首次启动时自行编译。因此即使将来游戏本体升级引擎，补丁也不会因为 `.rpyc` 失效而打不开。

## 维护者部分（不属于 PC 分发包）

仓库里另有两项只供维护者本地使用，发布 zip 中不包含：

- `deps/renpy.json` + `tools/fetch_renpy_sdk.py`：引擎依赖清单与获取脚本，固定了版本、官方下载地址与 sha256（引擎二进制不入库）。
- `docs/renpy8-migration.md`：Ren'Py 8 相关的个人安卓构建环境笔记。

`patch_tool.py check` 默认只做 PC 侧体检；需要核对个人安卓工程时显式加 `--android` 或 `--android-dir PATH`。

## 更新流程

1. 在本地 `tl_work/`（不入仓库）里改翻译，`python tl_tool.py build` 生成 `game/tl/chinese/*.rpy`；
2. 用游戏自带引擎重新编译：`WindsofChange.exe <游戏根目录> compile`；
3. 重跑构建脚本刷新 `payload/`、`manifest.json`；
4. `python tools/patch_tool.py check` 体检，通过后打包发布，并同步安卓工程。

## 变更记录

- **1.1.1** 移除 `game/gui/textbox.png` 与 `game/gui/phone/textbox.png`：这是一次无效替换，两个不同尺寸的原图被写成了同一张图。`tl_work/` 改为仅本地保留、不入仓库。
- **1.1.0** 改为备份式安装/卸载（不再分发游戏原文件）；识别引擎版本并按需跳过 `.rpyc`；新增 `check` 体检与 `deps/renpy.json` 依赖清单；`.gitattributes` 关闭换行转换。

## 说明

游戏本体、美术与音频版权归原开发者所有。本仓库只包含汉化改动内容与安装工具，不含游戏原始文件；引擎依赖需使用者按 `deps/renpy.json` 自行获取（Ren'Py 为 MIT 许可）。
