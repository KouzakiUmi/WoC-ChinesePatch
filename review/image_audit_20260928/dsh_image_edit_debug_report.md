# DSH 图像编辑工具调用调试报告（本会话实录）

> 目的：与 [image_generation_call_example.md](image_generation_call_example.md)（另一 DSH 会话中 GPT 成功执行 edit 的示例）对照，供排查两会话行为差异。
> 本会话环境：DeepSeek Harness（DSH NEXT），工作目录 `D:\WoC-ChinesePatch`，时间 2026-09-28（系统时钟）。所有内容为工具调用的逐字实录。

## 1. 症状摘要

| 调用 | 结果 |
| --- | --- |
| `read_image`（本地 PNG） | ✅ 返回图片，但**无 attachmentId 注册句柄行**（格式与示例会话不同，见 §3） |
| `codex_connect_image_generate`（operation=edit，target=本地图） | ❌ 两次均拒：`Target image: is unavailable or does not match a reference in this session. Select or attach the image again.` |
| `codex_connect_image_generate`（纯 generate） | 时段 A：❌ 三次 `The image generation request lost its network connection. The request may still be processing.`；时段 B（稍后）：✅ 成功（见 §5） |
| `grok_imagine`（对照组） | ✅ 正常（2730×1536 jpeg） |

## 2. 时间线（全部为本会话真实调用）

1. `view_image(tl_work/imagegen_inputs/books/b0004.png)` → 成功，返回归一化副本信息（格式见 §3-A）。
2. `codex_connect_image_generate{operation:"edit", target:{"attachmentId":"262e0bd7..."}}`（散列取自 view_image 返回的 sha256）→ ❌ target 不可用。
3. `codex_connect_image_generate{prompt:"A plain test image: ... 测试 ... 1280x720."}` ×3（间隔数分钟，最后一次改为 "Wide landscape format, high resolution."）→ ❌ 三次均网络错误。
4. `grok_imagine{prompt: 书页全文, aspect_ratio:"16:9", resolution:"2k"}` → ✅ 成功（对照：网络总体可用，仅 codex generate 当时失败）。
5. （收到示例文档后）`read_image(tl_work/imagegen_inputs/books/b0010.png)` → 成功，仍无 attachmentId 句柄行（§3-A）。
6. 按示例逐字段构造 edit 调用（§4）→ ❌ 同一 target 错误。
7. `codex_connect_image_generate{prompt:"A plain test image... Wide landscape, high resolution."}` → ✅ **成功**（网络已恢复），返回 1672×941 PNG 与 assetId（§5）。
8. 再次按示例 edit b0010 → ❌ 同一 target 错误。

## 3. 关键差异：`read_image` 返回格式

### A. 本会话（失败侧）——`read_image`/`view_image` 返回

```text
<path>D:\WoC-ChinesePatch\tl_work\imagegen_inputs\books\b0010.png</path>
<type>image</type>
<content>
image/png image, 1280x720 px, 1033268 bytes
</content>Image "b0010.png" (sha256:22ad0e295caec74053ec212d61d9bad9191bd8d48956df6521436a4c8cb2fecd); request preview 1280x720px. Normalized copy (read-only; may be resized or re-encoded): "C:\\Users\\Fractal\\.dsh\\attachments\\v1\\objects\\22\\22ad0e295caec74053ec212d61d9bad9191bd8d48956df6521436a4c8cb2fecd" (1280x720px, image/png). Source dimensions, format, and byte size may differ. Copy to a writable path ending in .png before editing.
```

要点：**没有 `attachmentId=` 句柄行**；归一化副本明确标注 read-only；sha256 值出现在括号与副本路径中，但它不是已注册的会话附件。

### B. 示例会话（成功侧）——`read_image` 返回（引自示例文档）

```text
attachmentId=sha256:22ad0e295caec74053ec212d61d9bad9191bd8d48956df6521436a4c8cb2fecd
mediaType=image/png, width=1280, height=720, bytes=1033268, name=b0010.png
```

同一文件、同一 sha256，但示例会话返回了**注册的 attachment 对象**（attachmentId 带 `sha256:` 前缀，且附 mediaType/尺寸/字节数/文件名）。工具说明中的一句暗示了开关存在："When image editing is enabled, Codex Connect places a model-visible handle line immediately after each request image" —— 本会话未出现该 handle line，疑似**本会话的图片编辑注册能力未启用**（或 read_image 实现版本不同）。

## 4. 本会话被拒的 edit 调用（逐字）

第一次（散列猜测，预期内失败）：

```json
{
  "operation": "edit",
  "prompt": "Use case: text-localization. ...（约1600字符书页本地化提示词）",
  "target": {"attachmentId": "262e0bd714b93893b795baf28f69ad327a1cc293a1b66b71c581c6a1aee8d6d7"}
}
```

