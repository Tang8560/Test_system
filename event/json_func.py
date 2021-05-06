# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : T8_rf.py
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

"""
執行 取出JSON資料、修改JSON資料、存入JSON資料
---------------------------------------------------
注意 JSON在編輯時，最後一項和最後的大括號後不能有逗號
斜線的使用，不能是單獨的 "\"，必須是 "\\" 或 "/"
"""
import os
import json

############################################################

## 開啟JSON檔案的位置 ##
# path = 'C:\\Users\\6065\\Desktop\\ATS_temp\\v3\\config\\product.json'
# path = "C:\\Users\\6065\\Desktop\\ATS_temp\\v3\\config\\station.json"

## 修改JSON檔案的位置 ##
# path1 = '\\config\\XXX.json'

 ###########################################################
       
params_rev={}

def get_json_data(path):
    """ get JSON data """
    json_path = path
    
    ## [ 單獨執行時 ] ##
    # json_path = path

    print("[INFO] Loading JSON:",json_path)  
    with open(json_path,'r',encoding = 'utf8') as f:
        params = json.load(f) 
    # print("parameter:",params) 
    f.close()    
    return params

def revised_json_data(params, item, key, value):
    """ 修改JSON資料 """
    params[item][key] = value      
    params_rev = params         # Save revise data to the variable "params_rev" 
    return params_rev

def write_json_data(path1, params_rev):
    json_path1 = path1
    with open(json_path1,'w') as r:    
        json.dump(params_rev,r, indent = 4, separators=(',', ': '))        
    r.close()
    print("[INFO] Revising JSON:",json_path1)

"""
使用上需要連續
"""

# get_data = get_json_data(path)

# revise_data = revised_json_data(get_data, 'MES_Information' ,'MES_Location', 'kymeta')
# write_data = write_json_data(path1, revise_data)
  
    
    
    
    
    
    
    
    



    
    