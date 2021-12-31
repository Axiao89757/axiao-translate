from tkinter import *
from tkinter.font import Font
import translate, utils, every_analysis_window as evr_anl_wd


class App:
    def __init__(self, root):
        self.root = root
        self.height = root.winfo_screenheight()
        self.width = root.winfo_screenwidth()
        self.org_is_en = True  # 交换功能所需字段
        # 记忆功能所需字段
        self.t_list_org = []  # 全部原始列表
        self.t_list_ed = []  # 全部译后列表
        self.t_cur_idx = 0  # 当前下标

        # frame
        self.f_org = Frame(root)
        self.f_btn = Frame(root)
        self.f_ed = Frame(root)

        # 标签
        self.l_org = Label(self.f_org, text="原文")
        self.l_ed = Label(self.f_ed, text="译文")

        # 按钮
        self.b_en2ch_clip = Button(self.f_btn, text='英to汉(剪切板)', width=13, height=1, fg="white", bg="ForestGreen",
                                   command=self.translate_en2ch_clip)
        self.b_en2ch = Button(self.f_btn, text='英to汉', width=8, height=1, command=self.translate_en2ch, fg="white",
                              bg="ForestGreen")
        self.b_every_anl = Button(self.f_btn, text='逐句分析', width=10, height=1, command=self.create_every_anl_wd,
                                  fg="white",
                                  bg="ForestGreen")
        self.b_wrap = Button(self.f_btn, text='↑↓', width=5, height=1, command=self.wrap)
        self.b_last = Button(self.f_btn, text='<', font=Font(weight="bold"), width=2, height=1, command=self.left,
                             state=DISABLED,
                             fg="ForestGreen")
        self.b_next = Button(self.f_btn, text='>', font=Font(weight="bold"), width=2, height=1, command=self.right,
                             state=DISABLED,
                             fg="ForestGreen")
        self.b_ch2en = Button(self.f_btn, text='汉to英', width=8, height=1, command=self.translate_ch2en)
        self.b_ch2en_clip = Button(self.f_btn, text='汉to英(剪切板)', width=13, height=1,
                                   command=self.translate_ch2en_clip)

        # 滑条
        self.scl_org = Scrollbar(self.f_org)
        self.scl_ed = Scrollbar(self.f_ed)

        # 文本框
        self.t_org = Text(self.f_org, wrap=WORD, height=12, font=("Times New Roman", 12))
        self.t_ed = Text(self.f_ed, height=12, font=("Times New Roman", 12))

        # 配置
        self.set_window()
        self.set_content()

    def set_window(self):
        self.root.title('笑翻')
        size_and_pos = str(int(0.35 * self.width)) + 'x' + str(int(0.5 * self.height)) + '+' + str(
            int(0.6 * self.width)) + '+' + str(int(0.2 * self.height))
        self.root.geometry(size_and_pos)
        self.root.iconbitmap('resources/icon.ico')
        self.root.wm_attributes('-topmost', 1)

        self.f_org.pack(expand=1)
        self.f_btn.pack(expand=1)
        self.f_ed.pack(expand=1)

    def set_content(self):
        # 原文标签
        self.l_org.pack(side=LEFT)
        # 原文文本框
        self.scl_org.config(command=self.t_org.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        self.t_org.config(yscrollcommand=self.scl_org.set)  # 将滚动条关联到文本框
        self.scl_org.pack(side=RIGHT, fill=Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
        self.t_org.pack(expand=1)

        # 译文标签
        self.l_ed.pack(side=LEFT)
        # 译文文本框
        self.scl_ed.config(command=self.t_ed.yview)
        self.t_ed.config(yscrollcommand=self.scl_ed.set)
        self.scl_ed.pack(side=RIGHT, fill=Y)
        self.t_ed.pack(expand=1)

        # 按钮
        self.b_en2ch_clip.pack(side=LEFT)
        self.b_en2ch.pack(side=LEFT)
        self.b_every_anl.pack(side=LEFT)
        self.b_wrap.pack(side=LEFT)
        self.b_ch2en.pack(side=LEFT)
        self.b_ch2en_clip.pack(side=LEFT)
        self.b_last.pack(side=LEFT)
        self.b_next.pack(side=LEFT)

    # 创建逐句分析窗口
    def create_every_anl_wd(self):
        # 句子翻译
        text_org = self.t_org.get('0.0', END).replace('\n', ' ').strip()
        if len(text_org) == 0:
            return
        text_ed = translate.translate(text_org, "zh-CN", "en")
        # 句子分割
        every_anl_org_list = utils.cut_sentences(text_org)
        every_anl_ed_list = utils.cut_sentences(text_ed)

        evr_anl_wd.EveryAnalysisWindow(self.root,
                                       str(int(0.35 * self.width)) + 'x' + str(int(0.4 * self.height)) + '+' + str(
                                           int(0.6 * self.width)) + '+' + str(int(0.23 * self.height)),
                                       every_anl_org_list, every_anl_ed_list)

    def text_list_append(self, text_org, text_ed):
        if len(self.t_list_org) > 0 and text_org == self.t_list_org[-1]:
            return
        self.t_list_org.append(text_org)
        self.t_list_ed.append(text_ed)
        t_cur_idx = len(self.t_list_org) - 1
        if t_cur_idx > 0:
            self.b_last.configure(state=NORMAL)
            self.b_next.configure(state=DISABLED)

    def update_text(self, text_org, text_ed):
        self.t_org.delete('1.0', END)
        self.t_org.insert(END, text_org)
        self.t_ed.delete('1.0', END)
        self.t_ed.insert(END, text_ed)

    def translate_en2ch(self):
        text = self.t_org.get('0.0', END).strip().replace('\n', ' ')
        if len(text) == 0:
            return
        result = translate.translate(text, "zh-CN", "en")
        self.update_text(text, result)
        self.text_list_append(text, result)

    def translate_ch2en(self):
        text = self.t_org.get('0.0', END).strip().replace('\n', ' ')
        if len(text) == 0:
            return
        result = translate.translate(text, "en", "zh-CH")
        self.update_text(text, result)
        self.text_list_append(text, result)

    def translate_en2ch_clip(self):
        text = self.root.clipboard_get().strip().replace('\n', ' ')
        if len(text) == 0:
            return
        result = translate.translate(text, "zh-CN", "en")
        self.update_text(text, result)
        self.text_list_append(text, result)

    def translate_ch2en_clip(self):
        text = self.root.clipboard_get().strip().replace('\n', ' ')
        if len(text) == 0:
            return
        result = translate.translate(text, "en", "zh-CH")
        self.update_text(text, result)
        self.text_list_append(text, result)

    def wrap(self):
        self.org_is_en = not self.org_is_en
        self.t_org.configure(wrap=WORD if self.org_is_en else CHAR)
        self.t_ed.configure(wrap=CHAR if self.org_is_en else WORD)
        text_ed = self.t_org.get('0.0', END).strip().replace('\n', ' ')
        text_org = self.t_ed.get('0.0', END).strip().replace('\n', ' ')
        self.update_text(text_org, text_ed)

    def left(self):
        self.t_cur_idx = self.t_cur_idx - 1
        self.b_next.configure(state=NORMAL)
        if self.t_cur_idx == 0:
            self.b_last.configure(state=DISABLED)
        self.update_text(self.t_list_org[self.t_cur_idx], self.t_list_ed[self.t_cur_idx])

    def right(self):
        self.t_cur_idx = self.t_cur_idx + 1
        self.b_last.configure(state=NORMAL)
        if self.t_cur_idx == len(self.t_list_org) - 1:
            self.b_next.configure(state=DISABLED)
        self.update_text(self.t_list_org[self.t_cur_idx], self.t_list_ed[self.t_cur_idx])
