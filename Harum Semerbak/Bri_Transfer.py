import uiautomator2 as u2
import os,csv,sys
import time
from alive_progress import alive_bar
import subprocess

def list_datasouce():
    direktori = os.getcwd()
    with open(direktori + '\\list_rek.csv') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        data_read = [row for row in reader]
    data_read = list(filter(None, data_read))
    return data_read

def login(mpin):
    d.app_start("src.com.bni",use_monkey=True)
    time.sleep(1)
    d.xpath('//*[@text="Login "]').click()
    d.xpath('//*[@resource-id="mpin"]').click()
    d.send_keys(mpin, clear=True)
    time.sleep(1)
    d.xpath('//*[@text="Login "]').click()
    time.sleep(1)
    d.xpath('//*[@text="Transfer"]').click()
    time.sleep(0.5)
    d.xpath('//*[@text="Rekening Sendiri"]').click()


def pilih_rek_anak(rekening_anak):
    print('Sedang Mencari Rekening')
    a = True
    dorman = False
    rek_terakhir = ''
    while a:
        d.swipe_ext("up",0.1)
        time.sleep(1)
        len_rek = len(d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening"))
        len_saldo = len(d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo"))
        len_rek = len(d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening"))
        len_saldo = len(d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo"))
        i_saldo = 0
        if len_saldo > len_rek :
            i_saldo = 1
        if len_rek > len_saldo :
            d.swipe_ext("up",0.1)
        for i in range(len_rek):
            rek_index = d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[i].get_text()
            rek_index_ =rek_index.replace(' ','') 
            print(rek_index)
            if rek_index_ == rekening_anak:
                print('Rekening Di temukan')
                print(rek_index)
                get_koor = d.xpath(f'//*[@text="{rek_index}"]')
                koordinat = get_koor.center()
                x = koordinat[0]
                y = koordinat[1]
                saldo = d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo")[i + i_saldo].get_text()
                saldo_ = saldo.replace("Rp","").replace(".","").split(',')[0]
                
                d.click(x,y)
                
                print(saldo_)
                a = False
                dorman = False
                return dorman,saldo_,rek_index_
            if d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[-1].get_text() == rek_terakhir :
                a = False
                print('Rekening Tidak Di temukan')
                saldo_ = '0'
                dorman = True
                return dorman,saldo_
        rek_terakhir = d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[-1].get_text()      
        d.swipe_ext("up",1)
        time.sleep(1)
        print(a)

def pilih_rekening_tujuan(rekening_tujuan):
    b = True
    dorman2 = False
    while b:
        for i in range(11):
            time.sleep(0.2)
            if d(resourceId="android:id/text1")[i].get_text() == rekening_tujuan:
                d.xpath(f'//*[@text={rekening_tujuan}]').click()
                b = False
                break
        d.swipe_ext("up",1)
    return dorman2


data_read = list_datasouce()
password_email = data_read[0][3]
#pin = data_read[0][2]
#pin = [*pin]
process = subprocess.check_output(['adb', 'devices'])
adb_devices = process.split()[4].decode()
print(adb_devices)
d = u2.connect(adb_devices)
d.app_start("id.co.bri.brimo",use_monkey=True)
d.xpath('//*[@text="Login"]').click()
d(resourceId="id.co.bri.brimo:id/til_password").click()

d.send_keys(password_email, clear=True)
time.sleep(1)
d.xpath('//*[@resource-id="id.co.bri.brimo:id/button_login"]').click_exists(timeout=10.0)

for kolom in data_read[1:]:
    rekening_anak= kolom[0]
    rekening_tujuan = kolom[1]
    pin = kolom[2]    
    print(rekening_anak, rekening_tujuan,pin)
    
    #transfer
    time.sleep(1)
    d.xpath('//*[@text="Transfer"]').click_exists(timeout=10.0)
    time.sleep(1)
    d.xpath('//*[@text="Tambah Penerima"]').click()
    d.xpath('//*[@resource-id="id.co.bri.brimo:id/tiAmount"]').click(timeout=10.0)
    d.send_keys(rekening_tujuan, clear=True)
    d.xpath('//*[@resource-id="id.co.bri.brimo:id/btnSubmit"]').click_exists(timeout=10.0)
    d(resourceId="id.co.bri.brimo:id/item_layout_background").click_exists(timeout=10.0)
    time.sleep(2)
    dorman,saldo,rekening_anak = pilih_rek_anak(rekening_anak)
    print(saldo)
    if dorman:
        d.press("back")
        f = open('Report Transfer.csv', 'a')
        f.write(f'{rekening_anak},{rekening_tujuan},{saldo},Dorman'+ '\n')
        f.close()
        continue

    time.sleep(2)
    
    transfer_nominal = int(saldo) - 50000
    print(transfer_nominal)
    if d(resourceId="id.co.bri.brimo:id/edNominal").exists:
        d(resourceId="id.co.bri.brimo:id/edNominal").click()
    else:
        os.system('pause')
        # d.press("back")
        # d(resourceId="id.co.bri.brimo:id/edNominal").click()
    time.sleep(2)
    d.send_keys(str(transfer_nominal))
    time.sleep(2)
    d.xpath('//*[@resource-id="id.co.bri.brimo:id/btnSubmit"]').click_exists(timeout=10.0)
    # confirm
    d.xpath('//*[@resource-id="id.co.bri.brimo:id/btnSubmit"]').click_exists(timeout=10.0)
    #Pin
    pin = [*pin]
    print(pin)
    for i in range(len(pin)):
        d(resourceId="id.co.bri.brimo:id/tvPinNum", text=pin[i]).click()

    d.xpath('//*[@resource-id="id.co.bri.brimo:id/btn_receipt"]').click()
    f = open('Report Transfer.csv', 'a')
    f.write(f'{rekening_anak},{rekening_tujuan},{transfer_nominal},Sukses'+ '\n')
    f.close()
    try:
        d.xpath('//*[@resource-id="id.co.bri.brimo:id/bt_lain"]').click(timeout=2)
    except:
        pass

    