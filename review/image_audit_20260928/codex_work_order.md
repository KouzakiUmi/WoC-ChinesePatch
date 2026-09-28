# Codex 图片修复工单（2026-09-28，含逐字完整正文）

> **重要**：Codex 图像识别不稳定，本工单为每张图附**修正后的完整正文全文**——生成时以下方文字为准，不要从旧图上 OCR。
> 管线约定：带 alpha 的图（书页/教程）输入=英文原图透明区填纯绿 #00ff00（书页绿底输入已备好在 `tl_work/imagegen_inputs/books/`）；**生成大图后缩回 1280×720（LANCZOS）**；生成图用绿键转 alpha（复用 `tl_work/image_repair_20260926/finish_assets.py` 的 `key_book`/`reconstruct_tutorial`）。完成后 `python tl_work/chain_build.py --apply` 同步 manifest。
> 已完成：zzz0-2.png（脚本改字入库）；不修：tut002/tut004（alpha 混叠工艺残留，玩家不可见）。

## 书页通用提示词前缀（4 张书页共用，正文见各条目）

```
Use case: text-localization. Asset: a 1280x720 PNG in-game readable book, 16:9 landscape. Input image is the original ENGLISH artwork composited on pure #00ff00 green, the sole edit target. Translate its English lettering into the exact Chinese supplied below. Keep book geometry, margins, parchment texture, ornaments, folds and colors unchanged. Use readable black LXGW WenKai-style Chinese calligraphic book typography; body about 23px at 1280x720, consistent size on both pages, well spaced lines, no tiny cramped text. Titles about 28px, same title at top of BOTH pages. Fit text through natural line wrapping and paragraph spacing. Maintain every paragraph and sentence verbatim; do not improvise or paraphrase. Keep original page numbers ~1~ and ~2~ centered at bottom. Only include a signature if explicitly specified. Outside the book keep a perfectly flat pure RGB(0,255,0) green screen with no shadows, gradients, checkerboard, noise or other marks; never paint green onto the parchment. No transparency requested here; downstream tool will key green to newly constructed alpha. Do not use old translated artwork. Generate at high resolution; downstream will downscale to 1280x720.
```

---

### 1. b0003.png（A 级）——输入 `tl_work/imagegen_inputs/books/b0003.png`

```
Title on both pages: 论书记官与幻象
LEFT PAGE paragraphs (verbatim):
瓦利诺斯的书记官之位举足轻重，不容轻视。他们受命聆听并解读先知的幻象，背负着沉重的精神负担。

灵有自己的语言，许多幻象的本质都晦涩难解。虽然它们随着时间推移变得更加清晰，最初却是一团混杂的隐喻与困惑。

仿佛经过许多年，灵界找到了更有效的沟通方式。这背后有许多耐人寻味之处。

我们不禁要问：灵界是否是一种有形的实体，能够成长和学习？对于沟通越来越清晰这一点，至今没有确切的解释。
RIGHT PAGE paragraphs (verbatim):
人们普遍认为，灵界承载着那些已经离开我们世界的灵魂。但迄今为止，从未有人真正与死者交流过，也没有见过久已逝去的挚爱之人。

相反，灵会把未来的幻象赐予能够看见它们的人。这些幻象几乎如同警示，帮助守护瓦利诺斯，也由此惠及阿莱斯蒂亚。

无论如何，由于幻象变得更加直白，书记官更像是一项仪式性的职位，不再承担真正的重责，只是延续瓦利诺斯的传统。

最近，瓦利诺斯为书记官配备了自己的门徒，以备不测时有人接班。因此，我正在瓦莱莎的指导下努力学习。
Right-page signature, right aligned above page number: ~福泰姆~
```

### 2. b0004.png（A 级）——输入 `tl_work/imagegen_inputs/books/b0004.png`

