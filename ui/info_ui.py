# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : info_ui.py
#--------------------------------------------------------------------------
# Build info
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import os
import wx
import sys
import glob
from pubsub import pub
from ObjectListView import ObjectListView, GroupListView, ColumnDefn

#==========================================================================
# IMPORTS INFO FUNCTION
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from event.info_func import info_event

#==========================================================================
# PUB Subscibe
#==========================================================================
project_menu = "project_menu"


#==========================================================================
# INFO LIST ITEM
#==========================================================================
class Item(object):
    def __init__(self, item, info, classname):
        """ List attribution """
        self.item = item
        self.info = info
        self.classname = classname

info_columns = [ "item", "info", "classname" ]
info_items = []
# info_items = [
#               Item("unknown", "unknown", "unknown"),
#               Item("unknown", "unknown", "unknown"),
#               Item("unknown", "unknown", "unknown"),
#              ]


#==========================================================================
# MAIN PROGRAM
#==========================================================================

class info_panel(wx.Panel):
    def __init__(self, parent):
        """ Info panel """
        super().__init__(parent, style=wx.SIMPLE_BORDER)
        self.info_items = info_items

        pub.subscribe(self.pub_project, project_menu)

        self.build_panel()

    def build_panel(self):


        info_sizer = wx.BoxSizer(wx.VERTICAL)

        ## Use for objectlistview
        # self.info_olv = ObjectListView(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        ## Use for grouplistview
        self.info_olv = GroupListView(self, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        ## Cancel the item background color
        self.info_olv.useAlternateBackColors = False

        self.setitem()

        # Allow the cell values to be edited when single-clicked
        # self.info_olv.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK

        info_sizer.Add(self.info_olv, 1, wx.EXPAND)
        self.SetSizer(info_sizer)
        self.Layout()
        info_sizer.Fit( self)

        self.Bind(wx.EVT_SIZE, self.onResize)
        self.info_olv.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemSelected)
        self.info_olv.Bind(wx.EVT_KILL_FOCUS, self.OnItemUnSelected)

    def setitem(self):
        """ Bind the item to the objectlistview """
        ss = self.GetSize()
        self.info_olv.useExpansionColumn = True
        self.info_olv.SetColumns([
                            ColumnDefn(info_columns[0], "left", ss[1]*0.7, info_columns[0]),
                            ColumnDefn(info_columns[1], "left", ss[1]*0.7, info_columns[1]),
                            ColumnDefn(info_columns[2], "left", ss[1]*0, info_columns[2])
                        ])

        ## Set the header of the grouplistview
        self.info_olv.SetSortColumn(self.info_olv.columns[3])
        self.info_olv.SetObjects(self.info_items)

    def onResize(self, event):
        self.setitem()
        self.Layout()
        self.Refresh()

    def OnItemSelected(self, event):
        self.info_olv.Select(event.Item.Id)
        row_id = event.GetIndex()
        col_id = event.GetColumn ()
        select_file = self.info_olv.GetItem(row_id, col_id).GetText()
        self.project_files = os.walk(self.project_path)

        for file in self.project_files:
            json_file = glob.glob(file[0] +'\*.json')
            if json_file:
                break
        for json in json_file:
            if select_file.lower() in json:
                os.system(json)
                break

    def OnItemUnSelected(self, event):
        pub.sendMessage(project_menu, project_path = self.project_path)

    def pub_project(self, project_path):
        self.project_path = project_path
        self.info_items= info_event(self.project_path).get_info_items()
        ## Transfer to item data format ##
        self.setitem()

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Info UI")
        self.panel = info_panel(self)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()