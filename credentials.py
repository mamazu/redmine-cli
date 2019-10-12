import os

CREDENTIAL_FILE = '.env'

def get_credentials():
    if os.path.exists(CREDENTIAL_FILE):
        [url, username, password] = [a.strip() for a in open(CREDENTIAL_FILE).readlines()]
    else:
        url = input('URL: ')
        username = input('Username: ')
        password = input('Password: ')
        f = open(CREDENTIAL_FILE, 'w')
        f.write(username+"\n")
        f.write(password)
        f.close()
    return [url, username, password]