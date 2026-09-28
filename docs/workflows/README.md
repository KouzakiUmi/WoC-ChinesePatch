# docs/workflows —— WoC 中文补丁技术工作流文档

本目录是维护者向的**完整技术文档**，覆盖翻译、校对、图片处理、构建发布四条工作流。
玩家向说明见根目录 [README.md](../../README.md)；角色语气档案见 [../characters.md](../characters.md)；设定/剧情参考库见 [../reference/](../reference/README.md)。

## 工作流索引

| 文档 | 覆盖范围 | 何时使用 |
| --- | --- | --- |
| [translation.md](translation.md) | TSV 译文源格式、编辑纪律、Ren'Py 翻译机制、构建链 | 修改任何译文/界面串之前必读 |
| [review.md](review.md) | 三层文本口径、术语表、检查工具、参考数据库、逐行精修纪律、全量审查方法 | 校对、术语统一、批量修复、质量审查 |
| [images.md](images.md) | 图片两条管线（脚本排字 / AI 图像编辑）、绿键与 alpha 后处理、验收标准 | 新增或修复任何图片资源 |
| [build-release.md](build-release.md) | chain_build 全链、manifest 同步、版本号、发布说明、CI | 每次提交前验证与每次发版 |

## 全局纪律（四条工作流共通）

1. **先读后改**：编辑任何现有文件前先读当前版本；批量脚本默认 dry-run，确认后才 `--apply`。
2. **逐行核对，不盲批**：任何批量替换都可能产生「灵体体」式事故——每一处改动都要对照英文原文判断上下文。宁可慢，不可错。
3. **全链验证不跳步**：任何译文/图片改动都必须走 `chain_build.py --apply` 全链并独立确认每一步退出码，详见 [build-release.md](build-release.md)。
4. **留档**：审查发现、裁决理由、驳回项都写入 `review/` 对应目录；改动了设定事实时同步更新 `docs/reference/`。
