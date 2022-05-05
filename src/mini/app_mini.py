from tkinter import *
# from tkinter import messagebox
import time, base64, os
import translate, utils
from pynput import keyboard, mouse
from common import icon
from threading import Thread

short_cut = [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]
short_cut_on_off = keyboard.Key.f8


class AppMini(Tk):
    def __init__(self):
        super(AppMini, self).__init__()
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.trayMenu = None
        # frame
        self.f_ed = Frame(self)

        # 菜单
        self.menu = Menu(self)
        # 1 设置菜单
        self.setting_menu = Menu(self.menu, tearoff=False)
        # 1.1 翻译开关
        self.on_off_val = BooleanVar()
        self.on_off_val.set(True)
        self.setting_menu.add_checkbutton(variable=self.on_off_val, label='开关', onvalue=True, offvalue=False,
                                          command=self.on_off, selectcolor='green', accelerator='F8')
        self.setting_menu.add_separator()
        # 1.2 自动复制
        self.auto_copy_menu = Menu(self.setting_menu, tearoff=False)
        self.copy_on_off_val = IntVar()
        self.copy_on_off_val.set(0)
        self.auto_copy_menu.add_radiobutton(label="关闭", variable=self.copy_on_off_val, value=0, selectcolor='green')
        self.auto_copy_menu.add_radiobutton(label="原文", variable=self.copy_on_off_val, value=1, selectcolor='green')
        self.auto_copy_menu.add_radiobutton(label="译文", variable=self.copy_on_off_val, value=2, selectcolor='green')
        self.setting_menu.add_cascade(label='自动复制', menu=self.auto_copy_menu)
        # 1.3 删除换行
        self.line_on_off_val = BooleanVar()
        self.line_on_off_val.set(True)
        self.setting_menu.add_checkbutton(label='去除换行', variable=self.line_on_off_val, onvalue=True, offvalue=False,
                                          command=self.line_on_off, selectcolor='green')
        # 1.4 快速翻译模式
        self.fast_on_off_val = BooleanVar()
        self.fast_on_off_val.set(False)
        self.setting_menu.add_checkbutton(label='快速模式', variable=self.fast_on_off_val, onvalue=True, offvalue=False,
                                          command=self.fast_on_off, selectcolor='green')

        # 2 语言菜单
        self.lng_menu = Menu(self.menu, tearoff=False)
        # 2.1 源语言
        self.lng_s_menu = Menu(self.lng_menu, tearoff=False)
        self.lng_s_val = StringVar()
        self.lng_s_val.set('auto')  # 默认自动
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

        self.config(menu=self.menu)

        # 滑条
        self.scl_ed = Scrollbar(self.f_ed)

        # 文本框
        self.t_ed = Text(self.f_ed, height=30, font=("Times New Roman", 12))

        # 配置
        self.set_window()
        self.set_content()

        # 监听器数据
        self.ms_pressed = False  # 鼠标按下了
        self.ms_pressed_and_moved = False  # 鼠标移动了
        self.translate_ready = False  # 翻译准备好了：1、鼠标移动了然后放开了 2、双击鼠标
        self.press_alt_time = None  # 按下翻译键盘的时间
        self.click_time = None  # 鼠标左键点击时间
        # 监听器
        self.mouse_listener = None
        self.keyboard_listener = None
        self.keyboard_listener_global = None
        self.fast_model_tread = None
        self.set_listeners()

        # 其他
        self.mouse_controller = mouse.Controller()
        self.org_clipboard_text = ""  # 保存非笑翻mini复制的剪切板内容

    def set_window(self):
        self.title('笑翻mini')
        self.geometry('300x200')
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(icon.img))
        tmp.close()
        self.iconbitmap("tmp.ico")
        os.remove("tmp.ico")
        self.state('iconic')

        self.f_ed.pack(expand=1)

    def set_content(self):
        # 译文文本框
        self.scl_ed.config(command=self.t_ed.yview)
        self.t_ed.config(yscrollcommand=self.scl_ed.set)
        self.scl_ed.pack(side=RIGHT, fill=Y)
        self.t_ed.pack(expand=1)

    def set_listeners(self):
        self.set_mouse_listener()
        self.keyboard_listener = keyboard.Listener(on_release=self.on_press)
        self.keyboard_listener_global = keyboard.Listener(on_release=self.on_press_global)
        self.keyboard_listener.start()
        self.keyboard_listener_global.start()
        self.protocol("WM_DELETE_WINDOW", self.stop_all_listeners)  # 退出窗口确保所有的监听器退出

    def set_mouse_listener(self):
        self.mouse_listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click)
        self.mouse_listener.start()

    def start_fast_model(self):
        Thread(target=self.fast_work).start()

    def fast_work(self):
        while self.fast_on_off_val.get() and self.on_off_val.get():
            if self.translate_ready:
                self.process()

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
                self.process()
            self.press_alt_time = time.time()

    def process(self):
        self.translate_ready = False
        try:
            self.org_clipboard_text = self.clipboard_get()  # 保存原来的剪切板内容
        except TclError:
            self.clipboard_append("Start")  # 解决剪切板空时的错误
            self.org_clipboard_text = self.clipboard_get()  # 保存原来的剪切板内容
        utils.do_ctrl_c()
        time.sleep(0.01)  # 解决翻译时读取到的剪切板内容是第二新的，不是最新的
        self.translate()
        if self.fast_on_off_val.get():
            self.set_mouse_listener()

    # 全局键盘
    def on_press_global(self, key):
        # print(f"{key.char if hasattr(key, 'char') else key.name}键")
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
        self.destroy()

    def update_text(self, text_ed):
        self.t_ed.delete('1.0', END)
        self.t_ed.insert(END, text_ed)

    def translate(self):
        loading = '翻译中……'
        self.update_text(loading)
        self.pop_win()
        self.locate(loading, relocate=True)

        self.focus()  # 聚焦到笑翻mini上来
        text = self.clipboard_get()
        utils.recovery_clipboard(self, self.org_clipboard_text)  # 还原由笑翻mini调用ctrl+c造成的剪切板内容垃圾
        text = text.strip().replace('\n', ' ') if self.line_on_off_val.get() else text
        if len(text) == 0:
            return
        try:
            result = translate.translate(text, self.lng_t_val.get(), self.lng_s_val.get())
        except BaseException:
            self.update_text('网络异常')
        else:
            self.update_text(result)
            self.locate(result)  # 重新定位笑翻min
            self.auto_copy(text, result)  # 复制翻译结果

    def pop_win(self):
        self.state('normal')
        self.wm_attributes('-topmost', 1)
        self.wm_attributes('-topmost', 0)

    def locate(self, text, relocate=False):
        pos = self.mouse_controller.position
        size = utils.adapt_size(text)
        if relocate:
            x = pos[0] - int(int(size[0]) / 2)
            y = pos[1] + 20
            self.geometry('x'.join(size) + '+' + str(x) + '+' + str(y))
        self.geometry('x'.join(size))

    def focus(self):
        pos = self.mouse_controller.position
        # 移动鼠标
        self.mouse_controller.position = (pos[0], pos[1] + self.winfo_height() + 20)
        self.mouse_controller.click(mouse.Button.left, 1)  # 点击左键

    def auto_copy(self, text, result):
        if self.copy_on_off_val.get() == 0:
            return
        elif self.copy_on_off_val.get() == 1:
            self.clipboard_clear()
            self.clipboard_append(text)
        elif self.copy_on_off_val.get() == 2:
            self.clipboard_clear()
            self.clipboard_append(result)

    # ##########check bottom函数##########
    # 翻译总开关
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
        text = self.clipboard_get()
        text = text.strip().replace('\n', ' ') if self.line_on_off_val.get() else text
        if len(text) == 0:
            return
        result = translate.translate(text, self.lng_t_val, self.lng_t_val)
        self.update_text(result)

    # 快速模式开关
    def fast_on_off(self):
        if self.fast_on_off_val.get():
            self.start_fast_model()

