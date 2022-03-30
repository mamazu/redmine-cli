import os
import getpass
import pathlib

CREDENTIAL_FILE = os.path.join(str(pathlib.Path(__file__).parent.absolute()),
                               '.env')


def get_credentials():
    print(CREDENTIAL_FILE)
    if os.path.exists(CREDENTIAL_FILE):
        [url, username,
         password] = [a.strip() for a in open(CREDENTIAL_FILE).readlines()]
    else:
        url = input('URL: ')
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        f = open(CREDENTIAL_FILE, 'w')
        f.write(url + "\n")
        f.write(username + "\n")
        f.write(password)
        f.close()
    return [url, username, password]
