# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 09:21:18 2021

@author: 6065
"""


import wx
from ObjectListView import ObjectListView, ColumnDefn


class Item(object):
    def __init__(self, item, info):
        self.item = item
        self.info = info
       
    
class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.items = [Item("Serial Number", ""), Item("User Name", "")]

        self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.setBooks()

        # Allow the cell values to be edited when double-clicked
        self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_DOUBLECLICK
        
        # create an update button
        updateBtn = wx.Button(self, wx.ID_ANY, "Update OLV")
        updateBtn.Bind(wx.EVT_BUTTON, self.updateControl)

        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)        

        mainSizer.Add(self.dataOlv, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(updateBtn, 0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(mainSizer)
        
    #----------------------------------------------------------------------
    def updateControl(self, event):
        """
        
        """
        print ("updating...")
        product_dict = [{"item":"Core Python Programming", "info":"Wesley Chun"},
                        {"item":"Python Programming", "info":"Michael Dawson"} ]
        data = self.items + product_dict
        self.dataOlv.SetObjects(data)
        
    #----------------------------------------------------------------------
    def setBooks(self, data=None):
        self.dataOlv.SetColumns([
            ColumnDefn("Item", "left", 200, "item"),
            ColumnDefn("Info", "left", 200, "info")
        ])
        
        self.dataOlv.SetObjects(self.items)
        



########################################################################
class MainFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, 
                          title="ObjectListView Demo", size=(800,600))
        panel = MainPanel(self)
        
########################################################################
class GenApp(wx.App):
    
    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        
    #----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = MainFrame()
        frame.Show()
        return True
    
#----------------------------------------------------------------------
def main():
    """
    Run the demo
    """
    app = GenApp()
    app.MainLoop()

if __name__ == "__main__":
    main()