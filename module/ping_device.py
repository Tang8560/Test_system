# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : ping_device.py
#--------------------------------------------------------------------------
# CMD to check connection successfully
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

import os
import re

def ping_device(host_IP, product_IP, ping_times):
    
    """ 若是這邊發生 Fail, 請檢查連線的IP是否正確 """
    
    for t in range(ping_times):
        
        #######################################################################################
        ## 開啟CMD執行ping的功能 ##       
        #######################################################################################
        ## [1] os.Popen ##
        
        output = os.popen('ping -S %s -n 2 -w 10 %s' % (host_IP, product_IP), 'r')
        result = output.read()
        # 沒關會出現ResourceWarning: subprocess xxx is still running的錯誤 ##
        output.close()
        
        ## [2] Subprocess.Popen ##
        
        # print("time ", t)
        # try:
        #     output = subprocess.Popen(['ping','-S', self.host_IP, "-n", "2", "-w", "10", self.product_IP ] ,stdout=subprocess.PIPE, shell =True)
    
        #     output.wait()
        #     if output.poll() == 0:
        #         out, err = output.communicate(timeout=15)
        #         result = out.decode(encoding='big5')
                
        # except Exception as e:
        #     print(e)
        #######################################################################################    
        print(result)           
        ## 取出Ping完後的回傳值 (只抓數字) ##
        ret_list = re.findall('= ([0-9]+)',result)
                    
        ## 當傳送封包和收到封包一致時代表連線成功 ##
        
        if ret_list[0] == ret_list[1]:
            server_alive = True
            print("[INFO] Successfully get the server.")
            break
        
        ## 當封包結果不一致時繼續執行 ##
        else: 
            if t < ping_times:
                server_alive = False
                continue
            else:
                print("[INFO] Connect Server Error")
                print("Check the end device setting or network connection error")
                server_alive = False
                self.prompt_msg("Product connection error")
                print("[INFO] Product connection error.")
                break
    return server_alive