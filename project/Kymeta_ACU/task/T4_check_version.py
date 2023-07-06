# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : T4_check_version.py
#--------------------------------------------------------------------------
# Check the ACU version after flash programming completelly.
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
import requests
from pubsub            import pub
from requests.auth     import HTTPBasicAuth

#==========================================================================
# IMPORTS Function
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from func.path_manager  import get_path
from event.json_func    import get_json_data
from module.ping_device import ping_device

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class T4_check_version(object):

    def __init__(self, thread_event):

        ## 預設檢查version的url路徑 ##
        self.Build()
        self.OnInit()

    def Build(self):
        self.product_path = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_path.Product_setting(get_path)
        get_product = get_json_data(self.product_path)
        self.ver_url    = get_product["Product"]["Version_URL"]
        self.host_IP    = get_product["Product"]["Host_IP"]
        self.product_IP = get_product["Product"]["Product_IP"]

    def OnInit(self):

        #----------------------------------------------------------------------
        ## [ 0.檢查版本- 利用ping等待確認產品連線 ] ##
        server_alive = ping_device(self.host_IP, self.product_IP, 50)  # 次數 # timeout
        #----------------------------------------------------------------------
        ## [ 1.檢查版本- 取出網址連結下的回傳值 ] ##
        print(server_alive)
        print(self.ver_url)

        if server_alive:
            try:
                auth = HTTPBasicAuth('mfg', '?M4nuf#!')
                header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

                r = requests.get(url=self.ver_url, headers = header, auth=auth, verify=False)
                jf = r.json()

                print(jf)
                self.ver_initial = jf["version"]
                ## fvt-ge046c70-dirty ==> ['ge046c70', 'dirty']
                self.ver = re.findall('(?<=-)\w+',self.ver_initial)[0]

                print("[INFO] Flash Programming Version: ", self.ver_initial)

            except Exception as e:

                self.traceback(e)
                self.ver = "Error"
                self.ver_initial = "Error"
        else:
            assert ConnectionError

    def version(self):
        try:
            pub.sendMessage("pass_to_grid",test_value = self.ver)
            pub.sendMessage("subtask_processbar", value = 3)
        except Exception as e:
            self.traceback(e)
            pub.sendMessage("pass_to_grid",test_value = "Boot Error")

    def version_initial(self):
        try:
            pub.sendMessage("pass_to_grid",test_value = self.ver_initial)
            pub.sendMessage("subtask_processbar", value = 4)
        except Exception as e:
            pub.sendMessage("pass_to_grid",test_value = "Boot Error")

    def prompt_msg(self, message):
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True)

    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,'line '+ str(traceback.tb_lineno))



