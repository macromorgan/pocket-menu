"""
This module is meant to house all the reusable UI elements, as well as the modifications to the
default theme to make it appear pretty.
"""

import tkinter
import tkinter.ttk
from PIL import ImageTk, Image
import __main__
import Modules.Wifi.wifi_widget as wifi_widget
import Modules.Bluetooth.bluetooth_widget as bluetooth_widget
import Modules.Battery.battery_widget as battery_widget

class AppButton(tkinter.Frame): #pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    This class defines a button, consisting of both a frame for the button itself containing an
    icon and a frame for the label. Sizes are defined by the parent which should derive them to
    make things scalable.
    """
    def __init__(self, parent, imagefile, appname, button_size):
        super().__init__(parent)
        self.parent = parent
        self.parent.update_idletasks()
        self.name = appname
        self.button_width = button_size
        self.get_element_sizes()
        self.get_font_size()
        self.configure(background=self.parent['background'])
        self.image_frame = tkinter.Frame(self, background=self.parent['background'],
                                         height=self.image_height, width=self.button_width)
        self.text_frame = tkinter.Frame(self, background=self.parent['background'],
                                        height=self.label_height, width=self.button_width)
        self.image_frame.pack(side="top", expand=True)
        self.text_frame.pack(side="bottom", expand=True)
        self.icon = tkinter.Button(self.image_frame, bd=0, background=self.parent['background'],
                                   activebackground=self.parent['background'], image=imagefile,
                                   height=self.image_height, width=self.button_width)
        self.icon.place(relx=0.5, rely=0.5, anchor="center")
        self.label = tkinter.Label(self.text_frame, bd=0, background=self.parent['background'],
                                   foreground="white", text=self.name,
                                   font=("default", self.font_size), height=self.label_height,
                                   width=self.button_width)
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.update()

    def get_element_sizes(self):
        """
        Based on the size passed to the widget, determine the image and label sizes.
        """
        self.image_height = (int(self.button_width/16) * 12)
        self.label_height = (int(self.button_width / 16) * 4)

    def get_font_size(self):
        """
        Based on the size of the label, determine the optimal font size.
        """
        half_height = (self.label_height / 2)
        self.font_size = int(half_height - (half_height % 4))

class MenuBar(tkinter.Frame): #pylint: disable=too-many-ancestors
    """
    Create a menu bar that is broken up into a left frame with left justified icons, a right frame
    that is broken up into right justified icons, and a center frame that contains the title of
    the active application screen.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(background=self.parent['background'])
        self.configure(height=self.get_menu_height())
        self.configure(width=self.parent.winfo_width())
        self.update()
        self.left_submenu = tkinter.Frame(self, background=self.parent['background'],
                                          height=self.get_menu_height())
        self.right_submenu = tkinter.Frame(self, background=self.parent['background'],
                                           height=self.get_menu_height())
        self.center_submenu = tkinter.Frame(self, background=self.parent['background'],
                                            height=self.get_menu_height(),
                                            width=round(self['width']/3))
        self.left_submenu.pack(side="left", fill="both", expand=True)
        self.right_submenu.pack(side="right", fill="both", expand=True)
        self.center_submenu.place(anchor="nw", y=0, x=round(self['width']/3))
        self.left_widgets = []
        self.right_widgets = []
        self.title = tkinter.Label(self.center_submenu,
                                   background=self.center_submenu['background'],
                                   font=("default", self.get_font_size()))
        self.title.place(relx=0.5, rely=0.5, anchor="center")
        self.add_widgets()
        self.update()

    def add_widgets(self):
        """
        Add widgets to the menubar.
        """
        self.right_widgets.append(wifi_widget.WifiIcon(self.right_submenu))
        self.right_widgets.append(bluetooth_widget.BluetoothIcon(self.right_submenu))
        self.left_widgets.append(battery_widget.BatteryIcon(self.left_submenu))
        for widget in self.right_widgets:
            widget.pack(side="right")
        for widget in self.left_widgets:
            widget.pack(side="left")

    def get_menu_height(self):
        """
        Derive the height of the menu based on the screen size (which should be the root window).
        """
        height = self.parent['height']
        menu_height = round((height * 0.1) / 16) * 16
        if menu_height > 96:
            menu_height = 96
        if menu_height < 32:
            menu_height = 32
        return menu_height

    def get_font_size(self):
        """
        Derive the font size from the given menu height.
        """
        menu_height = self.get_menu_height()
        return int(menu_height / 16) * 8

