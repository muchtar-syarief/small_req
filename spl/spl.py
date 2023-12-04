# # Jalankan kode main.py
# JALANKAN KODE main.py





# import uiautomator2 as u2
# import os,csv
# import time
# import subprocess

# #Error
# #Hasil tidak sesuai ketika username mirip atau sama dengan yang lain




# def list_datasouce():
#     direktori = os.getcwd()
#     with open(direktori + '\\username_toko.csv') as fp:
#         reader = csv.reader(fp, delimiter=',', quotechar='"')
#         data_read = [row for row in reader]
#     data_read = list(filter(None, data_read))
#     return data_read

# def cek_element(xpath_):
#     try:
#         d.xpath(xpath_).exists
#     except:
#         return False
#     return True

# mulai = int(input('Mulai dari line ke: ',))
# if mulai == 0 or mulai == 1:
#     mulai = 2
# mulai = mulai -1

# __app_package = "com.shopee.id"

# data_read = list_datasouce()
# process = subprocess.check_output(['adb', 'devices'])
# adb_devices = process.split()[4].decode()
# d = u2.connect(adb_devices)
# d.app_start(__app_package,use_monkey=True)
# print(adb_devices)
# for kolom in data_read[(mulai):]:
#     username_toko= kolom[0]
#     print('Checking ',username_toko)
#     d.xpath('//*[@resource-id="com.shopee.id:id/text_container"]').click()
#     d.send_keys(username_toko, clear=True)
#     d.press("enter")
#     try:
#         time.sleep(1)
#         d.xpath('//*[@resource-id="com.shopee.id:id/main_view"]/android.widget.FrameLayout[3]').click(timeout=2)
#         d.xpath('//*[@resource-id="buttonSearchResultPagePrice"]').click(timeout=2)
#         time.sleep(1)
#         d.xpath('//*[@resource-id="labelItemCardDiscPrice"]').click(timeout=2)
#         time.sleep(1)
#         d.xpath('//*[@text="Beli Sekarang"]').click(timeout=2)
#         while True:
#             try:
#                 d.xpath('//*[@resource-id="cartPanelTierVariation"]/android.view.ViewGroup[1]').click(timeout=5)
#                 d.xpath('//*[@text="Beli Sekarang"]').click()
#                 time.sleep(2)
#                 d.xpath('//*[@resource-id="sectionTierVariation"]/android.widget.ScrollView[1]/android.view.ViewGroup[1]/android.view.ViewGroup[3]/android.view.ViewGroup[1]/android.view.ViewGroup[1]').click(timeout=5)
#                 d.xpath('//*[@text="Beli Sekarang"]').click()
#                 break
#             except:
#                 break
#         try:
#             time.sleep(3)
#             d.swipe_ext("up",0.9)
#             d.xpath('//*[@text="Metode Pembayaran"]').click(timeout=5)
#             time.sleep(2)
#             status = 'No SPL'
#             if cek_element('//*[@resource-id="imageCheck"]'):
#                 status = 'SPL Aktiv'
#             while True:
#                 if d.xpath('//*[@resource-id="com.shopee.id:id/icon"]').exists:
#                     break
#                 else:
#                     d.press("back")
#         except:
#             print('Kosong')
#             status = 'No SPL'
#             while True:
#                 if d.xpath('//*[@resource-id="com.shopee.id:id/icon"]').exists:
#                     break
#                 else:
#                     d.press("back")
            
#     except:
#         while True:
#             if d.xpath('//*[@resource-id="com.shopee.id:id/icon"]').exists:
#                 break
#             else:
#                 d.press("back")
#         status = 'Status toko Off/Tidak ditemukan/Tidak ada Produk'

#     f = open('Report SPL.csv', 'a')
#     f.write(f'{username_toko},{status}'+ '\n')
#     f.close()

# d.app_stop(__app_package)
# d.press("home")
# d.shell(["input", "keyevent", "KEYCODE_APP_SWITCH"])
# d.shell(["input", "keyevent", "KEYCODE_DPAD_DOWN"])
# d.shell(["input", "keyevent", "DEL"])
# d.press("home")
    

# # if __name__ == "__main__":
# #     mulai = int(input('Mulai dari line ke: ',))
# #     if mulai == 0 or mulai == 1:
# #         mulai = 2
# #     mulai = mulai -1

# #     data_read = list_datasouce()
# #     process = subprocess.check_output(['adb', 'devices'])
# #     adb_devices = process.split()[4].decode()

# #     data_read = list_datasouce()

# #     d = u2.connect(adb_devices)
# #     steps = Steps(d)

# #     steps.open_app()

# #     results = []
# #     try:
# #         print("Masuk ke pencarian toko")
# #         for kolom in data_read[(mulai):]:
# #             shop = kolom[0]
# #             if steps.to_search_shop(shop):
# #                 break

# #         for kolom in data_read[(mulai):]:
# #             shop = kolom[0]
# #             status = 'Toko Tidak ditemukan'
# #             print('Checking ', shop)

# #             if not steps.search_shop(shop):
# #                 print(f"Toko {shop} tidak ditemukan")

# #                 result = [shop, status]
# #                 results.append(result)
# #                 continue
            
# #             time.sleep(2)
# #             steps.get_shop_product()
# #             steps.buy_now()

# #             time.sleep(3)
# #             if not steps.check_submit_buy():
# #                 print(f"Toko {shop} off")

# #                 status = "Status toko Off"
# #                 result = [shop, status]
# #                 results.append(result)
# #                 continue
            
# #             if steps.check_variant():
# #                 while True:
# #                     steps.select_default_variant()
# #                     time.sleep(1)
# #                     steps.submit_buy()
# #                     time.sleep(3)
# #                     if steps.check_checkout():
# #                         break
# #             else:
# #                 steps.submit_buy()

# #             steps.select_payment()

# #             if steps.is_use_paylater():
# #                 status = 'SPL Aktiv'
# #                 result = [shop, status]
# #                 results.append(result)
# #             else:
# #                 status = 'No SPL'
# #                 result = [shop, status]
# #                 results.append(result)

            
# #     except Exception as e:
# #         print(e)
    
# #     finally: 
# #         steps.close_app()

# #     headers = ["username","status"]
# #     with open("report_spl.csv", "w+", newline='') as f:
# #         writer = csv.writer(f)

# #         writer.writerow(headers)

# #         for row in results:
# #             writer.writerow(row)






