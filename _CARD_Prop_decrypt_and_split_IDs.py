'''
Credits:
akintos: https://gist.github.com/akintos/04e2494c62184d2d4384078b0511673b
timelic from NexusMods: https://forums.nexusmods.com/index.php?/user/145588218-timelic
'''

from typing import List
import json
#import os
import sys
import zlib

def FileCheck(filename):
    try:
      open(filename, 'r')
      return 1
    except IOError:
      # print 'Error: File does not appear to exist.'
      return 0

def Decrypt(filename):
    with open(f'{filename}', "rb") as f:
        data = bytearray(f.read())

    for i in range(len(data)):
        v = i + m_iCryptoKey + 0x23D
        v *= m_iCryptoKey
        v ^= i % 7
        data[i] ^= v & 0xFF

    with open(f'{filename}' + ".dec", "wb") as f:
        f.write(zlib.decompress(data))

def CheckCryptoKey():	
	try:
		Decrypt(CARD_Prop_filename)
		return 1
	except zlib.error:	
		return 0

# 1. Check if CARD_* files exist:

filenames_to_check = ['CARD_Prop', 'CARD_Prop.bytes', 'CARD_Prop.txt']
check_counter = -1
CARD_Prop_filename = ''

for i in filenames_to_check:
	check_counter += 1		
	if FileCheck(i) == 1 and i.find('CARD_Prop') != -1 and CARD_Prop_filename == '':
		CARD_Prop_filename = i
	if check_counter == len(filenames_to_check)-1 and CARD_Prop_filename == '':
		print('CARD_Prop file not found. The file name must be \"CARD_Prop\", \"CARD_Prop.bytes\" or \"CARD_Prop.txt\".\nPress <ENTER> to exit.')
		input()
		sys.exit()

# 2. Find crypto key

if FileCheck('!CryptoKey.txt') == 1:
	print('Trying to read crypto key from file...')
	with open('!CryptoKey.txt', 'rt') as f_CryptoKey:		
			m_iCryptoKey = int(f_CryptoKey.read(),16)			
	f_CryptoKey.close()	
	print('Read crypto key "' + hex(m_iCryptoKey) + '" from file, checking if it is correct...')
else:
	m_iCryptoKey = 0x0

if CheckCryptoKey() == 1:
	print('The crypto key "' + hex(m_iCryptoKey) + '" is correct.')
else:
	print('No correct crypto key found. Searching for crypto key...')
	m_iCryptoKey = 0x0	
	while True:
		try:
			Decrypt(CARD_Prop_filename)
			#if os.stat('CARD_Prop.dec').st_size > 0:
			break
		except zlib.error:
			#print('Wrong crypto key:', hex(m_iCryptoKey), ' (zlib error)')
			m_iCryptoKey = m_iCryptoKey + 1
		#except Exception:
			#print('Unexpected {err=}, {type(err)=}')
		#else:	
	with open('!CryptoKey.txt', 'w') as f_CryptoKey:
		f_CryptoKey.write(hex(m_iCryptoKey))
	f_CryptoKey.close()
	print('Found correct crypto key "' + hex(m_iCryptoKey) + '" and wrote it to file "!CryptoKey.txt".')

# 3. Decrypt CARD_Prop

filenames = [CARD_Prop_filename]

print('Decrypting files...')

for name in filenames:
	if FileCheck(name) == 1:
		Decrypt(name)
		print('Decrypted file "' + name + '".')	
	else:
		print("Could not decrypt file " + name + " because it does not appear to exist.")

# 4. Split CARD_Prop

def WriteJSON(l: list, json_file_path: str):
    with open(json_file_path, 'w', encoding='utf8') as f:
        json.dump(l, f, ensure_ascii=False, indent=4)

filenames = [CARD_Prop_filename]

# The start of CARD_Prop is 8.
def ProgressiveProcessing(filename):
	with open(CARD_Prop_filename + ".dec", "rb") as f:
		hex_str_list = ("{:02X}".format(int(c))
		for c in f.read())  # Define variables to accept file contents
	
	str_list = [str(s) for s in hex_str_list]  # Convert hexadecimal to string
	
	Card_ID_list = []
	for i in range(8,len(str_list)-1,8):
		Card_ID_list.append(''.join([str_list[i+1], str_list[i]]))
	
	Card_ID_dec_list = [int(s, 16) for s in Card_ID_list]  # Convert hexadecimal to decimal	
	WriteJSON(Card_ID_dec_list, f"{filename}" + ".Card_IDs.dec.json")

print('Splitting files...')

if __name__ == '__main__':    
    ProgressiveProcessing(filenames[0])

print('Finished splitting files.')