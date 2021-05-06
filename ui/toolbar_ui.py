# -*- coding: utf-8 -*-
#==========================================================================
# Project : Test System
# File    : menu_ui.py 
#--------------------------------------------------------------------------
# Create menubar 
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
import wx.lib.agw.aui as aui

#==========================================================================
# IMPORTS MENU FUNCTION
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from event.toolbar_func import toolbar_event

#==========================================================================
# SETTING TOOLBAR ICON SIZE
#==========================================================================
width  = 20
height = 20

#==========================================================================
# TEXTCTRL EVENT
#==========================================================================

class Placeholder(wx.TextCtrl):
    
    def __init__(self, parent, id, value):
        """ 當滑鼠按在TextCtrl上時將文字清空 """
        super().__init__(parent, id, value)
        self.default_text = value
        self.parent = parent
        self.OnKillFocus(None)
        self.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def OnFocus(self, event):
        self.SetForegroundColour(wx.BLACK)
        if self.GetValue() == self.default_text:
            self.SetValue("")
        event.Skip()

    def OnKillFocus(self, event):

        if self.GetValue().strip() == "":
            self.SetValue(self.default_text)
            self.SetForegroundColour(wx.LIGHT_GREY)
        if event:
            event.Skip()
            
#==========================================================================
# MAIN PROGRAM
#==========================================================================

class toolbar_panel(aui.AuiToolBar):
    def __init__(self, parent, src_path ):
        """ Toolbar panel """
        super().__init__(parent, -1, wx.DefaultPosition, wx.DefaultSize)   # agwStyle=aui.AUI_TB_TEXT  (show label)          
                                                                           # self.SetToolTextOrientation(1) (label orientation)
        self.parent = parent
        self.src_path = src_path
        self.toolbar_icon()
        self.toolbar_item()
        self.DoGetBestSize()
        
        self.event_handle()
        
    def path_trans(self, path):
        """Change source file path into the same type"""
        new_path = self.src_path + "\\" + path
        new_path = new_path.replace("/","\\")
        return new_path
              
    def toolbar_icon(self):
        """Get Icon"""
        self.project_image = wx.Image(self.path_trans('product.png')).Rescale(width, height)
        self.open_image    = wx.Image(self.path_trans('open.png')).Rescale(width, height)
        self.save_image    = wx.Image(self.path_trans('save.png')).Rescale(width, height)
        self.setting_image = wx.Image(self.path_trans('setting.png')).Rescale(width, height)
        self.run_image     = wx.Image(self.path_trans('run.png')).Rescale(width, height)
        self.abort_image   = wx.Image(self.path_trans('abort.png')).Rescale(width, height)
        self.manual_image  = wx.Image(self.path_trans('manual.png')).Rescale(width, height)
        self.serialnum = Placeholder(self,-1,"Serial Number") 
        self.dev = Placeholder(self,-1,"Dev")  
        self.testtype = wx.ComboBox( self, -1, value = "NormalPrd", choices = ["PreTest","NormalPrd","EngrTrial","Golden","RR","QC"], style = wx.CB_READONLY) 
        self.temperature = wx.ComboBox( self, -1, value = "Room", choices = ["Low","Room","High","BRoom","Packing"], style = wx.CB_READONLY) 
        
    def toolbar_item(self):
        """ Create Item """
        
        self.AddSimpleTool( 601, u"project", wx.Bitmap(self.project_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 602, u"open", wx.Bitmap(self.open_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 603, u"save", wx.Bitmap(self.save_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 604, u"setting", wx.Bitmap(self.setting_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 605, u"run", wx.Bitmap(self.run_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 606, u"abort", wx.Bitmap(self.abort_image, wx.BITMAP_TYPE_ANY) )
        self.AddSimpleTool( 607, u"manual", wx.Bitmap(self.manual_image, wx.BITMAP_TYPE_ANY) ) 
        self.AddSeparator()
        self.AddControl(self.serialnum)
        self.AddControl(self.dev)
        self.AddControl(self.testtype)
        self.AddControl(self.temperature)
        self.SetToolBitmapSize(wx.Size(128,128))
        self.Realize() 

    def event_handle(self): 
        """Add Event to "Toolbar" Item"""
        evt = toolbar_event(self.parent)  
        self.parent.Bind(wx.EVT_TOOL, evt.project_event, id = 601)
        self.parent.Bind(wx.EVT_TOOL, evt.open_event, id = 602)
        self.parent.Bind(wx.EVT_TOOL, evt.save_event, id = 603)
        self.parent.Bind(wx.EVT_TOOL, evt.setting_event, id = 604)
        self.parent.Bind(wx.EVT_TOOL, evt.run_continue_event, id = 605)
        self.parent.Bind(wx.EVT_TOOL, evt.run_abort_event, id = 606)
        self.parent.Bind(wx.EVT_TOOL, evt.manual_tool_event, id = 607)
      		
class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="Test Toolbar")
        self.panel = toolbar_panel(self, root + "\\source\\image\\")
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
