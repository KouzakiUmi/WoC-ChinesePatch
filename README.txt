Winds of Change 简体中文补丁（仅 PC / Steam 版）
版本：v1.3.6
从 v1.3.5 及更早版本升级时，请先用旧版补丁卸载，再安装新版。

完整说明见 README.md，记事本可直接阅读。

无需 Python：下载并运行 WoC-ChinesePatch.exe（图形界面，含完整补丁数据）。
遇到问题时，可在窗口中打开调试日志并发给维护者。

源码目录内也可用以下脚本（需要 Python 3.8+）：
  安装补丁.cmd    备份原文件并写入中文补丁
  卸载补丁.cmd    从备份完整还原，删除新增文件，清理缓存
  检查补丁.cmd    体检：引擎版本 / 文件完整性 / rpyc-rpy 配对

备份位置：<游戏目录>\woc_zh_patch_backup\
卸载优先从该备份还原，因此补丁包本身不含游戏原文件；
安装后被你自己改过的文件会被跳过而不是覆盖。

兜底：Steam -> 游戏属性 -> 已安装文件 -> 验证游戏文件完整性。

命令行（需 Python 3.8+，仅用标准库）：
  python tools\patch_tool.py install | uninstall | verify | check | backup | find
