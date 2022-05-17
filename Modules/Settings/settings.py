"""
This is the settings portion of the launcher, this module is responsible for presenting all of
the available settings to the end user. It creates a frame that is then placed on the main
launcher application.
"""

import tkinter
import tkinter.ttk
from tkinter.messagebox import askyesno
import os
import dbus
from PIL import ImageTk, Image
import __main__
import Modules.DBus.dbus_main as dbus_main
import Modules.Elements.ui_elements as ui_elements

class SettingsElementFrame(tkinter.Frame): #pylint: disable=too-many-ancestors
    """
    This class isn't used directly, but is instead a parent class of various settings widgets. It
    includes a title and the widget proper.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.update()
        self.configure(background=self.parent['background'])
        self.update()
        self.titleframe = tkinter.Label(self, background=self.parent['background'],
                                        width=self['width'], fg="white")
        self.titleframe.pack(side="top")
        self.widgetframe = tkinter.Frame(self, background=self.parent['background'],
                                         width=self['width'])
        self.widgetframe.pack(side="bottom")

class SettingsDivider(tkinter.Frame): #pylint: disable=too-many-ancestors
    """
    This draws a simple horizontal line for separating settings elements.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.update()
        self.configure(background=self.parent['background'], width=self.parent['width'], height=20)
        self.pack()
        self.dividingline = tkinter.Frame(self, background="#404040", height=2,
                                          width=int(self.parent['width']*0.9))
        self.dividingline.place(relx=0.5, rely=0.5, anchor="center")
        self.update()

class PowerSettings(SettingsElementFrame): #pylint: disable=too-many-ancestors
    """
    The main class for drawing power related widgets.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.update()
        self.button_size = 64
        self.icon_size = (int(self.button_size/16) * 12)
        self.titleframe.configure(text="Power Settings")
        self.shutdown_image = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Settings/shutdown.png").convert('RGBA').resize((self.icon_size,
                                                                      self.icon_size)))
        self.restart_image = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Settings/restart.png").convert('RGBA').resize((self.icon_size,
                                                                     self.icon_size)))
        self.shutdown_button = ui_elements.AppButton(self.widgetframe, self.shutdown_image,
                                                     "Shutdown", self.button_size)
        self.restart_button = ui_elements.AppButton(self.widgetframe, self.restart_image,
                                                    "Restart", self.button_size)
        self.widgetframe.configure(height=self.button_size)
        self.shutdown_button.grid(column=0, row=0)
        self.restart_button.grid(column=1, row=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.shutdown_button.icon.configure(command=self.shutdown_confirm)
        self.restart_button.icon.configure(command=self.restart_confirm)
        self.update()

    def shutdown_confirm(self): #pylint: disable=no-self-use
        """
        Simple function to trigger a dialog and shutdown if the answer is yes.
        """
        answer = askyesno(title="Shutdown System?", message="Are you sure you want to shutdown?")
        if answer:
            obj = dbus_main.DBUS_BUS.get_object('org.freedesktop.login1',
                                                '/org/freedesktop/login1')
            iface = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
            iface.PowerOff(1)

    def restart_confirm(self): #pylint: disable=no-self-use
        """
        Simple function to trigger a dialog and restart if the answer is yes.
        """
        answer = askyesno(title="Restart System?", message="Are you sure you want to restart?")
        if answer:
            obj = dbus_main.DBUS_BUS.get_object('org.freedesktop.login1',
                                                '/org/freedesktop/login1')
            iface = dbus.Interface(obj, 'org.freedesktop.login1.Manager')
            iface.Reboot(1)

class BacklightSettings(SettingsElementFrame): #pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    This class draws a scale to allow users to adjust the backlight value.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.backlight_name = self.get_backlight_name()
        self.backlight_max = self.get_backlight_max(self.backlight_name)
        self.titleframe.configure(text="Backlight Settings")
        self.backlightslider = ui_elements.PrettyScale(self.widgetframe)
        self.backlightslider.configure(from_=0, to=self.backlight_max,
                                       length=int(self.parent['width']*0.6))
        self.backlightslider.set(self.get_backlight_value(self.backlight_name))
        self.light_off_img = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Settings/light-off.png").convert('RGBA').resize((32, 32)))
        self.light_on_img = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Settings/light-on.png").convert('RGBA').resize((32, 32)))
        self.light_off_label = tkinter.Label(self.widgetframe, image=self.light_off_img,
                                             background=self.parent['background'])
        self.light_on_label = tkinter.Label(self.widgetframe, image=self.light_on_img,
                                            background=self.parent['background'])
        self.light_off_label.grid(row=0, column=0)
        self.backlightslider.grid(row=0, column=1)
        self.light_on_label.grid(row=0, column=2)
        self.update()
        self.backlightslider.bind("<ButtonRelease-1>", self.update_backlight)

    def update_backlight(self, frame=None, event=None): #pylint: disable=unused-argument
        """
        Update the backlight once the slider is done being triggered, and then set the slider to
        the new backlight value (slider can be float, but backlight can only be int, so set the
        slider to a matching int). If the backlight can't be set then set the slider back to what
        it was. We set with DBus since it allows us to do so without root.
        """
        backlight_value = round(self.backlightslider.get())
        try:
            obj = dbus_main.DBUS_BUS.get_object('org.freedesktop.login1',
                                                '/org/freedesktop/login1/session/auto')
            iface = dbus.Interface(obj, 'org.freedesktop.login1.Session')
            iface.SetBrightness('backlight', self.backlight_name, dbus.UInt32(backlight_value))
            self.backlightslider.set(backlight_value)
        except: #pylint: disable=bare-except
            self.backlightslider.set(self.get_backlight_value(self.backlight_name))

    def get_backlight_name(self): #pylint: disable=no-self-use
        """
        Get the name of the first backlight by traversing sysfs.
        """
        try:
            return os.listdir('/sys/class/backlight')[0]
        except: #pylint: disable=bare-except
            return None

    def get_backlight_max(self, backlight_name): #pylint: disable=no-self-use
        """
        Get the max value of the backlight from sysfs. Assume the min value is 0.
        """
        with open('/sys/class/backlight/'+backlight_name+'/max_brightness') as backlightfile:
            max_brightness = int(backlightfile.readline())
        return max_brightness

    def get_backlight_value(self, backlight_name): #pylint: disable=no-self-use
        """
        Get the current value of the backlight from sysfs.
        """
        with open('/sys/class/backlight/'+backlight_name+'/brightness') as backlightfile:
            brightness = int(backlightfile.readline())
        return brightness

class VolumeSettings(SettingsElementFrame): #pylint: disable=too-many-ancestors
    """
    This widget draws a scale to allow users to adjust the volume.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.titleframe.configure(text="Volume Settings")
        self.scale_value = tkinter.DoubleVar
        self.volumeslider = ui_elements.PrettyScale(self.widgetframe)
        self.volumeslider.configure(from_=0, to=10, length=int(self.parent['width']*0.6))
        self.light_off_img = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Settings/volume-low.png").convert('RGBA').resize((32, 32)))
        self.light_on_img = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Settings/volume-high.png").convert('RGBA').resize((32, 32)))
        self.light_off_label = tkinter.Label(self.widgetframe, image=self.light_off_img,
                                             background=self.parent['background'])
        self.light_on_label = tkinter.Label(self.widgetframe, image=self.light_on_img,
                                            background=self.parent['background'])
        self.light_off_label.grid(row=0, column=0)
        self.volumeslider.grid(row=0, column=1)
        self.light_on_label.grid(row=0, column=2)
        self.update()

