# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : server_check.py
#--------------------------------------------------------------------------
# Check Server Alive.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================
      

import os
import re
import time

def server_check(MES_Server,ping_times,timeout):
    """ 
    用於確認MES是否在可連線的狀態 
    -----------------------------------------
    MES_Server: MES的連線ip
    ping_times: ping次數
    timeout: 超時
    -----------------------------------------
    return: 是否連上伺服器，訊息 (group, test, msg) 
    """
    ## 計時器功能，計算連線時間 <t1, t2> ##
    t1 = time.perf_counter()

    for t in range(ping_times):
        ## 開啟CMD執行ping的功能 ##
        output = os.popen('ping %s -n 1' %MES_Server, 'r')
        result = output.read()
        
        ## 沒關會出現ResourceWarning: subprocess xxx is still running的錯誤 ##
        output.close()
        
        ## 取出Ping完後的回傳值 ##
        ret_list = re.findall('= ([0-9]+)',result)
        t2 = time.perf_counter() 

           
        ## 當傳送封包和收到封包一致時代表連線成功 ##
        if ret_list[0] == ret_list[1]:
            server_alive = True
            msg = u"[INFO] Successfully get the server."
            break
        
        ## 當封包結果不一致時繼續執行 ##
        else: 
            if t2-t1 < timeout:
                continue
            else:
                print("[SC01] Connect Server Error")
                print("Check the end device setting or network connection error")
                server_alive = False
                msg = u"[INFO] MES connection error."
                break                 
    print(msg)
    return server_alive, msg
    
# r = server_check("www.google.com",10,10)

