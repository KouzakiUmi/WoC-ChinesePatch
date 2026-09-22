# Winds of Change 中文补丁 —— 中文字体
#
# 补丁不随包分发任何字体文件, 中文一律使用系统中文字体。
#
# 原理: renpy.text.font.load_face() 先在游戏目录查找字体文件, 找不到就把传入
# 字符串按逗号拆分, 到系统字体表里按"文件路径后缀"匹配。
# 引擎默认 config.allow_sysfonts = False, 必须显式打开, 否则不会尝试系统字体。

init python:

    config.allow_sysfonts = True

    def _woc_cjk_font():
        """系统字体优先; 全部不可用时回退到本地/自带字体, 保证不会因缺字体而报错。"""
        import renpy.text.font as _font

        system = ",".join([
            "msyh.ttc",                  # Windows 微软雅黑
            "msyhbd.ttc",                # Windows 微软雅黑 Bold
            "Deng.ttf",                  # Windows 等线
            "simhei.ttf",                # Windows 黑体
            "simsun.ttc",                # Windows 宋体
            "NotoSansCJK-Regular.ttc",   # Android
            "NotoSansSC-Regular.otf",    # Android (部分机型)
            "DroidSansFallbackFull.ttf", # Android (旧机型)
        ])

        try:
            _font.load_face(system)
            return system
        except Exception:
            pass

        # 用户若自行在 game/fonts/ 放了中文字体, 用它
        if renpy.loadable("fonts/dengxian-regular.ttf"):
            return "fonts/dengxian-regular.ttf"

        # 最后退回游戏自带字体 (无中文字形, 但不会报错)
        return "gothic.ttf"


translate chinese python:

    gui.text_font = _woc_cjk_font()
    gui.name_text_font = _woc_cjk_font()
    gui.interface_text_font = _woc_cjk_font()
    gui.button_text_font = _woc_cjk_font()
    gui.choice_button_text_font = _woc_cjk_font()
