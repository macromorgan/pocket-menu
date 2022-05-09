"""
The purpose of this module is to manage the wifi icon that appears in the menu bar.
"""

import tkinter
from multiprocessing import Value
import dbus
from PIL import ImageTk, Image
import Modules.DBus.dbus_main as dbus_main
import __main__

def get_wifi_dev():
    """
    Get the first wifi device in the system.
    """
    proxy = dbus_main.DBUS_BUS.get_object('org.freedesktop.NetworkManager',
                                          '/org/freedesktop/NetworkManager')
    getmanager = dbus.Interface(proxy, 'org.freedesktop.NetworkManager')
    devices = getmanager.GetDevices()
    for device in devices:
        deviceobject = dbus_main.DBUS_BUS.get_object('org.freedesktop.NetworkManager', device)
        deviceinterface = dbus.Interface(deviceobject,
                                         dbus_interface='org.freedesktop.DBus.Properties')
        if deviceinterface.Get('org.freedesktop.NetworkManager.Device', 'DeviceType') == 2:
            return device
    return None

class WifiIcon(tkinter.Label): #pylint: disable=too-many-ancestors, too-many-instance-attributes
    """
    This is the main class for the wifi icon that gets displayed in the menubar.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.status_images = {}
        self.widget_size = self.parent['height']
        self.image_size = int(self.widget_size*0.8)
        self.configure(width=self.widget_size)
        self.configure(height=self.widget_size)
        self.configure(background=self.parent['background'])
        self.load_images()
        self.wifi_dev = get_wifi_dev()
        self.wifi_signal = Value('i', 100)
        self.wifi_status = Value('i', 1) #0=off, 1=connected, 2=disconnected
        self.wifi_connection = None
        self.get_active_wifi_connection()
        self.get_wifi_connection_strength()
        self.bind('<<wifi_update>>', self.select_image)
        self.select_image()
        dbus_main.DBUS_BUS.add_signal_receiver(self.dbus_signal_handler,
                                               bus_name='org.freedesktop.NetworkManager',
                                               dbus_interface='org.freedesktop.DBus.Properties',
                                               signal_name='PropertiesChanged',
                                               path=self.wifi_dev)
        dbus_main.DBUS_BUS.add_signal_receiver(self.dbus_signal_handler,
                                               bus_name='org.freedesktop.NetworkManager',
                                               dbus_interface='org.freedesktop.DBus.Properties',
                                               signal_name='PropertiesChanged',
                                               path=self.wifi_connection)
        self.update()

    def dbus_signal_handler(self, interface, data, signaltype): #pylint: disable=unused-argument
        """
        This is the main DBus callback that gets made whenever DBus signals a change to the wifi.
        """
        update = False
        if 'Strength' in data and int(data['Strength']) != self.wifi_signal.value:
            self.wifi_signal.value = int(data['Strength'])
            update = True
        if 'ActiveAccessPoint' in data and str(data['ActiveAccessPoint']) != self.wifi_connection:
            self.wifi_connection = str(data['ActiveAccessPoint'])
            update = True
        if update is True:
            self.event_generate('<<battery_update>>')
            update = False

    def get_active_wifi_connection(self):
        """
        Get the active wifi connection for the main wifi device.
        """
        proxy = dbus_main.DBUS_BUS.get_object('org.freedesktop.NetworkManager', self.wifi_dev)
        getmanager = dbus.Interface(proxy, dbus_interface='org.freedesktop.DBus.Properties')
        self.wifi_connection = str(getmanager.Get('org.freedesktop.NetworkManager.Device.Wireless',
                                                  'ActiveAccessPoint'))

    def get_wifi_connection_strength(self):
        """
        Get the wifi strength of the active wifi connection.
        """
        apobject = dbus_main.DBUS_BUS.get_object('org.freedesktop.NetworkManager',
                                                 self.wifi_connection)
        apinterface = dbus.Interface(apobject, dbus_interface='org.freedesktop.DBus.Properties')
        self.wifi_signal.value = int(apinterface.Get('org.freedesktop.NetworkManager.AccessPoint',
                                                     'Strength'))

    def load_images(self):
        """
        This function loads all the images necessary for the wifi status icon.
        """
        self.status_images['100'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Wifi/wifi_100.png").convert('RGBA').resize((self.image_size,
                                                                  self.image_size)))
        self.status_images['75'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Wifi/wifi_75.png").convert('RGBA').resize((self.image_size,
                                                                 self.image_size)))
        self.status_images['50'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Wifi/wifi_50.png").convert('RGBA').resize((self.image_size,
                                                                 self.image_size)))
        self.status_images['25'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Wifi/wifi_25.png").convert('RGBA').resize((self.image_size,
                                                                 self.image_size)))
        self.status_images['disc'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Wifi/wifi_disc.png").convert('RGBA').resize((self.image_size,
                                                                   self.image_size)))
        self.status_images['off'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Wifi/wifi_off.png").convert('RGBA').resize((self.image_size,
                                                                  self.image_size)))

    def select_image(self, event=None): #pylint: disable=unused-argument
        """
        This function is indirectly triggered by the DBus thread whenever there is a change to the
        wifi connection status or signal strength.
        """
        if self.wifi_status.value == 0:
            self.configure(image=self.status_images['off'])
            return
        if self.wifi_status.value == 2:
            self.configure(image=self.status_images['disc'])
            return
        if self.wifi_signal.value > 75:
            self.configure(image=self.status_images['100'])
            return
        if self.wifi_signal.value > 50:
            self.configure(image=self.status_images['75'])
            return
        if self.wifi_signal.value > 25:
            self.configure(image=self.status_images['50'])
            return
        self.configure(image=self.status_images['25'])
        return
