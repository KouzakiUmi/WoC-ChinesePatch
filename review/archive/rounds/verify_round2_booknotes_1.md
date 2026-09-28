# 第二轮修复书页复核（b0001 / b0004 / b0005 / b0006 / b0007 + 追加 b0002）

- 判定依据：`review/image-current-recheck.md` §P1/§P2；`review/semantic_booknotes_1a.md`；`review/semantic_booknotes_1b.md`
- 核对对象：`payload\game\images\` 新版 5 张（+追加 b0002）；基准：`tl_work\backup_book_notes_original_2026-09-22\` 英文原版
- 读图自检：13 次 `read_image` 全部正常显示，回传 sha256 与所请求文件一一对应，图内标题与文件名自洽（b0001「迈勒斯的笔记」/ b0002「论阿莱斯蒂亚的创世」/ b0004「灵的真正影响力」/ b0005「预视与画作」/ b0006「神秘的马泽奥」/ b0007「论瓦利诺斯的血叶」，英文侧 Mylus' Note / On Alestia's Creation / The True Reach of Spirits / Visions and Paintings / Mysterious Mazeo / On Valinorth's Bloodleaves），**无串图**（英文 b0007 sha256 `527baf32…` 与 semantic_booknotes_1b 记录一致）；b0005 为核第 13 项**主动重读** 1 次，sha256 `683d753c…` 与首读一致、内容一致。
- sha256：b0001 `b9d21fc1…`、b0002 `46244333…`、b0004 `ba22c0cd…`、b0005 `683d753c…`、b0006 `706cbd9b…`、b0007 `71715698…`。

图 | 项 | 结果 | 图上实际文字 | 备注
---|---|---|---|---
b0001 | 1（左页第2段询问对象） | PASS | 「在我这样的处境下，很难抵挡这份诱惑。我忍不住问他们究竟知道些什么。」 | 询问对象已回到"他们"，EN `I had to ask them exactly what they knew`；旧错译"时常问自己是否在追寻真相"已消失。
b0001 | 2（左页第2段末句 take it to my grave） | PASS | 「真相令我震惊，而我至今还没向任何人提起。或许我会把这个秘密一直带进坟墓。」 | 与 EN `I might take it to my grave` 对应；"陷入万劫不复"已消失。
b0001 | 3（左页第3段过去时） | PASS | 「这并非我所预料的真相，却深深地震撼了我。父亲当时正在执行一项重要任务。身为他的儿子，我觉得自己有责任帮他把这项任务完成。」 | "当时正在执行"为过去时/参与执行；EN `My Father was in the middle of an important task`；"正处于任务核心"已消失。
b0004 | 4（lash out 反义） | PASS | 「倘若灵界突然发难，让我们变得充满攻击性，甚至更糟，会怎样？」 | EN `What if the realm of spirits were to lash out, and make us aggressive, or worse?`；"任由其发展"已消失。
b0004 | 5（bend to their will 反义） | PASS | 「倘若它们正潜移默化地影响我们的思想，使我们逐渐屈从于它们的意志，又会怎样？到那时，它们岂不是能任意驱使我们？」 | EN `conditioning our minds to slowly bend to their will`；"偏离我们的意志"已消失。
b0005 | 6（assume 一次死亡 = 瓦利诺斯，新更准） | PASS | 「很多时候，细节会被忽略，只有整体画面受到采信。以死亡为例，我们只能推断瓦利诺斯即将有人死亡，几乎无法深入探究为何会发生。」 | 瓁利诺斯仍是"死亡将至"的确定地点，判定核心在；较 1a 记录文本又精简了无据增译"却无法确定是谁"，更贴 EN `we would only assume a death is coming to Valinorth`，不改判定。
b0002 | 7（merely，判定=旧更准；与第 12 项同一条） | PASS（旧更准=旧图"只是"，现图"仅仅"已合判定） | 「关于阿莱斯蒂亚如何诞生，存在许多理论。这些理论都没有确凿的证据，仅仅建立在个人的信仰和确信之上。」（b0002 **左页**第 1 段） | 原工单把本条排在"b0005 右页"系定位笔误：已逐字核对英文原版 b0005 全两页，无 merely 一词（b0005 右页 `only the bigger picture` 一句判定为"两者皆可"，现图「只有整体画面受到采信」相符）。本条实为 b0002 左页第 1 段，按 1a 第 12 行判定（旧更准：旧译"都只是…"为对、新译"大多"为错）核对，现图"仅仅"已合判定 → PASS；与第 12 项同条同结果。
b0005 | 8（末句 a thing of the past） | PASS | 「不过，灵体与我们联系、沟通的能力正随着时间逐渐增强。也许不久后，预视就会变得确凿明晰，而"解读"也将成为过去，不再有必要。」 | 已重译为"成为过去，不再有必要"＝不复存在类；两版旧错译"对过去的确切的事物/认知"均已消失，EN `and "interpretations" would become a thing of the past`。
b0006 | 9（corresponding / people of note） | PASS | 「我已经离开瓦利诺斯，并开始与马泽奥的一些重要人物通信。」 | EN `I've branched out of Valinorth and started corresponding with some people of note in Mazeo`；"通信"与"重要人物"均已到位，旧译"脱离…一些人接触"已不在。
b0007 | 10（左页第2段句首） | PASS | 「我们不去东冠，只因身体承受不住那里的严寒。不过，那是另一回事；这里我想谈谈瓦利诺斯特有的血叶。」 | EN `We don't venture into Eastcrown, simply because our bodies would not be able to handle it.`（英文无"并非因为……"前置否定、也无"胆怯"）；现图既无旧译"并非因为我们的身体无法承受其严寒"的反向表述，也已去掉中性补足"胆怯"，直接对应"身体承受不住酷寒"。
b0007 | 11（reach 影响范围） | PASS | 「但这种能量的影响范围并非无限，无法改变东冠更为寒冷的气候。」 | EN `But the reach of this energy is not infinite, and it cannot affect the colder climate seen in Eastcrown.`；译作"影响范围并非无限"，未译成储量义的"能量并非无穷无尽"。
b0002（追加） | 12（merely → 口径确认） | PASS | 「关于阿莱斯蒂亚如何诞生，存在许多理论。这些理论都没有确凿的证据，仅仅建立在个人的信仰和确信之上。」（**左页**第 1 段） | 上级已裁定以 `semantic_booknotes_1a.md` 为准（追加指令原口径写反）：1a 第 12 行判定「旧更准」——**旧译=「……不过都只是基于个人的信仰和观点，更多是出于个体的信念」为对，新译=「……不过大多基于个人信仰与观点」为错**（理由"英文 merely=只是；新译改'大多'把限定放宽"）。现图"仅仅建立在个人的信仰和确信之上"正对 EN `merely based on personal belief and the conviction of the individual`，且补回了 1a 指出曾丢失的 conviction＝"确信"，"大多"已不存在 → PASS（与第 7 项同条）。
b0005 | 13（often 频率信息，判定=旧更准） | PASS | 「当预视结束时，先知往往能清晰地回忆起整体画面，而较小的细节却会在传达过程中遗失。」 | EN `a Seer or Seeress can often vividly recall the bigger picture`；频率副词 **「往往」在位**（＝旧图"常常"一档），上一轮新版整词删除 often 的问题已修复；同行"细节却会在传达过程中遗失"对应 `smaller elements are lost in translation`，均合判定。

