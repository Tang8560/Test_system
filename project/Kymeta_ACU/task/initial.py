# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : initial.py 
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
from func.instrument_manager  import get_instr
from func.task_dialog         import dialog_thread, task_dialog 
from func.path_manager        import get_icon, get_task_image       

#==========================================================================
# MAIN PROGRAM
#==========================================================================     

class initial(object):
    
    def __init__(self, thread_event):
        try:
            self.thread_event = thread_event
            self.Build()
            self.OnInit()
                
        except Exception as e:
            print("[ERROR] [T0] Get task element failed ")
            print("Please check by the following steps")
            print("1. Check the 'instrument_manager.py' or connection error.")
            print("2. Setting error on the 'path_manager.py' or file loss.")
            self.traceback(e)

        
    def Build(self):

        ## image, icon path ##
        self.task_ico_fullpath     = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_icon.instrument_icon(get_icon)           
        self.init_fixture_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.init_fixture(get_task_image)
        self.init_barcode_fullpath = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.init_barcode(get_task_image)
        self.init_button_fullpath  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_task_image.init_button(get_task_image)            

        self.init_fixture_toggle    = zip([],[])
        self.init_fixture_btn = zip([""],["Next"])
        
        self.init_barcode_toggle    = zip([],[])
        self.init_barcode_btn = zip([""],["Next"])
        
        self.init_button_toggle    = zip([],[])
        self.init_button_btn = zip([""],["Next"])
        
        ## device ##
        self.instr = get_instr()
        self.GPIB_PS_ACU  =  self.instr.GPIB_PS_ACU() 
                 
    def OnInit(self):        
        ## Set icon ##
        ico = wx.Icon(self.task_ico_fullpath, wx.BITMAP_TYPE_ICO)     

        dialog_thread(None, "Initial Check", self.init_fixture_toggle, self.init_fixture_btn, self.init_fixture_fullpath, ico, self.thread_event)
        dialog_thread(None, "Initial Check", self.init_barcode_toggle, self.init_barcode_btn, self.init_barcode_fullpath, ico, self.thread_event)     
        dialog_thread(None, "Initial Check", self.init_button_toggle,  self.init_button_btn,  self.init_button_fullpath, ico, self.thread_event)

        self.GPIB_PS_ACU.write("VOLTage 13.8 ,(@1)")
        self.GPIB_PS_ACU.write("CURRent 6 ,(@1)")
        self.GPIB_PS_ACU.write("OUTPut ON,(@1)")
        self.instr.DAQ_ACC(False)
        self.instr.DAQ_LED(False)  
        
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))

        
