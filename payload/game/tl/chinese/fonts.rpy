# Winds of Change 中文补丁 —— 中文字体
#
# 本补丁不再新增字体文件, 而是直接替换游戏原版字体 game/gothic.ttf
# (换成 Sarasa UI SC 更纱黑体, 含完整中文字形, SIL OFL 1.1)。
# gui.rpy 原本就指向 "gothic.ttf", 因此无需任何字体覆写。
#
# 保留 config.allow_sysfonts 仅作兜底: 若某台机器上 gothic.ttf 被还原成原版
# (无中文字形), 引擎仍有机会在系统字体中寻找可用字体而不是直接报错。

init python:
    config.allow_sysfonts = True
