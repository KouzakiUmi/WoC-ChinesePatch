# 图片译文语义判定 · 书籍笔记 b0014–b0017（新版 v1.3.8 vs 旧版 v1.3.7，英文原版为基准）

## 判读自检

- `tl_work\_orig_onblack\b0014.png` / `b0015.png` 均返回 not found（黑底合成件不存在），故直接读取英文原版 `tl_work\backup_book_notes_original_2026-09-22\`。实际英文图为书页彩色底、深色斜体字，清晰可判读，**不需标注"英文版看不清"**。
- 内容自检通过：英文 b0015 正文含 "Draycu"（标题 *Draycu's Reign*）；b0014=*On Sixers*、b0016=*The Evolution of Tournaments*、b0017=*The Grand Library*，与旧/新中文同名图标题一一对应。
- 全部 12 次 `read_image` 返回的 sha256 两两不同（英文 b0014=f93d…、b0015=1782…、b0016=407c…、b0017=5473…；旧版 b0014=b449…、b0015=8ff7…、b0016=39fc…、b0017=6b85…；新版 b0014=59ad…、b0015=c567…、b0016=87d1…、b0017=f60d…），无串图、无需重读。

---

## 逐条判定

**b0014 | 旧更准 | 英文原句**："Disposing of criminals before making them serve sentences, or deliver a more conventional means of justice was barbaric. At least, that's what the activists said." **旧译**："在将罪犯处死之前，也可以采用更传统的方式来处置他们，比如判处监禁或宣告更严厉的刑罚，这原本会更加人道。至少这是活动人士们的说法。" **新译**："处决罪犯，或是让他们服刑、以更常规的方式伸张正义，都被当年的倡导者视为野蛮。至少，他们是这么说的。" **理由**：英文谓语是 *was barbaric*，其主语是"**在让罪犯服刑／给予常规司法之前就处决他们**"这一行为——"野蛮"只指向"处决"，而"服刑、更常规的司法方式"恰是活动人士主张的替代方案。旧译虽把 *before* 处理成时间先后、并补出"监禁/更严厉刑罚"的例子，但极性和指向正确：处决不人道、常规方式更人道，与英文同义。新译用"**都**"把"处决罪犯""让他们服刑""以更常规的方式伸张正义"三者并列进"被视为野蛮"，等于宣称常规司法也是野蛮的——这与英文原意（只有 disposing 是 barbaric）字面相反，也与本段后文"这种做法被废止、改以竞技场决斗、被视为更公平"的语境冲突。故旧译更准（新译虽保住了"野蛮/倡导者"两个关键词，却把范围搞反）。

**b0015 | 旧更准 | 英文原句**："Every year, Draycu hosts a ball in his castle, and freely spreads his riches amongst the citizens of Alarinthia. That, coupled with his strength keeps most of his subjects happy." **旧译**："每年，德拉库都会在他的城堡中举办一场宴会，并慷慨地将财富分发给阿拉林西亚的民众。此举，再加上他强大的实力，使得他的臣民大多保持快乐。" **新译**："每年，德雷库都会在城堡设宴，并慷慨地把财富分给阿拉林西亚的民众。再加上他实力强大，大多数臣民都安于现状。" **理由**：*keeps most of his subjects happy* 直义为"使大多数臣民保持快乐/满意"，旧译逐字对应。新译改为"安于现状"，把情绪状态（happy）偷换成"满足现状、不求改变"的政治态度；而"不求改变/不愿生事"本是**下一段**的内容（*Many are less inclined to insurrection* → "许多人不愿发动叛乱"），新译使两段语义重复，削平了原文的递进。新译行文更顺，但相对英文有语义偏移，故旧更准（新译属可读的意译，非硬错）。

**b0016（"Champion"制度 4 处：斗士→勇士）| 两者皆可 | 英文原句**："This is when the 'Champion' system came into play. Each fighter would elect a champion to fight by their side. … They'd have to fight their enemy, and their enemy's champion, while also protecting themselves and their champion." **旧译**（4 处）："这就是'**斗士**'制度产生的时刻。每位战士都会被推选为己方的**斗士**。……与敌方**斗士**交战，同时也要保护自己和己方的**斗士**。" **新译**（4 处）："于是，'**勇士**'制度应运而生。每位参战者都会选出一名**勇士**并肩作战。……既要与敌人及敌方**勇士**交手，也要保护自己和己方**勇士**。" **理由**：*champion* 在此指"被选出与你并肩作战、还需你保护的人"，汉语无唯一对应词，"斗士"与"勇士"都是可行译法，二者均未改变人物关系与事实，属术语风格差异 → 两者皆可。附注：英文同段还区分 *fighter* 与末段 *warriors*，新译用"参战者/勇士/战士"三词分别对应，术语分工略清晰；旧译把 *fighter*、*warriors* 都译作"战士"，且"每位战士都会被推选为己方的斗士"误把 *would elect*（选出）译成被动"被推选"——但该语态问题不属于本次列出的"斗士→勇士"改动，故本条仍判两者皆可。

**b0016（"一些简单的战斗"→"生死相搏"）| 新更准 | 英文原句**："What started out as simple fights to the death have evolved into a full-on sport." **旧译**："比赛最初只是一些简单的战斗，但随着时间的推移，逐渐演变成了一项完整的运动。" **新译**："最初只是生死相搏，如今已演变为完整的竞技运动。" **理由**：原句含两个要素：*simple*（简单）与 *fights to the death*（至死方休）。旧译只保留"简单"，丢掉 *to the death*——而这正是与后文"演变成完整体育运动"形成对比的核心（从你死我活的搏杀 → 规则化竞技）。新译保留"生死相搏"，只弱化了 *simple*，且句中"只是"承接了"仅仅/原本只是"的意味。关键信息在新译中得以保留，故新更准（理想译法应兼含"简单"与"至死方休"）。

**b0016（"一位统治者"→"潜在统治者"）| 新更准 | 英文原句**："But citizens quickly realized that this was not the best way to gauge a **potential ruler's** true strength." **旧译**："但民众很快意识到，这并不是衡量**一位统治者**真正实力的最佳方式。" **新译**："但民众很快意识到，这并非衡量**潜在统治者**真正实力的最佳方式。" **理由**：*a potential ruler* 指"尚未成王的候选人"，旧译漏译 *potential*，变成"任一（现任）统治者"，与上下文"如何选拔未来统治者"不符；新译补出"潜在"，与原意一致。同段旧译首句另有主动/被动误译（英文 *rulers of Alarinthia were decided during a simple one-on-one battle* → 旧"阿拉林西亚的统治者**决定**通过简单的一对一战斗来选拔勇士"），新译改为"统治者**由**一场简单的一对一决斗**选出**"，同样更贴合原文，进一步支持新译。

**b0017 | 新更准 | 英文原句**："**Rumors of a mysterious man tending to the books are rampant.** Could such a collection really be under the watch of one individual?" **旧译**："关于一名神秘男子**试图接触那些书籍**的流言甚嚣尘上。这样一套藏书是否真的**由某个个人所拥有**？" **新译**："关于一名神秘男子**看守藏书**的传闻甚嚣尘上。如此庞大的藏书，真能**由一人看管**吗？" **理由**：*tending to the books* = 照料/打理藏书（守护者），*under the watch of one individual* = 由一人看守。旧译两处皆错：把 *tending* 误作"试图接触"（tend ≠ attempt to access），把 *under the watch* 误作"由……所拥有"，且与后文"除这位'神秘男子'外无人能进入图书馆"衔接不上。新译"看守藏书""由一人看管"与原文逐点对应，故新更准（"看守"较 *tending*（照料）略偏"守卫"，但整体语义链完整正确）。

---

## 附加检查（4 张新版图）

- **英文残留**：无。b0014–b0017 新版图的标题与正文均为中文，未见本应中文化的英文句子残留；页脚仅有页码符号 `~1~` / `~2~`。
- **错别字**：未发现明显错别字（如"拥入怀中""偏颇""甚嚣尘上""应运而生"等均正确）。
- **文字压叠**：未发现文字互相压叠、超出书页边界或行距异常；左右页排版均在书页范围内。
- **其他观察（不在工单改动清单内，供参考）**：
  1. 新版四图在预览中书页外为**纯黑背景**，旧版为**透明棋盘格**，疑似新版丢失透明通道（改黑底）；本回合禁止执行命令，无法用 alpha 检测确认，建议用可执行的工具复核（若游戏内为透明叠加显示，黑底会形成黑框）。
  2. 译名/标题变化：德拉库→**德雷库**（b0015，Draycu）、阿莱斯提亚→**阿莱斯蒂亚**（b0017，Alestia）、"论六日者"→"**论六时人**"（b0014，*On Sixers*，原文双关 six hours/six days，新旧各取其一）、"竞技大会的演变"→"**竞技赛制的演变**"（b0016，*The Evolution of Tournaments*）。这些改动未列入本次判定工单，未计入统计。
