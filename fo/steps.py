import time

from uiautomator2 import Device
from uiautomator2._selector import UiObject
from uiautomator2.xpath import XPathSelector, XMLElement

from element import Element

class CheckingPaylaterError(Exception):
    pass

class Steps(Element):
    __app_package: str = "com.shopee.id"
    driver: Device

    def __init__(self, driver: Device) -> None:
        super().__init__(driver)

    @property
    def app_package(self) -> str:
        return self.__app_package

    def buy_now(self) -> None:
        buy_selector = '//*[@resource-id="buttonProductBuyNow"]'
        buy_element: XPathSelector = self.driver.xpath(buy_selector)
        buy_element.click()
    
    def check_submit_buy(self) -> bool:
        buy_selector = "buttonProductBuyNow"
        buy_element: XPathSelector = self.driver.xpath(buy_selector)
        buy_element.wait(timeout=2)
        if buy_element.exists:
            return True       

        self.back(3)
        return False
    
    def check_variant(self) -> bool:
        variant_selector = '//*[@resource-id="cartPanelTierVariation"]'
        element: XPathSelector = self.driver.xpath(variant_selector)
        element.wait(timeout=2)
        if element.exists:
            return True
        
        return False
    
    def all_variant_appear(self) -> bool:
        jumlah_selector = '//*[@text="Jumlah"]'
        jumlah_element: XPathSelector = self.driver.xpath(jumlah_selector)
        jumlah_element.wait(timeout=2)
        return jumlah_element.exists
    
    def scroll_variant(self) -> None:
        element: UiObject = self.driver(resourceId="sectionTierVariation")
        child = element.child(className="android.widget.ScrollView")
        child.scroll.to(text="Jumlah")

    def select_default_variant(self, start_from: int = 0) -> None:
        selector = 'cartPanelTierVariation'
        elements: UiObject = self.driver(resourceId=selector)

        btn_selector = "buttonOption_unselected"
        element: UiObject
        for ind, element in enumerate(elements):
            if ind < start_from:
                continue

            time.sleep(1)
            opts = element.child(resourceId=btn_selector)
            if opts.exists:
                if len(opts) > 8:
                    opts[-1].click()
                else:
                    opt: UiObject
                    for i, opt in enumerate(opts):
                        opt.click()
                        break

    def submit_buy(self) -> None:
        selector = '//*[@resource-id="buttonCartPanelSubmit"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        buy_btn: XMLElement = element.child("/android.view.ViewGroup")
        buy_btn.click()

    def check_checkout(self) -> bool:
        selector = '//*[@text="Checkout"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        if element.exists:
            return True
        return False
    
    def to_payment(self) -> None:
        payment_selector_id = "checkoutPaymentMethod"
        payment_selector = f'//*[@resource-id="{payment_selector_id}"]'
        payment_element: XPathSelector = self.driver.xpath(payment_selector)
        payment_element.wait(timeout=2)
        if payment_element.exists:
            payment_element.click()
            return
        
        element: UiObject = self.scroll()
        element.scroll.to(resourceId=payment_selector_id)
        
        return self.to_payment()
    
    def select_payment(self) -> None:
        transfer_bank = 'Transfer Bank'
        element: UiObject = self.driver(text=transfer_bank)
        element.wait(timeout=2)
        if element.exists:
            banks_selector = f'//*[@text="{transfer_bank}"]/../../../..'
            banks_element: XPathSelector = self.driver.xpath(banks_selector)
            banks_element.wait(timeout=3)
            if banks_element.exists:
                banks_element.click()
                return self.__select_payment()

        element: UiObject = self.scroll()
        element.scroll.to(text=transfer_bank)

        return self.select_payment()
    
    def __select_payment(self) -> None:
        selector = "Bank BCA"
        element: UiObject = self.driver(text=selector)
        element.wait(timeout=2)
        if element.exists:
            bank_selector = '//*[@text="Bank BCA"]/../../..'
            child: XPathSelector = self.driver.xpath(bank_selector)
            child.wait(timeout=2)
            if child.exists:
                child.click()
                return
        
        scroll_el: UiObject = self.scroll()
        scroll_el.scroll.to(text=selector)
        return self.__select_payment()
    
    def confirm_payment(self) -> None:
        selector = 'button_CONFIRM'
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=3)
        if element.exists:
            element.click()

    def check_has_unpaid_order(self):
        selector = '//*[@text="Lanjutkan Pembayaran"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=2)
        if element.exists:
            element.click()

    def check_set_payment_success(self) -> bool:
        selector = "//android.widget.TextView[contains(@text, 'Transfer Bank')]"
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        return element.exists
    
    def create_order(self) -> None:
        selector = '//*[@resource-id="buttonPlaceOrder"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=3)
        if element.exists: 
            element.click()

    def after_payment(self) -> None:
        selector = '//*[@text="OK"]/..'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)

        wait_payment_selector = '//*[@resource-id="labelOSPHeaderTitle"]'
        if element.exists:
            element.click()

            wait_payment: XPathSelector = self.driver.xpath(wait_payment_selector)
            wait_payment.wait(timeout=5)
            if wait_payment.exists:
                self.back(1)
                return

    def close_app(self) -> None:
        self.driver.app_stop(self.__app_package)
        self.driver.press("home")
        self.driver.shell(["input", "keyevent", "KEYCODE_APP_SWITCH"])
        self.driver.shell(["input", "keyevent", "KEYCODE_DPAD_DOWN"])
        self.driver.shell(["input", "keyevent", "DEL"])
        self.driver.press("home")
