# 笑翻
一个高效的论文即时翻译工具

# 使用
1. 综合版本：笑翻.exe
2. mini版本：笑翻mini.exe 
   > 1. 双击exe直接使用
   > 2. 选中文字，使用双击`ctrl`即可翻译英语
   > 3. 可控制开关、可控制是否格式化文本（去除换行）
   > 4. 快捷键F8控制笑翻mini的开关

# 注意
请关闭全局vpn翻墙

# 我的备忘
打包命令
```bash
pyinstaller ./src/main.py -i ./src/resources/icon.ico -w -n 笑翻 -F
```
bug记录
1. 逐行分析，i.e.解析错误
2. 笑翻mini，F8快捷键会跳出两次提示框

提升项
1. 笑翻mini关闭or退出缩小至系统托盘，参考https://blog.csdn.net/wodeyan001/article/details/82497564
2. 笑翻mini设置快速翻译模式，即选择完词语则马上翻译
3. 笑翻mini增加多语言翻译
4. 笑翻mini通过控制鼠标点击弹窗，即可完成弹出弹窗并且聚焦在笑翻上
5. 将icon保存在code中 https://blog.csdn.net/weixin_41596280/article/details/105420093
6. 笑翻mini翻译异常捕获
7. 增加置顶、不置顶切换功能，并添加快捷键
