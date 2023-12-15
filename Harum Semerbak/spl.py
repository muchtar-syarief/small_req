import uiautomator2 as u2
import os,csv,sys
import time
from alive_progress import alive_bar
import subprocess
from uiautomator2 import Direction

#Error
#Hasil tidak sesuai ketika username mirip atau sama dengan yang lain

def list_datasouce():
    direktori = os.getcwd()
    with open(direktori + '\\username_toko.csv') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        data_read = [row for row in reader]
    data_read = list(filter(None, data_read))
    return data_read

def cek_element(xpath_):
    try:
        d.xpath(xpath_).exists
    except:
        return False
    return True

mulai = int(input('Mulai dari line ke: ',))
if mulai == 0 or mulai == 1:
    mulai = 2
mulai = mulai -1

data_read = list_datasouce()
process = subprocess.check_output(['adb', 'devices'])
adb_devices = process.split()[4].decode()
d = u2.connect(adb_devices)
d.app_start("com.shopee.id",use_monkey=True)
print(adb_devices)
for kolom in data_read[(mulai):]:
    username_toko= kolom[0]
    print('Checking ',username_toko)
    d.xpath('//*[@resource-id="com.shopee.id:id/text_container"]').click()
    d.send_keys(username_toko, clear=True)
    d.press("enter")
    status = 'No SPL'
    if d.xpath('//*[@resource-id="com.shopee.id:id/main_view"]/android.widget.FrameLayout[3]').click_exists(timeout=5):
        try:
            time.sleep(1)        
            d.xpath('//*[@resource-id="com.shopee.id:id/main_view"]/android.widget.FrameLayout[3]').click(timeout=2)
            d.xpath('//*[@resource-id="buttonSearchResultPagePrice"]').click(timeout=2)
            time.sleep(1)
            d.xpath('//*[@resource-id="labelItemCardDiscPrice"]').click(timeout=2)
            time.sleep(3)
            d.xpath('//*[@text="Beli Sekarang"]').click(timeout=2)
            try:
                time.sleep(1)
                d.xpath('//*[@resource-id="cartPanelTierVariation"]/android.view.ViewGroup[1]').click()
                # d.xpath('//*[@resource-id="sectionProductImages"]/android.view.ViewGroup[4]/android.widget.HorizontalScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
                d.xpath('//*[@text="Beli Sekarang"]').click()
                time.sleep(1)
                try:
                    d.xpath('//*[@resource-id="sectionTierVariation"]/android.widget.ScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click(timeout=2)
                    d.xpath('//*[@text="Beli Sekarang"]').click()
                except:
                    pass
                #break
            except:
                time.sleep(1)
                d.xpath('//*[@text="Beli Sekarang"]').click(timeout=2)
            try:
                time.sleep(1)
                
            except:
                pass

            try:
                time.sleep(3)
                a = 0
                for i in range(5):
                    if d.xpath('//*[@text="Metode Pembayaran"]').exists:
                        d.swipe_ext("up",0.5)
                        break
                    else:
                        d.swipe_ext("up",0.8)
                        a = a + 1
                        # print(a)
                    
                # print(a)
                if a >= 5:
                    # print(a)
                    # d.press("back")
                    # if d.xpath('//*[@resource-id="sectionProductImages"]/android.view.ViewGroup[4]/android.widget.HorizontalScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click_exists(timeout=5):
                    #     d.xpath('//*[@resource-id="se  ctionProductImages"]/android.view.ViewGroup[4]/android.widget.HorizontalScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()
                    #     d.xpath('//*[@text="Beli Sekarang"]').click(timeout=2)
                    # for i in range(5):
                    #     if d.xpath('//*[@text="Metode Pembayaran"]').exists:
                    #         d.swipe_ext("up",0.5)
                    #         break
                    #     else:
                    #         d.swipe_ext("up",0.8)
                    status = 'Cek Manual Bro'
                    
                # d.xpath('//*[@text="Metode Pembayaran"]').click(timeout=5)
                # time.sleep(2)
                if d(text="x 1 bln").exists:
                    status = 'SPL Aktiv'
                while True:
                    if d.xpath('//*[@resource-id="com.shopee.id:id/icon"]').exists:
                        break
                    else:
                        d.press("back")
            except:
                while True:
                    if d.xpath('//*[@resource-id="com.shopee.id:id/icon"]').exists:
                        break
                    else:
                        d.press("back")
                
        except:
            while True:
                if d.xpath('//*[@resource-id="com.shopee.id:id/icon"]').exists:
                    break
                else:
                    d.press("back")
    else:
        while True:
            if d.xpath('//*[@resource-id="com.shopee.id:id/icon"]').exists:
                break
            else:
                d.press("back")
        status = 'Status toko Off/Tidak ditemukan/Tidak ada Produk'

    f = open('Report SPL.csv', 'a')
    f.write(f'{username_toko},{status}'+ '\n')
    f.close()
    