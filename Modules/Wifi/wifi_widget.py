"""
The purpose of this module is to manage the wifi icon that appears in the menu bar.
"""

import tkinter
from threading import Thread
from multiprocessing import Value
import random
import time
from PIL import ImageTk, Image
import __main__

class WifiIcon(tkinter.Label): #pylint: disable=too-many-ancestors
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
        self.wifi_signal = Value('i', 100)
        self.wifi_status = Value('i', 1) #0=off, 1=connected, 2=disconnected
        self.bind('<<wifi_update>>', self.select_image)
        self.select_image()
        self.wifi_thread = Thread(target=self.random_status, daemon=True)
        self.wifi_thread.start()
        self.update()

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

    def random_status(self):
        """
        This is a dummy function to randomly change the icon before I have a chance to hook up the
        DBus bindings.
        """
        while 1:
            self.wifi_status.value = random.randint(0, 2)
            self.wifi_signal.value = random.randint(1, 100)
            self.event_generate('<<wifi_update>>')
            time.sleep(1)
