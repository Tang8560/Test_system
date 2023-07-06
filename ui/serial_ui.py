# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : serial_ui.py
#--------------------------------------------------------------------------
# Build serial monitor
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
# PUB SUBSCRIBE
#==========================================================================

serial_return = "serial_return"

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class serial_panel ( wx.Panel ):

    def __init__( self, parent ):
        """ Serial panel """
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        wx.Panel.__init__ ( self, parent, -1, pos = wx.DefaultPosition, size = (framew*0.142 ,-1) ,style = wx.TAB_TRAVERSAL )

        self.com_txt = wx.TextCtrl( self, -1, "Serial COM port return:\n", style = wx.TE_MULTILINE)
        self.font(self.com_txt, 12)
        serial_Sizer = wx.BoxSizer( wx.VERTICAL )
        serial_Sizer.Add( self.com_txt, 1, wx.EXPAND )

        self.SetSizer( serial_Sizer )
        self.Layout()

        pub.subscribe(self.pub_serial_return,serial_return)

    def font(self, parent, size):
        parent.SetFont( wx.Font( size, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False) )
        return parent

    def pub_serial_return(self, serial_read):
        self.com_txt.AppendText(serial_read)

