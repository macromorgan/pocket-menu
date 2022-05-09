"""
The purpose of this module is to manage the bluetooth icon that appears in the menu bar.
"""

import tkinter
from multiprocessing import Value
import dbus
from PIL import ImageTk, Image
import Modules.DBus.dbus_main as dbus_main
import __main__

def get_bluetooth_device():
    """
    Function to get the first bluetooth device in the system.
    """
    proxy = dbus_main.DBUS_BUS.get_object('org.bluez', '/')
    get_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.ObjectManager')
    objects = get_manager.GetManagedObjects()
    for item in objects:
        if 'org.bluez.Adapter1' in objects[item]:
            return item
    return None

def get_bluetooth_state(power, connect, bt_device):
    """
    Function to get the current state of a bluetooth device.
    """
    try:
        proxy = dbus_main.DBUS_BUS.get_object('org.bluez', bt_device)
        get_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
        power.value = int(get_manager.Get('org.bluez.Adapter1', 'Powered'))
    except: #pylint: disable=bare-except
        power.value = 0
    try:
        proxy = dbus_main.DBUS_BUS.get_object('org.bluez', bt_device)
        get_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
        connect.value = int(get_manager.Get('org.bluez.Device1', 'Connected'))
    except: #pylint: disable=bare-except
        connect.value = 0

class BluetoothIcon(tkinter.Label): #pylint: disable=too-many-ancestors
    """
    The main class that manages drawing of the bluetooth icon.
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
        try:
            self.bt_device = get_bluetooth_device()
        except:
            raise ValueError('Bluetooth Not Present')
        self.bind('<<bluetooth_update>>', self.select_image)
        self.bluetooth_connect = Value('i', 0) #0=disconnected, 1=connected
        self.bluetooth_power = Value('i', 0) #0=off, 1=on
        get_bluetooth_state(self.bluetooth_connect, self.bluetooth_power, self.bt_device)
        self.select_image()
        dbus_main.DBUS_BUS.add_signal_receiver(self.dbus_signal_handler,
                                               bus_name='org.bluez',
                                               dbus_interface='org.freedesktop.DBus.Properties',
                                               signal_name='PropertiesChanged',
                                               path=self.bt_device)
        self.update()

    def dbus_signal_handler(self, interface, data, signaltype): #pylint: disable=unused-argument
        """
        This is the main DBus callback to process the signal when the bluetooth status changes.
        """
        update = False
        if 'Powered' in data and int(data['Powered']) != self.bluetooth_power.value:
            self.bluetooth_power.value = int(data['Powered'])
            update = True
        if 'Connected' in data and int(data['Connected']) != self.bluetooth_connect.value:
            self.bluetooth_connect.value = int(data['Connected'])
            update = True
        if update is True:
            self.event_generate('<<bluetooth_update>>')
            update = False

    def load_images(self):
        """
        This function manages the loading of the bluetooth icon images.
        """
        self.status_images['conn'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Bluetooth/bluetooth_conn.png").convert('RGBA').resize((self.image_size,
                                                                             self.image_size)))
        self.status_images['disc'] = ImageTk.PhotoImage(Image.open(__main__.DIR_PATH + \
            "/Modules/Bluetooth/bluetooth_disc.png").convert('RGBA').resize((self.image_size,
                                                                             self.image_size)))

    def select_image(self, event=None): #pylint: disable=unused-argument
        """
        This function is indirectly triggered by the DBus thread whenever there is a change to the
        bluetooth connection status.
        """
        if self.bluetooth_connect.value == 1 and self.bluetooth_power.value == 1:
            self.configure(image=self.status_images['conn'])
            return
        self.configure(image=self.status_images['disc'])
        return
