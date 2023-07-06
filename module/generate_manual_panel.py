# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : manual_ui.py
#--------------------------------------------------------------------------
# Instrument Control Panel
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================

import os
import wx
import wx.grid
import time
import inspect
import ctypes
import threading
from func.path_manager        import get_image
from func.test_daq            import daq_instr
from func.test_visa           import visa_instr
from func.instrument_manager  import get_instr

#==========================================================================
# BUTTON EVENT
#==========================================================================

class Toggle(wx.BitmapButton):

    def __init__(self, parent, function):
        """ 自定義按鈕 """
        wx.BitmapButton.__init__(self, parent, -1, size = (70,35))

        self.function = function

        openbtn  = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_image.openbtn_image(get_image)
        closebtn = "\\".join(os.path.abspath(__file__).split('\\')[:-2]) + get_image.closebtn_image(get_image)

        self.openbtn = wx.Bitmap(openbtn , wx.BITMAP_TYPE_ANY)
        self.closebtn = wx.Bitmap(closebtn , wx.BITMAP_TYPE_ANY)

        self.openbtn_img  = self.openbtn.ConvertToImage().Scale(70,35, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.closebtn_img = self.closebtn.ConvertToImage().Scale(70,35, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()

        self.state = False
        self.SetBitmapLabel(self.closebtn_img)

        self.Bind(wx.EVT_BUTTON,self.OnClick)

    def OnClick(self, event):
        """ 執行Toggle button的反轉動作 """
        # state = event.GetEventObject().GetBitmapFocus()

        if self.state==True:
            self.function(self.state)
            self.state = False
            self.SetBitmapLabel(self.closebtn_img)
        else:
            self.function(self.state)
            self.state = True
            self.SetBitmapLabel(self.openbtn_img)

        # print('Output =', self.Output())
        self.Refresh()

#==========================================================================
# TEXTCTRL EVENT
#==========================================================================

class Placeholder(wx.TextCtrl):

    def __init__(self, *args, **kwargs):
        """ 當滑鼠按在TextCtrl上時將文字清空 """
        self.default_text = kwargs.pop("placeholder", "")
        wx.TextCtrl.__init__(self, *args, **kwargs)
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

class manual_dialog ( wx.Dialog ):

    def __init__( self, parent ):
        """ 操作面板 """
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        wx.Dialog.__init__ ( self, parent, -1, u"Manual", size = (framew/1.6 ,frameh/1.6), style = wx.DEFAULT_DIALOG_STYLE|wx.TAB_TRAVERSAL )

        self.close_manual = False
        print("[INFO] Open manual panel")
        self.OnInit()

    def OnInit(self):
        self.manual_Sizer = wx.BoxSizer( wx.VERTICAL )
        self.manual_notebook = wx.Notebook( self, -1, style = wx.NB_FIXEDWIDTH )

        self.close_btn = wx.Button( self,-1, u"Close")

        ###############################################
        self.GPIB_panel()
        self.DAQ_panel()
        self.ETHERNET_panel()
        self.I2C_panel()
        ###############################################

        self.manual_Sizer.Add( self.manual_notebook, 1, wx.ALL|wx.EXPAND, 5 )
        self.manual_Sizer.Add( self.close_btn, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        self.close_btn.Bind(wx.EVT_BUTTON, self.On_Close)

        self.SetSizer( self.manual_Sizer )
        self.Layout()
        self.Show()

    ###########################################################################
    def GPIB_panel(self):

        self.gpib_panel = wx.Panel( self.manual_notebook, -1 )
        self.gpib = wx.StaticText( self.gpib_panel,-1, u"GPIB CONTROL" )
        self.gpib.SetFont( wx.Font( 15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ) )

        gpib_Sizer = wx.BoxSizer( wx.VERTICAL )
        gpib_Sizer.Add( self.gpib, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        gpib_Sizer1 = wx.BoxSizer( wx.HORIZONTAL)

        ## [ CONTROL PANEL ] ##
        gpib_control_bSizer = wx.StaticBoxSizer( wx.StaticBox( self.gpib_panel,-1, u"CONTROL" ), wx.VERTICAL )

        ## 滾動式panel ##
        self.gpib_control_scrolled = wx.ScrolledWindow( gpib_control_bSizer.GetStaticBox(),-1, style = wx.HSCROLL|wx.VSCROLL )
        self.gpib_control_scrolled.SetScrollRate(5, 5)
        self.gpib_control_scrolled.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        self.gpib_instr1     = wx.StaticText( self.gpib_control_scrolled,-1, u"ACU power supply" )
        self.gpib_instr2     = wx.StaticText( self.gpib_control_scrolled,-1, u"BUC power supply" )
        self.gpib_instrtxt1  = wx.TextCtrl( self.gpib_control_scrolled,-1, wx.EmptyString, style = wx.TE_CENTER )
        self.gpib_instrtxt2  = wx.TextCtrl( self.gpib_control_scrolled,-1, wx.EmptyString, style = wx.TE_CENTER )
        self.gpib_instrbtn1  = Toggle( self.gpib_control_scrolled, self.GPIB_ACU_switch )
        self.gpib_instrbtn2  = Toggle( self.gpib_control_scrolled, self.GPIB_BUC_switch )
        self.gpib_line1 = wx.StaticLine( self.gpib_control_scrolled, -1, style = wx.LI_HORIZONTAL )
        self.gpib_line2 = wx.StaticLine( self.gpib_control_scrolled, -1, style = wx.LI_HORIZONTAL )

        self.gpib_instrtxt1.SetFont( wx.Font( 15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ))
        self.gpib_instrtxt2.SetFont( wx.Font( 15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ))

        gpib_fgSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
        gpib_fgSizer.AddGrowableCol( 0 )
        gpib_fgSizer.AddGrowableCol( 1 )
        gpib_fgSizer.SetFlexibleDirection( wx.BOTH )
        gpib_fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        gpib_fgSizer.Add( self.gpib_instr1, 0, wx.ALIGN_CENTER|wx.ALL, 1 )
        gpib_fgSizer.Add( self.gpib_instr2, 0, wx.ALIGN_CENTER|wx.ALL, 1 )
        gpib_fgSizer.Add( self.gpib_instrtxt1, 1, wx.EXPAND|wx.ALL, 5 )
        gpib_fgSizer.Add( self.gpib_instrtxt2, 1, wx.EXPAND|wx.ALL, 5 )
        gpib_fgSizer.Add( self.gpib_instrbtn1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_fgSizer.Add( self.gpib_instrbtn2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_fgSizer.Add( self.gpib_line1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_fgSizer.Add( self.gpib_line2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        ## Grid1 ##
        self.grid1 = wx.StaticText( self.gpib_control_scrolled,-1, u"ACU", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.gpib_grid1 = wx.grid.Grid( self.gpib_control_scrolled,-1, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.gpib_grid1.CreateGrid( 3, 2 )
        self.gpib_grid1.HideRowLabels()
        self.gpib_grid1.HideColLabels()
        self.gpib_grid1.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.gpib_grid1.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )

        gpib_gSizer1 = wx.BoxSizer( wx.VERTICAL )
        gpib_gSizer1.Add( self.grid1, 0,  wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_gSizer1.Add( self.gpib_grid1, 0,  wx.ALIGN_CENTER|wx.ALL, 5 )

        self.gpib_grid1.SetCellValue(0, 0, "Address")
        self.gpib_grid1.SetCellValue(1, 0, "V-set (V)")
        self.gpib_grid1.SetCellValue(2, 0, "I-set (A)")

        self.gpib_grid1.SetCellValue(0, 1, "GPIB0::5::INSTR")
        self.gpib_grid1.SetCellValue(1, 1, "13.8")
        self.gpib_grid1.SetCellValue(2, 1, "6")

        ## Grid2 ##
        self.grid2 = wx.StaticText( self.gpib_control_scrolled,-1, u"BUC", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.gpib_grid2 = wx.grid.Grid( self.gpib_control_scrolled,-1, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.gpib_grid2.CreateGrid( 3, 2 )
        self.gpib_grid2.HideRowLabels()
        self.gpib_grid2.HideColLabels()
        self.gpib_grid2.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
        self.gpib_grid2.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_TOP )

        gpib_gSizer2 = wx.BoxSizer( wx.VERTICAL )
        gpib_gSizer2.Add( self.grid2, 0,  wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_gSizer2.Add( self.gpib_grid2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.gpib_grid2.SetCellValue(0, 0, "Address")
        self.gpib_grid2.SetCellValue(1, 0, "V-set (V)")
        self.gpib_grid2.SetCellValue(2, 0, "I-set (A)")

        self.gpib_grid2.SetCellValue(0, 1, "GPIB0::5::INSTR")
        self.gpib_grid2.SetCellValue(1, 1, "24")
        self.gpib_grid2.SetCellValue(2, 1, "6")

        gpib_fgSizer.Add( gpib_gSizer1, 0, wx.EXPAND, 5 )
        gpib_fgSizer.Add( gpib_gSizer2, 0, wx.EXPAND, 5 )

        self.gpib_control_scrolled.SetSizer( gpib_fgSizer )
        self.gpib_control_scrolled.Layout()
        gpib_fgSizer.Fit( self.gpib_control_scrolled )

        gpib_control_bSizer.Add( self.gpib_control_scrolled, 1, wx.EXPAND|wx.ALL, 1 )
        gpib_Sizer1.Add( gpib_control_bSizer, 1, wx.EXPAND|wx.ALL, 10 )
        #------------------------------------------------------------------------
        ## [ MANUAL PANEL ] ##
        gpib_manual_bSizer = wx.StaticBoxSizer( wx.StaticBox( self.gpib_panel,-1, u"MANUAL" ), wx.VERTICAL )
        gpib_instr1_Sizer  = wx.BoxSizer( wx.HORIZONTAL )
        gpib_instr2_Sizer  = wx.BoxSizer( wx.HORIZONTAL )

        gpib_Choices = [ u"write", u"read", u"query" ]

        self.gpib_instr1_address  = Placeholder(gpib_manual_bSizer.GetStaticBox(), -1, placeholder= u"address")
        self.gpib_instr1_command  = Placeholder(gpib_manual_bSizer.GetStaticBox(), -1, placeholder= u"command")
        self.gpib_instr1_choice  = wx.Choice( gpib_manual_bSizer.GetStaticBox(), -1, wx.DefaultPosition, wx.DefaultSize, gpib_Choices, 0 )
        self.gpib_instr1_choice.SetSelection( 0 )

        self.gpib_instr2_address  = Placeholder(gpib_manual_bSizer.GetStaticBox(), -1, placeholder= u"address")
        self.gpib_instr2_command  = Placeholder(gpib_manual_bSizer.GetStaticBox(), -1, placeholder= u"command")
        self.gpib_instr2_choice  = wx.Choice( gpib_manual_bSizer.GetStaticBox(), -1, wx.DefaultPosition, wx.DefaultSize, gpib_Choices, 0 )
        self.gpib_instr2_choice.SetSelection( 0 )

        self.gpib_return_text    = wx.StaticText( gpib_manual_bSizer.GetStaticBox(), -1, u"return:" )
        self.gpib_return_textCtrl= wx.TextCtrl( gpib_manual_bSizer.GetStaticBox(), -1, style = wx.TE_MULTILINE )

        self.gpib_start_btn = wx.Button(gpib_manual_bSizer.GetStaticBox(), -1, u"Start")

        gpib_instr1_Sizer.Add( self.gpib_instr1_address, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_instr1_Sizer.Add( self.gpib_instr1_command, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_instr1_Sizer.Add( self.gpib_instr1_choice, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_instr2_Sizer.Add( self.gpib_instr2_address, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_instr2_Sizer.Add( self.gpib_instr2_command, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        gpib_instr2_Sizer.Add( self.gpib_instr2_choice, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        gpib_manual_bSizer.Add( gpib_instr1_Sizer, 0, wx.ALIGN_CENTER, 5 )
        gpib_manual_bSizer.Add( gpib_instr2_Sizer, 0, wx.ALIGN_CENTER, 5 )
        gpib_manual_bSizer.Add( self.gpib_return_text, 0, wx.ALL, 5 )
        gpib_manual_bSizer.Add( self.gpib_return_textCtrl, 1, wx.ALL^wx.TOP| wx.EXPAND, 15 )
        gpib_manual_bSizer.Add( self.gpib_start_btn, 0, wx.ALL^wx.BOTTOM| wx.ALIGN_RIGHT, 5 )

        gpib_Sizer1.Add( gpib_manual_bSizer, 1, wx.EXPAND|wx.ALL, 10 )
        gpib_Sizer.Add( gpib_Sizer1, 1, wx.EXPAND|wx.ALL, 1 )

        self.gpib_start_btn.Bind(wx.EVT_BUTTON, self.GPIB_start)

        self.gpib_panel.SetSizer( gpib_Sizer )
        self.gpib_panel.Layout()
        gpib_Sizer.Fit( self.gpib_panel )
        self.manual_notebook.AddPage( self.gpib_panel, u"GPIB", True )

        #------------------------------------------------------------------------
        ## [ CONTROL DISPLAY ] ##
        self.GPIB_T = threading.Thread(target = self.GPIB_display, args = (self.close_manual,))
        self.GPIB_T.daemon = True
        self.GPIB_T.start()


    def GPIB_display(self, close_manual):
        self.instr = get_instr()
        self.GPIB_PS_ACU  =  self.instr.GPIB_PS_ACU()
        self.GPIB_PS_BUC  =  self.instr.GPIB_PS_BUC()

        try:
            while True:
                ACU_CURR = self.GPIB_PS_ACU.query("MEAS:CURR? (@1)")
                ACU_VOLT = self.GPIB_PS_ACU.query("MEAS:VOLT? (@1)")
                BUC_CURR = self.GPIB_PS_BUC.query("MEAS:CURR? (@2)")
                BUC_VOLT = self.GPIB_PS_BUC.query("MEAS:VOLT? (@2)")
                self.GPIB_PS_ACU.write("*SRE 0")
                self.GPIB_PS_BUC.write("*SRE 0")
                self.gpib_instrtxt1.SetValue(str(round(float(ACU_CURR),3)) + " A, "+ str(round(float(ACU_VOLT),3)) + " V" )
                self.gpib_instrtxt2.SetValue(str(round(float(BUC_CURR),3)) + " A, "+ str(round(float(BUC_VOLT),3)) + " V" )
                time.sleep(0.5)
                if close_manual == True:
                    break
        except:
            self.prompt_msg("[INFO] The power supply is not ready, please check the connection.")


    def GPIB_ACU_switch(self, state):
        self.instr = get_instr()
        self.GPIB_PS_ACU  =  self.instr.GPIB_PS_ACU()

        ## 這裡做其他指令的寫入 ##
        volt = self.gpib_grid1.GetCellValue(1, 1)
        curr = self.gpib_grid1.GetCellValue(2, 1)
        self.GPIB_PS_ACU.write("Volt %s,(@1)" % volt)
        self.GPIB_PS_ACU.write("CURR %s,(@1)" % curr)

        if not state:
            self.GPIB_PS_ACU.write(":OUTP ON,(@1)")
        else:
            self.GPIB_PS_ACU.write(":OUTP OFF,(@1)")

    def GPIB_BUC_switch(self, state):
        self.instr = get_instr()
        self.GPIB_PS_BUC  =  self.instr.GPIB_PS_BUC()

        ## 這裡做其他指令的寫入 ##
        volt = self.gpib_grid2.GetCellValue(1, 1)
        curr = self.gpib_grid2.GetCellValue(2, 1)
        self.GPIB_PS_ACU.write("Volt %s,(@2)" % volt)
        self.GPIB_PS_ACU.write("CURR %s,(@2)" % curr)

        if not state:
            self.GPIB_PS_BUC.write(":OUTP ON,(@2)")
        else:
            self.GPIB_PS_BUC.write(":OUTP OFF,(@2)")

    def GPIB_start(self, event):
        try:
            address1 = self.gpib_instr1_address.GetValue()
            command1 = self.gpib_instr1_command.GetValue()
            choice1  = self.gpib_instr1_choice.GetStringSelection()
            ret1 = visa_instr(address1, command1, choice1)

        except:
            ret1 = "NO RETURN"

        try:
            address2 = self.gpib_instr2_address.GetValue()
            command2 = self.gpib_instr2_command.GetValue()
            choice2  = self.gpib_instr2_choice.GetStringSelection()
            ret2 = visa_instr(address2, command2, choice2)
        except:
            ret2 = "NO RETURN"

        self.gpib_return_textCtrl.SetValue("GPIB1: " + str(ret1) + '\n' + "GPIB2: " +str(ret2))

    ##########################################################################

    def DAQ_panel(self):

        self.daq_panel = wx.Panel( self.manual_notebook,-1, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.daq = wx.StaticText( self.daq_panel,-1, u"DAQ CONTROL", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.daq.SetFont( wx.Font( 15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ) )

        daq_Sizer = wx.BoxSizer( wx.VERTICAL )
        daq_Sizer.Add( self.daq, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

        daq_Sizer1 = wx.BoxSizer( wx.HORIZONTAL )

        daq_control_bSizer = wx.StaticBoxSizer( wx.StaticBox( self.daq_panel,-1, u"CONTROL" ), wx.VERTICAL )
        daq_manual_bSizer = wx.StaticBoxSizer( wx.StaticBox( self.daq_panel,-1, u"MANUAL" ), wx.VERTICAL )

        ## [ CONTROL PANEL ] ##
        self.DAQ_ACC     = wx.StaticText( daq_control_bSizer.GetStaticBox(), wx.ID_ANY, u"ACC" )
        self.DAQ_LED     = wx.StaticText( daq_control_bSizer.GetStaticBox(), wx.ID_ANY, u"LED" )
        self.DAQ_ACC_btn = Toggle( daq_control_bSizer.GetStaticBox(), self.DAQ_ACC_switch )
        self.DAQ_LED_btn = Toggle( daq_control_bSizer.GetStaticBox(), self.DAQ_LED_switch )

        daq_control_bSizer.Add( self.DAQ_ACC, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        daq_control_bSizer.Add( self.DAQ_ACC_btn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        daq_control_bSizer.Add( self.DAQ_LED, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        daq_control_bSizer.Add( self.DAQ_LED_btn, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		#---------------------------------------------------------------------
        ## [ MANUAL PANEL ] ##
        daq_instr1_Sizer = wx.BoxSizer( wx.HORIZONTAL )
        daq_instr2_Sizer = wx.BoxSizer( wx.HORIZONTAL )
        daq_Choices = [ u"Digital Write", u"Digital Read", u"Analog Write", u"Analog Read" ]

        self.daq_instr1_address = Placeholder(daq_manual_bSizer.GetStaticBox(), -1, placeholder= u"address")
        self.daq_instr1_command = Placeholder(daq_manual_bSizer.GetStaticBox(), -1, placeholder= u"command")
        self.daq_instr1_choice    = wx.Choice( daq_manual_bSizer.GetStaticBox(), -1, wx.DefaultPosition, wx.DefaultSize, daq_Choices, 0 )
        self.daq_instr1_choice.SetSelection( 0 )

        self.daq_instr2_address = Placeholder(daq_manual_bSizer.GetStaticBox(), -1, placeholder= u"address")
        self.daq_instr2_command = Placeholder(daq_manual_bSizer.GetStaticBox(), -1, placeholder= u"command")
        self.daq_instr2_choice    = wx.Choice( daq_manual_bSizer.GetStaticBox(), -1, wx.DefaultPosition, wx.DefaultSize, daq_Choices, 0 )
        self.daq_instr2_choice.SetSelection( 0 )

        self.daq_return_text  = wx.StaticText( daq_manual_bSizer.GetStaticBox(), wx.ID_ANY, u"return:" )
        self.daq_return_textCtrl= wx.TextCtrl( daq_manual_bSizer.GetStaticBox(), -1, style = wx.TE_MULTILINE )

        self.daq_start_btn = wx.Button(daq_manual_bSizer.GetStaticBox(), -1, u"Start")

        daq_instr1_Sizer.Add( self.daq_instr1_address, 0, wx.ALL, 5 )
        daq_instr1_Sizer.Add( self.daq_instr1_command, 0, wx.ALL, 5 )
        daq_instr1_Sizer.Add( self.daq_instr1_choice, 0, wx.ALL, 5 )

        daq_instr2_Sizer.Add( self.daq_instr2_address, 0, wx.ALL, 5 )
        daq_instr2_Sizer.Add( self.daq_instr2_command, 0, wx.ALL, 5 )
        daq_instr2_Sizer.Add( self.daq_instr2_choice, 0, wx.ALL, 5 )

        daq_manual_bSizer.Add( daq_instr1_Sizer, 0, wx.ALIGN_CENTER, 5 )
        daq_manual_bSizer.Add( daq_instr2_Sizer, 0, wx.ALIGN_CENTER, 5 )
        daq_manual_bSizer.Add( self.daq_return_text, 0, wx.ALL, 5 )
        daq_manual_bSizer.Add( self.daq_return_textCtrl, 1, wx.ALL^wx.TOP| wx.EXPAND, 15 )
        daq_manual_bSizer.Add( self.daq_start_btn, 0, wx.ALL^wx.BOTTOM| wx.ALIGN_RIGHT, 5 )

        daq_Sizer1.Add( daq_control_bSizer, 1, wx.EXPAND|wx.ALL, 10 )
        daq_Sizer1.Add( daq_manual_bSizer, 1, wx.EXPAND|wx.ALL, 10 )
        daq_Sizer.Add( daq_Sizer1, 1, wx.EXPAND, 5 )

        self.daq_start_btn.Bind(wx.EVT_BUTTON, self.DAQ_start)

        self.daq_panel.SetSizer( daq_Sizer )
        self.daq_panel.Layout()
        daq_Sizer.Fit( self.daq_panel )
        self.manual_notebook.AddPage( self.daq_panel, u"DAQ", False )

    def DAQ_ACC_switch(self, state):
        self.instr = get_instr()
        self.instr.DAQ_ACC(state)

    def DAQ_LED_switch(self,state):
        self.instr = get_instr()
        self.instr.DAQ_LED(state)

    def DAQ_start(self, event):
        self.daq_instr1_address
        self.daq_instr1_command
        self.daq_instr1_choice

        self.daq_instr2_address
        self.daq_instr2_command
        self.daq_instr2_choice


        address1 = self.daq_instr1_address.GetValue()
        command1 = self.daq_instr1_command.GetValue()
        choice1  = self.daq_instr1_choice.GetStringSelection()
        ret1 = daq_instr(address1, command1, choice1)

        address2 = self.daq_instr2_address.GetValue()
        command2 = self.daq_instr2_command.GetValue()
        choice2  = self.daq_instr2_choice.GetStringSelection()
        ret2 = daq_instr(address2, command2, choice2)


        self.daq_return_textCtrl.SetValue("DAQ1: " + str(ret1.data) + '\n' + "DAQ2: " +str(ret2.data))
    ###########################################################################

    def ETHERNET_panel(self):

        self.ethernet_panel = wx.Panel( self.manual_notebook,-1 )
        self.ethernet = wx.StaticText( self.ethernet_panel,-1, u"ETHERNET CONTROL" )
        self.ethernet.SetFont( wx.Font( 15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ) )

        ethernet_display_bSizer = wx.StaticBoxSizer( wx.StaticBox( self.ethernet_panel,-1, u"CONTROL" ), wx.VERTICAL )
        ethernet_control_bSizer = wx.StaticBoxSizer( wx.StaticBox( self.ethernet_panel,-1, u"MANUAL" ), wx.VERTICAL )

        ethernet_Sizer = wx.BoxSizer( wx.VERTICAL )
        ethernet_Sizer.Add( self.ethernet, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        ethernet_Sizer1 = wx.BoxSizer( wx.HORIZONTAL )
        ethernet_Sizer1.Add( ethernet_display_bSizer, 1, wx.EXPAND|wx.ALL, 10 )
        ethernet_Sizer1.Add( ethernet_control_bSizer, 1, wx.EXPAND|wx.ALL, 10 )
        ethernet_Sizer.Add( ethernet_Sizer1, 1, wx.EXPAND, 5 )
        self.ethernet_panel.SetSizer( ethernet_Sizer )
        self.ethernet_panel.Layout()
        ethernet_Sizer.Fit( self.ethernet_panel )
        self.manual_notebook.AddPage( self.ethernet_panel, u"Ethernet", False )

    ###########################################################################
    def I2C_panel(self):

        self.i2c_panel = wx.Panel( self.manual_notebook,-1 )
        self.i2c = wx.StaticText( self.i2c_panel,-1, u"I2C CONTROL" )
        self.i2c.SetFont( wx.Font( 15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ) )

        i2c_display_bSizer = wx.StaticBoxSizer( wx.StaticBox( self.i2c_panel,-1, u"CONTROL" ), wx.VERTICAL )
        i2c_control_bSizer = wx.StaticBoxSizer( wx.StaticBox( self.i2c_panel,-1, u"MANUAL" ), wx.VERTICAL )

        i2c_Sizer = wx.BoxSizer( wx.VERTICAL )
        i2c_Sizer.Add( self.i2c, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        i2c_Sizer1 = wx.BoxSizer( wx.HORIZONTAL )
        i2c_Sizer1.Add( i2c_display_bSizer, 1, wx.EXPAND|wx.ALL, 10 )
        i2c_Sizer1.Add( i2c_control_bSizer, 1, wx.EXPAND|wx.ALL, 10 )
        i2c_Sizer.Add( i2c_Sizer1, 1, wx.EXPAND, 5 )
        self.i2c_panel.SetSizer( i2c_Sizer )
        self.i2c_panel.Layout()
        i2c_Sizer.Fit( self.i2c_panel )
        self.manual_notebook.AddPage( self.i2c_panel, u"I2C", False )

    def prompt_msg(self, message):
        """ 顯示訊息 """
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            dlg.Close(True)


    def On_Close(self, event):
        self.close_manual = True
        self.Hide()



# if __name__ == '__main__':
#     app = wx.App()
#     frame = manual_dialog(None)
#     app.MainLoop()