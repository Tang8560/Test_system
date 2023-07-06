# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : test_daq.py
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
#==========================================================================
# IMPORTS
#==========================================================================

import os
import wx
import sys
import nidaqmx

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class daq_instr(object):

    def __init__(self, address, command, function):
        """
        連接 DAQ --- 由於不用下指令，所以在function內填入輸出
        ------------------------------
        Instrument.JSON的設定方式，未填下的情況下會取出下面的預設值
        [ 數位 ] Dev1/port0/line0
        [ 類比 ] Dev1/ai0   Dev1/ao0
        """

        self.address = address
        self.command = command
        self.function = function

        try:
            self.command = float(self.command)
        except:
            self.command = self.command == "True"

        self.OnInit()

    def OnInit(self):

        if not self.address:
            system = nidaqmx.system.System()
            if not system.devices:
                self.prompt_msg("Cannot found the DAQ device.")
            else:
                self.name = system.devices[0].name
                ## 未輸入情況下的預設值 ##
                self.address = self.name + "/port0/line0"

        ## 建立任務 ## -- with 建立的task，需在with的結構內下指令才有用

        address_pin = self.address.split('/')

        try:
            with nidaqmx.Task() as task:
                if self.function == "Digital Write":
                    if len(address_pin) == 3:
                        task.do_channels.add_do_chan (self.address,"mychannel")
                        task.start()
                        task.write(self.command)
                        self.data = ""
                    else:
                        self.data = ""
                        self.prompt_msg("Something error happened on the DAQ address.")

                elif self.function  == "Digital Read":
                    if len(address_pin) == 3:
                        task.di_channels.add_di_chan (self.address)
                        task.start()
                        self.data = task.read()
                    else:
                        self.data = ""
                        self.prompt_msg("Something error happened on the DAQ address.")

                elif self.function  == "Analog Write":
                    if len(address_pin) == 2:
                        task.ao_channels.add_ao_voltage_chan(self.address,"analog_write",0,5)
                        task.start()
                        self.data = task.write(self.command)
                    else:
                        self.data = ""
                        self.prompt_msg("Something error happened on the DAQ address.")

                elif self.function  == "Analog Read":
                    if len(address_pin) == 2:
                        task.ai_channels.add_ai_voltage_chan(self.address)
                        task.start()
                        self.data = task.read()
                    else:
                        self.data = ""
                        self.prompt_msg("Something error happened on the DAQ address.")

                else:
                    self.data = ""
                    self.prompt_msg("The definition of DAQ IO port have something error.\t ex: [DIGITAL] Dev1/port0/line0]\t [ANALOG]  Dev1/ai0, Dev1/ao0" )
                task.stop()

        except Exception as e:
            self.traceback(e)
            self.data = ""
            msg = "[DAQ] No Connect "+ self.address
            print(msg)

        return self.data

    def prompt_msg(self, message):
        """ 顯示訊息 """
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True)

    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))





