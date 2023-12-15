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

def data_saldo():
    # a = True
    dorman = False
    rek_terakhir = ''
    log_rekening = []
    if d(resourceId="id.co.bri.brimo:id/iv_rekening_default").exists(timeout=20):
        a = True
        print('Siap Jalan .. ')
        time.sleep(5)
        # d.swipe_ext("down",0.7)
    # d.xpath('//*[@text="Total Saldo"]').click_exists(timeout=10.0)
    while a:
        len_rek = len(d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening"))
        len_saldo = len(d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo"))
        get_koor_rek = d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[0].center()
        y_rek = get_koor_rek[1]
        get_koor_saldo = d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo")[0].center()
        y_saldo = get_koor_saldo[1]
        if y_rek > y_saldo:
            # print(y_rek, y_saldo)
            i_saldo = 1
            len_loop = len_rek
        else:
            i_saldo = 0
            len_loop = len_saldo
        with alive_bar(len_rek) as bar:
            for i in range(len_loop):
                try:
                    rek_index = d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[i].get_text()
                    rek_index_ =rek_index.replace(' ','')
                    saldo = d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo")[i+i_saldo].get_text()
                    saldo_ = saldo.replace("Rp","").replace(".","").split(',')[0]
                except:
                    pass
                # print(rek_index_, saldo_)
                if rek_index_ not in log_rekening:
                    f = open('Report Saldo.csv', 'a')
                    f.write(f'{rek_index_},{saldo_}'+ '\n')
                    f.close()
                    log_rekening.append(rek_index_)
                    
                
                if d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[-1].get_text() == rek_terakhir :
                    # rek_index = d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[-1].get_text()
                    # rek_index_ =rek_index.replace(' ','')
                    # saldo = d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo")[-1].get_text()
                    # saldo_ = saldo.replace("Rp","").replace(".","").split(',')[0]
                    # if rek_index_ not in log_rekening:
                    #     f = open('Report Saldo.csv', 'a')
                    #     f.write(f'{rek_index_},{saldo_}'+ '\n')
                    #     f.close()
                    a = False
                    print('Done')
                    dorman = True
                    
                    return dorman,saldo_
                bar()
            
        rek_terakhir = d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[-1].get_text()      
        d.swipe_ext("up",0.7)
        time.sleep(2)

data_read = list_datasouce()
password_email = data_read[0][3]
process = subprocess.check_output(['adb', 'devices'])
adb_devices = process.split()[4].decode()
print(adb_devices)
d = u2.connect(adb_devices)
d.app_start("id.co.bri.brimo",use_monkey=True)
d.xpath('//*[@text="Login"]').click()
time.sleep(1)
d(resourceId="id.co.bri.brimo:id/til_password").click()
d.send_keys(password_email, clear=True)
time.sleep(1)
d.xpath('//*[@resource-id="id.co.bri.brimo:id/button_login"]').click_exists(timeout=10.0)
d.xpath('//*[@text="Rekening Lain"]').click_exists(timeout=10.0)
time.sleep(2)
data_saldo()