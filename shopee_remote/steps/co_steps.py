import time

from uiautomator2 import Device
from uiautomator2._selector import UiObject
from uiautomator2.xpath import XPathSelector, XMLElement

from widget.widget_behavior import WidgetBehavior

class CheckingPaylaterError(Exception):
    pass


class SelectVariantError(Exception):
    pass

class LimitCheckoutError(Exception):
    pass

class AccountLimiTCheckOutError(Exception):
    pass

class CoSteps(WidgetBehavior):

    def __init__(self, driver: Device) -> None:
        super().__init__(driver, "com.shopee.id")
    
    def buy_now(self) -> None:
        buy_selector = '//*[@resource-id="buttonProductBuyNow"]'
        buy_element: XPathSelector = self.driver.xpath(buy_selector)
        buy_element.wait(timeout=5)
        if buy_element.exists:
            time.sleep(0.25)
            buy_element.click()

    def is_shop_off(self):
        variation_element: UiObject = self.driver(resourceId="sectionTierVariation")
        variation_element.wait(timeout=5)
        if variation_element.exists:
            return False
        
        return True
    
    def check_variant(self) -> bool:
        variant_selector = '//*[@resource-id="cartPanelTierVariation"]'
        element: XPathSelector = self.driver.xpath(variant_selector)
        element.wait(timeout=5)
        return element.exists
    
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
        # first variant
        btn_variant_selector = '//*[@resource-id="buttonOption_unselected"]'

        ele: XPathSelector = self.driver.xpath('//*[@resource-id="cartPanelTierVariation"]')
        child = ele.child(btn_variant_selector)
        child.click()

        self.submit_buy()
        try:
            element: XPathSelector = self.driver.xpath('//*[@resource-id="sectionTierVariation"]/android.widget.ScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup[1]')
            child: XPathSelector = element.child(btn_variant_selector)
            child.click(timeout=2)
            self.submit_buy()
        except:
            pass

    def submit_buy(self):
        selector = '//*[@resource-id="buttonCartPanelSubmit"]/android.view.ViewGroup'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        element.click()

    def check_checkout(self) -> bool:
        selector = '//*[@text="Checkout"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        if element.exists:
            return True
        return False
    
    def to_address_setting(self) -> None:
        time.sleep(0.5)
        selector = "checkoutAddress"
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=10)
        if element.exists:
            element.click()
            return

        scroll_el = self.scroll()
        scroll_el.scroll.to(resourceId=selector)
        return self.to_address_setting()

    def select_address(self, last_tujuan_state: str = "") -> None:
        last_tujuan = last_tujuan_state.split("|")[0]
        last_tujuan = last_tujuan.strip()
        time.sleep(2)

        selector = "//android.view.ViewGroup[contains(@resource-id, 'addressRow')]"
        elements: XPathSelector = self.driver.xpath(selector)
        elements.wait(timeout=5)
        addresses: list[XMLElement] = elements.all()

        last_selected = "_".join(["addressRow", last_tujuan])
        for ind, address in enumerate(addresses):
            id = address.attrib.get("resource-id")
            if id == last_selected:
                if ind != len(addresses)-1:
                    next = ind+1
                    addresses[next].click()
                    return
                else:
                    addresses[0].click()
                    return
                
    def select_shipping_address(self, address: str):
        selector = "_".join(["addressRow", address])
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=10)
        if element.exists:
            element.click()
                
    def is_address_changed(self, address: str = ""):
        selector = f"//android.widget.TextView[contains(@text, '{address}')]"
        element: XPathSelector = self.driver.xpath(selector)
        return element.wait_gone(timeout=5)

    def to_payment(self) -> None:
        payment_selector_id = "checkoutPaymentMethod"
        payment_selector = f'//*[@resource-id="{payment_selector_id}"]'
        payment_element: XPathSelector = self.driver.xpath(payment_selector)
        payment_element.wait(timeout=2)
        if payment_element.exists:
            payment_element.click()
            return
        
        time.sleep(0.25)
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

        time.sleep(0.5)
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

    def check_has_unpaid_order(self) -> None:
        selector = '//*[@text="Lanjutkan Pembayaran"]'
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=2)
        if element.exists:
            element.click()

    def confirm_change_payment(self) -> None:
        selector = 'com.shopee.id:id/buttonDefaultPositive'
        element: UiObject = self.driver(resourceId=selector)
        element.wait(timeout=3)
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

    def check_valid_voucher(self) -> None:
        selector = "//android.widget.TextView[contains(@text, 'Kamu telah menggunakan promo ini')]"
        elem: UiObject = self.driver.xpath(selector)
        elem.wait(timeout=5)
        if elem.exists:
            el = self.driver(resourceId="com.shopee.id:id/buttonDefaultNegative")
            el.click()
            return False
        return True
    
    def limit_checkout(self) -> None:
        selector = "//android.widget.TextView[contains(@text, 'M10')]"
        elem: UiObject = self.driver.xpath(selector)
        elem.wait(timeout=5)
        if elem.exists:
            el = self.driver(resourceId="com.shopee.id:id/buttonDefaultNegative")
            el.click()
            return True
        return False
    
    def to_voucher(self) -> None:
        selector = "buttonCartPageUseVoucher"
        elem: UiObject = self.driver(resourceId=selector)
        elem.wait(timeout=2)
        if elem.exists:
            elem.click()
            return
        
        scroll_el = self.scroll()
        scroll_el.scroll.to(resourceId=selector)
        return self.to_voucher()
    
    def deactive_voucher(self) -> None:
        selector = "//android.widget.ImageView[contains(@resource-id, 'radioBtnVoucher')]/.."
        element: XPathSelector = self.driver.xpath(selector)
        element.wait(timeout=5)
        if element.exists:
            element.click()

    def select_voucher(self) -> None:
        selector = "btnOkVoucherSelectionSubmitSection"
        element: UiObject = self.driver(resourceId=selector)
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

    def restart_airplane_mode(self):
        self.driver.open_quick_settings()
        time.sleep(3)
        self.driver.shell(["cmd", "connectivity", "airplane-mode", "enable"])
        time.sleep(7)
        self.driver.shell(["cmd", "connectivity", "airplane-mode", "disable"])
        self.back(2)
        time.sleep(5)

    def close_app(self) -> None:
        self.driver.app_stop(self.__app_package)
        self.driver.press("home")
        self.driver.shell(["input", "keyevent", "KEYCODE_APP_SWITCH"])
        self.driver.shell(["input", "keyevent", "KEYCODE_DPAD_DOWN"])
        self.driver.shell(["input", "keyevent", "DEL"])
        self.driver.press("home")
