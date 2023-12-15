import adbutils
import uiautomator2 as ua
import traceback
import os
import csv
import time
import logging
import sys

from uiautomator2 import Device

from account import AccountSteps, SwitchingAccountError, Account
from atx import ATX
from chrome import Chrome
from product_info import Product, ProductSteps
from steps import Steps, SelectVariantError, AccountLimiTCheckOutError

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

def open_datasource() -> list[str]:
    datas: list[str]
    with open('./daftar_product.txt', 'r') as  f:
        content = f.read()
        datas = content.split("\n")
    
    return datas

def save_result(data: list[str]):
    with open("./report_fo.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

        
def open_driver() -> Device:
    adb = adbutils.adb
    devices = adb.list()

    serial = devices[0].serial

    driver = ua.connect(serial)
    if getattr(sys, 'frozen', False):
        atx = ATX(driver=driver)
        atx.init_atx_app()
    return driver


def override_req_cacert():
    def override_where():
        """ overrides certifi.core.where to return actual location of cacert.pem"""
        # change this to match the location of cacert.pem
        return sys._MEIPASS+"/certifi/cacert.pem"

    # is the program compiled?
    if hasattr(sys, "frozen"):
        import certifi.core

        os.environ["REQUESTS_CA_BUNDLE"] = override_where()
        certifi.core.where = override_where

        # delay importing until after where() has been replaced
        import requests.utils
        import requests.adapters
        # replace these variables in case these modules were
        # imported before we replaced certifi.core.where
        requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
        requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()




def init():
    file_path = "./report_fo.csv"
    open_type = "a"
    if not os.path.exists(file_path):
        open_type = "w+"
        headers = ["akun","produk", "url", "tujuan", "bank", "virtual_account", "nominal"]
        with open(file_path, open_type, newline="") as f:
            writer = csv.writer(f)
            if open_type == "w+":
                writer.writerow(headers)













if __name__ == "__main__":
    init()
    override_req_cacert()

    mulai = int(input('Mulai dari line ke: ',))
    if mulai != 0:
        mulai = mulai - 1

    driver = open_driver()

    chrome = Chrome(driver=driver)
    steps = Steps(driver=driver)
    account_steps = AccountSteps(driver=driver)
    product_steps = ProductSteps(driver=driver)

    driver.app_start(steps.app_package, use_monkey=True)

    account_state = {}

    try:
        urls = open_datasource()
        for ind, url in enumerate(urls[mulai:]):
            url = url.split("?")[0]

            logging.info(f"Url {ind+1} starting order {url}")

            account = Account()
            product = Product()
            if ind > 0:
                account.name = account_steps.get_account()

            chrome.open_url(url)
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
                    if not address:
                        addresses = account_steps.get_account_addresses()
                        account.main_address = addresses[0]
                        account.addresses = addresses
                        steps.back(1)
                        time.sleep(1)
                    else:
                        steps.select_shipping_address(address=address)
                        account.addresses = data.addresses
                        account.main_address = data.main_address

                        time.sleep(0.5)
                    if steps.check_checkout():
                        break
            else:
                addresses = account_steps.get_account_addresses()
                account.main_address = addresses[0]
                account.addresses = addresses
                steps.back(1)
                time.sleep(1)
            
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

            try:
                while True:
                    steps.create_order()

                    if not steps.check_valid_voucher():
                        steps.to_voucher()
                        steps.deactive_voucher()
                        steps.select_voucher()
                        continue
                    break

                if steps.limit_checkout():
                    raise AccountLimiTCheckOutError("Akun mencapai limit checkout")
                
                product.virtual_account = product_steps.set_virtual_account()

                steps.after_payment()
            except AccountLimiTCheckOutError as e:
                print(e)
                steps.back(3)


            account_steps.to_account()
            logging.info("Mulai berganti akun")

            if not account.name:
                account.name = account_steps.get_account()

            result = [account.name, product.name, product.url, product.tujuan, product.bank, product.virtual_account, product.nominal]
            save_result(result)

            account_state[account.name] = account


            account_steps.to_setting()
            account_steps.to_switch_account()
            account_steps.switching_account()
            

    except Exception as e:
        print(e)
        with open("./log_error.txt", "w+") as f:
                f.write(traceback.format_exc())
    finally:
        # steps.close_app()
        print("selesai")

