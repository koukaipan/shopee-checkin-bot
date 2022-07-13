# shopee-checkin-bot
Bot for automatically daily checkin Shopee <br>
每日蝦X領取機器人

## Prerequisite

- ### virtual env
For Linux
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
For Windows
```
python -m venv venv-win
.\venv-win\Scripts\Activate.ps1
pip install -r require
```

- ### 下載用於 selenium 串接 chrome driver 的 chrome driver
    * https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
    * https://chromedriver.chromium.org/downloads


## Run
```
python main.py
```

### Parameters
```
python main.py --help
```

- `-v`, `--verbose`: 顯示更多 debug 訊息
- `--cookie-path`: 指定 cookie 檔案路徑，讀取及存檔 cookie 時使用
- `--credential-path`: 登入的帳號、密碼資訊，以 json 方式保存
- `--chrome-driver-path`: selenium 串接 chrome 瀏覽器用的 chrome driver 位置，請參考: https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
- `--show-gui`: 顯示瀏覽器的 GUI 界面，有助於除錯

credential.json example:
```
{
    "username" : "myidislion",
    "password" : "mypasswordisqwerty"
}
```

## Exit Code

| Exit code | 解釋 |
| --------- | ----------- |
| 0         | 簽到成功。    |
| 1         | 今日已簽到。如果傳了 `--force` 參數，那就會改為回傳 0。 |
| 2         | 需要簡訊驗證，但你傳了 `--no-sms` 參數。 |
| 3         | 機器人遇到拼圖遊戲，但是它不會玩🥺🥺<br> 這通常是因為嘗試登入次數太多，被網站 ban 掉。 |
| 4         | 操作逾時。 |
| 5         | 觸發電子郵件驗證。機器人尚不支援。 |
| 6         | 使用者進行簡訊驗證時選擇拒絕機器人登入。 |
| 69        | 嘗試登入次數太多被 ban。 |
| 77        | 參數不合法。 |
| 87        | 帳號或密碼錯誤。 |
| 88        | 不明錯誤。 |


## Acknowledgements
這個機器人受 https://github.com/wdzeng/shopee-coins-bot 啟發，程式邏輯也是參考自該專案，在此致謝

## License
`shopee-checkin-bot` 採用 MIT 授權，中文翻譯可參考 http://lucien.cc/20080117-the-mit-license-mit%E6%8E%88%E6%AC%8A%E6%A2%9D%E6%AC%BE%E4%B8%8D%E8%B2%A0%E8%B2%AC%E4%BB%BB%E4%B8%AD%E8%AD%AF%E7%89%88/