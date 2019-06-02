#!/usr/bin/env python3.5
# -*- coding: UTF-8 -*-

import sys
import time
import urllib
import urllib.parse
import urllib.request
import random
import argparse
import binascii

def api(url, **kwargs):
  if kwargs:
    data = urllib.parse.urlencode(kwargs)
    request = urllib.request.Request(url, data.encode())
  else:
    request = urllib.request.Request(url)
  try:
    response = urllib.request.urlopen(request)
    html = response.read()
  except urllib.error.HTTPError as e:
    html = e.read()
  html = html.decode()
  if html.find('bad decrypt') >= 0:
    # print('bad decrypt')
    return False
  elif html.find('no!') >= 0:
    # print('valid')
    return True
  else:
    # print(html)
    return False

def is_valid(iv, c):
  # Test if the padding of (iv ^ c^(-1)) is valid.
  data = binascii.hexlify(bytearray(iv)).decode() + binascii.hexlify(bytearray(c)).decode()
  # print(data)
  return api('http://10.60.0.212:5757/test/' + data)

def attack(data, block_id, is_valid):
  if 16 * block_id + 32 > len(data):
    print('Block id is too large.')
    exit(1)
  c_p = list(data[16 * block_id:16 * block_id + 16]) # Previous cipher block
  iv = [random.choice(range(256)) for i in range(0, 16)] # *Random* initialization vector is necessary.
  c = data[16 * block_id + 16:16 * block_id + 32] # Current cipher block
  
  plain = []
  for n in range(1, 17): # Which byte (in reverse order)?
    for i in range(0, 256): # All possibilities of iv[-n]
      iv[-n] = i
      if is_valid(iv, c): # Padding is valid, so (iv[-n] ^ c^(-1)[-n]) is n, (iv[-n] ^ n) is c^(-1)[-n].
        break
    # print(iv[-n] ^ n ^ c_p[-n], chr(iv[-n] ^ n ^ c_p[-n])) 
    # Calculate plain text.
    # Note: (iv[-n] ^ n) is c^(-1)[-n], so ((iv[-n] ^ n) ^ c_p[-n]) == (c^(-1)[-n] ^ c_p[-n]) is (plain text)[-n].
    plain.append(iv[-n] ^ n ^ c_p[-n])
    for i in range(1, n + 1):
      iv[-i] = iv[-i] ^ n ^ (n + 1)
      # Note:
      # For futher attack,
      # For i in [1, n], we want (new iv[-i] ^ c^(-1)[-i]) to be (n + 1), so that we can attack c^(-1)[-(n + 1)] using padding oracle.
      # In particular, for i == n, we want (new iv[-n] ^ c^(-1)[-n]) to be (n + 1), so new iv[-n] should be (c^(-1)[-n] ^ (n + 1)) == ((iv[-n] ^ n) ^ (n + 1)).
      # In particular, for i in [1, n - 1], we want (new iv[-i] ^ c^(-1)[-i]) to be (n + 1). Please note that (iv[-i] ^ c^(-1)[-i]) is n, so new iv[-i] should be (c^(-1)[-i] ^ (n + 1)) == ((iv[-i] ^ n) ^ (n + 1))
  plain.reverse()
  return bytearray(plain)

def main():
  # Data from http://10.60.0.212:5757/generate
  data_hex = '74b6510402f53b1661b98a2cfee1f1b5d65753e5ca0ccb1356c0ef871a0118bc47c245dcb51dc51efd473e5f63f3a8c94818195d08d01e740f27d07b0893d0cd'
  data = binascii.unhexlify(data_hex)
  for i in range(0, 3):
    print(attack(data, i, is_valid).decode(), end='')

if __name__ == '__main__':
  main()