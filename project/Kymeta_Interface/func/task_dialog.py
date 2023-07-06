# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : task_dialog.py
#--------------------------------------------------------------------------
# Build Task Dialog.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================


"""
parent父層,
title標題,
btn_top上層按鈕      將標籤<list>, 按鈕文字<list> 做zip
btn_bottom下層按鈕數 將標籤<list>, 按鈕文字<list> 做zip
text_ctrl文字框      --- 暫未加入
img_path圖片路徑
return_value回傳值  回傳上層按鈕的值
"""

#==========================================================================
# IMPORTS
#==========================================================================

import os
import wx
import threading
from queue import Queue

#==========================================================================
# THREAD  (function)
#==========================================================================

class dialog_thread(threading.Thread):
    """ 創建線程，該線程用來作計時器使用 """
    def __init__(self, parent, title, btn_top, btn_bottom, text_ctrl, img_path, ico, thread_event, queue =None):

        threading.Thread.__init__(self)

        self.parent       =  parent
        self.title        =  title
        self.btn_top      =  btn_top
        self.btn_bottom   =  btn_bottom
        self.text_ctrl    =  text_ctrl
        self.img_path     =  img_path
        self.ico          =  ico
        self.thread_event =  thread_event
        self.queue        =  queue


        self.thread_event.clear()
        self.start()
        self.thread_event.wait()

    def run(self):
        pid = os.getpid()
        print(f'threading running: {pid}')
        wx.CallAfter(self.builddlg)

    def builddlg(self):
        dlg = task_dialog(self.parent, self.title, self.btn_top, self.btn_bottom, self.text_ctrl, self.img_path, self.thread_event, self.queue)
        dlg.SetIcon(self.ico)
        dlg.ShowModal()


