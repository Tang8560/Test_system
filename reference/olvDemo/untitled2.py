# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 14:06:28 2021

@author: 6065
"""


# -*- coding: UTF-8 -*-

import wx

class App(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(400, 300), style=wx.DEFAULT_FRAME_STYLE)

        # ステータスバー
        self.CreateStatusBar()

        # パネル
        p = wx.Panel(self, wx.ID_ANY)

        # インスタンス化
        self.listctrl = wx.ListCtrl(p, wx.ID_ANY, style=wx.LC_REPORT)
        self.listctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.item_select)

        # カラム
        self.listctrl.InsertColumn(0, "氏名", wx.LIST_FORMAT_LEFT, 150)
        self.listctrl.InsertColumn(1, "性別", wx.LIST_FORMAT_LEFT, 100)
        self.listctrl.InsertColumn(2, "年齢", wx.LIST_FORMAT_LEFT, 100)

        # ListCtrlにアイテムを追加
        for x in range(4):
            self.listctrl.InsertItem(x, '山田　%s郎' % x)
            self.listctrl.SetItem(x, 1, "男")
            self.listctrl.SetItem(x, 2, str((x + 1) * 5))

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.listctrl, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        p.SetSizer(layout)

        self.Show()

    def item_select(self, event):
        """ アイテム選択時のイベントハンドラー """
        # 選択したアイテムのインデックスを取得する
        select_index = self.listctrl.GetFirstSelected()

        # インデックスのアイテムからテキストを取得する
        text0 = self.listctrl.GetItemText(select_index, 0)  # 氏名
        text1 = self.listctrl.GetItemText(select_index, 1)  # 性別
        text2 = self.listctrl.GetItemText(select_index, 2)  # 年齢

        item_label = text0 + "は" + text1 + "で" + text2 + "歳です"

        # ステータスバーの文字列を変更
        self.SetStatusText(item_label)

app = wx.App()
App(None, wx.ID_ANY, 'ListCtrl REPORT')
app.MainLoop()