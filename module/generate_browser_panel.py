# -*- coding: utf-8 -*-
#==========================================================================
# Project : Test System
# File    : generate_browser_panel.py
#--------------------------------------------------------------------------
# Create Browser Tool
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

import wx
import wx.html2
from urllib.parse import urlparse

#==========================================================================
# TEXTCTRL EVENT
#==========================================================================
class Placeholder(wx.TextCtrl):

    def __init__(self, *args, **kwargs):
        """
        Build the TextCtrl
        ----------------------
        When the mouse click on the TextCtrl, then the text will be cleared.
        """
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
class Browser(wx.Panel):
  def __init__(self, parent, id=-1, title='browser'):
    super().__init__(parent, id)
    self.InitUI()

  def InitUI(self):
    self.InitMainView()

  def InitMainView(self):
    self.browser = wx.html2.WebView.New(self)
    self.browser.LoadURL("about:blank")
    self.url_text  = Placeholder(self, -1, placeholder= u"Enter URL", style = wx.TE_PROCESS_ENTER)
    self.Bind(wx.EVT_TEXT_ENTER, self.OnNewURL, self.url_text)
    vertical_box = wx.BoxSizer(wx.VERTICAL)
    vertical_box.Add(self.url_text, 0, flag=wx.EXPAND)
    vertical_box.Add((-1, 10))
    vertical_box.Add(self.browser, 1, flag=wx.EXPAND)
    self.SetSizerAndFit(vertical_box)

  def OnNewURL(self, event):
    """Make Broswer Connect to The Website"""
    new_url = urlparse(self.url_text.GetValue())
    request_path = new_url.geturl()
    if new_url.scheme != "http":
      request_path = "http://" + request_path
    print("[INFO] Connect to the " + request_path)
    self.browser.LoadURL(request_path)
    self.url_text.SetValue(request_path)

#==========================================================================
# USAGE
#==========================================================================
## if you want to execute this script on standalone, please modify the as following steps.

# 1. Change "class Browser(wx.Panel)"  into "class Browser(wx.Frame)"
# 2. Execute the following code ( just delete the symbol comment )

# if __name__ == '__main__':
#   app = wx.App()
#   web = Browser(None,-1,title="Browser Tool")
#   web.Show()
#   app.MainLoop()
