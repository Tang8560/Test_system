# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : end.py 
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

class end(object):
    
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
        ## device ##
        self.instr = get_instr()
        self.GPIB_PS_ACU  =  self.instr.GPIB_PS_ACU() 
                 
    def OnInit(self):        
        self.GPIB_PS_ACU.write("VOLTage 13.8 ,(@1)")
        self.GPIB_PS_ACU.write("CURRent 6 ,(@1)")
        self.GPIB_PS_ACU.write("OUTPut OFF,(@1)")
        self.instr.DAQ_ACC(True)
        self.instr.DAQ_LED(True)  
        
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))

        
