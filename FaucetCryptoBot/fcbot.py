from selenium import webdriver
from selenium.webdriver import Chrome

from .utils import *
from .log import Log
from .xpath import *
from .config import *


class FaucetCryptoBot:
    def __init__(self):

        self.user = user
        self.log = Log()
        self.driver = Chrome(options=self._get_opts(), executable_path=DRIVER_PATH)
        self.dash_board_url = "https://faucetcrypto.com/dashboard"
        self.banner = draw_banner()
        self.log.write_log(
            "browser", f"starting browser session: {self.driver.session_id}"
        )
        self.main_window = self.driver.current_window_handle
        self.debug = DEBUG

    def _get_opts(self):

        opts = webdriver.chrome.options.Options()

        if DRIVER_MODE == "headless":
            opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.binary_location = BROWSER_BINARY_LOCATION
        opts.add_argument("--ignore-certificate-erors")
        opts.add_argument("window-size=1920,1080")
        opts.add_argument("start-maximized")
        opts.add_argument("user-data-dir=" + USER_DATA_DIR)
        opts.add_argument("disable-infobars")
        opts.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        return opts

    def quit(self):
        self.driver.close()

    def sleep(self, mins):

        import time

        self.log.write_log("bot", self.log.blue_text(f"Sleeping for {mins}m"))
        time.sleep(60 * int(mins))

    def error_handler(self, msg):
        self.log.error_log(msg)

    def _click(self, element, msg="placeholder"):

        self.log.write_log(f"clicking on {msg}")
        self.driver.find_element_by_xpath(element).click()

    def _random_wait(self, t_min, t_max):

        import time
        import random

        random_time = random.randrange(t_min, t_max)
        self.log.write_log("bot", f"Waiting for {random_time} sec")
        time.sleep(random_time)

    def __switch_tab(self):

        self._random_wait(2, 4)
        visible_windows = self.driver.window_handles

        for window in visible_windows:
            if window != self.main_window:
                self.driver.switch_to.window(window)
                self.driver.close()
                self.driver.switch_to.window(self.main_window)

    def __get_xpath_elem(self, element):

        try:
            return self.driver.find_element_by_xpath(element)
        except Exception as e:

            if self.debug:
                self.log.write_log("warning", e)
            else:
                self.error_handler(e)
                pass

    def __check_main_reward_availability(self):

        if (
            "ready"
            in self.__get_xpath_elem(main_reward["main-reward-dash-link"]).text.lower()
        ):
            return True
        else:
            return False

    def __captcha_check(self, captcha_block):

        if "good person" in self.__get_xpath_elem(captcha_block).text.lower():
            self.log.write_log("success", "Havent caught me yet")
            return True
        else:
            self.log.write_log("warning", "Oops looks like i'm caught")
            return False

    def get_user_balance(self):

        if self.driver.current_url != self.dash_board_url:
            self.driver.get(self.dash_board_url)

        coin_balance = self.__get_xpath_elem(user["user-coin-balance"]).text
        btc_balance = self.__get_xpath_elem(user["user-btc-balance"]).text
        balance_msg = "User balance: " + self.log.yellow_text(
            coin_balance + "/" + btc_balance
        )
        self.log.write_log("bot", balance_msg)

    def get_user_level(self):

        user_level = self.__get_xpath_elem(user["user-level"]).text
        user_level_percent = self.__get_xpath_elem(user["user-level-percent"]).text
        level_msg = "User level: " + self.log.blue_text(
            user_level + "/" + user_level_percent
        )
        self.log.write_log("bot", level_msg)

    def get_current_coin_rate(self):

        coin_rate = self.__get_xpath_elem(user["user-coin-rate"]).text
        coin_rate_msg = "Coin rate: " + self.log.yellow_text(coin_rate)
        self.log.write_log("bot", coin_rate_msg)

    def _login_handler(self, email, password):

        user_email = self.__get_xpath_elem(user["user-email-field"]).send_keys(email)
        user_password = self.__get_xpath_elem(user["user-password-field"]).send_keys(
            password
        )
        user_remember_me = self._click(user["user-remember-me"])
        self._click(user["user-login-btn"])

    def get_main_reward(self):

        self.log.write_log("bot", self.log.green_text("MAIN REWARD"))
        if self.driver.current_url != self.dash_board_url:
            self.driver.get(self.dash_board_url)

        try:
            if self.__check_main_reward_availability():
                self.log.write_log("success", "Main reward is available")

                self._click(
                    main_reward["main-reward-dash-link"], "main reward dash link"
                )
                self._random_wait(3, 5)

                if self.__captcha_check(main_reward["main-reward-captcha-block"]):
                    self._random_wait(14, 16)
                    self._click(
                        main_reward["main-reward-claim-btn"], "main reward claim button"
                    )

                    self.log.write_log("success", "Collected the main reward")
                    self._random_wait(3, 5)

            else:
                self.log.write_log("bot", "Main reward is not available")

        except Exception as e:

            if self.debug:
                self.log.write_log("warning", e)
            else:
                self.error_handler(e)
                pass

    def get_ptc_ads(self):

        self.log.write_log("bot", self.log.green_text("PTC ADS"))
        if self.driver.current_url != self.dash_board_url:
            self.driver.get(self.dash_board_url)

        self._click(ptc_ads["ptc-ads-dash-link"])
        self._random_wait(3, 5)

        total_ads_amount = self.__get_xpath_elem(ptc_ads["ptc-ads-total-amount"]).text
        total_ads_amount_msg = f"Total ads amount: {total_ads_amount}"
        self.log.write_log("bot", total_ads_amount_msg)

        completed_ads = self.__get_xpath_elem(ptc_ads["ptc-ads-completed-ads"]).text
        completed_ads_msg = f"Completed ads: {completed_ads}"
        self.log.write_log("bot", completed_ads_msg)

        available_ads = self.__get_xpath_elem(ptc_ads["ptc-ads-available-ads"]).text
        available_ads_msg = f"Available ads: {available_ads}"
        self.log.write_log("bot", available_ads_msg)

        earnable_coins = self.__get_xpath_elem(ptc_ads["ptc-ads-earnable-coins"]).text
        earnable_coins_msg = f"Earnable coins: {earnable_coins}"
        self.log.write_log("bot", earnable_coins_msg)

        if int(available_ads) > 0:
            for ad_div_block_no in range(1, int(available_ads) + 1):

                try:
                    ad_title = self.__get_xpath_elem(ptc_ads["ptc-ads-title"]).text
                    ad_title_msg = f"Ad [{ad_div_block_no}] {ad_title}"
                    self.log.write_log("bot", ad_title_msg)

                    ad_comp_time = self.__get_xpath_elem(
                        ptc_ads["ptc-ads-completion-time"]
                    ).text[:2]
                    ad_comp_time_msg = f"Ad completion time: {ad_comp_time} sec"
                    self.log.write_log("bot", ad_comp_time_msg)

                    ad_rew_coin = self.__get_xpath_elem(
                        ptc_ads["ptc-ads-reward-coins"]
                    ).text
                    ad_rew_coin_msg = f"Ad reward: {ad_rew_coin} coins"
                    self.log.write_log("bot", ad_rew_coin_msg)

                    self._click(ptc_ads["ptc-ads-watch-button"])
                    self._random_wait(2, 4)

                    if self.__captcha_check(ptc_ads["ptc-ads-captcha-block"]):
                        self._random_wait(13, 16)
                        self._click(ptc_ads["ptc-ads-reward-claim-btn"])

                        self._random_wait(int(ad_comp_time) + 5, int(ad_comp_time) + 7)
                        self._click(ptc_ads["ptc-ads-continue-btn"])
                        self.__switch_tab()
                        self.log.write_log(
                            "bot", f"Fininshed {ad_title} ad successfully"
                        )
                        self._random_wait(2, 4)

                except Exception as e:

                    if self.debug:
                        self.log.write_log("warning", e)
                    else:
                        self.error_handler(e)
                        pass

    def get_shortlink_ads(self):

        self.log.write_log("bot", self.log.green_text("SHORTLINK ADS"))
        if self.driver.current_url != self.dash_board_url:
            self.driver.get(self.dash_board_url)

        self._click(shortlinks["general"]["shortlinks-dash-link"])
        self._random_wait(3, 5)

        shortlinks_amount = self.__get_xpath_elem(
            shortlinks["general"]["shortlinks-amount"]
        ).text
        shortlinks_amount_msg = f"Total shortlinks: {shortlinks_amount}"
        self.log.write_log("bot", shortlinks_amount_msg)

        shortlinks_completed = self.__get_xpath_elem(
            shortlinks["general"]["shortlinks-completed"]
        ).text
        shortlinks_completed_msg = f"Completed shortlinks: {shortlinks_completed}"
        self.log.write_log("bot", shortlinks_completed_msg)
        shortlinks_available = self.__get_xpath_elem(
            shortlinks["general"]["shortlinks-available"]
        ).text
        shortlinks_available_msg = f"Available shortlinks: {shortlinks_available}"
        self.log.write_log("bot", shortlinks_available_msg)

        shortlinks_earnable = self.__get_xpath_elem(
            shortlinks["general"]["shortlinks-earnable-coins"]
        ).text
        shortlinks_earnable_msg = f"Total earnable coins: {shortlinks_earnable}"
        self.log.write_log("bot", shortlinks_earnable_msg)

        def switch(link):
            link = str(link).lower()

            def exe_io():
                view_count = self.__get_xpath_elem(
                    shortlinks["exe.io"]["shortlinks-view-count"]
                ).text
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log("bot", view_count_msg)

                reward_coin = self.__get_xpath_elem(
                    shortlinks["exe.io"]["shortlinks-reward-coin"]
                ).text
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log("bot", reward_coin_msg)
                self._random_wait(5, 10)
                pass

            def fc_lc():
                view_count = self.__get_xpath_elem(
                    shortlinks["fc.lc"]["shortlinks-view-count"]
                ).text
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log("bot", view_count_msg)

                reward_coin = self.__get_xpath_elem(
                    shortlinks["fc.lc"]["shortlinks-reward-coin"]
                ).text
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log("bot", reward_coin_msg)
                self._random_wait(5, 10)
                pass

            def sh_faucetcrypto_com():
                view_count = self.__get_xpath_elem(
                    shortlinks["sh.faucetcrypto.com"]["shortlinks-view-count"]
                ).text
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log("bot", view_count_msg)

                reward_coin = self.__get_xpath_elem(
                    shortlinks["sh.faucetcrypto.com"]["shortlinks-reward-coin"]
                ).text
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log("bot", reward_coin_msg)

                self._click(shortlinks["sh.faucetcrypto.com"]["shortlinks-claim-btn"])
                self._random_wait(15, 18)

                orig_url = self.driver.current_url
                self._click(shortlinks["general"]["shortlinks-reward-claim-btn"])
                if self.driver.current_url == orig_url:
                    self._click(shortlinks["general"]["shortlinks-reward-claim-btn"])
                self._random_wait(5, 7)

                try:
                    step_count = self.__get_xpath_elem(
                        faucet["faucet-current-step"]
                    ).text

                    for i in range(int(step_count[2])):
                        step_count_msg = f"Current step: {i+1}/{step_count[2]}"
                        self.log.write_log(
                            "bot",
                            self.log.yellow_text(
                                f"Current step count {step_count_msg}"
                            ),
                        )

                        self._random_wait(5, 7)
                        source = self.driver.execute_script("goto()")
                        self._random_wait(3, 5)

                except Exception as e:

                    if self.debug:
                        self.log.write_log("warning", e)
                    else:
                        self.error_handler(e)
                        pass

            def sh_faucet_gold():
                view_count = self.__get_xpath_elem(
                    shortlinks[link]["shortlinks-view-count"]
                ).text
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log(view_count_msg)

                reward_coin = self.__get_xpath_elem(
                    shortlinks[link]["shortlinks-reward-coin"]
                ).text
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log(reward_coin_msg)

                self._click(shortlinks["sh.faucet.gold"]["shortlinks-claim-btn"])
                self._random_wait(15, 18)

                orig_url = self.driver.current_url
                self._click(shortlinks["general"]["shortlinks-reward-claim-btn"])
                if self.driver.current_url == orig_url:
                    self._click(shortlinks["general"]["shortlinks-reward-claim-btn"])
                self._random_wait(5, 7)

                try:
                    step_count = self.__get_xpath_elem(
                        faucet["faucet-current-step"]
                    ).text

                    for i in range(int(step_count[2])):
                        step_count_msg = f"Current step: {i+1}/{step_count[2]}"
                        self.log.write_log(
                            "bot",
                            self.log.yellow_text(
                                f"Current step count {step_count_msg}"
                            ),
                        )

                        self._random_wait(5, 7)
                        source = self.driver.execute_script("goto()")
                        self._random_wait(3, 5)

                except Exception as e:

                    if self.debug:
                        self.log.write_log("warning", e)
                    else:
                        self.error_handler(e)
                        pass

            def sh_claim4_fun():
                view_count = self.__get_xpath_elem(
                    shortlinks[link]["shortlinks-view-count"]
                ).text
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log(view_count_msg)

                reward_coin = self.__get_xpath_elem(
                    shortlinks[link]["shortlinks-reward-coin"]
                ).text
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log(reward_coin_msg)

                self._click(shortlinks["sh.claim4.fun"]["shortlinks-claim-btn"])
                self._random_wait(15, 18)

                orig_url = self.driver.current_url
                self._click(shortlinks["general"]["shortlinks-reward-claim-btn"])
                if self.driver.current_url == orig_url:
                    self._click(shortlinks["general"]["shortlinks-reward-claim-btn"])
                self._random_wait(5, 7)

                try:
                    step_count = self.__get_xpath_elem(
                        faucet["faucet-current-step"]
                    ).text

                    for i in range(int(step_count[2])):
                        step_count_msg = f"Current step: {i+1}/{step_count[2]}"
                        self.log.write_log(
                            "bot",
                            self.log.yellow_text(
                                f"Current step count {step_count_msg}"
                            ),
                        )
                        self._random_wait(5, 7)
                        source = self.driver.execute_script("goto()")
                        self._random_wait(3, 5)

                except Exception as e:

                    if self.debug:
                        self.log.write_log("warning", e)
                    else:
                        self.error_handler(e)
                        pass

            def default():
                self.log.write_log("warning", "Invalid option")

            dict = {
                "exe.io": exe_io,
                "fc.lc": fc_lc,
                "sh.faucetcrypto.com": sh_faucetcrypto_com,
                "sh.faucet.gold": sh_faucet_gold,
                "sh.claim4.fun": sh_claim4_fun,
            }
            dict.get(link, default)()

        for links in shortlinks:
            if links.lower() == "general":
                continue

            try:
                view_count = self.__get_xpath_elem(
                    shortlinks[links]["shortlinks-view-count"]
                ).text[0]
                if int(view_count) > 0:
                    self.log.write_log("bot", self.log.green_text(links.upper()))
                    switch(links)

            except Exception as e:

                if self.debug:
                    self.log.write_log("warning", e)
                else:
                    self.error_handler(e)
