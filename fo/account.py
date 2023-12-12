import time

from uiautomator2 import Device
from uiautomator2._selector import UiObject
from uiautomator2.xpath import XPathSelector

from element import Element


class Account(Element):

    def __init__(self, driver: Device):
        super().__init__(driver=driver)

    def to_account(self) -> None:
        selector = '//*[@content-desc="tab_bar_button_me"]/../..'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=2)
        element.click()

    def to_setting(self) -> None:
        selector = '//*[@resource-id="buttonAccountSettings"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=10)
        if element.exists:
            element.click()
            return
    
    def to_switch_account(self) -> None:
        selector = 'com.shopee.id:id/btnSwitchAccount'
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=2)
        if element.exists:
            element.click()
            return

        scroll_el = self.scroll()
        scroll_el.scroll.to(resourceId=selector)

        return self.to_switch_account()
    
    def check_active_all(self) -> bool:
        selector = 'com.shopee.id:id/container_layout'
        elements: UiObject = self.driver(resourceId=selector)
        elements.wait(timeout=3)

        if elements.exists:
            content_selector = 'com.shopee.id:id/tv_current'
            
            element: UiObject
            for i, element in enumerate(elements):
                current_account: UiObject = element.child(resourceId=content_selector)
                current_account.wait(timeout=3)

                if current_account.exists:
                    #  check last account is active 
                    if i == (len(elements)-1)-1:
                        return True
                    else: 
                        continue
                else:
                    if i == len(elements)-1:
                        return False
    
    def switch_account(self) -> None:        
        selector = 'com.shopee.id:id/container_layout'
        elements: UiObject = self.driver(resourceId=selector)
        elements.wait(timeout=3)

        if self.check_active_all():
            elements.click()
            return

        if elements.exists:
            content_selector = 'com.shopee.id:id/tv_current'
            
            element: UiObject
            for i, element in enumerate(elements):
                current_account: UiObject = element.child(resourceId=content_selector)
                current_account.wait(timeout=3)

                if current_account.exists:
                    contents: UiObject = current_account.child(className='android.widget.TextView')


                    # if i != len(elements)-1:
                    #     next = i+1
                    #     element[next].click()
                    #     return
                    # else:
                    #     elements.click()
                    #     return