"""
The purpose of this module is to manage the wifi icon that appears in the menu bar.
"""

from threading import Thread
import tkinter
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
        self.configure(image=self.status_images[random.choice(list(self.status_images))])
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

    def random_status(self):
        """
        This is a dummy function to randomly change the icon before I have a chance to hook up the
        DBus bindings.
        """
        while 1:
            self.configure(image=self.status_images[random.choice(list(self.status_images))])
            time.sleep(1)
