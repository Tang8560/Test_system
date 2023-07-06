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

from ObjectListView import ObjectListView, ColumnDefn

#==========================================================================
# INFO LIST ITEM
#==========================================================================

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

class Item(object):
    def __init__(self, item, info):
        """ List attribution """
        self.item = item
        self.info = info

info_columns = [ "item", "info" ]

info_items = [
              Item("Project", ""),
              Item("Serial number", ""),
              Item("User Name", ""),
              Item("Model", ""),
              Item("Model Rev", ""),
              Item("Dev", ""),
              Item("Temp", ""),
              Item("Test Type", ""),
              ]

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class info_panel(wx.Panel):
    def __init__(self, parent):
        """ Info panel """
        super().__init__(parent, style=wx.SIMPLE_BORDER)
        self.info_items = info_items
        info_sizer = wx.BoxSizer(wx.VERTICAL)

        self.info_olv = ObjectListView(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.info_olv.useAlternateBackColors = False

        self.setitem()

        # Allow the cell values to be edited when single-clicked
        self.info_olv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

        info_sizer.Add(self.info_olv, 1, wx.EXPAND)
        self.SetSizer(info_sizer)
        self.Layout()
        info_sizer.Fit( self)

        self.Bind(wx.EVT_SIZE, self.onResize)

    def setitem(self):
        """ Bind the item to the objectlistview """
        ss = self.GetSize()
        self.info_olv.SetColumns([
                            ColumnDefn(info_columns[0], "left", ss[1]*0.8, info_columns[0]),
                            ColumnDefn(info_columns[1], "left", ss[1]*0.8, info_columns[1])
                        ])
        self.info_olv.SetObjects(self.info_items)

    def onResize(self, event):
        self.setitem()
        self.Layout()
        self.Refresh()


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Info UI")
        self.panel = info_panel(self)
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()