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
        
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))

        
