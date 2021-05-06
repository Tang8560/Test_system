# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta fvt Test
# File    : route_check.py 
#--------------------------------------------------------------------------
# MES Route Check
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

# http://192.168.126.245/wuxi/routestation.asmx?wsdl
    # Service: RouteStationService
    #     Port: RouteStationServiceSoap (Soap11Binding: {http://tempuri.org/}RouteStationServiceSoap)
    # Operations:
    #     HelloWorld() -> HelloWorldResult: xsd:string
    #     RouteSation(strSN: xsd:string, strStep: xsd:string, strStation: xsd:string, strUser: xsd:string, strStatus: xsd:string, strType: xsd:string) -> RouteSationResult: xsd:string

""" 
Connect to the webserver to check the status of DUT currently.
-----------------------------------------
strSN:        DUT Serial Number
strUser:      User Name
strType:      MES Test Type
mes_step:      Test Step Name
mes_station:   Test Station Name
mes_server:   MES ip
mes_location: MES location (DNS) 
mes_state:    MES Status
-----------------------------------------
return: User department, Test?, Message (group, test, msg)   
"""
#==========================================================================
# IMPORTS
#==========================================================================
import os
import zeep
from event.json_func  import get_json_data

#==========================================================================
# MAIN PROGRAM
#==========================================================================

def route_check(strSN, strUser, strType, mes_step, mes_station, mes_server, mes_location, mes_state):
       
    if mes_state =='True': 
        WSDL = "http://"+mes_server+"/"+mes_location+"/routestation.asmx?wsdl"
        try:
            client = zeep.Client(wsdl = WSDL)
            CheckRoute_ = client.service.RouteSation(strSN, mes_step, mes_station, strUser, mes_state, strType)
            reture_message = CheckRoute_
            print('reture_message = ',reture_message)
            strlist   = reture_message.split(':')
            result    = strlist[1].replace('Model No','')
            modelno   = strlist[2].replace('Revision','')
            revision  = strlist[3].replace('Work Order','')
            workorder = strlist[4].replace('Error Message','')
            errormsg  = strlist[5]             
            if  result == 'PASS':
                test = True
                msg = "[INFO] Successfully get the DUT info!"
                DUT_info = [modelno,revision,workorder]
            else:
                test = False
                reture_message = 'NA'       
                if errormsg =="":
                    msg = '[WARNING] Web server error!!'
                    DUT_info = ['NA','NA','NA']
                else:
                    msg = "[WARNING] " + errormsg                   
                    DUT_info = ['NA','NA','NA']                    
        except Exception as e:  
            print("[INFO] MES route_check error.")
            print("Check the 'route_check.py'")
            print(e)         
            msg = "Route check function cannot work."
            test = False
            DUT_info = ['NA','NA','NA']
            reture_message = 'NA'    
    else:
        test = True
        msg = "[INFO] Skip route check step."
        DUT_info = ['NA','NA','NA']
        
    print('test= '+str(test)+'\n'+'Model Number= '+str(DUT_info[0])+'\n'+'Revision= '+str(DUT_info[1])+'\n'+ 'Work Order= '+str(DUT_info[2])+'\n'+str(msg))           
    return  test, DUT_info, msg

