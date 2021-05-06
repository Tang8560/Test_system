import wx
import wx.lib.agw.aui as aui
#import wx.aui as aui

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(800, 600))

        #
        # set up the menu
        #
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        toggle_item = menu.Append(wx.ID_ANY, "toggle visibility of pane1")
        menuBar.Append(menu, "Window")
        self.Bind(wx.EVT_MENU, self.OnToggle, toggle_item)
        self.SetMenuBar(menuBar)
        
        #
        # set up the AUI
        #
        agwFlags = aui.AUI_MGR_SMOOTH_DOCKING|aui.AUI_MGR_ALLOW_FLOATING|aui.AUI_MGR_LIVE_RESIZE|aui.AUI_MGR_ALLOW_ACTIVE_PANE|aui.AUI_MGR_TRANSPARENT_DRAG|aui.AUI_MGR_WHIDBEY_DOCKING_GUIDES
        self._mgr = aui.AuiManager(self,agwFlags=agwFlags)
     
        #self._mgr.SetManagedWindow(self) #including this crashes the code.  Don't know why.
        
        self.TextCtrl1 = wx.TextCtrl(self)
        self.TextCtrl2 = wx.TextCtrl(self)
        self.TextCtrl3 = wx.TextCtrl(self)
        self.TextCtrl1.SetValue("stuff "*40)
        self.TextCtrl2.SetValue("stuff "*40)
        self.TextCtrl3.SetValue("stuff "*40)
      
        self.pi1 = aui.AuiPaneInfo().Name("pane1").Right().Dockable().Caption("pane1").CaptionVisible(True).BestSize((400,200)).DestroyOnClose(False)
        self.pi2 = aui.AuiPaneInfo().Name("pane2").Bottom().Dockable().Caption("pane2").CaptionVisible(True).BestSize((400,200)).DestroyOnClose(False)
        self.pi3 = aui.AuiPaneInfo().Name("pane3").Left().Dockable().Caption("pane3").CaptionVisible(True).BestSize((400,200)).DestroyOnClose(False)
        self.pi1.NotebookDockable()
        self.pi2.NotebookDockable()
        self.pi3.NotebookDockable()
      
        self._mgr.AddPane(self.TextCtrl1,self.pi1,self.pi1.name)
        self._mgr.AddPane(self.TextCtrl2,self.pi2,self.pi2.name)
        self._mgr.AddPane(self.TextCtrl3,self.pi3,self.pi3.name)
       
        self._mgr.Update()
  
    def OnToggle(self,evt): 
        p = self.pi1
        visible = p.IsShown()
        print "On Toggle visible = " ,visible
        p.Show(not visible)
        self._mgr.Update()
    
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'AUI test')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()

