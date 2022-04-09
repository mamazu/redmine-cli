import os
import getpass
import pathlib

CREDENTIAL_FILE = os.path.join(str(pathlib.Path(__file__).parent.absolute()),
                               '.env')


def get_credentials(credential_file: str = CREDENTIAL_FILE):
    if os.path.exists(credential_file):
        [url, username,
         password] = [a.strip() for a in open(credential_file).readlines()]
    else:
        url = input('URL: ')
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        f = open(credential_file, 'w')
        f.write(f"{url}\n{username}\n{password}")
        f.close()
    return [url, username, password]
