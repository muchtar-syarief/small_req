import time

from uiautomator2 import Device, UiObject


class WidgetBehavior:
    driver: Device
    __app_package: str

    def __init__(self, driver: Device, app_package: str) -> None:
        self.driver = driver
        self.__app_package = app_package

    def back(self, count: int):
        for i in range(count):
            self.driver.press("back")
            time.sleep(1)
    
    def scroll(self) -> UiObject:
        scroll_selector = 'android.widget.ScrollView'
        scroll_element: UiObject = self.driver(className=scroll_selector)
        return scroll_element
    
    def close_app(self):
        self.driver.app_stop(self.__app_package)
        self.driver.press("home")
        self.driver.shell(["input", "keyevent", "KEYCODE_APP_SWITCH"])
        self.driver.shell(["input", "keyevent", "KEYCODE_DPAD_DOWN"])
        self.driver.shell(["input", "keyevent", "DEL"])
        self.driver.press("home")