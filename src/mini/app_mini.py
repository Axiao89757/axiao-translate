from tkinter import *
import translate, utils
from pynput.keyboard import Listener
from threading import Thread
from pynput.mouse import Controller


class AppMini:
    def __init__(self, root):
        self.root = root

        # frame
        self.f_select = Frame(root)
        self.f_ed = Frame(root)

        # 选择开关
        self.var = IntVar()
        self.var.set(1)
        self.on = Radiobutton(self.f_select, text="开", variable=self.var, value=1, command=self.on_off)
        self.off = Radiobutton(self.f_select, text="关", variable=self.var, value=0, command=self.on_off)

        # 滑条
        self.scl_ed = Scrollbar(self.f_ed)

        # 文本框
        self.t_ed = Text(self.f_ed, height=30, font=("Times New Roman", 12))

        # 配置
        self.set_window()
        self.set_content()

        # 绑定快捷键
        self.listener = None
        self.tread = Thread(target=self.set_monitor)
        self.tread.start()

    def set_window(self):
        self.root.title('笑翻mini')
        self.root.geometry('300x200')
        self.root.iconbitmap('./resources/icon.ico')
        self.root.state('iconic')

        self.f_select.pack(expand=1)
        self.f_ed.pack(expand=1)

    def set_content(self):
        # 选择开关
        self.on.pack(side=LEFT)
        self.off.pack(side=LEFT)

        # 译文文本框
        self.scl_ed.config(command=self.t_ed.yview)
        self.t_ed.config(yscrollcommand=self.scl_ed.set)
        self.scl_ed.pack(side=RIGHT, fill=Y)
        self.t_ed.pack(expand=1)

    def set_monitor(self):
        with Listener(on_release=self.translate_en2ch_clip) as h:
            self.listener = h
            h.join()

    def stop_listen(self):
        if self.listener is not None:
            self.listener.stop()

    def update_text(self, text_ed):
        self.t_ed.delete('1.0', END)
        self.t_ed.insert(END, text_ed)

    def translate_en2ch_clip(self, key):
        if str(key) == r"'\x03'":
            loading = '翻译中……'
            pos = Controller().position
            self.update_text(loading)
            self.root.state('normal')
            self.root.wm_attributes('-topmost', 1)
            self.root.wm_attributes('-topmost', 0)
            self.root.geometry(utils.adapt_size(loading) + '+' + str(pos[0] + 10) + '+' + str(pos[1] + 10))
            text = self.root.clipboard_get().strip().replace('\n', ' ')
            print(text)
            if len(text) == 0:
                return
            result = translate.translate(text, "zh-CN", "en")
            self.update_text(result)
            self.root.geometry(utils.adapt_size(result))

    def on_off(self):
        num = self.var.get()
        if num == 0:
            if self.listener is not None:
                self.listener.stop()
        else:
            self.tread = Thread(target=self.set_monitor)
            self.tread.start()

