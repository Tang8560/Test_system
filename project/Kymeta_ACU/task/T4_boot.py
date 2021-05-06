# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : T4_boot.py 
#--------------------------------------------------------------------------
# Re-boot and inspect the LED13 is green to make sure the programming have 
# been done.
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
import time
import serial
from queue                    import Queue
from pubsub                   import pub
from func.task_dialog         import dialog_thread 
from func.instrument_manager  import get_instr
from func.path_manager        import get_icon, get_task_image

#==========================================================================
# PARAMETER
#==========================================================================
T4_range = 5

#==========================================================================
# PUB SUBSCRIBE
#==========================================================================
pass_fail  = "pass_to_grid"

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class T4_boot(object): 

    def __init__(self, thread_event):       
        try:    
            self.thread_event = thread_event
            self.Build() 
            self.OnInit()
        except Exception as e:
            print("[ERROR] [T4] Get task element failed ")
            print("Please check by the following steps")
            print("1. Check the 'instrument_manager.py' or connection error.")
            print("2. Setting error on the 'path_manager.py' or file loss.")
            self.traceback(e)
            pub.sendMessage(pass_fail,test_value = "Boot Error")

    def Build(self):
        ## Get icon, image path and device ##
        self.task_ico_fullpath   = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.programming_icon(get_icon)
        self.boot_LED_fullpath   = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.boot_LED(get_task_image)
        self.boot_LED_toggle    = zip(["LED13"],["PASS"])
        self.boot_LED_btn = zip([""],["Next"])         
      
        self.instr   =  get_instr()
        self.COM     =  self.instr.COM_ACU_Serial()
        self.COM_ACU =  serial.Serial(self.COM, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 0)           

    def OnInit(self):
        ## Setting icon ##
        self.ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)
        pub.sendMessage("subtask_processbar_range", value = T4_range)
        
    def boot(self):          
        ## [ 0.re-boot- power on ] ##
        self.instr.DAQ_ACC(True)
        self.instr.DAQ_ACC(False)
        
        ## [ 1.re-boot- get warm-up messages ] ## 
        boot_success = self.serial_port_setting(self.COM_ACU, "kats-acu login:", 100)
        self.COM_ACU.close()
        
        ## Tansfer result to the PASS or FAIL ##
        if boot_success == 1:
            boot_success = "PASS"
        else:
            boot_success = "FAIL"
            
        pub.sendMessage(pass_fail,test_value = boot_success)
        pub.sendMessage("subtask_processbar", value = 1)       
    
    def boot_LED13(self):
        ## [ 2.re-boot- check LED13 to comfirm porgramming properly ] ## 
        q = Queue()
        dialog_thread(None, "Boot LED", self.boot_LED_toggle,  self.boot_LED_btn, self.boot_LED_fullpath, self.ico, self.thread_event, q)
   
        pub.sendMessage(pass_fail,test_value = self.convert(q.get()))
        pub.sendMessage("subtask_processbar", value = 2)   
        print("[T4] Complete ACU boot")
        
        
    def serial_port_setting(self, instr, find_string, timeout):
        """ 
        取出RS232, Serial com 讀到的回傳值
        ---------------------------------------------------------
        instr        : 裝置名稱
        find_string  : 找尋的字串已離開讀取的迴圈
        timeout      : 當迴圈執行的時間超過timeout時中離  
        """
        # "Booted from partition 1, currently active partition is 1"
        try:
            serial_time_start = time.perf_counter()
            success = 0
            while True:  
                if instr.in_waiting: 
                    read_raw = instr.readline()  # 讀取一行
                    read_line = read_raw.decode()   # 用預設的UTF-8解碼
                    serial_time_end = time.perf_counter()
                    time.sleep(0.05)
                    pub.sendMessage("serial_read",  serial_read = str(read_line))

                    ## 如果在時間內找到字串就跳出迴圈 ##
                    if find_string in read_line:
                        print("[INFO] Serial return find the match string.")
                        success = 1
                        break        
                    ## 如果超過時間就跳出迴圈 ## 
                    elif serial_time_end - serial_time_start >= timeout:
                        print("[INFO] Serial return cannot find the match string, then timeout break.")
                        self.prompt_msg(find_string + " Error.")
                        success = 0
                        break                
                    else: continue
                    instr.close()
                                        
        except Exception as e:
            self.traceback(e)   
            
        return success
        
    def convert(self, value):
        if value == False: value = "PASS"
        else: value = "FAIL"
        return value
    
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,'line '+ str(traceback.tb_lineno))
        
        
        