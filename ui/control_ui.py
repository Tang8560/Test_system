# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : control_ui.py 
#--------------------------------------------------------------------------
# Control panel (Start, Exit button)
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

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

#==========================================================================
# PUB SUBSCRIBE
#==========================================================================
user         = "username"
run_continue = "run_continue"
run_stopfail = "run_stopfail"
run_abort    = "run_abort"
bar_range    = "task_processbar_range"
bar_value    = "task_processbar"
subbar_range = "subtask_processbar_range"
subbar_value = "subtask_processbar"
send_result  = "send_result"

#==========================================================================
# BUTTON SIZE
#==========================================================================
width = 125
height = 45

#==========================================================================
# BUTTON EVENT
#==========================================================================

class Toggle(wx.BitmapButton):
     
    def __init__(self, parent, imgnon, imgon, imgoff, function):
        """ bitmap button """
        wx.BitmapButton.__init__(self, parent, -1)
        
        self.image_non = imgnon
        self.image_on = imgon
        self.image_off = imgoff
        self.function = function              
        self.state = None       
        

    def SetValue(self, state):
        self.state = state
        
        if state==True:
            self.SetBitmapLabel(self.image_on)
        elif state==False:
            self.SetBitmapLabel(self.image_off)
        else:
            self.SetBitmapLabel(self.image_non)

        self.Refresh()

    def GetValue(self):
        return self.state
    
#==========================================================================
# MAIN PROGRAM
#==========================================================================
        
class control_panel ( wx.Panel ):
	
    def __init__( self, parent, src_path ):
        wx.Panel.__init__ ( self, parent, -1, pos = wx.DefaultPosition, style = wx.TAB_TRAVERSAL )
        self.parent = parent
        self.src_path = src_path
        self.button_image()
        self.build_control()

        pub.subscribe(self.pub_user, user)        
        pub.subscribe(self.pub_run_continue, run_continue)
        pub.subscribe(self.pub_run_stopfail, run_stopfail)
        pub.subscribe(self.pub_run_stopfail, run_abort)
        pub.subscribe(self.pub_bar_range, bar_range)
        pub.subscribe(self.pub_bar_value, bar_value) 
        pub.subscribe(self.pub_subbar_range, subbar_range)
        pub.subscribe(self.pub_subbar_value, subbar_value)    
        pub.subscribe(self.pub_send_result, send_result)    

    def path_trans(self, path):
        """Change source file path into the same type"""
        new_path = self.src_path + "\\" + path
        new_path = new_path.replace("/","\\")
        return new_path

    def button_image(self):
        """Get Image"""
        start_image = wx.Image(self.path_trans('start.png')).Rescale(width, height)
        abort_image = wx.Image(self.path_trans('abort.png')).Rescale(width, height)
        pass_image  = wx.Image(self.path_trans('pass.png')).Rescale(width, height)
        fail_image  = wx.Image(self.path_trans('fail.png')).Rescale(width, height)
        blank_image = wx.Image(self.path_trans('blank.png')).Rescale(width, height)
        self.start  = wx.Bitmap(start_image , wx.BITMAP_TYPE_ANY)
        self.abort  = wx.Bitmap(abort_image , wx.BITMAP_TYPE_ANY)  
        self.pass_  = wx.Bitmap(pass_image , wx.BITMAP_TYPE_ANY)
        self.fail_  = wx.Bitmap(fail_image , wx.BITMAP_TYPE_ANY) 
        self.blank  = wx.Bitmap(blank_image , wx.BITMAP_TYPE_ANY)
       
   
    def build_control(self):

        self.alarm = wx.StaticText( self, -1, u"Alarm" ) 
        self.font(self.alarm, 12)
    
        self.alarm_txt = wx.TextCtrl( self, -1, wx.EmptyString)
        self.gauge1 = wx.Gauge( self, -1, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.gauge1.SetValue( 0 ) 
        self.gauge2 = wx.Gauge( self, -1, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.gauge2.SetValue( 0 ) 
        
        self.result  = Toggle(self, self.blank, self.fail_, self.pass_, self.result_event)
        self.result.SetBitmapLabel(self.result.image_non)         
        self.user_txt  = wx.TextCtrl( self, -1, "Username", style = wx.BORDER_NONE | wx.TE_READONLY | wx.TE_CENTRE)
        self.user_txt.SetBackgroundColour( "#d8dde1" )
        self.font(self.user_txt, 17)
        start_Sizer = wx.BoxSizer( wx.HORIZONTAL ) 
        
        monitor_Sizer = wx.BoxSizer( wx.VERTICAL )
        alarm_Sizer = wx.BoxSizer( wx.HORIZONTAL )        
        
        alarm_Sizer.Add( self.alarm, 0, wx.ALL|wx.ALIGN_CENTER, 5 )
        alarm_Sizer.Add( self.alarm_txt, 1, wx.ALL|wx.EXPAND, 5 )
        monitor_Sizer.Add( alarm_Sizer, 1, wx.EXPAND)
        monitor_Sizer.Add( self.gauge1, 1, wx.ALL^wx.TOP|wx.EXPAND, 5 )
        monitor_Sizer.Add( self.gauge2, 1, wx.ALL^wx.TOP|wx.EXPAND, 5 )
        
        btn_Sizer = wx.BoxSizer( wx.VERTICAL )
        btn_Sizer.Add( self.result, 0,  wx.ALL^wx.TOP|wx.EXPAND, 5) 
        btn_Sizer.Add( self.user_txt, 1,  wx.ALL|wx.EXPAND, 5)
        start_Sizer.Add( monitor_Sizer, 1, wx.EXPAND )
        start_Sizer.Add( btn_Sizer, 0, wx.EXPAND )
        
        self.SetSizer( start_Sizer )
        self.Layout()
        
    def font(self, parent, size): 
        parent.SetFont( wx.Font( size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Calibri" ) )
        return parent 

    def result_event(self, event):
        pass
    
    def pub_user(self, username):
        self.user_txt.SetValue(username)
    
    def pub_send_result(self, value):
        if value == "PASS":
            self.result.SetValue(False)
        else:
            self.result.SetValue(True)   

    def pub_run_continue(self, run):
        self.gauge1.SetValue(0)
        self.gauge2.SetValue(0)
    
    def pub_run_stopfail(self, run):
        self.gauge1.SetValue(0)
        self.gauge2.SetValue(0)

    def pub_bar_range(self, value):
        self.gauge1.SetRange(value)
              
    def pub_bar_value(self, value):
        self.gauge1.SetValue(value)
        
    def pub_subbar_range(self, value):
        self.gauge2.SetRange(value)
              
    def pub_subbar_value(self, value):
        self.gauge2.SetValue(value)

        
class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="Test Control")
        self.panel = control_panel(self, root + "\\source\\button\\")
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
        

        
