# review/archive —— 历史审计归档

## rounds/ —— v1.3.9–v1.3.10 各轮次过程报告（42 份）
保留作历史溯源；其中的发现与建议**均已执行完毕或过时**，不作为待办工单。
- 图片轮：`image-fix-report.md`、`image-current-recheck.md`、`image-repair-completion.md`、`image-repair-round3-completion.md`、`image-repair-round4-completion.md`、`image_metrics*.tsv`、`map_labels_room_check.md`、`en_*_labels.md`、`en_b0009_signature.md`、`recheck_b0009_b0002.md`
- 文本轮：`fantasy-proofread-report.md`、`report_sections_b/c.md`、`all-findings.tsv`（627 条总账）、`dedupe_groups.tsv`、`name_consistency.md`、`variant_names.md`
  （`worklist.md`/`checklist.csv`/`fixups.tsv` 为 review_tool 的现行输入输出，已留在 `review/` 顶层，不在此归档）
- 复核轮：`diff_*`、`semantic_*`、`recheck_*`、`verify_*`（含 round2/round3）、`summary_table.md`
- `remaining-issues.md` —— 图片修复后复盘（其 A 级已全部标 ✅；§5 图片建议当时即注明"不应直接作为执行工单"）

## 留存顶层（仍为现行有效）
- `terms.tsv` —— 术语规则表（含 2026-09-28 灵/灵体、The Monarchy 终裁）
- `verification-report.md` —— v1.3.10 主验收报告（§8.1 有勘误，见文内批注）
- `findings.md` / `candidates.tsv` / `register.md` / `fantasy_scan.tsv` / `worklist.md` / `checklist.csv` / `fixups.tsv` —— review_tool 的现行输入输出（重跑工具会原位刷新/读取，勿移走）
- `full_review/` —— **2026-09-28 全量终审报告与七路原始发现（现行主报告）**
- `work-fix/` —— 见该目录 README

## 备份目录（.gitignore 已忽略，未移动）
`backup_chunks_*` 系列为各批次改前快照，其中 `backup_chunks_termfix_20260926-112223` 是 §8.1 的对账基线，勿删。

## 已删除（2026-09-28 清理）
- `review/current-*.jpg/.json`、`pre-remake-*.png`（git 忽略的视觉复核件；图像原版保留于 `tl_work/image_repair_20260926/before/` 与 manifest 备份）
- `tl_work/` 内 70 个一次性审计图片与 `_export_spirits.py`（裁剪图/预览图，无脚本引用，主图均在 payload 与备份中）
