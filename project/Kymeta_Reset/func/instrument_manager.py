# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : instrument_manager.py
#--------------------------------------------------------------------------
# Build all device connection.
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
import nidaqmx
from pubsub            import pub
from func.path_manager import get_path

#==========================================================================
# IMPORTS JSON Function
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from event.json_func import get_json_data

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class get_instr(object):

    def __init__(self):
        """ instrument """
        self.instr_path = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_path.Instrument_setting(get_path)
        print(self.instr_path)
        get_instr = get_json_data(self.instr_path)
        self.RL_transecR = get_instr["Instrument"]["Relay_TRANSEC_R"]
        self.RL_transecG = get_instr["Instrument"]["Relay_TRANSEC_G"]
        self.RL_netR     = get_instr["Instrument"]["Relay_NET_R"]
        self.RL_netG     = get_instr["Instrument"]["Relay_NET_G"]
        self.RL_statusR  = get_instr["Instrument"]["Relay_STATUS_R"]
        self.RL_statusG  = get_instr["Instrument"]["Relay_STATUS_G"]
        self.RL_TXR      = get_instr["Instrument"]["Relay_TX_R"]
        self.RL_TXG      = get_instr["Instrument"]["Relay_TX_G"]
        self.RL_RXR      = get_instr["Instrument"]["Relay_RX_R"]
        self.RL_RXG      = get_instr["Instrument"]["Relay_RX_G"]
        self.RL_PWRR     = get_instr["Instrument"]["Relay_PWR_R"]
        self.RL_PWRG     = get_instr["Instrument"]["Relay_PWR_G"]


    def DAQ_transecR(self, value):
        self.RL_transecR_Device = self.Connect_DAQ(self.RL_transecR, 'w', value)
        return self.RL_transecR_Device

    def DAQ_transecG(self, value):
        self.RL_transecG_Device = self.Connect_DAQ(self.RL_transecG, 'w', value)
        return self.RL_transecG_Device

    def DAQ_netR(self, value):
        self.RL_netR_Device = self.Connect_DAQ(self.RL_netR, 'w', value)
        return self.RL_netR_Device

    def DAQ_netG(self, value):
        self.RL_netG_Device = self.Connect_DAQ(self.RL_netG, 'w', value)
        return self.RL_netG_Device

    def DAQ_statusR(self, value):
        self.RL_statusR_Device = self.Connect_DAQ(self.RL_statusR, 'w', value)
        return self.RL_statusR_Device

    def DAQ_statusG(self, value):
        self.RL_statusG_Device = self.Connect_DAQ(self.RL_statusG, 'w', value)
        return self.RL_statusG_Device

    def DAQ_TXR(self, value):
        self.RL_TXR_Device = self.Connect_DAQ(self.RL_TXR, 'w', value)
        return self.RL_TXR_Device

    def DAQ_TXG(self, value):
        self.RL_TXG_Device = self.Connect_DAQ(self.RL_TXG, 'w', value)
        return self.RL_TXG_Device

    def DAQ_RXR(self, value):
        self.RL_RXR_Device = self.Connect_DAQ(self.RL_RXR, 'w', value)
        return self.RL_RXR_Device

    def DAQ_RXG(self, value):
        self.RL_RXG_Device = self.Connect_DAQ(self.RL_RXG, 'w', value)
        return self.RL_RXG_Device

    def DAQ_PWRR(self, value):
        self.RL_PWRR_Device = self.Connect_DAQ(self.RL_PWRR, 'w', value)
        return self.RL_PWRR_Device

    def DAQ_PWRG(self, value):
        self.RL_PWRG_Device = self.Connect_DAQ(self.RL_PWRG, 'w', value)
        return self.RL_PWRG_Device


    def Connect_DAQ(self, address, function = "w", value = False):
        """
        連接 DAQ --- 由於不用下指令，所以在function內填入輸出
        ------------------------------
        Instrument.JSON的設定方式，未填下的情況下會取出下面的預設值
        [ 數位 ] Dev1/port0/line0
        [ 類比 ] Dev1/ai0   Dev1/ao0
        ------------------------------
        注意開電是False，關電是True
        """

        ## 單純取出字串 ##
        deviceIO = address

        if not deviceIO:
            system = nidaqmx.system.System()
            if not system.devices:
                self.prompt_msg("Cannot found the DAQ device.")
            else:
                self.name = system.devices[0].name
                ## 未輸入情況下的預設值 ##
                deviceIO =self.name + "/port0/line0"

        ## 建立任務 ##
        ## --- 由於是使用 with 建立的task，因此需在with的結構內下指令才有用

        deviceIO_pin = deviceIO.split('/')
        try:
            with nidaqmx.Task() as task:
                if len(deviceIO_pin) == 3:
                    if function == "w":
                        task.do_channels.add_do_chan (deviceIO,"digital_write")
                        task.start()
                        self.data = task.write(value)

                    elif function == "r":
                        task.di_channels.add_di_chan (deviceIO)
                        task.start()
                        self.data = task.read()
                elif len(deviceIO_pin) == 2:
                    if function == "w":
                        task.ao_channels.add_ao_voltage_chan(deviceIO,"analog_write",0,5)
                        task.start()
                        self.data = task.write()

                    elif function == "r":
                        task.ai_channels.add_ai_voltage_chan(deviceIO)
                        task.start()
                        self.data = task.read()
                else:
                    self.prompt_msg("The definition of DAQ IO port have something error.\t ex: [DIGITAL] Dev1/port0/line0]\t [ANALOG]  Dev1/ai0, Dev1/ao0" )
                task.stop()

        except Exception as e:
            self.data = None
            msg = "[DAQ] No Connect "+ deviceIO
            self.prompt_msg("Check the DAQ connection "+ deviceIO + "." )
            self.traceback(e)
            print(msg)
        return self.data

    def prompt_msg(self, message):
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True)

    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))