class task_dialog(wx.Dialog):
    """ 建立測試流程會出現的按鈕選擇視窗 """

    def __init__(self, parent, title, btn_top, btn_bottom, text_ctrl, img_path, thread_event, queue):

        framex, framey, framew, frameh = wx.ClientDisplayRect()
        super().__init__(parent, title = title)   # , size=(framew*0.5, frameh*0.8)
        self.btn_top      = btn_top
        self.btn_bottom   = btn_bottom
        self.text_ctrl    = text_ctrl
        self.img_path     = img_path
        self.thread_event = thread_event
        self.queue        = queue

        ## 設定圖片大小 ##
        cbitmap = self.convert_img(700, 500)
        self.OnInit(cbitmap)

        self.button_press = False

    def convert_img(self, width, height):  # 480, 300
        """ 圖片轉換 """
        bitmap = wx.Bitmap(self.img_path)
        image = bitmap.ConvertToImage()
        scale_image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        cbitmap = scale_image.ConvertToBitmap()
        return cbitmap

    def OnInit(self, cbitmap):

        # self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        self.SetBackgroundColour(( 230, 230, 15 ))

        ## 建立圖片 ##
        self.cbitmap = wx.StaticBitmap(self, -1, cbitmap )

        ## 建立上部按鈕 (文字+Toggle按鈕) ##
        top_Sizer = wx.BoxSizer( wx.VERTICAL )

        top_all = []

        for top in self.btn_top:

            setattr(task_dialog, format("txt_top"+str(top[0])), wx.StaticText( self, -1, top[0] ))
            setattr(task_dialog, format("btn_top"+str(top[0])),wx.ToggleButton( self, -1, top[1]))
            top_Sizer.Add(getattr(task_dialog, format("txt_top"+str(top[0]))),0, wx.ALIGN_CENTER|wx.ALL^wx.BOTTOM, 5)
            top_Sizer.Add(getattr(task_dialog, format("btn_top"+str(top[0]))),0, wx.ALIGN_CENTER|wx.ALL^wx.TOP, 5)
            self.text(getattr(task_dialog, format("txt_top"+str(top[0]))), 12)
            self.text(getattr(task_dialog, format("btn_top"+str(top[0]))), 20)

            ## Toggle按鈕綁定事件 ##
            getattr(task_dialog, format("btn_top"+str(top[0]))).SetBackgroundColour('GREEN')
            getattr(task_dialog, format("btn_top"+str(top[0]))).Bind(wx.EVT_TOGGLEBUTTON, self.On_Toggle)

            top_all.append(str(top[0]))
            self.top_all = top_all

        ## 建立下部按鈕 (按鈕) ##
        bottom_Sizer = wx.BoxSizer( wx.VERTICAL )
        for bottom in self.btn_bottom:
            setattr(task_dialog, format("btn_bottom"+str(bottom[1])), wx.Button( self, -1, bottom[1]))
            bottom_Sizer.Add(getattr(task_dialog, format("btn_bottom"+str(bottom[1]))), 0, wx.ALIGN_CENTER|wx.ALL, 5)

            getattr(task_dialog, format("btn_bottom"+str(bottom[1]))).SetFocus()
            self.text(getattr(task_dialog, format("btn_bottom"+str(bottom[1]))), 20)

        ## 當dialog 下層有叫 "Next 的按鈕" (self.btn_bottomNext)時，綁定self.On_Next ##
        try:
            self.btn_bottomNext.Bind(wx.EVT_BUTTON, self.On_Next)
        except: pass

        dialog_Sizer = wx.BoxSizer( wx.HORIZONTAL )
        button_Sizer = wx.BoxSizer( wx.VERTICAL )
        dialog_Sizer.Add(self.cbitmap,0, wx.ALL, 50)
        button_Sizer.Add(top_Sizer,0, wx.EXPAND|wx.ALL, 5)
        button_Sizer.Add( (0, 0), 1, wx.EXPAND, 5 )
        button_Sizer.Add(bottom_Sizer,0, wx.EXPAND|wx.ALL, 5)
        dialog_Sizer.Add(button_Sizer,1, wx.EXPAND|wx.ALL^ wx.LEFT, 50)
        self.SetSizer( dialog_Sizer )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )


    def text(self, obj, size):
        obj.SetFont( wx.Font( size, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ) )

    def On_Next(self, event):
        """ 當下層按鈕 Next按下時，執行的動作 """
        ## 這裡不能跑 for while迴圈
        if self.queue != None:
            if len(self.top_all) == 1:
                self.queue.put(getattr(task_dialog, format("btn_top"+str(self.top_all[0]))).GetValue())
            else:
                self.queue.put(getattr(task_dialog, format("btn_top"+str(self.top_all[0]))).GetValue())
                self.queue.put(getattr(task_dialog, format("btn_top"+str(self.top_all[1]))).GetValue())
                self.queue.put(getattr(task_dialog, format("btn_top"+str(self.top_all[2]))).GetValue())

        else: pass

        self.Close()
        self.thread_event.set()

    def On_Toggle(self, event):
        """ 當上層toggle按鈕點即時，背景和文字產生變化 """
        button = event.GetEventObject()

        if button.GetValue() == False:
            button.SetLabel("PASS")
            button.SetForegroundColour("BLACK")
            button.SetBackgroundColour('GREEN')
        else:
            button.SetLabel("FAIL")
            button.SetForegroundColour("WHITE")
            button.SetBackgroundColour('RED')



## 功能測試 ##
""" 記得import路徑、檔案路徑要更改 """

# app = wx.App()
# btn_top    = zip(["LED13","LED20","LED25"],["PASS","PASS","PASS"])
# btn_bottom = zip(["",""],["Next","Cancel"])
# task_dialog(parent=None, title="test", btn_top=btn_top , btn_bottom=btn_bottom, text_ctrl=0, img_path="C:\\Users\\6065\\Desktop\\ATS_temp\\v3\\src\\task_image\\1.init_fixture.JPG")
# app.MainLoop()








