import json
import logging
import selenium.webdriver.support.ui as ui
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import ShopeeCoinBotConfig as bot_config
from config import XpathConfig as bot_xpath
from credential import Credential
from local_types import StateText, ExitCode

class ShopeeCoinBot:
    def __init__(self, cred: Credential, chrome_driver_path: str,
                 cookie_path='', log_level=logging.ERROR, show_gui=False) -> None:
        self.init_logger(log_level)
        self.init_driver(chrome_driver_path, show_gui)

        if cred == None and len(cookie_path) == 0:
            self.critical('No credential given and no cookie, I cannot loggin.\n')
            return None

        self.cred = cred
        self.cookie_path = cookie_path
        if len(cookie_path) > 0:
            self.try_load_cookie()


    def init_driver(self, chrome_driver_path, show_gui):
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--lang=zh-TW")
        if not show_gui:
            options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_driver_path, options=options)
        # browser.implicitly_wait(10)
        self.wait = ui.WebDriverWait(self.browser, bot_config.web_timeout)


    def init_logger(self, log_level):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        self.logger.addHandler(ch)


    def try_load_cookie(self):
        # load cookie into browser, but it does not imply we've logged in
        try:
            with open(self.cookie_path, "r") as infile:
                cookie = json.load(infile)
                self.browser.get(bot_config.shopee_url)
                time.sleep(bot_config.web_shortdelay)
                self.wait.until(lambda x: x.current_url)
                for c in cookie:
                    self.browser.add_cookie(c)
                self.logger.info('Cookies are load')
                time.sleep(bot_config.web_shortdelay)
        except FileNotFoundError:
            # It does not matter, just skip, we still have a chance to use the
            # `cookie_path` when saving cookie
            self.logger.warning('No such file: %s Cannot load cookie' % self.cookie_path)


    def save_cookie(self):
        if len(self.cookie_path) == 0:
            self.logger.error('cookie_path is not specified.')
            return
        cookies = self.browser.get_cookies()
        with open(self.cookie_path, "w") as outfile:
            json.dump(cookies, outfile, indent=4)


    def proceed_sms_login(self):
        login_with_sms_btn = self.wait.until(lambda driver:
                                    driver.find_element(By.XPATH, bot_xpath.sms_login_button))
        login_with_sms_btn.click()
        self.logger.info('click login button')
        self.wait.until(lambda x: x.current_url == bot_config.verify_url)

        self.logger.warning('An SMS message is sent to your mobile.')
        self.logger.warning('Once you click the link I will keep going.')
        self.logger.warning('I will wait for you and please complete it in 10 minutes.')

        ui.WebDriverWait(self.browser, bot_config.sms_login_timeout).until(lambda x: bot_config.coin_url in x.current_url)

        return ExitCode.SUCCESS.value


    def try_login(self):
        self.browser.get(bot_config.login_url)
        time.sleep(bot_config.web_shortdelay)
        self.wait.until(lambda x: x.current_url)
        self.logger.info('current url: %s' % self.browser.current_url)

        # The webpage is redirected to the coin check-in page and therefore
        # the user must have been logged in.
        if self.browser.current_url.startswith(bot_config.coin_url):
            self.logger.info('Already logged in.')
            return 0

        inputUsername = self.wait.until(lambda driver:driver.find_element(By.XPATH, bot_xpath.login_key_input))
        inputUsername.send_keys(self.cred.username)
        inputPassword = self.wait.until(lambda driver:driver.find_element(By.XPATH, bot_xpath.password_input))
        inputPassword.send_keys(self.cred.password)

        btnLogin = self.wait.until(EC.element_to_be_clickable((By.XPATH, bot_xpath.login_button)))
        btnLogin.click() # do not await for this click since it may hang = =
        self.logger.info('Login form submitted. Waiting for redirect.')

        time.sleep(bot_config.web_shortdelay)
        find_strings = [StateText.USE_LINK.value,
            StateText.RECEIVE_COIN.value,
            StateText.SHOPEE_REWARD.value,
            StateText.TOO_MUCH_TRY.value,
            StateText.COIN_RECEIVED.value,
            StateText.PKAY_PUZZLE.value,
            StateText.EMAIL_AUTH.value,
            StateText.FAILURE.value]
        find_strings += ['%s'%s for s in StateText.WRONG_PASSWORDS.value]
        xpath_string = '|'.join([ '//div[text()="%s"]'%s for s in find_strings ])

        result = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_string)))
        text = result.text

        if text == StateText.SHOPEE_REWARD.value:
            self.logger.info('Login succeeded.')
            return ExitCode.SUCCESS.value

        if result.text in StateText.WRONG_PASSWORDS.value:
            self.logger.error('Login failed: wrong password.')
            return ExitCode.WRONG_PASSWORD.value

        if text == StateText.PKAY_PUZZLE.value:
            self.logger.error('Login failed: I cannot solve the puzzle.')
            return ExitCode.CANNOT_SOLVE_PUZZLE.value

        if text == StateText.EMAIL_AUTH:
            self.logger.error('Login failed: need email Auth')
            return ExitCode.NEED_EMAIL_AUTH.value

        if text == StateText.USE_LINK.value:
            self.logger.info('Login proceed: please continue to login via SMS.')
            return self.proceed_sms_login()

        self.logger.critical('Unexpected error occurred. Fetched text by xpath: %s' % text)
        return ExitCode.UNKNOWN_ERROR.value


    def checkin(self):
        if not self.browser.current_url.startswith(bot_config.coin_url):
            self.logger.error('Not in expected url:%s' % self.browser.current_url)
            return ExitCode.UNKNOWN_ERROR.value

        checkin_btn = self.wait.until(lambda driver:driver.find_element(By.XPATH, bot_xpath.checking_button))
        text = checkin_btn.text

        if text.startswith(StateText.COIN_RECEIVED.value):
            self.logger.warning('Coin already received. Nothing to be done')
            return ExitCode.ALREADY_RECEIVED.value

        checkin_btn.click()
        time.sleep(bot_config.web_shortdelay)
        self.logger.info('Daily checkin award GET!')
        return ExitCode.SUCCESS.value


    def run_bot(self):
        ret = self.try_login()
        if ret == ExitCode.SUCCESS.value:
            if len(self.cookie_path) > 0:
                self.save_cookie()
        else:
            return ret

        ret = self.checkin()
        self.logger.info('Execution result = %d' % ret)
        self.browser.quit()
        return ret
