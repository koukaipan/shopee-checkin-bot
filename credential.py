import json
import logging
import os

class Credential():
    def __init__(self, credential_file: str = '', use_env: bool = True, \
                 username: str = '', password: str = '') -> None:
        self.username = ''
        self.password = ''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        # priority 1: given username and password
        if (len(username) > 0 and len(password) > 0):
            self.username = username
            self.password = password
            if (len(self.username) > 0 and len(self.password) > 0):
                return
            else:
                self.logger.error('Specified invalid username or password')

        # priority 2: given file
        if ((len(self.username) == 0 or len(self.password) == 0) and len(credential_file) > 0):
            with open(credential_file) as f:
                __cred = json.load(f)
                self.username = __cred['username']
                self.password = __cred['password']
                if (len(self.username) > 0 and len(self.password) > 0):
                    return

        # error if they are still zero length
        if (len(self.username) > 0 and len(self.password) > 0):
            self.logger.critical('Missing username and password for login process')
            return

    def get(self):
        return (self.username, self.password)