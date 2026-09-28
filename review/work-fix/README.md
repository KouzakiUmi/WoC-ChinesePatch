# work-fix 工单与改行清单

## 当前有效内容
- `spirits_unify/` —— **2026-09-28 灵/灵体逐行精修工单**（candidates + decisions_g1-g4 + README），终审有效记录，配套报告见 `review/full_review/README.md`。

## 历史归档
- `archive_v1310/` —— **v1.3.9–v1.3.10 时代的 66 份工单/改行清单**（2026-09-26 第三轮全部执行完毕）。
  - ⚠️ **不要再次执行 `apply_worklist_changes.py --apply`**：清单值是"当时"的建议译文，此后有 `{w}` 标签回补、人名回填、同源行同步及 2026-09-28 终审修复等后续改进，重跑会回退当前更好版本。
  - 已知记录瑕疵（2026-09-28 审查确认，仅供参考不影响成品）：
    - `dialogue_0016.md` 无对应 changes.tsv（22 条从未执行，且无"经核不改"记录）；其 A 级方向错误（萨鲁斯→萨卢斯 是反向建议），2026-09-28 已按重审结论另行修复；
    - `tail_vivien_pronoun.md` 已被 v1.3.10 裁决作废（无 tsv，与裁决一致）；
    - changes.tsv 数据行合计 642，与本目录旧 README 宣称的 812 不符（812 实为 payload `.rpy` 差异行数口径，含后续批次）；
    - 约 30 份工单含过时的「个人住所」表述（终裁为「个人房间」，见 `review/terms.tsv`）。
  - 基线比对：`review/backup_chunks_termfix_20260926-112223/`。

## 本轮（2026-09-28）修复脚本索引（tl_work/，均可 dry-run 复演）
`apply_quality_fixes_r5.py`（已知问题 37 条）→ `apply_spirits_decisions.py`（灵/灵体 decisions 应用+同型同步）→ `apply_monarchy_unify.py`（The Monarchy=王室 62 行）→ `apply_full_review_g7.py`（strings 13 条）→ `apply_full_review_batch2.py`/`batch2b.py`（g1+g5，49 条）→ `apply_full_review_batch3.py`（g4+g6，48 条）→ `apply_full_review_batch4.py`（g2，31 条+场景同步 19 行）→ `apply_full_review_batch5.py`（g3，52 条+空甲 21 行）→ `sync_duplicate_long.py`（长句同型归一 43 处）。
