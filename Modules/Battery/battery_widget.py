"""
The purpose of this module is to manage drawing the menubar widget for the wireless icon.
"""

import tkinter
from multiprocessing import Value
import dbus
from PIL import ImageTk, Image
import Modules.DBus.dbus_main as dbus_main
import __main__

def check_battery():
    """
    This function is to check for the presense of a battery and return true if one is found. This
    function runs outside of the class because that seemed to interfere with the threading.
    """
    proxy = dbus_main.DBUS_BUS.get_object('org.freedesktop.UPower',
                                          '/org/freedesktop/UPower/devices/DisplayDevice')
    powerdev = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
    return bool(powerdev.Get('org.freedesktop.UPower.Device', 'IsPresent'))

def get_battery_details(charging, capacity):
    """
    This function is to check the battery capacity and charge state on initial widget load. Like
    the function above it this was excluded from the class because it interfered with the
    threading of the dbus mainloop function.
    """
    proxy = dbus_main.DBUS_BUS.get_object('org.freedesktop.UPower',
                                          '/org/freedesktop/UPower/devices/DisplayDevice')
    getmanager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
    update_battery = False
    try:
        new_capacity = int(getmanager.Get('org.freedesktop.UPower.Device', 'Percentage'))
        if new_capacity != capacity.value:
            capacity.value = new_capacity
            update_battery = True
        new_status = int(getmanager.Get('org.freedesktop.UPower.Device', 'State'))
        if new_status != charging.value:
            charging.value = new_status
            update_battery = True
    except: #pylint: disable=bare-except
        print("Error reading battery")
    if update_battery is True:
        update_battery = False

class BatteryIcon(tkinter.Label): #pylint: disable=too-many-ancestors
    """
    This is the class for handling the battery icon. It loads all the images and cycles through
    which ones to display based on the battery level.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.status_images = {}
        self.widget_size = self.parent['height']
        self.image_size = int(self.widget_size*0.8)
        self.configure(width=self.widget_size)
        self.configure(height=self.widget_size)
        self.configure(background=parent['background'])
        self.load_images()
        self.battery_capacity = Value('i', 100)
        self.battery_charging = Value('i', 1)
        self.present = check_battery()
        if self.present is True:
            get_battery_details(self.battery_charging, self.battery_capacity)
            self.bind('<<battery_update>>', self.select_image)
            self.select_image()
            dbus_main.DBUS_BUS.add_signal_receiver(self.dbus_signal_handler,
                                                   bus_name='org.freedesktop.UPower',
                                                   dbus_interface=\
                                                   'org.freedesktop.DBus.Properties',
                                                   signal_name='PropertiesChanged',
                                                   path=\
                                                   '/org/freedesktop/UPower/devices/DisplayDevice')
        else:
            raise ValueError('Battery Not Present')
        self.update()

    def dbus_signal_handler(self, interface, data, signaltype): #pylint: disable=unused-argument
        """
        This is the callback for handling signals returned from DBus to get the updated battery
        status.
        """
        update = False
        if 'State' in data and int(data['State']) != self.battery_charging.value:
            self.battery_charging.value = int(data['State'])
            update = True
        if 'Percentage' in data and int(data['Percentage']) != self.battery_capacity.value:
            self.battery_capacity.value = int(data['Percentage'])
            update = True
        if update is True:
            self.event_generate('<<battery_update>>')
            update = False

    def load_images(self):
        """
        Load the actual images and save them to the class so we don't have to keep loading them.
        """
        self.status_images['100'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Battery/battery_100.png").convert('RGBA').resize((self.image_size,
                                                                        self.image_size)))
        self.status_images['75'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Battery/battery_75.png").convert('RGBA').resize((self.image_size,
                                                                       self.image_size)))
        self.status_images['50'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Battery/battery_50.png").convert('RGBA').resize((self.image_size,
                                                                       self.image_size)))
        self.status_images['25'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Battery/battery_25.png").convert('RGBA').resize((self.image_size,
                                                                       self.image_size)))
        self.status_images['10'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Battery/battery_10.png").convert('RGBA').resize((self.image_size,
                                                                       self.image_size)))
        self.status_images['charge'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Battery/battery_charge.png").convert('RGBA').resize((self.image_size,
                                                                           self.image_size)))

    def select_image(self, event=None): #pylint: disable=unused-argument
        """
        This function is indirectly triggered by the DBus thread whenever there is a change to the
        battery charging status or capacity detected.
        """
        if self.battery_charging.value == 1:
            self.configure(image=self.status_images['charge'])
            return
        if self.battery_capacity.value > 75:
            self.configure(image=self.status_images['100'])
            return
        if self.battery_capacity.value > 50:
            self.configure(image=self.status_images['75'])
            return
        if self.battery_capacity.value > 25:
            self.configure(image=self.status_images['50'])
            return
        if self.battery_capacity.value > 10:
            self.configure(image=self.status_images['25'])
            return
        self.configure(image=self.status_images['10'])
        return
