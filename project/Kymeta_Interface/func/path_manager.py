# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
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

class get_dir(object):

    def ATS_Root_DIR(self):
        self.ATS_root_dir    = ""
        return self.ATS_root_dir

    def Config(self):
        self.config_dir = "\\config\\model\\Configuration"
        return self.Config_dir

    def Error(self):
        self.error_dir = "\\data\\error"
        return self.error_dir

    def Report(self):
        self.report_dir = "\\data\\report"
        return self.report_dir

    def Log(self):
        self.Log_dir = "\\data\\log"
        return self.Log_dir

class get_backimage(object):

    def head_backimage(self):
        self.headimg_path = "\\src\\image\\banner.png"
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

    def SSH_key(self):
        self.sshkey_path = "\\config\\acu_fvt_ossh_key"
        return self.sshkey_path

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

    def init_fixture(self):
        self.init_fixture_path = "\\src\\task_image\\1.init_fixture.jpg"
        return self.init_fixture_path

    def init_barcode(self):
        self.init_barcode_path = "\\src\\task_image\\2.init_barcode.jpg"
        return self.init_barcode_path

    def init_button(self):
        self.init_button_path = "\\src\\task_image\\3.init_button.jpg"
        return self.init_button_path

    def debug_LEDon(self):
        self.debug_LEDon_path = "\\src\\task_image\\4.debug_LEDon.jpg"
        return self.debug_LEDon_path

    def debug_bLEDon(self):
        self.debug_bLEDon_path = "\\src\\task_image\\5.debug_bLEDon.jpg"
        return self.debug_bLEDon_path

    def debug_LEDoff(self):
        self.debug_LEDoff_path = "\\src\\task_image\\6.debug_LEDoff.jpg"
        return self.debug_LEDoff_path

    def debug_bLEDoff(self):
        self.debug_bLEDoff_path = "\\src\\task_image\\7.debug_bLEDoff.jpg"
        return self.debug_bLEDoff_path

    def jtag_sw3(self):
        self.jtag_sw3_path = "\\src\\task_image\\8.jtag_sw3.jpg"
        return self.jtag_sw3_path

    def programming_init(self):
        self.programming_init_path = "\\src\\task_image\\9.programming_init.jpg"
        return self.programming_init_path

    def programming_set(self):
        self.programming_set_path = "\\src\\task_image\\10.programming_set.jpg"
        return self.programming_set_path

    def programming_end(self):
        self.programming_end_path = "\\src\\task_image\\11.programming_end.jpg"
        return self.programming_end_path

    def boot_LED(self):
        self.boot_LED_path = "\\src\\task_image\\12.boot_LED.jpg"
        return self.boot_LED_path

    def cold_reset(self):
        self.cold_reset_path = "\\src\\task_image\\13.cold_reset.jpg"
        return self.cold_reset_path

    def warm_reset(self):
        self.warm_reset_path = "\\src\\task_image\\14.warm_reset.jpg"
        return self.warm_reset_path

#############################################

## TypeError: 'str' object is not callable
## ------------------------------------------
## 檢查命名重複
