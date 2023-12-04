import time

from uiautomator2 import Device
from uiautomator2._selector import UiObject
from uiautomator2.xpath import XPathSelector, XMLElement

class Steps:
    __app_package: str = "com.shopee.id"
    driver: Device

    def __init__(self, driver: Device) -> None:
        self.driver = driver

    @property
    def app_package(self):
        return self.__app_package

    def open_app(self):
        self.driver.app_start(self.app_package, use_monkey=True)
        time.sleep(2)
        search_element: XPathSelector = self.driver.xpath('//*[@resource-id="com.shopee.id:id/text_container"]')
        search_element.click()

    def to_search_shop(self, shop_init: str) -> bool:
        self.input_element(shop_init)
        self.driver.press("enter")

        selector = "Toko Lainnya"
        element = self.driver(text=selector)
        element.wait(timeout=5)
        if element.exists:
            element.click()
            return True
        
        self.driver.press("back")
        return False
    
    def back(self, count: int):
        for i in range(count):
            self.driver.press("back")
            time.sleep(1)

        # search_selector = "android.widget.EditText"
        # search_element = self.driver(className=search_selector)
        # search_element.wait(timeout=1)
        # if search_element.exists:
        #     return
        
        # self.driver.press("back")
        # return self.back_until_search_shop()
    
    
    def input_element(self, input: str):
        search_selector = "android.widget.EditText"
        search_element = self.driver(className=search_selector)
        search_element.clear_text()
        search_element.send_keys(input)


    def search_shop(self, shop: str):
        self.input_element(shop)
        self.driver.press("back")

        username_selector = "//android.widget.TextView[contains(@resource-id, 'labelUserName')]"
        username_elements: XPathSelector = self.driver.xpath(username_selector)
        username_elements.wait(timeout=3)
        username_elements: list[XMLElement] = username_elements.all()

        for username in username_elements:
            if username.text == shop:
                parent = username.parent()
                parent.click()
                return True
            
        return False

        # selector = f"//android.widget.TextView[@text='{shop}']/.."
        # elements: XPathSelector = self.driver.xpath(selector)
        # elements.wait(timeout=3)
        # all_element: list[XMLElement] = elements.all()
        # for element in all_element:
        #     element.click()
        #     return True
        
        # return False

    def get_shop_product(self):
        product_selector = '//*[@content-desc="shop_page_product_tab"]'
        product_btn: XPathSelector = self.driver.xpath(product_selector)
        product_btn.wait(timeout=5)
        product_btn.click()

        selector = '//*[@resource-id="buttonSearchResultPagePrice"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        element.click()
        
        time.sleep(1)
        product_price_selector = '//*[@resource-id="labelItemCardDiscPrice"]/../..'
        product_element: XPathSelector = self.driver.xpath(product_price_selector)
        product_element.wait(timeout=10)
        product_element.click()


    def check_submit_buy(self):
        buy_selector = "buttonProductBuyNow"
        buy_element: XPathSelector = self.driver.xpath(buy_selector)
        buy_element.wait(timeout=5)
        if buy_element.exists:
            return True       

        self.back(3)
        return False

    def check_variation(self) -> bool:
        variation_selector = "sectionTierVariation"
        variation_element: XPathSelector = self.driver.xpath(variation_selector)
        variation_element.wait(timeout=2)
        if variation_element.exists:
            return True
        return False

    def select_payment(self) -> None:
        payment_selector_id = "checkoutPaymentMethod"
        payment_selector = f'//*[@resource-id="{payment_selector_id}"]'
        payment_element: XPathSelector = self.driver.xpath(payment_selector)
        payment_element.wait(timeout=2)
        if payment_element.exists:
            payment_element.click()
            return

        scroll_selector = 'android.widget.ScrollView'
        scroll_element: UiObject = self.driver(className=scroll_selector)
        scroll_element.scroll.to(resourceId=payment_selector_id)
        
        return self.select_payment()

    
    def buy_now(self) -> None:
        buy_selector = '//*[@resource-id="buttonProductBuyNow"]'
        buy_element: XPathSelector = self.driver.xpath(buy_selector)
        buy_element.click()
    
    def check_variant(self) -> bool:
        variant_selector = '//*[@resource-id="sectionTierVariation"]'
        element: XPathSelector = self.driver.xpath(variant_selector)
        element.wait(timeout=2)
        if element.exists:
            return True
        
        return False

    def select_default_variant(self) -> None:
        jumlah_selector = '//*[@text="Jumlah"]'
        jumlah_element: XPathSelector = self.driver.xpath(jumlah_selector)
        jumlah_element.wait(timeout=2)
        if not jumlah_element.exists:
            element: UiObject = self.driver(resourceId="sectionTierVariation")
            child = element.child(className="android.widget.ScrollView")
            child.scroll.to(text="Jumlah")

        time.sleep(1)
        selector = 'cartPanelTierVariation'
        elements: UiObject = self.driver(resourceId=selector)

        btn_selector = "buttonOption_unselected"
        element: UiObject
        for ind, element in enumerate(elements):
            time.sleep(1)
            opts = element.child(resourceId=btn_selector)
            if opts.exists:
                if len(opts) >= 8:
                    opts[-1].click()
                else:
                    opt: UiObject
                    for i, opt in enumerate(opts):
                        opt.click()
                        break

    def submit_buy(self):
        selector = '//*[@resource-id="buttonCartPanelSubmit"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        buy_btn: XMLElement = element.child("/android.view.ViewGroup")
        buy_btn.click()

    def check_checkout(self):
        selector = '//*[@text="Checkout"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        if element.exists:
            return True
        return False

            
    def is_use_paylater(self) -> bool:
        spl_active_selector = '//*[@resource-id="imageCheck"]'

        spl_selector = "//android.widget.TextView[contains(@text, 'SPayLater')]/.."
        spl_element: XPathSelector = self.driver.xpath(spl_selector)
        spl_element.wait(timeout=3)

        spl_active_element = spl_element.child(spl_active_selector)
        spl_active_element.wait(2)
        if spl_active_element.exists:
            self.back(4)
            return True
        
        self.back(4)
        return False


    def close_app(self):
        self.driver.app_stop(self.__app_package)
        self.driver.press("home")
        self.driver.shell(["input", "keyevent", "KEYCODE_APP_SWITCH"])
        self.driver.shell(["input", "keyevent", "KEYCODE_DPAD_DOWN"])
        self.driver.shell(["input", "keyevent", "DEL"])
        self.driver.press("home")
