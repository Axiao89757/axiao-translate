from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time, base64, os
import translate, utils
from pynput import keyboard, mouse
from common import tooltip, icon

short_cut = [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]
short_cut_on_off = keyboard.Key.f8


class AppMini:
    def __init__(self, root):
        self.root = root

        # frame
        self.f_ed = Frame(root)

        # 菜单
        self.menu = Menu(self.root)
        # 1 设置菜单
        self.setting_menu = Menu(self.menu, tearoff=False)
        # 1.1 翻译开关
        self.on_off_val = BooleanVar()
        self.on_off_val.set(True)
        self.setting_menu.add_checkbutton(variable=self.on_off_val, label='开关', onvalue=True, offvalue=False, command=self.on_off, selectcolor='green', accelerator='F8')
        self.setting_menu.add_separator()
        # 1.2 自动复制
        self.auto_copy_menu = Menu(self.setting_menu, tearoff=False)
        self.copy_on_off_val = IntVar()
        self.copy_on_off_val.set(0)
        self.auto_copy_menu.add_radiobutton(label="关闭", variable=self.copy_on_off_val, value=0,  selectcolor='green')
        self.auto_copy_menu.add_radiobutton(label="原文", variable=self.copy_on_off_val, value=1,  selectcolor='green')
        self.auto_copy_menu.add_radiobutton(label="译文", variable=self.copy_on_off_val, value=2,  selectcolor='green')
        self.setting_menu.add_cascade(label='自动复制', menu=self.auto_copy_menu)
        # 1.3 删除换行
        self.line_on_off_val = BooleanVar()
        self.line_on_off_val.set(True)
        self.setting_menu.add_checkbutton(label='去除换行', variable=self.line_on_off_val, onvalue=True, offvalue=False, command=self.line_on_off, selectcolor='green')

        # 2 语言菜单
        self.lng_menu = Menu(self.menu, tearoff=False)
        # 2.1 源语言
        self.lng_s_menu = Menu(self.lng_menu, tearoff=False)
        self.lng_s_val = StringVar()
        self.lng_s_val.set('en')  # 默认英语
        self.lng_s_menu.add_radiobutton(label="中文", variable=self.lng_s_val, value='zh-CN')
        self.lng_s_menu.add_radiobutton(label="英语", variable=self.lng_s_val, value='en')
        self.lng_s_menu.add_radiobutton(label="日语", variable=self.lng_s_val, value='ja')
        self.lng_s_menu.add_radiobutton(label="德语", variable=self.lng_s_val, value='de')
        self.lng_s_menu.add_radiobutton(label="法语", variable=self.lng_s_val, value='fr')
        self.lng_s_menu.add_radiobutton(label="韩语", variable=self.lng_s_val, value='ko')
        self.lng_s_menu.add_radiobutton(label="自动", variable=self.lng_s_val, value='auto')
        # 2.2 目标语言
        self.lng_t_menu = Menu(self.lng_menu, tearoff=False)
        self.lng_t_val = StringVar()
        self.lng_t_val.set('zh-CN')  # 默认中文
        self.lng_t_menu.add_radiobutton(label="中文", variable=self.lng_t_val, value='zh-CN')
        self.lng_t_menu.add_radiobutton(label="英语", variable=self.lng_t_val, value='en')
        self.lng_t_menu.add_radiobutton(label="日语", variable=self.lng_t_val, value='ja')
        self.lng_t_menu.add_radiobutton(label="德语", variable=self.lng_t_val, value='de')
        self.lng_t_menu.add_radiobutton(label="法语", variable=self.lng_t_val, value='fr')
        self.lng_t_menu.add_radiobutton(label="韩语", variable=self.lng_t_val, value='ko')

        self.lng_menu.add_cascade(label='原文', menu=self.lng_s_menu)
        self.lng_menu.add_cascade(label='译文', menu=self.lng_t_menu)
        self.menu.add_cascade(label='设置', menu=self.setting_menu)
        self.menu.add_cascade(label='语种', menu=self.lng_menu)

        self.root.config(menu=self.menu)

        # 滑条
        self.scl_ed = Scrollbar(self.f_ed)

        # 文本框
        self.t_ed = Text(self.f_ed, height=30, font=("Times New Roman", 12))

        # 配置
        self.set_window()
        self.set_content()

        # 监听器数据
        self.ms_pressed = False # 鼠标按下了
        self.ms_pressed_and_moved = False  # 鼠标移动了
        self.translate_ready = False  # 翻译准备好了：1、鼠标移动了然后放开了 2、双击鼠标
        self.press_alt_time = None  # 按下翻译键盘的时间
        self.click_time = None  # 鼠标左键点击时间
        # 监听器
        self.mouse_listener = None
        self.keyboard_listener = None
        self.keyboard_listener_global = None
        self.set_listeners()

        # 其他
        self.mouse_controller = mouse.Controller()
        self.org_clipboard_text = ""  # 保存非笑翻mini复制的剪切板内容

    def set_window(self):
        self.root.title('笑翻mini')
        self.root.geometry('300x200')
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(icon.img))
        tmp.close()
        self.root.iconbitmap("tmp.ico")
        os.remove("tmp.ico")
        self.root.state('iconic')

        self.f_ed.pack(expand=1)

    def set_content(self):
        # hover tooltip
        # tooltip.CreateToolTip(self.cb_on_off, text='翻译开关')
        # tooltip.CreateToolTip(self.cb_line_on_off, text='开启后：待翻译文本的换行将被去掉。看pdf论文时打开有更好体验。')
        # tooltip.CreateToolTip(self.cb_copy_on_off, text='开启后：将自动复制翻译结果。')
        # tooltip.CreateToolTip(self.en2zh_en_on_off, text='开启后：英译中，关闭后：中译英。')

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
        self.root.protocol("WM_DELETE_WINDOW", self.stop_all_listeners)  # 退出窗口确保所有的监听器退出

