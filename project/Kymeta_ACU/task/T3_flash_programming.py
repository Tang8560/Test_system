# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : T3_flash_programming.py
#--------------------------------------------------------------------------
# Run flash programming.
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
from pubsub                   import pub
from func.task_dialog         import dialog_thread
from func.instrument_manager  import get_instr
from func.path_manager        import get_path
from func.path_manager        import get_icon, get_task_image

#==========================================================================
# PARAMETER
#==========================================================================
T3_range = 3

#==========================================================================
# PUB SUBSCRIBE
#==========================================================================
pass_fail  = "pass_to_grid"
serial_return = "serial_return"

#==========================================================================
# MAIN PROGRAM
#==========================================================================
class T3_flash_programming(object):

    def __init__(self, thread_event):
        try:
            self.thread_event = thread_event
            self.Build()
            self.OnInit()
        except Exception as e:
            print("[ERROR] [T3] Get task element failed ")
            print("Please check by the following steps")
            print("1. Check the 'instrument_manager.py' or connection error.")
            print("2. Setting error on the 'path_manager.py' or file loss.")
            self.traceback(e)
            pub.sendMessage(pass_fail,test_value = "Flash Programming Error")

    def Build(self):
        ## Get icon, image path and device ##
        self.task_ico_fullpath      = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.programming_icon(get_icon)
        self.programming_init_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.programming_init(get_task_image)
        self.programming_set_fullpath  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.programming_set(get_task_image)
        self.programming_end_fullpath  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.programming_end(get_task_image)

        self.programming_init_toggle = zip([],[])
        self.programming_init_btn    = zip([""],["Next"])
        self.programming_set_toggle  = zip(["Timeout"],["PASS"])
        self.programming_set_btn     = zip([""],["Next"])
        self.programming_end_toggle  = zip([],[])
        self.programming_end_btn     = zip([""],["Next"])

        self.instr = get_instr()
        self.COM      =  self.instr.COM_ACU_Serial()
        self.COM_ACU  =  serial.Serial(self.COM, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout = 0)

    def OnInit(self):
        ## Setting icon ##
        ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)
        pub.sendMessage("subtask_processbar_range", value = T3_range)
        try:
            ## [ 1. Programming- Set swith to the eMMC programming mode ] ##
            self.instr.DAQ_ACC(True)
            dialog_thread(None, "eMMC flash programming", self.programming_init_toggle,  self.programming_init_btn, self.programming_init_fullpath, ico, self.thread_event)
            self.instr.DAQ_ACC(False)

            pub.sendMessage("subtask_processbar", value = 1)
            time.sleep(1)

            ## [ 2.Programming- Base on Serial return to check the ACU into the programming mode ] ##
            SDIO_success = self.serial_port_setting(self.COM_ACU, "Set SDIO mux: eMMC", 60)

            if SDIO_success:
                print("[T3] Complete entre the flash programming status")
                ## [ 3.Programming- Check the status is completly programming ] ##
                dialog_thread(None, "eMMC flash programming", self.programming_set_toggle,  self.programming_set_btn, self.programming_set_fullpath, ico, self.thread_event)
                flash_success = self.serial_port_setting(self.COM_ACU, "acu-bringup login:", 900)
                print("[T3] Complete flash programming")
            else:
                flash_success = 0

            ## There need to close, otherwise the console serial port cannot re-connection ##
            self.COM_ACU.close()
            del(self.COM_ACU)

            pub.sendMessage("subtask_processbar", value = 2)
            time.sleep(1)

            self.instr.DAQ_ACC(True)

            ## [ 4.Programming- Retrive SD card ] ##
            dialog_thread(None, "eMMC flash programming", self.programming_end_toggle,  self.programming_end_btn, self.programming_end_fullpath, ico, self.thread_event)
            pub.sendMessage("subtask_processbar", value = 3)
            time.sleep(1)

            ## Tansfer result to the PASS or FAIL ##
            if SDIO_success*flash_success == 1:
                flash_return = "PASS"
            else:
                flash_return = "FAIL"
        except Exception as e:
            self.COM_ACU.close()
            del(self.COM_ACU)
            flash_return = "Programming Error"
            print(e)

        pub.sendMessage("pass_to_grid",test_value = flash_return)

    def serial_port_setting(self, instr, find_string, timeout):
        """
        Get RS232, Serial return
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
                    pub.sendMessage(serial_return,  serial_read = str(read_line))
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
            print(e)
        return success

    def prompt_msg(self, message):
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True)

    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,'line '+ str(traceback.tb_lineno))






