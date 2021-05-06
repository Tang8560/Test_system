# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : check_func.py
#--------------------------------------------------------------------------
# Select Test Function.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import os
import wx
import glob
import pandas as pd

#==========================================================================
# TABLE RANGE
#==========================================================================
cols = "Class"

#==========================================================================
# CHECK LIST ITEM
#==========================================================================
class Item(object):

    def __init__(self, item):
        """ Check item attribution """
        self.item = item
        
#==========================================================================
# MAIN PROGRAM
#==========================================================================

class check_event(object):
    
    def __init__(self, project_path):

        self.project_files = os.walk(project_path)    
        self.get_spec_data()
        
    def get_spec_data(self):
        ## Get all json file ##
        for file in self.project_files:        
            spec_file = glob.glob(file[0] +'\Specification*.csv')
            if spec_file:
                spec_data = pd.read_csv(spec_file[0])
                self.spec_data = spec_data[cols].drop_duplicates().tolist()
                # print(self.spec_data )
                break
            else: continue   
        return self.spec_data
                    
    def get_class_items(self):            
        ## Transfer to item data format ## 
        ## Create a list of objects ##
        """
        format:
        ----------------------------------------
        info_items = [
              Item("unknown"),
              Item("unknown"),
              Item("unknown"),
             ]
        """
        class_items = []
        for item in self.spec_data:
            class_items.append(Item(item))

        return class_items