# ########## 监听函数 ##########
    # 鼠标点击
    def on_click(self, x, y, btn, is_press):
        # print(f"鼠标{btn}键在({x}, {y})处{'按下' if is_press else '松开'}")
        if str(btn) == 'Button.left':
            # 双击选择
            if self.click_time is not None and time.time() - self.click_time < 0.4 and time.time() - self.click_time > 0.1:
                self.translate_ready = True
            # 按下
            if is_press:
                self.ms_pressed = True
            # 鼠标抬起选择
            if not is_press:
                if self.ms_pressed_and_moved:
                    self.translate_ready = True
                self.ms_pressed = False
                self.ms_pressed_and_moved = False
                self.click_time = time.time()

    # 鼠标移动
    def on_move(self, x, y):
        # print(f"鼠标移动到: ({x}, {y})")
        if self.ms_pressed:
            self.ms_pressed_and_moved = True
        else:
            self.ms_pressed_and_moved = False

    # 键盘
    def on_press(self, key):
        # print(f"你松开了{key.char if hasattr(key, 'char') else key.name}键")
        if self.translate_ready and key in short_cut:
            if self.press_alt_time is not None and time.time() - self.press_alt_time < 0.5 and time.time() - self.press_alt_time > 0.1:
                try:
                    self.org_clipboard_text = self.root.clipboard_get()  # 保存原来的剪切板内容
                except TclError:
                    self.root.clipboard_append("Start")  # 解决剪切板空时的错误
                    self.org_clipboard_text = self.root.clipboard_get()  # 保存原来的剪切板内容
                utils.do_ctrl_c()
                time.sleep(0.01)  # 解决翻译时读取到的剪切板内容是第二新的，不是最新的
                self.translate()
                self.translate_ready = False
            self.press_alt_time = time.time()

    # 全局键盘
    def on_press_global(self, key):
        print(f"{key.char if hasattr(key, 'char') else key.name}键")
        if key == short_cut_on_off:
            self.on_off_val.set(not self.on_off_val.get())

# ########## 重要函数 ##########
    # 关闭翻译监听器
    def stop_listeners(self):
        if self.mouse_listener is not None:
            self.mouse_listener.stop()

    # 关闭所有的监听器
    def stop_all_listeners(self):
        self.mouse_listener is not None and self.mouse_listener.stop()
        self.keyboard_listener is not None and self.keyboard_listener.stop()
        self.keyboard_listener_global is not None and self.keyboard_listener_global.stop()
        print(self.keyboard_listener_global)
        self.root.destroy()

    def update_text(self, text_ed):
        self.t_ed.delete('1.0', END)
        self.t_ed.insert(END, text_ed)

    def translate(self):
        loading = '翻译中……'
        self.update_text(loading)
        self.pop_win()
        self.locate(loading)
        text = self.root.clipboard_get()
        utils.recovery_clipboard(self.root, self.org_clipboard_text)  # 还原由笑翻mini调用ctrl+c造成的剪切板内容垃圾
        text = text.strip().replace('\n', ' ') if self.line_on_off_val.get() else text
        print(text)
        if len(text) == 0:
            return
        try:
            result = translate.translate(text, self.lng_t_val.get(), self.lng_s_val.get())
        except BaseException:
            self.update_text('网络异常')
        else:
            self.update_text(result)
            self.locate(result)  # 重新定位笑翻min
            self.focus()  # 聚焦到笑翻mini上来
            self.auto_copy(text, result)  # 复制翻译结果

    def pop_win(self):
        self.root.state('normal')
        self.root.wm_attributes('-topmost', 1)
        self.root.wm_attributes('-topmost', 0)

    def locate(self, text):
        pos = self.mouse_controller.position
        size = utils.adapt_size(text)
        x = pos[0] - int(int(size[0]) / 2)
        y = pos[1] + 20
        self.root.geometry('x'.join(size) + '+' + str(x) + '+' + str(y))

    def focus(self):
        pos = self.mouse_controller.position
        # 移动鼠标
        self.mouse_controller.position = (pos[0], pos[1] + self.root.winfo_height() + 20)
        # 点击左键
        self.mouse_controller.click(mouse.Button.left, 1)

    def auto_copy(self, text, result):
        if self.copy_on_off_val.get() == 0:
            return
        elif self.copy_on_off_val.get() == 1:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        elif self.copy_on_off_val.get() == 2:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)


# ##########check bottom函数##########
    # 开关
    def on_off(self):
        if not self.on_off_val.get():
            if self.mouse_listener is not None:
                self.mouse_listener.stop()
            if self.keyboard_listener is not None:
                self.keyboard_listener.stop()
        else:
            self.set_listeners()

    # 格式化开关
    def line_on_off(self):
        text = self.root.clipboard_get()
        text = text.strip().replace('\n', ' ') if self.line_on_off_val.get() else text
        print(text)
        if len(text) == 0:
            return
        result = translate.translate(text, "zh-CN", "en")
        self.update_text(result)

# =============== 菜单回调
    def callback(self):
        print(111)