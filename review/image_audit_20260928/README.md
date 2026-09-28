# 图片译文全量审计报告（2026-09-28）

**范围**：payload/game/images 全部 51 张图（12 地图 + 17 书页 + 8 教程/杂项 + 14 开场字幕），逐张与英文原版比对。
**口径**：review/terms.tsv 终裁 + docs/reference/lore.md 设定（含 2026-09-28 灵/灵体二分裁决）。
**分组底稿**：a_maps.json（地图）、b_books1.json（b0001-9）、c_books2.json（b0010-17）、d_tutorials.json（教程/杂项）、e_opening.json（字幕）。
**英文原版来源**：backup_maps_original_2026-09-22、imagegen_inputs/books、backup_crawl_original、backup_images_2026-09-22_0430、backup_additional_text_images_2026-09-22、backup_opening_title_original_2026-09-22（注意：Steam 目录已是补丁版，不可作英文对照）。
**识别方法**：透明浮层图（zz 字幕等）用 `tl_work/flatten_png.py` 压平（白字自动压黑底）后比对。

## 结论：40/51 全合规；误译集中在 6 张图（均 A 级必修）+ 5 张 B 级打磨

**执行状态**：
- ✅ **zzz0-2 已修复**（脚本管线「众灵至高无上」），chain_build 已同步 manifest
- ✅ 其余 9 张按 **[Codex 工单](codex_work_order.md)** 全部从英文原图以图像接口重制：b0003、b0004、b0005、b0008、b0010、b0012、AlarinMapColi、AlarinMapCastle、tut006。书页绿键恢复透明，教程面板文字区按新字形重建 alpha；输出均为 1280×720，压平与深浅背景目视核查无明确文字错漏或绿边。图像编辑调用见 [image_generation_call_example.md](image_generation_call_example.md)。
- ✅ `chain_build.py --apply` 编译退出码 0，manifest 哈希已同步，`patch_tool.py check` 为 Payload files/hashes 68/68 OK；`screens.rpy` 临时文件已复原。
- ⚠️ 密集书页在 1280×720 预览下难以作法证级逐像素字形保证；后续若发现具体伪字，应从英文原图重新生成，不在旧中文版上局部脚本改字。
- 🔍 **独立复核（父代理，2026-09-28 晚）**：对 9 张重制图逐张 view_image 对照工单正文——b0003/4/5/8 全部裁决项落地（灵/幻象/灵力/依赖）、b0010 补译到位、b0012 三处改动到位（船行/正直/不去）、AlarinMapColi「室外」、AlarinMapCastle「舞厅」、tut006「心灵对话」×3 与三选项逐字一致；未见新错字、残英或绿边。复核后再跑 `chain_build.py --apply` 仍 68/68 OK。

### A 级（误译，必修）

| 图片 | 问题 | 修法 |
| --- | --- | --- |
| ✅ b0003 / b0004 / b0005 / b0008 | 抽象/信仰语境的 spirits 误译「灵体」共 9 处（图片重绘早于 2026-09-28 二分终裁，全部漏网）。b0004 尤其自相矛盾：标题「灵的真正影响力」用「灵」、正文用「灵体」 | 按二分终裁改「灵/众灵」（书页内容为学术/信仰语境，建议「灵」） |
| ✅ AlarinMapColi | OUTSIDE 译「城外」：竞技场在城内（AlarinMapCity 可证），该标签指场馆外的露天区，「城外」误导玩家到城墙之外 | 改「室外」（或「场外」） |
| ✅ zzz0-2 | "where the spirits reign supreme" 译「灵体至高无上……」：开场世界观属抽象语境 | 改「众灵至高无上……」 |

### B 级（口径/打磨，建议修）

| 图片 | 问题 | 修法 |
| --- | --- | --- |
| ✅ b0004 | 「灵性能量的容器」偏离术语（追加发现，父代理亲验） | 灵性能量→灵力 |
| ✅ AlarinMapCastle | BALLROOM 译「宴会厅」（且 lore：阿拉林西亚统治者每年办舞会） | 改「舞厅」 |
| ✅ tut006 | Heart-to-Heart 译「心与心的交谈」（标题+正文两处） | 统一「心灵对话」 |
| ✅ b0010 | 漏译首句 "This is it."（只译了 "I've finally done it"） | 已补「就是这一刻。」 |
| ✅ b0012 | honest 前后两译不一致（「安稳日子」vs「诚实劳动者」），弱化「清白守法」；**追加：「马泽奥航运公司」违反「马泽奥船行」终裁**（父代理亲验发现） | 统一为「正直」口径；航运公司→船行 |

### 可选小注（不改也可）
- ✅ b0005：右页 "would be impossible" 已重制为「绝不可能」，消除旧译「几乎无法」的程度弱化
- b0007：「逝者的眼泪，他们正试图…」代词「他们」应为「它们」（施事是眼泪）
- b0001：The Rebel Alliance 译「反抗军同盟」（EN 确为 Alliance，基准「反抗军」，可不改）

### 已知工艺残留（不修）
- **tut002 / tut004**：原图含半透明 alpha 层，生成模型无法输出 alpha，成品为「提取原图 alpha 混合生成图」——残存英文位于半透明混叠层，**玩家几乎不可见**（用户确认的既定工艺），译文本身经审计准确。不再列入修复范围。
- BalteusMap3 英文原图自带拼写错误 "MOUTAIN PASS"，中文「山口」正确，不受影响（可向原版作者反馈）。

### 全合规确认（40 张，要点）
- **RebelHQMap**：个人房间/成员宿舍/地道/作战桌——全部命中 terms.tsv 终裁
- 地图：四国名、佩雷格里诺/索尔伯格/东冠/瞭望台/命运之桥等全部一致；「帆船」两处图中带帆可证
- 书页：六时人（非六人帮）、审判庭、荣誉卫队、大图书馆、德雷库、阿尔古斯·维勒尔（已统一含"尔"）等全部合规
- 字幕 13/14 全合规；tut001/003/005、zzzzjournal1（瓦莱莎·克罗琳）、a0003（～后日谈～）合规

## 修复执行记录
仅以英文原图进行图像编辑生成；原始生成图、后处理成品和压平核查图保存在 `tl_work/image_audit_repair_20260928/`。后处理只缩放/恢复透明，不改写译文；`python tl_work/chain_build.py --apply` 已同步 manifest 并通过 68/68 检查。
