# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : info_func.py
#--------------------------------------------------------------------------
# Display Test Info
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================


#==========================================================================
# IMPORTS
#==========================================================================
import os
import glob

#==========================================================================
# IMPORTS FUNCTION
#==========================================================================
from event.json_func import get_json_data

#==========================================================================
# INFO LIST ITEM
#==========================================================================
class Item(object):
    def __init__(self, item, info, classname):
        """ List attribution """
        self.item = item
        self.info = info
        self.classname = classname
        
#==========================================================================
# MAIN PROGRAM
#==========================================================================

class info_event(object):
    
    def __init__(self, project_path):

        self.project_files = os.walk(project_path)
        self.get_json_data()        
        
    def get_json_data(self):
        ## Get all json file ##
        json_data = []
        for file in self.project_files:
        
            json_file = glob.glob(file[0] +'\*.json')
            json_data.extend(json_file)
        
        ## Get all parameter ##
        self.para = []  
        for get_data in json_data:
            data = get_json_data(get_data)
            for i in data:
                for j in data[i]:
                    self.para.append([j, data[i][j], i])
                    
    def get_info_items(self):            
        ## Transfer to item data format ## 
        ## Create a list of objects ##
        """
        format:
        ----------------------------------------
        info_items = [
              Item("unknown", "unknown", "unknown"),
              Item("unknown", "unknown", "unknown"),
              Item("unknown", "unknown", "unknown"),
             ]
        """
        info_items = []
        for item in self.para:
            info_items.append(Item(item[0], item[1], item[2]))

        return info_items

              



        
        

