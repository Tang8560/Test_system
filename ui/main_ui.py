# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : main_ui.py 
#--------------------------------------------------------------------------
# Combine all UI panel
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import os
import wx
import sys
import time
import threading
import importlib.util
from pubsub import pub 
from wx.lib.agw import aui

#==========================================================================
# IMPORTS UI PANEL
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)  

from ui.menu_ui     import  menu_panel
from ui.toolbar_ui  import  toolbar_panel
from ui.info_ui     import  info_panel
from ui.check_ui    import  check_panel
from ui.notebook_ui import  notebook_panel
from ui.log_ui      import  log_panel
from ui.serial_ui   import  serial_panel
from ui.control_ui  import  control_panel
from ui.setting_ui  import  setting_panel


#==========================================================================
# IMPORTS TASK FUNCTION
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from project.main_task    import main_process
from module.create_thread import Thread
from event.json_func      import get_json_data

from login.login_ui             import login_dialog
from login.route_check          import route_check
from module.generate_report_csv import csv_report, open_csv
from module.generate_report_txt import txt_report
from module.upload_server       import upload_server

#==========================================================================
# PUB SUBSCRIBE
#==========================================================================
project_menu    = "project_menu"
open_menu       = "open_menu"
save_menu       = "save_menu"
setting_menu    = "setting_menu"
manual_menu     = "manual_menu"
run_continue    = "run_continue"
run_stopfail    = "run_stopfail"
run_abort       = "run_abort"
test_end        = "test_end"
generate_csv    = "generate_csv"
generate_txt    = "generate_txt"
generate_serial = "generate_serial"
upload_file     = "upload_file"

#==========================================================================
# PARAMETER
#==========================================================================
menu_image_path    = root + "\\source\\image\\"
toolbar_image_path = root + "\\source\\image\\"
control_image_path = root + "\\source\\button\\"


#==========================================================================
# MAIN PROGRAM
#==========================================================================
                