```
Title on both pages: 灵的真正影响力
LEFT PAGE paragraphs (verbatim):
人们普遍认为，植物是储存灵力的容器。这种能量十分纯净，因此住在森林地区的人往往更快乐，生活也更充实。

尽管许多人害怕灵影响心情，但灵迄今并未带来负面影响。为此，许多人会特意选择在自然环绕、充满“正向”能量的地方安居。

无论影响是正面还是负面，意图不明的影响都令许多人担忧。人们似乎只是因为这种力量带来了好处，才容忍它的存在。
RIGHT PAGE paragraphs (verbatim):
倘若灵界突然发难，让我们变得充满攻击性，甚至更糟，会怎样？

倘若它们正潜移默化地影响我们的思想，使我们逐渐屈从于它们的意志，又会怎样？到那时，它们岂不是能任意驱使我们？

这种想法也让许多人远离阿莱斯蒂亚的这类地区。不过，大城市众多，找到合乎自己信念的居所并非难事。

许多人请三人执政团对此发表看法，但他们始终保持沉默。难道连我们的统治者也不知道灵的真正本质，以及它们的影响范围？
Right-page signature, right aligned above page number: ——阿尔古斯·维勒尔
```

### 3. b0005.png（A 级）——输入 `tl_work/imagegen_inputs/books/b0005.png`

```
Title on both pages: 幻象与画作
LEFT PAGE paragraphs (verbatim):
来自灵的幻象，似乎更像一幅画作。当幻象结束时，先知往往能清晰地回忆起整体画面，而较小的细节却会在传达过程中遗失。比如，若幻象关乎一位村民的死亡，死亡这件事会很清楚；但他如何死去，以及每位村民对此的反应，都很模糊。与其说是确切知晓，不如说是一种直觉，或对事件的一种解读。

有时，灵仿佛只传来一幅事件的画面，先知便在梦中将它演绎出来，试着理解其中含义。若同一幻象被不止一位先知看到，各自的解读很可能大相径庭。
RIGHT PAGE paragraphs (verbatim):
但由于任何时候都只有一位先知，我们永远无法检验这一点。书记官会与先知深入讨论每一场幻象，最终得出双方都能接受的解读。

很多时候，细节会被忽略，只有整体画面受到采信。以死亡为例，我们只能推断瓦利诺斯即将有人死亡，绝不可能深入探究为何会发生。

不过，灵与我们联系、沟通的能力正随着时间逐渐增强。也许不久后，幻象就会变得确凿明晰，而“解读”也将成为过去，不再有必要。
Right-page signature, right aligned above page number: ~福泰姆~
```

### 4. b0008.png（A 级）——输入 `tl_work/imagegen_inputs/books/b0008.png`

```
Title on both pages: 瓦利诺斯的先知血脉
LEFT PAGE paragraphs (verbatim):
瓦利诺斯的先知们帮助引领我们的民族走向持久和平。在瓦利诺斯，人人都在灵界指引下过着简单而幸福的生活。每一代只有一位先知；先知降生时，位于索尔伯格的灵像便会涌出一股能量。

预计会有新生儿降临时，守卫会轮流看守灵像。任何时候都只有一位先知，而先知更替之间的空档极短，因此我们总能准确预料下一位先知何时降生。

瓦利诺斯人口稀少，一夜之间诞生多个新生儿的情况极为罕见。
RIGHT PAGE paragraphs (verbatim):
然而，这并非我写下这些文字的本意。我想谈的是最近一代先知降生那一夜所观察到的情形。通常，灵像会迸发光芒与能量，然后恢复微光。但最近那位先知降生时，灵像并未恢复到微光的状态。最后一位先知来到我们身边后，留下的只有黑暗。

这对瓦利诺斯和阿莱斯蒂亚未来的影响，深远得难以想象。我们只能一天一天地过下去，明白对灵的依赖将会越来越少。如今，我们必须依靠阿莱斯蒂亚其他地方的人，而不能只靠自己。我会寻找未来可以共事的同道。
Right-page signature, right aligned above page number: ——瓦利诺斯长老
```

### 5. AlarinMapColi.png（A 级）——输入 `tl_work/backup_maps_original_2026-09-22/AlarinMapColi.png`（不透明地图，无需绿底；若需保留 alpha 则提取现行 payload 图的 alpha 混叠）

完整标签清单（除标注外其余与现行中文版一致）：
```
PRIVATE ROOM → 私人房间
ARENA → 竞技场
MAIN ATRIUM → 主中庭
OUTSIDE → 室外      ← 唯一改动（原译「城外」误导，竞技场在城内）
EXIT → 出口
```

## B 级（4 张）

