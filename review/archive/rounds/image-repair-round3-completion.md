# 第三轮图片修复记录（2026-09-26）

依据更新后的 `image-fix-report.md` ★节、`verification-report.md` §7，以及 `verify_round2_maps.md`、`verify_round2_booknotes_2.md`，本轮只处理两个尚未通过的图片项。已通过的教程、森林标签与其他书页保持不变，未修改剧本或界面文本。

## 已完成的两个修复

| 图片 | 最新工单要求 | 当前结果 |
| --- | --- | --- |
| `RebelHQMap.png` | `PERSONAL QUARTERS` 对应「个人住所」，与文本侧新裁决一致；其余五个标签不改。 | 从英文原图通过内置图像生成制作「个人住所」标签，仅合入该标签所在区域。保留「作战桌 / 成员宿舍 / 地道 / 主入口 / 出口」。 |
| `b0009.png` | `Instead` 不能译作「因此」，改为「反倒 / 反而」。 | 从英文原书页重新生成，现为「反而，我让他在酒馆里消磨时间，等你把剑带给他。」其余已修正的深夜、郊外会面、那柄剑及进入索尔伯格的授权均保留；没有添加英文原图不存在的署名。 |

## 制作与自查

- 两张生成图的唯一编辑目标均为英文原图；没有将旧中文图送入图像生成。
- 使用内置图像生成，书页采用文楷风格中文。HQ 生成结果只用于新标签的小区域合成，其他已有中文标签不经过重绘。
- HQ 的实际像素改动包围盒为 `[866,351,986,409)`，约 `120×58` 像素；合成范围外所有 RGBA 像素与本轮修复前逐像素一致，因此其他五个标签及地图其余部分保持不变。
- b0009 从生成结果清除绿幕并重建透明度，没有套用英文原图或旧中文图的 alpha。按此前审查的可见青绿判据检测，残留为 0；深浅背景预览未见书外绿雾。
- 两张最终图片均为 `1280×720` RGBA。已目视核对目标词、全文、页码及布局，没有看到截断或压叠。
- `manifest.json` 仅定点更新本轮两条的 SHA-256 与字节大小，保留 `original` 与版本字段。
- `python tools/patch_tool.py check`：`Payload files: OK (68)`、`.rpyc/.rpy pairs: OK`、`Check result: OK`。

以上为制作方自查，没有将第二轮审计的 FAIL / PARTIAL 直接改写成独立审计 PASS。没有执行游戏演出测试，没有安装或发布新包。

## 当前文件

| 文件 | 字节数 | SHA-256 |
| --- | --- | --- |
| `payload/game/images/RebelHQMap.png` | 1490005 | `1da88dd7a9e1f9a8275c2dba651b843979498dbb1f570a8d37fa03881298f122` |
| `payload/game/images/b0009.png` | 1214276 | `c6d011a73c03e46254c93aa01b3c7d95958a840026a0a535f9d0a5808841ad8d` |

完整提示词：[prompts.json](../tl_work/image_repair_round3_20260926/prompts.json)。生成文件映射：[generated_paths.json](../tl_work/image_repair_round3_20260926/generated_paths.json)。检查指标：[after_metrics.json](../tl_work/image_repair_round3_20260926/after_metrics.json)。修复前备份与中间输出位于 `tl_work/image_repair_round3_20260926/`，不随补丁发布。

README 与图片报告开头已同步当前制作状态；原验收表和文本侧记录保留。当前 v1.3.8 已发布包不变，待文本审计完成后统一打包。
