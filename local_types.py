from enum import Enum

class StateText(Enum):
    USE_LINK = '使用連結驗證'
    RECEIVE_COIN = '今日簽到獲得'
    SHOPEE_REWARD = '蝦幣獎勵'
    TOO_MUCH_TRY = '您已達到今日驗證次數上限。'
    COIN_RECEIVED = '明天再回來領取'
    WRONG_PASSWORDS = [
        '你的帳號或密碼不正確，請再試一次',
        '登入失敗，請稍後再試或使用其他登入方法',
        '您輸入的帳號或密碼不正確，若遇到困難，請重設您的密碼。'
    ]
    PKAY_PUZZLE = '點擊以重新載入頁面'
    EMAIL_AUTH = '透過電子郵件連結驗證'
    FAILURE = '很抱歉，您的身份驗證已遭到拒絕。'


class ExitCode(Enum):
    SUCCESS = 0
    ALREADY_RECEIVED = 1
    NEED_SMS_AUTH = 2
    CANNOT_SOLVE_PUZZLE = 3
    OPERATION_TIMEOUT_EXCEEDED = 4
    NEED_EMAIL_AUTH = 5
    LOGIN_DENIED = 6
    TOO_MUCH_TRY = 69
    INVALID_OPTIONS = 77
    WRONG_PASSWORD = 87
    UNKNOWN_ERROR = 88