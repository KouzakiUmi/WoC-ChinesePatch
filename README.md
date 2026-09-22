# Winds of Change 简体中文补丁

Steam《Winds of Change》的简体中文汉化补丁。**仅面向 PC（Steam）版**，一键安装、可完整卸载，不包含游戏原始文件。

| 项目 | 说明 |
| --- | --- |
| 最新版本 | **v1.2.1** |
| 适用游戏 | Steam《Winds of Change》(appid 594130) |
| 基线校验 | `game/script.rpy` sha256 `c11fbeb67c84...`（写入 `manifest.json`，不匹配会拒绝安装） |
| 引擎 | PC 端 Ren'Py 7.1.1.929；补丁对 Ren'Py 8.x 同样可用 |
| 补丁内容 | 70 个文件 = 54 个修改 + 16 个新增 |

## 包含什么

- **全文对白与旁白**汉化：`game/tl/chinese/` 下 6 组 `.rpy` + `.rpyc`（对白 10370 行、界面串 1253 条）
- **语言切换模块**与**标题粒子效果**（`zzz_chinese_language.rpy`、`00title_particles.rpy`）
- **52 张改版图片**：书页笔记、区域地图、教程、爬塔、主菜单等
- **界面汉化**：`gui.rpy`、`screens.rpy` 以及配套对话框贴图逻辑

## 快速开始

Windows 下双击仓库根目录的三个脚本即可：

| 文件 | 作用 |
| --- | --- |
| `安装补丁.cmd` | 备份原文件并安装中文补丁 |
| `卸载补丁.cmd` | 从备份完整还原并删除新增文件 |
| `检查补丁.cmd` | 体检：引擎版本、文件完整性、`.rpyc`/`.rpy` 配对、Python 2 残留 |

命令行等价（只需 Python 3.8+，纯标准库，无需安装依赖）：

```
python tools/patch_tool.py install    [--game-dir PATH] [--force] [--backup-dir PATH]
python tools/patch_tool.py uninstall  [--game-dir PATH] [--force] [--keep-backup]
python tools/patch_tool.py verify     [--game-dir PATH]
python tools/patch_tool.py check      [--game-dir PATH]
python tools/patch_tool.py backup     [--game-dir PATH]
python tools/patch_tool.py find
```

不加 `--game-dir` 时会自动扫描 Steam 库（`libraryfolders.vdf`）和注册表定位游戏。

## 安装与还原机制

- 安装前先把将被覆盖的 **54 个原文件**复制到 `<游戏目录>/woc_zh_patch_backup/`，再写入补丁内容。
- 卸载优先从这个**本地备份**还原（逐字节校验过），因此补丁包被删除或移动也不影响还原；仓库里不需要携带游戏原文件。
- 安装后被你自己改动过的文件，卸载时会**跳过而不是覆盖**，并打印原因。
- 卸载会顺带清理 `game/cache` 与新增文件留下的空目录；加 `--keep-backup` 可保留备份目录。
- 兜底办法：Steam → 游戏属性 → 已安装文件 → 验证游戏文件完整性。

## 目录结构

```
payload/game/      补丁内容（70 个文件：54 修改 + 16 新增）
tools/             patch_tool.py 安装器、review_tool.py 校对工作流、tl_tool.py 构建、fetch_renpy_sdk.py 依赖获取
manifest.json      文件清单：路径、类型、双方 sha256、基线校验、引擎编译版本
docs/              校对工作流与角色档案（proofreading-workflow.md、characters.md、character-stats.md、renpy8-migration.md）
review/            术语表 terms.tsv、润色表 fixups.tsv、预筛报告、校对工单与进度、子代理审计留痕
安装补丁.cmd / 卸载补丁.cmd / 检查补丁.cmd    Windows 一键脚本
tl_work/           翻译源（分块 TSV）与构建脚本，仅维护者本地保留，不入仓库
originals/         游戏原文件副本，仅本地保留，不入仓库
```

## 翻译质量

这份补丁经过分层校对与多轮收敛，不是一次性机翻：

**分层处理**（11,623 行按文本层分开管）

| 层 | 行数 | 处理要点 |
| --- | --- | --- |
| 内心独白（第一人称旁白） | 3407 | 口语为底、容许内省长句；禁现代职场词与网络词 |
| 人物对话 | 6963 | 按角色档案统一口吻；禁文言腔与现代职场词 |
| 界面串 | 1253 | 简短、菜单项同构、保留占位符语义 |

**一致性**

