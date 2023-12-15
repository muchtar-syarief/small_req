import uiautomator2 as u2
import os,time

d = u2.connect('e63794b9')
rek_index = []
while True:
    saldo_atas = False
    len_buku = len(d(resourceId="id.co.bri.brimo:id/cv_list_rekening"))
    len_rek = len(d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening"))
    len_saldo = len(d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo"))

    get_koor_rek = d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[0].center()
    y_rek = get_koor_rek[1]
    get_koor_saldo = d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo")[0].center()
    y_saldo = get_koor_saldo[1]
    if y_rek > y_saldo:
        print(y_rek, y_saldo)
        i_saldo = 1
        len_loop = len_rek
    else:
        i_saldo = 0
        len_loop = len_saldo
    for i in range(len_loop):
        try:
            rek_index = d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening")[i].get_text()
            saldo = d(resourceId="id.co.bri.brimo:id/tv_rekening_saldo")[i+i_saldo].get_text()
        except:
            pass
        f = open('Report Saldo2.csv', 'a')
        f.write(f'{rek_index},{saldo},{i_saldo}'+ '\n')
        f.close()
    if d(resourceId="id.co.bri.brimo:id/tv_detail_no_rekening").get_text() == '614601003733507':
        break
    d.swipe_ext("up",0.7)
    time.sleep(2)