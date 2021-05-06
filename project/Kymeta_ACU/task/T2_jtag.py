# -*- coding: utf-8 -*- 
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : T2_jtag.py 
#--------------------------------------------------------------------------
# PASS
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#========================================================================== 

import os
import wx
import time
import pandas as pd
from pubsub                   import pub 
from func.task_dialog         import task_dialog 
from func.instrument_manager  import get_instr
from func.path_manager        import get_path
from func.path_manager        import get_icon, get_task_image

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class T2_jtag(object):
    
    def __init__(self, thread_event):
        
        try:
            self.thread_event = thread_event
            self.OnInit()            
        except Exception as e:
            print(e)
            pub.sendMessage("pass_to_grid",test_value = "JTAG Error")           
                          
    def OnInit(self):
        pub.sendMessage("pass_to_grid",test_value = "PASS") 
