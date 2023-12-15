from uiautomator2 import Device
from uiautomator2.xpath import XPathSelector
from uiautomator2._selector import UiObject

from element import Element

class Product:
    name: str = ""
    url: str = ""
    tujuan: str = ""
    bank: str = "Bank BCA"
    virtual_account: str = ""
    nominal: str = ""

class ProductSteps(Element):

    def __init__(self, driver: Device) -> None:
        super().__init__(driver)
        
    def set_product_name(self) -> str:
        selector = '//*[@resource-id="labelProductPageProductName"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=30)
        product_title = element.get_text()
        return product_title
    
    def set_address_info(self) -> str:
        selector = '//*[@resource-id="labelDeliveryAddressInfo"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        address: str = element.get_text()
        self.tujuan = address
        return address.encode("unicode_escape").decode()
    
    def set_price_count(self) -> str:
        total_payment = "labelTotalPaymentPrice"
        selector = f'//*[@resource-id="{total_payment}"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=2)
        if element.exists:
            price_count = element.get_text()
            return price_count
        
        scroll_el: UiObject = self.scroll()
        scroll_el.scroll.toEnd()

        return self.set_price_count()
    
    def set_virtual_account(self) -> str:
        selector = '//*[@text="Bank BCA"]/..'
        elements: XPathSelector = self.driver.xpath(selector)
        elements.wait(timeout=15)

        child_selector = '/android.view.ViewGroup[1]/android.widget.TextView[2]'
        if elements.exists:
            va = elements.child(child_selector)
            return va.get_text()
        