class Main (wx.Frame):
	
    def __init__(self, parent):
        """ Main panel """
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        wx.Frame.__init__ (self, parent, -1, title = u"Test System", size=(framew, frameh))
        
        pub.subscribe(self.pub_project, project_menu)
        pub.subscribe(self.pub_open_csv, open_menu )     
        pub.subscribe(self.pub_save_csv, save_menu )  
        pub.subscribe(self.pub_setting, setting_menu )
        pub.subscribe(self.pub_manual, manual_menu )
          
        pub.subscribe(self.pub_run_continue, run_continue)
        pub.subscribe(self.pub_run_stopfail, run_stopfail)
        pub.subscribe(self.pub_run_abort, run_abort)

        pub.subscribe(self.pub_test_end, test_end)
        pub.subscribe(self.pub_generate_csv, generate_csv )
        pub.subscribe(self.pub_generate_txt, generate_txt )
        pub.subscribe(self.pub_generate_serial, generate_serial)
        pub.subscribe(self.pub_upload_file, upload_file )
        
        self.SetMinSize((framew*0.5, frameh*0.67))         
        self.Startup()   
        
        get_preferences = get_json_data("preferences.json")
        mes_state    = get_preferences["Preferences"]["MES_State"]
        
        if mes_state == "True":      
            self.login = login_dialog(self, "Login Dialog")
            self.login.ShowModal()

    def Startup(self):
        """ Startup the UI """  
        self.menu_panel = menu_panel(self, menu_image_path)
        self.Status()
        self.BuildPanel() 
        self.InitUI()
        
        # Create UI Thread 
        T_Timer = threading.Thread(target =self.Timer, args=())
        T_Timer.start()
        
    def BuildPanel(self):
        """ Build panel object """       
        ## Create Panel Object
        self.toolbar_build = toolbar_panel(self, toolbar_image_path)
        self.notebook_build = notebook_panel(self)
        self.info_build = info_panel(self)
        self.check_build = check_panel(self)
        self.log_build = log_panel(self)
        self.serial_build = serial_panel(self)
        self.control_build = control_panel(self, control_image_path)
        
        ## Create AUI Manager
        
        ## wx.aui.AuiManager
        self.manager = aui.AuiManager()
        self.manager.SetManagedWindow(self)
        
        ## wx.aui.AuiPaneInfo
        self.toolbar_info = aui.AuiPaneInfo().Name("toolbar").Caption(u"Toolbar").\
            ToolbarPane().LeftDockable(False).RightDockable(False).Top().Gripper(False).Row(0)
        
        self.info_info = aui.AuiPaneInfo().Name('info').Caption('Test Environment').\
            Left().LeftDockable(True).MaximizeButton(True).CloseButton(False).Show().Floatable(False).Movable(False).Position(0).Layer(1)     
        
        self.check_info = aui.AuiPaneInfo().Name('check').Caption('Test Item').\
            Left().LeftDockable(True).MaximizeButton(True).CloseButton(False).Show().Floatable(False).Movable(False).Position(1).Layer(1)   
            
        self.log_info = aui.AuiPaneInfo().Name('log').Caption('Log report').\
            Left().LeftDockable(True).MaximizeButton(True).CloseButton(False).Show().Floatable(False).Movable(False).Position(2).Layer(1)   
            
        self.serial_info = aui.AuiPaneInfo().Name('serial').Caption('Serial report').\
            Left().LeftDockable(True).MaximizeButton(True).CloseButton(False).Show().Floatable(False).Movable(False).Position(2).Layer(1)   
        
        self.notebook_info = aui.AuiPaneInfo().Name('notebook').Center().\
            MaximizeButton(True).CloseButton(False).Show().Movable(False).Floatable(True)

        self.control_info = aui.AuiPaneInfo().Name('control').CenterPane().\
            MaximizeButton(True).MinimizeButton(True).Show().Floatable(True).Movable(False).Fixed()  


    def InitUI(self):      
        """ Main frame layout """  
        self.manager.AddPane(self.toolbar_build, self.toolbar_info)        
        self.manager.AddPane(self.info_build, self.info_info) 
        self.manager.AddPane(self.check_build, self.check_info)  
        self.manager.AddPane(self.serial_build, self.serial_info)
        self.manager.AddPane(self.log_build, self.log_info, target=self.serial_info)
        
        self.manager.AddPane(self.notebook_build, self.notebook_info)
        self.manager.AddPane(self.control_build, self.control_info)
        
        ## [Note] Adjust Panel Proportion ##
        self.manager.GetPane("notebook").dock_proportion = 10
        self.manager.GetPane("control").dock_proportion = 2
        
        self.manager.Update()

        self.Bind(wx.EVT_SIZE, self.onResize)
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show()
        
    def Status(self):
        """ Statusbar """
        self.statusbar = self.CreateStatusBar(style = wx.STB_SIZEGRIP)
        self.statusbar.SetForegroundColour((255,255,255))
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-8,-1,-1])  # Status bar proportion (split into three part)
        self.statusbar.SetStatusText("UTF-8",1)

        self.total_seconds = 0     
            
    def Timer(self):
        """ Stopwatch """
        while True:
            time.sleep(1)
            self.total_seconds += 1
            seconds = self.total_seconds % 60
            minutes = int((self.total_seconds / 60) % 60)
            hours   = int((self.total_seconds / 3600) % 24)
            times   = str(hours).zfill(2)+":"+str(minutes).zfill(2)+":"+str(seconds).zfill(2)
            self.statusbar.SetStatusText("Run Time:     "+ times, 2) 
            self.statusbar.Layout()

    def onResize(self, event):
        framex, framey, framew, frameh = wx.ClientDisplayRect()
        self.framew = framew
        self.frameh = frameh
        self.Refresh()
        
    def task_flow(self, project_path, table, thread_event):
        # print("[INFO] Project path: " + self.project_path)
        
        product_path = self.project_path + self.func.get_path.Product_setting(self.func.get_path) 
        station_path = self.project_path + self.func.get_path.Station_setting(self.func.get_path)
        get_product = get_json_data(product_path)
        get_station = get_json_data(station_path)


        get_preferences = get_json_data("preferences.json")
        mes_state      = get_preferences["Preferences"]["MES_State"]
        mes_location   = get_preferences["Preferences"]["MES_Location"]
        mes_server     = get_preferences["Preferences"]["MES_Server"]
        mes_station    = get_station["Station"]["Station"]
        mes_step       = get_station["Station"]["Step"]
           
        serialnum = self.toolbar_build.serialnum.GetValue()
        user = self.control_build.user_txt.GetValue()
        testtype = str(self.toolbar_build.testtype.GetStringSelection())
        
        MES_return = route_check(serialnum, user, testtype, mes_step, mes_station, mes_server, mes_location, mes_state)  

        if MES_return[0] == True:
            main_process(project_path, table, thread_event)
        else:
            print("You need to inspect your authentication, and restart it again.\n")

    def pub_project(self, project_path):
        """ Based on the selected project to set the test table """
        self.project_path = project_path
        sys.path.append(self.project_path)

        modualspec = importlib.util.spec_from_file_location("func", self.project_path +'\\func\\path_manager.py' )                
        self.func = importlib.util.module_from_spec(modualspec)               
        modualspec.loader.exec_module(self.func)   
        

        modualspec = importlib.util.spec_from_file_location("func", self.project_path +'\\func\\manual_tool.py' )                
        self.manual = importlib.util.module_from_spec(modualspec)               
        modualspec.loader.exec_module(self.manual) 

    def pub_open_csv(self, file_path):
        print("[INFO] Open" + file_path)
        open_csv(file_path, self.notebook_build.test_grid)
        
    def pub_save_csv(self, file_path):
        print("[INFO] Save" + file_path)
        self.pub_test_end("0000",0,0)

        try:
            self.csv_file = csv_report(self.serial,self.model,self.modelrev,self.softrev,self.operator,self.result,self.label,self.data, file_path)                   
        except Exception as e:
            self.traceback(e) 

    def pub_setting(self, run):
        self.setting_build = setting_panel(self)
        self.setting_build.Show()
        
    def pub_manual(self, run):
        self.manual_build = self.manual.manual_tool(self)
        self.manual_build.Show()
      
    def pub_run_continue(self, run):
        print("[INFO] Run test")
        self.control_build.alarm_txt.SetValue("")
        self.control_build.result.SetBitmapLabel(self.control_build.result.image_non)
        self.table = self.notebook_build.set_table()
        self.notebook_build.selectrow = 0
        self.thread_event = threading.Event()
        self.t = Thread(target= self.task_flow, args=(self.project_path, self.table, self.thread_event,))
        self.t.daemon = True
        self.t.start()

    def pub_run_stopfail(self, run):   
        print("[INFO] Run test with stop on failure")
        self.table = self.notebook_build.set_table()
        self.notebook_build.selectrow = 0
        self.thread_event = threading.Event()
        self.t = Thread(target= self.task_flow, args=(self.project_path, self.table, self.thread_event,))
        self.t.daemon = True
        self.t.start() 
        
    def pub_run_abort(self, run):
        print("[INFO] Abort the test")
        try:
            self.t.terminate() 
        except Exception as e:
            self.traceback(e)
        
    def pub_test_end(self, date, start, end):
        try:
            self.date = date
            self.start = start
            self.end = end
            self.product_path = self.project_path + self.func.get_path.Product_setting(self.func.get_path) 
            self.station_path = self.project_path + self.func.get_path.Station_setting(self.func.get_path)
            get_product = get_json_data(self.product_path)
            get_station = get_json_data(self.station_path)
        
        except Exception as e:
            self.traceback(e)

        try:
            self.serial        = str(self.toolbar_build.serialnum.GetValue())
            self.dev           = str(self.toolbar_build.dev.GetValue())
            self.testtype      = str(self.toolbar_build.testtype.GetStringSelection())
            self.env           = str(self.toolbar_build.temperature.GetStringSelection())

            self.station       = get_station["Station"]["Station"]
            self.step          = get_station["Station"]["Step"]
            self.model         = get_product["Product"]["Part_number"]
            self.modelrev      = get_product["Product"]["Rev"]

            self.date_all      = self.date
            self.start_all     = self.start
            self.end_all       = self.end
            self.testtime      = str(self.end_all - self.start_all)

            error = []
            any((error.append("".join("[ErrorCode(%s)]" %i))) for i in list(dict.fromkeys(self.notebook_build.error_code)))
            self.error         = str(self.serial + ''.join(error))

            self.operator      = self.control_build.user_txt.GetValue()
            
            self.wo            = "NA"
            self.failitemnum   = str(len(self.notebook_build.error_code))
            self.softrev       = "01.00"
            self.datasheetrev  = "NA"

            
            self.label    = []
            self.data     = []
            self.data_all = []
            
            for col in range(self.notebook_build.test_grid.GetNumberCols()):
                self.label.append(self.notebook_build.test_grid.GetColLabelValue(col)) 
                for row in range(self.notebook_build.test_grid.GetNumberRows()):
                    self.data.append(self.notebook_build.test_grid.GetCellValue(row, col))
            for row in range(self.notebook_build.test_grid.GetNumberRows()):       
                # print(data[row:24:4])
                self.data_all.append(self.data[row: self.notebook_build.test_grid.GetNumberCols()*self.notebook_build.test_grid.GetNumberRows():self.notebook_build.test_grid.GetNumberRows()])
                
            self.data = self.data_all 
            print("Successfully get data from window.")

            if len(error) > 0: 
                self.result = "FAIL"
            else: 
                self.result = "PASS"
            
            self.control_build.alarm_txt.SetValue(str(self.error))
            
        except Exception as e:
            self.traceback(e)
    
    def pub_generate_csv(self):
        try:
            self.csv_file = csv_report(self.serial,self.model,self.modelrev,self.softrev,self.operator,self.result,self.label,self.data)                   
        except Exception as e:
            self.traceback(e)        
    def pub_generate_txt(self):
        try:
            self.text_file = txt_report(self.serial,self.station,self.step,self.date,self.start_all,self.end_all,self.testtime,self.result,self.error,self.operator,self.wo,\
                    self.model,self.modelrev,self.failitemnum,self.testtype,self.softrev,self.datasheetrev,self.env,self.label,self.data)       
        except Exception as e:
            self.traceback(e)
        
    def pub_generate_serial(self):
        pass
        
    def pub_upload_file(self):     
        
        testtype = str(self.toolbar_build.testtype.GetStringSelection()) 
        product_path = self.project_path + self.func.get_path.Product_setting(self.func.get_path) 
        station_path = self.project_path + self.func.get_path.Station_setting(self.func.get_path)
        path_path    = self.project_path + self.func.get_path.Path_setting(self.func.get_path)

        get_product = get_json_data(product_path)
        get_station = get_json_data(station_path)
        get_path   = get_json_data(path_path)

        print(get_product)
        print(get_station)
        print(get_path)

        try:     ## [ upload MES Server ] [FTP]  ##                                      
            self.Upload_MES_Src      = get_path["Path"]["Save_Report_Path"] 
            self.Upload_MES_Dist     = get_station["Station"]["FTP_Upload"]                    
            self.Upload_MES_Dist1    = self.Upload_MES_Dist.split('/')[0]+'_UADC/'+self.Upload_MES_Dist.split('/')[1]                                        
            
            self.mes_server   = get_station["Station"]["FTP_Server"]       # 172.16.10.11
            self.mes_username = get_station["Station"]["FTP_UserName"]     # uadc
            self.mes_password = get_station["Station"]["FTP_Password"]     # uadc           
            upload_server().MTI_upload(testtype, self.text_file.filepath, self.Upload_MES_Dist, self.Upload_MES_Dist1, self.mes_server, self.mes_username, self.mes_password)   
            
            # "ATS/Kymeta_Interface_Test_UADC/"  
            # "C:/Users/user/Desktop/Report"
            # "ATS_UADC/Kymeta_Interface_Test_UADC/"  
            
        except Exception as e:
            print('MES report upload failed.\n')         
            self.traceback(e) 
        
        try:     ## [ upload Kymeta Server ] [Telnet] ##  
            self.Upload_Product_Src  = get_path["Path"]["Save_Product_Path"] 
            self.Upload_Product_Dist = get_product["Product"]["Server_Path"]        
            upload_server().kymeta_upload(testtype, self.Upload_Product_Dist, self.csv_file.filepath)    
            
             # "//172.16.129.11/ops_data/U8_ACU"
            # "C:/Users/USER/Desktop/Product"
            
        except Exception as e:
            print('KYMETA report upload failed.\n')
            self.traceback(e)               

            
    def mkdir(self, path):
        """ Create folder """
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
            print("[ INFO ] Create folder successfully: ", path)
        else:
            pass  
    
    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))

        
if __name__ == '__main__':
    app = wx.App(0)                                 
    frame = Main(None)
    frame.Show()
    app.MainLoop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    