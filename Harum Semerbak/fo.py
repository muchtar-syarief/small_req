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
d.xpath('//*[@resource-id="com.shopee.id:id/text_container"]').click()
d.send_keys("hitampekad", clear=True)
d.press("enter")
status = 'No SPL'
if d.xpath('//*[@resource-id="com.shopee.id:id/main_view"]/android.widget.FrameLayout[3]').click_exists(timeout=5):
    #try:
    time.sleep(1)        
    d.xpath('//*[@resource-id="com.shopee.id:id/main_view"]/android.widget.FrameLayout[3]').click(timeout=2)
    time.sleep(1)
    #def order():

    d.xpath('//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.view.ViewGroup[1]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click()



chrome = 'com.android.chrome'
url = 'https://shopee.co.id/Troli-Belanja-Barang-Lipat-2-roda-Galon-Tabung-Gas-Serbaguna-Krisbow-i.11669330.13850954582'
print(d.window_size())
d.app_start(chrome,use_monkey=True)
time.sleep(3)   
d.xpath('//*[@resource-id="com.android.chrome:id/url_bar"]').click()
time.sleep(5)   
d.send_keys(url, clear=True)
time.sleep(1)   
d.press("enter")
time.sleep(10)   
try:
    d.xpath('//*[@text="Jual Troli Belanja Barang Lipat 2 roda Galon Tabung Gas Serbaguna Krisbow | Shopee Indonesia"]/android.view.View[1]/android.view.View[1]/android.view.View[1]/android.view.View[2]').click()
except:
    pass
d.xpath('//*[@text="Chat Sekarang"]').click()

#comment live
d(resourceId="com.shopee.id.dfpluginshopee7:id/tv_send_message").click()
d.send_keys("halo ka", clear=True)
time.sleep(1)   
d.press("enter")

#like Live :
for i in range(10) :
    d(resourceId="com.shopee.id.dfpluginshopee7:id/iv_like").click()

#checkout keranjang
d.xpath('//*[@text="Beli"]').click()
#d.xpath('//*[@text="Beli Sekarang"]').click()
time.sleep(1)
try:

    d.xpath('//*[@text="Masukkan Keranjang"]').click()
    time.sleep(1)
    try:
        d(resourceId="buttonOption_unselected").click()
        time.sleep(1)
        d.xpath('//*[@resource-id="sectionTierVariation"]/android.widget.ScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click(timeout=2)
        d.xpath('//*[@text="Masukkan Keranjang"]').click()
    except:
        pass
#break
except:
    time.sleep(1)
    d.xpath('//*[@text="Masukkan Keranjang"]').click(timeout=2)


#ganti akun
if d.xpath('//*[@resource-id="com.shopee.id:id/icon"]').exists:
    d(resourceId="com.shopee.id:id/icon", description="tab_bar_button_me").click()
        
d.xpath('//*[@resource-id="buttonAccountSettings"]/android.widget.ImageView[1]').click()

for i in range(5):
    if d.xpath('//*[@text="Ganti Akun"]').exists:
        d.swipe_ext("up",0.5)
        break
    else:
        d.swipe_ext("up",0.8)

d.xpath('//*[@text="Ganti Akun"]').click()

#pilih akun 
#d.xpath('//*[@resource-id="com.shopee.id:id/rv_account_list"]/android.widget.FrameLayout[1]')