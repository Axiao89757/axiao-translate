from tkinter import *


class Translator:
    def __init__(self):
        self.window = Tk()
        self.window.title('Google Translate')
        self.window.geometry('500x300')

        # 三个frame
        self.f_org = Frame(self.window)
        self.f_org.pack()
        self.f_btn = Frame(self.window)
        self.f_btn.pack()
        self.f_ed = Frame(self.window)
        self.f_ed.pack()

        # 两个scroller
        scl_org = Scrollbar(self.f_org)
        scl_ed = Scrollbar(self.f_ed)

        # 原文文本框
        self.label_org = Label(self.f_org, text="原文")
        self.label_org.pack(side=LEFT)
        self.t_org = Text(self.f_org, height=5, wrap=WORD)
        self.t_org.pack()

        # 按钮
        self.b_en2ch = Button(self.f_btn, text='英 to 中', width=10, height=1, command=self.translate())
        self.b_en2ch.pack()

        # 译文文本框
        self.label_org = Label(self.f_ed, text="译文")
        self.label_org.pack(side=LEFT)
        self.t_ed = Text(self.f_ed, height=5, wrap=WORD)
        self.t_ed.pack()

        self.window.mainloop()

    def translate(self):
        var = self.t_org.get('1.0', '6.0')
        self.t_ed.insert(END, var)


translator = Translator()

