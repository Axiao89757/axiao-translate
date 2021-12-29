from tkinter import Frame, Scrollbar, Label, Text, LEFT, WORD, RIGHT, Y, END, Button, Tk
import re
import html
from urllib import parse
from requests import get

# 翻译接口
GOOGLE_TRANSLATE_URL = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'


def translate(text, to_language="auto", text_language="auto"):
    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text, to_language, text_language)
    response = get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if len(result) == 0:
        return ""

    return html.unescape(result[0])


# 窗口程序
window = Tk()
window.title('Axiao Google Translate')
window.geometry('650x600')
window.wm_attributes('-topmost', 1)

# 三个frame
f_org = Frame(window)
f_org.pack(expand=1)
f_btn = Frame(window)
f_btn.pack(expand=1)
f_ed = Frame(window)
f_ed.pack(expand=1)

# 两个scroller
scl_org = Scrollbar(f_org)
scl_ed = Scrollbar(f_ed)

# 原文文本框
Label(f_org, text="原文").pack(side=LEFT)
t_org = Text(f_org, height=12, wrap=WORD)
scl_org.pack(side=RIGHT, fill=Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
scl_org.config(command=t_org.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
t_org.config(yscrollcommand=scl_org.set)  # 将滚动条关联到文本框
t_org.configure(font=("Times New Roman", 12))
t_org.pack()

# 译文文本框
Label(f_ed, text="译文").pack(side=LEFT)
t_ed = Text(f_ed, height=12)
scl_ed.pack(side=RIGHT, fill=Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
scl_ed.config(command=t_ed.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
t_ed.config(yscrollcommand=scl_ed.set)  # 将滚动条关联到文本框
t_ed.configure(font=("Times New Roman", 12))
t_ed.pack()


def translate_en2ch():
    text = t_org.get('0.0', END).replace('\n', ' ')
    result = translate(text, "zh-CN", "en")
    t_ed.delete('1.0', END)
    t_ed.insert(END, result)


def translate_ch2en():
    text = t_org.get('0.0', END).replace('\n', ' ')
    result = translate(text, "en", "zh-CH")
    print(text)
    print(result)
    t_ed.delete('1.0', END)
    t_ed.insert(END, result)


def translate_en2ch_clip():
    text = window.clipboard_get().replace('\n', ' ')
    t_org.delete('1.0', END)
    t_org.insert(END, text)
    result = translate(text, "zh-CN", "en")
    t_ed.delete('1.0', END)
    t_ed.insert(END, result)


def translate_ch2en_clip():
    text = window.clipboard_get().replace('\n', ' ')
    t_org.delete('1.0', END)
    t_org.insert(END, text)
    result = translate(text, "en", "zh-CH")
    t_ed.delete('1.0', END)
    t_ed.insert(END, result)


def wrap():
    text_org = t_org.get('0.0', END)
    text_ed = t_ed.get('0.0', END)
    t_org.delete('1.0', END)
    t_org.insert(END, text_ed)
    t_ed.delete('1.0', END)
    t_ed.insert(END, text_org)


# 按钮
b_en2ch = Button(f_btn, text='英 to 汉', width=10, height=1, command=translate_en2ch)
b_en2ch.pack(side=LEFT)
b_en2ch_clip = Button(f_btn, text='英 to 汉（剪切板）', width=20, height=1, command=translate_en2ch_clip)
b_en2ch_clip.pack(side=LEFT)
b_wrap = Button(f_btn, text='交换', width=10, height=1, command=wrap)
b_wrap.pack(side=LEFT)
b_ch2en = Button(f_btn, text='汉 to 英', width=10, height=1, command=translate_ch2en)
b_ch2en.pack(side=LEFT)
b_ch2en_clip = Button(f_btn, text='汉 to 英（剪切板）', width=20, height=1, command=translate_ch2en_clip)
b_ch2en_clip.pack(side=LEFT)

window.mainloop()
