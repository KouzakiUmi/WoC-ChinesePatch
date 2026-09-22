# Winds of Change 简体中文补丁

Steam《Winds of Change》的简体中文补丁。**仅用于 PC（Steam）版**，一键安装、可完整还原，不携带游戏原始文件。

| 项目 | 说明 |
| --- | --- |
| 适用游戏 | Steam《Winds of Change》(appid 594130) |
| 游戏引擎 | Ren'Py 7.1.1.929（PC 端），补丁同时兼容 Ren'Py 8.x |
| 基线校验 | `game/script.rpy` 的 sha256 `c11fbeb67c84...`，不匹配会拒绝安装 |
| 补丁规模 | 70 个文件 = 54 个修改 + 16 个新增（含 52 张改版图片） |
| 运行要求 | 只需 Python 3.8+（纯标准库，无第三方依赖） |

## 安装 / 卸载 / 检查

双击仓库根目录的三个脚本即可（Windows）：

| 脚本 | 作用 |
| --- | --- |
| `安装补丁.cmd` | 备份被覆盖的原文件，然后写入中文补丁 |
| `卸载补丁.cmd` | 从备份完整还原，删除新增文件，清理缓存 |
| `检查补丁.cmd` | 体检：引擎版本、文件完整性、`.rpyc`/`.rpy` 配对、Python 2 残留 |

命令行等价形式（不指定 `--game-dir` 时会自动扫描 Steam 库与注册表定位游戏）：

```bat
python tools\patch_tool.py install    [--game-dir PATH] [--force] [--backup-dir PATH]
python tools\patch_tool.py uninstall  [--game-dir PATH] [--force] [--keep-backup]
python tools\patch_tool.py verify     [--game-dir PATH]
python tools\patch_tool.py check      [--game-dir PATH]
python tools\patch_tool.py find
```

安装后直接启动游戏即为中文。若界面异常，删除 `<游戏目录>\game\cache` 后重启即可。

## 安装器做了什么

