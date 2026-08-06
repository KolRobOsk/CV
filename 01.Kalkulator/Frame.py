import wx
class Frame(wx.Frame):
    def __init__(self):
        #tworzenie okna i kontrolera (sizer) rozstawienia elementów na oknie
        wx.Frame.__init__(self, None, title="")
        self.SetLabel("Kalkulator Prawdopodobieństwa")
        self.panel = wx.Panel(self)
        self.my_sizer = wx.GridBagSizer(self.panel.GetSize()[0]//2, self.panel.GetSize()[1])
        #deklaracja elementów w oknie
        self.walls_label = wx.StaticText(self.panel, label="Ilość ścianek:")
        self.rolls_label = wx.StaticText(self.panel, label="Ilość rzutów:")
        self.divisible_label = wx.StaticText(self.panel, label="Podzielne przez:")
        self.results_label = wx.StaticText(self.panel, label="")
        self.is_odd = wx.CheckBox(self.panel, wx.ID_ANY, 'Uzględnić wartości nieparzyste?')
        self.is_even = wx.CheckBox(self.panel, wx.ID_ANY, 'Uzględnić wartości parzyste?')
        #pola wprowadzenia wartości
        self.walls_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.rolls_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.divisible_input = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        #przycisk uruchomienia skryptu
        self.execute_button = wx.Button(self.panel, wx.ID_ANY, 'Oblicz', (15, 15))
        self.walls_input.SetFocus()
        #powiązanie funkcji i interakcji użytkownika z oknem
        self.execute_button.Bind(wx.EVT_BUTTON, self.execute_script)
        #dodanie do kontrolera wszystkich elementów
        #pierwsza kolumna
        self.my_sizer.Add(self.walls_label, pos=(0,0))
        self.my_sizer.Add(self.walls_input, pos=(1,0))
        self.my_sizer.Add(self.divisible_label, pos=(2,0))
        self.my_sizer.Add(self.divisible_input, pos=(3,0))
        self.my_sizer.Add(self.rolls_label, pos=(4,0))
        self.my_sizer.Add(self.rolls_input, pos=(5,0))
        #druga kolumna
        self.my_sizer.Add(self.is_odd, pos=(0,1))   
        self.my_sizer.Add(self.is_even, pos=(1,1))
        self.my_sizer.Add(self.results_label, pos=(2,1))
        self.my_sizer.Add(self.execute_button, pos=(6,1))
        self.panel.SetSizer(self.my_sizer)
        self.Show()
        
    def execute_script(self, event):
        self.check_vals_empty()
        if self.is_odd.Value or self.is_even.Value:
            results = self.get_results()
            if results == 1:
                self.results_label.SetLabel("Prawdopodobieństwo:\n" + str(1))
            elif results > 1:
                #zmienne wynikowe
                results = self.get_results()
                self.results_label.SetLabel("Prawdopodobieństwo:\n" + str(results) + "/"+ str(self.walls_input.Value))
                #przedwczesny koniec działania funkcji
            else:
                self.results_label.SetLabel("Brak możliwych wyników:\n")
        else:
            self.results_label.SetLabel("Brak możliwych wyników:\n")

    def check_divisible(self, value):
        if value%int(self.divisible_input.Value)==0:
            return True
        else:
            return False
        
    def check_set_empty(self, set_num):
        #sprawdź czy ilość możliwości jest większa od 0
        if set_num == []:
            return True
        else: 
            return False
        
    def check_vals_empty(self):
        self.walls_input.Value = self.check_empty_singular(self.walls_input)
        self.rolls_input.Value = self.check_empty_singular(self.rolls_input)
        self.divisible_input.Value = self.check_empty_singular(self.divisible_input)
        
    def get_results(self):
        odd, even, counter = self.is_odd.Value, self.is_even.Value, 0
        if odd or even:
            for value in range(1, 1 + int(self.walls_input.Value)):
                if self.check_divisible(value):
                    if (odd and even) or (odd and value%2==1) or (even and value%2==0):
                        counter += 1
        return counter                       
                                
    def check_empty_singular(self, field):
        if field.GetValue().strip()=="":
            return "1"
        else:
            return field.GetValue()
