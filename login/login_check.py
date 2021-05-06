# -*- coding: utf-8 -*-

# module name: Login check

import re
import zeep
from requests.exceptions import ConnectionError



def login_check(MES_Server,UserName,Password):      
    """ 
    連線到網路伺服器，調用功能並取得回傳值
    -----------------------------------------
    MES_Server: MES的連線ip
    UserName:   輸入帳號
    Password:   輸入密碼
    -----------------------------------------
    return: 用戶單位，使用權限?，訊息 (group, test, msg)   
    """
    
    LoginWSUrl = "http://%s/mes/executive.asmx?WSDL"
    WSDL = (LoginWSUrl %MES_Server)
    
    try:
        client = zeep.Client(wsdl = WSDL)
        LoginUser_ = client.service.LoginUser(UserName,Password)
        if LoginUser_['StatusMessage'] == '1':
            
           # 在webserver上允許被使用的function
           # GetUserGroups(sessionID: xsd:string, strUserName: xsd:string) -> GetUserGroupsResult: xsd:string
            
           GetUserGroups_ = client.service.GetUserGroups(LoginUser_['LoginUserResult'],UserName)
           group = re.search('"(.+?)"', GetUserGroups_).group(1)
           test = True
           msg = u"[INFO] Successfully login your account."                        
        else:
            group ='Error'  
            test = False  
            msg = u"[INFO] Please check your login account!"
    except ConnectionError as e:
        print(e)
        group ='Error' 
        test = False  
        print("[LC01] Connect Server Error")
        print("Check the end device setting or network connection error")
        msg = u"Please check the MES status and inform manager!"
        
    print(msg)
    print("[INFO] Your Group: ", group)
    return  group, test, msg
    
        
## [ UserGuide ] ##
    
# Login_check = login_check('172.16.10.104','5689','5689')
# Login_check = login_check('192.168.126.245','5133','5133')

          
    
