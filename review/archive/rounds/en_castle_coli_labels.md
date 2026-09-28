# 英文原版地图房间标签抄录

## AlarinMapCastle.png（sha256 前12位 0d62d9b91971）
- 实际读取路径：`tl_work\backup_additional_text_images_2026-09-22\AlarinMapCastle.png`
  （任务给定的 `tl_work\backup_maps_original_2026-09-22\AlarinMapCastle.png` 不存在；该目录下只有
  AlarinMapCity / AlarinMapColi / AlarinMapDesert / BalteusMap1-3 / MazeoAreaMap / RebelHQMap /
  ValinorthAreaMap / ValinorthMap / WorldMap）
- 自检：图内含 `THRONE ROOM`、`CASTLE FRONT`，与文件名 Castle 相符 → 非串图
- 位置 | 英文原文
- 顶部中央 | THRONE ROOM
- 中部偏左 | BALLROOM
- 中部偏右 | **PRIVATE ROOM**
- 底部中央 | CASTLE FRONT
- 底部右侧 | EXIT
- 无 `TUNNEL` / `PASSAGE` / `CREW QUARTERS` 字样

## AlarinMapColi.png（sha256 前12位 145c4c99d8e6）
- 实际读取路径：`tl_work\backup_maps_original_2026-09-22\AlarinMapColi.png`
- 自检：图内含 `ARENA`、`MAIN ATRIUM`，与文件名 Coli（Coliseum）相符 → 非串图
- 位置 | 英文原文
- 左侧（竖排两行 PRIVATE / ROOM，合读为一个标签）| **PRIVATE ROOM**
- 中央圆场内 | ARENA
- 中央下方 | MAIN ATRIUM
- 底部 | OUTSIDE
- 右侧小圆区 | EXIT
- 右上角信笺、左下角信笺为手写花体装饰文字（不可读的装饰性书写体，非房间标签）
- 无 `TUNNEL` / `PASSAGE` / `CREW QUARTERS` 字样

## 判定
- Castle 房间标签原文 = `PRIVATE ROOM`（逐字；单数 ROOM，两词，非复数 ROOMS）
- Coli 房间标签原文 = `PRIVATE ROOM`（逐字；图中竖排两行 PRIVATE / ROOM）
- 两张图均**没有** `PERSONAL QUARTERS`，也**没有** `PRIVATE ROOMS`（复数）、`TUNNEL`、`PASSAGE`、`CREW QUARTERS`
- 结论：中文「私人房间」是否正确 = **正确**（原文是 PRIVATE ROOM，与总部图的 PERSONAL QUARTERS 不同词，
  无需改为「个人住所」）

## 读取备注
- 防串图：两次 read_image 返回的 sha256 分别为 Castle=0d62d9b91971…、Coli=145c4c99d8e6…，
  图内地名均与文件名自检项一致，未发生串图；无需重读。
- 工具说明：因给定路径下不存在 AlarinMapCastle.png，除 read_image / write 外另用了一次 glob
  仅用于定位文件名（未执行任何命令、未读取任何报告）。
