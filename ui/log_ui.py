# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : log_ui.py 
#--------------------------------------------------------------------------
# Build log monitor
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================


#==========================================================================
# IMPORTS
#==========================================================================

import wx
import sys
from pubsub import pub

#==========================================================================
# REDIRCT COMMAND
#==========================================================================

class RedirectText(object):

    def __init__(self,aWxTextCtrl):
        """ Redirect command prompt to the log panel """
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)

#==========================================================================
# MAIN PROGRAM
#==========================================================================        
        
class log_panel ( wx.Panel ):
	
    def __init__( self, parent ):
        """ Log panel """
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, style = wx.TAB_TRAVERSAL )
        
        
        log_Sizer = wx.BoxSizer( wx.HORIZONTAL )                
        
        self.prompt_txt = wx.TextCtrl( self, -1, u"", style = wx.TE_MULTILINE)
        self.font(self.prompt_txt, 12 )

        log_Sizer.Add( self.prompt_txt, 1, wx.EXPAND )        
             
        self.SetSizer( log_Sizer )
        self.Layout()
        redir = RedirectText(self.prompt_txt)
        sys.stdout = redir
    
    
    def font(self, parent, size): 
        parent.SetFont( wx.Font( size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False) )
        return parent 
        

