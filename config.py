import os

from local_types import StateText

class XpathConfig:
    checking_button = '//button[@class="pcmall-dailycheckin_3uUmyu"]'
    login_button = '//button[text()="登入"]'
    sms_login_button = '//div[text()="%s"]' % StateText.USE_LINK.value
    login_key_input = '//input[@name="loginKey"]'
    password_input = '//input[@name="password"]'


class ShopeeCoinBotConfig:
    login_url = 'https://shopee.tw/buyer/login?from=https%3A%2F%2Fshopee.tw%2Fuser%2Fcoin&next=https%3A%2F%2Fshopee.tw%2Fshopee-coins'
    coin_url = 'https://shopee.tw/shopee-coins'
    verify_url = 'https://shopee.tw/verify/link'
    shopee_url = 'https://shopee.tw/'
    web_timeout = 5
    web_shortdelay = 3
    sms_login_timeout = 600

class DefaultConfig:
    cookie_path = os.path.join('.', 'cookies')
    chrome_driver_path = os.path.join('.', 'chromedriver')
    credential_path = os.path.join('.', 'credential.json')