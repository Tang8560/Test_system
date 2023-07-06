# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta Reset
# File    : manual_tool.py
#--------------------------------------------------------------------------
# Manual Tool
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================

import wx
from func.instrument_manager  import get_instr


#==========================================================================
# PARAMETER
#==========================================================================
open_RL = True
close_RL = False


#==========================================================================
# MAIN PROGRAM
#==========================================================================

class manual_tool( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, None, -1, "Manual Tool")

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        self.instr = get_instr()
        self.OnInit()
        self.initial()
        self.event()

    def OnInit(self):
        bSizer1       = wx.BoxSizer( wx.VERTICAL )
        TRANSEC_Sizer = wx.StaticBoxSizer( wx.StaticBox( self, -1, u"TRANSEC" ), wx.HORIZONTAL )
        NET_Sizer     = wx.StaticBoxSizer( wx.StaticBox( self, -1, u"NET" ), wx.HORIZONTAL )
        STATUS_Sizer  = wx.StaticBoxSizer( wx.StaticBox( self, -1, u"STATUS" ), wx.HORIZONTAL )
        TX_Sizer      = wx.StaticBoxSizer( wx.StaticBox( self, -1, u"TX" ), wx.HORIZONTAL )
        RX_Sizer      = wx.StaticBoxSizer( wx.StaticBox( self, -1, u"RX" ), wx.HORIZONTAL )
        PWR_Sizer     = wx.StaticBoxSizer( wx.StaticBox( self, -1, u"PWR" ), wx.HORIZONTAL )
        btn_Sizer     = wx.BoxSizer( wx.HORIZONTAL )

        self.TRANSEC_R = wx.RadioButton( TRANSEC_Sizer.GetStaticBox(), -1, u"RED  ")
        self.TRANSEC_G = wx.RadioButton( TRANSEC_Sizer.GetStaticBox(), -1, u"GREEN")
        self.TRANSEC_C = wx.RadioButton( TRANSEC_Sizer.GetStaticBox(), -1, u"CLOSE")
        self.NET_R     = wx.RadioButton( NET_Sizer.GetStaticBox(), -1, u"RED  ")
        self.NET_G     = wx.RadioButton( NET_Sizer.GetStaticBox(), -1, u"GREEN")
        self.NET_C     = wx.RadioButton( NET_Sizer.GetStaticBox(), -1, u"CLOSE")
        self.STATUS_R  = wx.RadioButton( STATUS_Sizer.GetStaticBox(),-1, u"RED  ")
        self.STATUS_G  = wx.RadioButton( STATUS_Sizer.GetStaticBox(), -1, u"GREEN")
        self.STATUS_C  = wx.RadioButton( STATUS_Sizer.GetStaticBox(), -1, u"CLOSE")
        self.TX_R      = wx.RadioButton( TX_Sizer.GetStaticBox(), -1, u"RED  ")
        self.TX_G      = wx.RadioButton( TX_Sizer.GetStaticBox(), -1, u"GREEN")
        self.TX_C      = wx.RadioButton( TX_Sizer.GetStaticBox(), -1, u"CLOSE")
        self.RX_R      = wx.RadioButton( RX_Sizer.GetStaticBox(), -1, u"RED  ")
        self.RX_G      = wx.RadioButton( RX_Sizer.GetStaticBox(), -1, u"GREEN")
        self.RX_C      = wx.RadioButton( RX_Sizer.GetStaticBox(), -1, u"CLOSE")
        self.PWR_R     = wx.RadioButton( PWR_Sizer.GetStaticBox(), -1, u"RED  ")
        self.PWR_G     = wx.RadioButton( PWR_Sizer.GetStaticBox(), -1, u"GREEN")
        self.PWR_C     = wx.RadioButton( PWR_Sizer.GetStaticBox(), -1, u"CLOSE")
        self.ALL_R       = wx.Button( self, -1, u"ALL RED")
        self.ALL_G       = wx.Button( self, -1, u"ALL GREEN")
        self.RESET     = wx.Button( self, -1, u"RESET")

        TRANSEC_Sizer.Add( self.TRANSEC_R, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        TRANSEC_Sizer.Add( self.TRANSEC_G, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        TRANSEC_Sizer.Add( self.TRANSEC_C, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        NET_Sizer.Add( self.NET_R, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        NET_Sizer.Add( self.NET_G, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        NET_Sizer.Add( self.NET_C, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        STATUS_Sizer.Add( self.STATUS_R, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        STATUS_Sizer.Add( self.STATUS_G, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        STATUS_Sizer.Add( self.STATUS_C, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        TX_Sizer.Add( self.TX_R, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        TX_Sizer.Add( self.TX_G, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        TX_Sizer.Add( self.TX_C, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        RX_Sizer.Add( self.RX_R, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        RX_Sizer.Add( self.RX_G, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        RX_Sizer.Add( self.RX_C, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        PWR_Sizer.Add( self.PWR_R, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        PWR_Sizer.Add( self.PWR_G, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        PWR_Sizer.Add( self.PWR_C, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        btn_Sizer.Add( self.ALL_R, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        btn_Sizer.Add( self.ALL_G, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        btn_Sizer.Add( self.RESET, 1, wx.ALIGN_CENTER | wx.ALL, 5 )
        bSizer1.Add( TRANSEC_Sizer, 1, wx.EXPAND | wx.ALL, 15 )
        bSizer1.Add( NET_Sizer, 1, wx.EXPAND | wx.ALL, 15 )
        bSizer1.Add( STATUS_Sizer, 1, wx.EXPAND | wx.ALL, 15 )
        bSizer1.Add( TX_Sizer, 1, wx.EXPAND | wx.ALL, 15 )
        bSizer1.Add( RX_Sizer, 1, wx.EXPAND | wx.ALL, 15 )
        bSizer1.Add( PWR_Sizer, 1, wx.EXPAND | wx.ALL, 15 )
        bSizer1.Add( btn_Sizer, 1, wx.EXPAND | wx.ALL, 15 )

        self.SetSizer( bSizer1 )
        self.Fit()
        self.Layout()
        self.Centre( wx.BOTH )
        self.Show()

    def initial(self):
        self.TRANSEC_C.SetValue(True)
        self.NET_C.SetValue(True)
        self.STATUS_C.SetValue(True)
        self.TX_C.SetValue(True)
        self.RX_C.SetValue(True)
        self.PWR_C.SetValue(True)
        self.DAQ_transecR =  self.instr.DAQ_transecR(close_RL)
        self.DAQ_netR     =  self.instr.DAQ_netR(close_RL)
        self.DAQ_statusR  =  self.instr.DAQ_statusR(close_RL)
        self.DAQ_TXR      =  self.instr.DAQ_TXR(close_RL)
        self.DAQ_RXR      =  self.instr.DAQ_RXR(close_RL)
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(close_RL)
        self.DAQ_netG     =  self.instr.DAQ_netG(close_RL)
        self.DAQ_statusG  =  self.instr.DAQ_statusG(close_RL)
        self.DAQ_TXG      =  self.instr.DAQ_TXG(close_RL)
        self.DAQ_RXG      =  self.instr.DAQ_RXG(close_RL)
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(close_RL)


    def event(self):
        self.TRANSEC_R.Bind(wx.EVT_RADIOBUTTON, self.TRANSEC_R_event)
        self.TRANSEC_G.Bind(wx.EVT_RADIOBUTTON, self.TRANSEC_G_event)
        self.TRANSEC_C.Bind(wx.EVT_RADIOBUTTON, self.TRANSEC_C_event)
        self.NET_R.Bind(wx.EVT_RADIOBUTTON, self.NET_R_event)
        self.NET_G.Bind(wx.EVT_RADIOBUTTON, self.NET_G_event)
        self.NET_C.Bind(wx.EVT_RADIOBUTTON, self.NET_C_event)
        self.STATUS_R.Bind(wx.EVT_RADIOBUTTON, self.STATUS_R_event)
        self.STATUS_G.Bind(wx.EVT_RADIOBUTTON, self.STATUS_G_event)
        self.STATUS_C.Bind(wx.EVT_RADIOBUTTON, self.STATUS_C_event)
        self.TX_R.Bind(wx.EVT_RADIOBUTTON, self.TX_R_event)
        self.TX_G.Bind(wx.EVT_RADIOBUTTON, self.TX_G_event)
        self.TX_C.Bind(wx.EVT_RADIOBUTTON, self.TX_C_event)
        self.RX_R.Bind(wx.EVT_RADIOBUTTON, self.RX_R_event)
        self.RX_G.Bind(wx.EVT_RADIOBUTTON, self.RX_G_event)
        self.RX_C.Bind(wx.EVT_RADIOBUTTON, self.RX_C_event)
        self.PWR_R.Bind(wx.EVT_RADIOBUTTON, self.PWR_R_event)
        self.PWR_G.Bind(wx.EVT_RADIOBUTTON, self.PWR_G_event)
        self.PWR_C.Bind(wx.EVT_RADIOBUTTON, self.PWR_C_event)
        self.ALL_R.Bind(wx.EVT_BUTTON, self.ALL_R_event)
        self.ALL_G.Bind(wx.EVT_BUTTON, self.ALL_G_event)
        self.RESET.Bind(wx.EVT_BUTTON, self.RESET_event)

    def TRANSEC_R_event(self, event):
        self.DAQ_transecR =  self.instr.DAQ_transecR(close_RL)
        self.DAQ_transecG =  self.instr.DAQ_transecG(close_RL)
        self.DAQ_transecR =  self.instr.DAQ_transecR(open_RL)

    def TRANSEC_G_event(self, event):
        self.DAQ_transecR =  self.instr.DAQ_transecR(close_RL)
        self.DAQ_transecG =  self.instr.DAQ_transecG(close_RL)
        self.DAQ_transecG =  self.instr.DAQ_transecG(open_RL)

    def TRANSEC_C_event(self, event):
        self.DAQ_transecR =  self.instr.DAQ_transecR(close_RL)
        self.DAQ_transecG =  self.instr.DAQ_transecG(close_RL)

    def NET_R_event(self, event):
        self.DAQ_netR     =  self.instr.DAQ_netR(close_RL)
        self.DAQ_netG     =  self.instr.DAQ_netG(close_RL)
        self.DAQ_netR     =  self.instr.DAQ_netR(open_RL)

    def NET_G_event(self, event):
        self.DAQ_netR     =  self.instr.DAQ_netR(close_RL)
        self.DAQ_netG     =  self.instr.DAQ_netG(close_RL)
        self.DAQ_netG     =  self.instr.DAQ_netG(open_RL)

    def NET_C_event(self, event):
        self.DAQ_netR     =  self.instr.DAQ_netR(close_RL)
        self.DAQ_netG     =  self.instr.DAQ_netG(close_RL)

    def STATUS_R_event(self, event):
        self.DAQ_statusR  =  self.instr.DAQ_statusR(close_RL)
        self.DAQ_statusG  =  self.instr.DAQ_statusG(close_RL)
        self.DAQ_statusR  =  self.instr.DAQ_statusR(open_RL)

    def STATUS_G_event(self, event):
        self.DAQ_statusR  =  self.instr.DAQ_statusR(close_RL)
        self.DAQ_statusG  =  self.instr.DAQ_statusG(close_RL)
        self.DAQ_statusG  =  self.instr.DAQ_statusG(open_RL)

    def STATUS_C_event(self, event):
        self.DAQ_statusR  =  self.instr.DAQ_statusR(close_RL)
        self.DAQ_statusG  =  self.instr.DAQ_statusG(close_RL)

    def TX_R_event(self, event):
        self.DAQ_TXR      =  self.instr.DAQ_TXR(close_RL)
        self.DAQ_TXG      =  self.instr.DAQ_TXG(close_RL)
        self.DAQ_TXR      =  self.instr.DAQ_TXR(open_RL)

    def TX_G_event(self, event):
        self.DAQ_TXR      =  self.instr.DAQ_TXR(close_RL)
        self.DAQ_TXG      =  self.instr.DAQ_TXG(close_RL)
        self.DAQ_TXG      =  self.instr.DAQ_TXG(open_RL)

    def TX_C_event(self, event):
        self.DAQ_TXR      =  self.instr.DAQ_TXR(close_RL)
        self.DAQ_TXG      =  self.instr.DAQ_TXG(close_RL)

    def RX_R_event(self, event):
        self.DAQ_RXR      =  self.instr.DAQ_RXR(close_RL)
        self.DAQ_RXG      =  self.instr.DAQ_RXG(close_RL)
        self.DAQ_RXR      =  self.instr.DAQ_RXR(open_RL)

    def RX_G_event(self, event):
        self.DAQ_RXR      =  self.instr.DAQ_RXR(close_RL)
        self.DAQ_RXG      =  self.instr.DAQ_RXG(close_RL)
        self.DAQ_RXG      =  self.instr.DAQ_RXG(open_RL)

    def RX_C_event(self, event):
        self.DAQ_RXR      =  self.instr.DAQ_RXR(close_RL)
        self.DAQ_RXG      =  self.instr.DAQ_RXG(close_RL)

    def PWR_R_event(self, event):
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(close_RL)
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(close_RL)
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(open_RL)

    def PWR_G_event(self, event):
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(close_RL)
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(close_RL)
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(open_RL)

    def PWR_C_event(self, event):
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(close_RL)
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(close_RL)

    def ALL_R_event(self, event):
        self.TRANSEC_R.SetValue(True)
        self.NET_R.SetValue(True)
        self.STATUS_R.SetValue(True)
        self.TX_R.SetValue(True)
        self.RX_R.SetValue(True)
        self.PWR_R.SetValue(True)
        self.DAQ_transecG =  self.instr.DAQ_transecG(close_RL)
        self.DAQ_netG     =  self.instr.DAQ_netG(close_RL)
        self.DAQ_statusG  =  self.instr.DAQ_statusG(close_RL)
        self.DAQ_TXG      =  self.instr.DAQ_TXG(close_RL)
        self.DAQ_RXG      =  self.instr.DAQ_RXG(close_RL)
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(close_RL)
        self.DAQ_transecR =  self.instr.DAQ_transecR(open_RL)
        self.DAQ_netR     =  self.instr.DAQ_netR(open_RL)
        self.DAQ_statusR  =  self.instr.DAQ_statusR(open_RL)
        self.DAQ_TXR      =  self.instr.DAQ_TXR(open_RL)
        self.DAQ_RXR      =  self.instr.DAQ_RXR(open_RL)
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(open_RL)

    def ALL_G_event(self, event):
        self.TRANSEC_G.SetValue(True)
        self.NET_G.SetValue(True)
        self.STATUS_G.SetValue(True)
        self.TX_G.SetValue(True)
        self.RX_G.SetValue(True)
        self.PWR_G.SetValue(True)
        self.DAQ_transecR =  self.instr.DAQ_transecR(close_RL)
        self.DAQ_netR     =  self.instr.DAQ_netR(close_RL)
        self.DAQ_statusR  =  self.instr.DAQ_statusR(close_RL)
        self.DAQ_TXR      =  self.instr.DAQ_TXR(close_RL)
        self.DAQ_RXR      =  self.instr.DAQ_RXR(close_RL)
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(close_RL)
        self.DAQ_transecG =  self.instr.DAQ_transecG(open_RL)
        self.DAQ_netG     =  self.instr.DAQ_netG(open_RL)
        self.DAQ_statusG  =  self.instr.DAQ_statusG(open_RL)
        self.DAQ_TXG      =  self.instr.DAQ_TXG(open_RL)
        self.DAQ_RXG      =  self.instr.DAQ_RXG(open_RL)
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(open_RL)

    def RESET_event(self, event):
        self.TRANSEC_C.SetValue(True)
        self.NET_C.SetValue(True)
        self.STATUS_C.SetValue(True)
        self.TX_C.SetValue(True)
        self.RX_C.SetValue(True)
        self.PWR_C.SetValue(True)
        self.DAQ_transecR =  self.instr.DAQ_transecR(close_RL)
        self.DAQ_netR     =  self.instr.DAQ_netR(close_RL)
        self.DAQ_statusR  =  self.instr.DAQ_statusR(close_RL)
        self.DAQ_TXR      =  self.instr.DAQ_TXR(close_RL)
        self.DAQ_RXR      =  self.instr.DAQ_RXR(close_RL)
        self.DAQ_PWRR     =  self.instr.DAQ_PWRR(close_RL)
        self.DAQ_transecG =  self.instr.DAQ_transecG(close_RL)
        self.DAQ_netG     =  self.instr.DAQ_netG(close_RL)
        self.DAQ_statusG  =  self.instr.DAQ_statusG(close_RL)
        self.DAQ_TXG      =  self.instr.DAQ_TXG(close_RL)
        self.DAQ_RXG      =  self.instr.DAQ_RXG(close_RL)
        self.DAQ_PWRG     =  self.instr.DAQ_PWRG(close_RL)


if __name__ == "__main__":
    app = wx.App(False)
    frame = manual_tool(None)
    app.MainLoop()
