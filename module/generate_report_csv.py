# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : generate_report_csv.py 
#--------------------------------------------------------------------------
# Generate CSV Report.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================


#==========================================================================
# IMPORTS
#==========================================================================
import wx
import wx.grid
import os
import sys
import csv
import glob
import pandas as pd
from datetime import datetime

from event.notebook_func import DataTable

#==========================================================================
# SAVE CSV PARAMETER
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

save_report = True
save_report_path  = root + r"\data"


#==========================================================================
# MAIN PROGRAM
#==========================================================================

class csv_report(object):
    """Create the kymeta test report"""
    
    def __init__(self,serial,model,modelrev,softrev,operator,result,label,data, report_path = save_report_path):
        
        self.save_report = save_report
        self.save_report_path  = report_path 
        items = ["CSV", "csv"]
        
        if self.save_report == True:
            if any(i in self.save_report_path for i in items):
                self.filepath = self.save_report_path
            else:
                self.filepath = self.save_report_path  +'\\'+model+'_'+serial+'_station1_'+self.DTG()[0]+'.csv'
            print("KYMETA path: ", self.filepath)
            
            try:
                with open(self.filepath,'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['DTG', self.DTG()[0]])
                    writer.writerow(['Serial Number', serial])
                    writer.writerow(['Part Number', model])
                    writer.writerow(['Rev', modelrev])
                    writer.writerow(['SW Rev', softrev ]) 
                    writer.writerow(['Test Operator', operator])           
                    writer.writerow(['Test Result', result]) 
                    writer.writerow([''])
                    writer.writerow(['[Test Log]'])
                    writer.writerow(label) 
                    for line in range(len(data)):
                        writer.writerow(data[line]) 
                    print('[INFO] Successfully generate CSV report.')   
            except Exception as e:
                print('[INFO] Generate CSV report have error happened.')
                self.traceback(e)
                
        else:
            print("[INFO] Not save CSV report. if you want to change, please modify setting panel.")
            
            
    def DTG(self):
        """ Compute the end of the test time """
        end = datetime.now()
        dt_string = end.strftime("%Y%m%d%H%M%S")
        end = end.strftime("%Y-%m-%d %H:%M:%S")
        return dt_string, end
    
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))
    


class open_csv(object):

    def __init__(self, file_path, grid_table):
        print(file_path)

        try:
            self.spec = pd.read_csv(file_path, header = 9, sep = ',', encoding='utf-8')
            # delimiter="\t" use to avoid "ParserError: Error tokenizing data. C error: Expected 1 fields in line 29, saw 2"
            spec_dataframe = pd.DataFrame(self.spec).iloc[:,1::]        
            spec_table = DataTable(spec_dataframe)
            grid_table.SetTable(spec_table, takeOwnership=True, selmode = wx.grid.Grid.SelectRows) 
            self.resize(grid_table)
        except Exception as e:
            self.traceback(e) 

    def resize(self, table):
        ss = table.GetParent().GetSize()
        if table.GetNumberCols() > 1:
            ## [Tab1] Grid Panel: when the sizer changed, the content will auto-tune to fit the sizer. ##
            for i in range(table.GetNumberCols()):
                if i == 0:
                    table.SetColSize( 0,ss[0]/(table.GetNumberCols()*2))
                else:
                    table.SetColSize( i,ss[0]/(table.GetNumberCols()-0.5))
        # If the column is only an index column, make the index column fill all the space.
        else: table.SetColSize( 0,ss[0])
        table.AutoSizeRows()
        table.selectrow = 0
        table.GetParent().Layout()
        table.GetParent().Refresh()

    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))