# -*- coding: utf-8 -*- 
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : T1_debug_indicators.py 
#--------------------------------------------------------------------------
# Inspect the LED color on On/Off power.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

"""
from pubsub import pub會讓變數變成全域性的變數，不一定要綁定在event之中

在子任務中要調用儀器，可以以兩種方式執行:
    1. 重新對儀器建立連線
    2. 調用在initial預先建好的連線--
        調用方式:  將在instrument_manager建好的物件取出
                    (1) 透過return取出要用的參數
                    (2) 利用getattr取出要用的儀器屬性
        --------------------------------------------------------------------------------------------------         
                    (3) 本想透過 pub來調用，但是pub只能將sendMessage傳送的變數侷限在subscribe所建立的function下執行
                        即便是self的方式也無法在function外使用，因此該方法不適用
"""
#==========================================================================
# IMPORTS
#==========================================================================

import os
import wx
import sys
import pandas as pd
from queue                    import Queue
from pubsub                   import pub
from task.task_dialog         import dialog_thread  
from func.instrument_manager  import get_instr
from func.path_manager        import get_path
from func.path_manager        import get_icon, get_task_image

#==========================================================================
# MAIN PROGRAM
#==========================================================================

""" 決定測試項目是否存取log檔 """
save_log = True

""" 載入Spec，用來確定測試項目的子項目數量 """ 
spec_path = get_path.Specification(get_path)
spec_data = pd.read_csv(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + spec_path)
test_item_num = list(spec_data["Class"]).count("Debug Indicators")

#==========================================================================


