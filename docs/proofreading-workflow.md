# 精校工作流 (统一口径)

目标有两个: **跨 chunk 一致** 和 **分层语域正确**。前者靠角色档案 + 术语表 + 重复句统一, 后者靠把文本分成三层分别套规则。

## 一、三层文本

| 层 | 判定 | 行数 | 基调 |
| --- | --- | --- | --- |
| 内心独白 | `speaker` 为空 (主角第一人称旁白) | 3407 | 口语为底、允许内省长句; 禁现代职场词、禁网络词、禁文白跳脱 |
| 人物对话 | `speaker` 非空 | 6963 | 以该角色档案为准; 禁文言腔、禁现代职场词 |
| 界面串 | `kind=strings` | 1253 | 简短、无句末句号、保留 `%` 与 `[...]` 占位符 |

分层由 `review_tool.py` 的 `classify()` 自动完成, 不要靠肉眼判断。

## 二、五步闭环

1. **建基准** — `chars` 生成 `docs/character-stats.md` 证据表 → 据此定稿 `docs/characters.md`(角色语气/敬语/称呼)；术语进 `review/terms.tsv`。
2. **出工单** — `worklist` 生成 `review/worklist.md`(按 chunk 列出候选) 与 `review/checklist.csv`(进度)。
3. **逐 chunk 精校** — 每个 chunk 先读角色档案, 再按层处理候选, 同时人工通读该 chunk; 改完 `mark <chunk> 已完成`。
4. **自动收敛** — `terms --apply`(术语)、`dedupe --apply`(重复句)、`review/fixups.tsv`(一次性润色)。
5. **回归发布** — `build` → `WindsofChange.exe <游戏目录> compile` → `patch_tool.py verify` → 提交 → **新增** Release(不覆盖旧版)。

## 三、常用命令

```
python tools/review_tool.py chars                  # 刷新角色语气证据表
python tools/review_tool.py worklist               # 出/刷新工单 + 进度清单
python tools/review_tool.py mark data/dialogue_0005.tsv 已完成
python tools/review_tool.py register               # 分层语域违规 (对话查书面腔/现代词, 独白查口语网络词)
python tools/review_tool.py scan                   # 通用预筛 (标签/术语/未翻译/标点等)
python tools/review_tool.py terms --apply --build --game-root "<游戏目录>"
python tools/review_tool.py dedupe --apply --build --game-root "<游戏目录>"
python tools/patch_tool.py verify --game-dir "<游戏目录>"
```

## 四、验收标准 (每个 chunk 都要过)

- `{}` 标签与 `[]` 插值 0 不一致；`\n` 位置合理且数量一致。
- 术语表 0 违规 (`terms` 无输出)；专名与头衔统一。
- 该 chunk 内重复句与全篇同句译法一致 (`dedupe` 无输出)。
- 对话层无文言腔 (`亦然/意欲何为/乃至/皆/乃/岂/予以/加以/从而/因而/故而/极为/甚为/颇为/亦/遂`)、无现代职场词 (`团队/优先级/进度/效率/资源/管理员/失业/制度/流程/反馈/沟通/管理`)。
- 独白层无网络口语 (`稳了/溜了/咋/咱/绝了/上头/破防/哥们/老铁/大佬/事儿/味儿`)。
- 敬语与人称符合 `docs/characters.md` 的 您/你 口径。
- 中文标点全角；界面串无句末句号。

## 五、纪律

- 只改 `tl_work/chunks/*.tsv` 的最后一列, 不要动 speaker/source/结构。
- 任何改动都要走 `build` + `compile` + `verify` 全链, 不跳步。
- **迭代期间不发布**: 精校过程中只提交代码与译文, 不发 Release; 全部 chunk 确认后再一次性发布新版本 (发布一律新增, 不覆盖旧版)。
- 迭代期间 manifest 版本记为 `x.y.z-dev`, 定稿时去掉 `-dev` 并发布。
