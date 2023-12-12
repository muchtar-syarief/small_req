import adbutils
import time
import uiautomator2 as ua
import traceback
import os
import csv

from chrome import Chrome
from steps import Steps
from product_info import Product
from account import Account

def open_datasource() -> list[str]:
    datas: list[str]
    with open('./daftar_product.txt', 'r') as  f:
        datas = f.readlines()
    
    return datas


if __name__ == "__main__":
    urls = open_datasource()

    adb = adbutils.adb
    devices = adb.list()

    serial = devices[0].serial

    driver = ua.connect(serial)

    chrome = Chrome(driver=driver)
    steps = Steps(driver=driver)
    product = Product(driver=driver)
    account = Account(driver=driver)
    
    
    driver.app_start(steps.app_package, use_monkey=True)
    account.to_account()
    account.to_setting()
    account.to_switch_account()

    print(account.check_active_all())

    account.switch_account()

    # file_path = "./report_fo.csv"
    # open_type = "w+"
    # if os.path.exists(file_path):
    #     open_type = "a"

    # headers = ["akun","produk", "url", "tujuan", "bank", "virtual_account", "nominal"]
    # with open(file_path, open_type) as f:
    #     writer = csv.writer(f)

    #     if open_type == "w+":
    #         writer.writerow(headers)

    #     try:
    #         for url in urls:
    #             chrome.open_url(url)

    #             product.set_product_name()
    #             product.set_url(url=url)

    #             steps.buy_now()
    #             if not steps.check_submit_buy():
    #                 status = "Status toko Off"
    #                 print(status)
                            
    #             if steps.check_variant():
    #                 if steps.all_variant_appear():
    #                     while True:
    #                         steps.select_default_variant()
    #                         time.sleep(1)
    #                         steps.submit_buy()
    #                         if steps.check_checkout():
    #                             break
    #                 else:
    #                     while True:
    #                         steps.select_default_variant()
    #                         steps.scroll_variant()
    #                         steps.select_default_variant(1)
    #                         time.sleep(1)
    #                         steps.submit_buy()
    #                         if steps.check_checkout():
    #                             break

    #             else:
    #                 steps.submit_buy()

    #             product.set_address_info()

    #             while True:    
    #                 steps.to_payment()
    #                 steps.select_payment()
    #                 steps.confirm_payment()
    #                 steps.check_has_unpaid_order()
    #                 if steps.check_set_payment_success:
    #                     break
                
    #             product.set_price_count()

    #             steps.create_order()

    #             product.set_virtual_account()

    #             steps.after_payment()

    #             account.to_account()

    #             product.set_account()

    #             account.to_setting()
    #             account.to_switch_account()
    #             account.switch_account()
                

    #     except Exception as e:
    #         with open("./log_error.txt", "a+") as f:
    #                 f.write(traceback.format_exc())

    #     finally:
    #         # steps.close_app()
    #         print(product.__dict__)
    #         print("selesai")






