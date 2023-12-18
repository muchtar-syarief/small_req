from uiautomator2 import Device

class Chrome:
    __app_package: str = "com.android.chrome"

    driver: Device

    def __init__(self, driver: Device) -> None:
        self.driver = driver

    def open_url(self, url: str):
        self.driver.open_url(url=url)

    @property
    def app_package(self) -> str:
        return self.__app_package

    