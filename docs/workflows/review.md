# 校对与审查工作流

目标：**跨 chunk 一致** + **分层语域正确** + **对照英文原文逐行准确**。
体例基线另见 [../proofreading-standard-western-fantasy.md](../proofreading-standard-western-fantasy.md)（西方奇幻小说规格）；旧工单式流程见 [../proofreading-workflow.md](../proofreading-workflow.md)（历史文档，发布步骤以本文档与 [build-release.md](build-release.md) 为准）。

## 一、三层文本口径

| 层 | 判定 | 基调 |
| --- | --- | --- |
| 内心独白 | `speaker` 为空 | 口语为底、允许内省长句；禁现代职场词、禁网络词、禁文白跳脱 |
| 人物对话 | `speaker` 非空 | 以该角色档案为准（[../characters.md](../characters.md)）；禁文言腔、禁现代职场词 |
| 界面串 | strings chunk | 简短、无句末句号、保留占位符 |

分层由 `tools/review_tool.py` 的 `classify()` 自动完成，不靠肉眼。

## 二、检查工具

```cmd
python tools\review_tool.py scan        :: 通用预筛（标签/术语/未翻译/标点）
python tools\review_tool.py register    :: 分层语域违规
python tools\review_tool.py terms       :: 术语表违规（--apply 应用）
python tools\review_tool.py dedupe      :: 同文异译（--apply 统一）
python tools\review_tool.py chars       :: 刷新角色语气证据表 docs/character-stats.md
```

`tl_work/` 下的专项扫描：`fantasy_check.py`（语域）、`gender_check.py`（代词性别冲突）、`punct_check.py`、`quote_check.py`、`honorific_check.py`（敬语）、`name_consistency.py`、`variant_check.py`。

**已知良性噪音**（不必清零）：scan 的 term-private-room 3 条（0004#1329 雅间等语境例外）、英文残留中的书目编号/版权/日期、punct 的 0026 打字机省略号（刻意）、quote 的既定风格。

## 三、术语表 review/terms.tsv

7 列（Tab 分隔）：

```
en ⇥ cn ⇥ variants(其他译法|分隔) ⇥ protect(保护片段) ⇥ mode(word|phrase) ⇥ exclude_en ⇥ note
```

- **终裁才入表**，note 必须写裁决日期与依据（含 seq 引用）。
- 语境二义的词**不写自动规则**，只在注释中说明判定口径（范例：spirits 二分、crew quarters 陆上/船上分工），靠人工逐行判定。
- 当前有效终裁摘录：The Monarchy→王室；The Monarch→君主；visions→幻象；空甲；内殿；烽火；心灵对话；马泽奥船行；灵力；personal quarters→个人房间（与 HQ 地图标签一致）。

## 四、参考数据库 docs/reference/

精校前按需查阅（索引与使用约定见 [../reference/README.md](../reference/README.md)）：

- `characters.md`：角色性格画像（这句话符不符合这个人）
- `lore.md`：设定（灵体系/王室/放逐之刃/地理/终局揭示）——**注意 §6 剧透分层**，精校前期 chunk 时不得用后期才揭示的信息
- `plot.md`：四幕时序 37 节点、双轨结构（0021-0026 为平行重述轨）、结局变体

seq 引用格式：`0009#3335` = `dialogue_0009.tsv` 的 seq 3335；`strings#483`、`zzz#L56`（`payload/game/zzz_chinese_language.rpy` 行号）。改动台词若改变设定事实，须同步更新参考库并保持引用有效。

## 五、逐行精修纪律（血泪教训）

1. **任何批量改动先出决策清单**（每行：seq、EN、旧译、新译、判定理由），人工确认后才应用。参考 `review/work-fix/spirits_unify/decisions_g1-g4.json` 的模式。
2. **不要批量替换**——正则不知道上下文。事故案例：
   - 「灵体体」：批量把 灵→灵体 时命中已含「灵体」的行，双重转换。
   - G2 并发事故：12 行信仰短语被误改「灵体」，靠 decisions JSON 回退复验。
3. 每条改动对照英文原文判断，不是只看中文顺不顺。
4. 复审驳回项同样留档（附理由），防止下一轮审查重复提出。

## 六、全量审查方法（2026-09-28 实测）

完整案例见 [../../review/full_review/README.md](../../review/full_review/README.md)。要点：

1. **无抽样**：26 dialogue + 3 strings 全覆盖，按 chunk 分组逐行对照英文（可并行多路，每路一个 chunk 段，结果落 `g*.json`）。
2. **分级**：A 级误译/结构硬伤（必修）→ B 级术语/敬语/口径（应修）→ C 级风格打磨（建议修）。
3. **复审**：每条发现二次复核，应用或驳回都留档；批量型发现（如 0013 盔甲×21）单独成批。
4. **同型行归一**：重复场景与长句（EN>30 词）同文异译归一，语气短句的合法变体保留。
5. **修复批次脚本化**：每批一个 `apply_full_review_batchN.py`，dry-run 确认后 apply，最后全链验证。

## 七、验收标准（每 chunk / 每批次）

- `{}` 标签与 `[]` 插值 0 不一致；`\n` 数量与位置合理。
- `terms` 0 违规；`dedupe` 同文异译归一（合法变体除外）。
- 对话层无文言腔（亦然/意欲何为/乃至/皆/乃/岂/予以/从而/故而/甚为…）、无现代职场词（团队/优先级/进度/效率/资源/流程/反馈…）。
- 独白层无网络口语（稳了/溜了/绝了/上头/破防/老铁…）。
- 敬语符合角色档案的 您/你 口径（范例：豪尔对君主句含「你」= 0）。
- 中文标点全角；界面串无句末句号。
- 终验：`chain_build.py --apply` 全绿 + `patch_tool.py check` 68/68。
