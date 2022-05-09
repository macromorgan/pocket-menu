"""
This module is supposed to contain the main DBus loop as well as start running a separate thread
for the main DBus loop once loaded. All consumers of DBus will reference this module to speak to
the main DBus thread.
"""
from threading import Thread
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from gi.repository import GObject

try:
    DBusGMainLoop(set_as_default=True)
    GObject.threads_init()
    dbus.mainloop.glib.threads_init()
    DBUS_LOOP = DBusGMainLoop()
    DBUS_BUS = dbus.SystemBus(mainloop=DBUS_LOOP)
    MAINLOOP = GLib.MainLoop()
    DBUS_THREAD = Thread(target=MAINLOOP.run, daemon=True)
    DBUS_THREAD.start()
except: #pylint: disable=bare-except
    print("Error Loading DBus, functionality will be reduced!")
