import time
import os
import sys
import requests

from uiautomator2 import GatewayError, NullObjectExceptionError, NullPointerExceptionError, StaleObjectExceptionError, ServerError
from uiautomator2 import Device


class ATX:
    def __init__(self, driver: Device) -> None:
        self.driver = driver
        
    def init_atx_app(self):
        try:
            return self.driver._jsonrpc_call("deviceInfo")
        except (requests.ReadTimeout, ServerError) as e:
            self.reset_uiautomator(str(e))  # uiautomator可能出问题了，强制重启一下
        except (NullObjectExceptionError,
                NullPointerExceptionError,
                StaleObjectExceptionError) as e:
            self.driver.logger.warning("jsonrpc call got: %s", str(e))
            self.reset_uiautomator(str(e))  # added to fix strange fatal jsonrpc NullPointerException
        return self.driver._jsonrpc_call("deviceInfo")    

    def reset_uiautomator(self, reason="unknown", depth=0):
        """
        Reset uiautomator

        Raises:
            GatewayError

        Orders:
            - stop uiautomator keeper
            - am force-stop com.github.uiautomator
            - start uiautomator keeper(am instrument -w ...)
            - wait until uiautomator service is ready
        """
        with self.driver._filelock:
            if depth >= 2:
                raise GatewayError(
                    "Uiautomator started failed.",
                    reason,
                    "https://github.com/openatx/uiautomator2/wiki/Common-issues",
                    "adb shell am instrument -w -r -e debug false -e class com.github.uiautomator.stub.Stub com.github.uiautomator.test/android.support.test.runner.AndroidJUnitRunner",
                )

            if depth > 0:
                self.driver.logger.info("restart-uiautomator since \"%s\"", reason)

            # Note:
            # atx-agent check has moved to _AgentRequestSession
            # If code goes here, it means atx-agent is fine.

            if self.driver._is_alive():
                return

            # atx-agent might be outdated, check atx-agent version here
            if self.driver._is_agent_outdated():
                if self.driver._serial: # update atx-agent will not work on WiFi
                    self.driver._prepare_atx_agent()

            ok = self._force_reset_uiautomator_v2(
                launch_test_app=depth > 0)  # uiautomator 2.0
            if ok:
                self.driver.logger.info("uiautomator back to normal")
                return

            output = self.driver._test_run_instrument()
            if "does not have a signature matching the target" in output:
                self._setup_uiautomator()
                reason = "signature not match, reinstall uiautomator apks"

        return self.reset_uiautomator(reason=reason,
                                    depth=depth + 1)
        
    def _setup_uiautomator(self):
        self.driver.shell(["pm", "uninstall", "com.github.uiautomator"])
        self.driver.shell(["pm", "uninstall", "com.github.uiautomator.test"])
        
        base_app_path = "/assets/app/"

        for name in ("app-uiautomator.apk", "app-uiautomator-test.apk"):
            apk_path = sys._MEIPASS+base_app_path+name
            cwd_apk_path = sys._MEIPASS+base_app_path+name
            if not os.path.exists(apk_path) and os.path.exists(cwd_apk_path):
                apk_path = cwd_apk_path
            target_path = "/data/local/tmp/" + name
            self.driver.logger.debug("Install %s", name)
            self.driver.push(apk_path, target_path)
            self.driver.shell(['pm', 'install', '-r', '-t', target_path])
        
    def _force_reset_uiautomator_v2(self, launch_test_app=False):
        brand = self.driver.shell("getprop ro.product.brand").output.strip()
        # self.logger.debug("Device: %s, %s", brand, self.serial)
        package_name = "com.github.uiautomator"

        self.driver.uiautomator.stop()

        self.driver.logger.debug("kill process(ps): uiautomator")
        self.driver._kill_process_by_name("uiautomator")

        ## Note: Here do not reinstall apks, since vivo and oppo reinstall need password
        # if self._is_apk_outdated():
        #     self._setup_uiautomator()
        if self.driver._is_apk_required():
            self._setup_uiautomator()

        if launch_test_app:
            self.driver._grant_app_permissions()
            self.driver.shell(['am', 'start', '-a', 'android.intent.action.MAIN', '-c',
                        'android.intent.category.LAUNCHER', '-n', package_name + "/" + ".ToastActivity"])
            
        self.driver.uiautomator.start()

        # wait until uiautomator2 service is working
        time.sleep(.5)
        deadline = time.time() + 40.0  # in vivo-Y67, launch timeout 24s
        flow_window_showed = False
        while time.time() < deadline:
            self.driver.logger.debug("uiautomator-v2 is starting ... left: %.1fs",
                         deadline - time.time())

            if not self.driver.uiautomator.running():
                break

            if self.driver._is_alive():
                # 显示悬浮窗，增加稳定性
                # 可能会带来悬浮窗对话框
                # 利大于弊，先加了
                # show Float window 在华为手机上，还需要再次等待
                if not flow_window_showed:
                    flow_window_showed = True
                    self.driver.show_float_window(True)
                    self.driver.logger.debug("show float window")
                    time.sleep(1.0)
                    continue
                return True
            time.sleep(1.0)

        self.driver.uiautomator.stop()
        return False