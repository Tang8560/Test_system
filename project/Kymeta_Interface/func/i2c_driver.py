# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 13:47:25 2020

@module name I2C driver
    input  : I2C Function | input data (Address, Register, Data)
    output : Result | Data 
    
@user guide
    I2C_Driver(self, I2C_Function, Address, Register, Data) 
        
    I2C_Function (str)
    Address      (str)
    Register     (str)
    Data         (str)       
"""
import wx
import time
# Use for transmitting handle value and connecting device
import pickle  
import aardvark_py as aa
from array import array

class I2C_Driver(wx.Frame):
    
    def __init__(self):    
        self.setting(True)
        
    def setting(self,Enable):
        """
        Initial Setting
        --------------------
        When I2C_Driver be as external call, the Enable should be set to "False".
        self.Enable : Build temp file 
        """    
        # Realize to pass the instrument handle by extracting/storing a handle variable to register file.    
        self.Enable = Enable            #  (option) [True, False] 
        
        # Select flags parameter
        self.b10_addressing = False     #  (option) [True, False]  
        self.comb_format    = False     #  (option) [True, False]
        self.no_stop        = False     #  (option) [True, False]   
        
        b10_addressing = int(self.b10_addressing == 'true')
        comb_format = int(self.comb_format == 'true')*2
        no_stop = int(self.no_stop == 'true')*4              
        self.flags = b10_addressing or comb_format or no_stop
        return  self.flags           
                                               
    def initial(self,rcp="I2C",pomp="Both",pump="Both"): 
        """
        Start I2C connection and setting configuration
        """
        #Setting the connection and pull-up resustance of I2C device. # (option)
        requested_config = {'GPIO Only':0,'SPI + GPIO':1,'GPIO + I2C':2,'I2C':3,'Query':128}
        power_mask       = {'Off' :0,'Both':1,'Query':2}
        pullup_mask      = {'None':0,'Both':1,'Query':2,'< 3 >':3,'< 128 >':4} 
        
        rc  = requested_config[rcp]   
        pom = power_mask[pomp]
        pum = pullup_mask[pump]            
        
        # Use for the connection more then one time, it will pop-up window
        self.i = 0
        self.Data_out = ""
        print('Device connecting...')
        while True:
            device = array('H', [0]*4)
            self.return_,self.devices = aa.aa_find_devices(device)
            # print('[ return ]',self.return_,'[ port_number ]',self.devices[0])  
            self.handle = aa.aa_open(self.devices[0])
            # print('[ handle ]',self.handle)  
            if self.handle <= 0: self.handle = 0
            else: self.handle = self.handle
            # print('[ handle_mod ]',self.handle)
            
            if self.handle == 0:
                self.result = False                
                if self.i == 0:        
                    aa.aa_close(1)
                    self.i += 1
                    print('Please wait....')
                else:
                    print("Failed to connect the i2c : [initial]" )
                    msg = "Can\'t find the i2c, please check the connection!"       
                    caption = "Connection Error"
                    self.Error_handling(msg, caption) 
                    return
            else:
                print('Successfully connect: [%s]' % rcp)
                aa.aa_configure(self.handle, rc)
                tp = aa.aa_target_power(self.handle, pom) 
                if tp == 3:
                    tp = True 
                else: tp = False
                icp = aa.aa_i2c_pullup(self.handle, pum)               
                if icp == 3:
                    icp = True 
                else: tp = False
                self.result = tp & icp
                self.i += 1      
                print('Initial Complete...')
                return
            
        if self.Enable ==True:    
            with open('handle_variable', 'wb') as f:
                # print('Make handle= %s write into register file' % self.handle)
                pickle.dump(self.handle, f)
        else: pass            
        print("------------------------------------------")       
        return self.result, self.Data_out, self.handle
    
    def write(self,Address,Register,Data): 
        print("[write] %s %s %s" %(Address,Register,Data))
        self.Address = Address
        self.Register = Register
        self.Data = Data
        
        if self.Enable ==True:         
            self.Temporal_file(self.Enable)
            if self.handle == 1:
                print('Connection status: [PASS]')   
            else:
                print('Connection status: [FAIL]')
        else: 
            print('Connection interrupt: [setting]')
            print("Can\'t find the i2c, please check the connection!") 
            return                 
    
        Address=int(self.Address,16)   
        Register=int(self.Register,16) 
        
        if type(self.Data) == list:
            self.Data0 = []
            for d in self.Data:
                self.Data0.append(int(d,16))
                
            self.Data1 = array('B',[Register,self.Data0[0],self.Data0[1]])
            self.Data2 = array('B',[Register])
        else: 
            self.Data = self.Data
            self.Data0 = int(self.Data,16)
            self.Data1 = array('B',[Register,self.Data0])
            self.Data2 = array('B',[Register])
        
        print('Address = %s, Register = %s, Data = %s' %(self.Address,self.Register,self.Data))
        # print('Hexadecimal to Decimal.')
        # print('Address = %s, Register = %s, Data = %s' %(Address,Register,self.Data0))

        aa.aa_i2c_write_ext(self.handle,Address,self.flags,self.Data1)

        if self.Address =='2E': wait = 0.3
        else: wait = 0.02
        time.sleep(wait)    
        status,nbw  = aa.aa_i2c_write_ext(self.handle,Address,self.flags,self.Data2)

        if status >= 0:  nbw = nbw
        else:            nbw = 0
        # print('i2c_write_ext return : status = %s,nbw = %s' % (status ,nbw))
        print('i2c write data...')
        
        if type(self.Data) != list:
            self.Data = [self.Data]
            
        # self.Data = array('B',[0 for _ in range(nbw)])
        self.Data = array('B',[0]*len(self.Data))
        
        _ret_, data_in, num_read  = aa.aa_i2c_read_ext(self.handle,Address,self.flags,self.Data)
        # print('i2c_read_ext return : return = %s  data_in = %s, num_read = %s ' % (_ret_ ,data_in, num_read)) 
        incoming_data = data_in
 
        print('[ write ] Compltetly write data: ',incoming_data)
        # print (incoming_data[0])
        # print ('self.Data0',self.Data0)  
        
        # Obtain array value        
        try:
            # for i in range(len(self.Data))
            # string = incoming_data[0]
            # print(string)
            # self.Data_out = hex(string)[-2:].zfill(2)         
            # self.Data_out = str(string)
            # print('Data_out =',self.Data_out)       
            # print('Data0 =',self.Data0)    
            self.Data_out = incoming_data
            if incoming_data == self.Data:
                self.result = True
            else:
                self.result = False
        except Exception as e:
            print (e)
            
            self.Data_out = ""
            self.result = False
        print("Hex output [result=%s, Data_out=%s] " % (self.result,self.Data_out))
        print("------------------------------------------")
        return self.result,self.Data_out,self.handle 

    def read(self,Address,Register,nbw): 
        print("[ read ] %s %s %s" %(Address,Register,nbw))
        self.Address = Address
        self.Register = Register
        self.nbw = nbw
        
        if self.Enable ==True:         
            self.Temporal_file(self.Enable)
            if self.handle == 1:
                print('Connection status: [PASS]')   
            else:
                print('Connection status: [FAIL]')
        else: 
            print('Connection interrupt: [setting]')
            print("Can\'t find the i2c, please check the connection!")                   
            return
      
        Address=int(self.Address,16)   
        Register=int(self.Register,16)      
        print('Address = %s, Register = %s' %(self.Address,self.Register))
        # print('Hexadecimal to Decimal.')
        # print('Address = %s, Register = %s' %(Address,Register))
        status, nbw  = aa.aa_i2c_write_ext(self.handle,Address,self.flags,array('B',[Register]))
        # print('i2c_write_ext return : status = %s,nbw = %s' % (status ,nbw))
        
        if status >= 0: 
            length = max(int(self.nbw),nbw)
            nbw = array('B', [0]*length)
        else:           nbw = 0
            
        _ret_, data_in, num_read  = aa.aa_i2c_read_ext(self.handle,Address,self.flags,nbw)
        # print('i2c_read_ext return : return = %s  data_in = %s, num_read = %s ' % (_ret_ ,data_in, num_read))
        print('i2c read data...')

        incoming_data = data_in 
        print('[ read ] Compltetly read the data: ',incoming_data)
        
        #Obtain value
        try:
            self.Data_out = []
            for i in range(num_read):
                string = incoming_data[i]
                self.Data_out.append(hex(string)[-2:].zfill(2))   
            self.Data_out = str(self.Data_out)
        except Exception as e:
            print(e)
            self.Data_out = "" 
        # detect status equal to 0 or not
        self.result = status is 0  
        print("Hex output [result=%s, Data_out=%s]" % (self.result,self.Data_out))
        print("------------------------------------------")
        return self.result, self.Data_out, self.handle        

            
    def close(self): 
        if self.Enable ==True:         
            self.Temporal_file(self.Enable)         
            # print('Loading handle = %s' % self.handle)   
        else: pass           
        _ret_ = aa.aa_close(self.handle) 
        
        # print(_ret_)
        self.handle = 0
        self.Data_out = ''
        self.result = True
        print('Disconnect i2c ')
        # print (Style.BRIGHT)
        # print(" close return ",Fore.RED +'[self.result=%s, self.Data_out=%s, self.handle=%s]' % (self.result,self.Data_out,self.handle ))
        # print(Style.RESET_ALL)
        print("------------------------------------------")
        return self.result, self.Data_out, self.handle 
        
    def Error_handling(self,message,caption):
        
        dlg = wx.MessageDialog(parent = None, message = message, caption = caption)
        dlg.ShowModal()
        dlg.Destroy()
 
    def Array_String(self,Data_in):
        """usage: (srting) = Array_String(u08[] data_in)"""  
        try:
            Data_out = '0'+hex(Data_in[1])+hex(Data_in[2])[0]
        except:
            print("[ Error ] It seems that you didn't import an completely array.")  
            Data_out = None
        return Data_out
    
    def Temporal_file(self,Enable):
        if Enable == True:
            with open('handle_variable', 'rb') as f:
                self.handle = pickle.load(f)
        else: 
            print("Can\'t find the i2c, please check the connection")


      




    

















