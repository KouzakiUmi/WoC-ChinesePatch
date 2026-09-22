# Winds of Change 中文补丁 —— 中文字体
#
# 不硬编码随包字体: 优先使用系统中文字体, 仅在系统字体不可用时才回退到
# 游戏目录里已有的 fonts/dengxian-regular.ttf (若存在)。
#
# 原理: renpy.text.font.load_face() 先在游戏目录找字体文件, 找不到就把传入
# 字符串按逗号拆开, 到系统字体表里按"文件路径后缀"匹配。
# 引擎默认 config.allow_sysfonts = False, 必须显式打开, 否则不会尝试系统字体。

init python:

    config.allow_sysfonts = True

    def _woc_cjk_font():
        """返回可用的字体名: 系统字体优先, 兜底用游戏目录内的字体。"""
        import renpy.text.font as _font
        system = ",".join([
            "msyh.ttc",        # Windows 微软雅黑
            "msyhbd.ttc",      # Windows 微软雅黑 Bold
            "Deng.ttf",        # Windows 等线
            "simhei.ttf",      # Windows 黑体
            "simsun.ttc",      # Windows 宋体
            "NotoSansCJK-Regular.ttc",   # Android
            "NotoSansSC-Regular.otf",    # Android (部分机型)
            "DroidSansFallbackFull.ttf", # Android (旧机型)
        ])
        try:
            _font.load_face(system)
            return system
        except Exception:
            # 系统字体都找不到时才用随游戏目录的字体
            return "fonts/dengxian-regular.ttf"


translate chinese python:

    gui.text_font = _woc_cjk_font()
    gui.name_text_font = _woc_cjk_font()
    gui.interface_text_font = _woc_cjk_font()
    gui.button_text_font = _woc_cjk_font()
    gui.choice_button_text_font = _woc_cjk_font()
