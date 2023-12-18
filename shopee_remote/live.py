import random
import logging
import time

from uiautomator2 import Device
from driver import open_driver
from helper.file import save_error
from helper.certifi import override_req_cacert
from steps.account_steps import AccountSteps
from steps.co_steps import CoSteps
from steps.live_steps import LiveSteps


logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

class LiveBot:
    live_steps: LiveSteps
    co_steps: CoSteps
    account_steps: AccountSteps

    def __init__(self, driver: Device) -> None:
        self.co_steps = CoSteps(driver=driver)
        self.live_steps = LiveSteps(driver=driver)
        self.account_steps = AccountSteps(driver=driver)

    def open_live(self, url: str) -> None:
        self.live_steps.open_live(url=url)

    def add_to_bucket(self):
        self.live_steps.open_live_bucket()
        self.live_steps.add_to_bucket()
        if self.co_steps.check_variant():
            self.co_steps.select_variant_alternative()
        self.live_steps.back(1)


    def open_comment(self) -> list[str]:
        with open("./comment.txt", "r") as file:
            content = file.read()
            data = content.split("\n")
    
        return data

    def send_comment(self, comments: list[str]) -> None:
        for comment in comments:
            self.live_steps.send_comment(comment=comment)

    def tap_love(self, duration: int = 5) -> None:
        self.live_steps.tap_love(duration=duration)

    def open_tab_menu(self) -> None:
        self.co_steps.back(1)

    def change_account(self) -> None:
        self.account_steps.to_account()
        self.account_steps.to_setting()
        self.account_steps.to_switch_account()
        self.account_steps.switching_account()

    def close_app(self):
        self.live_steps.close_app()



def main():
    input_url = input("Masukkan url live : ")
    url = input_url.strip()

    driver = open_driver()

    
    bot = LiveBot(driver=driver)

    try:
        while True:
            logging.info("Menuju live")
            bot.open_live(url=url)

            logging.info("Tap love")
            count_tap = random.randint(3,7)
            bot.tap_love(count_tap)

            list_comment = bot.open_comment()
            count_comment = random.randint(1, 3)
            comments = random.sample(list_comment, count_comment)

            logging.info("Sending comment")
            bot.send_comment(comments=comments)

            logging.info("Add product to bucket")
            bot.add_to_bucket()

            bot.open_tab_menu()

            logging.info("Change account")
            bot.change_account()
    except Exception as e:
        print(e)
        save_error(e)
    finally:
        # bot.close_app()
        print("selesai")






















if __name__ == "__main__":
    override_req_cacert()


    main()