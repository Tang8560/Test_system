# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 14:30:07 2020

@author: 6065
"""


import wx

class Toggle(wx.Frame):
     
    def __init__(self,state):
        wx.Frame.__init__(self, None, title="Test")
        self.state = state
        self.openbtn = wx.Bitmap("open.png", wx.BITMAP_TYPE_ANY)
        self.closebtn = wx.Bitmap("close.png", wx.BITMAP_TYPE_ANY)
        panel = wx.Panel(self,-1,name="panel")        
        self.Button = wx.BitmapButton(panel,bitmap=self.closebtn, style =0)
        
        # self.Button1.SetBitmapLabel(self.closebtn)    
        # self.Button1.SetBitmapFocus(self.closebtn)      # 直接固定
        # self.Button1.SetBitmapSelected(self.openbtn)    # 點選後會回彈
        # self.Button1.SetBitmapDisabled(self.closebtn)   #        
        # print(self.Button.__dict__)
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.Button) 
        self.Show()
        
    def OnClick(self, event):
        """does the toggling"""
        # state = event.GetEventObject().GetBitmapFocus()

        if self.state==True:
            self.state = False
            self.Button.SetBitmapLabel(self.closebtn)
            # print("False")
        else:
            self.state = True
            self.Button.SetBitmapLabel(self.openbtn)
            # print("True")
        print('Output =', self.Output())
        self.Refresh()
        
    def Output(self):
        return self.state



# if __name__ == "__main__":
#       app = wx.App()
#       frame = Toggle(False)
#       app.MainLoop()


###############################################################
##外部調用方式       
############################################################### 

class MyFrame1 (wx.Frame):
    def __init__(self):
        app = wx.App()
        t =Toggle(False)
        print(Toggle.Output(t))
        app.MainLoop()

frame = MyFrame1()