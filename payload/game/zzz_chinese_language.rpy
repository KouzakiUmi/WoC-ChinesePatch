# Winds of Change 中文补丁 —— 语言设置与未覆盖字符串的运行时翻译
#
# 本文件由补丁新增, 不属于游戏原始文件; 卸载补丁时会被直接删除。
#
# 为什么需要它:
#   renpy.notify(...) 与 renpy.input(...) 收到的是裸 Python 字符串。
#   Ren'Py 的翻译提取只覆盖 say / menu / _() 包裹的字符串,
#   函数调用里的普通字符串不会被提取, 所以这些提示原本一直是英文。
#   下面把两个函数包一层, 让提示语先查字符串表 (translate chinese strings)。

define config.language = "chinese"

init python:

    _woc_orig_notify = renpy.notify

    def _woc_notify(message, *args, **kwargs):
        try:
            message = renpy.translation.translate_string(message)
        except Exception:
            pass
        return _woc_orig_notify(message, *args, **kwargs)

    renpy.notify = _woc_notify

    _woc_orig_input = renpy.input

    def _woc_input(prompt="", *args, **kwargs):
        try:
            prompt = renpy.translation.translate_string(prompt)
        except Exception:
            pass
        return _woc_orig_input(prompt, *args, **kwargs)

    renpy.input = _woc_input


translate chinese strings:

    old "Enjoy your adventure, and choose wisely..."
    new "祝你旅途愉快，谨慎抉择……"

    old "Use Enter or Left Click to advance text."
    new "按回车键或鼠标左键推进文本。"

    old "This choice will determine your gender."
    new "这个选择将决定你的性别。"

    old "Icons will display the tone of your response."
    new "图标会显示你回应的语气。"

    old "This choice will affect the flow of the story."
    new "这个选择会影响剧情的走向。"

    old "Choices can create meaningful bonds, and romances."
    new "选择可以缔结深厚的羁绊与恋情。"

    old "Use keyboard to enter name"
    new "请用键盘输入名字"

    old "You retain knowledge from any books you've read."
    new "你读过的书，知识都会保留下来。"

    old "You aren't knowledgable on this subject."
    new "你对这个主题并不了解。"

    old "Troop Morale is at 90 Percent."
    new "部队士气为 90%。"

    old "Troop Morale has risen to 100 Percent."
    new "部队士气已升至 100%。"

    old "Troop Morale has risen by 5 Percent."
    new "部队士气提升了 5%。"

    old "Troop Morale has risen by 10 Percent."
    new "部队士气提升了 10%。"

    old "Troop Morale has fallen to 50 Percent."
    new "部队士气已跌至 50%。"

    old "Troop Morale has fallen to 25 Percent."
    new "部队士气已跌至 25%。"

    old "Troop Morale has fallen to 0 Percent."
    new "部队士气已跌至 0%。"

    old "This choice will permanently alter your relationship with Fortaime."
    new "这个选择将永久改变你与福泰姆的关系。"

    old "This choice may permanently alter your relationship with Ulric."
    new "这个选择可能永久改变你与乌尔里克的关系。"

    old "This choice will permanently alter your relationship with Ulric."
    new "这个选择将永久改变你与乌尔里克的关系。"

    old "This choice will permanently alter your relationship with Pro."
    new "这个选择将永久改变你与普洛的关系。"

    old "This choice will permanently alter your relationship with Damek."
    new "这个选择将永久改变你与达梅克的关系。"

    old "This choice will permanently alter your relationship with Valessa."
    new "这个选择将永久改变你与瓦莱莎的关系。"

    old "This choice will change the future of Alestia."
    new "这个选择将改变阿莱斯蒂亚的未来。"

    old "This choice will affect the future of Alestia."
    new "这个选择会影响阿莱斯蒂亚的未来。"

    old "This choice will shape the future of Alestia."
    new "这个选择将决定阿莱斯蒂亚的未来。"

    old "This choice will change Alestia's future."
    new "这个选择将改变阿莱斯蒂亚的未来。"

    old "This choice will affect your future."
    new "这个选择会影响你的未来。"

    old "This speech is a culmination of all of your choices thus far."
    new "这段演说汇聚了你此前所有选择的成果。"

    old "You have earned Valessa's loyalty."
    new "你赢得了瓦莱莎的忠诚。"

    old "You have earned Fortaime's loyalty."
    new "你赢得了福泰姆的忠诚。"

    old "You have earned Pro's loyalty."
    new "你赢得了普洛的忠诚。"

    old "You have earned Ulric's loyalty."
    new "你赢得了乌尔里克的忠诚。"

    old "You have earned Damek's loyalty."
    new "你赢得了达梅克的忠诚。"

    old "You have earned Howl's loyalty."
    new "你赢得了豪尔的忠诚。"

    old "You have earned Sovy's loyalty."
    new "你赢得了索维的忠诚。"

    old "Your relationship with Sovy has changed."
    new "你与索维的关系发生了变化。"

    old "Click the idol to step toward it."
    new "点击灵像，朝它迈步。"

    old "Click the idol to walk toward it."
    new "点击灵像，向它走去。"

    old "Step toward the idol once more."
    new "再次朝灵像迈步。"

