import adbutils
import uiautomator2 as ua2
import time

from uiautomator2 import Device

from steps import Steps, SelectVariantError
from product_info import Product, ProductSteps
from account import Account, AccountSteps, SwitchingAccountError

def open_driver() -> Device:
    adb = adbutils.adb
    devices = adb.list()
    serial = devices[0].serial

    driver = ua2.connect(serial)
    return driver


def open_datasource() -> list[str]:
    datas: list[str]
    with open('./daftar_product.txt', 'r') as  f:
        content = f.read()
        datas = content.split("\n")
    
    return datas

def main():
    driver = open_driver()

    urls = open_datasource()
    steps = Steps(driver=driver)
    account_steps = AccountSteps(driver=driver)
    product_steps = ProductSteps(driver=driver)

    account_state = {}


    for url in urls:
        url = url.split("?")[0]
        driver.open_url(url)

        account = Account()
        account.name = "hitampekad"
        product = Product()
        try:
            product.name = product_steps.set_product_name()
            product.url = url
        except Exception as e:
            print(e)
            print(f"Kesalahan membuka produk {url}")
            continue

        steps.buy_now()
        if steps.is_shop_off():
            status = f"Ada masalah dengan produk {url}"
            print(status)
            continue


        try:                
            if steps.check_variant():
                steps.select_default_variant()
                steps.submit_buy()
                if not steps.check_checkout():
                    raise SelectVariantError("Uiautomator can't handle variant")
            else:
                steps.submit_buy()
        except SelectVariantError as e:
            print(e)
            print("Try alternative")
            steps.select_variant_alternative()
            if not steps.check_checkout():
                raise SelectVariantError("Uiautomator can't handle variant")
        except Exception as e:
            print(url, "Tolong cek manual")
            continue
                    
        time.sleep(1)
        steps.to_address_setting()
        if account.name in account_state.keys():
            while True:
                data: Account = account_state[account.name]
                address = data.next_selected_address()
                steps.select_shipping_address(address=address)
                time.sleep(0.5)

                account.addresses = data.addresses
                account.main_address = data.main_address
                if steps.check_checkout():
                    break
        else:
            addresses = account_steps.get_account_addresses()
            account.main_address = addresses[0]
            account.addresses = addresses
            print(account.addresses)
            time.sleep(0.25)
            steps.back(1)
        
        selected_address = product_steps.set_address_info()
        account.set_last_selected(selected_address)
        product.tujuan = selected_address

        while True:    
            steps.to_payment()
            steps.select_payment()
            steps.confirm_payment()
            steps.check_has_unpaid_order()
            steps.confirm_change_payment()
            if steps.check_set_payment_success:
                break

        product.nominal = product_steps.set_price_count()


        account_state[account.name] = account


if __name__ == "__main__":
    # main()

    driver = open_driver()

    steps = Steps(driver=driver)
    account_steps = AccountSteps(driver=driver)

    # driver.app_start(steps.app_package)
    driver.open_quick_settings()
    time.sleep(3)
    el = driver.xpath('//*[@text="Mode Pesawat"]/../../..')
    el.click()
    time.sleep(5)
    el.click()
    # driver.shell(["settings", "put", "global", "airplane_mode_on", "1"])
    # driver.shell(["am", "start", "global", "-a", "android.settings.AIRPLANE_MODE_SETTINGS"])
       


    

    # adb shell input keyevent KEYCODE_DPAD_DOWN
    # adb shell input keyevent KEYCODE_DPAD_UP

    # while True:
    #     account_steps.to_account()

    #     account_steps.to_setting()
    #     account_steps.to_switch_account()
    #     account_steps.switch_account()
    #     if not account_steps.is_success_switching():
    #         raise SwitchingAccountError("failed to change account")