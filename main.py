import logging
import os
import argparse

from config import DefaultConfig as dft_cfg
from credential import Credential
from Bot import ShopeeCoinBot

def parse_argument():
    parser = argparse.ArgumentParser(description='Shopee daily checkin bot.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    parser.add_argument("--cookie-path", type=str, default=dft_cfg.cookie_path,
                        help="cookie file path")
    parser.add_argument("--credential-path", type=str, default=dft_cfg.credential_path,
                        help="credential file path (in json format)")
    parser.add_argument("--chrome-driver-path", type=str, default=dft_cfg.chrome_driver_path,
                        help="chrome driver path")
    parser.add_argument("--show-gui", action="store_true",
                        help="Display browser's GUI")
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_argument()
    cred = Credential('./credential.json')

    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    bot = ShopeeCoinBot(cred, chrome_driver_path=args.chrome_driver_path,
                        cookie_path=args.cookie_path, log_level=log_level,
                        show_gui=args.show_gui)
    ret = bot.run_bot()
    os._exit(ret)
