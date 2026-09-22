Winds of Change 中文补丁 v1.1.0

完整说明见 README.md（用记事本或任意文本编辑器可直接阅读）。

快速使用：
  安装补丁.cmd    备份原文件并安装中文补丁
  卸载补丁.cmd    从备份还原，删除新增文件
  检查补丁.cmd    体检：引擎版本 / 文件完整性 / 与安卓工程同步状态

安装时会把即将被覆盖的 56 个原文件备份到：
  <游戏目录>\woc_zh_patch_backup\
卸载时从该备份还原，因此补丁包本身不需要携带游戏原文件。

彻底兜底：Steam -> 游戏属性 -> 已安装文件 -> 验证游戏文件完整性。

命令行（需要 Python 3.8+，仅用标准库）：
  python tools\patch_tool.py install|uninstall|verify|check|backup|find
  python tools\fetch_renpy_sdk.py --list
