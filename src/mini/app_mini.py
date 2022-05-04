from tkinter import *
from tkinter import messagebox
import time
import translate, utils
from pynput import keyboard, mouse
from pynput.mouse import Controller

short_cut = [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]
short_cut_on_off = keyboard.Key.f8


class AppMini:
    def __init__(self, root):
        self.root = root

        # frame
        self.f_select = Frame(root)
        self.f_ed = Frame(root)

        # 选择开关
        self.on_off_val = BooleanVar()
        self.on_off_val.set(True)
        self.cb_on_off = Checkbutton(self.f_select, variable=self.on_off_val, text='开(F8)', onvalue=True, offvalue=False, command=self.on_off)

        # 换行开关
        self.line_on_off_val = BooleanVar()
        self.line_on_off_val.set(True)
        self.cb_line_on_off = Checkbutton(self.f_select, variable=self.line_on_off_val, text='格式化', onvalue=True, offvalue=False, command=self.line_on_off)

        # 滑条
        self.scl_ed = Scrollbar(self.f_ed)

        # 文本框
        self.t_ed = Text(self.f_ed, height=30, font=("Times New Roman", 12))

        # 配置
        self.set_window()
        self.set_content()

        # 监听器数据
        self.ms_moved = False  # 鼠标移动了
        self.translate_ready = False  # 翻译准备好了：1、鼠标移动了然后放开了 2、双击鼠标
        self.press_alt_time = None  # 按下翻译键盘的时间
        self.click_time = None  # 鼠标左键点击时间
        # 监听器
        self.mouse_listener = None
        self.keyboard_listener = None
        self.keyboard_listener_global = None
        self.set_listeners()

    def set_window(self):
        self.root.title('笑翻mini')
        self.root.geometry('300x200')
        # self.root.iconbitmap('./resources/icon.ico')
        self.root.state('iconic')

        self.f_select.pack(expand=1)
        self.f_ed.pack(expand=1)

    def set_content(self):
        # 启动开关
        self.cb_on_off.pack(side=LEFT)
        self.cb_line_on_off.pack(side=LEFT)

        # 译文文本框
        self.scl_ed.config(command=self.t_ed.yview)
        self.t_ed.config(yscrollcommand=self.scl_ed.set)
        self.scl_ed.pack(side=RIGHT, fill=Y)
        self.t_ed.pack(expand=1)

    def set_listeners(self):
        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_release=self.on_press)
        self.keyboard_listener_global = keyboard.Listener(on_release=self.on_press_global)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.keyboard_listener_global.start()

    def on_click(self, x, y, btn, is_press):
        # print(f"鼠标{btn}键在({x}, {y})处{'按下' if is_press else '松开'}")
        if str(btn) == 'Button.left':
            # 双击选择
            if self.click_time is not None and time.time() - self.click_time < 0.5:
                self.translate_ready = True
            self.click_time = time.time()

            # 鼠标抬起选择
            if not is_press:
                if self.ms_moved:
                    self.translate_ready = True
                self.ms_moved = False

    def on_move(self, x, y):
        # print(f"鼠标移动到: ({x}, {y})")
        self.ms_moved = True

    def on_press(self, key):
        # print(f"你松开了{key.char if hasattr(key, 'char') else key.name}键")
        if self.translate_ready and key in short_cut:
            if self.press_alt_time is not None and time.time() - self.press_alt_time < 0.5:
                utils.do_ctrl_c()
                time.sleep(0.01)  # 解决翻译时读取到的剪切板内容是第二新的，不是最新的
                self.translate()
                self.translate_ready = False
            self.press_alt_time = time.time()

    def on_press_global(self, key):
        # print(f"你松开了{key.char if hasattr(key, 'char') else key.name}键")
        if key == short_cut_on_off:
            self.on_off_val.set(not self.on_off_val.get())
            messagebox.showinfo('笑翻mini', '笑翻mini启动！！' if self.on_off_val.get() else '笑翻mini已经关闭')
            self.root.iconify()

    def stop_listeners(self):
        if self.mouse_listener is not None:
            self.mouse_listener.stop()

    def update_text(self, text_ed):
        self.t_ed.delete('1.0', END)
        self.t_ed.insert(END, text_ed)

    def translate(self):
        loading = '翻译中……'
        self.update_text(loading)
        self.pop_win()
        self.locate(loading)
        text = self.root.clipboard_get()
        text = text.strip().replace('\n', ' ') if self.line_on_off_val.get() else text
        print(text)
        if len(text) == 0:
            return
        result = translate.translate(text, "zh-CN", "en")
        self.update_text(result)
        self.locate(result)
        self.focus()

    def pop_win(self):
        self.root.state('normal')
        self.root.wm_attributes('-topmost', 1)
        self.root.wm_attributes('-topmost', 0)

    def locate(self, text):
        mouse_controller = Controller()
        pos = mouse_controller.position
        size = utils.adapt_size(text, self.line_on_off_val.get())
        x = pos[0] - int(int(size[0]) / 2)
        y = pos[1] + 20
        self.root.geometry('x'.join(size) + '+' + str(x) + '+' + str(y))

    def focus(self):
        mouse_controller = Controller()
        pos = mouse_controller.position
        mouse_controller.position = (pos[0], pos[1] + 30)
        mouse_controller.press(mouse.Button.left)
        mouse_controller.release(mouse.Button.left)

    def on_off(self):
        if not self.on_off_val.get():
            if self.mouse_listener is not None:
                self.mouse_listener.stop()
            if self.keyboard_listener is not None:
                self.keyboard_listener.stop()
        else:
            self.set_listeners()

    def line_on_off(self):
        text = self.root.clipboard_get()
        text = text.strip().replace('\n', ' ') if self.line_on_off_val.get() else text
        print(text)
        if len(text) == 0:
            return
        result = translate.translate(text, "zh-CN", "en")
        self.update_text(result)



