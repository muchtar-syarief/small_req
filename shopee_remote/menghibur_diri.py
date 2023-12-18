import uiautomator2 as u2
import os,csv,sys
import time
from alive_progress import alive_bar
import subprocess

process = subprocess.check_output(['adb', 'devices'])
adb_devices = process.split()[4].decode()
d = u2.connect(adb_devices)

#comment live
d(resourceId="com.shopee.id.dfpluginshopee7:id/tv_send_message").click()
d.send_keys("ready ka", clear=True)
time.sleep(1)   
d.press("enter")


# OPEN SHOPEE BY URL
# chrome = 'com.android.chrome'
# url = 'https://shopee.co.id/universal-link?redir=https://live.shopee.co.id/share/'
# print(d.window_size())
# d.app_start(chrome,use_monkey=True)
# time.sleep(3)   
# d.xpath('//*[@resource-id="com.android.chrome:id/url_bar"]').click()
# time.sleep(5)   
# d.send_keys(url, clear=True)
# time.sleep(1)   
# d.press("enter")
# d.xpath('//*[@text="Lanjutkan"]').click()
# time.sleep(10)   


#like Live :
for i in range(10) :
    d(resourceId="com.shopee.id.dfpluginshopee7:id/iv_like").click()
    d(resourceId="com.shopee.id.dfpluginshopee7:id/iv_like").click()
    d(resourceId="com.shopee.id.dfpluginshopee7:id/iv_like").click()
    d(resourceId="com.shopee.id.dfpluginshopee7:id/iv_like").click()
    d(resourceId="com.shopee.id.dfpluginshopee7:id/iv_like").click()

#checkout keranjang
d.xpath('//*[@text="Beli"]').click()
time.sleep(1)
try:
    #Handling Variasi
    d.xpath('//*[@text="Masukkan Keranjang"]').click()
    time.sleep(1)
    try:
        d(resourceId="buttonOption_unselected").click()
        time.sleep(1)
        d.xpath('//*[@resource-id="sectionTierVariation"]/android.widget.ScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click(timeout=2)
        d.xpath('//*[@text="Masukkan Keranjang"]').click()
    except:
        pass
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
