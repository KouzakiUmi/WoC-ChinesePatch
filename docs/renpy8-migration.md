# Ren'Py 8 迁移：现状与补丁侧的应对

> 维护者笔记。**发布的 PC 补丁包不含本文档，也不含 `deps/`**；这里记录的是个人安卓构建环境与引擎版本的实测结论。

核对时间：2026-09-22。以下结论都来自对本机文件的实测，不是推测。

## 一、现状：三套树，两种引擎

| 位置 | 引擎 | Python | 角色 |
| --- | --- | --- | --- |
| `C:/SteamLibrary/steamapps/common/winds-of-change` | Ren'Py 7.1.1.929 | 2.7（`lib/pythonlib2.7`） | PC 端游戏本体，补丁的目标 |
| `C:/renpy8/renpy-8.6.0-sdk/winds-of-change` | Ren'Py 8.6.0.25112108 | 3.12（`lib/py3-*`） | 安卓构建工程 |
| `C:/renpy-android/renpy-7.8.7-sdk` | Ren'Py 7.8.7.25031702 | 2.7（`lib/py2-*`） | 旧安卓管线，已被上面取代 |

安卓构建脚本 `C:/renpy8/build8.cmd`：设 `JAVA_HOME` 指向 JDK 21，调用 launcher 的 `android_build` 子命令，产物输出到 `C:/renpy8/dist`。最近一次产物 `com.fractal.windsofchange-1.0-1790040365-release.apk`（917,910,310 字节，2026-09-22 09:27:05）。

**所以"迁移到 Ren'Py 8"不是安卓独有的事，而是安卓侧已经完成、PC 侧还没做。** PC 端游戏本体仍跑在 Ren'Py 7.1.1 上，本补丁的 `payload` 就是针对它构建并验证的。

## 二、补丁侧：已经是版本无关的

三点实测证据：

1. **`.rpyc` 都有配套 `.rpy`。** Ren'Py 的加载逻辑（`renpy/script.py` 的 `load_appropriate_file`）在 `.rpyc` 加载抛异常时会捕获并回退去编译同名 `.rpy`；当 `.rpy` 与 `.rpyc` 的 md5 不匹配时也直接编译 `.rpy`。因此即使把 7.1.1 编译的 `.rpyc` 放到 Ren'Py 8 下，最坏情况也只是重新编译一次。`patch_tool.py check` 会持续核对这个配对关系。

2. **安装器按引擎主版本决定是否投放 `.rpyc`。** `manifest.json` 里记录了 `compiled_with`（7.1.1.929 / Python 2）。目标引擎主版本不同时，安装器跳过全部 `.rpyc`，只放 `.rpy`，交给引擎自己编译；`verify` 读安装状态，不会把这些跳过的文件误报为缺失。两种场景都做过端到端测试：

   - Ren'Py 7.1.1 目标：安装 54 改 + 16 新，校验 70/70，卸载后 54 个文件与原版逐字节一致；
   - Ren'Py 8.6.0 目标：跳过 8 个 `.rpyc`，安装 54 改 + 8 新，校验 62/62，卸载同样逐字节还原。

3. **补丁内 `.rpy` 没有 Python 2 专有写法。** `check` 会扫描 `.rpy` 的 `python` 块与 `$` 行，匹配 `.iteritems()`、`.has_key()`、`unicode(`、`xrange(`、`print` 语句等。当前结果：未发现。

另外，安卓工程与 `payload` 的源文件已逐字节一致（62/62，0 分叉，0 缺失）；8 个 `.rpyc` 中 7 个不同属正常，因为两边引擎的 Python 版本不同、各自编译。

## 三、真正的迁移工作量在游戏本体，不在补丁

补丁只覆盖它拥有的文件（翻译、图片、`gui.rpy`、`screens.rpy`、语言切换、标题粒子）。要把 PC 端也搬到 Ren'Py 8，需要处理的是游戏自带脚本：

