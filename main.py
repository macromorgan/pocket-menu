#!/usr/bin/python3

"""
This is the launcher application written in Python 3 / TKinter to replace the Pocket-Home app for
devices running Debian 11. This file represents the main executable that kicks off the program as
a whole.
"""

import tkinter
import os
import Modules.Elements.ui_elements as ui_elements
import Modules.Launcher.launcher as launcher

class Main(tkinter.Tk):
    """
    The main class which draws the screen, consisting of a frame, which is divided into a menu upper
    and a body lower. The menu upper is 10% of the screen Y size or 32 pixels (which ever is bigger)
    and spans the full X size. The body lower uses the remaining screen real estate.
    """
    def __init__(self):
        super().__init__()
        #self.root.attributes('-fullscreen', True)
        self.geometry("480x272")
        self.update()
        self.configure(background="#505050")
        self.accent_color = '#0078D4'
        self.style = ui_elements.CustomStyle(self)
        self.resizable(0, 0)
        self.main_window = tkinter.Frame(self, background=self['background'], borderwidth=0,
                                         width=self.winfo_width(), height=self.winfo_height())
        self.main_window.pack(fill="both", expand=True)
        self.main_window.update()
        self.menu = ui_elements.MenuBar(self.main_window)
        self.menu.pack(side="top", fill="x")
        self.menu.update()
        self.body = tkinter.Frame(self.main_window, background=self.main_window['background'])
        self.body.pack(side="bottom", fill="both", expand=True)
        self.body.update()
        self.body.configure(height=self.body.winfo_height(), width=self.body.winfo_width())
        self.update()
        self.applauncher = launcher.MainAppWindow(self.body)
        self.applauncher.pack(fill="both", expand=True)
        self.menu.title.config(text=self.applauncher.active_tab_name, fg="white")

if __name__ == '__main__':
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    MAINAPP = Main()
    MAINAPP.mainloop()
