init 999 python:

    _zh_char_names = {
        "Valessa": u"瓦莱莎",
        "Valesa": u"瓦莱莎",
        "Ulric": u"乌尔里克",
        "Damek": u"达梅克",
        "Pro": u"普洛",
        "Sovy": u"索维",
        "Fortaime": u"福泰姆",
        "Howl": u"豪尔",
        "Halin": u"哈林",
        "Shane": u"肖恩",
        "Mylus": u"迈勒斯",
        "The Triumvirate": u"三人执政团",
        "Triumvir": u"执政官",
        "Honor Guard": u"荣誉卫队",
        "The Elder": u"长老",
        "Gryz": u"格瑞兹",
        "Alex": u"亚历克斯",
        "Nada": u"娜达",
        "Airen": u"艾琳",
        "Lillith": u"莉莉丝",
        "Vivien": u"薇薇安",
        "Draycu": u"德雷库",
        "Drayu": u"德雷乌",
        "Drakeor": u"德雷克",
        "Carmen": u"卡门",
        "Spice": u"斯派斯",
        "Zamira": u"扎米拉",
        "Kira": u"基拉",
        "Ignace": u"伊格纳斯",
        "Nyx": u"妮克斯",
        "Rygar": u"雷加",
        "Huskers": u"哈斯克",
        "Zorion": u"佐里昂",
        "Pommy": u"波米",
        "Vance": u"万斯",
        "Westy": u"韦斯蒂",
        "Laiki": u"莱基",
        "Saxxon": u"萨克斯顿",
        "Keaton": u"基顿",
        "Grayson": u"格雷森",
        "Algus": u"阿尔古斯",
        "Acheron": u"阿刻戎",
        "Brogatar": u"布罗加塔",
        "Cosmic": u"宇宙",
    }

    def _zh_char_name(s):
        try:
            if renpy.game.preferences.language == "chinese":
                return _zh_char_names.get(s, s)
        except Exception:
            pass
        return s

    _string_types = basestring

    try:
        for _sd in renpy.python.store_dicts.values():
            for _c in list(_sd.values()):
                if isinstance(_c, ADVCharacter) and getattr(_c, "dynamic", False):
                    _n = getattr(_c, "name", None)
                    if isinstance(_n, _string_types) and not _n.startswith("_zh_char_name("):
                        _c.name = "_zh_char_name(" + _n + ")"
    except Exception:
        pass
