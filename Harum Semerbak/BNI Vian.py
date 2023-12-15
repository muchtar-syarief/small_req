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

def session_habis():
    if d.xpath('//*[@resource-id="android:id/message"]').get_text() == '"Sesi Anda habis, silakan login kembali"':
        print('Session Berakhir silahkan login kembali, Klik Continue jika sudah di halaman Transfer')
        os.system('pause')
        pass

def pilih_rek_awal(rekening_asal):
    print('Sedang Mencari Rekening')
    a = True
    dorman = False
    rek_terakhir = ''
    while a:
        # print(rek_terakhir)
        rek_tampil = len(d(resourceId="android:id/text1"))
        # print(rek_tampil)
        d.swipe_ext("up",0.1)
        for i in range(11):
            # time.sleep(0.1)
            # d.swipe_ext("up",0.1)
            # try:
            rek_index = d(resourceId="android:id/text1")[i].get_text()
            print(rek_index)
            # except:
            #     d.swipe_ext("up",0.1)
            #     rek_index = d(resourceId="android:id/text1")[i].get_text()
            #     print(rek_index)
            if rek_index == rekening_asal:
                d.xpath(f'//*[@text={rekening_asal}]').click()
                print('Rekening Di temukan')
                a = False
                dorman = False
                return dorman
            if d(resourceId="android:id/text1")[-1].get_text() == rek_terakhir :
                a = False
                print('Rekening Tidak Di temukan')
                dorman = True
                return dorman
        rek_terakhir = d(resourceId="android:id/text1")[-1].get_text()      
        d.swipe_ext("up",1)
        print(a)
    # return dorman

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
# print ('1. Xiaomi BNI Vian = 3bc721730904')
# print ('2. Asus BNI Vian = JAAXGF003746X4Z')
# hp =  int(input('Silahkan Pilih Handphine: ',))
# if hp == 1:
#     hp_input = '3bc721730904'
#     nama_hp = 'Xiaomi BNI Vian'
# elif hp == 2:
#     hp_input = 'JAAXGF003746X4Z'
#     nama_hp = 'Asus BNI Vian'
# print(nama_hp, hp_input)
pin =str(input('Silahkan masukan Pin: ',))
process = subprocess.check_output(['adb', 'devices'])
adb_devices = process.split()[4].decode()
print(adb_devices)
for kolom in data_read[1:]:
    rekening_asal= kolom[0]
    rekening_tujuan = kolom[1]
    nomimal = kolom[2]    
    print(rekening_asal, rekening_tujuan, nomimal)
    d = u2.connect(adb_devices)
    d.xpath('//*[@resource-id="sel1"]').click()
    time.sleep(2)
    dorman = pilih_rek_awal(rekening_asal)
    print(dorman)
    if dorman:
        d.press("back")
        f = open('Report Transfer.csv', 'a')
        f.write(f'{rekening_asal},{rekening_tujuan},{nomimal},Dorman'+ '\n')
        f.close()
        continue
    d.xpath('//*[@resource-id="toAccount"]').click()
    pilih_rekening_tujuan(rekening_tujuan)
    time.sleep(3)
    d.xpath('//*[@resource-id="amount"]').click()
    d.send_keys(nomimal, clear=True)
    time.sleep(1)
    d.xpath('//*[@text="Lanjut"]').click()

    #Pin
    time.sleep(3)
    d.xpath(f'//*[@resource-id="passcode"]').click()
    d.send_keys(pin, clear=True)
    time.sleep(1)
    d.xpath('//*[@text="Selanjutnya"]').click()
    time.sleep(1)
    try:
        d.xpath('//*[@text="  Transaksi Lagi"]').click()
    except:
        d.xpath('//*[@text="  Transaksi Lagi"]').click()
    f = open('Report Transfer.csv', 'a')
    f.write(f'{rekening_asal},{rekening_tujuan},{nomimal},Sukses'+ '\n')
    f.close()
    # except:
    #     f = open('Report Transfer.csv', 'a')
    #     f.write(f'{rekening_asal},{rekening_tujuan},{nomimal},Dorman'+ '\n')
    #     f.close()
# d.xpath('//*[@text="Kembali ke Beranda"]').clcik()