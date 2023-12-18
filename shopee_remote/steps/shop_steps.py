import time

from uiautomator2 import Device
from uiautomator2._selector import UiObject
from uiautomator2.xpath import XPathSelector, XMLElement
from retry import retry
from ..widget.widget_behavior import WidgetBehavior

class SelectVariantError(Exception):
    pass

class SortProductPriceError(Exception):
    pass

class CheckingPaylaterError(Exception):
    pass

class ShopSteps(WidgetBehavior):

    def __init__(self, driver: Device) -> None:
        super().__init__(driver, "com.shopee.id")

    @property
    def app_package(self):
        return self.__app_package

    def open_app(self):
        self.driver.app_start(self.app_package, use_monkey=True)
    
    def tap_search_bar(self) -> None:
        search_element: XPathSelector = self.driver.xpath('//*[@resource-id="com.shopee.id:id/text_container"]')
        search_element.wait(timeout=10)
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


    @retry(exceptions=SortProductPriceError, tries=3, delay=0.5)
    def get_shop_product(self):
        product_selector = '//*[@content-desc="shop_page_product_tab"]'
        product_btn: XPathSelector = self.driver.xpath(product_selector)
        product_btn.wait(timeout=5)
        product_btn.click()

        selector = '//*[@resource-id="buttonSearchResultPagePrice"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        if not element.exists: 
            raise SortProductPriceError("Sort product price element not found")
        else:
            element.click()
        
        time.sleep(1)
        product_price_selector = '//*[@resource-id="labelItemCardDiscPrice"]/../..'
        product_element: XPathSelector = self.driver.xpath(product_price_selector)
        product_element.wait(timeout=10)
        product_element.click()


    def is_shop_off(self):
        variation_element: UiObject = self.driver(resourceId="sectionTierVariation")
        variation_element.wait(timeout=5)
        if variation_element.exists:
            return False
        
        return True

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
        
        time.sleep(0.5)
        return self.select_payment()

    
    def buy_now(self) -> None:
        buy_selector = '//*[@resource-id="buttonProductBuyNow"]'
        buy_element: XPathSelector = self.driver.xpath(buy_selector)
        buy_element.wait(timeout=5)
        if buy_element.exists:
            time.sleep(0.25)
            buy_element.click()
    
    def check_variant(self) -> bool:    
        variant_selector = '//*[@resource-id="cartPanelTierVariation"]'
        element: XPathSelector = self.driver.xpath(variant_selector)
        element.wait(timeout=5)
        if element.exists:
            return True
        return False
    
    def all_variant_appear(self) -> bool:
        jumlah_selector = '//*[@text="Jumlah"]'
        jumlah_element: XPathSelector = self.driver.xpath(jumlah_selector)
        jumlah_element.wait(timeout=2)
        return jumlah_element.exists
    
    def scroll_variant(self):
        element: UiObject = self.driver(resourceId="sectionTierVariation")
        child = element.child(className="android.widget.ScrollView")
        child.scroll.to(text="Jumlah")

    def select_default_variant(self, start_from: int = 0) -> None:
        if start_from >= 2:
            return

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
                start_from += 1
        
        if self.all_variant_appear():
            return

        self.scroll_variant()
        return self.select_default_variant(start_from=start_from)

    def select_variant_alternative(self):
        time.sleep(1)
        self.driver.xpath('//*[@resource-id="cartPanelTierVariation"]/android.view.ViewGroup[1]').click()
        self.driver.xpath('//*[@text="Beli Sekarang"]').click()
        time.sleep(1)
        try:
            self.driver.xpath('//*[@resource-id="sectionTierVariation"]/android.widget.ScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click(timeout=2)
            self.driver.xpath('//*[@text="Beli Sekarang"]').click()
        except:
            pass


    def submit_buy(self):
        selector = '//*[@resource-id="buttonCartPanelSubmit"]/android.view.ViewGroup'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        element.click()

    def check_checkout(self):
        selector = '//*[@text="Checkout"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        if element.exists:
            return True
        return False

    @retry(exceptions=CheckingPaylaterError, tries=3, delay=0.5)
    def is_use_paylater(self) -> bool:
        spl_selector = "//android.widget.TextView[contains(@text, 'SPayLater')]/../../../../../.."
        spl_element: XPathSelector = self.driver.xpath(spl_selector)
        spl_element.wait(timeout=20)
        if spl_element.exists:

            spl_monthly_selector = '//*[@resource-id="buttonExpandedOption"]'
            spl_active_element: XPathSelector = spl_element.child(spl_monthly_selector)
            spl_active_element.wait(timeout=3)
            if spl_active_element.exists:
                return True
            
            return False
        
        raise CheckingPaylaterError("checking pay later error")


