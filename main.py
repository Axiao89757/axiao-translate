from tkinter import *
import re
import html
from tkinter.font import Font
from urllib import parse
from requests import get
import every_analysis_window as evr_anl_wd

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
height = window.winfo_screenheight()
width = window.winfo_screenwidth()
window.title('Axiao Google Translate')
window.geometry(str(int(0.35 * width)) + 'x' + str(int(0.5 * height)) + '+'
                + str(int(0.6 * width)) + '+' + str(int(0.2 * height)))
window.iconbitmap('icon.ico')
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

# 初始原文是英文
org_is_en = True
# 记忆存储
t_list_org = []
t_list_ed = []
t_cur_idx = 0
every_anl_list = []

# 原文文本框
Label(f_org, text="原文").pack(side=LEFT)
t_org = Text(f_org, wrap=WORD, height=12)
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
t_ed.pack(expand=1)


# 逐句分析
def every_anl():
    global every_anl_list


# 创建逐句分析窗口
def create_every_anl_wd():
    # 句子翻译
    text_org = t_org.get('0.0', END).replace('\n', ' ').strip()
    if len(text_org) == 0:
        return
    text_ed = translate(text_org, "zh-CN", "en")
    # 句子分割
    every_anl_org_list = cut_sentences(text_org)
    every_anl_ed_list = cut_sentences(text_ed)

    evr_anl_wd.EveryAnalysisWindow(window,
                                   str(int(0.35 * width)) + 'x' + str(int(0.4 * height)) + '+' + str(
                                       int(0.6 * width)) + '+' + str(int(0.23 * height)),
                                   every_anl_org_list, every_anl_ed_list)


# 分割句子
def cut_sentences(content):
    # 结束符号，包含中文和英文的
    end_flag = ['?', '!', '.', '？', '！', '。', '…']

    content_len = len(content)
    sentences = []
    tmp_char = ''
    for idx, char in enumerate(content):
        # 拼接字符
        tmp_char += char

        # 判断是否已经到了最后一位
        if (idx + 1) == content_len:
            sentences.append(tmp_char)
            break

        # 判断此字符是否为结束符号
        if char in end_flag:
            # 再判断下一个字符是否为结束符号，如果不是结束符号，则切分句子
            next_idx = idx + 1
            if not content[next_idx] in end_flag:
                sentences.append(tmp_char)
                tmp_char = ''

    return sentences


def text_list_append(text_org, text_ed):
    global t_list_org, t_list_ed, t_cur_idx
    if len(t_list_org) > 0 and text_org == t_list_org[-1]:
        return
    t_list_org.append(text_org)
    t_list_ed.append(text_ed)
    t_cur_idx = len(t_list_org) - 1
    if t_cur_idx > 0:
        b_last.configure(state=NORMAL)
        b_next.configure(state=DISABLED)


def update_text(text_org, text_ed):
    t_org.delete('1.0', END)
    t_org.insert(END, text_org)
    t_ed.delete('1.0', END)
    t_ed.insert(END, text_ed)


def translate_en2ch():
    text = t_org.get('0.0', END).strip().replace('\n', ' ')
    if len(text) == 0:
        return
    result = translate(text, "zh-CN", "en")
    update_text(text, result)
    text_list_append(text, result)


def translate_ch2en():
    text = t_org.get('0.0', END).strip().replace('\n', ' ')
    if len(text) == 0:
        return
    result = translate(text, "en", "zh-CH")
    update_text(text, result)
    text_list_append(text, result)


def translate_en2ch_clip():
    text = window.clipboard_get().strip().replace('\n', ' ')
    if len(text) == 0:
        return
    result = translate(text, "zh-CN", "en")
    update_text(text, result)
    text_list_append(text, result)


def translate_ch2en_clip():
    text = window.clipboard_get().strip().replace('\n', ' ')
    if len(text) == 0:
        return
    result = translate(text, "en", "zh-CH")
    update_text(text, result)
    text_list_append(text, result)


def wrap():
    global org_is_en
    org_is_en = not org_is_en
    t_org.configure(wrap=WORD if org_is_en else CHAR)
    t_ed.configure(wrap=CHAR if org_is_en else WORD)
    text_ed = t_org.get('0.0', END).strip().replace('\n', ' ')
    text_org = t_ed.get('0.0', END).strip().replace('\n', ' ')
    update_text(text_org, text_ed)


def left():
    global t_cur_idx
    t_cur_idx = t_cur_idx - 1
    b_next.configure(state=NORMAL)
    if t_cur_idx == 0:
        b_last.configure(state=DISABLED)
    update_text(t_list_org[t_cur_idx], t_list_ed[t_cur_idx])


def right():
    global t_cur_idx, t_list_org
    t_cur_idx = t_cur_idx + 1
    b_last.configure(state=NORMAL)
    if t_cur_idx == len(t_list_org) - 1:
        b_next.configure(state=DISABLED)
    update_text(t_list_org[t_cur_idx], t_list_ed[t_cur_idx])


# 按钮

b_en2ch_clip = Button(f_btn, text='英to汉(剪切板)', width=13, height=1, fg="white", bg="ForestGreen",
                      command=translate_en2ch_clip)
b_en2ch = Button(f_btn, text='英to汉', width=8, height=1, command=translate_en2ch, fg="white", bg="ForestGreen")
b_every_anl = Button(f_btn, text='逐句分析', width=10, height=1, command=create_every_anl_wd, fg="white", bg="ForestGreen")
b_wrap = Button(f_btn, text='↑↓', width=5, height=1, command=wrap)
b_last = Button(f_btn, text='<', font=Font(weight="bold"), width=2, height=1, command=left, state=DISABLED,
                fg="ForestGreen")
b_next = Button(f_btn, text='>', font=Font(weight="bold"), width=2, height=1, command=right, state=DISABLED,
                fg="ForestGreen")
b_ch2en = Button(f_btn, text='汉to英', width=8, height=1, command=translate_ch2en)
b_ch2en_clip = Button(f_btn, text='汉to英(剪切板)', width=13, height=1,
                      command=translate_ch2en_clip)

b_en2ch_clip.pack(side=LEFT)
b_en2ch.pack(side=LEFT)
b_every_anl.pack(side=LEFT)
b_wrap.pack(side=LEFT)
b_ch2en.pack(side=LEFT)
b_ch2en_clip.pack(side=LEFT)
b_last.pack(side=LEFT)
b_next.pack(side=LEFT)

window.mainloop()
