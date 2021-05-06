# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : test_visa.py 
#--------------------------------------------------------------------------
# Instrument Manual Panel
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================
"""
儀器控制  GPIB、 Ethernet、Serial、DAQ
-------------------------------------------------------
在 OnInit中會建立好所有儀器的連結，只需取出變數後下達指令即可
"""
import os
import wx
import sys 
import time
import pyvisa

class get_instr(object): 
    
    def __init__(self, address):
        
        self.address = address

    ## 連線所有的儀器 (可直接下指令) ##        
    def device(self):
        
        self.device = self.Connect_VISA(self.address)
        return self.device   

    def Connect_VISA(self, address):
        """ 
        連接GPIB、Ethernet、Serial COM -- 不過命令須從回傳的device再去做下達的動作
        ------------------------------------------------
        Instrument.JSON的設定方式，可透過VISA查詢
        [ GPIB ] GPIB0::5::INSTR
        [ Ethernet ] TCPIP0::192.168.0.100::inst0::INSTR
        [ Serial ] COM1
        -------------------------------------------------
        """

        for i in range(10):
            try: 
                 rm = pyvisa.ResourceManager()                             
                 self.device = rm.open_resource(address, open_timeout=3000) 
                 if self.device:
                    msg = "[VISA] Connect "+ address +" Successfully."
                    break
                 else:
                    time.sleep(2)
                    continue
            except Exception as e:
                 self.device = None
                 msg = "[VISA] No Connect "+ address
                 self.traceback(e)
        
        if not self.device:
            self.prompt_msg("Check the VISA connection "+ address + "." )        
        print(msg)
        print(self.device)        
        return self.device
    
    def prompt_msg(self, message): 
        """ 顯示訊息 """
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True) 
            
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))
        
        
                 
def visa_instr(address, command, choice ):
    
    if choice == "write":    
        ret = get_instr(address).device().write(command)  
    
    elif choice == "read":
        ret = get_instr(address).device().read(command)  

    elif choice == "query":
        ret = get_instr(address).device().query(command)  
        
    return ret




    
    
    
    
    
    
    
    
    
    
    
    
                 
