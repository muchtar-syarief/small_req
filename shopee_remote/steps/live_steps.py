
from datetime import datetime, timedelta
from uiautomator2 import Device, UiObject
from uiautomator2.xpath import XPathSelector

from widget.widget_behavior import WidgetBehavior


class LiveSteps(WidgetBehavior):

    def __init__(self, driver: Device) -> None:
        super().__init__(driver, "com.shopee.com")


    def open_live(self, url: str) -> None:
        self.driver.open_url(url=url)

    def send_comment(self, comment: str) -> None:
        selector = "com.shopee.id.dfpluginshopee7:id/tv_send_message"
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=25)
        element.click()

        comment_selector = "android.widget.EditText"
        comment_el: UiObject = self.driver(className=comment_selector)
        comment_el.wait(timeout=25)
        if comment_el.exists:
            comment_el.send_keys(comment)
            self.driver.press("enter")

    def tap_love(self, duration: int = 5):
        selector = "com.shopee.id.dfpluginshopee7:id/iv_like"
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=25)
        if element.exists:

            end_time = datetime.utcnow() + timedelta(seconds=duration)
            while datetime.utcnow() < end_time:
                x, y = element.center()
                self.driver.double_click(x, y)

    def open_live_bucket(self) -> None:
        selector = "com.shopee.id.dfpluginshopee7:id/tv_product_num"
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=25)
        if element.exists:
            element.click()


    def add_to_bucket(self) -> None:
        selector = "//*[@text='Beli Sekarang']/../../.."
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=25)
        if element.exists:
            child = element.child("//android.view.ViewGroup")
            child.wait(timeout=25)
            child.click()


    