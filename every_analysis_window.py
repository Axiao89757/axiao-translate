from tkinter import *
from tkinter.font import Font


# 逐句分析窗口
class EveryAnalysisWindow:
    def __init__(self, root, size_and_pos, every_anl_org_list, every_anl_ed_list):
        self.root = Toplevel(root)
        self.size_and_pos = size_and_pos
        self.every_anl_org_list = every_anl_org_list
        self.every_anl_ed_list = every_anl_ed_list
        self.cur_inx = IntVar()
        self.cur_inx.set(1)
        # frame
        self.f_org = Frame(self.root)
        self.f_count = Frame(self.root)
        self.f_btn = Frame(self.root)
        self.f_ed = Frame(self.root)

        # 标签
        self.l_org = Label(self.f_org, text="原文")
        self.l_ed = Label(self.f_ed, text="译文")
        self.l_site = Label(self.f_count, textvariable=self.cur_inx,
                            font=Font(weight="bold"))
        self.l_site_sep = Label(self.f_count, text="/",
                                font=Font(weight="bold"))
        self.l_site_sum = Label(self.f_count, text=str(len(self.every_anl_org_list)),
                                font=Font(weight="bold"))

        # 按钮
        self.b_last = Button(self.f_btn, text='上一句', width=8, height=1,
                             command=self.on_click_last, state=DISABLED, fg="white", bg="ForestGreen")
        self.b_next = Button(self.f_btn, text='下一句', width=8, height=1,
                             command=self.on_click_next, fg="white", bg="ForestGreen")

        # 滑条
        self.scl_org = Scrollbar(self.f_org)
        self.scl_ed = Scrollbar(self.f_ed)

        # 文本框
        self.t_org = Text(self.f_org, wrap=WORD, height=9, font=("Times New Roman", 12))  # 原文文本框
        self.t_ed = Text(self.f_ed, height=9, font=("Times New Roman", 12))  # 译文文本框

        # 配置
        self.set_window()
        self.set_content()

    # 配置窗口
    def set_window(self):
        self.root.title('Every Analysis')
        self.root.geometry(self.size_and_pos)
        self.root.iconbitmap('icon.ico')
        self.root.wm_attributes('-topmost', 1)

        self.f_org.pack(expand=1)
        self.f_count.pack(expand=1)
        self.f_btn.pack(expand=1)
        self.f_ed.pack(expand=1)

    # 配置内容
    def set_content(self):
        # 原文标签
        self.l_org.pack(side=LEFT)
        # 原文文本框
        self.scl_org.config(command=self.t_org.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        self.t_org.config(yscrollcommand=self.scl_org.set)  # 将滚动条关联到文本框
        self.scl_org.pack(side=RIGHT, fill=Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
        self.t_org.pack()

        # 译文标签
        self.l_ed.pack(side=LEFT)
        # 译文文本框
        self.scl_ed.config(command=self.t_ed.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
        self.t_ed.config(yscrollcommand=self.scl_ed.set)  # 将滚动条关联到文本框
        self.scl_ed.pack(side=RIGHT, fill=Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
        self.t_ed.pack()

        self.update_text(self.every_anl_org_list[self.cur_inx.get() - 1],
                         self.every_anl_ed_list[self.cur_inx.get() - 1])

        # 标签
        self.l_site.pack(side=LEFT)
        self.l_site_sep.pack(side=LEFT)
        self.l_site_sum.pack(side=LEFT)

        # 按钮
        self.b_last.pack(side=LEFT)
        self.b_next.pack(side=LEFT)

    def on_click_last(self):
        print("last")
        if self.cur_inx.get() == 1:
            return
        self.b_next.configure(state=NORMAL)
        self.cur_inx.set(self.cur_inx.get() - 1)
        if self.cur_inx.get() == 1:
            self.b_last.configure(state=DISABLED)
        self.update_text(self.every_anl_org_list[self.cur_inx.get() - 1], self.every_anl_ed_list[self.cur_inx.get() - 1])

    def on_click_next(self):
        print("nest")
        if self.cur_inx.get() == len(self.every_anl_org_list):
            return
        self.b_last.configure(state=NORMAL)
        self.cur_inx.set(self.cur_inx.get() + 1)
        if self.cur_inx.get() == len(self.every_anl_org_list):
            self.b_next.configure(state=DISABLED)
        self.update_text(self.every_anl_org_list[self.cur_inx.get() - 1], self.every_anl_ed_list[self.cur_inx.get() - 1])

    def update_text(self, text_org, text_ed):
        self.t_org.delete('1.0', END)
        self.t_org.insert(END, text_org)
        self.t_ed.delete('1.0', END)
        self.t_ed.insert(END, text_ed)
