# Winds of Change — Android APK 移植进度

记录时间：2026-09-22

## 【已解决】崩溃根因与最终方案（2026-09-22）

### 根因：Ren'Py 7.8.x 引擎回归（非游戏问题、非内存不足）
- GitHub **renpy/renpy#6514**：「Bug - 7.8.7, Memory Leak During Playtest of Video Files」
  - 原文：*"This didn't happen in earlier versions of Ren'py 7, and **doesn't happen in Ren'py 8**"*
  - 另一位报告者：升到 7.8.7 后 Android/Windows 收到数百例 OOM，多层透明叠加场景内存飙到 26 GB；**升 Ren'Py 8 解决**
  - 7.x 已停止支持，官方不会回补
- 机制：7.8.x 的 gl2 纹理路径**每帧新建纹理，删除后显存不归还**（在 Adreno 830 上表现为 KGSL GfxDev 疯涨）
  - Ren'Py 侧释放逻辑正确：`Texture.__del__` → `free_list` → 每帧 `cleanup()` 调 `glDeleteTextures`
  - 手机 log 无 `Leaking texture:` 警告 → 泄漏在驱动/编译层，引擎侧 `free_memory()`/`kill_textures()` 无法回收
  - 实测：GfxDev 约 9 MB/帧、280 MB/s，开场演出 36 秒即达 10 GB 被 MIUI 杀掉

### 最终方案：升级到 Ren'Py 8.6.0
- 脚本 Python 3 兼容性已通过 `lint` 验证（游戏本体几乎无 Py2 语法）
- 需要的兼容改写（**仅语法/语义等价，不是 workaround**）：
  1. `00title_particles.rpy`：`iteritems()`→`items()`、`itervalues()`→`values()`、`lambda(k, v)`→`lambda kv: kv[0]`
  2. 同文件：`r.get_size()` / `child_render.get_size()` 结果转 `int()`（Ren'Py 8 返回 float）
  3. 同文件：`random.randrange(-config.screen_width / 2, ...)` → `// 2`（Py3 整数除法）
- **实测结果（手机 Adreno 830）**：连续运行 5+ 分钟，`Gfx dev` 稳定 ~6 MB、`TOTAL RSS` ~950 MB、无 swap 抖动；
  开场演出 + 后续对白全部通过，中文对白/名字框/选项/菜单正常，飘落树叶正常渲染

### 已还原的错误修复（重要，别再犯）
| 曾做过的改动 | 为什么错 |
|---|---|
| `00title_particles.rpy` 缓存 Transform | 没治住泄漏，还导致树叶不渲染 |
| `zzz_android_perf.rpy`（`gl_framerate=30`、`image_cache_size_mb=128`、`_gfx_cleanup`）| 缓存缩小反而**增加**淘汰-重传 churn；每 2 秒 `kill_textures()` 制造 alloc/free churn，实测无效 |
| SDK `renpy/display/core.py` 强制允许 GL1 渲染器 | 方向错误，安卓端 GL2 才是正路 |
以上均已还原，`00title_particles.rpy` 回到原始实现（仅保留上述 3 处 Py3 兼容改写）。

