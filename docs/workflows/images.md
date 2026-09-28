# 图片处理工作流

补丁含 54 张改版图片（12 地图 + 17 书页 + 8 教程/杂项 + 14 开场字幕 + 主菜单等）。按内容性质分**两条管线**，选错管线是历史返工的主要来源。

DSH 会话内有两个配套技能，处理图片前先用 skill 工具加载：`imagegen`（通用图像生成/编辑纪律）与 `game-image-localization`（本仓库实测配方与验收流程）。技能全文在 `C:\Users\Fractal\.dsh\skills\` 下，含本文件未重复的全部禁令。

## 一、管线 A：纯文字浮层（脚本排字）

适用：开场字幕（zzz0-2 等）、纯文字且背景透明的图。这些图文字就是全部内容，不需要图像生成。

- 脚本：`tl_work/render_opening_caption_text.py`
- 文本来源：`tl_work/opening_caption_text.json`（改译文只改这个 JSON）
- 渲染参数：LXGWWenKai Regular/Medium 字体（`C:\Windows\Fonts\`）、4 倍超采样、倾斜 10°、白字、透明 RGBA 输出。
- 改字流程：改 JSON → 跑脚本 → `flatten_png.py` 压平目视 → `chain_build.py --apply` 同步。

## 二、管线 B：位图重绘（AI 图像编辑）

适用：书页、地图、教程等有底图/纹理/截图的图。**文字由图像接口整图重绘，不得用 Python/PIL 画字，不得在旧中文版上局部改字。**

### 1. 英文原图来源（只能从这些位置取）

| 类型 | 位置 |
| --- | --- |
| 书页 b0001-b0017 | `tl_work/imagegen_inputs/books/`（已做绿底准备） |
| 地图 | `tl_work/backup_maps_original_2026-09-22/` |
| 教程/杂项 | `tl_work/backup_additional_text_images_2026-09-22/`、`tl_work/backup_images_2026-09-22_0430/game/images/` |

⚠️ Steam 游戏目录里的图已是补丁版中文版，**不能**当英文对照；`payload/game/images/` 与备份目录里的中文版也**不能**当编辑目标。

### 2. 调用图像编辑接口（DSH 会话内）

```
read_image <英文原图路径>          → 返回 name / sha256 / 宽高 / bytes
codex_connect_image_generate({
  "operation": "edit",
  "target": { "attachment": {
      "attachmentId": "sha256:<上一步返回的完整哈希>",
      "mediaType": "image/png", "width": ..., "height": ...,
      "bytes": ..., "name": "<文件名>" } },
  "prompt": "……逐字中文全文……"
})
```

- `attachmentId` 就是 `sha256:` 前缀加 read_image 返回的哈希，其余字段照抄。
- 提示词纪律：用例 `text-localization`；每个文本区域给**逐字全文**（标题/正文/署名/页码/地图全部标签/教程选项）；明确保留项（纹理/角色/排版/图案）与禁止项（残留英文）；说明绿底或透明外侧要求。
- 每张独立资产单独调用一次；结果尺寸由服务决定（本项目实测 1672×941），不要硬保证。
- **调用成功 ≠ 图片合格**：逐字核对发现错字/漏字/伪字/残英，从英文原图重新生成（或用返回的 `assetId` 继续编辑后**重新完整验收**），验收不过就重试，不自动放行。
- 完整工单范例：`review/image_audit_20260928/codex_work_order.md`；调用 JSON 实例：`review/image_audit_20260928/image_generation_call_example.md`。

### 3. 取回原图字节

优先在结果卡片「下载原图」；或从 DSH 附件缓存 `C:\Users\Fractal\.dsh\attachments\v1\objects\<前2位>\<完整sha256>` 复制——**必须先验证文件存在且 SHA-256 与返回值逐字节一致**。保存到独立 staging（如 `tl_work/image_audit_repair_20260928/generated/`），不直接覆盖游戏资源。

### 4. 非文字后处理

脚本：`tl_work/image_audit_repair_20260928/finish_generated.py`（**仅限特定九图**，拒绝覆盖现有输出，尺寸固定 1672×941，教程文字区坐标写死；版式变化须先审查更新脚本）：

```cmd
python tl_work\image_audit_repair_20260928\finish_generated.py --generated <原图目录> --staged <全新输出目录>
```

- **书页**：先键掉纯绿（`key_book`）→ LANCZOS 缩到 1280×720 → 去绿色溢边 → RGBA。
- **地图**：等比 LANCZOS 缩到 1280×720，RGB 不透明。
- **教程**：英文 RGBA 原图先把透明外侧填纯绿供编辑；生成后还原透明外侧与面板半透明，**文字矩形 alpha 先归一到邻近面板 217，再仅按新字白字亮度恢复字形**——旧英文文字的 alpha 绝不能混进新画面（`TEXT_BOXES` 坐标写死）。
- 底层函数在 `tl_work/image_repair_20260926/finish_assets.py`（`key_book` / `reconstruct_tutorial`）；**不要**直接跑它的批量 `process()`，会意外覆盖其他素材。

### 5. 验收（双背景 + 逐字）

1. `python tl_work\flatten_png.py <staged目录>` 生成压平副本（自动选底：白字压黑底，暗字压白底）——透明浮层图不压平会白字白底看不见。
2. 看完整分辨率图、1280×720 目标尺寸图、白底/深底压平图。
3. **逐字对照工单**：地图每个标签、教程三个选项、署名、页码。
4. 检查：无英文残影、透明边缘无绿边/光晕、正文不越边、教程截图图标与选中条仍在。
5. 人工读不清就不能宣称逐字零误；必要时独立复核者目视。
6. 全部通过才复制到 `payload/game/images/`，复制后核对源/目标 SHA-256；一张不过不标 ✅。

### 6. 安装与终验

```cmd
python tl_work\chain_build.py --apply
```

独立确认：`compile 退出码: 0`、manifest 同步、`screens.rpy.__tmp` 已复原、`Payload files/hashes: OK (68)`。

## 三、历史教训（勿重蹈）

- **tut002/tut004 白边**：旧 alpha 混合工艺残留，用户确认不修的已知瑕疵；新版教程工艺已避免。
- **b0004 灵性能量/灵体混用**：图片重绘早于术语终裁导致漏网——图片修复必须先查 `review/terms.tsv` 最新裁决再写提示词。
- **旧中文版当输入**：第三轮 HQ 地图曾局部合成，后按裁决整图重制替换；规则就是——编辑目标永远是英文原图。
