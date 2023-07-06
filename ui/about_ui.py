# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 11:04:22 2021

@author: 6065
"""


import wx
import wx.richtext
import wx.lib.agw.hyperlink as hl

class about_panel(wx.Dialog):
    """Generate the dialog to enter the product serial number and part number"""
    def __init__(self, parent, title):
        """Main dialog"""
        super().__init__(parent, title = title, size = (500,500))
        Sizer1 = wx.BoxSizer( wx.VERTICAL )
        msg1 = 'Automated Testing System\n\n'
        msg2 = ['Version: 1.0.0 (user setup)\n',
                'Last Update Date: 2021-05-01\n'
                'OS: Windows_NT x64\n'
                'Python 3.7.6 64-bit | Wxpython 4.1.0\n\n',
                'How to use:\n',
                '1. Install Python Package:\n',
                '\tOnline Download:\n',
                '\t\tpip install wxpython\n',
                '\t\tpip install pubsub\n',
                ]
        m=''
        for i in msg2:
            m+=i

        self.info = wx.StaticText( self, wx.ID_ANY, msg1+m, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.info.SetFont( wx.Font( 10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Semibold" ) )
        self.lnk =  hl.HyperLinkCtrl(self, -1, "MTI website", URL="https://www.mtigroup.com/index_c.php")
        Sizer1.Add( self.info, 0, wx.ALL, 20 )
        Sizer1.Add( self.lnk, 0, wx.ALL, 20 )
        self.SetSizer( Sizer1 )
        self.Layout()
        self.Centre( wx.BOTH )

    def OnNext(self, event):
        self.Close()


class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="Test About")
        self.panel = about_panel(self, "About")
        self.panel.ShowModal()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
