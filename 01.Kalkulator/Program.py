# -*- coding: utf-8 -*-
"""pip 
Created on Tue Jul 28 10:39:56 2026

@author: Robert
"""
from Frame import Frame
from wx import App

if __name__ == "__main__":
    app = App(False) 
    frame = Frame() 
    frame.Show(True)     
    app.MainLoop()      