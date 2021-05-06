# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 10:29:36 2021

@author: 6065
"""


import wx
from wx.lib.mixins.listctrl import TextEditMixin

class EditableListCtrl(wx.ListCtrl, TextEditMixin):
    def __init__(self, *args, **kw):
        wx.ListCtrl.__init__(self, *args, **kw)
        TextEditMixin.__init__(self)


class MainFrame(wx.Frame):
    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(762, 347), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.main_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        panel_sizer = wx.BoxSizer(wx.VERTICAL)

        self.list_ctrl = EditableListCtrl(self.main_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     wx.LC_EDIT_LABELS | wx.LC_REPORT) # ---- Changed ------
        panel_sizer.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        self.main_panel.SetSizer(panel_sizer)
        self.main_panel.Layout()
        panel_sizer.Fit(self.main_panel)
        main_sizer.Add(self.main_panel, 1, wx.EXPAND, 5)

        self.SetSizer(main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.list_ctrl.InsertColumn(0, "Make")
        self.list_ctrl.InsertColumn(1, "Model")
        self.list_ctrl.InsertColumn(2, "Year")
        self.list_ctrl.InsertColumn(3, "Color")

        rows = [("Ford", "Taurus", "1996", "Blue"),
                ("Nissan", "370Z", "2010", "Green"),
                ("Porche", "911", "2009", "Red")
                ]
        index = 0
        for row in rows:
            self.list_ctrl.InsertStringItem(index, row[0])
            self.list_ctrl.SetStringItem(index, 1, row[1]) # ---- Changed ------
            self.list_ctrl.SetStringItem(index, 2, row[2]) # ---- Changed ------
            self.list_ctrl.SetStringItem(index, 3, row[3]) # ---- Changed ------
            index += 1
        self.list_ctrl.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnUpdate)




    def OnUpdate(self, event):
        self.list_ctrl.Select(event.Item.Id) # force the list to select the event item
        row_id = event.GetIndex() #Get the current row
        col_id = event.GetColumn () #Get the current column
        if col_id < 0: # ---- Changed ------
            col_id = 0 # ---- Changed ------
        new_data = event.GetText() #Get the changed data
        print (new_data)
        cols = self.list_ctrl.GetColumnCount() #Get the total number of columns
        rows = self.list_ctrl.GetItemCount() #Get the total number of rows


        #Get the changed item use the row_id and iterate over the columns
        print (" ".join([self.list_ctrl.GetItem(row_id, colu_id).GetText() for colu_id in range(cols)]))
        print ("Changed Item:", new_data, "Column:", col_id)

        #Get the entire listctrl iterate over the rows and the columns within each row
        print ("\nEntire listctrl BEFORE the update:")
        for row in range(rows):
            row_data = (" ".join([self.list_ctrl.GetItem(row, col).GetText() for col in range(cols)]))
            print (row_data)

        #Set the new data in the listctrl
        self.list_ctrl.SetStringItem(row_id,col_id,new_data)

        print ("\nEntire listctrl AFTER the update:")
        #Create a list that can be used to export data to a file
        data_for_export=[]
        for row in range(rows):
            row_data = (" ".join([self.list_ctrl.GetItem(row, col).GetText() for col in range(cols)]))
            print (row_data)
            data_for_export.append(row_data) #Add to the exportable data

        print ("\nData for export")
        for row in data_for_export: #Print the data
            print (row)

try:
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
except Exception:
    from traceback import format_exc
    print(format_exc())
    raw_input("")