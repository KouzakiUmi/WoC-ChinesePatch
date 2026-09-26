# 教程图措辞语义复核（旧版 v1.3.7 vs 新版 v1.3.8，基准=英文原版）

- 英文原版来源：`tl_work\backup_images_2026-09-22_0430\game\images\`（tut001 774d6852…、tut003 ccc09ab1…、tut005 53568950…、tut006 ebeef1e2…，均清晰可读，无需备用件）
- 旧版：`_old_images\`（tut001 d0fb440d…、tut003 afe26452…、tut005 07862b60…、tut006 96334b73…）
- 新版：`payload\game\images\`（tut001 13fb322c…、tut003 4e378ad9…、tut005 14367e46…、tut006 c1131cee…）
- 各图 read_image 返回的 sha256 与所请求路径一致，无串图。

## 逐处差异

| 图 | 行/位置 | 旧译 | 新译 | 英文原句(关键片段) | 结论 |
|---|---|---|---|---|---|
| tut001 | 右上角提示 | 在任意地图点击此图标，可再次打开本教程。 | 点击任意地图上的此图标，可再次打开本教程。 | "Clicking this icon on any map will open this tutorial once more." | 两者皆可 |
| tut001 | 第1条（光标） | 你可以在画面中自由移动光标。 | 你可以在屏幕上自由移动光标。 | "You can freely move the cursor around the screen." | 两者皆可（screen 直译"屏幕"，游戏语境"画面"亦通） |
| tut001 | 第2条（悬停） | 当光标悬停在可互动的对象上时，它会改变。点击这些对象即可互动。 | 将光标悬停在可互动对象上时，光标会改变。点击这些对象即可与之互动。 | "It will change when you hover above an interactable object. Clicking on these objects will interact with them." | 两者皆可（新版重复"光标"指代更明，旧版"它"同样可解） |
| tut001 | 第4条（书籍） | 这些图标显示本区域书籍总数，以及你已找到的数量。 | 这些图标显示该区域的书籍总数以及你已找到的数量。 | "how many books are in the area and how many you've found" | 两者皆可（本/该区域同义） |
| tut001 | 第5条（世界地图） | 在可用时，此图标会带你前往世界地图。 | 此图标可用时，会带你前往世界地图。 | "This icon, when applicable, takes you to the world map." | 新更准（旧"在可用时"中文别扭，把 when applicable 挤成前置时间状语；新贴合原文插入结构） |
| tut001 | 第6条（存档） | 此图标会打开存档菜单。 | 此图标可打开存档菜单。 | "This icon opens the save menu." | 两者皆可（"会/可"差异极小） |
| tut001 | 右下角（区域导航） | 有些地点分为多个区域。点击这些箭头可在区域之间切换。 | 有些地区分为多个区域。点击箭头即可在区域间切换。 | "Some locales are divided into multiple areas. Click these arrows to navigate between them." | 两者皆可（locales 地点/地区两可；旧保留"这些"更贴 these arrows） |
| tut003 | 正文第2句 | 虽然故事从你的视角展开，但众多角色始终各有行动。 | 尽管故事从你的视角展开，众多角色也始终各有行动。 | "Though the story takes place from your perspective, the large cast of characters is always up to something." | 两者皆可 |
| tut003 | 中部（支线入口） | 在适用地图的左上角，点击角色图标即可查看支线剧情。 | 在相应地图的左上角，点击角色图标即可查看支线剧情。 | "In the top left of applicable maps, you can view subplots…" | 旧更准（applicable＝适用；"相应"偏离原义） |
| tut003 | 底部两行 | 你可以按任意顺序完成这些内容。但建议按照显示顺序进行。 | 这些支线可以按任意顺序完成。不过，建议按照它们出现的顺序进行。 | "You can do these in any order. But it is recommended to do them in the order you see them." | 新更准（these 明确回指 subplots；"order you see them"→"出现的顺序"更贴） |
| tut005 | 标题 | 纯洁与堕落 | 纯洁与腐化 | "Purity and Corruption" | 新更准（Corruption＝腐化，且与正文用词一致；"堕落"偏 fall/depravity） |
| tut005 | 正文第1行 | 在游戏过程中，你将作出许多重要决定。 | 在游戏过程中，你会作出许多重要决定。 | "you will make many important decisions" | 两者皆可（将/会，will 的两种译法） |
| tut005 | 正文第2行 | 这些决定会影响名为"纯洁与堕落"的隐藏数值。 | 这些决定会影响一项名为"纯洁与腐化"的隐藏数值。 | "These will increase a background stat known as purity and corruption." | 新更准（术语一致；注：两版都把 increase 弱化成"影响"，属共同不足） |
| tut005 | 正文第3行 | 你可以在存档界面查看这些数值。 | 你可以在存档界面查看这两项数值。 | "You can monitor these stats on the save screen." | 两者皆可（stats 指 purity/corruption 两项，"这两项"更明确，"这些"亦对应复数） |
| tut005 | 正文中段第1行 | 你的纯洁与堕落等级代表你在这个世界中的行事方式。 | 你的纯洁与腐化程度，体现了你在这个世界中的处世方式。 | "Your purity and corruption levels represent how you carry yourself in the world." | 新更准（术语；levels→等级/程度、carry yourself→行事/处世方式本身两可） |
| tut005 | 正文中段第3行 | 你的倾向会影响剧情与对话。 | 你的倾向会影响剧情和对话。 | "Your alignment will effect both story and dialogue." | 两者皆可（both…and→与/和） |
| tut005 | 正文底部行 | 你可以在游戏世界中点击纯洁／堕落图标，查看更多信息。 | 点击游戏中的纯洁/腐化图标，可了解更多信息。 | "You can click on purity/corruption icons in the game world for more information." | 新更准（术语） |
| tut005 | 右侧地图截图地名 | 保留英文 "TCROWN"（截图遮挡，原文可见 …CROWN） | 汉化为"东冠" | 地图截图内文字 "…CROWN"（英文原版即为英文） | 两者皆可（新版汉化对中文玩家更友好；建议与正文地名用字比对后定稿） |
| tut006 | 正文第1行 | 带有爱心标记时，与同伴交谈会开启特殊场景。 | 同伴标有爱心图标时，与其交谈便会触发特殊场景。 | "When marked with a heart, talking to a comrade starts a special scene." | 新更准（原文 when marked 主语含糊，新版补明"同伴标有爱心图标"；starts→触发更贴） |
| tut006 | 正文第2行 | 这些场景只能体验一次，作出的决定也无法更改。 | 每段场景只能体验一次，作出的选择也无法更改。 | "You can only play these once, and your decisions are final." | 两者皆可（decisions 决定/选择两可） |
| tut006 | 正文第3行 | 它们散布在游戏各处，必须按顺序完成。 | 这些场景散布于游戏各处，必须按顺序完成。 | "They are scattered through the game, and must be done in order." | 两者皆可 |
| tut006 | 底部第1行 | 这些场景是巩固友谊、发展恋情的关键。 | 这些场景对于巩固友谊、发展恋情至关重要。 | "These scenes are key to solidifying friendships and pursuing romance." | 两者皆可 |
| tut006 | 底部第2行 | 完成角色的心与心交谈，最终会解锁忠诚任务。 | 与角色完成心与心的交谈，最终会解锁忠诚任务。 | "Doing a character's heart-to-hearts will eventually unlock a loyalty quest." | 旧更准（do a character's heart-to-hearts＝完成"该角色的"心心，旧结构直接对应；新把 character 变成伴随对象，语义略偏） |

## 一致性专项核查

### 1) tut005 核心术语：图片该用「腐化」还是「堕落」
- 英文原版标题与正文均用 **Purity / Corruption**（"Purity and Corruption"、"a background stat known as purity and corruption"、"purity/corruption icons"）。
- 中文游戏正文用「纯洁与**腐化**」（对白 dialogue_0015 有 2 处，来自父任务报告）。
- 结论：**图片应采用「纯洁与腐化」**。旧版「纯洁与堕落」与正文不一致且偏离 Corruption 本义；新版改「腐化」→ **新更准**，涉及 4 处（标题、正文第2行、中段第1行、底部行）+ 1 处"等级/程度"行的术语部分。

### 2) 教程专有名词与正文一致性
- **阿莱斯蒂亚（Alestia）**：~~tut003 新旧两版均作「阿莱斯提亚」，两版图内一致，拼写与原文吻合~~ **【勘误】本条判错**：旧版作「阿莱斯**提**亚」（正是工单 A-3 要修的错字），**新版已改为「阿莱斯蒂亚」**——经 `verify_tutorials.md` 与主校对者本人读图两次确认，新版首行为"阿莱斯蒂亚是一个鲜活的世界。"。英文 "The world of Alestia"。故此处 **新更准、A-3 已修复**。
- **瓦莱莎（Valessa）**：仅旧版 tut006 中文截图出现「瓦莱莎」；新版该截图为英文，图内不再出现中文名。
- **佩雷格里诺（Peregrino）**：仅旧版 tut005 底部对话框出现「佩雷格里诺」；新版该框为英文，图内不再出现。
- **福泰姆**：本次四张教程图（tut001/003/005/006）中未出现该词，无法从图片侧核对。
- **限制说明**：本任务硬约束仅允许 read/read_image/write，无法用 grep/glob 检索正文；已尝试读取 `payload\game\dialogue_0015.txt/.rpy`、`tl_work\dialogue_0015.txt` 等若干路径均不存在。因此"图片名词 vs 正文用字"的逐字比对未能独立完成，正文术语依据父任务提供的 dialogue_0015 信息与英文原词判定；建议由具备检索工具的一方复核「阿莱斯提亚/瓦莱莎/佩雷格里诺/福泰姆」正文用字。

### 3) 对话框/截图新版是否为英文（独立复核）
- **tut005 底部两对话框**：英文原版为英文；旧版为中文（「这段队伍闲聊会受到你选择保留佩雷格里诺酒馆的影响。」「你选择保留佩雷格里诺，使其继续作为酒馆。」）；**新版为英文**（"This party banter is affected by your choice to keep Peregrino as a tavern." / "You chose to keep Peregrino intact, remaining as a tavern."）。→ **复核确认：新版是英文（回照英文原版，等于中文版残留未译文本）。**
- **tut006 中部对话截图**：英文原版为英文三句台词；旧版为中文（「当然。我们会一起面对一切。」「发掘内心的力量也很棒，瓦莱莎。」「只要你需要，我随时乐意帮忙。」）；**新版为英文**（"Of course. We'll handle everything together." / "Finding inner strength is also great, Valessa." / "I'm glad to help any time you need it."）。→ **复核确认：新版是英文。**
- 附带：tut005 右侧地图截图地名，旧版保留英文 "…CROWN"，新版汉化为「东冠」（与上述两处方向相反，属新增汉化）。

统计 新更准=7 旧更准=2 皆可=14 都不准=0
