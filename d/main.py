import os,csv, sys
import time
import subprocess
import adbutils
import uiautomator2 as u2

from steps import Steps

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
        return sys._MEIPASS+"/certify/cacert.pem"

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

class NoDeviceConnectedError(Exception):
    pass


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
    steps = Steps(d)

    steps.open_app()

    results = []
    try:
        print("Masuk ke pencarian toko")
        for kolom in data_read[(mulai):]:
            shop = kolom[0]
            if steps.to_search_shop(shop):
                break

        for kolom in data_read[(mulai):]:
            shop = kolom[0]
            status = 'Toko Tidak ditemukan'
            print('Checking ', shop)

            if not steps.search_shop(shop):
                print(f"Toko {shop} tidak ditemukan")

                result = [shop, status]
                results.append(result)
                continue
            
            time.sleep(2)
            steps.get_shop_product()
            steps.buy_now()

            time.sleep(3)
            if not steps.check_submit_buy():
                print(f"Toko {shop} off")

                status = "Status toko Off"
                result = [shop, status]
                results.append(result)
                continue
            
            if steps.check_variant():
                while True:
                    steps.select_default_variant()
                    time.sleep(1)
                    steps.submit_buy()
                    time.sleep(3)
                    if steps.check_checkout():
                        break
            else:
                steps.submit_buy()

            steps.select_payment()

            if steps.is_use_paylater():
                status = 'SPL Aktiv'
                result = [shop, status]
                results.append(result)
            else:
                status = 'No SPL'
                result = [shop, status]
                results.append(result)

            
    except Exception as e:
        print(e)
    
    finally: 
        steps.close_app()

    headers = ["username","status"]
    with open("report_spl.csv", "w+", newline='') as f:
        writer = csv.writer(f)

        writer.writerow(headers)

        for row in results:
            writer.writerow(row)




