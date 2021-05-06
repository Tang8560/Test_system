# -*- coding: utf-8 -*- 
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : T1_debug_indicators.py 
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
from func.path_manager        import get_path, get_icon, get_task_image

#==========================================================================
# PARAMETER
#==========================================================================

## set subprocess bar range ##
T1_range = 8

#==========================================================================
# PUB SUBSCRIBE
#==========================================================================
pass_fail  = "pass_to_grid"
subbar_range = "subtask_processbar_range"
subbar_value = "subtask_processbar"

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class T1_debug_indicators(object):
    
    def __init__(self, thread_event):       
        try:
            self.thread_event = thread_event
            self.Build()
            self.OnInit()         
        except Exception as e:       
            print("[ERROR] [T1] Get task element failed ")
            print("Please check by the following steps")
            print("1. Check the 'instrument_manager.py' or connection error.")
            print("2. Setting error on the 'path_manager.py' or file loss.")
            self.traceback(e)
            pub.sendMessage(pass_fail,test_value = "Debug Indicators Error")
                 
    def Build(self):
        ## Get icon, image path ##
        self.task_ico_fullpath      = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.task_icon(get_icon)
        self.debug_LEDon_fullpath   = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.debug_LEDon(get_task_image)
        self.debug_bLEDon_fullpath  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.debug_bLEDon(get_task_image)
        self.debug_LEDoff_fullpath  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.debug_LEDoff(get_task_image)
        self.debug_bLEDoff_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.debug_bLEDoff(get_task_image)
        
        ## Build dialog button ##
        self.debug_LED13on_toggle = zip(["LED13"],["PASS"])
        self.debug_LED13on_btn    = zip([""],["Next"])        
        self.debug_LED20on_toggle = zip(["LED20"],["PASS"])
        self.debug_LED20on_btn    = zip([""],["Next"])       
        self.debug_LED25on_toggle = zip(["LED25"],["PASS"])
        self.debug_LED25on_btn    = zip([""],["Next"])  
        self.debug_LED85on_toggle = zip(["LED85"],["PASS"])
        self.debug_LED85on_btn    = zip([""],["Next"])
        self.debug_LED13off_toggle= zip(["LED13"],["PASS"])
        self.debug_LED13off_btn   = zip([""],["Next"]) 
        self.debug_LED20off_toggle= zip(["LED20"],["PASS"])
        self.debug_LED20off_btn   = zip([""],["Next"])        
        self.debug_LED25off_toggle= zip(["LED25"],["PASS"])
        self.debug_LED25off_btn   = zip([""],["Next"])
        self.debug_LED85off_toggle= zip(["LED85"],["PASS"])
        self.debug_LED85off_btn   = zip([""],["Next"])
        
        ## device ##
        self.instr = get_instr()
        self.GPIB_PS_ACU  =  self.instr.GPIB_PS_ACU()
        
    def OnInit(self):        
        ## Setting icon ##
        self.ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)
        pub.sendMessage(subbar_range, value = T1_range)

        
    def check_LED13_on(self): 
        if self.GPIB_PS_ACU != None:
            q = Queue()
            dialog_thread(None, "Debug Indicators", self.debug_LED13on_toggle,  self.debug_LED13on_btn, self.debug_LEDon_fullpath, self.ico, self.thread_event, q)
            pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
            pub.sendMessage(subbar_value, value = 1)
        else: pub.sendMessage(pass_fail,test_value = "Debug Indicators Error")
        
    def check_LED20_on(self):        
        if self.GPIB_PS_ACU != None:
            q = Queue()
            dialog_thread(None, "Debug Indicators", self.debug_LED20on_toggle,  self.debug_LED20on_btn, self.debug_LEDon_fullpath, self.ico, self.thread_event, q)
            pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
            pub.sendMessage(subbar_value, value = 2)
        else: pub.sendMessage(pass_fail,test_value = "Debug Indicators Error")
        
    def check_LED25_on(self):
        if self.GPIB_PS_ACU != None: 
            q = Queue()
            dialog_thread(None, "Debug Indicators", self.debug_LED25on_toggle,  self.debug_LED25on_btn, self.debug_LEDon_fullpath, self.ico, self.thread_event, q)
            pub.sendMessage(pass_fail,test_value = self.convert(q.get())) 
            pub.sendMessage(subbar_value, value = 3)
        else: pub.sendMessage(pass_fail,test_value = "Debug Indicators Error")
        
    def check_LED85_on(self): 
        if self.GPIB_PS_ACU != None:
            q = Queue()
            dialog_thread(None, "Debug Indicators", self.debug_LED85on_toggle,  self.debug_LED85on_btn, self.debug_bLEDon_fullpath, self.ico, self.thread_event, q)
            pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
            pub.sendMessage(subbar_value, value = 4)
        else: pub.sendMessage(pass_fail,test_value = "Debug Indicators Error")

    def check_LED13_off(self): 
        if self.GPIB_PS_ACU != None:
            self.instr.DAQ_LED(True)        
            self.instr.DAQ_ACC(True)
            q = Queue()
            dialog_thread(None, "Debug Indicators", self.debug_LED13off_toggle,  self.debug_LED13off_btn, self.debug_LEDoff_fullpath, self.ico, self.thread_event, q)
            pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
            pub.sendMessage(subbar_value, value = 5)
        else: pub.sendMessage(pass_fail,test_value = "Debug Indicators Error")

    def check_LED20_off(self):  
        if self.GPIB_PS_ACU != None:      
            q = Queue()
            dialog_thread(None, "Debug Indicators", self.debug_LED20off_toggle,  self.debug_LED20off_btn, self.debug_LEDoff_fullpath, self.ico, self.thread_event, q)
            pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
            pub.sendMessage(subbar_value, value = 6)
        else: pub.sendMessage(pass_fail,test_value = "Debug Indicators Error")

    def check_LED25_off(self): 
        if self.GPIB_PS_ACU != None:
            q = Queue()
            dialog_thread(None, "Debug Indicators", self.debug_LED25off_toggle,  self.debug_LED25off_btn, self.debug_LEDoff_fullpath, self.ico, self.thread_event, q)
            pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
            pub.sendMessage(subbar_value, value = 7)
        else: pub.sendMessage(pass_fail,test_value = "Debug Indicators Error")

    def check_LED85_off(self): 
        if self.GPIB_PS_ACU != None:
            q = Queue()
            dialog_thread(None, "Debug Indicators", self.debug_LED85off_toggle,  self.debug_LED85off_btn, self.debug_bLEDoff_fullpath, self.ico, self.thread_event, q)
            pub.sendMessage(pass_fail,test_value = self.convert(q.get()))        
            pub.sendMessage(subbar_value, value = 8)  
            self.instr.DAQ_ACC(False)
        else: pub.sendMessage(pass_fail,test_value = "Debug Indicators Error")

    def convert(self, value):
        """ convert toggle button return value """
        if value == False: value = "PASS"
        else: value = "FAIL"
        return value
        
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))
        
        
        
        
