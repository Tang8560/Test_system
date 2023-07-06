# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : login_ui.py
#--------------------------------------------------------------------------
# Login interface.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

"""
note: "self.Close" and "wx.EVT_CLOSE" are the same function.
      "event.Veto" is used to stop the event propagation
"""


#==========================================================================
# IMPORTS
#==========================================================================
import os
import wx
from pubsub             import pub
from login.server_check import server_check
from login.login_check  import login_check
from event.json_func  import get_json_data


#==========================================================================
# PUB SENDMESSAGE
#==========================================================================
user = "username"
login_exit = "exit"
#==========================================================================
# MAIN PROGRAM
#==========================================================================
class login_dialog ( wx.Dialog ):

    def __init__( self, parent, title):
        """ login framework """
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        super().__init__ ( parent, -1, title =title, size=(framew*0.3, frameh*0.38), style = wx.CAPTION|wx.SYSTEM_MENU)
        self.SetMaxSize((framew*0.3, frameh*0.38))
        self.SetMinSize((framew*0.3, frameh*0.38))

        self.sc_ret = [False,'NA']
        self.lc_ret = ['NA',False,'NA']
        self.exit   = ''
        self.OnInit()

    def OnInit(self):
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )

        ## top panel ##
        self.top_panel = wx.Panel( self, -1, style = wx.TAB_TRAVERSAL )
        self.top_panel.SetBackgroundColour( wx.Colour( 238, 238, 238 ) )
        self.cation_txt = wx.StaticText( self.top_panel, -1, u"ATS LOGIN" )
        self.cation_txt.SetFont( wx.Font( 20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Semibold" ) )

        ## bottom panel ##
        self.bottom_panel = wx.Panel( self, -1, style = wx.TAB_TRAVERSAL )

        self.name = wx.StaticText( self.bottom_panel, -1, u"User Name:" )
        self.name_txt = wx.TextCtrl( self.bottom_panel, -1, wx.EmptyString, wx.DefaultPosition, (150,28), 0 )
        self.name_txt.SetFocus()
        self.password = wx.StaticText( self.bottom_panel, -1, u"Password:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.password_txt = wx.TextCtrl( self.bottom_panel, -1, wx.EmptyString, wx.DefaultPosition, (150,28), wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        self.login_btn = wx.Button( self.bottom_panel, -1, u"Login", wx.DefaultPosition, (100,30), 0 )
        self.exit_btn = wx.Button( self.bottom_panel, -1, u"Exit", wx.DefaultPosition, (100,30), 0 )

        self.name.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Semibold" ) )
        self.name_txt.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Semibold" ) )
        self.password.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Semibold" ) )
        self.password_txt.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Semibold" ) )
        self.login_btn.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Semibold" ) )
        self.exit_btn.SetFont( wx.Font( 12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI Semibold" ) )

        self.login_btn.Bind(wx.EVT_BUTTON,self.On_Login)
        self.exit_btn.Bind(wx.EVT_BUTTON,self.On_Exit)
        self.password_txt.Bind(wx.EVT_TEXT_ENTER, self.On_Enter)
        self.username = self.name_txt.GetValue()

        ## layout ##
        panel_Sizer = wx.BoxSizer( wx.VERTICAL )
        top_panel_Sizer = wx.BoxSizer( wx.VERTICAL )
        top_panel_Sizer.Add( self.cation_txt, 0, wx.ALIGN_CENTER|wx.ALL ^ wx.BOTTOM, 5 )
        self.top_panel.SetSizer( top_panel_Sizer )
        self.top_panel.Layout()
        top_panel_Sizer.Fit( self.top_panel )
        panel_Sizer.Add( self.top_panel, 1, wx.EXPAND |wx.ALL, 5 )

        bottom_panel_Sizer = wx.BoxSizer( wx.VERTICAL )
        keyin_Sizer    = wx.BoxSizer( wx.HORIZONTAL )
        setfont_Sizer  = wx.BoxSizer( wx.VERTICAL )
        textctrl_Sizer = wx.BoxSizer( wx.VERTICAL )
        button_Sizer   = wx.BoxSizer( wx.HORIZONTAL )

        setfont_Sizer.AddSpacer(10)
        setfont_Sizer.Add( self.name,         0, wx.ALIGN_CENTER|wx.ALL, 5 )
        setfont_Sizer.Add( self.password,     0, wx.ALIGN_CENTER|wx.ALL, 5 )
        textctrl_Sizer.AddSpacer(12)
        textctrl_Sizer.Add( self.name_txt,    0, wx.ALIGN_CENTER|wx.ALL, 5 )
        textctrl_Sizer.Add( self.password_txt,0, wx.ALIGN_CENTER|wx.ALL, 5 )
        button_Sizer.Add( self.login_btn,     0, wx.ALIGN_CENTER|wx.ALL, 5 )
        button_Sizer.AddSpacer(30)
        button_Sizer.Add( self.exit_btn,      0, wx.ALIGN_CENTER|wx.ALL, 5 )
        keyin_Sizer.Add( setfont_Sizer,       0, wx.ALIGN_CENTER|wx.ALL, 5 )
        keyin_Sizer.Add( textctrl_Sizer,      0, wx.ALIGN_CENTER|wx.ALL, 5 )
        bottom_panel_Sizer.Add( keyin_Sizer,  0, wx.ALIGN_CENTER|wx.ALL, 5 )
        bottom_panel_Sizer.Add( button_Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.bottom_panel.SetSizer( bottom_panel_Sizer )
        self.bottom_panel.Layout()
        bottom_panel_Sizer.Fit( self.bottom_panel )
        panel_Sizer.Add( self.bottom_panel, 3, wx.EXPAND |wx.ALL, 5 )

        self.SetSizer( panel_Sizer )
        self.Layout()
        self.Centre( wx.BOTH )
        self.Show(True)

    def On_Login(self,event):

        get_preferences = get_json_data("preferences.json")
        mes_state    = get_preferences["Preferences"]["MES_State"]
        mes_location = get_preferences["Preferences"]["MES_Location"]
        mes_server   = get_preferences["Preferences"]["MES_Server"]

        ## get return ##
        username = self.name_txt.GetValue()
        password = self.password_txt.GetValue()

        if username == "":
            self.prompt_msg("Username cannot be empty")
            self.ShowModal()
            event.Skip()
        elif password == "":
            self.prompt_msg("Password cannot be empty")
            self.ShowModal()
            event.Skip()

        self.username = username
        print("[INFO] Username: %s" %username)

        if mes_state == 'True':
            ##  Enter MES ip, connect time and timeout to check the MES system whether enable or not.(Server Check) ##
            try:
                self.sc_ret = server_check(mes_server, 3, 500)
            except Exception as e:
                print("[INFO] MES server_check error")
                print("Check the 'server_check.py'")
                print(e)

            if self.sc_ret[0] == True:
                try:
                    self.lc_ret = login_check(mes_server, username, password)
                    self.prompt_msg(self.lc_ret[-1])
                    if self.lc_ret[1] == True:
                        pub.sendMessage(user, username=self.username)
                        self.Destroy()
                        event.Skip()
                    else:
                        self.ShowModal()
                        event.Skip()
                except Exception as e:
                    print("[INFO] MES login_check error")
                    print("Check the 'login_check.py'")
                    print(e)
            else:
                self.prompt_msg("[INFO] MES connection error.")
                self.ShowModal()
                event.Skip()

        ## When "MES_State" is not "True", then skip the MES ##
        elif mes_state == 'Flase':
            self.sc_ret = [True,'NA']         # [server_alive, msg]
            self.lc_ret = ["NA",True,'NA']  # [group, test, msg]
            self.Destroy()

        return self.username, self.sc_ret, self.lc_ret


    def On_Enter(self,event):
        try:
            self.On_Login(event)
            event.Skip()
        except Exception as e:
            print("[LD05] login_ui error")
            print("Check the 'login_ui.py'")
            print(e)

    def On_Exit(self,event):

        dlg=wx.MessageDialog(None,u"Are you sure you want to exit program?",u"Confirm close",wx.YES_NO)
        if dlg.ShowModal()==wx.ID_YES:
            self.exit = True
            try:
                pub.sendMessage(login_exit, exit_panel =self.exit)
            except Exception as e:
                print(e)
            print("[INFO] Exit the program")
            self.Destroy()
        else:
            return

    def prompt_msg(self,message):
        dlg = wx.MessageDialog(parent = None, message = message, style=wx.OK|wx.CENTRE)
        if dlg.ShowModal()==wx.ID_OK:
            self.Close(True)

if __name__ == '__main__':
    app = wx.App()
    frame = login_dialog(None,"User Login")
    app.MainLoop()

