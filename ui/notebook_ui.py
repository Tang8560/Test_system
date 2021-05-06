# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : notebook_ui.py 
#--------------------------------------------------------------------------
# Build notebook
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import os
import sys
import wx.aui
import wx.grid
import wx.html2
from pubsub import pub

#==========================================================================
# IMPORTS NOTEBOOK FUNCTION
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from event.notebook_func import table_event
from module.generate_browser_panel import Browser

#==========================================================================
# PUB SUBSCRIBE
#==========================================================================
project_menu    = "project_menu"
check_ui        = "check_ui"
run_continue    = "run_continue"
run_stopfail    = "run_stopfail"
run_abort       = "run_abort"
pass_fail       = "pass_to_grid"
get_result      = "get_result"
test_end        = "test_end"
#==========================================================================
# PUB SENDMESSAGE
#==========================================================================
send_result     = "send_result"

#==========================================================================
# DEFAULT GRID SIZE
#==========================================================================
numRows = 100
numCols = 7

#==========================================================================
# GET TABLE COLUMN
#==========================================================================
# 作為表格顯示欄位
cols             = ["Test_Name", "L_LMT", "H_LMT", "Test_Value", "Test_Result", "Unit"]
low_col         = "L_LMT"
high_col        = "H_LMT"
test_value_col  = "Test_Value"
test_result_col = "Test_Result"

# 作為錯誤碼的欄位
error_col = "Code"
# 作為判斷PASS/FAIL的欄位
compare_col = "Compare"

## Get the column index
test_value_idx = cols.index(test_value_col) + 1
low_idx =  cols.index(low_col) + 1
high_idx = cols.index(high_col) + 1          
test_result_idx = cols.index(test_result_col) + 1     

#==========================================================================
# DATA DISPLAY
#==========================================================================
# 如果"True"則會依據檔案中Class內的項目順序以組的方式呈現，而內容則由勾選的Class項目決定
# 如果"False"則會依據檔案中Class內的項目順序呈現，而內容則由勾選的Class項目決定
# if "True", the data will re-ordering by the group of "Class".
# if "False", the data will dispaly with the original order
group = False  


