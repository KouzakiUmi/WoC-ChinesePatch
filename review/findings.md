# 翻译校对预筛报告

生成时间: 2026-09-22 21:07

扫描条目: 11623; 候选问题: 85

| 等级 | 规则 | 数量 | 说明 |
| --- | --- | --- | --- |
| term | term-blade | 2 | 术语不一致 |
| term | term-blades | 1 | 术语不一致 |
| term | term-sword | 1 | 术语不一致 |
| low | ascii-residue | 36 | 残留英文单词 |
| low | halfwidth-punct | 2 | 半角标点 |
| low | length-ratio | 12 | 长度异常 |
| low | repeated-char | 13 | 重复用字 |
| info | engine-string | 18 | 引擎内置串 (正常) |

---

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

## [term] term-sword — 1 条

- `dialogue_0023.tsv#9027` char_ulric
  - 原文: Obviously I'm a little older. I wasn't a victim of The Occupation.\nWhen it happened, I was just arriving in Mazeo to se
  - 现译: 显然我年纪大一些。我不是占领的受害者。\n那件事发生时，我刚抵达马泽奥，准备当佣兵卖命。\n一有机会我就从阿拉林西亚搬到了这里。
  - 说明: 术语 sword 应为「剑」

## [low] ascii-residue — 36 条

- `strings_0003.tsv#926` 
  - 原文: Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]
  - 现译: 使用 {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only] 制作。\n\n[renpy.license!t]
  - 说明: 残留英文单词: Ren
- `strings_0003.tsv#966` 
  - 原文: Escape
  - 现译: Escape
  - 说明: 残留英文单词: Escape
- `strings_0003.tsv#968` 
  - 原文: Ctrl
  - 现译: Ctrl
  - 说明: 残留英文单词: Ctrl
- `strings_0003.tsv#970` 
  - 原文: Tab
  - 现译: Tab
  - 说明: 残留英文单词: Tab
- `strings_0003.tsv#972` 
  - 原文: Page Up
  - 现译: Page Up
  - 说明: 残留英文单词: Page
- `strings_0003.tsv#974` 
  - 原文: Page Down
  - 现译: Page Down
  - 说明: 残留英文单词: Down,Page
- ... 其余 30 条见 candidates.tsv

## [low] halfwidth-punct — 2 条

- `strings_0003.tsv#930` 
  - 原文: {#file_time}%A, %B %d %Y, %H:%M
  - 现译: {#file_time}%Y年%m月%d日 %H:%M
  - 说明: 中文里出现半角 , ; : ! ?
- `strings_0003.tsv#1034` 
  - 原文: %b %d, %H:%M
  - 现译: %m月%d日 %H:%M
  - 说明: 中文里出现半角 , ; : ! ?

## [low] length-ratio — 12 条

- `dialogue_0026.tsv#10147` char_valessa
  - 原文: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 现译: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 说明: 长度比 1.00 偏离常规
- `dialogue_0026.tsv#10148` char_fortaime
  - 原文: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 现译: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 说明: 长度比 1.00 偏离常规
- `dialogue_0026.tsv#10195` char_valessa
  - 原文: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 现译: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 说明: 长度比 1.00 偏离常规
- `dialogue_0026.tsv#10196` char_fortaime
  - 原文: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 现译: {w=1.0}.{w=1.0}.{w=1.0}.{w}
  - 说明: 长度比 1.00 偏离常规
- `strings_0001.tsv#124` 
  - 原文: {image=icons/651.png} Yes
  - 现译: {image=icons/651.png} 是
  - 说明: 长度比 0.92 偏离常规
- `strings_0001.tsv#125` 
  - 原文: {image=icons/651.png} No
  - 现译: {image=icons/651.png} 否
  - 说明: 长度比 0.96 偏离常规
- ... 其余 6 条见 candidates.tsv

## [low] repeated-char — 13 条

- `dialogue_0003.tsv#897` 
  - 原文: He's almost cryptically telling me what I already know.{w}\nI know that the blade deals with the spirits of its victims.
  - 现译: 他几乎是在隐晦地告诉我我早已知道的事。{w}\n我知道那把剑会摆布受害者的灵。{w}\n三人执政团曾用它制造出他们自己的庞大军队。
  - 说明: 可能重复用字: 我我
- `dialogue_0007.tsv#2485` char_pro
  - 原文: Yeah, but it's not just Alarinthia, Valessa.\nYou could say that about this entire war in general.\nSometimes it's bette
  - 现译: 是啊，但不止是阿拉林西亚，瓦莱莎。\n整场战争都可以这么说。\n有时候，把别人看作“达到目的的手段”会更好。
  - 说明: 可能重复用字: 的的
- `dialogue_0009.tsv#3309` 
  - 原文: I laugh softly, and tell him he's not dead.{w}\nBut he seems to have me confused with Salus.
  - 现译: 我轻轻笑了笑，告诉他他没死。{w}\n但他似乎把我错认成了萨鲁斯。
  - 说明: 可能重复用字: 他他
- `dialogue_0012.tsv#4665` 
  - 原文: After a few hours of waiting, I almost can't handle it anymore.{w}\nIt's impossible for me to rest when my friends could
  - 现译: 等了几个小时后，我几乎再也受不了了。{w}\n朋友们可能身陷险境，我根本无法休息。{w}\n我朝出口走去，暗暗祈祷一切平安。
  - 说明: 可能重复用字: 了了
- `dialogue_0013.tsv#4828` char_valessa
  - 原文: Maybe not. We're here for a reason, remember?\nLet's find the owner, and see what they can tell us.
  - 现译: 还是别了。我们来这儿是有目的的，还记得吗？\n先找到这里的主人，看看他能告诉我们什么。
  - 说明: 可能重复用字: 的的
- `dialogue_0016.tsv#6268` 
  - 原文: I tell him that he can. He just needs to be brave enough.{w}\nThere may not be any music here, but I hold out my hands.{
  - 现译: 我告诉他他可以。他只需要鼓起勇气。{w}\n这里也许没有音乐，但我伸出了双手。{w}\n我问他是否愿意试一试。就在一切结束之前，试一次。
  - 说明: 可能重复用字: 他他
- ... 其余 7 条见 candidates.tsv

## [info] engine-string — 18 条

- `strings_0003.tsv#933` 
  - 原文: {#auto_page}A
  - 现译: {#auto_page}A
  - 说明: 引擎内置字符串, 通常保留原文
- `strings_0003.tsv#934` 
  - 原文: {#quick_page}Q
  - 现译: {#quick_page}Q
  - 说明: 引擎内置字符串, 通常保留原文
- `strings_0003.tsv#966` 
  - 原文: Escape
  - 现译: Escape
  - 说明: 引擎内置字符串, 通常保留原文
- `strings_0003.tsv#968` 
  - 原文: Ctrl
  - 现译: Ctrl
  - 说明: 引擎内置字符串, 通常保留原文
- `strings_0003.tsv#970` 
  - 原文: Tab
  - 现译: Tab
  - 说明: 引擎内置字符串, 通常保留原文
- `strings_0003.tsv#972` 
  - 原文: Page Up
  - 现译: Page Up
  - 说明: 引擎内置字符串, 通常保留原文
- ... 其余 12 条见 candidates.tsv

