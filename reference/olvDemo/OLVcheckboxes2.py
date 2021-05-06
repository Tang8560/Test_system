# OLVcheckboxes2.py

import wx
from ObjectListView import ObjectListView, ColumnDefn

########################################################################
class Results(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, tin, zip_code, plus4, name, address):
        """Constructor"""
        self.tin = tin
        self.zip_code = zip_code
        self.plus4 = plus4
        self.name = name
        self.address = address
    

########################################################################
class OLVCheckPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.test_data = [Results("123456789", "50158", "0065", "Patti Jones",
                                  "111 Centennial Drive"),
                          Results("978561236", "90056", "7890", "Brian Wilson",
                                  "555 Torque Maui"),
                          Results("456897852", "70014", "6545", "Mike Love", 
                                  "304 Cali Bvld")
                          ]
        self.resultsOlv = ObjectListView(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        
        self.setResults()
        
        checkBtn = wx.Button(self, label="Check")
        checkBtn.Bind(wx.EVT_BUTTON, self.onCheck)
        btnSizer.Add(checkBtn, 0, wx.ALL, 5)
        
        uncheckBtn = wx.Button(self, label="Uncheck")
        uncheckBtn.Bind(wx.EVT_BUTTON, self.onUncheck)
        btnSizer.Add(uncheckBtn, 0, wx.ALL, 5)
        
        mainSizer.Add(self.resultsOlv, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.CENTER|wx.ALL, 5)
        self.SetSizer(mainSizer)
        
    #----------------------------------------------------------------------
    def onCheck(self, event):
        """"""
        objects = self.resultsOlv.GetObjects()
        
        for obj in objects:
            self.resultsOlv.SetCheckState(obj, True)
        self.resultsOlv.RefreshObjects(objects)
        
    #----------------------------------------------------------------------
    def onUncheck(self, event):
        """"""
        objects = self.resultsOlv.GetObjects()
                
        for obj in objects:
            self.resultsOlv.SetCheckState(obj, False)
        self.resultsOlv.RefreshObjects(objects)        
        
    #----------------------------------------------------------------------
    def setResults(self):
        """"""
        self.resultsOlv.SetColumns([
            ColumnDefn("TIN", "left", 100, "tin"),
            ColumnDefn("Zip", "left", 75, "zip_code"),
            ColumnDefn("+4", "left", 50, "plus4"),
            ColumnDefn("Name", "left", 150, "name"),
            ColumnDefn("Address", "left", 200, "address")
            ])
        self.resultsOlv.CreateCheckStateColumn()
        self.resultsOlv.SetObjects(self.test_data)
        
    
########################################################################
class OLVCheckFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        title = "OLV Checkbox Tutorial"
        wx.Frame.__init__(self, parent=None, title=title, size=(1024, 768))
        panel = OLVCheckPanel(self)
        
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = OLVCheckFrame()
    frame.Show()
    app.MainLoop()