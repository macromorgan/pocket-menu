"""
The purpose of this module is to manage drawing the menubar widget for the wireless icon.
"""

import tkinter
from threading import Thread
import random
import time
from PIL import ImageTk, Image
import __main__

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
        self.configure(image=self.status_images[random.choice(list(self.status_images))])
        self.battery_thread = Thread(target=self.random_status, daemon=True)
        self.battery_thread.start()
        self.update()

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

    def random_status(self):
        """
        This is just a dummy function to keep updating the image before I have a chance to
        implement proper DBus bindings.
        """
        while 1:
            self.configure(image=self.status_images[random.choice(list(self.status_images))])
            time.sleep(1)
