Winds of Change 简体中文补丁 v1.2.1（仅 PC / Steam 版）

完整说明见 README.md，用记事本也能直接阅读。

一键使用：
  安装补丁.cmd    备份原文件并安装中文补丁
  卸载补丁.cmd    从备份完整还原，删除新增文件
  检查补丁.cmd    体检：引擎版本、文件完整性、rpyc/rpy 配对

安装时会把即将被覆盖的 54 个原文件备份到：
  <游戏目录>\woc_zh_patch_backup\

卸载优先从这个备份还原，所以补丁包本身不需要携带游戏原文件；
安装后你自己改过的文件会被跳过而不是覆盖。

兜底办法：Steam -> 游戏属性 -> 已安装文件 -> 验证游戏文件完整性。

命令行（需要 Python 3.8+，只用标准库）：
  python tools\patch_tool.py install | uninstall | verify | check | backup | find
