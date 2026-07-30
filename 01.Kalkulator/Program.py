# -*- coding: utf-8 -*-
"""pip 
Created on Tue Jul 28 10:39:56 2026

@author: Robert
"""
import wx

app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = wx.Frame(None, wx.ID_ANY, "Kalkulator") # A Frame is a top-level window.
frame.Show(True)     # Show the frame.spyd
app.MainLoop()