## 工具链（更新）
| 组件 | 版本 | 路径 |
|---|---|---|
| **Ren'Py SDK（当前使用）** | **8.6.0** | `C:\renpy8\renpy-8.6.0-sdk` |
| 工程副本 | | `C:\renpy8\renpy-8.6.0-sdk\winds-of-change` |
| 输出 APK | | `C:\renpy8\dist\` |
| 打包命令 | | `cmd /c "C:\renpy8\build8.cmd"` |
| （旧，已弃用）Ren'Py 7.8.7 | 有泄漏回归 | `C:\renpy-android\renpy-7.8.7-sdk` |

## 旧的排查记录（供参考，结论已被上面的方案取代）

把 Steam 版《Winds of Change》（Ren'Py 7.1.1 / Python 2 项目）打包成可在手机上自用的 APK。
不需要分发。

## 工具链（已搭好，免安装，全在 C:\renpy-android）
| 组件 | 版本 | 路径 |
|---|---|---|
| Ren'Py SDK | 7.8.7 | `C:\renpy-android\renpy-7.8.7-sdk` |
| RAPT | 7.8.7 | `C:\renpy-android\renpy-7.8.7-sdk\rapt` |
| JDK | Temurin 21 | `C:\renpy-android\jdk-21.0.12.1+1` |
| Android SDK | platform-tools + android-35 | `C:\renpy-android\renpy-7.8.7-sdk\rapt\Sdk` |
| 工程副本 | 游戏文件 | `C:\renpy-android\renpy-7.8.7-sdk\winds-of-change\game` |
| 输出 APK | | `C:\renpy-android\dist\` |

### 重新打包
```powershell
cmd /c "C:\renpy-android\build.cmd"
```
（`build.cmd` 里已设好 JAVA_HOME / RENPY_LOG_TO_STDOUT，并从中立目录运行避免遮蔽 SDK 的 renpy）

### 安装/测试（adb 无线调试）
```powershell
$adb="C:\renpy-android\renpy-7.8.7-sdk\rapt\Sdk\platform-tools\adb.exe"
& $adb connect 192.168.2.45:35805      # 端口每次开无线调试都会变
& $adb -s 192.168.2.45:35805 install -r <apk>
```
手机：Xiaomi 24129PN74C，Android 16，GPU Adreno 830，屏 2670x1200。

## 关键信息
- 游戏体积 2.24 GB，超过 APK 2GB 上限 → 已用 ffmpeg 重压音频：
  - `se/` 1710 MB → 412 MB（240kbps 单声道 → 约64kbps）
  - `bgm/` 188 MB → 91 MB
  - 工程 `game/` 现 818 MB，APK 873 MB
- 必须用 Ren'Py 7.x（Python 2），8.x 会大面积报错
- 安卓上 `config.gl2 = False` 无效：`renpy/display/core.py:1224` 会强制改回 `"auto"`
  → **已打补丁**：去掉该行的 `renpy.android`，这样 `preferences.renderer = "gles"` 才能生效

## 已解决的崩溃原因（重要）
### 1. 标题粒子系统显存泄漏（已修）
`game/00title_particles.rpy` 的 `ParticleDisplayable.render()` 每帧为每个粒子**新建 Transform**，
带 rotate/zoom 的 Transform 需要 render-to-texture → 每帧申请 GPU 缓冲。
- 现象：主菜单停留约 40 秒，`GfxDev` 涨到 **10 GB**，被 MIUI 内存管理杀掉
- 修复：改成只建一次 Transform，每帧改 `t.state.xzoom/rotate/alpha` + `renpy.display.render.invalidate(t)`
- 结果：主菜单显存稳定在 ~50 MB（已验证）
- ⚠️ 副作用待查：修复后截图里主菜单的飘落树叶似乎不再显示，需要复查

### 2. 开场演出（map004 TitleCrawl）仍泄漏（未解决）
- 现象：进入游戏后约 36 秒（开场第 4 行文字附近），`GfxDev` 涨到 **8~10 GB**，
  系统 thrashing（lowmemorykiller 报告 thrashing 89%）→ 连带杀掉其他 App 后杀掉游戏
- 日志证据：
  ```
  E/MIUIScout Memory: Name: com.fractal.windsofchange Rss=10532360kB GfxDev=10410524kB
  D/lowmemorykiller: thrashing (89%) ...
  I/lowmemorykiller: Kill 'com.xiaomi.xmsf:services' ... reason: free is low with low file page
  killProcess is called for pid : 22656   <- 我们的 App
  I/ActivityManager: Process com.fractal.windsofchange has died: fg TOP
  ```
- 排除项：
  - 不是音频（跳过图片演出时音频照常播放，不崩）
  - 不是 Python 异常（无 traceback.txt，日志停在 "Hid presplash."）
  - 不是物理内存不足（手机 16GB）
  - `kill_textures()` + `render.free_memory()` 每 2 秒调用一次**无效**
    → 说明不是 Ren'Py 的纹理/渲染缓存，而是 GPU 驱动层每帧约 10MB 的分配泄漏
- 估算：约 280 MB/s ≈ 30fps 下每帧 ~9MB（接近一个全屏 render target）
- 帧率修复有效但治标：日志确认 `swap interval: 4 frames`（30 FPS）已生效，
  把泄漏速度降到 1/4，但 90 秒的开场演出仍会累积到 10GB

## 已尝试的修复（按时间顺序）
1. `zzz_android_perf.rpy`：`gl_framerate = 30` + `image_cache_size_mb = 128`
   → 帧率生效（swap interval 4），但崩溃依旧
2. 粒子系统 Transform 复用 → 主菜单泄漏解决，开场仍崩
3. `cache_surfaces = True` + 每 2 秒 `kill_textures()` → 无效
4. **待测**：打补丁允许 GL1 渲染器 + `preferences.renderer = "gles"`
   → APK 已生成：`dist\com.fractal.windsofchange-1.0-1790026800-release.apk`（5:40:57）
   → 还没安装测试

## 下一步
1. 安装测试 GL1 版 APK（`1790026800`），看开场演出是否还崩
   - 若 GL1 也崩：考虑换 Ren'Py 7.4.4 重建（该版本 gl2 默认关闭）
   - 若 GL1 正常：复查粒子是否正常显示，再处理画面差异
2. 复查 `00title_particles.rpy` 的改动是否导致树叶不显示
3. 翻译侧遗留（见下）

## 翻译侧修复（已完成，2026-09-22）
依据审计报告 `C:\Users\Fractal\Documents\Codex\2026-09-22\jia\outputs\winds-of-change-zh-audit.md`
与候选清单 `zh_fix_candidates.tsv`，用 `tl_work\fix_audit.py` 一次性修复（改动只在 chunks 的 target 列）：

| 类别 | 数量 | 说明 |
|---|---|---|
| 人名冲突 | 151 + 6 | 维维安→薇薇安、格里兹→格瑞兹、艾伦→艾琳、普罗→普洛、德雷科尔→德雷克（+补漏 6 行 Airen）|
| 术语 | 70 + 157 | 流亡之刃/流放之刃→出埃及之刃；记录官/书记员/抄写员→书记官；灵魂神像/灵魂偶像/神灵像/灵偶/神像→灵像 |
| 引号 | 63 + 744 | 正文半角 `"…"`→`“…”`；strings 的 `\"…\"` 也统一为 `“…”` |
| 未译文本 | 16 | 6 个语气标签 `[[Sad]`→`[[悲伤]` 等；6 行 `View Parallel Chronicle …`→`查看平行编年史 …`；1 行 `Access Sovy Heart-to-Heart 1?`→`进入索维的谈心 1？` |
| 标签/空格 | 14 | 补回 3 处 `{i}` 强调标签；清理 11 行尾随空格 |
| 额外归一 | 35 | 审判庭（宗教裁判所/宗教审判庭）、王室（君主团/君主制）、斗士（救世主/勇士/冠军）、大迁徙→出埃及 |

