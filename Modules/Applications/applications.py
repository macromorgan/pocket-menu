"""
This module is responsible for handling the application list of the main launcher. It will parse
and display all applications that should be presented to the user.
"""

import tkinter
import tkinter.ttk
from PIL import ImageTk, Image
import __main__
import Modules.Elements.ui_elements as ui_elements

class IconList(tkinter.Frame): #pylint: disable=too-many-ancestors
    """
    The icon list is a frame inside of the application launcher that contains all the application
    buttons. The icon list tries to dynamically identify the opimum number of rows and columns
    based on the size of the screen.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.update()
        self.configure(background=self.parent['background'], width=self.parent['width'],
                       height=self.parent['height'])
        self.button_size = self.derive_button_size()
        self.num_columns = self.get_num_columns()
        self.configure_columns(self.num_columns)
        self.application_buttons = []
        self.app_list = self.read_application_lists()
        self.create_app_buttons()
        self.num_rows = self.get_num_rows()
        self.is_scroll_needed()
        self.update()

    def get_num_rows(self):
        """
        Get the number of rows by finding the maximum row number in the active application buttons.
        """
        num_rows = 0
        for button in self.application_buttons:
            if button.grid_info()['row'] > num_rows:
                num_rows = button.grid_info()['row']
        return num_rows + 1

    def is_scroll_needed(self):
        """
        Determine if the number of applications to display requires us to scroll. Returns a boolean
        which is used to draw the scroll bar (or not).
        """
        if self.num_rows * self.button_size > self['height']:
            self.scroll_needed = True
        else:
            self.scroll_needed = False

    def get_num_columns(self):
        """
        Based on the image size determine how many columns we should have for application buttons.
        """
        remainder = self['width'] % self.button_size
        intermediate_size = self['width'] - remainder
        return int(intermediate_size / self.button_size)

    def configure_columns(self, num_columns):
        """
        Iterate over the columns to make sure they expand properly to fill the display space.
        """
        for column in range(num_columns):
            self.columnconfigure(column, weight=1)

    def read_application_lists(self):
        """
        This is a half-complete function that is designed to load application icons. This
        hard-codes the values today, but in the future we will search through a directory
        for *.desktop files.
        """
        icon_size = (int(self.button_size/16) * 12)
        app_list = [{'name': 'File Browser',
                     'icon': __main__.DIR_PATH + '/Modules/Applications/browser.png',
                     'shortcut': '/usr/bin/true'},
                    {'name': 'Terminal',
                     'icon': __main__.DIR_PATH + '/Modules/Applications/console.png',
                     'shortcut': '/usr/bin/true'},
                    {'name': 'Chat',
                     'icon': __main__.DIR_PATH + '/Modules/Applications/chat.png',
                     'shortcut': '/usr/bin/true'},
                    {'name': 'Games',
                     'icon': __main__.DIR_PATH + '/Modules/Applications/controller.png',
                     'shortcut': '/usr/bin/true'},
                    {'name': 'Web Browser',
                     'icon': __main__.DIR_PATH + '/Modules/Applications/internet.png',
                     'shortcut': '/usr/bin/true'},
                    {'name': 'Email',
                     'icon': __main__.DIR_PATH + '/Modules/Applications/mail.png',
                     'shortcut': '/usr/bin/true'},
                    {'name': 'Music',
                     'icon': __main__.DIR_PATH + '/Modules/Applications/music.png',
                     'shortcut': '/usr/bin/true'},
                    {'name': 'Text Editor',
                     'icon': __main__.DIR_PATH + '/Modules/Applications/notepad.png',
                     'shortcut': '/usr/bin/true'}
                    ]
        for record in app_list:
            record['image_blob'] = \
                ImageTk.PhotoImage(Image.open(record['icon']).convert('RGBA').resize((icon_size,
                                                                                      icon_size)))
        return app_list

    def create_app_buttons(self):
        """
        For the list of given applications create app buttons for them (including deriving the
        necessary padding).
        """
        x_padding = int((self['width'] % self.button_size) / self.num_columns / 2)
        current_column = 0
        current_row = 0
        for application in self.app_list:
            self.application_buttons.append(ui_elements.AppButton(self, application['image_blob'],
                                                                  application['name'],
                                                                  self.button_size))
        for application_button in self.application_buttons:
            if current_column > self.num_columns - 1:
                current_column = 0
                current_row += 1
            application_button.grid(column=current_column, row=current_row, ipadx=x_padding)
            current_column += 1

    def derive_button_size(self):
        """
        Based on the size of the parent window, determine the optimal button size.
        """
        intermediate_size = (self['height'] -(self['height'] % 16)) / 16
        button_size = ((intermediate_size - (intermediate_size % 2)) / 2) * 16
        return int(button_size)

class ApplicationsFrame(ui_elements.LauncherFrame): #pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    The main LauncherFrame is a subclass of the AppFrame which holds a list of all the applications
    available to be launched.
    """
    def __init__(self, parent, nav_widget_size, width, height):
        super().__init__(parent, nav_widget_size)
        self.configure(background=self.parent['background'], width=width,
                       height=height)
        self.parent.update()
        self.iconlist = IconList(self.center)
        self.center.create_window(0, 0, window=self.iconlist, anchor="nw")
        self.iconscroll = tkinter.ttk.Scrollbar(self.nav_right_trough,
                                                style="arrowless.Vertical.TScrollbar",
                                                orient='vertical',
                                                command=self.center.yview)
        if self.iconlist.scroll_needed:
            self.iconscroll.place(height=int(self.nav_right_trough['height']*0.8), width=8,
                                  relx=0.5, anchor="center", rely=0.5)
            self.update()
            self.center.config(yscrollcommand=self.iconscroll.set,
                               scrollregion=self.center.bbox("all"))
        self.update()
