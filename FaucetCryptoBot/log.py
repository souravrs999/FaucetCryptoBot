from datetime import datetime
from colorama import init, Fore


class Log:
    def __init__(self, log=True, logfile="error-logs.txt"):
        init(autoreset=True)
        self.log = log
        self.logfile = logfile

    def get_time(self):
        date = datetime.now()
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def green_text(self, text):
        return Fore.LIGHTGREEN_EX + str(text) + Fore.RESET

    def blue_text(self, text):
        return Fore.LIGHTBLUE_EX + str(text) + Fore.RESET

    def red_text(self, text):
        return Fore.LIGHTRED_EX + str(text) + Fore.RESET

    def yellow_text(self, text):
        return Fore.LIGHTYELLOW_EX + str(text) + Fore.RESET

    def __get_bot_badge(self):
        return Fore.LIGHTBLUE_EX + "  BOT  " + Fore.RESET

    def __get_browser_badge(self):
        return Fore.YELLOW + "BROWSER" + Fore.RESET

    def __get_warning_badge(self):
        return Fore.LIGHTRED_EX + "WARNING" + Fore.RESET

    def __get_success_badge(self):
        return Fore.LIGHTGREEN_EX + "SUCCESS" + Fore.RESET

    def write_log(self, badge="bot", msg=" "):
        if badge.upper() == "BOT":
            print(f"[ {self.get_time()} ] [{self.__get_bot_badge()}] {msg}")
        elif badge.upper() == "BROWSER":
            print(f"[ {self.get_time()} ] [{self.__get_browser_badge()}] {msg}")
        elif badge.upper() == "WARNING":
            print(f"[ {self.get_time()} ] [{self.__get_warning_badge()}] {msg}")
        elif badge.upper() == "SUCCESS":
            print(f"[ {self.get_time()} ] [{self.__get_success_badge()}] {msg}")

    def error_log(self, error_msg):
        if self.log:
            with open(self.logfile, "a") as log:
                error_msg_line = f'[ {self.get_time()} ] [  ERROR  ] {str(error_msg)}\n'
                log.write(error_msg_line)