- **术语统一**：`The Blade of Exodus` → **放逐之刃**（专名），`the Exodus` 作持有者名号 → **放逐者**，另有放逐突袭 / 放逐训练 / 放逐理论；`blade`、`sword` 统一为「剑」（保留 knife＝刀、捅刀、刀刃上、两面三刀与「双刃剑」固定搭配）；`soul`＝灵魂、`spirit`＝灵/灵体、`idol`＝灵像。
- **重复句零分歧**：全篇 708 组重复出现的原文，同一句、同一说话人全篇采用同一译法。
- **角色语气档案**：12 位具名角色 + 145 类通用 NPC 的敬语、称呼、句长特征写入 `docs/characters.md`，跨章节保持一致（例如 Howl 对君主一律用「您」、Fortaime 从不用「您」）。

**逐句精校**

- 6 个独立代理分批逐句比对原文，提出 382 条修改建议，按行去重并做标签/插值/换行合法性校验后**采纳 318 条**（误译 62、术语 112、语气 61、标点 55、其他 28），驳回 64 条（多为纯措辞偏好）。
- 另派 4 个代理**只看语境与角色**复核这 317 处改动，**撤销 2 条**（恢复更贴角色的旧译）、**再改 15 条**，并删掉 2 处串入相邻台词的内容。
- 审计留痕全部保留在 `review/subagent/`（原始建议、含上下文的改动清单、复核裁决），任何一处改动都能追溯。

**验收状态**：`{}` 标签与 `[]` 插值 0 处不一致；术语 0 违规；重复句 0 分歧；`patch_tool verify` 70/70。

## 维护者工作流

改译文、校对、统一术语都在 `tools/review_tool.py` 里完成：

```
python tools/review_tool.py stats                    # 进度 + 预筛统计
python tools/review_tool.py scan                     # 规则预筛 -> review/findings.md
python tools/review_tool.py register                 # 分层语域检查 (对话查文言/现代词, 独白查口语)
python tools/review_tool.py chars                    # 刷新角色语气证据表
python tools/review_tool.py worklist                 # 生成逐 chunk 工单与进度清单
python tools/review_tool.py mark <chunk> 已完成       # 更新校对进度
python tools/review_tool.py terms --apply            # 术语统一 (默认 dry-run)
python tools/review_tool.py dedupe --apply           # 重复句统一
python tools/tl_tool.py build --tl-dir tl_work --game-root "<游戏目录>"
python tools/patch_tool.py verify --game-dir "<游戏目录>"
```

改动流程固定为：编辑 `tl_work/chunks/*.tsv` 的译文列 → `build` 生成 `game/tl/chinese/*.rpy` → `WindsofChange.exe "<游戏目录>" compile` 重新编译 → `verify` 核对 → 提交。**迭代期间只提交、不发布；确认后一次性新增 Release，不覆盖历史版本。**

## 引擎版本兼容

`patch_tool.py` 会读取 `renpy/vc_version.py`、`renpy/__init__.py` 或 `log.txt` 判断引擎版本。补丁内的 `.rpyc` 由 PC 端 Ren'Py 7.1.1 编译（记录在 `manifest.json` 的 `compiled_with`）；若目标引擎主版本不同，安装器**跳过 `.rpyc`**、只投放 `.rpy`，由引擎首次启动时自行编译——因为 payload 中每个 `.rpyc` 都有配套 `.rpy`。游戏本体将来若升级引擎，补丁不会因 `.rpyc` 失效而打不开。

## 版本历史

| 版本 | 主要内容 |
| --- | --- |
| v1.2.1 | 子代理逐句精校（382 条建议采纳 318）+ 语境/人物视角复核（撤销 2、再改 15） |
| v1.2.0 | 全量精校定稿：分层校对、Exodus 统一「放逐」词根、去文言与现代职场词、独白去口语 |
| v1.1.5 | 全量收敛：重复句零分歧、对话层去文言、笔误病句修正 |
| v1.1.4 | Exodus 全文分析定译、独白去口语、敬语口径统一 |
| v1.1.3 | 引入分层校对（内心独白 / 人物对话） |
| v1.1.2 | 术语统一：放逐之刃、blade/sword = 剑；payload 与翻译源对齐 |

## 说明

游戏本体、美术与音频版权归原作者及发行方所有。本仓库只包含汉化改动内容与安装工具，不含游戏原始文件；引擎相关依赖按 `deps/renpy.json` 记录的官方地址获取（Ren'Py 为 MIT 许可）。