### 6. AlarinMapCastle.png ——输入 `tl_work/backup_additional_text_images_2026-09-22/AlarinMapCastle.png`

```
THRONE ROOM → 王座大厅
BALLROOM → 舞厅      ← 唯一改动（原译「宴会厅」；ballroom=舞厅，该国统治者每年办舞会）
PRIVATE ROOM → 私人房间
CASTLE FRONT → 城堡前庭
EXIT → 出口
```

### 7. tut006.png（B 级）——输入 `tl_work/backup_images_2026-09-22_0430/game/images/tut006.png`（需自行填绿；后处理复用 `finish_assets.py` 的 `reconstruct_tutorial`，tut006 面板参数已在其中）

完整正文（旧提示词同结构，仅「心与心的交谈」全部改为「心灵对话」）：
```
Title between original hearts: 心灵对话
Top three centered lines:
同伴标有爱心图标时，与其交谈便会触发特殊场景。
每段场景只能体验一次，作出的选择也无法更改。
这些场景散布于游戏各处，必须按顺序完成。
In the MIDDLE RIGHT screenshot, keep three rows with existing icons and selected first-row orange highlight. Replace ALL THREE English options verbatim:
“当然。我们会一起面对一切。”
“发掘内心的力量也很好，瓦莱莎。”
“只要你需要，我随时乐意帮忙。”
Bottom three left-aligned lines:
这些场景对于巩固友谊、发展恋情至关重要。
完成某位角色的心灵对话，最终会解锁该角色的忠诚任务。
每位同伴的个人故事与主线任务同样重要。
```
（版面/绿底/面板等指令沿用 `prompts.json` → `tut006` 的完整英文部分，不变。）

### 8. b0010.png（B 级）——输入 `tl_work/imagegen_inputs/books/b0010.png`

```
Title on both pages: 神秘日记
LEFT PAGE paragraphs (verbatim):
就是这一刻。我终于做到了。

这十年来，我一直训练身体，以适应东冠的严寒。起初，我几乎走不了几英尺就得停下。可如今，我几乎能坚持一整天才需要折返。我知道，答案已近在眼前。

东冠究竟有何目的？阿莱斯蒂亚还有多少未曾探索的疆域？

我打算最后一次深入这些冰封群山，我知道自己会找到真相。明天我会与妻儿道别，把日记留在入口处。如果我能活着回来，接下来的篇章便会写满奇观与发现。届时，我们终将明白一切。
RIGHT PAGE (verbatim):
[其余页面均为空白。]
（右页仅此一句居中；页码 ~1~ ~2~ 保留；无署名）
```

### 9. b0012.png（B 级）——输入 `tl_work/imagegen_inputs/books/b0012.png`

```
Title on both pages: 海盗行为的模糊界限
LEFT PAGE paragraphs (verbatim):
马泽奥的海盗负责非法货物的进出口。其他事务都由马泽奥船行经手，两派之间几乎没有别的区分。

双方都建立了贸易航线，在阿莱斯蒂亚各地拥有大量工人与客户。许多人视海盗为无害的普通人，不过是靠把握别人不去把握的机会谋生。

如今人们对待海盗的方式，与三人执政团占领马泽奥之前大不相同。这是有意为之吗？我们不禁要问，这是否正是三人执政团的目的。问及此事时，当地海盗领袖亚历克斯这样说道：
RIGHT PAGE paragraphs (verbatim):
“我很难相信，区区一纸文书竟会挡在我和我的人民过上正直日子的路上。我们不伤害任何人，也不会把谁置于险境。马泽奥的人死抱着一条毫无道理的法律不放。我希望贸易禁令能够解除，让我和我的人民以诚实劳动者的身份重回社会。这是我的梦想，我会为此继续奋斗。”

被问及看法时，另一位海盗领袖娜达拒绝置评。
```
（改动 3 处：马泽奥航运公司→马泽奥船行〔终裁〕、安稳日子→正直日子〔honest〕、不愿把握→不去把握）

## 完成后回归验证清单
1. 每张图 flatten（`tl_work/flatten_png.py`）目视核对：与本工单正文逐字一致、无残字、无绿边。
2. `python tl_work/chain_build.py --apply`（重建+编译+manifest 哈希同步+check 68/68）。
3. 在 review/image_audit_20260928/README.md 对应条目标 ✅。
