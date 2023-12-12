import time

from uiautomator2 import Device
from uiautomator2._selector import UiObject


class Element:
    driver: Device

    
    def __init__(self, driver: Device) -> None:
        self.driver = driver

    def back(self, count: int):
        for i in range(count):
            self.driver.press("back")
            time.sleep(1)

    def scroll(self) -> UiObject:
        scroll_selector = 'android.widget.ScrollView'
        scroll_element: UiObject = self.driver(className=scroll_selector)
        return scroll_element