# -*- coding: utf-8 -*-
#==========================================================================
# Project : Test System
# File    : setting_ui.py
#--------------------------------------------------------------------------
# Create setting Panel
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import wx
import wx.lib.agw.labelbook as LB
import wx.lib.scrolledpanel as SC
from pubsub            import  pub
from event.json_func import get_json_data, revised_json_data, write_json_data

#==========================================================================
# MAIN PROGRAM
#==========================================================================

class setting_panel(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None, -1, "MDI Child", size = (600,400))
        super().__init__(parent, -1, "Setting Panel", wx.DefaultPosition, wx.DefaultSize)
        self.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
        self.OnInit()

    def OnInit(self):
        setting_Sizer = wx.BoxSizer( wx.VERTICAL )
        self.setting_listbook = LB.LabelBook(self, -1, agwStyle=LB.INB_FIT_LABELTEXT|LB.INB_LEFT|LB.INB_DRAW_SHADOW|LB.INB_BOLD_TAB_SELECTION)

        self.panel1 = SC.ScrolledPanel( self.setting_listbook, -1, style = wx.DOUBLE_BORDER|wx.TAB_TRAVERSAL )
        self.panel1.SetAutoLayout(1)
        self.panel1.SetupScrolling()

        self.path = "preferences.json"
        self.import_data(self.panel1, self.path)
        self.setting_listbook.AddPage( self.panel1, u"MES info", True)

        setting_Sizer.Add( self.setting_listbook, 1, wx.EXPAND |wx.ALL, 5 )

        self.btn_panel = wx.Panel( self, -1, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.ok_btn = wx.Button( self.btn_panel, -1, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cancel_btn = wx.Button( self.btn_panel, -1, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.apply_btn = wx.Button( self.btn_panel, -1, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )

        btn_Sizer = wx.BoxSizer( wx.HORIZONTAL )
        btn_Sizer.Add( self.ok_btn, 0, wx.ALL, 0 )
        btn_Sizer.Add( self.cancel_btn, 0, wx.ALL, 0 )
        btn_Sizer.Add( self.apply_btn, 0, wx.ALL, 0 )

        self.btn_panel.SetSizer( btn_Sizer )
        self.btn_panel.Layout()
        btn_Sizer.Fit( self.btn_panel )
        setting_Sizer.Add( self.btn_panel, 0, wx.EXPAND |wx.ALL, 5 )

        self.SetSizer( setting_Sizer )
        self.setting_listbook.Fit()

        self.Bind(wx.EVT_CLOSE, self.On_Exit)
        self.ok_btn.Bind(wx.EVT_BUTTON, self.On_Ok)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.On_Cancel)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.On_Apply)
        self.Layout()
        self.Show()

    def On_Exit(self, event):
        self.Hide()

    def On_Ok(self, event):
        self.Hide()

    def On_Cancel(self, event):
        self.Hide()

    def On_Apply(self, event):
        rev = self.export_data(self.path)
        self.save_data(self.path, rev)
        self.Hide()

    def save_data(self, json_path, revise_data):
        """將setting_ui上textctrl得到的所有值存到檔案中"""
        write_data = write_json_data(json_path, revise_data)
        return write_data


    def export_data(self, json_path):
        """先執行import_data得到textctrl屬性後，才能做revise_data，以將textctrl得到的值寫入JSON"""
        get_data = get_json_data(json_path)
        self.revise_data = get_data
        for item in enumerate(get_data):

            for subitem in enumerate(get_data[item[1]]):
                revise_para = getattr(setting_panel, format(str(item[1])+str(subitem[1])+"_subtxt")).GetValue()
                origin_para = str(get_data[item[1]][subitem[1]])
                print(origin_para,"-->",revise_para)
                self.revise_data = revised_json_data(self.revise_data, str(item[1]), str(subitem[1]), str(revise_para))

        return self.revise_data

    def import_data(self, panel, json_path):
        """讀取檔案內JSON檔，並顯示到setting_ui的panel上"""
        get_data = get_json_data(json_path)
        total_Sizer = wx.FlexGridSizer(0,2,0,0)

        if len(get_data) > 1:
            total_Sizer.AddGrowableCol( 0 )
            total_Sizer.AddGrowableCol( 1 )
        total_Sizer.SetFlexibleDirection( wx.BOTH )
        total_Sizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        ## method 2 --利用字典儲存所有 textctrl 變數，無法得到每個textctrl的值 XXXX##
        # self.textctrl_dict = {}

        for item in enumerate(get_data):

            vars()["item_Sizer"+str(item[0])] = wx.BoxSizer( wx.VERTICAL )
            vars()["item_txt"+str(item[0])] = wx.StaticText( panel, -1, str(item[1]))
            vars()["item_txt"+str(item[0])].SetFont( wx.Font( 14, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Calibri" ) )
            vars()["item_Sizer"+str(item[0])].Add( vars()["item_txt"+str(item[0])], 0, wx.ALL, 10 )

            vars()["sub_Sizer"+str(item[0])] = wx.FlexGridSizer(0,2,0,0)
            vars()["sub_Sizer"+str(item[0])].AddGrowableCol( 0 )
            vars()["sub_Sizer"+str(item[0])].AddGrowableCol( 1 )
            vars()["sub_Sizer"+str(item[0])].SetFlexibleDirection( wx.HORIZONTAL )
            vars()["sub_Sizer"+str(item[0])].SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


            for subitem in enumerate(get_data[item[1]]):

                vars()["sub"+str(subitem[0])] = wx.StaticText( panel, -1, str(subitem[1]))
                vars()["sub_Sizer"+str(item[0])].Add( vars()["sub"+str(subitem[0])], 0, wx.ALL | wx.ALIGN_CENTER, 1)


                ## 目的一次完成所有在setting頁面的屬性抓取，已得到更新後的屬性值存入JSON ##
                ## 問題: 由於是批量產生變數，所以無法透過self的屬性變數給function外使用

                ## method 1-- 無法產生self的屬性變數 XXXX ##
                # vars()[str(subitem[1])+"_subtxt"] = wx.TextCtrl( panel, -1, str(get_data[item[1]][subitem[1]]), style = wx.TE_CENTER)
                #----------------------------------------------------------------------------------------------------------
                # vars()["sub_Sizer"+str(item[0])].Add( vars()[str(subitem[1])+"_subtxt"], 0, wx.ALL, 1 )

                ## method 2 ##
                # self.textctrl_dict[str(subitem[1])+"_subtxt"] = str(get_data[item[1]][subitem[1]])

                ## method 3-- 利用getattr、setattr完成 ##
                ## 為避免(item, key, value)-->item或是key在不同頁面有命名重複的可能，因此在textctrl
                ## 變數方面使用了 item + key + _subtxt的組合  str(item[1])+str(subitem[1])+"_subtxt"
                setattr(setting_panel, format(str(item[1])+str(subitem[1])+"_subtxt"), wx.TextCtrl( panel, -1, str(get_data[item[1]][subitem[1]]), style = wx.TE_CENTER))

                ## method 3 ##
                vars()["sub_Sizer"+str(item[0])].Add(getattr(setting_panel, format(str(item[1])+str(subitem[1])+"_subtxt")), 0, wx.EXPAND | wx.ALL, 5)


            vars()["item_Sizer"+str(item[0])].Add( vars()["sub_Sizer"+str(item[0])], 0, wx.EXPAND|wx.ALL, 5 )

            total_Sizer.Add(vars()["item_Sizer"+str(item[0])], 1, wx.EXPAND)

        panel.SetSizer( total_Sizer )

        panel.Layout()
        total_Sizer.Fit( panel )



class MainFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        super().__init__(None, -1, title="Test MDI")
        self.panel = setting_panel(self)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()