class debug_indicators(object):
    
    def __init__(self, thread_event):
        
        try:
            self.thread_event = thread_event
            self.BuildPath()
            self.OnInit()
            
        except Exception as e:
            print(e)        
            ## 當發生錯誤導致無法測試時，將測試項目中的測試結果變成Error ##
            for item in range(test_item_num):
                pub.sendMessage("pass_to_grid",test_value = "Debug Indicators Error")

                 
    def BuildPath(self):
        try:
            ## 標誌路徑 ##
            self.task_ico_fullpath      = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.task_icon(get_icon)

        except Exception as e:
            print("[T1-01] Get task icon failed ")
            print("Check the 'path_manager.py'")
            self.traceback(e)

        try:    
            ## 圖片路徑 ##
            self.debug_LEDon_fullpath   = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.debug_LEDon(get_task_image)
            self.debug_bLEDon_fullpath  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.debug_bLEDon(get_task_image)
            self.debug_LEDoff_fullpath  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.debug_LEDoff(get_task_image)
            self.debug_bLEDoff_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.debug_bLEDoff(get_task_image)

        except Exception as e:
            print("[T1-02] Get task image failed ")
            print("Check the 'path_manager.py'")
            self.traceback(e)
        
        ## 雖然在initial時做過儀器連線的確認，這裡為避免斷線的可能所以在做一次，同時只取會用到的儀器 ##
        try:    
            ## 儀器控制 ##
            self.instr = get_instr()
            self.GPIB_PS_ACU  =  self.instr.GPIB_PS_ACU()
            
        except Exception as e:
            print("[T1-03] Get task instrument failed ")
            print("Check the 'instrument_manager.py'")
            self.traceback(e)
        
    def OnInit(self):
        
        debug_LEDon_top    = zip(["LED13","LED20","LED25"],["PASS","PASS","PASS"])
        debug_LEDon_bottom = zip([""],["Next"])
        
        debug_bLEDon_top    = zip(["LED85"],["PASS"])
        debug_bLEDon_bottom = zip([""],["Next"])
        
        debug_LEDoff_top    = zip(["LED13","LED20","LED25"],["PASS","PASS","PASS"])
        debug_LEDoff_bottom = zip([""],["Next"])
        
        debug_bLEDoff_top    = zip(["LED85"],["PASS"])
        debug_bLEDoff_bottom = zip([""],["Next"])
        
        ## 設定標誌 ##
        ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)
        
        ## 設定子進度條長度 ##
        self.T1_range = 4
        pub.sendMessage("subtask_processbar_range", value = self.T1_range)
        pub.sendMessage("subtask_processbar", value = 0)
        
        ## 執行流程 ##
        ## 開啟Power Supply  ##
        self.GPIB_PS_ACU.write("VOLt 13.8")
        self.GPIB_PS_ACU.write("CURR 6")
        self.GPIB_PS_ACU.write(":OUPT ON")
        print("[INFO] Open ACU power supply successfully")
        
        ## 開啟DAQ 控制Relay  ##
        ## 注意這裡DAQ False是開啟，True是關閉 ##
        
        #----------------------------------------------------------------------
        ## [ 0.檢查LED- 開電 ] ##
        self.instr.DAQ_ACC(False)
        self.instr.DAQ_LED(False)        
        
        #----------------------------------------------------------------------
        ## [ 1.檢查LED- 開電下LED13, LED20, LED25 ] ## 
        q = Queue()
        dialog_thread(None, "Debug Indicators", debug_LEDon_top,  debug_LEDon_bottom,  0, self.debug_LEDon_fullpath, ico, self.thread_event, q)
        
        ## 傳遞抓到的值回傳到grid_ui，顯示在網格控件上，並和規格比較後填入值 ##
        # (1) LED13 On
        pub.sendMessage("pass_to_grid",test_value = self.convert(q.get()))
        # (2) LED20 On
        pub.sendMessage("pass_to_grid",test_value = self.convert(q.get()))
        # (3) LED25 On
        pub.sendMessage("pass_to_grid",test_value = self.convert(q.get()))
        
        ## 設定子進度條的值 ##
        pub.sendMessage("subtask_processbar", value = 1) 
        print("[T1] Complete LED13, LED20, LED25 ON")
        
        #----------------------------------------------------------------------
        ## [ 2.檢查LED- 開電下LED85 ] ##           
        dialog_thread(None, "Debug Indicators", debug_bLEDon_top,  debug_bLEDon_bottom,  0, self.debug_bLEDon_fullpath, ico, self.thread_event, q)
        
        # (4) LED85 On
        pub.sendMessage("pass_to_grid",test_value = self.convert(q.get()))        
        pub.sendMessage("subtask_processbar", value = 2)
        print("[T1] Complete LED85 ON")
        
        self.instr.DAQ_LED(True)        
        self.instr.DAQ_ACC(True)
        
        #----------------------------------------------------------------------
        ## [ 3.檢查LED- 開電下LED13, LED20, LED25 ] ## 
        dialog_thread(None, "Debug Indicators", debug_LEDoff_top,  debug_LEDoff_bottom,  0, self.debug_LEDoff_fullpath, ico, self.thread_event, q)
        
        # (5) LED13 Off
        pub.sendMessage("pass_to_grid",test_value = self.convert(q.get()))
        # (6) LED20 Off
        pub.sendMessage("pass_to_grid",test_value = self.convert(q.get()))
        # (7) LED25 Off
        pub.sendMessage("pass_to_grid",test_value = self.convert(q.get()))      
        pub.sendMessage("subtask_processbar", value = 3)

        print("[T1] Complete LED13, LED20, LED25 OFF")
        
        #----------------------------------------------------------------------
        ## [ 4.檢查LED- 關電下LED85 ] ## 
        dialog_thread(None, "Debug Indicators", debug_bLEDoff_top,  debug_bLEDoff_bottom,  0, self.debug_bLEDoff_fullpath, ico, self.thread_event, q)
        
        # (8) LED85 Off
        pub.sendMessage("pass_to_grid",test_value = self.convert(q.get()))
        pub.sendMessage("subtask_processbar", value = 4)

        print("[T1] Complete LED85 OFF")
        
        self.instr.DAQ_ACC(False)    
        
        #----------------------------------------------------------------------
        ## [ 5.將記錄檔暫存 ] ##
        ## save_log決定是否要先存檔
        pub.sendMessage("save_log",log = save_log) 
        
    def convert(self, value):
        """ 將button取出的bool轉成字串 """
        if value == False:
            value = "PASS"
        else:
            value = "FAIL"
        return value
        
    def prompt_msg(self, message): 
        """ 顯示訊息 """
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True) 
            
    def traceback(self, error):
        """ 在發生錯誤時顯示檔案位置和錯誤的line """
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))
        
        
        

## 功能測試 ##  
""" 記得import路徑、檔案路徑要更改 """ 
# app = wx.App()         
# debug_indicators()
# app.MainLoop()        
        
        
        
