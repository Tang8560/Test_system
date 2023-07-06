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


#==========================================================================
# IMPORTS
#==========================================================================

import os
import wx
import sys
import threading
from queue import Queue

#==========================================================================
# LOAD BACKGROUND IMAGE
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from func.path_manager import get_backimage
from module.rewrite_statictext_transparent import transparentText

#==========================================================================
# IMAGE SIZE
#==========================================================================
width = 700
height = 250

#==========================================================================
# THREAD  (function)
#==========================================================================

class input_thread(threading.Thread):

    def __init__(self, parent, title, text_ctrl, btn, img_path, ico, thread_event, queue =None):

        threading.Thread.__init__(self)

        self.parent       =  parent
        self.title        =  title
        self.btn          =  btn
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
        dlg = task_dialog(self.parent, self.title, self.text_ctrl, self.btn, self.img_path, self.thread_event, self.queue)
        dlg.SetIcon(self.ico)
        dlg.ShowModal()


class task_dialog(wx.Dialog):

    def __init__(self, parent, title, text_ctrl, btn, img_path, thread_event, queue):

        framex, framey, framew, frameh = wx.ClientDisplayRect()
        super().__init__(parent, title = title)   # , size=(framew*0.5, frameh*0.8)
        self.text_ctrl    = text_ctrl
        self.btn          = btn
        self.img_path     = img_path
        self.thread_event = thread_event
        self.queue        = queue

        cbitmap = self.convert_img(width, height)
        self.OnInit(cbitmap)

        self.button_press = False

    def convert_img(self, width, height):
        bitmap = wx.Bitmap(self.img_path)
        image = bitmap.ConvertToImage()
        scale_image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        cbitmap = scale_image.ConvertToBitmap()
        return cbitmap

    def OnInit(self, cbitmap):

        self.cbitmap = wx.StaticBitmap(self, -1, cbitmap )

        text_Sizer = wx.BoxSizer( wx.HORIZONTAL )
        text_all = []

        for text in self.text_ctrl:
            setattr(task_dialog, format("txt_text"+str(text[0])), transparentText( self, -1, text[0] ))
            setattr(task_dialog, format("ctr_text"+str(text[0])),wx.TextCtrl( self, -1))
            text_Sizer.Add(getattr(task_dialog, format("txt_text"+str(text[0]))),0, wx.ALIGN_CENTER|wx.ALL, 5)
            text_Sizer.Add(getattr(task_dialog, format("ctr_text"+str(text[0]))),1, wx.ALIGN_CENTER|wx.ALL, 5)
            self.text(getattr(task_dialog, format("txt_text"+str(text[0]))), 12)
            getattr(task_dialog, format("txt_text"+str(text[0]))).SetForegroundColour((255,255,255))
            self.text(getattr(task_dialog, format("ctr_text"+str(text[0]))), 20)

            text_all.append(str(text[0]))
            self.text_all = text_all

        btn_Sizer = wx.BoxSizer( wx.VERTICAL )
        for btn in self.btn:
            setattr(task_dialog, format("btn"+str(btn[1])), wx.Button( self, -1, btn[1]))
            btn_Sizer.Add(getattr(task_dialog, format("btn"+str(btn[1]))), 0, wx.ALIGN_CENTER|wx.ALL, 5)

            getattr(task_dialog, format("btn"+str(btn[1]))).SetFocus()
            self.text(getattr(task_dialog, format("btn"+str(btn[1]))), 20)

        ## 當dialog 下層有叫 "Next 的按鈕" (self.btn_bottomNext)時，綁定self.On_Next ##
        try:
            self.btnNext.Bind(wx.EVT_BUTTON, self.On_Next)
        except: pass

        dialog_Sizer = wx.BoxSizer( wx.VERTICAL )
        button_Sizer = wx.BoxSizer( wx.HORIZONTAL )
        dialog_Sizer.Add(self.cbitmap,0, wx.ALL, 50)
        button_Sizer.Add(text_Sizer,1, wx.ALL, 5)
        button_Sizer.Add(btn_Sizer,0, wx.ALL, 5)

        dialog_Sizer.Add(button_Sizer,1, wx.ALIGN_CENTER | wx.ALL^ wx.TOP^ wx.BOTTOM, 50)
        self.SetSizer( dialog_Sizer )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)

    def text(self, obj, size):
        obj.SetFont( wx.Font( size, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ) )

    def On_Next(self, event):
        """ 當下層按鈕 Next按下時，執行的動作 """
        ## 這裡不能跑 for while迴圈
        if self.queue != None:
            try:
                self.queue.put(getattr(task_dialog, format("ctr_text"+str(self.text_all[0]))).GetValue())
            except:
                pass
            try:
                if len(self.top_all) == 1:
                    self.queue.put(getattr(task_dialog, format("btn_top"+str(self.top_all[0]))).GetValue())
                else:
                    self.queue.put(getattr(task_dialog, format("btn_top"+str(self.top_all[0]))).GetValue())
                    self.queue.put(getattr(task_dialog, format("btn_top"+str(self.top_all[1]))).GetValue())
                    self.queue.put(getattr(task_dialog, format("btn_top"+str(self.top_all[2]))).GetValue())
            except:
                pass
        else: pass

        self.Close()
        self.thread_event.set()

    def On_Toggle(self, event):
        button = event.GetEventObject()

        if button.GetValue() == False:
            button.SetLabel("PASS")
            button.SetForegroundColour("BLACK")
            button.SetBackgroundColour('GREEN')
        else:
            button.SetLabel("FAIL")
            button.SetForegroundColour("WHITE")
            button.SetBackgroundColour('RED')

    def on_erase_background(self, event):

        width, height = self.GetSize()
        self.head_backimg  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) +get_backimage.head_backimage(get_backimage)
        self.back_img = wx.Image(self.head_backimg, wx.BITMAP_TYPE_ANY).Scale(width, height)
        self.back_cbmp = self.back_img.ConvertToBitmap()

        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)

        dc.Clear()
        dc.DrawBitmap(self.back_cbmp,0,0)
        self.Layout()






