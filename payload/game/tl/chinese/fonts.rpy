# Winds of Change 中文补丁 —— 中文字体
#
# 顺序: ① 随包 Sarasa UI SC (更纱黑体, SIL OFL 1.1) —— 保证任何机器都有中文字形
#       ② 系统字体兜底 (微软雅黑/等线/黑体/宋体; Noto Sans SC; 霞鹜文楷; 其他 Sarasa)
#
# 说明: renpy.text.font.load_face() 先在游戏目录找文件, 找不到才把传入字符串按逗号拆分到系统字体表匹配;
#       因此"随包字体优先 + 系统字体兜底"用两段式返回即可。gothic.ttf 不含中文字形, 不再作为兜底。

init python:

    config.allow_sysfonts = True

    _WOC_BUNDLED_FONT = "fonts/SarasaUiSC-Regular.ttf"

    _WOC_SYSTEM_FONTS = ",".join([
        "msyh.ttc", "msyhbd.ttc", "Deng.ttf", "simhei.ttf", "simsun.ttc",   # Windows
        "NotoSansSC-VF.ttf", "NotoSerifSC-VF.ttf",                          # Noto
        "LXGWWenKai-Regular.ttf",                                           # 霞鹜文楷
        "SarasaUiSC-Regular.ttf", "SarasaTermSC-Regular.ttf",               # 其他 Sarasa
        "NotoSansCJK-Regular.ttc", "NotoSansSC-Regular.otf",                # Android
        "DroidSansFallbackFull.ttf",
    ])

    def _woc_cjk_font():
        """随包 Sarasa 优先, 缺失时回退系统字体。"""
        if renpy.loadable(_WOC_BUNDLED_FONT):
            return _WOC_BUNDLED_FONT
        return _WOC_SYSTEM_FONTS


translate chinese python:

    gui.text_font = _woc_cjk_font()
    gui.name_text_font = _woc_cjk_font()
    gui.interface_text_font = _woc_cjk_font()
    gui.button_text_font = _woc_cjk_font()
    gui.choice_button_text_font = _woc_cjk_font()
