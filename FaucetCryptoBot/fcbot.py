import os
import pickle
from datetime import datetime
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from .utils import *
from .log import Log
from .xpath import *


class FaucetCryptoBot:
    def __init__(self):

        self.debug = self._configParser()[5]
        self.proxy = self._configParser()[6]
        self.user_mail = self._configParser()[3]
        self.user_pswd = self._configParser()[4]
        self.driver_path = self._configParser()[1]
        self.browser_mode = self._configParser()[0]
        self.browser_binary_location = self._configParser()[2]

        self.log = Log()
        self.login_url = "https://faucetcrypto.com/login"
        self.ptc_url = "https://faucetcrypto.com/ptc/list"
        self.dash_board_url = "https://faucetcrypto.com/dashboard"
        self.shortlink_url = "https://faucetcrypto.com/shortlink/list"
        self.faucet_url = "https://faucetcrypto.com/task/faucet-claim"
        self.achievement_url = "https://faucetcrypto.com/achievement/list"
        self.banner = draw_banner()
        self.driver = Chrome(options=self._get_opts(), executable_path=self.driver_path)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.log.write_log(
            "browser", f"starting browser session: {self.driver.session_id}"
        )
        self.main_window = self.driver.current_window_handle

    def _get_opts(self):

        opts = webdriver.chrome.options.Options()
        prefs = {"profile.managed_default_content_settings.images": 2}

        if self.browser_mode == "headless":
            opts.add_argument("--headless")
        if self.proxy != "":
            opts.add_argument("--proxy-server=%s" % self.proxy)

        # Chrome optional flags
        opts.add_argument("--no-sandbox")
        opts.add_argument("no-first-run")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--log-level-3")
        opts.add_argument("--disable-dev-shm-usage")
        opts.binary_location = self.browser_binary_location
        opts.add_argument("--disable-notifications")
        opts.add_argument("--ignore-certificate-erors")
        opts.add_argument("no-default-browser-check")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--start-maximized")
        opts.add_argument("--disable-infobars")
        opts.add_argument("--user-agent={UserAgent().random}")
        opts.add_argument("--disable-blink-features")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        opts.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option("useAutomationExtension", False)

        # Chrome experimental flags
        if self.browser_mode == "headless":
            opts.add_experimental_option("prefs", prefs)

        return opts

    def __exWaitS(self):

        # Implicit waiting functions
        return WebDriverWait(self.driver, 5)

    def __exWaitM(self):

        # Implicit waiting functions
        return WebDriverWait(self.driver, 10)

    def __exWaitL(self):

        # Implicit waiting functions
        return WebDriverWait(self.driver, 20)

    def __exWaitSL(self):

        # Implicit waiting functions
        return WebDriverWait(self.driver, 60)

    def _configParser(self):

        # Gather all the data from the config file
        # and create respective options for the chrome
        # driver
        from configparser import ConfigParser

        config = ConfigParser()
        config.readfp(open(f"config.cfg"))

        browser_mode = config.get("Browser", "browser-mode")
        driver_path = config.get("Browser", "driver-path")
        browser_binary_location = config.get("Browser", "browser-binary-location")

        user_mail = config.get("User", "mail")
        user_pswd = config.get("User", "password")

        debug = config.getboolean("Misc", "debug")
        proxy = config.get("Misc", "proxy")

        return (
            browser_mode,
            driver_path,
            browser_binary_location,
            user_mail,
            user_pswd,
            debug,
            proxy,
        )

    def quit(self):

        # Check for any open tabs and close all of them
        for window in self.driver.window_handles:
            self.driver.switch_to.window(window)
            self.driver.close()

    def sleep(self, mins):

        # Put the bot to sleep for some time to avoid triggering
        # captchas and also to give the bot a break
        import time

        self.log.write_log("bot", self.log.blue_text(f"Sleeping for {mins}m"))
        time.sleep(60 * int(mins))

    def error_handler(self, msg):

        # Handles any stupid errors that might occur
        # and write them to the error file rather than
        # dumping everything to the terminal
        self.log.error_log(msg)

    def _click(self, element, msg=" "):

        # This functions job is to just click stuff
        self.log.write_log("bot", msg)
        element.click()

    def _random_wait(self, t_min, t_max, msg=""):

        import time
        import random

        random_time = random.randrange(t_min, t_max)
        self.log.write_log("bot", msg)
        time.sleep(random_time)

    def __switch_tab(self):

        # Use this function to check if there are any
        # unwanted tabs that are open. if it finds one
        # switch to that tab and close it
        self._random_wait(
            2, 4, "Closing tabs we don't want chrome to eat your RAM now do we"
        )
        visible_windows = self.driver.window_handles

        for window in visible_windows:
            if window != self.main_window:
                self.driver.switch_to.window(window)
                self.driver.close()
                self.driver.switch_to.window(self.main_window)

    def __get_xpath_elem(self, element):

        # Returns the element based on the respective xpath
        try:
            return self.driver.find_element_by_xpath(element)
        except Exception as e:

            if self.debug:
                self.log.write_log("warning", e)
            else:
                self.error_handler(e)
                pass

    def __check_main_reward_availability(self):

        # This function just checks if the main reward is available
        # and returns a boolean
        if (
            "ready"
            in self.__get_xpath_elem(main_reward["main-reward-dash-link"]).text.lower()
        ):
            return True
        else:
            return False

    def __captcha_check(self, captcha_block):

        # Checks if the captcha has been triggered and returns
        # the respective boolean
        if (
            "good person"
            in self.__exWaitM()
            .until(
                ec.presence_of_element_located(
                    (By.XPATH, captcha_block),
                ),
                message="timeout trying to find captcha block",
            )
            .text.lower()
        ):
            self.log.write_log("success", "Havent caught me yet")
            return True
        else:
            self.log.write_log("warning", "Oops looks like i'm caught")
            self.driver.get(dashboard_url)
            self.sleep(60)

    def _modal_handler(self):

        # Closes the annoying modal and chat window
        # that pops up every single time.
        try:
            modalClose = self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, user["user-modal-close"])),
                message="timeout trying to find modal",
            )
            self._click(modalClose, "closing modal window")
            chatClose = self.__exWaitS().until(
                ec.presence_of_element_located((By.XPATH, user["user-chat-close"])),
                message="timeout trying to find chat",
            )
            self._click(chatClose, "closing chat window")

        except Exception as e:
            pass

    def get_user_balance(self):

        # Returns the coin balance of the current user
        if self.driver.current_url != self.dash_board_url:
            self.driver.get(self.dash_board_url)

        coin_balance = self.__get_xpath_elem(user["user-coin-balance"]).text
        btc_balance = self.__get_xpath_elem(user["user-btc-balance"]).text
        balance_msg = "User balance: " + self.log.yellow_text(
            coin_balance + "/" + btc_balance
        )
        self.log.write_log("bot", balance_msg)

    def get_user_level(self):

        # Returns the exp level of the current user
        user_level = self.__get_xpath_elem(user["user-level"]).text
        user_level_percent = self.__get_xpath_elem(user["user-level-percent"]).text
        level_msg = "User level: " + self.log.blue_text(
            user_level + "/ " + user_level_percent
        )
        self.log.write_log("bot", level_msg)

    def get_current_coin_rate(self):

        # Returns the present coin rate as given by the site
        coin_rate = self.__get_xpath_elem(user["user-coin-rate"]).text
        coin_rate_msg = "Coin rate: " + self.log.yellow_text(coin_rate)
        self.log.write_log("bot", coin_rate_msg)

    def login_handler(self, remember=True, cookies=True):

        # checks if the cookie file of the user is present
        # if not login with the credentials provided in the
        # config file
        if self.driver.current_url == self.dash_board_url:
            pass

        else:
            self.driver.get(self.login_url)
            try:
                with open("cookies", "rb") as f:
                    cookies = pickle.load(f)
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
                self.driver.refresh()

            except Exception as e:

                emailField = self.__exWaitS().until(
                    ec.presence_of_element_located(
                        (By.XPATH, user["user-email-field"])
                    ),
                    message="timeout trying to find email field",
                )
                emailField.send_keys(self.user_mail)
                pswdField = self.__exWaitS().until(
                    ec.presence_of_element_located(
                        (By.XPATH, user["user-password-field"])
                    ),
                    message="timeout trying to find password field",
                )
                pswdField.send_keys(self.user_pswd)

                if remember:
                    remMe = self.__exWaitS().until(
                        ec.presence_of_element_located(
                            (By.XPATH, user["user-remember-me"])
                        ),
                        message="timeout trying to find remember me checkbox",
                    )
                    self._click(remMe, "checking remember me")

                loginBtn = self.__exWaitS().until(
                    ec.element_to_be_clickable((By.XPATH, user["user-login-btn"])),
                    message="timeout trying to find the login button",
                )
                self._click(loginBtn, "clicking login button")

                if cookies:
                    if self.driver.current_url == self.dash_board_url:
                        with open("cookies", "wb") as f:
                            pickle.dump(self.driver.get_cookies(), f)

    def get_main_reward(self):

        # Logic to collect the main faucet reward
        self.log.write_log("bot", self.log.green_text("MAIN REWARD"))
        if self.driver.current_url != self.dash_board_url:
            self.driver.get(self.dash_board_url)

        # if the bot was able to login successfully then save the
        # cookies for further logins
        self._modal_handler()
        if not os.path.exists("cookies"):
            with open("cookies", "wb") as f:
                pickle.dump(self.driver.get_cookies(), f)

        try:
            if self.__check_main_reward_availability():
                self.log.write_log("success", "Main reward is available")

                self.driver.get(self.faucet_url)
                if self.__captcha_check(main_reward["main-reward-captcha-block"]):

                    # checks if the claim button has become active if then click
                    # on it and recieve the main reward
                    mainRewardClaimBtnTxt = self.__exWaitL().until(
                        ec.text_to_be_present_in_element(
                            (By.XPATH, main_reward["main-reward-claim-btn"]),
                            "Get Reward",
                        ),
                        message="timeout trying to find faucet claim button",
                    )
                    mainRewardClaimBtn = self.__exWaitS().until(
                        ec.element_to_be_clickable(
                            (By.XPATH, main_reward["main-reward-claim-btn"])
                        ),
                        message="timeout trying to find faucet claim btn",
                    )

                    self._click(
                        mainRewardClaimBtn, "clicking on main reward claim button"
                    )

                    # this wait is needed because the site dosent register the
                    # button click and takes some seconds or sometimes some minutes
                    # for it to claim properly
                    self._random_wait(5, 7, "waiting for the click to be registered")
                    self.log.write_log("success", "Collected the main reward")

            else:
                self.log.write_log("bot", "Main reward is not available")

        except Exception as e:

            if self.debug:
                self.log.write_log("warning", e)
            else:
                self.error_handler(e)
                pass

    def get_achievements(self):

        self.log.write_log("bot", self.log.green_text("ACHIEVEMENTS"))
        if self.driver.current_url != self.achievement_url:
            self.driver.get(self.achievement_url)

        try:
            # Total achievements available
            total_ach_amount = (
                self.__exWaitM()
                .until(
                    ec.presence_of_element_located(
                        (By.XPATH, achievement["achievement-total-amount"])
                    ),
                    message="timeout trying to find total achievement amount",
                )
                .text
            )
            total_ach_amount_msg = f"Total achievements amount: {total_ach_amount}"
            self.log.write_log("bot", total_ach_amount_msg)

            # Available achievement amount
            ava_ach_amount = (
                self.__exWaitM()
                .until(
                    ec.presence_of_element_located(
                        (By.XPATH, achievement["achievement-available-amount"])
                    ),
                    message="timeout trying to find available achievement amount",
                )
                .text
            )
            ava_ach_amount_msg = f"Available achievements amount: {ava_ach_amount}"
            self.log.write_log("bot", ava_ach_amount_msg)

            # Completed achievements amount
            comp_ach_amount = (
                self.__exWaitM()
                .until(
                    ec.presence_of_element_located(
                        (By.XPATH, achievement["achievement-completed-amount"])
                    ),
                    message="timeout trying to find completed achievement amount",
                )
                .text
            )
            comp_ach_amount_msg = f"Completed achievements amount: {comp_ach_amount}"
            self.log.write_log("bot", comp_ach_amount_msg)

            # Unlocked achievements amount
            unl_ach_amount = (
                self.__exWaitM()
                .until(
                    ec.presence_of_element_located(
                        (By.XPATH, achievement["achievement-unlocked-amount"])
                    ),
                    message="timeout trying to find unlocked achievement amount",
                )
                .text
            )
            unl_ach_amount_msg = f"Unlocked achievements amount: {unl_ach_amount}"
            self.log.write_log("bot", unl_ach_amount_msg)

            try:
                for _gpx in [
                    "achievement-level",
                    "achievement-ptc",
                    "achievement-shortlinks",
                ]:
                    achievements = self.__exWaitM().until(
                        ec.presence_of_element_located((By.XPATH, achievement[_gpx])),
                        message=f"timeout finding {_gpx}",
                    )
                    self.driver.click(achievements)
                    grid = self.__exWaitM().until(
                        ec.presence_of_element_located(
                            (By.XPATH, achievement["achievement-grid"])
                        ),
                        message="timeout finding achievement grid.",
                    )
                    _apxs = grid.find_elements_by_tag_name("a")
                    for _apx in _apxs:
                        self.driver.click(_apx)
            except:
                pass

        except Exception as e:
            if self.debug:
                self.log.write_log("warning", e)
            else:
                self.error_handler(e)
                pass

    def get_ptc_ads(self):

        self.log.write_log("bot", self.log.green_text("PTC ADS"))
        if self.driver.current_url != self.ptc_url:
            self.driver.get(self.ptc_url)

        # Ptc ads amount
        total_ads_amount = (
            self.__exWaitM()
            .until(
                ec.presence_of_element_located(
                    (By.XPATH, ptc_ads["ptc-ads-total-amount"])
                ),
                message="timeout trying to find total ads amount",
            )
            .text
        )
        total_ads_amount_msg = f"Total ads amount: {total_ads_amount}"
        self.log.write_log("bot", total_ads_amount_msg)

        # Ptc completed ads
        completed_ads = (
            self.__exWaitM()
            .until(
                ec.presence_of_element_located(
                    (By.XPATH, ptc_ads["ptc-ads-completed-ads"])
                ),
                message="timeout trying to find completed ads",
            )
            .text
        )
        completed_ads_msg = f"Completed ads: {completed_ads}"
        self.log.write_log("bot", completed_ads_msg)

        # Ptc available ads
        available_ads = (
            self.__exWaitM()
            .until(
                ec.presence_of_element_located(
                    (By.XPATH, ptc_ads["ptc-ads-available-ads"])
                ),
                message="timeout trying to find available ads",
            )
            .text
        )
        available_ads_msg = f"Available ads: {available_ads}"
        self.log.write_log("bot", available_ads_msg)

        # Ptc earnable coins
        earnable_coins = (
            self.__exWaitM()
            .until(
                ec.presence_of_element_located(
                    (By.XPATH, ptc_ads["ptc-ads-earnable-coins"])
                ),
                message="timeout trying to find earnable-coins",
            )
            .text
        )
        earnable_coins_msg = f"Earnable coins: {earnable_coins}"
        self.log.write_log("bot", earnable_coins_msg)

        if int(available_ads) > 0:
            for ad_div_block_no in range(0, int(available_ads) + 1):

                try:
                    # Ptc ads title
                    ad_title = (
                        self.__exWaitS()
                        .until(
                            ec.presence_of_element_located(
                                (By.XPATH, ptc_ads["ptc-ads-title"])
                            ),
                            message="timeout trying to find ad title",
                        )
                        .text
                    )
                    ad_title_msg = f"Ad [{int(ad_div_block_no) + 1}] {ad_title}"
                    self.log.write_log("bot", ad_title_msg)

                    # Ptc ads completion time
                    ad_comp_time = (
                        self.__exWaitS()
                        .until(
                            ec.presence_of_element_located(
                                (By.XPATH, ptc_ads["ptc-ads-completion-time"])
                            ),
                            message="timeout trying to find ad time",
                        )
                        .text[:2]
                    )
                    ad_comp_time_msg = f"Ad completion time: {ad_comp_time} sec"
                    self.log.write_log("bot", ad_comp_time_msg)

                    # Ptc ads reward
                    ad_rew_coin = (
                        self.__exWaitS()
                        .until(
                            ec.presence_of_element_located(
                                (By.XPATH, ptc_ads["ptc-ads-reward-coins"])
                            ),
                            message="timeout trying to ad reward coins",
                        )
                        .text
                    )
                    ad_rew_coin_msg = f"Ad reward: {ad_rew_coin} coins"
                    self.log.write_log("bot", ad_rew_coin_msg)

                    ptcAdsWatchBtn = self.__exWaitS().until(
                        ec.element_to_be_clickable(
                            (By.XPATH, ptc_ads["ptc-ads-watch-button"])
                        ),
                        message="timeout trying to find ad watch button",
                    )
                    self._click(ptcAdsWatchBtn, "clicking on ptc watch button")

                    if self.__captcha_check(ptc_ads["ptc-ads-captcha-block"]):
                        ptcRewardClaimBtnTxt = self.__exWaitL().until(
                            ec.text_to_be_present_in_element(
                                (By.XPATH, ptc_ads["ptc-ads-reward-claim-btn"]),
                                "Get Reward",
                            ),
                            message="timeout trying to find ad captcha block",
                        )
                        ptcRewardClaimBtn = self.__exWaitS().until(
                            ec.element_to_be_clickable(
                                (By.XPATH, ptc_ads["ptc-ads-reward-claim-btn"])
                            ),
                            message="timeout trying to find ad claim button",
                        )
                        self._click(
                            ptcRewardClaimBtn, "clicking on ptc reward claim button"
                        )

                        self._random_wait(3, 5, "waiting for the page to load")
                        if "ptc-advertisement" in self.driver.current_url:
                            self.driver.refresh()
                            continue

                        if "faucetcrypto" not in self.driver.current_url:
                            self.log.write_log(
                                "bot", "Looks like we've got a sneaky ad boy."
                            )
                            self.driver.save_screenshot("Liessss!.png")
                            self.driver.get(self.ptc_url)
                            continue

                        ptcContinueBtnTxt = self.__exWaitSL().until(
                            ec.text_to_be_present_in_element(
                                (By.XPATH, ptc_ads["ptc-ads-continue-btn"]),
                                "Continue",
                            ),
                            message="timeout trying to find ad continue button",
                        )
                        ptcContinueBtn = self.__exWaitL().until(
                            ec.element_to_be_clickable(
                                (By.XPATH, ptc_ads["ptc-ads-continue-btn"])
                            ),
                            message="timeout trying to find ad continue button",
                        )
                        self._click(ptcContinueBtn, "clicking on ptc continue button")
                        self.__switch_tab()
                        self.log.write_log(
                            "success", f"Fininshed {ad_title} ad successfully"
                        )

                except Exception as e:

                    if self.debug:
                        self.log.write_log("warning", e)
                    else:
                        self.error_handler(e)
                        pass

    def get_shortlink_ads(self):

        self.log.write_log("bot", self.log.green_text("SHORTLINK ADS"))
        if self.driver.current_url != self.shortlink_url:
            self.driver.get(self.shortlink_url)

        # Shortlinks amount
        shortlinks_amount = (
            self.__exWaitM()
            .until(
                ec.presence_of_element_located(
                    (By.XPATH, shortlinks["general"]["shortlinks-amount"])
                ),
                message="timeout trying to find shortlinks amount",
            )
            .text
        )
        shortlinks_amount_msg = f"Total shortlinks: {shortlinks_amount}"
        self.log.write_log("bot", shortlinks_amount_msg)

        # Shortlinks completed
        shortlinks_completed = (
            self.__exWaitM()
            .until(
                ec.presence_of_element_located(
                    (By.XPATH, shortlinks["general"]["shortlinks-completed"])
                ),
                message="timeout trying to find shortlinks completed",
            )
            .text
        )
        shortlinks_completed_msg = f"Completed shortlinks: {shortlinks_completed}"
        self.log.write_log("bot", shortlinks_completed_msg)

        # Shortlinks available
        shortlinks_available = (
            self.__exWaitM()
            .until(
                ec.presence_of_element_located(
                    (By.XPATH, shortlinks["general"]["shortlinks-available"])
                ),
                message="timeout trying to find shortlinks available",
            )
            .text
        )
        shortlinks_available = self.__get_xpath_elem(
            shortlinks["general"]["shortlinks-available"]
        ).text
        shortlinks_available_msg = f"Available shortlinks: {shortlinks_available}"
        self.log.write_log("bot", shortlinks_available_msg)

        # Shortlinks earnable
        shortlinks_earnable = (
            self.__exWaitM()
            .until(
                ec.presence_of_element_located(
                    (By.XPATH, shortlinks["general"]["shortlinks-earnable-coins"])
                ),
                message="timeout trying to find shortlinks earnable",
            )
            .text
        )
        shortlinks_earnable_msg = f"Total earnable coins: {shortlinks_earnable}"
        self.log.write_log("bot", shortlinks_earnable_msg)

        # Scroll all the shortlinks in to view
        self.driver.execute_script("window.scrollTo(0,1000)")

        def switch(link):
            link = str(link).lower()

            def exe_io():

                # exe.io viewcount
                view_count = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (By.XPATH, shortlinks["exe.io"]["shortlinks-view-count"])
                        ),
                        message="timeout trying to find exe.io viewcount",
                    )
                    .text
                )
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log("bot", view_count_msg)

                # exe.io reward
                reward_coin = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (By.XPATH, shortlinks["exe.io"]["shortlinks-reward-coin"])
                        ),
                        message="timeout trying to find exe.io reward",
                    )
                    .text
                )
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log("bot", reward_coin_msg)
                self._random_wait(5, 10, "Sorry mate can't do this.")
                pass

            def fc_lc():

                # fc.lc viewcount
                view_count = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (By.XPATH, shortlinks["fc.lc"]["shortlinks-view-count"])
                        ),
                        message="timeout trying to find fc.lc viewcount",
                    )
                    .text
                )
                view_count = self.__get_xpath_elem(
                    shortlinks["fc.lc"]["shortlinks-view-count"]
                ).text
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log("bot", view_count_msg)

                # fc.lc reward
                reward_coin = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (By.XPATH, shortlinks["fc.lc"]["shortlinks-reward-coin"])
                        ),
                        message="timeout trying to find fc.lc reward",
                    )
                    .text
                )
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log("bot", reward_coin_msg)

                self._random_wait(5, 10, "Sorry mate can't do this.")
                pass

                # fc.lc claim btn
                # claim_btn = self.__exWaitM().until(
                #     ec.element_to_be_clickable(
                #         (
                #             By.XPATH,
                #             shortlinks["fc.lc"]["shortlinks-claim-btn"],
                #         )
                #     ),
                #     message="timeout trying to find fc.lc claim btn",
                # )
                # self._click(claim_btn, "clicking shortlink claim link btn")

                # if self.__captcha_check(
                #     shortlinks["general"]["shortlinks-captcha-block"]
                # ):
                #     # Shotlink claim button
                #     shortlinkRewardClaimBtnTxt = self.__exWaitL().until(
                #         ec.text_to_be_present_in_element(
                #             (
                #                 By.XPATH,
                #                 shortlinks["general"]["shortlinks-reward-claim-btn"],
                #             ),
                #             "Get Reward",
                #         ),
                #         message="timeout trying to find shortlink claim btn",
                #     )
                #     shortlinkRewardClaimBtn = self.__exWaitS().until(
                #         ec.element_to_be_clickable(
                #             (
                #                 By.XPATH,
                #                 shortlinks["general"]["shortlinks-reward-claim-btn"],
                #             )
                #         ),
                #         message="timeout trying to find shortlink claim button",
                #     )
                #     orig_url = self.driver.current_url
                #     self._click(
                #         shortlinkRewardClaimBtn,
                #         "clicking on shortlink reward claim button",
                #     )
                #     self._random_wait(3, 5, "Waiting for the page to load")

                #     # if the button click didnt register try again
                #     if self.driver.current_url == orig_url:
                #         self._click(
                #             shortlinkRewardClaimBtn,
                #             "clicking again on the claim button",
                #         )
                #         self._random_wait(3, 5, "Waiting for the page to load")

                #     try:
                #         cnt_btn_1 = self.__exWaitM().until(
                #             ec.element_to_be_clickable(
                #                 (By.XPATH, shortlinks["fc.lc"]["continue-btn-1"])
                #             ),
                #             message="timeout trying to find fc.lc continue btn.",
                #         )
                #         self._click(cnt_btn_1, "clicking fc.lc continue btn.")
                #         cnt_btn_2 = self.__exWaitM().until(
                #             ec.element_to_be_clickable(
                #                 (By.XPATH, shortlinks["fc.lc"]["continue-btn-2"])
                #             ),
                #             message="timeout trying to find fc.lc continue btn.",
                #         )
                #         self._click(cnt_btn_2, "clicking fc.lc continue btn")

                #         retry_count = 0
                #         while retry_count < 5:
                #             get_link_btn = self.__exWaitM().until(
                #                 ec.element_to_be_clickable(
                #                     (By.XPATH, shortlinks["fc.lc"]["get-link-btn"])
                #                 ),
                #                 message="timeout trying to find Get Link btn.",
                #             )
                #             self._click(get_link_btn, "clicking on fc.lc Get link btn.")
                #             retry_count += 1
                #     except Exception as e:
                #         if self.debug:
                #             self.log.write_log("warning", e)
                #         else:
                #             self.error_handler(e)
                #             self.driver.get(self.shortlink_url)
                #             pass

            def sh_faucetcrypto_com():

                # sh.faucetcrypto.com viewcount
                view_count = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (
                                By.XPATH,
                                shortlinks["sh.faucetcrypto.com"][
                                    "shortlinks-view-count"
                                ],
                            )
                        ),
                        message="timeout trying to find sh.faucetcrypto.com viewcount",
                    )
                    .text
                )
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log("bot", view_count_msg)

                # sh.faucetcrypto.com reward
                reward_coin = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (
                                By.XPATH,
                                shortlinks["sh.faucetcrypto.com"][
                                    "shortlinks-reward-coin"
                                ],
                            )
                        ),
                        message="timeout trying to find sh.faucetcrypto.com reward",
                    )
                    .text
                )
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log("bot", reward_coin_msg)

                # sh.faucetcrypto.com claim btn
                claim_btn = self.__exWaitM().until(
                    ec.element_to_be_clickable(
                        (
                            By.XPATH,
                            shortlinks["sh.faucetcrypto.com"]["shortlinks-claim-btn"],
                        )
                    ),
                    message="timeout trying to find sh.faucetcrypto.com claim btn",
                )
                self._click(claim_btn, "clicking shortlink claim link btn")

                if self.__captcha_check(
                    shortlinks["general"]["shortlinks-captcha-block"]
                ):
                    # Shotlink claim button
                    shortlinkRewardClaimBtnTxt = self.__exWaitL().until(
                        ec.text_to_be_present_in_element(
                            (
                                By.XPATH,
                                shortlinks["general"]["shortlinks-reward-claim-btn"],
                            ),
                            "Get Reward",
                        ),
                        message="timeout trying to find shortlink claim btn",
                    )
                    shortlinkRewardClaimBtn = self.__exWaitS().until(
                        ec.element_to_be_clickable(
                            (
                                By.XPATH,
                                shortlinks["general"]["shortlinks-reward-claim-btn"],
                            )
                        ),
                        message="timeout trying to find shortlink claim button",
                    )
                    orig_url = self.driver.current_url
                    self._click(
                        shortlinkRewardClaimBtn,
                        "clicking on shortlink reward claim button",
                    )
                    self._random_wait(3, 5, "Waiting for the page to load")

                    # if the button click didnt register try again
                    if self.driver.current_url == orig_url:
                        self._click(
                            shortlinkRewardClaimBtn,
                            "clicking again on the claim button",
                        )
                        self._random_wait(3, 5, "Waiting for the page to load")

                    try:
                        # Current step count
                        step_count = (
                            self.__exWaitM()
                            .until(
                                ec.presence_of_element_located(
                                    (By.XPATH, faucet["faucet-current-step"])
                                ),
                                message="timeout trying to find faucet step",
                            )
                            .text
                        )

                        # Loop through the three steps
                        for i in range(int(step_count[2])):
                            step_count_msg = f"Current step: {i+1}/{step_count[2]}"
                            self.log.write_log(
                                "bot",
                                self.log.yellow_text(
                                    f"Current step count {step_count_msg}"
                                ),
                            )

                            self._random_wait(
                                5, 7, "If i dont wait he dose'nt like it."
                            )
                            source = self.driver.execute_script("goto()")
                            self._random_wait(
                                3, 5, "Need to wait for this snail to load."
                            )
                        self.log.write_log(
                            "success", f"Fininshed shortlink successfully"
                        )

                    except Exception as e:

                        if self.debug:
                            self.log.write_log("warning", e)
                        else:
                            self.error_handler(e)
                            pass

            def sh_faucet_gold():

                # sh.faucet.gold viewcount
                view_count = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (
                                By.XPATH,
                                shortlinks["sh.faucet.gold"]["shortlinks-view-count"],
                            )
                        ),
                        message="timeout trying to find sh.faucet.gold viewcount",
                    )
                    .text
                )
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log("bot", view_count_msg)

                # sh.faucet.gold reward
                reward_coin = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (
                                By.XPATH,
                                shortlinks["sh.faucet.gold"]["shortlinks-reward-coin"],
                            )
                        ),
                        message="timeout trying to find sh.faucet.gold reward",
                    )
                    .text
                )
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log("bot", reward_coin_msg)

                # sh.faucet.gold claim btn
                claim_btn = self.__exWaitM().until(
                    ec.element_to_be_clickable(
                        (
                            By.XPATH,
                            shortlinks["sh.faucet.gold"]["shortlinks-claim-btn"],
                        )
                    ),
                    message="timeout trying to find sh.faucet.gold claim btn",
                )
                self._click(claim_btn, "clicking shortlink claim link btn")

                if self.__captcha_check(
                    shortlinks["general"]["shortlinks-captcha-block"]
                ):
                    # Shotlink claim button
                    shortlinkRewardClaimBtnTxt = self.__exWaitL().until(
                        ec.text_to_be_present_in_element(
                            (
                                By.XPATH,
                                shortlinks["general"]["shortlinks-reward-claim-btn"],
                            ),
                            "Get Reward",
                        ),
                        message="timeout trying to find shortlink claim btn",
                    )
                    shortlinkRewardClaimBtn = self.__exWaitS().until(
                        ec.element_to_be_clickable(
                            (
                                By.XPATH,
                                shortlinks["general"]["shortlinks-reward-claim-btn"],
                            )
                        ),
                        message="timeout trying to find shortlink claim button",
                    )
                    orig_url = self.driver.current_url
                    self._click(
                        shortlinkRewardClaimBtn,
                        "clicking on shortlink reward claim button",
                    )
                    self._random_wait(3, 5, "Waiting for the page to load.")

                    # if the button click didnt register try again
                    if self.driver.current_url == orig_url:
                        self._click(
                            shortlinkRewardClaimBtn,
                            "clicking again on the claim button",
                        )
                        self._random_wait(3, 5, "Waiting for the page to load.")

                    try:
                        # Current step count
                        step_count = (
                            self.__exWaitM()
                            .until(
                                ec.presence_of_element_located(
                                    (By.XPATH, faucet["faucet-current-step"])
                                ),
                                message="timeout trying to find faucet step",
                            )
                            .text
                        )

                        # Loop through the three steps
                        for i in range(int(step_count[2])):
                            step_count_msg = f"Current step: {i+1}/{step_count[2]}"
                            self.log.write_log(
                                "bot",
                                self.log.yellow_text(
                                    f"Current step count {step_count_msg}"
                                ),
                            )

                            self._random_wait(5, 7, "Need to slow down for this snail")
                            source = self.driver.execute_script("goto()")
                            self._random_wait(3, 5, "Just load already.")
                        self.log.write_log(
                            "success", f"Fininshed shortlink successfully"
                        )

                    except Exception as e:

                        if self.debug:
                            self.log.write_log("warning", e)
                        else:
                            self.error_handler(e)
                            pass

            def sh_claim4_fun():

                # sh.claim4.fun viewcount
                view_count = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (
                                By.XPATH,
                                shortlinks["sh.claim4.fun"]["shortlinks-view-count"],
                            )
                        ),
                        message="timeout trying to find sh.claim4.fun viewcount",
                    )
                    .text
                )
                view_count_msg = f"View count: {link} [{view_count}]"
                self.log.write_log("bot", view_count_msg)

                # sh.claim4.fun reward
                reward_coin = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (
                                By.XPATH,
                                shortlinks["sh.claim4.fun"]["shortlinks-reward-coin"],
                            )
                        ),
                        message="timeout trying to find sh.claim4.fun reward",
                    )
                    .text
                )
                reward_coin_msg = f"Reward coins: {link} [{reward_coin}]"
                self.log.write_log("bot", reward_coin_msg)

                # sh.claim4.fun claim btn
                claim_btn = self.__exWaitM().until(
                    ec.element_to_be_clickable(
                        (
                            By.XPATH,
                            shortlinks["sh.claim4.fun"]["shortlinks-claim-btn"],
                        )
                    ),
                    message="timeout trying to find sh.claim4.fun claim btn",
                )
                self._click(claim_btn, "clicking shortlink claim link btn")

                if self.__captcha_check(
                    shortlinks["general"]["shortlinks-captcha-block"]
                ):
                    # Shotlink claim button
                    shortlinkRewardClaimBtnTxt = self.__exWaitL().until(
                        ec.text_to_be_present_in_element(
                            (
                                By.XPATH,
                                shortlinks["general"]["shortlinks-reward-claim-btn"],
                            ),
                            "Get Reward",
                        ),
                        message="timeout trying to find shortlink claim btn",
                    )
                    shortlinkRewardClaimBtn = self.__exWaitS().until(
                        ec.element_to_be_clickable(
                            (
                                By.XPATH,
                                shortlinks["general"]["shortlinks-reward-claim-btn"],
                            )
                        ),
                        message="timeout trying to find shortlink claim button",
                    )
                    orig_url = self.driver.current_url
                    self._click(
                        shortlinkRewardClaimBtn,
                        "clicking on shortlink reward claim button",
                    )
                    self._random_wait(3, 5, "Waiting for the page to load.")

                    # if the button click didnt register try again
                    if self.driver.current_url == orig_url:
                        self._click(
                            shortlinkRewardClaimBtn,
                            "clicking again on the claim button",
                        )
                    self._random_wait(3, 5, "Waiting for the page to load.")

                    try:
                        # Current step count
                        step_count = (
                            self.__exWaitM()
                            .until(
                                ec.presence_of_element_located(
                                    (By.XPATH, faucet["faucet-current-step"])
                                ),
                                message="timeout trying to find faucet step",
                            )
                            .text
                        )

                        # Loop through the three steps
                        for i in range(int(step_count[2])):
                            step_count_msg = f"Current step: {i+1}/{step_count[2]}"
                            self.log.write_log(
                                "bot",
                                self.log.yellow_text(
                                    f"Current step count {step_count_msg}"
                                ),
                            )

                            self._random_wait(5, 7, "Why are you so slow?")
                            source = self.driver.execute_script("goto()")
                            self._random_wait(
                                3, 5, "Every 60s in Africa a minute passes."
                            )
                        self.log.write_log(
                            "success", f"Fininshed shortlink successfully"
                        )

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
                view_count = (
                    self.__exWaitM()
                    .until(
                        ec.presence_of_element_located(
                            (
                                By.XPATH,
                                shortlinks[links]["shortlinks-view-count"],
                            )
                        ),
                        message="timeout trying to shortlinks viewcount",
                    )
                    .text[0]
                )
                if int(view_count) > 0:
                    self.log.write_log("bot", self.log.green_text(links.upper()))
                    switch(links)

            except Exception as e:

                if self.debug:
                    self.log.write_log("warning", e)
                else:
                    self.error_handler(e)
