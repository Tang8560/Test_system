# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : notebook_func.py
#--------------------------------------------------------------------------
# Create notebook event handle
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
# GRID COLOUR
#==========================================================================
EVEN_ROW_COLOUR = '#CCE6FF'
GRID_LINE_COLOUR = '#ccc'

#==========================================================================
# GET TABLE COLUMN
#==========================================================================
# 作為表格顯示欄位
cols = ["Test_Name", "L_LMT", "H_LMT", "Test_Value", "Test_Result", "Unit"]
# 作為勾選項目的欄位
group_col = ["Class"]
# 作為測試任務的欄位
task_col = ["Test_Name", "Script", "Function"]
# 作為錯誤碼的欄位
error_col = "Code"
# 作為判斷PASS/FAIL的欄位
compare_col = "Compare"

#==========================================================================
# TEST RESULT COLUMN
#==========================================================================
## The reason for adding 1 comes from the addition index column
result_column = cols.index("Test_Result") + 1

#==========================================================================
# INDEX COLUMN ORDERING
#==========================================================================
# 當True時，index欄位會根據勾選完的項目去重新排列編號順序
# 當False時, index欄位則會依照原先的編號順序
## if "True", the order will re-arrange by the select item
## if "False", the order will follow the origin setting
reorder_index = True

#==========================================================================
# CREATE DATA TABLE
#==========================================================================
class DataTable(wx.grid.GridTableBase):

    def __init__(self, data=None):
        wx.grid.GridTableBase.__init__(self)
        self.headerRows = 1
        if data is None:
            data = pd.DataFrame()
        self.data = data

    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data.columns) + 1

    def GetValue(self, row, col):
        if col == 0:
            return self.data.index[row]
        return self.data.iloc[row, col - 1]

    def SetValue(self, row, col, value):
        self.data.iloc[row, col - 1] = value

    def GetColLabelValue(self, col):
        if col == 0:
            if self.data.index.name is None:
                return 'Index'
            else:
                return self.data.index.name
        return str(self.data.columns[col - 1])

    def GetAttr(self, row, col, prop):
        attr = wx.grid.GridCellAttr()
        if row % 2 == 1:
            attr.SetBackgroundColour(EVEN_ROW_COLOUR)
        else: pass
        if col == result_column:
            if self.GetValue(row, col) == "pass":
                attr.SetBackgroundColour("green")
            elif self.GetValue(row, col) == "fail":
                attr.SetBackgroundColour("red")
        else: pass
        return attr

#==========================================================================
# TEST TABLE EVENT
#==========================================================================
class table_event(object):

    def __init__(self, project_path):
        self.project_files = os.walk(project_path)

        ## Get all json file ##
        for file in self.project_files:
            spec_file = glob.glob(file[0] +'\Specification*.csv')
            if spec_file:
                self.spec = pd.read_csv(spec_file[0])
                break
            else: continue

    ## [1] ##
    def get_spec_data(self):
        ## 從指定欄位取出資料 (只能取出指定範圍內的值) ##
        ## Get data from the specific column ##

        self.ALL_CHECK_DATA = self.spec
        self.spec_data = self.spec.loc[:,cols]
        spec_dataframe = pd.DataFrame(self.spec_data)
        spec_table = DataTable(spec_dataframe)

        func_data = self.get_task_function()
        return spec_table, func_data

    ## [2] ##
    def get_spec_group_data(self, rows):
        ## 根據勾選的"Class"欄位下的項目去取出在指定欄位下的所有資料，並且資料會依據Class在spec的順序以組的方式排列 (會打亂檔案下的排序) ##
        ## Based on the value under the "Class" column to get the data from the specific column,
        ## and the data will be arranged by the group of "Class" value and order by "Class" on the spec file ##
        group_all_data = pd.DataFrame()
        spec_data = self.spec.groupby(group_col)
        if rows:
            for row in rows:
                group_data = spec_data.get_group(row)
                group_all_data = pd.concat([group_all_data, group_data])

            self.ALL_CHECK_DATA = group_all_data
            group_all_data = group_all_data.loc[:,cols]
            spec_dataframe = pd.DataFrame(group_all_data)
            if reorder_index:
                spec_dataframe.reset_index(drop=True, inplace=True)  ## Remove index to let class "DataTable" to redefine.
        else:
            spec_dataframe = pd.DataFrame()
        spec_table = DataTable(spec_dataframe)

        func_data = self.get_task_function()
        return spec_table, func_data

    ## [3] ##
    def get_spec_nongroup_data(self, rows):
        ## 根據勾選的"Class"欄位下的值去取出在指定欄位下的所有資料，並且資料會依據Class的順序去排列 (不會打亂檔案下的排序) ##
        ## Based on the value under the "Class" column to get the data from the specific column,
        ## and the data will be arranged by the order of "Class" on the spec file ##

        ## <Method-1>
        ## 下面 file.Class的Class是檔案中的"Class"欄位
        # file = pd.read_csv(file_path)
        # select_item = ["A", "B", "C"]
        # spec_filter = file.Class.isin(select_item)  ## Class represent the label of the cloumn name
        # spec_table = file[spec_filter]
        spec_filter = self.spec.Class.isin(rows)
        spec_dataframe = self.spec[spec_filter]
        self.ALL_CHECK_DATA = spec_dataframe

        spec_dataframe = spec_dataframe.loc[:,cols]
        if reorder_index:
            spec_dataframe.reset_index(drop=True, inplace=True)
        spec_table = DataTable(spec_dataframe)

        ## <Method-2> ---利用*迭代會入參數
        ## 利用filter的方式，不過無法透過迭代的方式匯入判斷式，因此放棄
        # file = pd.read_csv(file_path)
        # select_item = ["A", "B", "C"]
        # data = []
        # for i in select_item:
        #     data.append(file["Class"] == i)
        # spec_table = file[np.logical_or(*data)]
        # 目標 fliter = np.logical_or(self.spec["Class"] == "A", self.spec["Class"] == "B")

        func_data = self.get_task_function()
        return spec_table, func_data

    ## [sub-function] ##
    def get_task_function(self):
        """
        func column:    Get "Test Name", "Script", "Fuction"
        code column:    Get "Error Code"
        compare column: Get "Compare"
        """
        func = self.ALL_CHECK_DATA.loc[:,task_col]
        code = self.ALL_CHECK_DATA.loc[:,error_col]
        compare = self.ALL_CHECK_DATA.loc[:,compare_col]

        data = [ func, code, compare ]

        return data
