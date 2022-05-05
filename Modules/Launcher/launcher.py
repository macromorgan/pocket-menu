"""
This module is responsible for the main launcher module. Along with the menu bar the launcher is
one of two critical components for the UI. Children of the main launcher will be drawn on the
notebook element (the MainAppWindow) and include things such as the application menu and the
settings menu.
"""

import tkinter
import tkinter.ttk
from PIL import ImageTk, Image
import __main__
import Modules.Applications.applications as applications
import Modules.Settings.settings as settings

class MainAppWindow(tkinter.Frame): #pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    The MainAppWindow is a frame that contains a notebook style widget. This allows us to easily
    switch between our settings and applications "tabs". We draw our applications to the various
    frames we register, and use the icons to switch between them.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.update()
        self.get_nav_widget_size()
        self.appsimage = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Launcher/app.png").convert('RGBA').resize((self.nav_widget_size,
                                                                 self.nav_widget_size)))
        self.settingsimage = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Launcher/settings.png").convert('RGBA').resize((self.nav_widget_size,
                                                                      self.nav_widget_size)))
        self.notebook = tkinter.ttk.Notebook(parent, style='TNotebook', padding=(0, 0, 0, 0),
                                             width=self.parent['width'],
                                             height=self.parent['height'])
        self.appstab = tkinter.Frame(self.notebook, background=self.parent['background'],
                                     width=self.frame_width, height=self.frame_height, border=0)
        self.activetab = 0
        self.tabs = {}
        self.settingstab = tkinter.Frame(self.notebook, bg=self.parent['background'],
                                         width=self.frame_width, height=self.frame_height,
                                         border=0)
        self.notebook.add(self.appstab, image=self.appsimage)
        self.tabs[0] = "Apps"
        self.active_tab_name = "Apps"
        self.notebook.add(self.settingstab, image=self.settingsimage)
        self.tabs[1] = "Settings"
        self.notebook.pack()
        self.notebook.update()
        self.appwindow = applications.ApplicationsFrame(self.appstab, self.nav_widget_size,
                                                        width=self.frame_width,
                                                        height=self.frame_height)
        self.settingswindow = settings.SettingsFrame(self.settingstab, self.nav_widget_size,
                                                     width=self.frame_width,
                                                     height=self.frame_height)
        self.appwindow.pack()
        self.settingswindow.pack()
        self.notebook.bind('<<NotebookTabChanged>>', self.get_active_tab_name)
        self.update()

    def get_nav_widget_size(self):
        """
        Derive the size of the navigation widgets (used to determine the left and right margins).
        """
        width = self.parent['width']
        widget_width = round((width * 0.08) / 16) * 16
        if widget_width > 96:
            widget_width = 96
        if widget_width < 32:
            widget_width = 32
        self.nav_widget_size = widget_width
        self.frame_width = int(self.parent['width'] - self.nav_widget_size)
        self.frame_height = int(self.parent['height'])

    def get_active_tab_name(self, event): #pylint: disable=unused-argument
        """
        Not only get the active tab name based on the different tab indexes, but also post the
        active tab name back to the menubar for display on the UI. The event argument is not
        used but is returned by the bound caller, so if we don't include it here we get an error.
        """
        self.activetab = int(self.notebook.index(self.notebook.select()))
        if self.activetab == 0:
            self.active_tab_name = "Apps"
        if self.activetab == 1:
            self.active_tab_name = "Settings"
        __main__.MAINAPP.menu.title.config(text=self.active_tab_name, fg="white")
