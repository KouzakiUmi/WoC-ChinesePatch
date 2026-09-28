# HQ 地图整图重制记录（2026-09-26）

用户最新裁决：`PERSONAL QUARTERS` 在 HQ 地图上采用「个人房间」，覆盖此前图片审查中的「个人住所」建议。用户要求从英文原版整张重做，避免在中文版本上局部覆盖造成字形不统一。

## 制作结果

- 唯一生成输入：`tl_work/backup_maps_original_2026-09-22/RebelHQMap.png`（英文原图）。
- 使用内置图像生成工具，六个标签在同一次生成中统一采用类似 LXGW 文楷的书面字体。
- 最终使用生成结果的完整画布，缩放至 `1280×720` 并保存为 RGBA；没有合入旧中文图的任何局部。
- 六个标签：作战桌、成员宿舍、地道、个人房间、主入口、出口。地下 HQ 的住宿区域仍为「成员宿舍」。
- 目视自查：六个标签文字正确、风格与字号一致，没有压字或截断。此记录是制作方自查，未改写此前独立验收结果。
- `manifest.json` 仅更新该图片的目标 `sha256/size`，原始文件字段及版本号未变。`patch_tool check` 通过，68/68 个 payload 哈希一致。
- 未修改剧本、术语表或其它图片；未重新打包发布。

## tut004.png

检查确认可见白边存在，英文原版也有此表现。用户随后要求不处理，已撤回临时清理并逐字节恢复至本轮开始时的文件。最终哈希 `78751609bf90c24f4823e3fb69164969815c5f835e0e85aa5e49c41cc325a64f`；本轮对该文件无改动。

## 文件与可复查资料

| 文件 | 结果 |
| --- | --- |
| `payload/game/images/RebelHQMap.png` | RGBA，1280×720，1,526,708 字节 |
| SHA-256 | `6e39ef17ad75e88d5984868e3f013c59db947715809000fdb9ea569aca6fce16` |
| 提示词 | `tl_work/image_repair_round4_20260926/prompts.json` |
| 生成原件 | `tl_work/image_repair_round4_20260926/RebelHQMap-generated.png` |
| 后处理脚本 | `tl_work/image_repair_round4_20260926/finish_map.py` |
| 指标与生成路径 | 同目录 `after_metrics.json`、`generated_paths.json` |

本轮覆盖第三轮 HQ 图片的术语、字形及局部合成方式；`b0009` 第三轮「反而」修复继续保留。第三轮及更早审查报告保留为历史记录。