1. **定位游戏**：扫 `libraryfolders.vdf` 与注册表，找到 Steam 库中的游戏根目录。
2. **基线校验**：比对 `game/script.rpy` 的 sha256 与 `manifest.json` 中记录的值。不一致说明游戏版本不同或已被其他补丁改过，安装器会拒绝；确认无碍可用 `--force` 跳过。
3. **备份**：把将要覆盖的 54 个原文件复制到 `<游戏目录>\woc_zh_patch_backup\`，再写入补丁内容。
4. **还原优先用本地备份**：卸载时从该备份逐字节还原，因此补丁包被移动或删除也不影响还原；仓库无需携带游戏原文件。
5. **保护用户改动**：安装后被你自己改过的文件，卸载时跳过而不是覆盖，并打印原因。
6. **清理**：卸载会清空 `game/cache` 与新增文件留下的空目录；`--keep-backup` 可保留备份。

兜底方案：Steam → 游戏属性 → 已安装文件 → 验证游戏文件完整性。

## 补丁内容

- `game/tl/chinese/`：全文对白与旁白译文（6 组 `.rpy` + `.rpyc`，对白 10,370 块、界面串 1,253 条）
- `game/zzz_chinese_language.rpy`：语言开关 + 界面提示的运行时翻译钩子（见下文"技术细节"）
- `game/00title_particles.rpy`：标题粒子效果
- `game/gui.rpy`、`game/screens.rpy`：中文字体与界面适配（含存档界面中文标签）
- `game/images/`：52 张改版图片（书页笔记、区域地图、教程、爬塔、主菜单等）

## 目录结构

```
payload/game/      补丁内容（70 个文件：54 修改 + 16 新增）
tools/             patch_tool.py 安装器 / review_tool.py 校对工作流 / tl_tool.py 构建 / fetch_renpy_sdk.py 依赖获取
manifest.json      文件清单：路径、类型、双方 sha256、基线校验值、引擎编译版本
docs/              校对工作流（proofreading-workflow.md）、角色语气档案（characters.md / character-stats.md）
review/            术语表 terms.tsv、润色表 fixups.tsv、预筛报告与校对进度
安装补丁.cmd / 卸载补丁.cmd / 检查补丁.cmd
tl_work/           翻译源（分块 TSV）与构建脚本，仅维护者本地保留
originals/         游戏原文件副本，仅维护者本地保留（用于无备份时的兜底还原）
```

## 技术细节

### 译文如何生效

补丁使用 Ren'Py 原生的翻译机制：`game/tl/chinese/` 下的 `translate chinese ...` 块，配合 `zzz_chinese_language.rpy` 里的 `define config.language = "chinese"`，启动即中文，无需玩家手动切换语言。

### 界面提示为什么需要运行时钩子

`renpy.notify(...)` 与 `renpy.input(...)` 接收的是**裸 Python 字符串**。Ren'Py 的翻译提取只覆盖 say 语句、menu 选项和 `_()` 包裹的字符串，函数调用里的普通字符串不会被提取——这类提示（如开场的 "Use Enter or Left Click to advance text."、取名界面的 "Use keyboard to enter name"）原本一直是英文。

补丁在自己新增的 `zzz_chinese_language.rpy` 里把这两个函数包了一层，让提示语先经过 `renpy.translation.translate_string()` 查字符串表：

```
renpy.notify -> translate_string(message) -> 原 notify
renpy.input  -> translate_string(prompt)  -> 原 input
```

配套的 39 条英文/中文映射写在同一文件的 `translate chinese strings:` 块里。这样处理**不需要改动任何游戏原始脚本**，卸载时删除该文件即完全还原。

### 引擎版本兼容

`patch_tool.py` 会读取 `renpy/vc_version.py`、`renpy/__init__.py` 或 `log.txt` 判断目标引擎版本。补丁内的 `.rpyc` 由 PC 端 Ren'Py 7.1.1（Python 2）编译，版本记录在 `manifest.json` 的 `compiled_with` 字段；若目标引擎主版本不同，安装器**跳过 `.rpyc`**、只投放 `.rpy`，由引擎在首次启动时自行编译（payload 中每个 `.rpyc` 都有配套 `.rpy`）。因此把补丁装到 Ren'Py 8 的工程上也不会因字节码不兼容而出错。

### 校验机制

- `manifest.json` 为每个文件记录 sha256 与类型（modified / new），`verify` 据此核对安装结果。
- `base_check` 记录 `game/script.rpy` 的哈希，用于判断游戏基线是否匹配（该文件补丁从不修改，因此始终是原版哈希）。
- `check` 额外核对：`.rpyc` 与 `.rpy` 的配对关系、补丁内 `.rpy` 是否存在 Python 2 专有写法。

## 术语与体例

| 原文 | 译法 | 说明 |
| --- | --- | --- |
| The Blade of Exodus | 放逐之刃 | 专名，取自游戏内"放逐"这一设定 |
| the Exodus（持有者名号） | 放逐者 | 原文是给持有者的称号 |
| blade / sword | 剑 | 保留 `knife`＝刀、`捅刀`、`刀刃上`、`两面三刀`、`双刃剑` 等固定用法 |
| spirit / soul / idol | 灵 / 灵魂 / 灵像 | 三者分工不同，不混用 |
| Alestia | 阿莱斯蒂亚 | 全篇统一音译 |

体例约定：对话层不用文言腔与现代职场词（如"团队""优先级""进度"），内心独白层不用网络口语；中文标点全角；菜单项句式同构、不加句末句号。

## 构建与发布（维护者）

译文源在 `tl_work/chunks/*.tsv`（只编辑每行最后一列），工具链如下：

```bat
python tools\tl_tool.py build --tl-dir tl_work --game-root "<游戏目录>"   :: 生成 game/tl/chinese/*.rpy
python tools\review_tool.py scan          :: 规则预筛（标签/术语/未翻译/语域）
python tools\review_tool.py register      :: 分层语域检查（独白 / 对话）
python tools\review_tool.py terms --apply :: 术语与专名统一（默认 dry-run）
python tools\review_tool.py dedupe --apply:: 重复句统一
python tools\review_tool.py worklist      :: 生成逐 chunk 工单与进度清单
"<游戏目录>\WindsofChange.exe" "<游戏目录>" compile   :: 重新编译 .rpyc
python tools\patch_tool.py verify --game-dir "<游戏目录>"
```

改动流程固定为：编辑译文 → `build` → `compile` → `verify` → 提交。发布采用**新增** Release 的方式，不覆盖历史版本；每个发布包内的 `manifest.json` 记录该版本的文件清单与哈希。

版本历史见 [GitHub Releases](https://github.com/KouzakiUmi/WoC-ChinesePatch/releases)。

## 说明

游戏本体、美术与音频版权归原作者及发行方所有。本仓库仅包含汉化改动内容与工具，不含游戏原始文件；Ren'Py 引擎相关依赖按 `deps/renpy.json` 记录的官方地址获取（引擎为 MIT 许可）。