第二次（按示例逐字段构造，仍失败）：

```json
{
  "operation": "edit",
  "target": {
    "attachment": {
      "attachmentId": "sha256:22ad0e295caec74053ec212d61d9bad9191bd8d48956df6521436a4c8cb2fecd",
      "mediaType": "image/png",
      "width": 1280,
      "height": 720,
      "bytes": 1033268,
      "name": "b0010.png"
    }
  },
  "prompt": "请仅编辑这张英文书页图片上的文字，保持原图书本的大小、轮廓、视角、装饰、旧羊皮纸质感、光影和页边距不变，擦除全部英文，不得留下残字。左右页顶部均为标题「神秘日记」。左页按段落顺序写下以下全文，逐字准确，不增删，不改写：\n\n就是这一刻。我终于做到了。\n\n这十年来，我一直训练身体，以适应东冠的严寒。起初，我几乎走不了几英尺就得停下。可如今，我几乎能坚持一整天才需要折返。我知道，答案已近在眼前。\n\n东冠究竟有何目的？阿莱斯蒂亚还有多少未曾探索的疆域？\n\n我打算最后一次深入这些冰封群山，我知道自己会找到真相。明天我会与妻儿道别，把日记留在入口处。如果我能活着回来，接下来的篇章便会写满奇观与发现。届时，我们终将明白一切。\n\n右页中部仅一句「[其余页面均为空白。]」，无其他正文。左页下方页码「~1~」，右页下方「~2~」，不加署名。采用清楚可读的深褐黑色中文书法字，正文两页字体一致，自然换行、段落分明，不挤入边框。书本外的所有区域必须是完全均匀的纯 RGB(0,255,0) 绿幕，无渐变阴影杂点，也绝不可在纸张上覆盖绿色。输出尽可能高分辨率，以便缩至1280×720。尤其注意中文所有字均正确，不能出现伪字或乱码。"
}
```

两次错误均为（未触发网络请求，本地引用校验即拒绝）：

```text
Error: Target image: is unavailable or does not match a reference in this session. Select or attach the image again.
```

## 5. generate 成功时的返回格式（供对照）

```text
Generated 1 image:
1. original image/png, 1672x941 px, 915566 bytes; preview 1672x941 px, attachment sha256:278d0c20ac5beb1829b76fe1307dc515f19ba31ffe89dcbb0ed969ccbe2a5e42codex-connect-image-result-v1:[{"original":{"assetId":"img_b284149e64b04f949675c9dcb322d33b","mediaType":"image/png","width":1672,"height":941,"bytes":915566,"name":"codex-image-1.png","sha256":"278d0c20ac5beb1829b76fe1307dc515f19ba31ffe89dcbb0ed969ccbe2a5e42"},"preview":{"attachmentId":"sha256:278d0c20ac5beb1829b76fe1307dc515f19ba31ffe89dcbb0ed969ccbe2a5e42","mediaType":"image/png","width":1672,"height":941,"bytes":915566,"name":"codex-image-1.png"}}]
```

要点：generate 结果同时给出 `assetId`（original）与 `attachmentId`（preview，带 `sha256:` 前缀）。按示例文档，对生成原图继续 edit 应使用 `target:{"assetId":"img_..."}`——本会话尚未实测该路径（无合适的生成原图可编辑）。

## 6. 排查假设（供检查 DSH 环境）

1. **会话级能力开关**：示例会话的 read_image 注册 attachment（返回 attachmentId 句柄行），本会话不注册（只读归一化副本）。两会话若在 DSH 版本/配置上有差异（如 image-editing flag、attachment registry），可解释全部现象。
2. **attachment 注册时机**：或许只有「用户上传的附件」与「本工具 generate 的结果」会注册；示例会话若实际是用户先上传了图片再 read，则其 attachmentId 来自上传而非 read_image——示例文档措辞（"先用 read_image 查看……本次工具返回相邻的图片句柄"）暗示句柄来自 read_image，需核实。
3. **网络瞬断**：时段 A 的三次 `lost its network connection` 为 generate 端点的临时故障，时段 B 已恢复；与 edit 被拒无关（edit 错误发生在本地引用校验阶段）。

## 7. 复现步骤（本会话）

```text
read_image tl_work/imagegen_inputs/books/b0010.png
# → 观察返回中是否有 "attachmentId=" 句柄行（本会话：无）

codex_connect_image_generate {
  operation: "edit",
  target: { attachment: { attachmentId: "sha256:22ad0e29...", mediaType:"image/png", width:1280, height:720, bytes:1033268, name:"b0010.png" } },
  prompt: "（任意编辑指令）"
}
# → 本会话：Error: Target image: is unavailable or does not match a reference in this session.
```
