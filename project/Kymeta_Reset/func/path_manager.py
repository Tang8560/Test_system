# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta Reset
# File    : path_manager.py
#--------------------------------------------------------------------------
# Build path manager for csv, json, image
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

"""
由於屬性事件在 class --> function，因此調用類別時是不會得到function內的屬性的，
所以 ex:  getattr(get_icon, format("task_ico_path")) 會得不到東西

需要進到 function內取值
return = get_icon.task_icon(get_icon)

"""

#==========================================================================
# IMPORTS
#==========================================================================
from pubsub import pub


class get_backimage(object):

    def head_backimage(self):
        self.headimg_path = "\\src\\image\\back.jpg"
        return self.headimg_path

class get_path(object):

    def Specification(self):
        self.spec_path = "\\config\\Specification.csv"
        return self.spec_path

    def Product_setting(self):
        self.product_path = "\\config\\product.json"
        return self.product_path

    def Path_setting(self):
        self.path_path = "\\config\\path.json"
        return self.path_path

    def Instrument_setting(self):
        self.instr_path = "\\config\\instrument.json"
        return self.instr_path

    def Station_setting(self):
        self.station_path = "\\config\\station.json"
        return self.station_path

    def Other_setting(self):
        self.other_path = "\\config\\other.json"
        return self.other_path


class get_icon(object):

    def login_icon(self):
        self.login_ico_path = "\\src\\image\\login.ico"
        return self.login_ico_path

    def instrument_icon(self):
        self.instrument_ico_path = "\\src\\image\\instrument.ico"
        return self.instrument_ico_path

    def task_icon(self):
        self.task_ico_path = "\\src\\image\\product.ico"
        return self.task_ico_path

    def programming_icon(self):
        self.programming_ico_path = "\\src\\image\\path.ico"
        return self.programming_ico_path

class get_image(object):

    def passbtn_image(self):
        self.passbtn_image_path = "\\src\\button\\pass.png"
        return self.passbtn_image_path

    def failbtn_image(self):
        self.failbtn_image_path = "\\src\\button\\fail.png"
        return self.failbtn_image_path

    def blankbtn_image(self):
        self.blankbtn_image_path = "\\src\\button\\blank.png"
        return self.blankbtn_image_path

    def openbtn_image(self):
        self.openbtn_image_path = "\\src\\button\\on.png"
        return self.openbtn_image_path

    def closebtn_image(self):
        self.closebtn_image_path = "\\src\\button\\off.png"
        return self.closebtn_image_path

class get_task_image(object):

    def init(self):
        self.init_path = "\\src\\task_image\\0.Init.jpg"
        return self.init_path

    def open_switch(self):
        self.open_switch_path = "\\src\\task_image\\1.Normally_open_switch.png"
        return self.open_switch_path

    def depressed_switch(self):
        self.depressed_switch_path = "\\src\\task_image\\2.Depressed_Switch.png"
        return self.depressed_switch_path

    def TRANSEC_R(self):
        self.transec_R_path = "\\src\\task_image\\3.TRANSEC_R.png"
        return self.transec_R_path

    def TRANSEC_G(self):
        self.transec_G_path = "\\src\\task_image\\4.TRANSEC_G.png"
        return self.transec_G_path

    def NET_R(self):
        self.net_R_path = "\\src\\task_image\\5.NET_R.png"
        return self.net_R_path

    def NET_G(self):
        self.net_G_path = "\\src\\task_image\\6.NET_G.png"
        return self.net_G_path

    def STATUS_R(self):
        self.status_R_path = "\\src\\task_image\\7.STATUS_R.png"
        return self.status_R_path

    def STATUS_G(self):
        self.status_G_path = "\\src\\task_image\\8.STATUS_G.png"
        return self.status_G_path

    def TX_R(self):
        self.TX_R_path = "\\src\\task_image\\9.TX_R.png"
        return self.TX_R_path

    def TX_G(self):
        self.TX_G_path = "\\src\\task_image\\10.TX_G.png"
        return self.TX_G_path

    def RX_R(self):
        self.RX_R_path = "\\src\\task_image\\11.RX_R.png"
        return self.RX_R_path

    def RX_G(self):
        self.RX_G_path = "\\src\\task_image\\12.RX_G.png"
        return self.RX_G_path

    def PWR_R(self):
        self.PWR_R_path = "\\src\\task_image\\13.PWR_R.png"
        return self.PWR_R_path

    def PWR_G(self):
        self.PWR_G_path = "\\src\\task_image\\14.PWR_G.png"
        return self.PWR_G_path

#############################################

## TypeError: 'str' object is not callable
## ------------------------------------------
## 檢查命名重複
