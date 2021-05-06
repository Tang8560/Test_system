# -*- coding: utf-8 -*- 
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta Reset Test
# File    : T1_switch.py 
#--------------------------------------------------------------------------
# Inspect the LED color on On/Off power.
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
import pandas as pd
from queue                    import Queue
from pubsub                   import pub 
from func.input_dialog        import input_thread 
from func.path_manager        import get_path
from func.path_manager        import get_icon, get_task_image

#==========================================================================
# MAIN PROGRAM
#==========================================================================


class T1_switch(object):
    
    def __init__(self, thread_event):
        
        try:
            self.thread_event = thread_event
            self.Build()
            self.OnInit()
        except Exception as e:
            self.traceback(e)        
            pub.sendMessage("pass_to_grid",test_value = "Switch Error")

                 
    def Build(self):
        self.task_ico_fullpath               = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.task_icon(get_icon)
        self.Normally_open_switch_fullpath   = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.open_switch(get_task_image)
        self.Depressed_switch_fullpath       = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.depressed_switch(get_task_image)

        self.Normally_open_switch_text    = zip(["Switch"])
        self.Normally_open_switch_btn = zip([""],["Next"])
        
        self.Depressed_switch_text    = zip(["Switch"])
        self.Depressed_switch_btn = zip([""],["Next"])

    def OnInit(self):
        self.ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)
        
        ## 設定子進度條長度 ##
        self.T1_range = 2
        pub.sendMessage("subtask_processbar_range", value = self.T1_range)

    def open_switch(self):
        ## [ 1.檢查switch- normally open switch ] ##
        q = Queue()                  
        input_thread(None, "Check Switch", self.Normally_open_switch_text, self.Normally_open_switch_btn, self.Normally_open_switch_fullpath, self.ico, self.thread_event, q)        
        pub.sendMessage("pass_to_grid",test_value = q.get())
        pub.sendMessage("subtask_processbar", value = 1) 
        print("[T1] Complete normally open switch")
        

    def depress_switch(self):        
        ## [ 2.檢查switch- Depressed_Switch ] ##  
        q = Queue()          
        input_thread(None, "Check Switch", self.Depressed_switch_text, self.Depressed_switch_btn, self.Depressed_switch_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage("pass_to_grid",test_value = q.get())       
        pub.sendMessage("subtask_processbar", value = 2)
        print("[T1] Complete Depressed Switch")
        
        
    def convert(self, value):
        if value == False:
            value = "PASS"
        else:
            value = "FAIL"
        return value
        
    def prompt_msg(self, message): 
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True) 
            
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))
        
        
        

## 功能測試 ##  
""" 記得import路徑、檔案路徑要更改 """ 
# app = wx.App()         
# debug_indicators()
# app.MainLoop()        
        
        
        
