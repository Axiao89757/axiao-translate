import base64
open_icon = open(r"E:\Projects\pythonProject\axiao-translate\src\resources\icon.ico", "rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
data = "img = '%s'" % b64str
f = open("icon.py", "w+")
f.write(data.replace("b'", "").replace("''", "'"))
f.close()
