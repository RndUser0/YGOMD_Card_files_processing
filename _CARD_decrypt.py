'''
Credit: akintos: https://gist.github.com/akintos/04e2494c62184d2d4384078b0511673b
'''

import sys
import zlib

file_name = sys.argv[1]
m_iCryptoKey = 0x7a

with open(file_name, "rb") as f:
	data = bytearray(f.read())

for i in range(len(data)):
	v = i + m_iCryptoKey + 0x23D
	v *= m_iCryptoKey
	v ^= i % 7
	data[i] ^= v & 0xFF

with open(file_name + ".dec", "wb") as f:
	f.write(zlib.decompress(data))