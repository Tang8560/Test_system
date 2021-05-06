# -*- coding: utf-8 -*-


"""
一次轉多個文件
"""


import sys
from wx.tools import img2py

# 名稱 -- 圖片路徑 -- 生成py檔名
## 切到資料夾內再執行 ##

command_lines = [
    "-a -F -n manual_img manual.png images.py",
    "-a -F -n setting_img setting.png images.py",
    "-a -F -n product_img product.png images.py",
    "-a -F -n path_img path.png images.py",
    "-a -F -n station_img station.png images.py",
    "-a -F -n instrument_img instrument.png images.py",
    "-a -F -n other_img other.png images.py",
    "-a -F -n login_img login.png images.py",
    ]


if __name__ == "__main__":
    for line in command_lines:
        args = line.split()
        img2py.main(args)

#%%
"""
只能轉換單一文件
"""        
from wx.tools import img2py
 
image_file = 'XXX/XXX.png'
python_file = 'python_img.py'
 
img2py.img2py(image_file=image_file, python_file=python_file,
              imgName='get_python_img', icon=True)
