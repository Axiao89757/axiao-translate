# 笑翻
一个高效的论文即时翻译工具

# 使用
1. 综合版本：笑翻.exe
2. mini版本：笑翻mini.exe 
   > 1. 双击exe直接使用
   > 2. 使用`ctrl + c`即可翻译英语
   > 3. 可控制开关

# 注意
请关闭全局vpn翻墙

# 我的备忘
打包命令
```bash
pyinstaller ./src/main.py -i ./src/resources/icon.ico -w -n 笑翻 -F
```
bug记录
1. 逐行分析，i.e.解析错误
2. 增加置顶、不置顶切换功能

提升项
1. 笑翻mini关闭or退出缩小至系统托盘，参考https://blog.csdn.net/wodeyan001/article/details/82497564
2. 为笑翻mini翻译功能的启停添加快捷键