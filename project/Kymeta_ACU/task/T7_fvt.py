# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : T7_fvt.py
#--------------------------------------------------------------------------
# Perform some simple CURL operations with BUC web interface.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================


#==========================================================================
# IMPORTS
#==========================================================================
import os
import wx
import re
import sys
import json
import time
import warnings
import requests
import pandas as pd
from pubsub                   import pub
from module.ping_device       import ping_device
from func.path_manager        import get_path
from func.instrument_manager  import get_instr

#==========================================================================
# IMPORTS JSON Function
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from event.json_func import get_json_data

#==========================================================================
# PARAMETER
#==========================================================================

""" 決定測試項目是否存取log檔 """
save_log = True

""" 載入Spec，用來確定測試項目的子項目數量 """ 
spec_path = get_path.Specification(get_path)
spec_data = pd.read_csv(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + spec_path)
test_item_num = list(spec_data["Class"]).count("FVT")

#==========================================================================
# MAIN PROGRAM
#==========================================================================
spec_path = get_path.Specification(get_path)

class T7_fvt(object):

    def __init__(self, thread_event):
        try:
            self.Build()
            self.OnInit()
        except Exception as e:
            print("[ERROR] [T7] Get task element failed ")
            print("Please check by the following steps")
            print("1. Check the 'instrument_manager.py' or connection error.")
            print("2. Setting error on the 'path_manager.py' or file loss.")
            self.traceback(e)
            for item in range(test_item_num):
                pub.sendMessage("pass_to_grid",test_value = "FVT Error")
    
    def Build(self):       
        ## get FVT url ##

        self.product_path = get_path.Product_setting(get_path)  
        print("\\".join(os.path.abspath(__file__).split('\\')[:-2]) + self.product_path)          
        get_product = get_json_data("\\".join(os.path.abspath(__file__).split('\\')[:-2]) + self.product_path)
        self.fvt_url = get_product["Product"]["FVT_URL"]
        self.host_IP    = get_product["Product"]["Host_IP"]
        self.product_IP = get_product["Product"]["Product_IP"]

        self.instr  =  get_instr()
        self.GPIB_PS_BUC  =  self.instr.GPIB_PS_BUC()
    
    def OnInit(self):  
        self.GPIB_PS_BUC.write("VOLTage 24 ,(@2)")
        self.GPIB_PS_BUC.write("CURRent 3 ,(@2)")
        self.GPIB_PS_BUC.write("OUTPut ON ,(@2)")
        

        ## [ 0.fvt- use ping to check oonnection successfully ] ## 
        server_alive = ping_device(self.host_IP, self.product_IP, 50)  # 次數 # timeout
        ## [ 1.fvt ] ##    
        if server_alive:
            ## Get value from the webpage ##
            comb = self.fvt_buc()
            print("[T7] Get FVT data: ", str(comb))
         
        ## 取出所有分類在FVT的所有欄位 ##    
        specific_fvt_data = self.fvt_check_spec()
        
        ## 取出所有分類在FVT的Test_Name ##
        specific_fvt_testname = specific_fvt_data["Test_Name"]
        
        self.T7_range = len(specific_fvt_testname)
        pub.sendMessage("subtask_processbar_range", value = self.T7_range)
        
        for item in enumerate(specific_fvt_testname):

            # print(item[1].split('-')[1])
            # print(comb[item[1].split('-')[1]])
            # print(type(comb[item[1].split('-')[1]]))
            
            if item[1].split('-')[1] in comb:
                ## 當測試規格中的值出現在網頁抓到的所有值comb中，就從JSON格式下的comb取出對應的值 ##
                pub.sendMessage("pass_to_grid",test_value = comb[item[1].split('-')[1]])
                pub.sendMessage("subtask_processbar", value = item[0]+1)
                    
        self.GPIB_PS_BUC.write("OUTPut OFF ,(@2)")             
   
    def fvt_buc(self): 
        """ 取出網頁上處理後抓到的 [name, value] """
        warnings.simplefilter('ignore',ResourceWarning)          
        auth = requests.auth.HTTPBasicAuth('mfg', '?M4nuf#!')
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}      
    
        for times in range(50):
            try:
                fvt_json = requests.get(url = self.fvt_url, headers = header, auth=auth, verify=False)
                fvt = fvt_json.json()
                fvt_data = fvt["data"]["testsuites"][0]
                Failures  = fvt_data["failures"]
                testsuite = fvt_data["testsuite"]
             
                comb= {}      
                for testcase in testsuite:                  
                    for subtestcase in testcase["testcase"]:                
                         comb[str(subtestcase["name"])] = subtestcase["value"]
                                                                 
                if str(subtestcase["name"]) == "gnssFix":                   
                    if str(subtestcase["value"]) != "" and str(subtestcase["value"]) != "0":
                       break
                    else: 
                        continue 
                with open('FVT.json', 'w') as fp:
                    json.dump(fvt, fp)
                fvt_json.close()               
            except:
                comb = 'Cannot fetch the json data.! Please check the connection route or Something wrong happen on the UUT!'   
        return comb
    
    def fvt_check_spec(self):       
        """ 
        取出在column [class] 下為FVT的所有對應欄位
        -------------------------------------------------------------
        用於將網頁取出的值和對應在規格上的值比較，並照規格上的順序依序填入
        """
        specific_data = pd.read_csv(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+spec_path)
        group_class = specific_data.groupby("Class", sort = False)
        specific_fvt_data = group_class.get_group("FVT")
        
        return specific_fvt_data          

    def prompt_msg(self, message): 
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True) 
            
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,'line '+ str(traceback.tb_lineno)) 
     
