# Winds of Change 中文补丁 —— 中文字体
#
# 顺序: ① 本地附带的中文字体(如 fonts/dengxian-regular.ttf) 优先
#       ② 缺失时回退到系统字体 (Windows 微软雅黑/等线/黑体/宋体; Android Noto CJK)
#
# 说明:
#   - 该额外字体文件不由本补丁分发, 仅当用户本地已有该文件时才会被使用; 干净安装会自动走系统字体。
#   - renpy.text.font.load_face() 先在游戏目录找文件, 找不到才把传入字符串按逗号拆分到系统字体表匹配,
#     因此"本地文件优先 + 系统字体兜底"用两段式返回即可实现。
#   - 引擎默认 config.allow_sysfonts = False, 必须显式打开才会尝试系统字体。

init python:

    config.allow_sysfonts = True

    _WOC_LOCAL_FONT = "fonts/dengxian-regular.ttf"

    _WOC_SYSTEM_FONTS = ",".join([
        "msyh.ttc",                  # Windows 微软雅黑
        "msyhbd.ttc",                # Windows 微软雅黑 Bold
        "Deng.ttf",                  # Windows 等线
        "simhei.ttf",                # Windows 黑体
        "simsun.ttc",                # Windows 宋体
        "NotoSansSC-VF.ttf",         # Noto Sans SC (OFL)
        "NotoSansCJK-Regular.ttc",   # Android
        "NotoSansSC-Regular.otf",    # Android (部分机型)
        "DroidSansFallbackFull.ttf", # Android (旧机型)
    ])

    def _woc_cjk_font():
        """本地附带中文字体优先, 缺失则回退系统字体。"""
        if renpy.loadable(_WOC_LOCAL_FONT):
            return _WOC_LOCAL_FONT
        return _WOC_SYSTEM_FONTS


translate chinese python:

    gui.text_font = _woc_cjk_font()
    gui.name_text_font = _woc_cjk_font()
    gui.interface_text_font = _woc_cjk_font()
    gui.button_text_font = _woc_cjk_font()
    gui.choice_button_text_font = _woc_cjk_font()
