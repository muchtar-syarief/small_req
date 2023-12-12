from uiautomator2 import Device
from uiautomator2.xpath import XPathSelector
from uiautomator2._selector import UiObject

from element import Element

class Product(Element):
    akun: str
    produk: str
    url: str
    tujuan: str
    bank: str = "Bank BCA"
    virtual_account: str
    nominal: str


    def __init__(self, driver: Device) -> None:
        super().__init__(driver)
        
    def set_product_name(self) -> str:
        selector = '//*[@resource-id="labelProductPageProductName"]'
        element: XPathSelector = self.driver.xpath(selector)
        product_title = element.get_text()
        self.produk = product_title
        return product_title
    
    def set_address_info(self) -> str:
        selector = '//*[@resource-id="labelDeliveryAddressInfo"]'
        element: XPathSelector = self.driver.xpath(selector)
        address = element.get_text()
        self.tujuan = address
        return address
    
    def set_price_count(self) -> str:
        total_payment = "labelTotalPaymentPrice"
        selector = f'//*[@resource-id="{total_payment}"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=2)
        if element.exists:
            price_count = element.get_text()
            self.nominal = price_count
            return price_count
        
        scroll_el: UiObject = self.scroll()
        scroll_el.scroll.to(resourceId=total_payment)

        return self.set_price_count()
    
    def set_url(self, url: str):
        self.url = url
        return self.url
    
    def set_virtual_account(self):
        selector = '//*[@text="Bank BCA"]/..'
        elements: XPathSelector = self.driver.xpath(selector)
        elements.wait(timeout=15)

        child_selector = '/android.view.ViewGroup[1]/android.widget.TextView[2]'
        if elements.exists:
            va = elements.child(child_selector)
            self.virtual_account = va.get_text()
            return self.virtual_account
        
    def set_account(self):
        selector = '//*[@resource-id="labelUserName"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=10)
        if element.exists:
            username = element.get_text()
            self.akun = username
            return self.akun
        