- `game/script.rpy`、`game/options.rpy`、`game/00saving.rpy`、`game/00cursors.rpy`、`game/00zoom_parallax.rpy`、`game/00main_menu_bg.rpy`、`game/zzversion.rpy`
- `game/screens.rpy` 里的自定义 Python（`FileJson`、`char_dict` 等存档界面逻辑）——这是 7.1 时代的写法，Python 3 下最容易出问题的地方
- 7.1 → 8.6 之间的屏幕语言与 `config.*` 变更

好消息是：安卓工程用同一份游戏脚本在 Ren'Py 8.6.0 上成功打出了 APK，说明这些脚本在 8 上至少能跑通。所以 PC 侧迁移的主要工作是换引擎运行时，而不是重写脚本。

## 四、PC 端迁移步骤（如需执行）

1. 获取 SDK：`python tools/fetch_renpy_sdk.py --channel stable`（8.5.3 稳定线）或复用本地 8.6.0 包（`--local`）。
2. 备份整个游戏目录；本补丁已安装的话，`<游戏目录>/woc_zh_patch_backup/` 里已有原文件备份。
3. 用 SDK 的 `renpy/`、`lib/`、可执行文件与启动脚本替换游戏目录中的同名部分。
4. 删除 `game/cache/`（7.1 写的是 `bytecode.rpyb`，8.x 用 `bytecode-312.rpyb` 这类带版本号的文件名，旧缓存不会被复用）以及全部 `.rpyc`。
5. 用 SDK 跑一次 `lint` 与 `compile`，按报错修 Python 2 残留。
6. 重装本补丁：`python tools/patch_tool.py install --force`。安装器会识别出 Ren'Py 8 并自动跳过 `.rpyc`。
7. 启动游戏确认中文、字体、对话框、语言切换、标题粒子都正常。

## 五、版本选择上的一个提醒

`8.6.0.25112108` 的构建号对应 2025-11-21，来自 master 分支（`renpy/vc_version.py` 里 `branch = 'master'`），且在 GitHub release 上没有对应资源；当前官方稳定版是 `8.5.3.26051504`（2026-05-15），比这个 8.6.0 快照更新。如果后续要长期维护安卓包，值得评估切到稳定线，避免踩到预发布版本里未修的问题。两者的下载地址与 sha256 都已写入 `deps/renpy.json`。

## 六、PC 与安卓在字体处理上的刻意差异（2026-09-23）

- **PC 端**：`tl/chinese/fonts.rpy` 采用**系统字体优先** —— 打开 `config.allow_sysfonts`，按候选列表匹配系统中文字体（Windows: `msyh.ttc` / `Deng.ttf` / `simhei.ttf` / `simsun.ttc`），仅当系统字体不可用时才回退到 `fonts/dengxian-regular.ttf`。
- **安卓端**：**有意保持**硬编码 `fonts/dengxian-regular.ttf`（随工程分发该字体），不启用系统字体回退 —— 安卓机型字体差异大，随包字体才能保证渲染一致。
- 因此同步补丁内容到安卓工程时，**不要覆盖 `game/tl/chinese/fonts.rpy`**，该文件在两端保持不同内容。

## 八、字体顺序最终确定 (2026-09-23)

- **顺序**：① 本地附带的中文字体 `fonts/dengxian-regular.ttf`（若存在）→ ② 系统字体（Windows 微软雅黑/等线/黑体/宋体；Android Noto CJK）。
- 不再回退到 `gothic.ttf`——它不含中文字形，只会显示方块。
- 该额外字体**不由补丁分发**（它是 Windows「等线」的副本，微软字体不可再分发）；干净安装自动走系统字体，两种路径都能正常渲染中文。
- **安卓端**仍固定使用随包 `fonts/dengxian-regular.ttf`，同步时不要覆盖 `tl/chinese/fonts.rpy`。
