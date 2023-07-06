# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : setting_ui.py
#--------------------------------------------------------------------------
# Modify Configuration File
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
from func.path_manager import get_path
from func.json_manager import get_json_data, revised_json_data, write_json_data

# from src import images


#==========================================================================
# MAIN PROGRAM
#==========================================================================

class setting_dialog ( wx.Dialog ):

    def __init__( self, parent ):

        framex, framey, framew, frameh = wx.ClientDisplayRect()
        wx.Dialog.__init__ ( self, parent, -1, u"Settings", size = (framew/1.6 ,frameh/1.6), style = wx.DEFAULT_DIALOG_STYLE|wx.TAB_TRAVERSAL )
        print("[INFO] Open setting panel")
        self.OnInit()

    def OnInit(self):

        self.product_path = get_path.Product_setting(get_path)
        self.path_path    = get_path.Path_setting(get_path)
        self.instr_path   = get_path.Instrument_setting(get_path)
        self.station_path = get_path.Station_setting(get_path)
        self.other_path   = get_path.Other_setting(get_path)


        setting_Sizer = wx.BoxSizer( wx.VERTICAL )

        # 因為Lisbook無法調整頁面大小，所以改用Labelbook
        self.setting_listbook = LB.LabelBook(self, -1, agwStyle=LB.INB_FIT_LABELTEXT|LB.INB_LEFT|LB.INB_GRADIENT_BACKGROUND|LB.INB_BOLD_TAB_SELECTION)

        self.panel1 = SC.ScrolledPanel( self.setting_listbook, -1, style = wx.DOUBLE_BORDER|wx.TAB_TRAVERSAL )
        self.panel1.SetAutoLayout(1)
        self.panel1.SetupScrolling()
        self.panel2 = SC.ScrolledPanel( self.setting_listbook, -1, style = wx.DOUBLE_BORDER|wx.TAB_TRAVERSAL )
        self.panel2.SetAutoLayout(1)
        self.panel2.SetupScrolling()
        self.panel3 = SC.ScrolledPanel( self.setting_listbook, -1, style = wx.DOUBLE_BORDER|wx.TAB_TRAVERSAL )
        self.panel3.SetAutoLayout(1)
        self.panel3.SetupScrolling()
        self.panel4 = SC.ScrolledPanel( self.setting_listbook, -1, style = wx.DOUBLE_BORDER|wx.TAB_TRAVERSAL )
        self.panel4.SetAutoLayout(1)
        self.panel4.SetupScrolling()
        self.panel5 = SC.ScrolledPanel( self.setting_listbook, -1, style = wx.DOUBLE_BORDER|wx.TAB_TRAVERSAL )
        self.panel5.SetAutoLayout(1)
        self.panel5.SetupScrolling()

        self.import_data(self.panel1, self.product_path)
        self.import_data(self.panel2, self.path_path)
        self.import_data(self.panel3, self.instr_path)
        self.import_data(self.panel4, self.station_path)
        self.import_data(self.panel5, self.other_path)


        # 無法在labelbook中匯入圖片(待改進)
        # il = wx.ImageList(16, 16)
        # img_group = ["product_img", "path_img", "instrument_img", "station_img", "other_img" ]

        # pages = [(self.panel1, u"Product info"),
        #          (self.panel2, u"Path manager"),
        #          (self.panel3, u"Instrument manager"),
        #          (self.panel4, u"Station info"),
        #          (self.panel5, u"Other"),]

        #for x in img_group:
        #    obj = getattr(images, x)
        #    bmp = obj.GetBitmap()
        #    il.Add(bmp)

        #self.setting_listbook.AssignImageList(il)

        #imID = 0
        #for page, label in pages:
        #    self.setting_listbook.AddPage(page, label, imID)
        #    imID += 1

        self.setting_listbook.AddPage( self.panel1, u"Product info", True)
        self.setting_listbook.AddPage( self.panel2, u"Path manager", False)
        self.setting_listbook.AddPage( self.panel3, u"Instrument manager", False)
        self.setting_listbook.AddPage( self.panel4, u"Station info", False)
        self.setting_listbook.AddPage( self.panel5, u"Other", False)

        setting_Sizer.Add( self.setting_listbook, 1, wx.EXPAND |wx.ALL, 5 )

        self.btn_panel = wx.Panel( self, -1, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.reset_btn = wx.Button( self.btn_panel, -1, u"Reset to Defaults", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ok_btn = wx.Button( self.btn_panel, -1, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cancel_btn = wx.Button( self.btn_panel, -1, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.apply_btn = wx.Button( self.btn_panel, -1, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )

        btn_Sizer = wx.BoxSizer( wx.HORIZONTAL )
        btn_Sizer.Add( self.reset_btn, 0, wx.ALL, 0 )
        btn_Sizer.Add( ( 0, 0), 1, wx.EXPAND, 5 )
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
        self.reset_btn.Bind(wx.EVT_BUTTON, self.On_Reset)
        self.ok_btn.Bind(wx.EVT_BUTTON, self.On_Ok)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.On_Cancel)
        self.apply_btn.Bind(wx.EVT_BUTTON, self.On_Apply)
        self.Layout()
        self.Show()

    def On_Exit(self, event):
        self.Hide()

    def On_Reset(self, event):
        """利用備存檔案取代後再次開啟檔案"""
        self.Hide()

    def On_Ok(self, event):
        self.Hide()

    def On_Cancel(self, event):
        self.Hide()

    def On_Apply(self, event):
        product_rev = self.export_data(self.product_path)
        path_rev = self.export_data(self.path_path)
        instr_rev = self.export_data(self.instr_path)
        station_rev = self.export_data(self.station_path)
        other_rev = self.export_data(self.other_path)
        self.save_data(self.product_path, product_rev)
        self.save_data(self.path_path, path_rev)
        self.save_data(self.instr_path, instr_rev)
        self.save_data(self.station_path, station_rev)
        self.save_data(self.other_path, other_rev)

        ## 當按下Apply時會傳遞訊號給info_ui和control_ui ##
        self.apply_msg = True
        pub.sendMessage("apply", apply = self.apply_msg)
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

                revise_para = getattr(setting_dialog, format(str(item[1])+str(subitem[1])+"_subtxt")).GetValue()
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
                setattr(setting_dialog, format(str(item[1])+str(subitem[1])+"_subtxt"), wx.TextCtrl( panel, -1, str(get_data[item[1]][subitem[1]]), style = wx.TE_CENTER))

                ## method 3 ##
                vars()["sub_Sizer"+str(item[0])].Add(getattr(setting_dialog, format(str(item[1])+str(subitem[1])+"_subtxt")), 0, wx.EXPAND | wx.ALL, 5)


            vars()["item_Sizer"+str(item[0])].Add( vars()["sub_Sizer"+str(item[0])], 0, wx.EXPAND|wx.ALL, 5 )

            total_Sizer.Add(vars()["item_Sizer"+str(item[0])], 1, wx.EXPAND)

        panel.SetSizer( total_Sizer )

        panel.Layout()
        total_Sizer.Fit( panel )


# if __name__ == '__main__':
#     app = wx.App()
#     dialog = setting_dialog(None)
#     app.MainLoop()

