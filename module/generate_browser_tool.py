import wx
import wx.html2
from urllib.parse import urlparse   

class Browser(wx.Frame):
    
    def __init__(self, parent=None, id=-1, title='Simple browser'):
        super(Browser, self).__init__(parent=parent, id=id, title=title)
        self.InitUI()
        self.Maximize()
    
    def alert_error(self, message):
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)
    
    def InitUI(self):
        self.InitStatusBar()
        self.InitMenuBar()
        self.InitMainView()
    
    def InitMainView(self):
        self.browser = wx.html2.WebView.New(self)
        self.browser.LoadURL("about:blank")
        self.url_text = wx.TextCtrl(self, -1, "Enter URL", style = wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnNewURL, self.url_text)
        vertical_box = wx.BoxSizer(wx.VERTICAL)
        vertical_box.Add(self.url_text, 0, flag=wx.EXPAND)
        vertical_box.Add((-1, 10))
        vertical_box.Add(self.browser, 1, flag=wx.EXPAND)
        self.SetSizerAndFit(vertical_box)
    
    def OnNewURL(self, event):
        new_url = urlparse(self.url_text.GetValue())
        request_path = new_url.geturl()
        if new_url.scheme != "http":
            request_path = "http://" + request_path
            
        self.browser.LoadURL(request_path)
        self.url_text.SetValue(request_path)

    def InitMenuBar(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        quit_item = file_menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)
        # Bind quit to actually quit the app:
        self.Bind(wx.EVT_MENU, self.OnQuit, quit_item)
      
        view_menu = wx.Menu()
        self.toggle_status_bar = view_menu.Append(-1, 'Show status bar', 'Toggle show status bar', kind=wx.ITEM_CHECK)
        menu_bar.Append(view_menu, "&View")
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.toggle_status_bar)
        view_menu.Check(self.toggle_status_bar.GetId(), True)
        # Help menu:
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, '&About', 'Show information about the app')
        self.Bind(wx.EVT_MENU, self.OnAbout, about_item)
        menu_bar.Append(help_menu, "&Help")

    def ToggleStatusBar(self, event):
        is_toggled = self.toggle_status_bar.IsChecked()
        if is_toggled:
            self.status_bar.Show()
        else:
            self.status_bar.Hide()

    def OnAbout(self, event):
        about_dialog = wx.MessageDialog(None, message="About window", style=wx.OK)
        dialog_button = about_dialog.ShowModal()
    
    def InitStatusBar(self):
       self.status_bar = self.CreateStatusBar()

    def OnQuit(self, event):
        verify_quit_dialog = wx.MessageDialog(
            None,
            message="Are you sure you want to quit?",
            style=wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        )
        result = verify_quit_dialog.ShowModal()
        if result == wx.ID_YES:
          self.Close()

if __name__ == '__main__':
  app = wx.App()
  dialog = SimpleBrowser(title="My simple browser")
  dialog.Show()
  app.MainLoop()
