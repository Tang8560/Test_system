# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : toolbar_func.py 
#--------------------------------------------------------------------------
# Create toolbar event handle
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
from pubsub import pub

#==========================================================================
# IMPORTS UI PANEL
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from ui.about_ui import about_panel

#==========================================================================
# PUB SENDMESSAGE
#==========================================================================
project_menu = "project_menu"
open_menu    = "open_menu"
save_menu    = "save_menu"
setting_menu = "setting_menu"
manual_menu  = "manual_menu"
run_continue = "run_continue"
run_stopfail = "run_stopfail"
run_abort    = "run_abort"

#==========================================================================
# MAIN PROGRAM
#==========================================================================
class toolbar_event(object):
    
    def __init__(self, parent):
        self.parent = parent
        
        self.functional_data = None

    def project_event(self, event):
        """ Select the project """
        print("[INFO] Open the project")
        dirpath = wx.DirDialog(self.parent, u"Select project")
 
        if dirpath.ShowModal() == wx.ID_OK:
            self.project_path = dirpath.GetPath()
            print("[INFO] Select the project: " + os.path.basename(self.project_path))
            dirpath.Destroy()
            pub.sendMessage(project_menu, project_path = self.project_path)

    def open_event(self, event):
        """ Open test table data """
        print("[INFO] Open data file")
        filepath = wx.FileDialog(self.parent, u"Open file", wildcard="CSV files (*.csv)|*.csv",style = wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        
        if filepath.ShowModal() == wx.ID_OK:
            self.open_path = filepath.GetPath()
            print("[INFO] Open the file: " + os.path.basename(self.open_path))
            pub.sendMessage(open_menu, file_path = self.open_path)
            filepath.Destroy()
            
    def save_event(self, event):
        """ Save test table data """
        print("[INFO] Save Test Table")
        filepath = wx.FileDialog(self.parent, u"Save file",wildcard="CSV files (*.csv)|*.csv",style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_NO_FOLLOW)
        
        if filepath.ShowModal() == wx.ID_OK:
            self.save_path = filepath.GetPath()
            print("[INFO] Save the file: " + os.path.basename(self.save_path))
            pub.sendMessage(save_menu, file_path = self.save_path)
            filepath.Destroy()

    def quit_event(self, event):
        """ Menubar quit """
        print("[INFO] Exit the program")
        try:
            dlg = wx.MessageDialog(None,u"Are you sure you want to close the window?",u"Confirm close",wx.YES_NO)                         
            if dlg.ShowModal()==wx.ID_YES:              
                wx.CallAfter(self.parent.Destroy)
                event.Skip()
            
        except Exception as e:
            self.traceback(e)

    def setting_event(self, event):
        print("[INFO] Open the setting panel")
        pub.sendMessage(setting_menu, run = event)

    def run_continue_event(self, event):
        """ Run Continue """
        print("[INFO] Run test")
        pub.sendMessage(run_continue, run = event)
                
    def run_abort_event(self, event):
        """ Abort """
        print("[INFO] Abort the test")
        pub.sendMessage(run_abort, run = event)
      
    def manual_tool_event(self, event):
        print("[INFO] Open the manual tool")
        pub.sendMessage(manual_menu, run = event)

    def about_event(self, event):
        print("[INFO] Open the about tool") 
        about = about_panel(self.parent,"About")
        about.ShowModal()     

    def traceback(self, error):
        """ Error handling """
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,'line '+ str(traceback.tb_lineno))
   
        
        
        