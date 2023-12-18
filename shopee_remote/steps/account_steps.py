
from retry import retry
from uiautomator2 import Device
from uiautomator2._selector import UiObject
from uiautomator2.xpath import XPathSelector, XMLElement

from widget.widget_behavior import WidgetBehavior


class SwitchingAccountError(Exception):
    pass

class MainAddressError(Exception):
    pass


class Account:
    name: str = ""
    main_address: str = ""
    addresses: list[str] = []
    last_selected: str = ""

    def next_selected_address(self) -> str:
        if len(self.addresses) == 1:
            return self.addresses[0]
        
        for ind, address in enumerate(self.addresses):
            if address == self.last_selected:
                if ind != len(self.addresses)-1:
                    next = ind+1
                    return self.addresses[next]
                return self.addresses[0]
            
    def set_last_selected(self, data: str) -> None:
        selected = data.split("|")[0]
        self.last_selected = selected.strip()

class AccountSteps(WidgetBehavior):

    def __init__(self, driver: Device):
        super().__init__(driver=driver, app_package="com.shopee.id")

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
            content_selector = 'com.shopee.id:id/img_current'
            
            element: UiObject
            for i, element in enumerate(elements):
                current_account: UiObject = element.child(resourceId=content_selector)
                current_account.wait(timeout=2)

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
        selector = 'com.shopee.id:id/rv_account_list'
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=15)
        if not element.exists:
            raise NotImplementedError

        selector = 'com.shopee.id:id/container_layout'
        elements: UiObject = self.driver(resourceId=selector)
        elements.wait(timeout=3)

        active_all = self.check_active_all()
        if active_all:
            elements.click()
            return

        if elements.exists:
            content_selector = "com.shopee.id:id/img_current"
            
            element: UiObject
            for i, element in enumerate(elements):
                current_account: UiObject = element.child(resourceId=content_selector)
                current_account.wait(timeout=3)

                if current_account.exists:
                    next = i+1
                    next_account: UiObject = elements[next].child(resourceId=content_selector)
                    next_account.wait(timeout=3)
                    if not next_account.exists:
                        elements[next].click()
                        break
    
    def is_success_switching(self) -> bool:
        selector = 'sectionMeHeader'
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=20)
        return element.exists
    
    @retry(exceptions=SwitchingAccountError, tries=3, delay=0.5)
    def switching_account(self):
        self.switch_account()
        if not self.is_success_switching():
            raise SwitchingAccountError("switching account failed")
    
    def get_account(self) -> str:
        selector = '//*[@resource-id="labelUserName"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=10)
        if element.exists:
            username = element.get_text()
            return username
        
    def get_account_addresses(self) -> list[str]:
        selector = "//android.view.ViewGroup[contains(@resource-id, 'addressRow')]"
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=10)
        addresses_el: list[XMLElement] = element.all()

        addresses: list[str] = []
        for address in addresses_el:
            id: str = address.attrib.get("resource-id")
            address_name = id.split("_")[-1]
            addresses.append(address_name)

        return addresses