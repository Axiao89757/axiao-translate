from tkinter import *

window = Tk()

window.title('Google Translate')

window.geometry('500x300')

# 两个frame
f_org = Frame(window)
f_ed = Frame(window)

# 两个scroller
scl_org = Scrollbar(f_org)
scl_ed = Scrollbar(f_ed)

# 原文文本框
label_org = Label(f_org, text="Label")
label_org.pack(side=LEFT)
t_org = Text(f_org, height=5, wrap=WORD)
t_org.pack()
t_ed = Text(f_ed, height=5, wrap=WORD)
t_ed.pack()


def translate():
    var = t_org.get('1.0', '6.0')
    t_ed.insert(END, var)


b_en2ch = Button(window, text='英 to 中', width=10,
                 height=1, command=translate)
b_en2ch.pack()

window.mainloop()
