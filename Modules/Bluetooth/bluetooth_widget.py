"""
The purpose of this module is to manage the bluetooth icon that appears in the menu bar.
"""

import tkinter
from threading import Thread
from multiprocessing import Value
import random
import time
from PIL import ImageTk, Image
import __main__

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
        self.bind('<<bluetooth_update>>', self.select_image)
        self.bluetooth_connect = Value('i', 0) #0=disconnected, 1=connected
        self.configure(image=self.status_images[random.choice(list(self.status_images))])
        self.bluetooth_thread = Thread(target=self.random_status, daemon=True)
        self.bluetooth_thread.start()
        self.update()

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
        if self.bluetooth_connect.value == 0:
            self.configure(image=self.status_images['disc'])
            return
        self.configure(image=self.status_images['conn'])
        return

    def random_status(self):
        """
        This is a dummy function that is only used to randomly switch the icon until I have
        a chance to hook up the DBus functions.
        """
        while 1:
            self.bluetooth_connect.value = random.randint(0, 1)
            self.event_generate('<<bluetooth_update>>')
            time.sleep(1)
