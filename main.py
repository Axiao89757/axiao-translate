from tkinter import Frame, Scrollbar, Label, Text, LEFT, WORD, RIGHT, Y, END, Button, Tk
import translator


window = Tk()
window.title('Axiao Google Translate')
window.geometry('650x600')

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


def translate():
    text = t_org.get('0.0', END).replace('\n', ' ')
    result = translator.translate(text, "zh-CN", "en")
    t_ed.delete('1.0', END)
    t_ed.insert(END, result)


# 按钮
b_en2ch = Button(f_btn, text='英 to 中', width=10, height=1, command=translate)
b_en2ch.pack()


window.mainloop()
