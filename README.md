<!-- Logo and description part -->
<div align="center">
<img src="media/fc-bot-logo.png" alt="Faucet Crypto Bot logo" width="200"/>
<br>
<p> A bot for the high paying popular cryptocurrency faucet Faucet Crypto. The bot is built using Python and Selenium, currently it is under active development and can do tasks like PTC ads, main rewards, and shortlinks except exe.io and fc.lc
</p>
</div>

<!-- Requirement Badges -->
<!-- Python badge -->
<p align="center">
<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/PYTHON-3.8-3B82F6.svg?style=for-the-badge" alt="made with python"/>
</a>
<!-- Selenium badge -->
<a href="https://www.selenium.dev/">
<img src="https://img.shields.io/badge/SELENIUM-3.141.0-3B82F6.svg?style=for-the-badge" alt="Selenium webdriver"/>
</a>
<!-- Brave badge -->
<a href="https://brave.com/">
<img src="https://img.shields.io/badge/BRAVE-88.0-3B82F6.svg?style=for-the-badge" alt="Brave browser"/>
</a>
<!-- Chrome driver badge -->
<a href="https://chromedriver.chromium.org/downloads">
<img src="https://img.shields.io/badge/CHROME DRIVER-88.0-3B82F6.svg?style=for-the-badge" alt="chromium driver for selenium"/>
</a>
</p>

<!-- Description -->
## [Faucet Crypto]('https://faucetcrypto.com/')
<img src="media/fc-home-sc.png" alt="Faucet Crypto landing page" style="float: center; margin-right: 10px;" width="1000"/>

<!-- Browser preference -->
### Brave Browser

The browser of choice for this project is Brave browser due to its native ad-blocking scripts which are pretty good and prevents random popup openings, which can mess with the bots proper execution.

If you don't have Brave browser installed you can download it from here.

<p align="center">
<a href="https://brave.com/">
<img src="media/brave-logo.png" style="float: center; margin-right: 10px;" width="100"/>
</a>
</p>

### Installation

create a virtual environment with virtualenv

``` bash
virtualenv env
```

Activate the virtual environment

```bash
source env/bin/activate
```

Install all the necessary packages

```bash
pip install -r requirements.txt
```

### Setup

Set the correct path for your brave browser in the config file config.py
``` python
"" Path to your defautl browser profile directory ""
USER_DATA_DIR = "/home/darkstalker/.config/BraveSoftware/Brave-Browser"

"" Path to your browser binary location ""
BROWSER_BINARY_LOCATION = "/usr/bin/brave-browser"

"" Path to your chromedriver binary path ""
DRIVER_PATH = "/usr/local/bin/chromedriver"

"" Headless mode flag runs the browser without UI ""
# params: <headless> or <empty>
DRIVER_MODE = ""

"" If set to true will show warnings and errors in the terminal else logs it to error-logs.txt file ""
DEBUG = False"
```

### Run

Run the bot by

``` bash
python bot.py
```
