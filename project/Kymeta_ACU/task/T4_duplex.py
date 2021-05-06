# -*- coding: utf-8 -*-
#==========================================================================
# Copyright © MTI, Inc.
#--------------------------------------------------------------------------
# Project : Kymeta ACU
# File    : T4_duplex.py 
#--------------------------------------------------------------------------
# Check the NIC connection status to ensure the speed on 1 Gbps and full-duplex.
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

""" 
psutil可用來查看系統狀態
------------------------------------------------------------
類似於調用 Windows 的powershell的功能，不過這個套件是跨平台的
包括: CPU, Memory, Disk, Network, Sensor
https://psutil.readthedocs.io/en/latest/

"""
#==========================================================================
# IMPORTS
#==========================================================================
import os
import sys
import time
import psutil
from pubsub   import pub
from func.path_manager import get_path

#==========================================================================
# IMPORTS JSON Function
#==========================================================================
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from event.json_func import get_json_data

#==========================================================================
# PARAMETER
#==========================================================================
network_name = None

#==========================================================================
# MAIN PROGRAM
#==========================================================================

## 回傳網路相關資訊 ##
class T4_duplex(object):
    
    def __init__(self, thread_event):
        print("T4_duplex")
        try:        
            self.update_info()
            self.network_name = network_name
            if self.network_name == None:
                self.network_name = self.product_nic
                
            self.OnInit()
        except:
            # (1) duplex
            pub.sendMessage("pass_to_grid",test_value = "Boot Error")
            
    def update_info(self):
        print("T4_duplex_info")        
        product_path = get_path.Product_setting(get_path)
        get_product = get_json_data("\\".join(os.path.abspath(__file__).split('\\')[:-2]) + product_path) 
        self.product_nic = get_product["Product"]["NetCard_name"] 
        
        
    def OnInit(self):
        
        #----------------------------------------------------------------------
        ## [ 1.速度與全半雙工檢查 ] ##
        
        network = self.network_status(self.network_name)
        try:
            if network.isup:  
                print("[network isup]", network.duplex )
                print("[network speed]", network.speed )
                
                if str(network.duplex) == "NicDuplex.NIC_DUPLEX_FULL":                  
                    if str(network.speed) == "1000":
                        self.check_duplex_speed = "PASS"
                else:
                    self.check_duplex_speed = "FAIL"
                    print("[T4-3-02] Check the NIC's 'speed  & duplex' on '1.0 Gbps Full Duplex'.")                          
            else:
                self.check_duplex_speed = "FAIL"
                print("[T4-3-01] Cannot find the specific NIC or not connect to the end-device.")
            
            pub.sendMessage("pass_to_grid",test_value = self.check_duplex_speed)
            pub.sendMessage("subtask_processbar", value = 5)
            
        except Exception as e:
            print(e)
            pub.sendMessage("pass_to_grid",test_value = "Boot Error")
            assert ConnectionError
        
    
    def network_connect(self):  # (暫未用到)
        """ 
        取出目前的連線
        ------------------------------
        kind: 選擇過濾的網路類型
            "inet"	IPv4 and IPv6 ("inet4"	IPv4)       ("inet6"	IPv6)
            "tcp"	TCP           ("tcp4" TCP over IPv4)("tcp6"	TCP over IPv6)
            "udp"	UDP           ("udp4" UDP over IPv4)("udp6"	UDP over IPv6)
            "unix"	UNIX socket (both UDP and TCP protocols)
            "all"	the sum of all the possible families and protocols
        ------------------------------
        return:
            fd: the socket file descriptor
            family: the address family, either AF_INET, AF_INET6 or AF_UNIX.
            type: the address type, either SOCK_STREAM, SOCK_DGRAM or SOCK_SEQPACKET.
            laddr: the local address as a (ip, port) named tuple or a path in case of AF_UNIX sockets.
            raddr: the remote address as a (ip, port) named tuple or an absolute path in case of UNIX sockets.
            status: represents the status of a TCP connection.
            pid: the PID of the process which opened the socket, if retrievable, else None.
        """
        
        self.net_connections = psutil.net_connections(kind='inet')

    def network_address(self):  # (暫未用到)
        """
        取出網路卡 NIC (network interface card)相關位址資訊
        --------------------------------
        family: the address family, either AF_INET or AF_INET6 or psutil.AF_LINK, which refers to a MAC address.
        address: the primary NIC address (always set).
        netmask: the netmask address (may be None).
        broadcast: the broadcast address (may be None).
        ptp: stands for “point to point”; it’s the destination address on a point to point interface (typically a VPN).
        """
        self.net_address = psutil.net_if_addrs()

    
    def network_status(self, network_name):
        """
        取出網路卡 NIC (network interface card)相關狀態資訊
        network_name <string> 網卡名稱
        --------------------------------
        [確認網路是否有連線]
        isup: a bool indicating whether the NIC is up and running (meaning ethernet cable or Wi-Fi is connected).
        [查看全半雙工]
        duplex: the duplex communication type; it can be either NIC_DUPLEX_FULL, NIC_DUPLEX_HALF or NIC_DUPLEX_UNKNOWN.
        [查看連線速度]
        speed: the NIC speed expressed in mega bits (MB), if it can’t be determined (e.g. ‘localhost’) it will be set to 0.
        mtu: NIC’s maximum transmission unit expressed in bytes.
        """
        self.net_status = psutil.net_if_stats()
        # print(self.net_status["乙太網路"])       # snicstats(isup=False, duplex=<NicDuplex.NIC_DUPLEX_FULL: 2>, speed=0, mtu=1500)
        # print(self.net_status[network_name].isup)
        # print(self.net_status[network_name].duplex)
        # print(self.net_status[network_name].speed)
        
        self.network = self.net_status[network_name]
        
        return self.network 

# network = system("乙太網路").network
# print(network)
