import adbutils
import uiautomator2 as ua2
import sys

from uiautomator2 import Device
from atx.atx import ATX

def open_driver() -> Device:
    adb = adbutils.adb
    device = adb.device()
    serial = device.serial

    driver = ua2.connect(serial)
    if getattr(sys, 'frozen', False):
        atx = ATX(driver=driver)
        atx.init_atx_app()
    return driver