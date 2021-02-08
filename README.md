<!-- Logo and description part -->
<div align="center">
<img src="media/fc-bot-logo.png" alt="Faucet Crypto Bot logo" width="200"/>
<p>
<br>
<br>
A bot for the high paying popular cryptocurrency faucet Faucet Crypto.
The bot is built using Python and Selenium, currently it is under active development and,
can do tasks like PTC ads, main rewards, and shortlinks except exe.io and fc.lc
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

<!-- Status -->
<p align="center">
<br>
<img src="https://img.shields.io/badge/STATUS-WORKING-00cc00.svg?style=for-the-badge" alt="Bot status"/>
<!-- <img src="https://img.shields.io/badge/STATUS-NOT WORKING-ff0000.svg?style=for-the-badge" alt="Bot status"/> -->
</p>

<!-- Status -->
### Status

The issue of the bot was unable to find the claim button was fixed. The reason was due to an update in Faucet Crypto website. New xpaths have been updated you can copy the new xpaths to your old xpaths file.
(keep and eye on the bot status for further changes and updates that might occur.)

<!-- Description -->
## [Faucet Crypto]('https://faucetcrypto.com/')
<img src="media/fc-home-sc.png" alt="Faucet Crypto landing page" style="float: center; margin-right: 10px;" width="1000"/>

<!-- Star reminder -->
#### If you found this repo useful please don't forget to give me a :star:

<!-- Browser preference -->
### Brave Browser

The browser of choice for this project is Brave browser due to its native
ad-blocking scripts which are pretty good and prevents random popup openings,
which can mess with the bots proper execution.

If you don't have Brave browser installed you can download it from here.

<p align="center">
<a href="https://brave.com/">
<img src="media/brave-logo.png" style="float: center; margin-right: 10px;" width="70"/>
</a>
</p>

### Changes

- Added logic to save cookies and use them for logging in. This prevents
using the default profile directory of your browser and dosen't mess it up.

- Added logic to close the welcome modal and chat which covered the dashboard
visibilty.

- Cookies are now saved to a cookie file if it is not present in the directory
the bot will automatically login with the user email and password provided on 
the config file and generate a new cookie file.

- Added proxy incase you want to generate some referrals. This method is not
recommended yet and try this at your own risk.

- Fixed the issue when the browser was running in normal mode the bot closing all
the open tabs.

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
``` bash
[Browser]
browser-mode =              #takes two parameters headless or leave it empty
driver-path =               #path to your chrome driver
browser-binary-location =   #path to your browser binary location

[User]
mail =                      #Your faucet crypto account mail
password =                  #your faucet crypto account password

[Misc]
debug =                     #takes two arguments True of False
proxy =                     #proxy address and port try not to use a proxy
                            #and leave this empty
```

### Run

Run the bot by

``` bash
python bot.py
```
<!-- screenshot -->

<img src="media/bot-sc-1.png" alt="Bot terminal" style="float: center; margin-right: 10px;" width="1000"/>

### Account setup

If it's your first time running the bot you need to login to Faucet crypto.
Run the bot in normal-mode(default) it will redirect to login page where you can login,
the bot will do the rest from there by collecting from all the ads. (Note) The bot can't
yet do the exe.io and fc.lc shortlinks so you would have to help it do that. If you've logged in successfully then you can run the bot in headless mode from then on you can set the bot
to headless mode by setting the "headless" flag in the config file.

```python
browser-mode = "headless"
```

### Contributions

Feel free to contribute to this project and help me improve this project


##### Thank You, 
###### Sourav
