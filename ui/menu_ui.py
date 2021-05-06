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

#==========================================================================
# IMPORTS MENU FUNCTION
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from event.menu_func import menu_event

#==========================================================================
# SETTING MENU ICON SIZE
#==========================================================================
width  = 15
height = 15

#==========================================================================
# MAIN PROGRAM
#==========================================================================
class menu_panel( object ):     
    def __init__( self, parent, src_path ):  
        """Create Menu"""
        self.parent = parent
        self.src_path = src_path
        self.parent.menubar = wx.MenuBar()
        self.menu_build()
        self.menu_icon()
        self.menu_item()
        self.menu_item_icon()
        self.file_menu()
        self.edit_menu()
        self.run_menu()
        self.tool_menu()
        self.help_menu()
        self.parent.SetMenuBar( self.parent.menubar )
        
        self.event_handle()
        
    def path_trans(self, path):
        """Change source file path into the same type"""
        new_path = self.src_path + "\\" + path
        new_path = new_path.replace("/","\\")
        return new_path
    
    def menu_build(self):
        """Create Menubar Item"""
        self.file = wx.Menu()
        self.edit = wx.Menu()
        self.run  = wx.Menu()
        self.tool = wx.Menu()
        self.help = wx.Menu()
           
    def menu_icon(self):
        """Get Icon"""
        self.project_image = wx.Image(self.path_trans('product.png')).Rescale(width, height)
        self.open_image    = wx.Image(self.path_trans('open.png')).Rescale(width, height)
        self.save_image    = wx.Image(self.path_trans('save.png')).Rescale(width, height)
        self.quit_image    = wx.Image(self.path_trans('quit.png')).Rescale(width, height)
        self.setting_image = wx.Image(self.path_trans('setting.png')).Rescale(width, height)
        self.run_image     = wx.Image(self.path_trans('run.png')).Rescale(width, height)
        self.stop_image    = wx.Image(self.path_trans('stop.png')).Rescale(width, height)
        self.abort_image   = wx.Image(self.path_trans('abort.png')).Rescale(width, height)
        self.manual_image  = wx.Image(self.path_trans('manual.png')).Rescale(width, height)
        
    def menu_item(self):
        """
        Create Item
        ------------------------------------------
        'MenuItem' object has no attribute 'Bind', thus we must use id to bind the menu event.
        """
        self.project = wx.MenuItem( self.file, 100, "&Project\tCtrl+P", kind = wx.ITEM_NORMAL )
        self.open    = wx.MenuItem( self.file, 101, "&Open\tCtrl+O"   , kind = wx.ITEM_NORMAL )
        self.save    = wx.MenuItem( self.file, 102, "&Save\tCtrl+S"   , kind = wx.ITEM_NORMAL )
        self.quit    = wx.MenuItem( self.file, 103, "&Quit\tCtrl+Q"   , kind = wx.ITEM_NORMAL )
        self.flow    = wx.MenuItem( self.edit, 201, "&Flow\tCtrl+F"   , kind = wx.ITEM_NORMAL )
        self.setting = wx.MenuItem( self.edit, 202, "&Setting\tCtrl+Shift+S", kind = wx.ITEM_NORMAL )
        self.run_continue = wx.MenuItem( self.run, 301, "&Run\tF5"      , kind = wx.ITEM_NORMAL )
        self.run_stopfail = wx.MenuItem( self.run, 302, "&Run fail-stop\tF6", kind = wx.ITEM_NORMAL )
        self.run_abort    = wx.MenuItem( self.run, 303, "&Abort\tCtrl+C", kind = wx.ITEM_NORMAL )
        self.manual_tool  = wx.MenuItem( self.tool, 401, "&Manual"      , kind = wx.ITEM_NORMAL ) 
        self.about        = wx.MenuItem( self.help, 501, "&About\tF1"   , kind = wx.ITEM_NORMAL ) 
        
    def menu_item_icon(self):
        """Add Icon to Menu Item"""
        self.project.SetBitmap(wx.Bitmap(self.project_image))
        self.open.SetBitmap(wx.Bitmap(self.open_image)) 
        self.save.SetBitmap(wx.Bitmap(self.save_image)) 
        self.quit.SetBitmap(wx.Bitmap(self.quit_image)) 
        self.setting.SetBitmap(wx.Bitmap(self.setting_image)) 
        self.run_continue.SetBitmap(wx.Bitmap(self.run_image))
        self.run_stopfail.SetBitmap(wx.Bitmap(self.stop_image))
        self.run_abort.SetBitmap(wx.Bitmap(self.abort_image))
        self.manual_tool.SetBitmap(wx.Bitmap(self.manual_image))
        self.about.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_MENU,(width,height))) 
        
    def file_menu(self):  
        """File Menu Layout""" 
        self.file.Append( self.project ) 
        self.file.AppendSeparator()        
        self.file.Append( self.open )         
        self.file.Append( self.save )
        self.file.Append( self.quit )        
        self.parent.menubar.Append( self.file, u" File " ) 
        
    def edit_menu(self):  
        """Edit Menu Layout"""
        self.edit.Append( self.flow )
        self.edit.Append( self.setting )
        self.parent.menubar.Append( self.edit, u" Edit " )     
        
    def run_menu(self):  
        """Run Menu Layout"""
        self.run.Append( self.run_continue )
        self.run.Append( self.run_stopfail )
        self.run.Append( self.run_abort )
        self.parent.menubar.Append( self.run, u" Run " ) 
        
    def tool_menu(self):  
        """Tool Menu Layout"""
        self.tool.Append( self.manual_tool )
        self.parent.menubar.Append( self.tool, u" Tool " ) 
        
    def help_menu(self):  
        """Help Menu Layout"""
        self.help.Append( self.about )
        self.parent.menubar.Append( self.help, u" Help " )
        
    def event_handle(self): 
        """Add Event to Menu Item"""
        evt = menu_event(self.parent)               
        self.parent.Bind(wx.EVT_MENU, evt.project_event, id = 100)
        self.parent.Bind(wx.EVT_MENU, evt.open_event, id = 101)
        self.parent.Bind(wx.EVT_MENU, evt.save_event, id = 102)
        self.parent.Bind(wx.EVT_MENU, evt.quit_event, id = 103)
        self.parent.Bind(wx.EVT_MENU, evt.flow_event, id = 201)
        self.parent.Bind(wx.EVT_MENU, evt.setting_event, id = 202)
        self.parent.Bind(wx.EVT_MENU, evt.run_continue_event, id = 301)
        self.parent.Bind(wx.EVT_MENU, evt.run_stopfail_event, id = 302)
        self.parent.Bind(wx.EVT_MENU, evt.run_abort_event, id = 303)
        self.parent.Bind(wx.EVT_MENU, evt.manual_tool_event, id = 401)
        self.parent.Bind(wx.EVT_MENU, evt.about_event, id = 501)


class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="Test Menu")
        self.panel = menu_panel(self, root + "\\source\\image\\")
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
