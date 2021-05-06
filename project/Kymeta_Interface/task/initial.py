# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : T0_initial.py 
#--------------------------------------------------------------------------
# Build Test Environment.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================
"""
主要在於測試前的環境以及儀器控制的物件建立
"""

#==========================================================================
# IMPORTS
#==========================================================================

import os
import wx
import sys
import threading
from pubsub                   import pub  
from task.task_dialog         import dialog_thread 
from func.path_manager        import get_icon, get_task_image       

#==========================================================================
# MAIN PROGRAM
#==========================================================================     

class initial(object):
    
    def __init__(self, thread_event):
        
        self.thread_event = thread_event
        self.BuildPath()
        self.OnInit()   ## 改從儀器控制的結果來決定要不要繼續執行 ##
        
    def BuildPath(self):
        try:
            ## 標誌路徑 ##
            self.task_ico_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.instrument_icon(get_icon)
            
        except Exception as e:
            print("[T0-01] Get task icon failed ")
            print("Check the 'path_manager.py'")
            self.traceback(e)
            pass
        
        try:
            ## 圖片路徑 ##
            self.init_fixture_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.init_fixture(get_task_image)
            self.init_barcode_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.init_barcode(get_task_image)
            self.init_button_fullpath  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.init_button(get_task_image)
            
        except Exception as e:
            print("[T0-02] Get task image failed ")
            print("Check the 'path_manager.py'")
            self.traceback(e)
            pass
        
                 
    def OnInit(self):
        init_fixture_top    = zip([],[])
        init_fixture_bottom = zip([""],["Next"])
        
        init_barcode_top    = zip([],[])
        init_barcode_bottom = zip([""],["Next"])
        
        init_button_top    = zip([],[])
        init_button_bottom = zip([""],["Next"])
        
        ## 設定標誌 ##
        ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)
        

        dialog_thread(None, "Initial Check", init_fixture_top, init_fixture_bottom, 0, self.init_fixture_fullpath, ico, self.thread_event)
        dialog_thread(None, "Initial Check", init_barcode_top, init_barcode_bottom, 0, self.init_barcode_fullpath, ico, self.thread_event)     
        dialog_thread(None, "Initial Check", init_button_top,  init_button_bottom,  0, self.init_button_fullpath, ico, self.thread_event)

        
    def traceback(self, error):
        """ 在發生錯誤時顯示檔案位置和錯誤的line """
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))

        
## 功能測試 ##  
""" 記得import路徑、檔案路徑要更改 """ 
# app = wx.App()         
# initial()
# app.MainLoop()         
        
