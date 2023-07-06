# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Test System
# File    : upload_server.py
#--------------------------------------------------------------------------
# Upload File to server.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================

import os
import sys
import glob
import datetime
import shutil
import warnings
from ftplib import FTP
# from func.path_manager import get_path
# from event.json_func     import get_json_data

#==========================================================================
# PUB Subscibe
#==========================================================================
project_menu = "project_menu"


#==========================================================================
# MAIN PROGRAM
#==========================================================================

class upload_server(object):

    def mkdir(self, path):
        """ Create directionary """
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
            print("[ INFO ] Create folder successfully: ", path)
        else:
            pass


    # Kymeta
    def kymeta_upload(self, test_type, dist, src):
        warnings.simplefilter('ignore',ResourceWarning)

        if test_type == 'RR' or test_type == 'NormalPrd':

            print("Dist folder", dist)
            print("Src folder", src)
            print('Upload to Kymeta server...')
            self.product_dist = dist +'\\'+str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month).zfill(2)+'/'+os.path.basename(src).split('_')[1] ## [位置]/[年-月]/[檔名(序號)
            try:
                self.mkdir(self.product_dist)
                upload = shutil.copy(src, dist)
                print("Upload to KYMETA server successfully.")
            except Exception as e:
                self.traceback(e)
        else:
            print("KYMETA report not upload.")

    # MTI FTP
    def MTI_upload(self, test_type, src, dist, dist1, mes_server, mes_username, mes_password):
        """
        上傳資料到 MES FTP Server
        --------------------------------
        test_type: 用來決定什麼情況下上傳
        dist: 目標資料夾 'ATS/Kymeta_Interface_Test_UADC/'
        src: 來源檔案位置 'C:/Users/XXXX.log'
        """
        ftp = FTP()
        timeout = 30
        port = 21

        if test_type == 'RR' or test_type == 'NormalPrd':
            upload_path = [dist, dist1]
        else:
            upload_path = [dist]

        for path in upload_path:
            print("Upload to ",'**',path,'**')
            remotepath = path
            try:
                ftp.connect(mes_server, port, timeout)      # Connect FTP server
                ftp.login(mes_username,mes_password)   # Login
                # print (ftp.getwelcome())                       # Check server connection

                ftp.cwd(remotepath)                              # Set FTP path
                # ftp_list = ftp.nlst()                          # Get directory
                # for name in ftp_list:
                #     print(name)                                # Print file name
                localpath = src                                  # Set the local path

                # f = open(path,'wb')                            # Open a file for wanted-storage
                # filename = 'RETR ' + name
                # ftp.retrbinary(filename,f.write)               # Retrieve FTP file
                # ftp.delete(name)                               # Delete FTP file

                print('Upload to MTI MES server...')
                print('[INFO] localpath: ',  localpath)
                print('[INFO] remotepath: ', remotepath)

                fp = open(localpath,'rb')                        # Upload FTP file
                filename = localpath.split('\\')[-1].split('.')[0]
                ftp.storbinary('STOR '+filename, fp)


                # 將離線資料上傳: 但是離線下會無法登入 (該功能有矛盾)
                backup_path = 'backup\\'+ path
                try:
                    os.chdir(backup_path)
                    All = glob.glob('*.log')
                    print('backup_path',backup_path)
                    print('All',All)

                    if All:
                        for back in All:
                            fp_back = open(backup_path +'\\'+ back,'rb')
                            print(fp_back)
                            filename_back = back.split('.')[0]
                            ftp.storbinary('STOR '+filename_back, fp_back)
                    else: pass
                except: pass
                print('[ MES ] Upload MES server successfully')
                webserver = 'PASS'
                ftp.quit()                                       # Exit FTP server

            except Exception as e:
                print('No MES connection Currently')
                self.traceback(e)
        return webserver

    def traceback(self, error):
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,', line '+ str(traceback.tb_lineno))

# webserver = MTI_upload('NormalPrd', 'C:/Users/6065/Desktop/Kymeta_U8/data/' + 'PASS' +'_'+'TEST1216201'+'_'+'20201216183254'+'.log', 'ATS_UADC/Kymeta_Interface_Test_UADC/')
# print(webserver)


