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
from func.task_dialog         import dialog_thread 
from func.instrument_manager  import get_instr
from func.path_manager        import get_icon, get_task_image       

#==========================================================================
# MAIN PROGRAM
#==========================================================================     

class initial(object):
    
    def __init__(self, thread_event):
        try:
            self.thread_event = thread_event
            self.instr = get_instr()
            self.Build()
            self.OnInit()
                
        except Exception as e:
            print("[ERROR] [T0] Get task element failed ")
            print("Please check by the following steps")
            print("1. Check the 'instrument_manager.py' or connection error.")
            print("2. Setting error on the 'path_manager.py' or file loss.")
            self.traceback(e)  

    def Build(self):
        self.task_ico_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.instrument_icon(get_icon)
        self.init_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.init(get_task_image)
        self.init_toggle    = zip([],[])
        self.init_btn       = zip([""],["Next"])   
                
    def OnInit(self):
        close_RL = False
        self.DAQ_transecR =  self.instr.DAQ_transecR(close_RL)
        self.DAQ_transecG =  self.instr.DAQ_transecG(close_RL)
        self.DAQ_netR     =  self.instr.DAQ_netR(close_RL)
        self.DAQ_netG     =  self.instr.DAQ_netG(close_RL)
        self.DAQ_statusR  =  self.instr.DAQ_statusR(close_RL)
        self.DAQ_statusG  =  self.instr.DAQ_statusG(close_RL)   
        self.DAQ_TXR      =  self.instr.DAQ_TXR(close_RL)        
        self.DAQ_TXG      =  self.instr.DAQ_TXG(close_RL)  
        self.DAQ_RXR      =  self.instr.DAQ_RXR(close_RL)        
        self.DAQ_RXG      =  self.instr.DAQ_RXG(close_RL)    
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(close_RL)
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(close_RL) 

        ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)   
        dialog_thread(None, "Initial Check", self.init_toggle, self.init_btn, self.init_fullpath, ico, self.thread_event)
        
    def traceback(self, error):
        """ 在發生錯誤時顯示檔案位置和錯誤的line """
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))

        
## 功能測試 ##  
""" 記得import路徑、檔案路徑要更改 """ 
# app = wx.App()         
# initial()
# app.MainLoop()         
        
