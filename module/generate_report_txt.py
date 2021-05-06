# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : generate_report_txt.py 
#--------------------------------------------------------------------------
# Generate TXT Report.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

""" 
生成MES的上傳形式 
-----------------------------------------
SerialNumber      產品序號
Station           測試站名
Step              測試步驟
Start             起始時間 (日期)
end               結束時間 (日期)
Start All         起始時間 (秒)
End All           結束時間 (秒)
Test Time         結束時間 - 起始時間
Result            測試結果
ErrorCode         錯誤代碼
UserName          操作人員
WO                None
Model             產品型號
Model Rev         產品版本
FailItemNumber  
TestTime          測試時間
Test Type         測試模式
Test SoftwareRev  軟體版本
Test DataSheetRev 測試表格版本
Test Environment  測試環境溫度
------------------------------------------
"""

#==========================================================================
# IMPORTS
#==========================================================================

import os
import sys
from datetime                 import datetime

#==========================================================================
# SAVE TXT PARAMETER
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

save_report = True
save_report_path   = root + r"\data"

#==========================================================================
# MAIN PROGRAM
#==========================================================================


class txt_report(object):
    
    def __init__(self,serial,station,step, start,start_all,end_all,testtime, result,error,operator,wo, model,modelrev,failitemnum,testtype,softrev,datasheetrev,env,label,data):

        self.serial       = str(serial)
        self.station      = str(station)
        self.step         = str(step)
        self.start        = str(start)
        self.end          = str(self.DTG()[1])
        self.start_all    = str(start_all)
        self.end_all      = str(end_all)
        self.testtime     = str(testtime)
        self.result       = str(result)   # MES只接受 P或F  (PASS/FAIL)
        self.error        = str(error)
        self.operator     = str(operator)
        self.wo           = str(wo)
        self.model        = str(model)
        self.modelrev     = str(modelrev)
        self.failitemnum  = str(failitemnum)
        self.testtype     = str(testtype)
        self.softrev      = str(softrev)
        self.datasheetrev = str(datasheetrev)
        self.env          = str(env)
        self.label        = label
        self.data         = data
        
        self.save_report        = save_report 
        self.save_report_path   = save_report_path  
        
        if self.save_report == True:
            
            self.filepath = self.save_report_path+'\\'+ self.result +'_'+ self.serial +'_'+ self.DTG()[0]+'.log'
            print("MES path: ", self.filepath)
            try:
                with open(self.save_report_path+'\\'+ self.result +'_'+ self.serial +'_'+ self.DTG()[0]+'.log','w', newline='') as txtfile:
                    
                    header = self.header()
                    txtfile.writelines(header)
                    print('[INFO] Successfully generate MES report.')
                    
                self.file_time = self.DTG()[0]
                
            except Exception as e:
                print('[INFO] Generate MES report have error happened.', e)
                
        else:
            print("[INFO] Not save MES report. if you want to change, please modify setting panel.")
              
            
    def DTG(self):
        """ 在生成檔案的情況下計算結束時間 """
        end = datetime.now()
        dt_string = end.strftime("%Y%m%d%H%M%S")
        end = end.strftime("%Y-%m-%d %H:%M:%S")
        return dt_string, end
    
    
    def header(self):
        """ 
        寫入檔案的資料形式 
        --------------------------------
        下面可以決定資料形式要不要額外加index
        """
        #------------------------------------------------------------------
        ## [ 資料中加入index ] ##       ## 用來在data前面加上index，若是需要可自行開啟 ##    
                                        ## self.data = [[xxx,xxx],[xxx,xxx],[xxx,xxx]]
        # mesdata_all =''      
        # itemnum = 0
        # for row in self.data:
        #     row.insert(0,itemnum)
        #     itemnum += 1
        #     for col in row:
        #         con = str(col)+'\t'
        #         mesdata_all += con
        #     mesdata_all+='\n'
        #------------------------------------------------------------------        
        ## [ 資料中不加入index ] ##        
        mesdata_all =''      
        for row in self.data:
            for col in row:
                con = str(col)+'\t'
                mesdata_all += con
            mesdata_all+='\n'        
        #------------------------------------------------------------------  
        ## [ 處理label ] ##        
        meslabel_all =''  
        # self.label --> ['Index', 'Test_Name', 'H_LMT', 'L_LMT', 'Test_Value', 'Test_Result', 'Unit']
        for col in self.label:
            con = str(col)+'\t'
            meslabel_all += con
        meslabel_all+='\n'  
            
            
        
        header = ["[START_LOG]\n\n",
                  "SerialNumber:       " + self.serial       + "\n",      
                  "Station:            " + self.station      + "\n",
                  "Step:               " + self.step         + "\n",
                  "Start Time:         " + self.start        + "\n",
                  "EndTime:            " + self.end          + "\n",
                  "Result:             " + self.result[0]    + "\n",   # PASS --> P ; FAIL --> F
                  "ErrorCode:          " + self.error        + "\n",
                  "UserName:           " + self.operator     + "\n",
                  "WO:                 " + self.wo           + "\n",
                  "Model:              " + self.model        + "\n",
                  "Model Rev:          " + self.modelrev     + "\n",
                  "FailItemNumber:     " + self.failitemnum  + "\n",
                  "TestTime:           " + self.testtime     + "\n",
                  "Test Type:          " + self.testtype     + "\n",
                  "Test SoftwareRev:   " + self.softrev      + "\n",
                  "Test DataSheetRev:  " + self.datasheetrev + "\n" ,
                  "Test Environment:   " + self.env          + "\n",
                  "==========================================================================\n",
                  "[START_TEST_LIST]\n",
                   meslabel_all,
                   mesdata_all,
                  "==========================================================================\n",
                  "[END_TEST_LIST]\n",
                  "==========================================================================\n",
                  "[END_LOG]\n",]
        return header


    
    
    
    
    
    
    
    
    