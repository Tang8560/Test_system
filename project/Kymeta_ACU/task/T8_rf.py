# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : T8_rf.py
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

"""KYMETA RF TESE"""
#==========================================================================
# IMPORTS
#==========================================================================
import os, re, wx
import sys, pip, time
import json
import numpy
import requests
import paramiko
import scipy.fftpack
import pandas as pd
from pubsub                   import pub
from func.path_manager        import get_path
from func.instrument_manager  import get_instr
from func.SA268x              import TG, TG_level, freq_span, center_freq, marker_on, q_makerY
from module.ping_device       import ping_device

#==========================================================================
# IMPORTS JSON Function
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from event.json_func import get_json_data


## 自動安裝套件 ##
# module = ['requests', 'paramiko', 'pyvisa', 'scipy.fftpack', 'numpy']
# for m in module:
#     if m not in sys.modules.keys():
#         pip.main(['install', m])
#     else: 
#         print("%s already install" %m)
#     exec('import ' + m)  

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
requests.packages.urllib3.disable_warnings()

#==========================================================================
# MAIN PROGRAM
#==========================================================================

""" 決定測試項目是否存取log檔 """
save_log = True

""" 載入Spec，用來確定測試項目的子項目數量 """ 
spec_path = get_path.Specification(get_path)
spec_data = pd.read_csv(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + spec_path)
test_item_num = list(spec_data["Class"]).count("RF")

spec_path = get_path.Specification(get_path)


