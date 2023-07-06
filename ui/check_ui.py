# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : check_ui.py
#--------------------------------------------------------------------------
# Build check
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
import time
from pubsub import pub
from ObjectListView import ObjectListView, ColumnDefn, OLVEvent

#==========================================================================
# IMPORTS CHECK FUNCTION
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from event.check_func import check_event

#==========================================================================
# PUB Subscibe
#==========================================================================
project_menu = "project_menu"

#==========================================================================
# PUB Sendmessage
#==========================================================================
check_ui     = "check_ui"

#==========================================================================
# CHECK LIST ITEM
#==========================================================================
class Item(object):

    def __init__(self, item):
        """ Check item attribution """
        self.item = item

class_items = []

# class_items = [Item("unknown"),
#              Item("unknown"),
#              Item("unknown")
#             ]
#==========================================================================
# MAIN PROGRAM
#==========================================================================

class check_panel(wx.Panel):

    def __init__(self, parent):
        """ Check panel """
        wx.Panel.__init__(self, parent=parent, style=wx.SIMPLE_BORDER)

        pub.subscribe(self.pub_project, project_menu)


        self.build_panel()

    def build_panel(self):

        check_sizer = wx.BoxSizer(wx.VERTICAL)

        self.class_items = class_items
        self.background = wx.RED
        self.check_olv = ObjectListView(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_NO_HEADER)
        self.check_olv.useAlternateBackColors = False
        self.setitem()

        self.select = wx.CheckBox( self, -1, u"Select All")

        check_sizer.Add(self.check_olv, 1, wx.EXPAND)
        check_sizer.Add(self.select , 0, wx.LEFT|wx.ALL, 5)
        self.SetSizer(check_sizer)
        self.Layout()
        check_sizer.Fit( self)
        self.check_olv.Bind(OLVEvent.EVT_ITEM_CHECKED, self.onChecklist)
        self.select.Bind(wx.EVT_CHECKBOX, self.onCheck)
        self.Bind(wx.EVT_SIZE, self.onResize)

    def onCheck(self, event):
        """ Check all item (Select All) """

        select = event.GetEventObject()
        try:
            all_value = []
            if select.GetValue() == True:
                objects = self.check_olv.GetObjects()
                for obj in objects:
                    self.check_olv.SetCheckState(obj, True)
                    value = self.check_olv.GetStringValueAt(obj,1)
                    all_value.append(value)
            else:
                objects = self.check_olv.GetObjects()
                for obj in objects:
                    self.check_olv.SetCheckState(obj, False)

            self.check_olv.RefreshObjects(objects)
            pub.sendMessage("check_ui", check_item = all_value)
        except:
            pass

    def onChecklist(self, event):
        all_value = []
        objects = self.check_olv.GetObjects()
        for obj in objects:
            state = self.check_olv.GetCheckState(obj)
            # When the item is selected, then put the item string into the all_value
            if state:
                # GetStringValueAt(modelObject,columnIndex) --> 0 represent the checkbox; 1 represent the location of item
                value = self.check_olv.GetStringValueAt(obj,1)
                all_value.append(value)
        # print(all_value)
        pub.sendMessage("check_ui", check_item = all_value)

    def setitem(self):
        """ Bind the item to the objectlistview """
        ss = self.GetSize()
        self.check_olv.SetColumns([
            ColumnDefn("item", "left", ss[1]*1.5, "item")
            ])

        ## Add the checkbox ##
        self.check_olv.CreateCheckStateColumn()
        self.check_olv.SetObjects(self.class_items)

    def onResize(self, event):
        self.Layout()
        self.Refresh()

    def pub_project(self, project_path):
        self.class_items= check_event(project_path).get_class_items()
        self.setitem()
        self.select.SetValue(True)

        objects = self.check_olv.GetObjects()
        for obj in objects:
            self.check_olv.SetCheckState(obj, True)
        self.check_olv.RefreshObjects(objects)


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Check UI")
        self.panel = check_panel(self)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()