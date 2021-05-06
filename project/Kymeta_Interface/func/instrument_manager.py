# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
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

"""
儀器控制  GPIB、 Ethernet、Serial、DAQ
-------------------------------------------------------
在 OnInit中會建立好所有儀器的連結，只需取出變數後下達指令即可
"""
import os
import wx
import sys 
import time
import serial
import pyvisa
import nidaqmx
from pubsub            import pub
from func.path_manager import get_path
from func.json_manager import get_json_data

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class get_instr(object): 
    
    def __init__(self):
        """ 建立儀器路徑 """
        pub.subscribe(self.update_apply_via_pub, "apply")
        self.instr_path = get_path.Instrument_setting(get_path)
        
        get_instr = get_json_data(self.instr_path)
               
        self.PS_ACU   = get_instr["Instrument_Address"]["Power_Supply_ACU"]
        self.PS_BUC   = get_instr["Instrument_Address"]["Power_Supply_BUC"]
        self.Spectrum = get_instr["Instrument_Address"]["Spectrum_Analyzer"]
        self.RL_ACC   = get_instr["Instrument_Address"]["Relay_ACC"]
        self.RL_LED   = get_instr["Instrument_Address"]["Relay_LED"] 
        self.COM      = get_instr["COM_Port_Address"]["EMMC_COM"]        
      
    ## 連線所有的儀器 (可直接下指令) ##   
    ## GPIB的初始化動作不能在這裡做，否則當前儀器狀態會重設並關電 ##
    def GPIB_PS_ACU(self):
        self.PS_ACU_Device = self.Connect_VISA(self.PS_ACU)
        return self.PS_ACU_Device
    
    def GPIB_PS_BUC(self):
        self.PS_BUC_Device = self.Connect_VISA(self.PS_BUC)
        return self.PS_BUC_Device
    
    def Ethernet_SA(self):
        self.Spectrum_Device = self.Connect_VISA(self.Spectrum)
        return self.Spectrum_Device
        
    def DAQ_ACC(self, value):
        self.RL_ACC_Device = self.Connect_DAQ(self.RL_ACC, 'w', value)  
        return self.RL_ACC_Device
    
    def DAQ_LED(self, value):
        self.RL_LED_Device = self.Connect_DAQ(self.RL_LED, 'w', value) 
        return self.RL_LED_Device
    
    ##########################################################################
    ## [ 注意 ]     
    ## Serial COM Port 不能先建立物件，在被調用  
    ## 如此會有 " 拒絕存取的問題 "， 導致完全無法連線  
    ##########################################################################
    # def COM_ACU_VISA(self):
    #     """ 
    #     利用pyvisa進行序列埠連線
    #     -----------------------------------------
    #     "ASRL5::INSTR"或"COM5"都可用 
    #     """
    #     self.COM_Device = self.Connect_VISA(self.COM)
    #     self.COM_Device.timeout = 0
    #     self.COM_Device.baud_rate = 115200 
    #     self.COM_Device.data_bits = 8
    #     self.COM_Device.write_termination = '\n',  ## \r或CR：回車  \n或LF：換行  \r\n或CRLF：上述兩個序列 (也可以寫成一行)
    #     self.COM_Device.read_termination = '\n'
    #     return self.COM_Device
          
    # def COM_ACU_Serial(self):
    #     """ 
    #     利用pyserial進行序列埠連線
    #     -----------------------------------------
    #     "ASRL5::INSTR"或"COM5"都可用 
    #     """    
    #     # 這裡的timeout要設0,代表非阻塞模式，在任何情況下均立即返回，返回零或多個，直至請求的字節數(假如有設的情況下)
    #     self.COM_Device = self.Connect_Serial(self.COM, 115200)    
    #     return self.COM_Device
    
    def COM_ACU_Serial(self):
        """ 只回傳串列埠的名稱，不建立裝置物件 """
        return self.COM
        
    def update_apply_via_pub(self, apply):
        get_instr = get_json_data(self.instr_path)
        
        """ 當Setting改變時重新取得參數 (按下Apply時) """
        
        self.PS_ACU   = get_instr["Instrument_Address"]["Power_Supply_ACU"]
        self.PS_BUC   = get_instr["Instrument_Address"]["Power_Supply_BUC"]
        self.Spectrum = get_instr["Instrument_Address"]["Spectrum_Analyzer"]
        self.RL_ACC   = get_instr["Instrument_Address"]["Relay_ACC"]
        self.RL_LED   = get_instr["Instrument_Address"]["Relay_LED"]
        self.COM      = get_instr["COM_Port_Address"]["EMMC_COM"]          

    def Connect_VISA(self, address):
        """ 
        連接GPIB、Ethernet、Serial COM -- 不過命令須從回傳的device再去做下達的動作
        -------------------------------------------
        Instrument.JSON的設定方式，可透過VISA查詢
        [ GPIB ] GPIB0::5::INSTR
        [ Ethernet ] TCPIP0::192.168.0.100::inst0::INSTR
        [ Serial ] COM1
        """

        for i in range(50):
            try: 
                 rm = pyvisa.ResourceManager()                           
                 device = rm.open_resource(address, open_timeout=1000) 
                 if device:
                    msg = "[VISA] Connect "+ address +" Successfully."
                    break
                 else:
                    time.sleep(2)
                    continue
            except Exception as e:
                 device = None
                 msg = "[VISA] No Connect "+ address
                 self.traceback(e)
        
        if not device:
            self.prompt_msg("Check the VISA connection "+ address + "." )   
        print(msg)       
        return device
    
    def Connect_Serial(self, address, baudrate):
        """ 
        由於使用pyVISA會在Serial出現 VI_ERROR_TMO、VI_ERROR_ASRL_OVERRUN的錯誤資訊
        ，因此想嘗試改用pySerial
        """
        device = serial.Serial(address, baudrate, parity='N', stopbits=1, bytesize=8, timeout=0)   # 初始化序列通訊埠 
        if not device:
            self.prompt_msg("Check the Serial connection "+ address + "." )           
        return device
        
        ## 使用方式 ##
        # while True:
        #     while device.in_waiting:
        #         # str=device.read(ser.in_waiting ).decode("gbk")
        #         data_raw = ser.readline()  # 讀取一行
        #         data = data_raw.decode()
            
        #         if(str=="XXX"):#退出標誌
        #             break
        # device.close()
    
        
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
        """ 顯示訊息 """
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True) 
            
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))
                 

    

    
    
    
    
    
    
    
    
    
    
    
    
    
                 