## 副作用检查（目视，不计入下方统计）

图 | 检查项 | 结果 | 说明
---|---|---|---
b0001 | 英文残留/错别字/压叠截断/行距溢出/署名/青绿 | PASS | 无英文残留；未见错别字；正文无压叠、截断或溢出，行距均匀；页码 ~1~/~2~；**署名**：英文原版右页本就无落款（标题 Mylus' Note 承担署名），新版同样无落款，与原文一致、非丢失；书外透明区目视干净，未见青绿残留。
b0004 | 同上 | PASS | 无英文残留；未见错别字；无压叠/溢出，行距正常；页码 ~1~/~2~；署名「——阿尔古斯·维勒尔」在（EN ~Algus Veilleur）；书外未见青绿残留（书缘灰白为纸边纹理）。
b0005 | 同上 | PASS | 无英文残留；未见错别字；无压叠/溢出；页码 ~1~/~2~；署名「~福泰姆~」在（EN ~Fortaime）；书外目视干净，未见青绿。
b0006 | 同上 | PASS | 无英文残留；未见错别字（"专政暴虐"属措辞生硬、非错字，1b 已记）；无压叠/溢出；页码 ~1~/~2~；署名「——瓦利诺斯长老」在（EN ~The Elder of Valinorth.）；右缘灰白斑为纸边，未见青绿残留。
b0007 | 同上 | PASS | 无英文残留；未见错别字；无压叠/溢出，行距正常；页码 ~1~/~2~；署名「——瓦利诺斯长老」在（EN ~The Elder of Valinorth）；未见青绿残留。
b0002 | 追加项（人名/署名/页码/青绿） | PASS | 标题及正文均作「阿莱斯蒂亚」；署名「——阿尔古斯·维勒尔」在；页码 ~1~/~2~ 正常；书外透明区目视干净，上一轮"大片青绿斑块"未再出现（本轮键控清理后）。

## 读图记录

- 13 次 read_image：12 次首读正常显示、sha256 与请求文件对应；第 13 次为 b0005 主动重读（第 13 项 often 复核），sha256 `683d753c…` 与首读一致、内容一致。全程无内容/文件名不符、无"图未显示"。
- 英文原版作基准逐句核对：b0001、b0002、b0004、b0005、b0006、b0007 各 1 张。

统计 PASS=13 FAIL=0 PARTIAL=0
