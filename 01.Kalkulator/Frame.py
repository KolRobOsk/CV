import wx
class Frame(wx.Frame):
    def __init__(self):
        #tworzenie okna i kontrolera (sizer) rozstawienia elementów na oknie
        wx.Frame.__init__(self, None, title="")
        self.panel = wx.Panel(self)
        self.my_sizer = wx.BoxSizer(wx.VERTICAL)
        #deklaracja elementów w oknie
        self.walls_label = wx.StaticText(self.panel, label="Ilość Ścianek:")
        self.results_label = wx.StaticText(self.panel, label="1")
        self.walls_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.execute_button = wx.Button(self.panel, wx.ID_ANY, 'Oblicz', (15, 15))
        self.walls_input.SetFocus()
        #powiązanie funkcji i interakcji użytkownika z oknem
        self.execute_button.Bind(wx.EVT_BUTTON, self.execute_script)
        #dodanie do kontrolera wszystkich elementów
        self.my_sizer.Add(self.walls_label,0, wx.ALL, 5)
        self.my_sizer.Add(self.walls_input, 0, wx.ALL, 5)
        self.my_sizer.Add(self.results_label,0, wx.ALL, 5)
        self.my_sizer.Add(self.execute_button ,0, wx.ALL, 5)
        self.panel.SetSizer(self.my_sizer)
        self.Show()
        
    def execute_script(self, event):
        #text = self.txt.GetValue()
        try:
            self.results_label.SetLabel("2")
            self.sizer.Layout()
        except:
            pass
            
            

