import wx
import wx.lib.hyperlink as HL
import sys

HDS_FULLDRAG = 128

if wx.Platform == "__WXMSW__":
	import win32gui, win32con

class RedirectOutput:
	def __init__(self, log):
		self.log = log
	def write(self, text):
		self.log.AppendText(text)

class CustomListCtrl(wx.ListCtrl):
	def __init__(self, parent, id, pos=wx.DefaultPosition,
									size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, -1, pos, size, style)
		self.link_dict = {}
		self.Bind(wx.EVT_SCROLLWIN, self.OnScroll)
		self.Bind(wx.EVT_MOUSEWHEEL, self.OnScroll)
		self.Bind(wx.EVT_LIST_COL_DRAGGING, self.test)
		self.Bind(wx.EVT_LIST_COL_END_DRAG, self.OnRepositionHyperlinks)
		
	def test(self, event):
		print "AA"
	
	def InsertHyperlink(self, row, col, text, url):
		if col == 0:#Insert a blank string item so it can be referenced later
			self.InsertStringItem(row, "")
		width = self.GetColumnWidth(col)
		rect = self.GetItemRect(row)
		height = rect[3]
		start_x = rect[0]+(col*width)
		start_y = rect[1]
		
		link = HL.HyperLinkCtrl(self, wx.ID_ANY, text, URL=url)
		link.SetRect((start_x, start_y, width, height))
		link.SetBackgroundColour(wx.WHITE)
		self.link_dict[(row, col)] = link
		return link
		
	def GetHyperlink(self, row, col):
		try:
			return self.link_dict[(row, col)]
		except KeyError:
			return None
	
	def OnScroll(self, event):		
		event.Skip()
		#self.RepositionHyperlinks()
		wx.CallLater(1, self.OnRepositionHyperlinks)
	
	def ItemIsVisible(self, row):
		#rect = self.GetItemRect(row)
		#Figure out how to tell if an item is visible
		pass
		
	def GetColumnStartX(self, col, start_x=0):
		for x in range(0, col):
			start_x += self.GetColumnWidth(x)
		return start_x
	
	def OnRepositionHyperlinks(self, event=None):
		for key in self.link_dict:
			row, col = key
			link = self.link_dict[key]
			###############print "client rect: "+str(self.GetClientRect())
			###############print "rect: "+str(self.GetRect())
			#print "client arear origin: "+str(self.GetClientAreaOrigin())
			#print "virt size: "+str(self.GetVirtualSize())
			#print "pos: "+str(self.GetConstraints())
			#print "constaints: "+str(self.GetConstraints())
			#print self.GetItem(row).GetText()+" rect: "+str(self.GetItemRect(row))
			rect = self.GetItemRect(row)
			#print "item rect: "+str(rect)
			width = self.GetColumnWidth(col)
			#print width, self.GetColumnWidth(1)
			height = rect[3]
			x = self.GetColumnStartX(col)
			print "col %s, starts at %s pixels" % (str(col), str(x))
			y = rect[1]
			
			if y < 20:#Change later to use ItemIsVisible
				link.SetRect((-100, -100, width, height))
			else:
				link.SetRect((x, y, width, height))
			
			self.Refresh()
		

class Main(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, -1, title, size=(500, 300))
		
		panel = wx.Panel(self, -1)
		self.lst = CustomListCtrl(panel, -1, style=wx.LC_REPORT|wx.LC_HRULES)
		self.lst.InsertColumn(0, "Column A")
		self.lst.InsertColumn(1, "Column B")
		self.lst.InsertColumn(2, "Column C")
		self.lst.InsertColumn(3, "Column D")
		
		self.log = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY)
		sys.stdout = RedirectOutput(self.log)
		sys.stderr = RedirectOutput(self.log)
		
		for x in range(0, 30):
			if x == 4:
				link = self.lst.InsertHyperlink(idx, 0, "link "+str(idx), "C:\\")
				idx = 3
			else:
				idx = self.lst.InsertStringItem(sys.maxint, "item "+str(x))
			
			for y in range(1, 4):
				if y == 1 and idx == 8:
					link = self.lst.InsertHyperlink(idx, y, "link "+str(idx), "C:\\")
				elif y == 2 and idx == 5:
					link = self.lst.InsertHyperlink(idx, y, "link "+str(idx), "C:\\")
				elif y == 3 and idx == 22:
					link = self.lst.InsertHyperlink(idx, y, "link "+str(idx), "C:\\")
				else:
					self.lst.SetStringItem(idx, y, "sub-item "+str(idx))
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.lst, 2, wx.EXPAND)
		sizer.Add(self.log, 1, wx.EXPAND)
		panel.SetSizer(sizer)
		
		self.Center()
		self.Show()
		
		if wx.Platform == "__WXMSW__":
			hwnd = self.GetListCtrl_hwnd()
			style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
			if style & HDS_FULLDRAG:
				print "Removing HDS_FULLDRAG style"
				win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style & ~HDS_FULLDRAG)
	
	def GetListCtrl_hwnd(self):
		hwnd = win32gui.GetActiveWindow()
		print hwnd
		child_windows = []
		win32gui.EnumChildWindows(hwnd, lambda hwnd, resultList: resultList.append((hwnd, win32gui.GetWindowText(hwnd), win32gui.GetClassName(hwnd))), child_windows)
		for hwnd, text, class_name in child_windows:
			if class_name == "SysHeader32":
				break
		return hwnd	

app = wx.App()
frame = Main(None, -1, "CustomListCtrl")
app.MainLoop()