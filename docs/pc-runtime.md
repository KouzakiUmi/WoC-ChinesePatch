# PC 补丁运行环境

本补丁只面向 Windows / Steam 版《Winds of Change》，目标引擎为 Ren'Py 7.1.1.929（Python 2.7）。

安装器会核对游戏脚本基线和引擎版本；任一项不匹配都会停止安装。补丁中的 `.rpyc` 由目标引擎编译，所有 `.rpyc` 都有配套的 `.rpy` 源码。

发布前运行：

```cmd
python tools\patch_tool.py check --no-game
python tools\patch_tool.py check --game-dir "<游戏目录>"
python tools\patch_tool.py verify --game-dir "<游戏目录>"
```

`check` 核对目标引擎、payload 文件及源码/编译文件配对；`verify` 核对已安装文件的哈希。
