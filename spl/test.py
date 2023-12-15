import subprocess
import uiautomator2 as u2
import adbutils

# Serial number perangkat
adb = adbutils.adb
devices = adb.list()
serial = devices[0].serial
d = u2.connect(serial)
# Package name untuk browser bawaan di beberapa perangkat Android
chrome_package = "com.android.chrome"

# URL yang ingin dibuka
url = 'https://shopee.co.id/PROMO-SALEE!!!-SEPSEIAL-IP-15-PRO-256GB-LOGAMULIA-LAINYYA-SEMUA-BERHADIA-EMAS-i.435812713.22787428479'

# Membuka browser Chrome dengan adb shell am start
subprocess.run(["adb", "-s", serial, "shell", "am", "start", "-n", f"{chrome_package}/com.google.android.apps.chrome.Main", "-a", "android.intent.action.VIEW", "-d", url])

d(text="Chat Sekarang").click()

try:
    d(resourceId="android:id/button1").click()
except:
    pass
d(text="Beli Sekarang").click()