class PrettyScale(tkinter.ttk.Scale): #pylint: disable=too-many-ancestors
    """
    This class generates the custom scale widget using our custom style. The custom style must be
    initalized first.
    """
    def __init__(self, parent):
        super().__init__(parent, orient="horizontal")
        self.parent = parent
        self.update()
        self.configure(style="custom.Horizontal.TScale")
        self.configure(length=int(self.parent['width']*0.6))
        self.update()

class CustomStyle(tkinter.ttk.Style): #pylint: disable=too-many-ancestors
    """
    This class initalizes our custom style. Only run it once in the main thread.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.theme_use('default')
        self.img_slider = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
                        "/Modules/Elements/circle.png").convert('RGBA').resize((32, 32)))
        self.img_trough = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
                        "/Modules/Elements/slider.png").convert('RGBA'))
        self.element_create('custom.Horizontal.Scale.slider', 'image', self.img_slider,
                            ('active', self.img_slider))
        self.element_create('custom.Vertical.Scrollbar.thumb', 'image', self.img_slider,
                            ('active', self.img_slider))
        self.element_create('custom.Horizontal.Scale.trough', 'image', self.img_trough,
                            ('active', self.img_trough))
        self.layout('custom.Horizontal.TScale',
                    [('custom.Horizontal.Scale.trough',
                      {'sticky': 'nswe',
                       'children': [('custom.Horizontal.Scale.slider',
                                     {'side': 'left', 'sticky': ''})]})])
        self.configure('custom.Horizontal.TScale', background=self.parent['background'])
        self.configure('custom.Horizontal.TScale.trough', height=10)
        self.configure('arrowless.Vertical.TScrollbar', background=self.parent.accent_color,
                       troughcolor=self.parent['background'],
                       bordercolor=self.parent['background'], borderwidth=0)
        self.layout('arrowless.Vertical.TScrollbar',
                    [('arrowless.Vertical.Scrollbar.trough',
                      {'children': [('arrowless.Vertical.Scrollbar.thumb',
                                     {'expand': '1', 'sticky': 'nswe'})],
                       'sticky': 'ns'})])
        self.configure('TNotebook', tabposition='w', background=self.parent['background'],
                       borderwidth=0)
        self.map('TNotebook.Tab', background=[("selected", self.parent['background'])],
                 foreground=[("selected", self.parent['background'])])
        self.configure('TNotebook.Tab', background=self.parent['background'],
                       foreground=self.parent['background'],
                       focuscolor=self.parent['background'], borderwidth=0)


class LauncherFrame(tkinter.Frame): #pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    The main LauncherFrame is supposed to be a container that holds the screen data proper as well
    as a right trough, called the "nav_right", which is used for holding scrollbars when present.
    The nav_right is further subdivided into a nav_right_bottom and a nav_right_top which are
    strictly meant to be empty placeholders, and a nav_right_trough where the scrollbar itself
    should be drawn. The main app container is called the "center", and its where things such
    as the application frame or the settings frame should go. Note that it's a canvas, this is
    so that it can extend beyond the screen size (and thus be scrollable). SubClasses are
    responsible for registering their own scrollbars.
    """
    def __init__(self, parent, nav_widget_size):
        super().__init__(parent)
        self.parent = parent
        self.nav_widget_size = nav_widget_size
        self.configure(height=self.parent['height'],
                       width=self.parent['width'], background=self.parent['background'])
        self.nav_right = tkinter.Frame(self, background=self.parent['background'],
                                       height=self.parent['height'],
                                       width=self.nav_widget_size)
        self.center = tkinter.Canvas(self, background=self.parent['background'], bd=0,
                                     height=self.parent['height'],
                                     width=(self.parent['width'] - (self.nav_widget_size * 2)),
                                     highlightthickness=0)
        self.nav_right.pack(side="right", fill="both")
        self.center.pack(fill="both")
        self.nav_right_trough = tkinter.Frame(self.nav_right, background=self.parent['background'],
                                              width=self.nav_widget_size,
                                              height=(self.parent['height'] - \
                                                      self.nav_widget_size))
        self.nav_right_bottom = tkinter.Frame(self.nav_right, background=self.parent['background'],
                                              height=self.nav_widget_size,
                                              width=self.nav_widget_size)
        self.nav_right_top = tkinter.Frame(self.nav_right, background=self.parent['background'],
                                           height=self.nav_widget_size, width=self.nav_widget_size)
        self.nav_right_top.pack(expand=True, side="top")
        self.nav_right_bottom.pack(expand=True, side="bottom")
        self.nav_right_trough.pack(expand=True, side="top")
        self.update()
