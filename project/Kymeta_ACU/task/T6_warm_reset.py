# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : T6_warm_reset.py
#--------------------------------------------------------------------------
# Push switch 6 to execute warm reset and fetch the serial return to deter-
# mine the test result.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

"""
由於目前執行warm_reset和warm_rest的方式一樣，之後需去檢查輸出的log，
比較兩者的不同 -- 待處理
"""

#==========================================================================
# IMPORTS
#==========================================================================

import os
import wx
import sys
import time
import serial
from pubsub                   import pub
from func.task_dialog         import dialog_thread 
from func.instrument_manager  import get_instr
from func.path_manager        import get_icon, get_task_image

#==========================================================================
# MAIN PROGRAM
#==========================================================================

""" 決定測試項目是否存取log檔 """
save_log = True

#==========================================================================

class T6_warm_reset(object):
    
    def __init__(self, thread_event):
        
        try:
            self.thread_event = thread_event
            self.Build()
            self.OnInit()
        except Exception as e:
            print("[ERROR] [T6] Get task element failed ")
            print("Please check by the following steps")
            print("1. Check the 'instrument_manager.py' or connection error.")
            print("2. Setting error on the 'path_manager.py' or file loss.")
            self.traceback(e)
            pub.sendMessage("pass_to_grid",test_value = "Warm Error")
        
    def Build(self):

        self.task_ico_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.programming_icon(get_icon)
        self.warm_reset_fullpath   = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.warm_reset(get_task_image)

        self.warm_reset_toggle    = zip([],[])
        self.warm_reset_btn = zip([""],["Next"])
      
        self.instr  =  get_instr()
        self.COM  =  self.instr.COM_ACU_Serial()
        self.COM_ACU  =  serial.Serial(self.COM, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 0)           

    
    def OnInit(self):
        ## Setting icon ##
        ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)
        
        self.T5_range = 1
        pub.sendMessage("subtask_processbar_range", value = self.T5_range)
         
        pub.sendMessage("subtask_processbar", value = 0)
        time.sleep(1)      
        #----------------------------------------------------------------------
        ## [ 1.warm ] ## 
        dialog_thread(None, "Warm Reset", self.warm_reset_toggle,  self.warm_reset_btn, self.warm_reset_fullpath, ico, self.thread_event)      
        
        warm_success = self.serial_port_setting(self.COM_ACU, "kats-acu login:", 100)
        self.COM_ACU.close()
        
        ## 將成功或失敗轉成PASS或FAIL ##
        if warm_success == 1:
            warm_success = "PASS"
        else:
            warm_success = "FAIL"

        pub.sendMessage("pass_to_grid",test_value = warm_success)
        pub.sendMessage("subtask_processbar", value = 1)
        time.sleep(1)   
    
        
    def serial_port_setting(self, instr, find_string, timeout):

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
                    else:
                        continue
                    instr.close()
                 
        except Exception as e:
            success = 0
            print(e)    
            
        return success

    def prompt_msg(self, message): 
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True) 
            
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,'line '+ str(traceback.tb_lineno))         