#==========================================================================
# MAIN PROGRAM
#==========================================================================
class notebook_panel ( wx.Panel ): 
	
    def __init__( self, parent ):
        """ Notebook panel """
        super().__init__(parent)
        
        self.check_item = None
        self.table = None
        self.selectrow = 0
        self.error_code = []
        
        pub.subscribe(self.pub_project, project_menu)
        pub.subscribe(self.pub_check, check_ui)
        pub.subscribe(self.pub_pass_fail, pass_fail)
        pub.subscribe(self.pub_get_result, get_result)
        pub.subscribe(self.pub_test_end, test_end)
        
        self.build_panel()
    
    def build_panel(self):
        
        Notebook_Sizer = wx.BoxSizer( wx.VERTICAL )
        
        self.tabctrl = wx.aui.AuiNotebook( self, -1, style = wx.aui.AUI_NB_TAB_FIXED_WIDTH )
        
        # ====================================================================        
        ## [ Create Tab1 Grid Panel ] ##
        # ====================================================================
        self.grid_panel = wx.Panel( self.tabctrl,  -1)       
        self.grid_sizer = wx.BoxSizer( wx.VERTICAL )
           
        self.test_grid = wx.grid.Grid(self.grid_panel, -1, style = wx.VSCROLL )
        self.test_grid.CreateGrid(numRows, numCols, selmode=wx.grid.Grid.GridSelectRows)
        self.test_grid.HideRowLabels() 
        self.test_grid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE ) 
        self.test_grid.AutoSizeColLabelSize(0)
        self.test_grid.AutoSizeColumns()
        self.test_grid.AutoSizeRows()
        self.test_grid.DisableDragRowSize()
        self.grid_sizer.Add( self.test_grid, 1, wx.ALL|wx.EXPAND, 5 )
                   
        self.grid_panel.SetSizer( self.grid_sizer )
        self.grid_panel.Layout()
        self.grid_sizer.Fit( self.grid_panel )   
        self.tabctrl.AddPage( self.grid_panel, u"Test Table", True )
      
        # ====================================================================
        ## [ Create Tab2 Web Panel ] ##
        # ====================================================================
        self.display_panel = wx.Panel( self.tabctrl,  -1)       
        self.display_sizer = wx.BoxSizer( wx.VERTICAL )
        self.display_sizer.Add( Browser(self.display_panel,-1,title="browser"), 1, wx.ALL|wx.EXPAND, 5 )
                   
        self.display_panel.SetSizer( self.display_sizer )
        self.display_panel.Layout()
        self.display_sizer.Fit( self.display_panel )   
        self.tabctrl.AddPage( self.display_panel, u"Display", False )
        
        # ====================================================================
        ## [ Create Tab3 plg-in Panel ] ##
        # ====================================================================
        # ... load plug-in page
              
        Notebook_Sizer.Add( self.tabctrl, 1, wx.EXPAND |wx.ALL, 5 )
        self.Bind(wx.EVT_SIZE, self.onResize)       
        self.SetSizer( Notebook_Sizer )
        self.Layout()
        
    def onResize(self, event):
        self.resize()

    def pub_project(self, project_path):
        """ Based on the selected project to set the test table """
        self.project_path = project_path
        
        self.table = table_event(project_path).get_spec_data() 
        self.test_grid.SetTable(self.table[0], takeOwnership=True, selmode = wx.grid.Grid.SelectRows)  
        self.resize()
        
    def pub_check(self, check_item):
        """ Based on the selected item to set the test table """
        self.check_item = check_item              
        self.set_table()
            
    def set_table(self):
        if group:
            self.table = table_event(self.project_path).get_spec_group_data(self.check_item) 
        else:
            self.table = table_event(self.project_path).get_spec_nongroup_data(self.check_item)
        self.test_grid.SetTable(self.table[0], takeOwnership=True, selmode = wx.grid.Grid.SelectRows)  
        self.resize() 
        self.error_code = []         
        return self.table
            
    def pub_pass_fail(self, test_value):
        try:
            self.test_grid.MakeCellVisible(self.selectrow + 3, 5)
            self.test_grid.SetCellValue(self.selectrow, test_value_idx, test_value)
            compare = self.table[1][2].values
            
            set_pass = [self.selectrow, test_result_idx, 'pass']
            set_fail = [self.selectrow, test_result_idx, 'fail']
            get_high = [self.selectrow,high_idx]
            get_low  = [self.selectrow,low_idx]

            if compare[self.selectrow] == "NO":
                self.test_grid.SetCellValue(*set_pass)                                        
            elif compare[self.selectrow] == "NZ":
                try:
                    if float(test_value) != 0:
                        self.test_grid.SetCellValue(*set_pass)
                    else:
                        self.test_grid.SetCellValue(*set_fail) 
                        self.error_code.append(self.table[1][1].values[self.selectrow])
                except:
                    if test_value != "0" and "Error" not in test_value:
                        self.test_grid.SetCellValue(*set_pass)                                      
                    else:
                        self.test_grid.SetCellValue(*set_fail)
                        self.error_code.append(self.table[1][1].values[self.selectrow])                                   
            else:
                if test_value == self.test_grid.GetCellValue(*get_high):
                    self.test_grid.SetCellValue(*set_pass)          
                else:
                    try:
                        if float(test_value) <= float(self.test_grid.GetCellValue(*get_high)) and float(test_value) >= float(self.test_grid.GetCellValue(*get_low)):
                            self.test_grid.SetCellValue(*set_pass)
                        else:
                            self.test_grid.SetCellValue(*set_fail)
                            self.error_code.append(self.table[1][1].values[self.selectrow])
                    except:  
                        self.test_grid.SetCellValue(*set_fail)
                        self.error_code.append(self.table[1][1].values[self.selectrow])
                       
            self.test_grid.SelectRow(self.selectrow)            
            self.selectrow += 1 

        except Exception as e:
            print('test item pass/fail judgement has something error happens!\n')
            self.traceback(e)

    def pub_test_end(self, date, start, end):
        test_result = lambda m, n: m if self.error_code == [] else n
        self.result = test_result("PASS", "FAIL")
        pub.sendMessage(send_result, value = self.result)
        
    def pub_get_result(self):
        if self.error_code == []:
            self.pub_pass_fail("PASS")
        else:
            self.pub_pass_fail("FAIL")


    def resize(self):
        ss = self.GetSize()
        if self.test_grid.GetNumberCols() > 1:
            ## [Tab1] Grid Panel: when the sizer changed, the content will auto-tune to fit the sizer. ##
            for i in range(self.test_grid.GetNumberCols()):
                if i == 0:
                    self.test_grid.SetColSize( 0,ss[0]/(self.test_grid.GetNumberCols()*2))
                else:
                    self.test_grid.SetColSize( i,ss[0]/(self.test_grid.GetNumberCols()-0.5))
        # If the column is only an index column, make the index column fill all the space.
        else: self.test_grid.SetColSize( 0,ss[0])
        self.test_grid.AutoSizeRows()
        self.test_grid.selectrow = 0
        self.Layout()
        self.Refresh()
        
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))
                

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Test Notebook")
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        self.panel = notebook_panel(self)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
    