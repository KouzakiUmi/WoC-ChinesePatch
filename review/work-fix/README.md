# work-fix 工单与改行清单

- `dialogue_*.md` / `strings_*.md` / `tail_*.md` —— **工单**（由 `tl_work/gen_worklist.py`、`gen_tail_worklist.py` 生成）：逐条列出该 chunk 的待修条目与改写规则。
- `*.changes.tsv` —— **改行清单**（各路修复 agent 产出），由 `tl_work/apply_worklist_changes.py [--apply]` 应用到 `tl_work/chunks/`。

## ⚠️ 这些清单已经全部应用过了（2026-09-26 第三轮）

**不要再次执行 `apply_worklist_changes.py --apply`**：清单里的值是"当时"的建议译文，此后又发生过
`{w}` 标签回补（`repair_tags.py`）、人名回填、同源行同步（`dedupe_analysis.py`）、fixups 等**后续改进**，
重跑会把当前更好的版本**回退**。

- 应用前的安全机制：行数/列数不变、除译文列外逐字节不变、新译文的 `{}` 标签与 `[]` 插值必须与旧译文一致（不一致会被拦截）。
- 现状核验：`apply_worklist_changes.py`（dry-run）中"当前值 == 基线值"的未应用行 = **0**；
  实测改动 812 行 = payload `.rpy` 差异 812 行（差额 0）。
- 若要重算：先用 `review/backup_chunks_termfix_20260926-112223/chunks/` 做基线比对。