class T8_rf(object):
    
    def __init__(self, thread_event):       
        try:
            self.Build()
            self.OnInit()
        except Exception as e:
            print("[ERROR] [T8] Get task element failed ")
            print("Please check by the following steps")
            print("1. Check the 'instrument_manager.py' or connection error.")
            print("2. Setting error on the 'path_manager.py' or file loss.")
            self.traceback(e)
            for item in range(test_item_num):
                pub.sendMessage("pass_to_grid",test_value = "RF Error")
    
    def Build(self):    
        ## Get product IP and the connection username ##
        self.product_path = get_path.Product_setting(get_path) 
        get_product = get_json_data("\\".join(os.path.abspath(__file__).split('\\')[:-2]) + self.product_path)
        self.host_IP    = get_product["Product"]["Host_IP"]
        self.product_IP = get_product["Product"]["Product_IP"]
        self.username   = get_product["Product"]["Username"]
        
        ## Get RF test URL ##
        self.rf_url = get_product["Product"]["RF_URL"]
        
        ## Get the location of SSH key ##
        self.sshkey_path = get_path.SSH_key(get_path) 
        self.ssh_key = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + self.sshkey_path
         
        self.instr  =  get_instr()
        self.Ethernet_SA  =  self.instr.Ethernet_SA()          # connect to SA268x spectrum analyzer 

    def OnInit(self):       
        ## [ 0.rf- 利用ping等待確認產品連線 ] ## 
        server_alive = ping_device(self.host_IP, self.product_IP, 50)  # 次數 # timeout

        set_freq = [["940000000", "950 MHz"], ["1300000000", "1350 MHz"],
                    ["1720000000", "1750 MHz"], ["2100000000", "2145 MHz"]]
        test_value = []
        
        TG_level(self.Ethernet_SA, "-20")
        freq_span(self.Ethernet_SA, "0 Hz")
        
        #----------------------------------------------------------------------
        ## [ 1.RF -利用SSH key登入產品 ] ## 
        self.connect(self.ssh_key)
        ## [ 2.RF -利用已知量測的頻率執行迴圈 ] ##                
        for f in set_freq:
            ## [ 3.RF -Set local frequency ] ## 
            self.set_loc(f[0])
            ## [ 4.RF -取出SA抓到的訊號強度 ] ##             
            strength = self.spectrum_strength(self.Ethernet_SA, f[1])
            print("freq: ", f[1])
            ## [ 5.RF -取出網頁抓到的IQ值 ] ##            
            return_iq = self.get_iq(f[1])
            ## [ 6.RF -將IQ值進行FFT並取出強度、頻率 ] ##              
            maxx_i, maxy_i, maxx_q, maxy_q = self.convert(return_iq)
            test_value.extend([str(strength), str(maxx_i[0]/1000000), str(maxy_i[0]), str(maxx_q[0]/1000000), str(maxy_q[0])])  # 一次只能append一個東西
        print(test_value)
        self.ssh.close()
        
        TG(self.Ethernet_SA, "Off")
        # power_off(self.Ethernet_SA)
        
        self.T8_range = len(test_value)
        pub.sendMessage("subtask_processbar_range", value = self.T8_range)
        
        for item in enumerate(test_value):
            pub.sendMessage("pass_to_grid",test_value = item[1])
            pub.sendMessage("subtask_processbar", value = item[0]+1)  

    def connect(self, sshk):
        """ use SSH key to login product """
        # sshk = 'acu_fvt_ossh_key' # openSSH private key
        # connect to kymeta product by ssh connection
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname = self.product_IP, port = 22, username = self.username, key_filename=sshk)

        except Exception as e:
            self.traceback(e)
            print("ssh connection error")

    def set_loc(self, lo_freq): 
        """ set local frequency """    
        if self.ssh._transport is None: 
            print("please check openssh private key location")
            sys.exit()
        else:
            command = "libkymetaservice-set-setting.py -s hardware-service -i rx-demod -k lo_freq:" + lo_freq  
            self.ssh.exec_command(command = command, bufsize=-1, timeout=None, get_pty=False, environment=None)
            # print(stdout.readlines().decode('utf-8')) 
    
    def spectrum_strength(self, device, test_freq): 
        """ After use trace generator (TG) to feed signal, then get the strength return. """        
        if device is None: 
            sys.exit()           
        trace = "1" 
        center_freq(device, test_freq)   
        TG(device, "On")
        marker_on(device, trace, "On")
        time.sleep(2)
        
        Y = float(q_makerY(device, trace))  
        marker_on(device, trace, "Off")
        print("strength: ", Y)       
        return Y
    
    def get_iq(self,n):
        """CURL""" 
        # --Curl get IQ data

        auth = requests.auth.HTTPBasicAuth('mfg', '?M4nuf#!')
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}    
        try:
            r = requests.get(url="https://192.168.0.10/v1/internal/adc-samples", headers=header, auth=auth, verify=False)
            # parser html
            return_iq = r.json()
            with open('RF'+n+'.json', 'w') as fp:
                json.dump(return_iq, fp)    
                
        except requests.HTTPError:  # HTTPError
            # print(e.code)
            print('please check the connection status')
            return_iq = "NA"

        return return_iq


    def convert(self, return_iq):
        """
        將IQ data經過FFT轉換後得到強度、頻率
        """
        # --get I and Q Amp&Freq by IQ data usage FFT
 
        data = return_iq
        sample_freq = data['sample_freq']
        samples = data['samples']
        print("sample_freq: ", data['sample_freq'])
        
        sample_i = numpy.empty([len(samples)])
        sample_q = numpy.empty([len(samples)])
        # sampleint = np.empty([len(samples)])
        # sampletime = np.empty([len(samples)])
        
        for i in range(len(samples)):
            sample_i[i] = int(samples[i][0])
            sample_q[i] = int(samples[i][1])     
            
        N = len(sample_i)
        T = 1/int(sample_freq)
        yf_i = (scipy.fftpack.fft(sample_i))
        yf_q = (scipy.fftpack.fft(sample_q))
        xf = numpy.linspace(0.0, 1.0//(2.0*T), N//2)
        #fig,ax = plt.subplots()
        # ax.plot(xf,1.0/N * numpy.abs(yf_i[:N//2]))
        # plt.show()
        
        maxindx_i = numpy.where(numpy.abs(yf_i[:N//2]) == max(numpy.abs(yf_i[:N//2])))
        maxy_i = numpy.abs(yf_i[maxindx_i])/N
        maxx_i = xf[maxindx_i]
        
        maxindx_q = numpy.where(numpy.abs(yf_q[:N//2]) == max(numpy.abs(yf_q[:N//2])))
        maxy_q = numpy.abs(yf_q[maxindx_q])/N
        maxx_q = xf[maxindx_i]
        
        print("[T8] IQ result ")
        print("I_freq: ", str(maxx_i))
        print("I_Amp: ", str(maxy_i))
        print("Q_freq: ", str(maxx_q))
        print("Q_Amp: ", str(maxy_q))
        return maxx_i, maxy_i, maxx_q, maxy_q

    def prompt_msg(self, message): 
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True) 
            
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,'line '+ str(traceback.tb_lineno)) 
        
        
   
    