**主菜单按钮（图片）也已汉化**：`game\images\main_menu\Command_0~2.png`
原本是英文烘焙图片（New Game / Continue / Options），已用 PIL 重制为
「新游戏 / 继续 / 选项」，保留原样式（粗体、青绿悬停/灰白常态渐变、深色描边），
上下两行结构（上=hover，下=idle）与尺寸（130/111/98 × 60）不变。
原图备份：`tl_work\backup_main_menu_original\`

### 校验结果（修复后）
- 少数派变体残留：全部 0
- 含 `idol` 的 198 行：196 行用「灵像」，1 行用「雕像」（该行原文是 statue，正确）
- 对话正文半角引号残留：0；strings 转义引号残留：0
- `{i}` 标签数量不一致的行：0
- 构建同步：PC 与安卓工程 `script.rpy` 字节数一致（4,545,770）
- `compile` 退出码 0，无 `errors.txt`

### 「Exodus」译名考证（2026-09-22，结论：维持「流亡」）
原文里 "Exodus" **不是历史事件**，而是**剑名 + 持剑者称号**（与 Seer/Seeress 同类）：
- `dialogue_0026` seq 10020：「Or maybe it's a title for whoever wields it. You know, something like Seer or Seeress. What about it...? Should we call you Exodus?」
- `dialogue_0026` seq 10023：「Walking around as Exodus would put a huge target on us.」
- `dialogue_0023` seq 8994：剑的来历在游戏内**没有解释**（"I have no idea where it came from"）

真正的历史事件叫 **The Occupation**（三人执政团占领马泽奥/瓦利诺斯，造成大量孤儿，现译「占领」，正确）。
**The Exodus Raid** 是二十年后孤儿军发动的**主动军事行动**（侦察+突袭），不是被动逃亡。

因此不能按「迁徙／被迫逃亡」翻。经确认维持：`流亡之刃` / 称号`流亡` / `流亡突袭` / `流亡理论`。

### 待定项
- **「教堂」22 行**：原文是 "The Triumvirate's Church"，`教堂`带基督教色彩。
  若要更贴奇幻设定，可换成 `圣殿` 或 `神殿`（改映射重跑即可，约 22 行）。
- 安卓工程已同步全部翻译修复与菜单图片，但 **APK 尚未重新打包**（按用户要求暂停 APK 排查）。

### 第二轮修复（P2/P3，2026-09-22）
用 `tl_work\fix_rem.py`：

| 问题 | 行数 | 处理 |
|---|---|---|
| `dialogue_0022` 目标列残留反斜杠 `\“...\”` | 24 | 去掉反斜杠 → `“...”`（`pair_quotes()` 只换了引号字符，漏了 `\`）|
| 引号方向反了（原文 key 引号数为奇数）| 5 | strings_0001 seq99、strings_0002 seq420/425/444/466 删掉末尾多余的 `“` |
| 「神像」漏网 | 8 | strings_0001 seq198/372、strings_0002 seq476/477/539/697/698、dialogue_0023 seq9194 → `灵像` |
| 半角单引号包裹中文 | 4 | strings_0002 seq418/624/743 → `‘…’`；seq733 `'流亡'突袭` → `流亡突袭` |

残留的 6 处半角单引号是 `Ren'Py`（引擎名，撇号必须保留）和 3 行自朗读快捷键提示（`'shift+C'`，PC 系统文本），合理保留。

### 终检（第二轮后）
反斜杠残留 0；`神像` 0 / `灵像` 206；`出埃及` 0；引号方向异常 0；
`{i}` 标签不一致 0；人名/术语少数派变体全部 0；PC 与安卓工程 `script.rpy` 一致（4,545,520 字节）。

### 注意
- `fix_audit.py` 会改写 chunks；若要回滚，用 `tl_work\chunks_bak_before_fix\`
- 安卓工程已同步修复后的 `tl/chinese/*.rpy` 与菜单图片，但**APK 尚未重新打包**
  （按你的要求先暂停），下次 `build.cmd` 即包含全部修复


## 相关文件清单
- 游戏本体（PC/Steam）：`C:\SteamLibrary\steamapps\common\winds-of-change`
- 翻译工具与分块：`tl_work\tl_tool.py`、`tl_work\chunks\`、`tl_work\template\`
- 安卓工程副本：`C:\renpy-android\renpy-7.8.7-sdk\winds-of-change\game`
- 原版开场图片备份：`tl_work\backup_crawl_original\`
