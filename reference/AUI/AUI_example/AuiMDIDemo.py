
import wx
import aui


class ParentFrame(aui.AuiMDIParentFrame):
    
    def __init__(self, parent):

        aui.AuiMDIParentFrame.__init__(self, parent, -1, title="AuiMDIParentFrame",
                                       size=(640, 480), style=wx.DEFAULT_FRAME_STYLE)
        self.count = 0
        mb = self.MakeMenuBar()
        self.SetMenuBar(mb)
        self.CreateStatusBar()


    def MakeMenuBar(self):

        mb = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "New child window\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.OnNewChild, item)
        item = menu.Append(-1, "Close parent")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        mb.Append(menu, "&File")
        return mb

        
    def OnNewChild(self, evt):

        self.count += 1
        child = ChildFrame(self, self.count)
        child.Show()

    def OnDoClose(self, evt):
        self.Close()
        

#----------------------------------------------------------------------

class ChildFrame(aui.AuiMDIChildFrame):

    def __init__(self, parent, count):

        aui.AuiMDIChildFrame.__init__(self, parent, -1, title="Child: %d" % count)
        mb = parent.MakeMenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "This is child %d's menu" % count)
        mb.Append(menu, "&Child")
        self.SetMenuBar(mb)
        
        p = wx.Panel(self)
        wx.StaticText(p, -1, "This is child %d" % count, (10, 10))
        p.SetBackgroundColour('light blue')

        sizer = wx.BoxSizer()
        sizer.Add(p, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        wx.CallAfter(self.Layout)

        from wx.lib.inspection import InspectionTool
        if not InspectionTool().initialized:
            InspectionTool().Init()

        # Find a widget to be selected in the tree.  Use either the
        # one under the cursor, if any, or this frame.
        wnd = wx.FindWindowAtPointer()
        if not wnd:
            wnd = self
        InspectionTool().Show(wnd, True)


def Main():

    app = wx.PySimpleApp()
    frame = ParentFrame(None)
    frame.CenterOnScreen()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    Main()