class AllSettings(tkinter.Frame): #pylint: disable=too-many-ancestors
    """
    This class is called to bring together all widgets in a single frame for including
    on the canvass element of the main frame.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.update()
        self.configure(background=self.parent['background'], width=self.parent['width'],
                       height=self.parent['height'])
        self.update()
        self.settings_providers = []
        self.separators = []
        self.register_settings_providers()
        self.is_scroll_needed()
        self.update()
        self.parent.update()

    def register_settings_providers(self):
        """
        Iterate through the (currently hard-coded) settings providers to register them one by one.
        """
        self.settings_providers.append(PowerSettings(self))
        self.settings_providers.append(VolumeSettings(self))
        try:
            self.settings_providers.append(BacklightSettings(self))
        except: #pylint: disable=bare-except
            print("Cannot register backlight control")
        for settings_provider in self.settings_providers:
            settings_provider.pack(side="top", expand=True)
            if settings_provider != self.settings_providers[-1]:
                self.separators.append(SettingsDivider(self))

    def is_scroll_needed(self):
        """
        Determine if the scrollbar element should be visible.
        """
        widget_heights = 0
        for settings_provider in self.settings_providers:
            #This is one of the few times we don't already know the hight of a given widget.
            widget_heights += settings_provider.winfo_reqheight()
        for separator in self.separators:
            widget_heights += separator.winfo_reqheight()
        if widget_heights > self['height']:
            self.scroll_needed = True
        else:
            self.scroll_needed = False

class SettingsFrame(ui_elements.LauncherFrame): #pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    The main SettingsFrame is a subclass of the AppFrame which holds a list of all the various user
    adjustable settings.
    """
    def __init__(self, parent, nav_widget_size, width, height):
        super().__init__(parent, nav_widget_size)
        self.configure(background="black", width=width,
                       height=height)
        self.update()
        self.settingslist = AllSettings(self.center)
        self.center.create_window(0, 0, window=self.settingslist, anchor="nw")
        self.settingsscroll = tkinter.ttk.Scrollbar(self.nav_right_trough,
                                                    style="arrowless.Vertical.TScrollbar",
                                                    orient='vertical',
                                                    command=self.center.yview)
        if self.settingslist.scroll_needed:
            self.settingsscroll.place(height=int(self.nav_right_trough['height']*0.8), width=8,
                                      relx=0.5, anchor="center", rely=0.5)
            self.update()
            self.center.config(yscrollcommand=self.settingsscroll.set,
                               scrollregion=(self.center.bbox("all")))
        self.update()
