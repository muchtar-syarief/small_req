import os,csv, sys
import adbutils
import uiautomator2 as u2

from steps import Steps, SelectVariantError
from atx import ATX


class NoDeviceConnectedError(Exception):
    pass


def list_datasouce():
    direktori = os.getcwd()
    with open(direktori + '\\username_toko.csv') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        data_read = [row for row in reader]
    data_read = list(filter(None, data_read))
    return data_read


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

def save_results(data: list[str]):
    with open("./report_spl.csv", "a", newline="") as file:
        w = csv.writer(file)
        w.writerow(data)

if __name__ == "__main__":
    override_req_cacert()

    mulai = int(input('Mulai dari line ke: ',))
    if mulai == 0 or mulai == 1:
        mulai = 2
    mulai = mulai -1

    data_read = list_datasouce()
    
    adb = adbutils.adb
    devices = adb.list()
    if len(devices) == 0:
        raise NoDeviceConnectedError("Tidak ada perangkat yang tersambung")

    device = devices[0].serial


    data_read = list_datasouce()

    d = u2.connect(device)
    if getattr(sys, 'frozen', False):
        atx = ATX(driver=d)
        atx.init_atx_app()
    
    steps = Steps(d)


    file_path = "./report_spl.csv"
    open_type = "a"
    if not os.path.exists(file_path):
        open_type = "w+"
        headers = ["username","status"]
        with open(file_path, open_type, newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    try:
        steps.open_app()
        steps.tap_search_bar()

        print("Masuk ke pencarian toko")
        for kolom in data_read[(mulai):]:
            shop = kolom[0]
            if steps.to_search_shop(shop):
                break

        for kolom in data_read[(mulai):]:
            shop = kolom[0]
            status = 'Toko Tidak ditemukan'
            print('Checking ', shop)


            result: list[str]

            if not steps.search_shop(shop.strip()):
                print(f"Toko {shop} tidak ditemukan")

                result = [shop, status]
                save_results(result)
                continue
                
            try:
                steps.get_shop_product()
            except Exception as e:
                print(e)
                steps.back(1)
                continue

            steps.buy_now()

            if steps.is_shop_off():
                print(f"Toko {shop} off")
                status = "Status toko Off"
                result = [shop, status]

                save_results(result)
                steps.back(3)
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
                print(shop, e)
                result = [shop, "Tolong cek manual"]
                save_results(result)
                steps.back(3)
                continue

            steps.select_payment()

            try:
                if steps.is_use_paylater():
                    status = 'SPL Aktiv'
                    result = [shop, status]
                else:
                    status = 'No SPL'
                    result = [shop, status]
                save_results(result)
            except Exception as e:
                print(shop, e)
                result = [shop, "Tolong cek manual"]
                save_results(result)
            finally:
                steps.back(4)

    except Exception as e:
        print(shop, e)
        with open("log_error", "w+", newline='') as f:
            f.write(e.__str__())
    finally: 
        steps.close_app()
