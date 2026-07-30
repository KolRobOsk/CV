import wx
class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="")
        self.panel = wx.Panel(self)
        self.my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.walls_label = wx.StaticText(self.panel, label="Ilość Ścianek:")
        self.results_label = wx.StaticText(self.panel, label="1")
        self.my_sizer.Add(self.walls_label,0, wx.ALL, 5)
        self.walls = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.walls.SetFocus()
        self.walls.Bind(wx.EVT_TEXT_ENTER, self.OnClick)
        self.my_sizer.Add(self.walls, 0, wx.ALL, 5)
        self.my_sizer.Add(self.results_label,0, wx.ALL, 5)
        self.panel.SetSizer(self.my_sizer)
        self.Show()
        
    def OnClick(self, event):
        #text = self.txt.GetValue()
        try:
            self.results_label.SetLabel("2")
            self.sizer.Layout()
        except:
            pass
            
            

