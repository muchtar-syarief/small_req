import os,csv, sys
import adbutils
import uiautomator2 as u2
import atexit
import logging

 
from pathlib import Path
from uiautomator2 import Device
from uiautomator2.core import MockAdbProcess, BasicUiautomatorServer, launch_uiautomator
from typing import Union

from steps import Steps, SelectVariantError
from src.atx.req import override_req_cacert
from src.helper.file_txt import file_load_lines

logging.basicConfig(format='%(asctime)2s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class NoDeviceConnectedError(Exception):
    pass


def list_datasouce():
    direktori = os.getcwd()
    with open(direktori + '\\username_toko.csv') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        data_read = [row for row in reader]
    data_read = list(filter(None, data_read))
    return data_read


def save_results(data: list[str]):
    with open("./report_spl.csv", "a", newline="") as file:
        w = csv.writer(file)
        w.writerow(data)

        
class BasicUiAutomatorCustom(BasicUiautomatorServer):
    def __init__(self, dev: adbutils.AdbDevice) -> None:
        self._dev = dev
        self._process = None
        self._debug = False
        self.start_uiautomator()
        atexit.register(self.stop_uiautomator, wait=False)



class UiAutomatorCustom(Device):
    def __init__(self, serial: Union[str, adbutils.AdbDevice] = None):
        if isinstance(serial, adbutils.AdbDevice):
            self._serial = serial.serial
            self._dev = serial
        else:
            self._serial = serial
            self._dev = self._wait_for_device()
        self._debug = False
        BasicUiAutomatorCustom.__init__(self, self._dev)

    def _setup_jar(self):
        jar_path: str | Path
        if hasattr(sys, "frozen"):     
            local_file = sys._MEIPASS+ "/assets"
            jar_path = local_file +"/u2.jar"
        else:
            local_file = Path(__file__).parent / "assets"
            jar_path = local_file / "u2.jar"

        target_path = "/data/local/tmp/u2.jar"
        if self._check_device_file_hash(jar_path, target_path):
            logger.debug("file u2.jar already pushed")
        else:
            logger.debug("push %s -> %s", jar_path, target_path)
            self._dev.sync.push(jar_path, target_path, check=True)

def check_report_file(pathfile: str) -> None:
    open_type = "a"
    if not os.path.exists(report_filepath):
        open_type = "w+"
        headers = ["username","status"]
        with open(report_filepath, open_type, newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)


def log(msg: str) ->None:
    logging.info(f"[ LOG ]: {msg}")

if __name__ == "__main__":
    log("Starting shopee paylater checker....")
    
    log("Initializing mobile device...")
    adb = adbutils.adb
    devices = adb.list()
    if len(devices) == 0:
        raise NoDeviceConnectedError("Tidak ada perangkat yang tersambung")

    serial = devices[0].serial
    device = UiAutomatorCustom(serial)
    
    shops_username = file_load_lines("./toko.txt")

    report_filepath = "./report_spl.csv"
    check_report_file(report_filepath)

    steps = Steps(driver=device)
    try: 
        log("Initializing shopee aplication...")
        steps.open_app()
        steps.tap_search_bar()


        log("Masuk kepencarian toko...")
        for item in shops_username:
            if steps.to_search_shop(item.strip()):
                break

        log("Mulai mencari toko...")
        for item in shops_username:
            item = item.strip()

            try:
                item = item.replace("\n", "")
                log(f"Mencari toko {item}...")

                status: str
                result: list[str]

                if not steps.search_shop(item.lower()):
                    log(f"{item} tidak ditemukan...")
                    status = "TOKO TIDAK DITEMUKAN"

                    result = [item, status]
                    save_results(result)
                    continue
                
                log(f"Mencari produk toko {item}...")
                try:
                    steps.get_shop_product()
                except Exception as e:
                    print(e)
                    steps.back(1)
                    continue

                steps.buy_now()

                if steps.is_shop_off():
                    log(f"{item} tidak aktif dalam selang waktu...")
                    status = "TOKO TIDAK AKTIF"
                    result = [item, status]

                    save_results(result)
                    steps.back(3)
                    continue

                log("Mecoba memilih variasi produk...")
                try:                
                    if steps.check_variant():
                        steps.select_default_variant()
                        steps.submit_buy()
                        if not steps.check_checkout():
                            raise SelectVariantError("Uiautomator can't handle variant")
                    else:
                        steps.submit_buy()
                except SelectVariantError as e:
                    log("Uiautomator can't handle variant")
                    log("Mencoba cara lain...")
                    steps.select_variant_alternative()
                    if not steps.check_checkout():
                        raise SelectVariantError("Uiautomator can't handle variant")
                except Exception as e:
                    result = [item, "CEK MANUAL"]
                    log(f"{item} status paylater {result[-1]}")
                    save_results(result)
                    steps.back(2)
                    continue

                log("Mencari metode pembayaran...")
                steps.select_payment()

                log("Memeriksa shopee paylater...")
                try:
                    if steps.is_use_paylater():
                        status = 'AKTIF'
                        result = [item, status]
                    else:
                        status = 'TIDAK AKTIF'
                        result = [item, status]
                    
                    log(f"{item} status paylater {result[-1]}")
                    save_results(result)
                except Exception as e:
                    result = [item, "CEK MANUAL"]
                    log(f"{item} status paylater {result[-1]}")
                    save_results(result)
                finally:
                    steps.back(4)

            except Exception as e:
                print(e)

                # restart app
                log("Restarting application...")
                steps.close_app()

                log("Initializing shopee aplication...")
                steps.open_app()
                steps.tap_search_bar()

                log("Masuk kepencarian toko...")
                for item in shops_username:
                    if steps.to_search_shop(item):
                        break

    except Exception as e:
        print(e)

    finally:
        steps.close_app()