# =============== 菜单回调
#     def on_closing(self):
#         if not self.trayMenu:  # when system tray is not exists.
#             selection = messagebox.askyesnocancel("Tips",
#                                                   "Quit directly?\nYes : Quit.\nNo:Minimize to system tray.")  # "Yes" will return True, "Cancel" will return None, "No" will return False.
#             if selection:  # when select yes, quit the app directly.
#                 self.destroy()
#             elif selection == False:  # Minimize to system tray.
#                 # make a system tray
#                 self.withdraw()
#                 # use bulitin tk.Menu
#
#                 # The work about "Winico"
#                 self.tk.call('package', 'require',
#                              'Winico')  # use the tcl "winico", make sure the folder of "winico" is in the same path.
#                 icon = self.tk.call('winico', 'createfrom', '2.ico')  # this is the icon on the system tray.
#                 self.tk.call('winico', 'taskbar', 'add', icon,  # set the icon
#                              '-callback', (self.register(self.menu_func), '%m', '%x', '%y'),
#                              # refer to winico documentation.
#                              '-pos', 0,
#                              '-text', u'jizhihaoSAMA’s Tool')  # the hover text of the system tray.
#
#                 # About menu
#                 self.trayMenu = Menu(self, tearoff=False)
#                 self.trayMenu.add_command(label="Show my app", command=self.deiconify)
#
#                 # You could also add a cascade menu
#                 cascadeMenu = Menu(self, tearoff=False)
#                 cascadeMenu.add_command(label="Casacde one", command=lambda: print("You could define it by yourself"))
#                 cascadeMenu.add_command(label="Cascade two")
#                 self.trayMenu.add_cascade(label="Other", menu=cascadeMenu)
#
#                 self.trayMenu.add_separator()  # you could add a separator
#
#                 self.trayMenu.add_command(label="Quit", command=self.destroy)
#
#                 # you could also add_command or add_checkbutton for what you want
#             else:  # This is cancel operation
#                 pass
#         else:
#             self.withdraw()  # when system tray exists, hide the window directly.
#
#     def menu_func(self, event, x, y):
#         if event == 'WM_RBUTTONDOWN':  # Mouse event, Right click on the tray.Mostly we will show it.
#             self.trayMenu.tk_popup(x, y)  # pop it up on this postion
#         if event == 'WM_LBUTTONDOWN':  # Mouse event, Left click on the tray,Mostly we will show the menu.
#             self.deiconify()  # show it.
