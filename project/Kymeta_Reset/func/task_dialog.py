# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
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

class dialog_thread(threading.Thread):
    """ Create Dialog Thread """
    def __init__(self, parent, title, toggle, origin, img_path, ico, thread_event, queue =None):
        
        threading.Thread.__init__(self)   
        
        self.parent       =  parent 
        self.title        =  title
        self.toggle       =  toggle
        self.origin       =  origin
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
        dlg = task_dialog(self.parent, self.title, self.toggle, self.origin, self.img_path, self.thread_event, self.queue)
        dlg.SetIcon(self.ico)
        dlg.ShowModal()  


class task_dialog(wx.Dialog): 
    """ Create Test Dialog """
    
    def __init__(self, parent, title, toggle, origin, img_path, thread_event, queue): 
            
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        super().__init__(parent, title = title)   # , size=(framew*0.5, frameh*0.8)
        self.toggle      = toggle
        self.origin   = origin
        self.img_path     = img_path
        self.thread_event = thread_event
        self.queue        = queue 
        
        ## Setting image size ##
        cbitmap = self.convert_img(width, height)           
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
        
        ## Build image ##
        self.cbitmap = wx.StaticBitmap(self, -1, cbitmap )
        
        toggle_Sizer = wx.BoxSizer( wx.HORIZONTAL )    
        toggle_all = []
        
        for toggle in self.toggle:  
            
            setattr(task_dialog, format("txt_toggle"+str(toggle[0])), transparentText( self, -1, toggle[0] ))
            setattr(task_dialog, format("toggle"+str(toggle[0])),wx.ToggleButton( self, -1, toggle[1]))
            toggle_Sizer.Add(getattr(task_dialog, format("txt_toggle"+str(toggle[0]))),0, wx.ALIGN_CENTER|wx.ALL, 5)
            toggle_Sizer.Add(getattr(task_dialog, format("toggle"+str(toggle[0]))),0, wx.ALIGN_CENTER|wx.ALL, 5)
            self.text(getattr(task_dialog, format("txt_toggle"+str(toggle[0]))), 12)
            getattr(task_dialog, format("txt_toggle"+str(toggle[0]))).SetForegroundColour((255,255,255))
            self.text(getattr(task_dialog, format("toggle"+str(toggle[0]))), 20)
            
            ## Toggle button binding ##
            getattr(task_dialog, format("toggle"+str(toggle[0]))).SetBackgroundColour('GREEN')	
            getattr(task_dialog, format("toggle"+str(toggle[0]))).Bind(wx.EVT_TOGGLEBUTTON, self.On_Toggle) 
            
            toggle_all.append(str(toggle[0]))
            self.toggle_all = toggle_all 
        

        origin_Sizer = wx.BoxSizer( wx.HORIZONTAL )
        for origin in self.origin:            
            setattr(task_dialog, format("origin"+str(origin[1])), wx.Button( self, -1, origin[1]))
            origin_Sizer.Add(getattr(task_dialog, format("origin"+str(origin[1]))), 0, wx.ALL, 5)
            
            getattr(task_dialog, format("origin"+str(origin[1]))).SetFocus()
            self.text(getattr(task_dialog, format("origin"+str(origin[1]))), 20)
        
        ## 當dialog 下層有叫 "Next 的按鈕" (self.originNext)時，綁定self.On_Next ##
        try:     
            self.originNext.Bind(wx.EVT_BUTTON, self.On_Next)            
        except: pass
                  
        dialog_Sizer = wx.BoxSizer( wx.VERTICAL )
        button_Sizer = wx.BoxSizer( wx.HORIZONTAL )
        dialog_Sizer.Add(self.cbitmap,0, wx.ALL^ wx.BOTTOM, 50)
        button_Sizer.Add(toggle_Sizer,1, wx.ALL, 5)  

        button_Sizer.Add(origin_Sizer,0, wx.ALL, 5)
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
            if len(self.toggle_all) == 1:
                self.queue.put(getattr(task_dialog, format("toggle"+str(self.toggle_all[0]))).GetValue())
            else:
                self.queue.put(getattr(task_dialog, format("toggle"+str(self.toggle_all[0]))).GetValue())
                self.queue.put(getattr(task_dialog, format("toggle"+str(self.toggle_all[1]))).GetValue())
                self.queue.put(getattr(task_dialog, format("toggle"+str(self.toggle_all[2]))).GetValue())
     
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
        








