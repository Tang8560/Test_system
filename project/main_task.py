# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : main_task.py 
#--------------------------------------------------------------------------
# Control the test flow.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================


# perf_counter有一個特點,就是如果函數A中調用了函數B,函數2中先調用了perf_counter,
# 那麼perf_counter的第一次計數就是從函數B中的調用算起。

# Notice: File name and class name need to be as same

#==========================================================================
# IMPORTS
#==========================================================================
import os
import sys 
import glob   
import time
import importlib.util
from pubsub import pub 
from datetime import datetime
        
#==========================================================================
# PUB SENDMESSAGE
#==========================================================================
test_end        = "test_end"
generate_csv    = "generate_csv"
generate_txt    = "generate_txt"
generate_serial = "generate_serial"
bar_range       = "task_processbar_range"
bar_value       = "task_processbar"
subbar_range    = "subtask_processbar_range"
subbar_value    = "subtask_processbar"
upload_file     = "upload_file"

#==========================================================================
# MAIN PROGRAM
#==========================================================================   
        
def main_process(project_path, table, thread_event):
    
    spec_table, func_data = table[0], table[1]             
    
    ## [ IMPORT TASK FUNCTION ] ##
    ## 在project選定後，以import的方式載入在project下task資料夾內的所有py檔
    ## 之後調用上以檔名調用即可，不含後綴
    ## 效果等同於 "import task_name"
    ## ------------------------------------------
    ## user guide:
    ## <method-1> getattr(Main, format("task_name")).class_name()
    ## <method-2> class_name = getattr(getattr(Main, format("task_name")), "class_name")
    ##            class_name()
    
    print("Task File Path: " + project_path +'\\task')
    sys.path.append(project_path)
    print("[INFO] import task file")
    
    try:
        task_files = glob.glob(project_path +'\\task\\*.py')
        if task_files:
            for file_path in task_files:
                filename = os.path.basename(file_path)
                (file, ext) = os.path.splitext(filename)
                modualspec = importlib.util.spec_from_file_location("task", file_path)                
                setattr(main_process, format(file), importlib.util.module_from_spec(modualspec))                
                modualspec.loader.exec_module(getattr(main_process, format(file)))     
                print(file)
    except Exception as e:
        print(e)               
                
    
    ## [ TEST PROCESS ] ##
    # getattr(main_process, format("initial")).initial(self.thread_event)
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    test_start_time = time.perf_counter()   

    init = getattr(getattr(main_process, format("initial")), "initial")
    init(thread_event)
    
    task_function_ = func_data[0]        
    script = task_function_.loc[:,"Script"]
    function = task_function_.loc[:,"Function"]
    # code = func_data[1]
    # compare = func_data[2]
    
    
    pub.sendMessage(bar_range, value = len(list(dict.fromkeys(script))))
    pub.sendMessage(bar_value, value = 0)
    pub.sendMessage(subbar_value, value = 0)
    bar_task_value = 0
    task_old = None
    
    for task in zip(script, function):
        print("[INFO] Current task:" + str([task[0], task[1]]))
        
        if task[0] != task_old :          
            task_old = task[0]
            bar_task_value += 1
            pub.sendMessage(bar_value, value = bar_task_value)
            
        try:
            task_function = getattr(getattr(main_process, format(task[0])), task[0])            
            ## determine the value on the function whether is valid ## 
            if  isinstance(task[1], str):
                call_func = getattr(task_function(thread_event), format(task[1]))
                call_func()
            else:
                task_function(thread_event)
                
        except Exception as e:
            print(e)
            pub.sendMessage(subbar_value, value = 0)
            pass

    end = getattr(getattr(main_process, format("end")), "end")
    end(thread_event)
    test_end_time = time.perf_counter()   
    
    print("test start time: ", test_start_time)                 
    print("test end time: "  , test_end_time)

    ## [ AFTER TEST ] ##
    time.sleep(1)
    print("========== TEST END ==========")
    time.sleep(1)
    pub.sendMessage(test_end, date = date_time, start = test_start_time, end = test_end_time)
    print("======== GENERATE CSV ========")
    time.sleep(1)
    pub.sendMessage(generate_csv)
    print("======== GENERATE TXT ========")  
    time.sleep(1)
    pub.sendMessage(generate_txt)   
    print("======  GENERATE SERIAL  ======")
    time.sleep(1)  
    pub.sendMessage(generate_serial)
    print("========  UPLOAD FILE  ========")
    time.sleep(1)
    pub.sendMessage(upload_file)    


        
        
        
        
        