# Winds of Change 简体中文补丁

**《Winds of Change》的非营利性中文汉化补丁，仅面向 PC（Steam）版。**

![Status](https://img.shields.io/badge/Status-Stable-success?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=flat-square)
![Engine](https://img.shields.io/badge/Engine-Ren'Py%207.1.1-blueviolet?style=flat-square)
![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey?style=flat-square)

> **By KouzakiUmi (呜咪 / 神前海)**

---

**项目说明**：本补丁覆盖全文对白与旁白、界面文本与 53 张改版图片，走 Ren'Py 原生翻译机制，随包附带独立安装器与校验工具。安装过程会先备份原文件，卸载可逐字节完整还原，因此**补丁包本身不携带游戏原始文件**。

| 项目 | 说明 |
| --- | --- |
| 适用游戏 | Steam《Winds of Change》(appid 594130)，开发商/发行商 **Klace** |
| 游戏引擎 | 仅支持 Ren'Py 7.1.1.929（PC / Steam） |
| 基线校验 | `game/script.rpy` 的 sha256 `c11fbeb67c84...`，不匹配会拒绝安装 |
| 补丁规模 | 68 个文件 = 56 个修改 + 12 个新增（含 53 张改版图片） |
| 当前版本 | v1.3.4：新增无需 Python 的 Windows 单文件图形安装器 |
| 运行要求 | 下载独立 GUI 安装器后无需安装 Python；源码命令行工具需要 Python 3.8+ |

---

## 📥 安装 / 卸载 / 检查

Windows 玩家直接运行发布包中的 `WoC-ChinesePatch.exe`，无需安装 Python。它包含图形界面和完整补丁数据，可安装、卸载、检查与验证，并在窗口内显示逐文件反馈；遇到问题可打开调试日志。

从源码运行时，也可双击仓库根目录的三个 `.cmd` 脚本（需要 Python 3.8+）：

| 脚本 | 作用 |
| --- | --- |
| `安装补丁.cmd` | 备份被覆盖的原文件，然后写入中文补丁 |
| `卸载补丁.cmd` | 从备份完整还原，删除新增文件，清理缓存 |
| `检查补丁.cmd` | 体检：目标引擎版本、文件完整性、`.rpyc`/`.rpy` 配对 |

从 v1.3.2 及更早版本升级时，请先用旧版补丁卸载，再安装 v1.3.4，以清理旧版新增文件。

命令行等价形式（不指定 `--game-dir` 时会自动扫描 Steam 库与注册表定位游戏）：

```cmd
python tools\patch_tool.py install    [--game-dir PATH] [--force] [--backup-dir PATH]
python tools\patch_tool.py uninstall  [--game-dir PATH] [--force] [--keep-backup]
python tools\patch_tool.py verify     [--game-dir PATH]
python tools\patch_tool.py check      [--game-dir PATH]
python tools\patch_tool.py find
```

> 💡 安装后直接启动游戏即为中文。若界面显示异常，删除 `<游戏目录>\game\cache` 后重启即可。

---

## 🎮 安装与还原机制

1. **定位游戏**：扫描 `libraryfolders.vdf` 与注册表，找到 Steam 库中的游戏根目录。
2. **基线校验**：比对 `game/script.rpy` 的 sha256 与 `manifest.json` 记录值。不一致说明游戏版本不同或已被其他补丁修改，安装器会拒绝；确认无碍可用 `--force` 跳过。
3. **先备份再写入**：把将覆盖的 54 个原文件复制到 `<游戏目录>\woc_zh_patch_backup\`，随后写入补丁内容。
4. **还原优先用本地备份**：卸载时从该备份逐字节还原，所以补丁包被移动或删除都不影响还原；仓库无需携带游戏原文件。
5. **保护用户改动**：安装后被你自己改过的文件，卸载时跳过而不是覆盖，并打印原因。
6. **清理**：卸载会清空 `game/cache` 与新增文件留下的空目录；`--keep-backup` 可保留备份目录。

> 💡 兜底方案：Steam → 游戏属性 → 已安装文件 → 验证游戏文件完整性。

---

## 🧩 补丁内容

| 内容 | 说明 |
| --- | --- |
| `game/tl/chinese/` | 全文对白与旁白译文（5 组 `.rpy` + `.rpyc`，对白 10,370 块、界面串 1,253 条） |
| `game/zzz_chinese_language.rpy` | 语言开关 + 界面提示的运行时翻译钩子（见"技术细节"） |
| `game/gui.rpy`、`game/screens.rpy` | 中文字体与界面适配（含存档界面中文标签） |
| `game/images/` | 53 张改版图片：书页笔记、区域地图、教程、爬塔、主菜单等 |

---

## 📁 目录结构

```
payload/game/      补丁内容（68 个文件：56 修改 + 12 新增）
tools/             patch_tool.py 安装器 / review_tool.py 校对工作流 / tl_tool.py 构建
manifest.json      文件清单：路径、类型、双方 sha256、基线校验值、引擎编译版本
docs/              PC 运行环境说明（pc-runtime.md）、校对工作流与角色语气档案
review/            术语表 terms.tsv、润色表 fixups.tsv、预筛报告与校对进度
安装补丁.cmd / 卸载补丁.cmd / 检查补丁.cmd
tl_work/           翻译源（分块 TSV）与构建脚本，仅维护者本地保留
originals/         游戏原文件副本，仅维护者本地保留（无备份时的兜底还原）
```

---

## 🛠️ 技术细节

### 译文如何生效

使用 Ren'Py 原生翻译机制：`game/tl/chinese/` 下的 `translate chinese ...` 块，配合 `zzz_chinese_language.rpy` 里的 `define config.language = "chinese"`，启动即中文，无需玩家手动切换语言。

### 界面提示为什么需要运行时钩子

`renpy.notify(...)` 与 `renpy.input(...)` 接收的是**裸 Python 字符串**。Ren'Py 的翻译提取只覆盖 say 语句、menu 选项与 `_()` 包裹的字符串，函数调用里的普通字符串不会被提取——这类提示（如开场的 `Use Enter or Left Click to advance text.`、取名界面的 `Use keyboard to enter name`）原本始终显示英文。

补丁在自己新增的 `zzz_chinese_language.rpy` 中把这两个函数包了一层，让提示语先经 `renpy.translation.translate_string()` 查字符串表，配套 39 条映射写在同一文件的 `translate chinese strings:` 块里。这样处理**不需要改动任何游戏原始脚本**，卸载时删除该文件即完全还原。

### 引擎版本

补丁只支持 PC / Steam 版 Ren'Py 7.1.1.929。安装器会核对引擎版本和 `game/script.rpy` 基线，不匹配时拒绝安装。随包 `.rpyc` 均由该引擎编译，并与 `.rpy` 配套。

### 校验机制

| 机制 | 作用 |
| --- | --- |
| `manifest.json` | 为每个文件记录 sha256 与类型（modified / new），`verify` 据此核对安装结果 |
| `base_check` | 记录 `game/script.rpy` 的哈希，用于判断游戏基线是否匹配（该文件补丁从不修改） |
| `check` | 核对目标引擎版本、payload 完整性及 `.rpyc` / `.rpy` 配对关系 |

---

## 📘 术语与体例

| 原文 | 译法 | 说明 |
| --- | --- | --- |
| The Blade of Exodus | 放逐之刃 | 专名，取自游戏内"放逐"这一设定 |
| the Exodus（持有者名号） | 放逐者 | 原文是给予持有者的称号 |
| blade / sword | 剑 | 保留 `knife`＝刀、`捅刀`、`刀刃上`、`两面三刀`、`双刃剑` 等固定用法 |
| spirit / soul / idol | 灵 / 灵魂 / 灵像 | 三者分工不同，不混用 |
| Alestia | 阿莱斯蒂亚 | 全篇统一音译 |

体例约定：对话层不使用文言腔与现代职场词（如"团队""优先级""进度"），内心独白层不使用网络口语；中文标点全角；菜单项句式同构、不加句末句号。

---

## ⚙️ 构建与发布（维护者）

Windows 单文件 GUI 安装器由 GitHub Actions 在 Windows runner 上构建，不在维护者电脑本地打包。修改安装器、清单或 `payload/` 后推送会触发构建；也可在 Actions 手动运行 **Build standalone installer**。下载工作流产出的 `WoC-ChinesePatch-windows-x64` artifact。首次启动会解包到临时目录，退出后自动清理。

译文源在 `tl_work/chunks/*.tsv`（只编辑每行最后一列），工具链如下：

```cmd
python tools\tl_tool.py build --tl-dir tl_work --game-root "<游戏目录>"   :: 生成 game/tl/chinese/*.rpy
python tools\review_tool.py scan          :: 规则预筛（标签 / 术语 / 未翻译 / 语域）
python tools\review_tool.py register      :: 分层语域检查（内心独白 / 人物对话）
python tools\review_tool.py terms --apply :: 术语与专名统一（默认 dry-run）
python tools\review_tool.py dedupe --apply:: 重复句统一
python tools\review_tool.py worklist      :: 生成逐 chunk 工单与进度清单
"<游戏目录>\WindsofChange.exe" "<游戏目录>" compile   :: 重新编译 .rpyc
python tools\patch_tool.py verify --game-dir "<游戏目录>"
```

改动流程固定为：编辑译文 → `build` → `compile` → `verify` → 提交。发布采用**新增** Release 的方式，不覆盖历史版本；每个发布包的 `manifest.json` 记录该版本的文件清单与哈希。

版本历史见 [Releases](../../releases)。

---

## ⚠️ 版权与许可

- **原作者**：本游戏《Winds of Change》(Steam appid 594130) 由 **Klace** 开发并发行，游戏的所有权利（原作、美术、音频、剧情、人物等）均归原作者所有。
- **素材声明**：本项目使用了**翻译后的游戏原版资源**——包含对白文本的译文，以及对部分游戏原图（地图、书页、教程图等）改写后的版本；这些资源随补丁分发，其原始版权仍属于游戏作者。
- **不含游戏本体**：本仓库仅包含翻译文件、改版资源与工具逻辑，**不含任何游戏本体的原始文件**；使用前请自行购买并安装正版游戏。
- **非营利**：仅限非营利目的使用与分享，严禁用于商业用途。


**字体**：中文界面使用 [Sarasa Gothic（更纱黑体）](https://github.com/be5invis/Sarasa-Gothic) UI SC，以 **SIL OFL 1.1** 许可随补丁分发（许可全文见 [OFL-SarasaGothic.txt](OFL-SarasaGothic.txt)）。补丁的做法是直接替换游戏原版的 `game/gothic.ttf`，不新增字体目录。

**许可证**：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)（全文见 [LICENSE](LICENSE)）
