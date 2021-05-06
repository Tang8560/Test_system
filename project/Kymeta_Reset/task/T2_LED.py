# -*- coding: utf-8 -*- 
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta Reset
# File    : T2_LED.py 
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
from queue                    import Queue
from pubsub                   import pub
from func.task_dialog         import dialog_thread  
from func.instrument_manager  import get_instr
from func.path_manager        import get_path
from func.path_manager        import get_icon, get_task_image


#==========================================================================
# PUB SUBSCRIBE
#==========================================================================
pass_fail  = "pass_to_grid"
subbar_range = "subtask_processbar_range"
subbar_value = "subtask_processbar"

#==========================================================================
# PARAMETER
#==========================================================================
open_RL = True
close_RL = False
#==========================================================================
# MAIN PROGRAM
#==========================================================================

class T2_LED(object):
    
    def __init__(self, thread_event):
        
        try:
            self.thread_event = thread_event
            self.instr = get_instr()
            self.Build()
            self.OnInit()
            
        except Exception as e:
            self.traceback(e)        
            pub.sendMessage("pass_to_grid",test_value = "Check LED Error")

                 
    def Build(self):
        
        self.task_ico_fullpath    = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.task_icon(get_icon)
        self.TRANSEC_R_fullpath   = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.TRANSEC_R(get_task_image)
        self.TRANSEC_G_fullpath   = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.TRANSEC_G(get_task_image)
        self.NET_R_fullpath       = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.NET_R(get_task_image)
        self.NET_G_fullpath       = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.NET_G(get_task_image)
        self.STATUS_R_fullpath    = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.STATUS_R(get_task_image)
        self.STATUS_G_fullpath    = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.STATUS_G(get_task_image)
        self.TX_R_fullpath        = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.TX_R(get_task_image)
        self.TX_G_fullpath        = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.TX_G(get_task_image)
        self.RX_R_fullpath        = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.RX_R(get_task_image)
        self.RX_G_fullpath        = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.RX_G(get_task_image)
        self.PWR_R_fullpath       = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.PWR_R(get_task_image)
        self.PWR_G_fullpath       = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.PWR_G(get_task_image)
        
        self.TRANSEC_R_toggle  = zip(["LED1 RED"],["PASS"])
        self.TRANSEC_R_btn     = zip([""],["Next"])   
        self.TRANSEC_G_toggle  = zip(["LED1 GREEN"],["PASS"])
        self.TRANSEC_G_btn     = zip([""],["Next"])
        
        self.NET_R_toggle    = zip(["LED2 RED"],["PASS"])
        self.NET_R_btn       = zip([""],["Next"]) 
        self.NET_G_toggle    = zip(["LED2 GREEN"],["PASS"])
        self.NET_G_btn       = zip([""],["Next"])
        
        self.STATUS_R_toggle = zip(["LED3 RED"],["PASS"])
        self.STATUS_R_btn    = zip([""],["Next"])    
        self.STATUS_G_toggle = zip(["LED3 GREEN"],["PASS"])
        self.STATUS_G_btn    = zip([""],["Next"])
        
        self.TX_R_toggle     = zip(["LED4 RED"],["PASS"])
        self.TX_R_btn        = zip([""],["Next"])      
        self.TX_G_toggle     = zip(["LED4 GREEN"],["PASS"])
        self.TX_G_btn        = zip([""],["Next"])

        self.RX_R_toggle    = zip(["LED5 RED"],["PASS"])
        self.RX_R_btn       = zip([""],["Next"])     
        self.RX_G_toggle    = zip(["LED5 GREEN"],["PASS"])
        self.RX_G_btn       = zip([""],["Next"])
        
        self.PWR_R_toggle   = zip(["LED6 RED"],["PASS"])
        self.PWR_R_btn      = zip([""],["Next"])    
        self.PWR_G_toggle   = zip(["LED6 GREEN"],["PASS"])
        self.PWR_G_btn      = zip([""],["Next"])            
                           
    def OnInit(self):
        self.ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)
        
        ## 設定子進度條長度 ##
        self.T1_range = 12
        pub.sendMessage("subtask_processbar_range", value = self.T1_range)

    def check_TRANSEC_R(self):
        self.DAQ_transecR =  self.instr.DAQ_transecR(open_RL)
        q = Queue()
        dialog_thread(None, "Check LED", self.TRANSEC_R_toggle,  self.TRANSEC_R_btn, self.TRANSEC_R_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 1)
        print("[T2] Complete LED: TRANSEC_R")
        self.DAQ_transecR =  self.instr.DAQ_transecR(close_RL)


    def check_TRANSEC_G(self):
        self.DAQ_transecG =  self.instr.DAQ_transecG(open_RL)
        q = Queue()
        dialog_thread(None, "Check LED", self.TRANSEC_G_toggle,  self.TRANSEC_G_btn, self.TRANSEC_G_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 2)
        print("[T2] Complete LED: TRANSEC_G")
        self.DAQ_transecG =  self.instr.DAQ_transecG(close_RL)
        
    def check_NET_R(self):
        self.DAQ_netR     =  self.instr.DAQ_netR(open_RL)
        q = Queue()
        dialog_thread(None, "Check LED", self.NET_R_toggle,  self.NET_R_btn, self.NET_R_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 3)
        print("[T2] Complete LED: NET_R")
        self.DAQ_netR     =  self.instr.DAQ_netR(close_RL)

    def check_NET_G(self):
        self.DAQ_netG     =  self.instr.DAQ_netG(open_RL) 
        q = Queue()
        dialog_thread(None, "Check LED", self.NET_G_toggle,  self.NET_G_btn, self.NET_G_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 4)
        print("[T2] Complete LED: NET_G")
        self.DAQ_netG     =  self.instr.DAQ_netG(close_RL) 

    def check_STATUS_R(self):
        self.DAQ_statusR  =  self.instr.DAQ_statusR(open_RL)
        q = Queue()
        dialog_thread(None, "Check LED", self.STATUS_R_toggle,  self.STATUS_R_btn, self.STATUS_R_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 5)
        print("[T2] Complete LED: STATUS_R")
        self.DAQ_statusR  =  self.instr.DAQ_statusR(close_RL)
        
    def check_STATUS_G(self):
        self.DAQ_statusG  =  self.instr.DAQ_statusG(open_RL)
        q = Queue()
        dialog_thread(None, "Check LED", self.STATUS_G_toggle,  self.STATUS_G_btn, self.STATUS_G_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 6)
        print("[T2] Complete LED: STATUS_G")
        self.DAQ_statusG  =  self.instr.DAQ_statusG(close_RL)
        
    def check_TX_R(self):
        self.DAQ_TXR      =  self.instr.DAQ_TXR(open_RL)
        q = Queue()
        dialog_thread(None, "Check LED", self.TX_R_toggle,  self.TX_R_btn, self.TX_R_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 7)
        print("[T2] Complete LED: TX_R")
        self.DAQ_TXR      =  self.instr.DAQ_TXR(close_RL)
        
    def check_TX_G(self):
        self.DAQ_TXG      =  self.instr.DAQ_TXG(open_RL) 
        q = Queue()
        dialog_thread(None, "Check LED", self.TX_G_toggle,  self.TX_G_btn, self.TX_G_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 8)
        print("[T2] Complete LED: TX_G")
        self.DAQ_TXG      =  self.instr.DAQ_TXG(close_RL) 
        
    def check_RX_R(self):
        self.DAQ_RXR      =  self.instr.DAQ_RXR(open_RL)
        q = Queue()
        dialog_thread(None, "Check LED", self.RX_R_toggle,  self.RX_R_btn, self.RX_R_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 9)
        print("[T2] Complete LED: RX_R")
        self.DAQ_RXR      =  self.instr.DAQ_RXR(close_RL)
        
    def check_RX_G(self):
        self.DAQ_RXG      =  self.instr.DAQ_RXG(open_RL) 
        q = Queue()
        dialog_thread(None, "Check LED", self.RX_G_toggle,  self.RX_G_btn, self.RX_G_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 10)
        print("[T2] Complete LED: RX_G")
        self.DAQ_RXG      =  self.instr.DAQ_RXG(close_RL) 

    def check_PWR_R(self):
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(open_RL)
        q = Queue()
        dialog_thread(None, "Check LED", self.PWR_R_toggle,  self.PWR_R_btn, self.PWR_R_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 11)
        print("[T2] Complete LED: PWR_R")
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(close_RL)
        
    def check_PWR_G(self):
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(open_RL)  
        q = Queue()
        dialog_thread(None, "Check LED", self.PWR_G_toggle,  self.PWR_G_btn, self.PWR_G_fullpath, self.ico, self.thread_event, q)
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage(subbar_value, value = 12)
        print("[T2] Complete LED: PWR_G")
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(close_RL)  
         
        
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
        
        
        
