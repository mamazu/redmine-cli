import os
import sys
import getpass

CREDENTIAL_FILE = '.env'


def get_input(prompt=''):
    if sys.version_info >= (3, 0):
        return input(prompt)
    return raw_input(prompt)


def get_credentials():
    if os.path.exists(CREDENTIAL_FILE):
        [url, username, password] = [a.strip() for a in open(CREDENTIAL_FILE).readlines()]
    else:
        url = get_input('URL: ')
        username = get_input('Username: ')
        password = getpass.getpass('Password: ')
        f = open(CREDENTIAL_FILE, 'w')
        f.write(url + "\n")
        f.write(username + "\n")
        f.write(password)
        f.close()
    return [url, username, password]
