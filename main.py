# -*- coding: utf-8 -*-

import wx
from ui.main_ui import Main


if __name__ == '__main__':
    app = wx.App()
    frame = Main(None)
    frame.Show()
    app.MainLoop()
