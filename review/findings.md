# 翻译校对预筛报告

生成时间: 2026-09-22 20:35

扫描条目: 11623; 候选问题: 91

| 等级 | 规则 | 数量 | 说明 |
| --- | --- | --- | --- |
| high | key-leak | 1 | 译文混入内部键号/英文角色名 |
| term | term-blade | 2 | 术语不一致 |
| term | term-blades | 1 | 术语不一致 |
| term | term-exodus | 2 | 术语不一致 |
| term | term-sword | 1 | 术语不一致 |
| low | ascii-residue | 37 | 残留英文单词 |
| low | halfwidth-punct | 3 | 半角标点 |
| low | length-ratio | 12 | 长度异常 |
| low | repeated-char | 14 | 重复用字 |
| info | engine-string | 18 | 引擎内置串 (正常) |

---

## [high] key-leak — 1 条

- `dialogue_0020.tsv#7896` char_damek
  - 原文: Damek: z01605\nShould we continue the rest on the ship?\nThere's sitll a few people you need to meet.\nAfter that, we're
  - 现译: Damek: z01605\n剩下的要不要到船上再说？\n还有几个人你得见一见。\n之后，我们就要踏上漫长又无聊的旅程了。
  - 说明: 译文里混入了内部键号或英文角色名

## [term] term-blade — 2 条

- `dialogue_0001.tsv#100` 
  - 原文: To break the deadlock, Ulric kicks his opponent in the gut.{w}\nThey stumble back, and ready their blade with a flourish
  - 现译: 为了打破僵局，乌尔里克一脚踹在对手的腹部。{w}\n那人踉跄着后退，炫技般重新举起兵器。{w}\n没过多久，他们又朝他冲了过来。
  - 说明: 术语 blade 应为「剑」
- `dialogue_0007.tsv#2702` char_sovy
  - 原文: The most important thing on my mind, is \"why\"...?\nWhy did you welcome me with open arms after what I did?\nI feel lik
  - 现译: 我心中最重要的问题，就是“为什么”……？\n在我做了那些事之后，你为什么还张开双臂欢迎我？\n我觉得任何有点常识的人都会把我处死。
  - 说明: 术语 blade 应为「剑」

## [term] term-blades — 1 条

- `dialogue_0026.tsv#10202` char_mylus
  - 原文: We might be a bit behind, but we'll meet in Mazeo.\nThere's lots to plan, and little time to plan it.\nWe'll need new ho
  - 现译: 我们或许会落后一些，但会在马泽奥会合。\n要筹划的事很多，时间却很少。\n我们需要新家园，还要为志愿者备好兵器。
  - 说明: 术语 blades 应为「剑」

## [term] term-exodus — 2 条

- `dialogue_0026.tsv#10020` char_fortaime
  - 原文: Or maybe it's a title for whoever wields it.\nYou know, something like Seer or Seeress.\nWhat about it...? Should we cal
  - 现译: 或者是持有者的称号。\n你知道的，就像先知那样的名号。\n怎么样……？要不我们叫你“流亡”？
  - 说明: 术语 Exodus 应为「放逐」
- `dialogue_0026.tsv#10023` char_valessa
  - 原文: Yeah, especially if The Triumvirate wants it back.\nWalking around as Exodus would put a huge target on us.\nThat's not 
  - 现译: 是啊，尤其三人执政团还想把它夺回去。\n顶着“流亡”的名号到处走，会让我们成为活靶子。\n想融入人群，我们可负担不起这个。
  - 说明: 术语 Exodus 应为「放逐」

## [term] term-sword — 1 条

- `dialogue_0023.tsv#9027` char_ulric
  - 原文: Obviously I'm a little older. I wasn't a victim of The Occupation.\nWhen it happened, I was just arriving in Mazeo to se
  - 现译: 显然我年纪大一些。我不是占领的受害者。\n那件事发生时，我刚抵达马泽奥，准备当佣兵卖命。\n一有机会我就从阿拉林西亚搬到了这里。
  - 说明: 术语 sword 应为「剑」

## [low] ascii-residue — 37 条

- `dialogue_0020.tsv#7896` char_damek
  - 原文: Damek: z01605\nShould we continue the rest on the ship?\nThere's sitll a few people you need to meet.\nAfter that, we're
  - 现译: Damek: z01605\n剩下的要不要到船上再说？\n还有几个人你得见一见。\n之后，我们就要踏上漫长又无聊的旅程了。
  - 说明: 残留英文单词: Damek
- `strings_0003.tsv#926` 
  - 原文: Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]
  - 现译: 使用 {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only] 制作。\n\n[renpy.license!t]
  - 说明: 残留英文单词: Ren
- ... 其余 35 条见 candidates.tsv

## [low] halfwidth-punct — 3 条

- `dialogue_0020.tsv#7896` char_damek
  - 原文: Damek: z01605\nShould we continue the rest on the ship?\nThere's sitll a few people you need to meet.\nAfter that, we're
  - 现译: Damek: z01605\n剩下的要不要到船上再说？\n还有几个人你得见一见。\n之后，我们就要踏上漫长又无聊的旅程了。
  - 说明: 中文里出现半角 , ; : ! ?
- `strings_0003.tsv#930` 
  - 原文: {#file_time}%A, %B %d %Y, %H:%M
  - 现译: {#file_time}%Y年%m月%d日 %H:%M
  - 说明: 中文里出现半角 , ; : ! ?
- ... 其余 1 条见 candidates.tsv

## [low] length-ratio — 12 条

- `dialogue_0026.tsv#10147` char_valessa
  - 原文: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 现译: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 说明: 长度比 1.00 偏离常规
- `dialogue_0026.tsv#10148` char_fortaime
  - 原文: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 现译: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 说明: 长度比 1.00 偏离常规
- ... 其余 10 条见 candidates.tsv

## [low] repeated-char — 14 条

- `dialogue_0003.tsv#897` 
  - 原文: He's almost cryptically telling me what I already know.{w}\nI know that the blade deals with the spirits of its victims.
  - 现译: 他几乎是在隐晦地告诉我我早已知道的事。{w}\n我知道那把剑会摆布受害者的灵。{w}\n三人执政团曾用它制造出他们自己的庞大军队。
  - 说明: 可能重复用字: 我我
- `dialogue_0007.tsv#2485` char_pro
  - 原文: Yeah, but it's not just Alarinthia, Valessa.\nYou could say that about this entire war in general.\nSometimes it's bette
  - 现译: 是啊，但不止是阿拉林西亚，瓦莱莎。\n整场战争都可以这么说。\n有时候，把别人看作“达到目的的手段”会更好。
  - 说明: 可能重复用字: 的的
- ... 其余 12 条见 candidates.tsv

## [info] engine-string — 18 条

- `strings_0003.tsv#933` 
  - 原文: {#auto_page}A
  - 现译: {#auto_page}A
  - 说明: 引擎内置字符串, 通常保留原文
- `strings_0003.tsv#934` 
  - 原文: {#quick_page}Q
  - 现译: {#quick_page}Q
  - 说明: 引擎内置字符串, 通常保留原文
- ... 其余 16 条见 candidates.tsv

