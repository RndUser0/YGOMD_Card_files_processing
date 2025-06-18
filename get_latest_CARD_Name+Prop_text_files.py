'''
Credits:
akintos: https://gist.github.com/akintos/04e2494c62184d2d4384078b0511673b
timelic: https://github.com/timelic/master-duel-chinese-translation-switch
'''

from pathlib import Path
from typing import List
import fileinput
import re
import json
import os
import shutil
import subprocess
import sys
import time
import zlib

# 0. Definitions

def FileCheck(file_path):
	if os.path.isfile(file_path):
		print(f'The file "{file_path}" exists and is a regular file.')
		return 1
	else:
		print(f'The file "{file_path}" does not exist or is not a regular file.')
		return 0

def DirCheck(directory_path):
	if os.path.isdir(directory_path):
		return 1
	else:
		return 0

def LocalDataDirCheck(directory_path):
	substring = '\\Yu-Gi-Oh!  Master Duel\\LocalData\\'
	if substring in directory_path:
		return 1
	else:
		return 0

def AddBackslash(directory_path):
	#Add backslash at the end if it doesn't exist.
	if directory_path[-1] != '\\':
		directory_path = directory_path + '\\'
	return directory_path

def Get_LD_BaseDir():
	if FileCheck(settings_dir + '!LocalData dir.txt') == 1:
		print('Trying to read LocalData directory path from file...')
		with open(settings_dir + '!LocalData dir.txt', 'r', encoding='utf-8') as f_LD_BaseDir:
				LD_BaseDir = f_LD_BaseDir.read()
		f_LD_BaseDir.close()	
		print('Read directory "' + LD_BaseDir + '" from file, checking if it is correct...')
	
		if (DirCheck(LD_BaseDir) and LocalDataDirCheck(LD_BaseDir)):
			#Add backslash at the end if it doesn't exist.
			LD_BaseDir = AddBackslash(LD_BaseDir)
			print('"' + LD_BaseDir + '" will be used as Master Duel LocalData directory.')
			return LD_BaseDir
		else:
			if not DirCheck(LD_BaseDir):
				print("Directory doesn't exist.")		
			if not LocalDataDirCheck(LD_BaseDir):
				print('"' + LD_BaseDir + '" is not a Master Duel LocalData Directory.')	
			return ''
		
	else:		
		LD_BaseDir = ''
		print('Enter the path of your account-specific Master Duel LocalData directory. \nExample: C:\\Program Files (x86)\\Steam\\steamapps\\common\\Yu-Gi-Oh!  Master Duel\\LocalData\\1a2b3c4d')

		#Get directory and check it.
		while not (DirCheck(LD_BaseDir) and  LocalDataDirCheck(LD_BaseDir)):
			print('Path:', end=' ')
			LD_BaseDir = input()
			if not DirCheck(LD_BaseDir):
				print("Directory doesn't exist.")
			if DirCheck(LD_BaseDir) and not LocalDataDirCheck(LD_BaseDir):
				print('"' + LD_BaseDir + '" is not a Master Duel LocalData Directory.')

		#Add backslash at the end if it doesn't exist.
		LD_BaseDir = AddBackslash(LD_BaseDir)
		
		print('"' + LD_BaseDir + '" will be used as Master Duel LocalData directory.')
		
		#Write LD_BaseDir to file
		with open(settings_dir + '!LocalData dir.txt', 'w', encoding='utf-8') as f_LD_BaseDir:
			f_LD_BaseDir.write(LD_BaseDir)
		f_LD_BaseDir.close()
		print('Wrote "' + LD_BaseDir + '" to file "' + settings_dir + '!LocalData dir.txt".')	
	
		return LD_BaseDir

def MkDir(FolderName):	
	try:
		os.mkdir(FolderName)
		print(f'Directory "{FolderName}" created successfully.')
	except FileExistsError:
		print(f'Directory "{FolderName}" already exists.')
	except PermissionError:
		print(f'Permission denied: Unable to create "{FolderName}".')
	except Exception as e:
		print(f'An error occurred: {e}')
	return AddBackslash(os.path.abspath(FolderName))

def Del_all_files_in_dir(Directory):
	print('Deleting all files in directory "' + Directory + '"...')
	for filename in os.listdir(Directory):
		file_path = os.path.join(Directory, filename)
		if os.path.isfile(file_path):
			os.remove(file_path)		
	print('All files in directory "' + Directory + '" have been deleted.')

def MoveFile(SourceFile, Destination):
	try:
		shutil.move(SourceFile, Destination)
		print(f'File "{SourceFile}" moved to "{Destination}" successfully.')
	except FileNotFoundError:
		print(f'Error: Source file "{Sourcefile}" not found.')
	except Exception as e:
		print(f"An error occurred: {e}")

def Sort_by_last_modified_rev(directory_path):
	"""
	Sorts files and subdirectories by last modification time, with subdirectories last.
	"""
	items = []
	for root, dirs, files in os.walk(directory_path):
		for name in files:
			path = os.path.join(root, name)
			mod_time = os.path.getmtime(path)
			items.append((mod_time, 0, path)) # 0 for files

	# Sort by modification time (ascending), then by type (files before directories)
	sorted_items = sorted(items, key=lambda x: (x[0], x[1]), reverse=True)

	# Extract just the paths
	sorted_paths = [item[2] for item in sorted_items]
	return sorted_paths

def All_CARD_files_exist(Directory):	
	if ((os.path.exists(Directory + "\\CARD_Desc.bytes"))
	and (os.path.exists(Directory + "\\CARD_Indx.bytes"))
	and (os.path.exists(Directory + "\\CARD_Name.bytes"))
	and (os.path.exists(Directory + "\\CARD_Prop.bytes"))):
		return 1
	else:
		return 0

def DecryptData(data: bytes, m_iCryptoKey):	
	data = bytearray(data)
	try:
		for i in range(len(data)):
			v = i + m_iCryptoKey + 0x23D
			v *= m_iCryptoKey
			v ^= i % 7
			data[i] ^= v & 0xFF			
		return zlib.decompress(data)		
	except zlib.error:
		#print('zlib.error because of wrong crypo key:' + hex(m_iCryptoKey))		
		return bytearray()
	#except Exception:
	#else:

def DecryptFile(filename):
	with open(f'{filename}', "rb") as f:
		data = bytearray(f.read())

	for i in range(len(data)):
		v = i + m_iCryptoKey + 0x23D
		v *= m_iCryptoKey
		v ^= i % 7
		data[i] ^= v & 0xFF

	with open(f'{filename}' + ".dec", "wb") as f:
		f.write(zlib.decompress(data))

def ReadByteData(filename):
	with open(f'{filename}', "rb") as f:
		data = f.read()
	f.close()
	return data

def WriteDecByteData(filename, data):
	with open(f'{filename}' + ".dec", "wb") as f:
		f.write(data)
	f.close()

def CheckCryptoKey(filename, m_iCryptoKey):	
	data = ReadByteData(filename)	
	if DecryptData(data, m_iCryptoKey) == bytearray():
		return 0
	else:
		return 1

def FindCryptoKey(filename):
	print('No correct crypto key found. Searching for crypto key...')
	m_iCryptoKey = -0x1	
	data = ReadByteData(filename)	
	dec_data = bytearray()	
	while dec_data == bytearray():			
			m_iCryptoKey = m_iCryptoKey + 1				
			dec_data = DecryptData(data, m_iCryptoKey)
			#if os.stat('CARD_Indx.dec').st_size > 0:						
	with open(settings_dir + '!CryptoKey.txt', 'w') as f_CryptoKey:
		f_CryptoKey.write(hex(m_iCryptoKey))
	f_CryptoKey.close()
	print('Found correct crypto key "' + hex(m_iCryptoKey) + '" and wrote it to file "' + settings_dir + '"!CryptoKey.txt".')	
	return m_iCryptoKey

def GetCryptoKey(filename):
	if FileCheck(settings_dir + '!CryptoKey.txt') == 1:
		print('Trying to read crypto key from file...')
		with open(settings_dir + '!CryptoKey.txt', 'rt') as f_CryptoKey:		
				m_iCryptoKey = int(f_CryptoKey.read(),16)			
		f_CryptoKey.close()	
		print('Reading crypto key "' + hex(m_iCryptoKey) + '" from file, checking if it is correct...')
	else:
		m_iCryptoKey = 0x0

	if CheckCryptoKey(filename, m_iCryptoKey) == 1:
		print('The crypto key "' + hex(m_iCryptoKey) + '" is correct.')
	else:
		m_iCryptoKey = FindCryptoKey(filename)	
	return m_iCryptoKey

def Check_files(Filename_list):
	Checked_filename_list = []
	File_found_list = []
	
	for i in range(len(Filename_list)):
		Filename = Filename_list[i]
		
		if Filename.find('.') == -1: #if no dot found in filename			
			if FileCheck(Filename) == 1:
				Checked_filename_list.append(Filename)
			elif FileCheck(Filename + '.bytes') == 1				:
				Checked_filename_list.append(Filename + '.bytes')
			elif FileCheck(Filename + '.txt') == 1:
				Checked_filename_list.append(Filename + '.txt')			
		
		if Filename.find('.dec') ==  len(Filename) - 4: #if ".dec" found at the end of filename
			if FileCheck(Filename) == 1:
				Checked_filename_list.append(Filename)
			elif FileCheck(Filename.replace('.dec', '.bytes.dec')) == 1:
				Checked_filename_list.append(Filename.replace('.dec', '.bytes.dec'))
			elif FileCheck(Filename.replace('.dec', '.txt.dec')) == 1:
				Checked_filename_list.append(Filename.replace('.dec', '.txt.dec'))

		if Filename.find('.dec.json') ==  len(Filename) - 9: #if ".dec.json" found at the end of filename									
			if FileCheck(Filename) == 1:
				Checked_filename_list.append(Filename)				
			if FileCheck(Filename.replace('.dec.json', '.bytes.dec.json')) == 1:				
				Checked_filename_list.append(Filename.replace('.dec.json', '.bytes.dec.json'))				
			if FileCheck(Filename.replace('.dec.json', '.txt.dec.json')) == 1:
				Checked_filename_list.append(Filename.replace('.dec.json', '.txt.dec.json'))
		
		if Filename.find('Replace Guide.txt') !=  -1: #if "Replace Guide.txt" found in filename
			if FileCheck(Filename) == 1:
				Checked_filename_list.append(Filename)
			elif FileCheck(Filename.replace(' ', '_')) == 1:
				Checked_filename_list.append(Filename.replace(' ', '_'))
	
		if len(Checked_filename_list) == i + 1:
			File_found_list.append(True)
		else:
			File_found_list.append(False)
		
	for i in range(len(Checked_filename_list)):
		Filename = Filename_list[i]
		Checked_filename = Checked_filename_list[i]
		File_found = File_found_list[i]
		
		if  File_found == False:
			print('"' + Filename + '" file not found.\nPress <ENTER> to exit.')
			input()
			sys.exit()
			
	return Checked_filename_list

def WriteJSON(l: list, json_file_path: str):
	with open(json_file_path, 'w', encoding='utf8') as f:
		json.dump(l, f, ensure_ascii=False, indent=4)

# The start of Name and Desc is 0 and 4 respectively
def ProgressiveProcessing1(CARD_Indx_filename, filename, start):

	# Read binary index
	with open(CARD_Indx_filename + ".dec", "rb") as f:
		hex_str_list = ("{:02X}".format(int(c))
						for c in f.read())  # Define variables to accept file contents
	dec_list = [int(s, 16) for s in hex_str_list]  # Convert hexadecimal to decimal

	# Get the index of Desc
	indx = []
	for i in range(start, len(dec_list), 8):
		tmp = []
		for j in range(4):
			tmp.append(dec_list[i + j])
		indx.append(tmp)

	def FourToOne(x: List[int]) -> int:
		res = 0
		for i in range(3, -1, -1):
			res *= 16 * 16
			res += x[i]
		return res

	indx = [FourToOne(i) for i in indx]
	indx = indx[1:]
		
	# Convert Decrypted CARD files to JSON files	
	def Solve(data: bytes, desc_indx: List[int]):
		res = []
		for i in range(len(desc_indx) - 1):
			s = data[desc_indx[i]:desc_indx[i + 1]]
			s = s.decode('UTF-8')
			while len(s) > 0 and s[-1] == '\u0000':
				s = s[:-1]
			res.append(s)
		return res

	# Read Desc file
	with open(f"{filename}" + ".dec", 'rb') as f:
		data = f.read()

	desc = Solve(data, indx)
	
	WriteJSON(desc, f"{filename}" + ".dec.json")
	
# A1. Create folders if they doesn't exist

output_dir = MkDir('_Output')
game_files_dir = MkDir('Game files')
settings_dir = MkDir('Settings')
print ('The output directory is: "' + output_dir + '"')
print ('The game files directory is: "' + game_files_dir + '"')
print ('The settings directory is: "' + settings_dir + '"')

# A2. Get Master Duel \LocalData\????????\ folder

LD_BaseDir = Get_LD_BaseDir()
BaseDir = LD_BaseDir + '0000\\'
print('"' + BaseDir + '" will be used as base directory.')

#A3 Delete all files in output folder

Del_all_files_in_dir(output_dir)
Del_all_files_in_dir(game_files_dir)

# A4. Scan game files
#Check if AssetStudioModCLI app exists
AssetStudio_path = '.\\Tools\\AssetStudioModCLI_aelurum\\AssetStudioModCLI.exe'

if FileCheck(AssetStudio_path) == 0:
	print('AssetStudioModCLI app not found in path"' + AssetStudio_path +'".\nPress <ENTER> to exit.')
	input()
	sys.exit()

print('Scanning game files for CARD-related ones...')

Path_list = Sort_by_last_modified_rev(BaseDir)
script_dir = Path(__file__).parent / ''

i = 0
while i < len(Path_list) and not All_CARD_files_exist(game_files_dir):
	# Run an executable with arguments, capture output and check return code
	result = subprocess.run([AssetStudio_path, Path_list[i], "-o", game_files_dir, "-t", "textAsset", "-g", "None","--filter-by-name", "CARD_Desc", "--filter-by-name", "CARD_Indx", "--filter-by-name", "CARD_Name", "--filter-by-name", "CARD_Prop", "--log-level", "error" ], cwd=script_dir, capture_output=True, text=True, check=True)
	#print("Output:", result.stdout)
	#print("Error:", result.stderr)
	i += 1
print('All CARD-related files have been found.')

# B1. Check if CARD_* files exist:

CARD_filename_list = Check_files([game_files_dir + 'CARD_Indx', game_files_dir + 'CARD_Name', game_files_dir + 'CARD_Desc'])
CARD_Indx_filename = CARD_filename_list[0]
CARD_Name_filename = CARD_filename_list[1]
CARD_Desc_filename = CARD_filename_list[2]

# B2. Get crypto key

m_iCryptoKey = GetCryptoKey(CARD_Indx_filename)

# B3. Decrypt card files from section 1

print('Decrypting files...')

for filename in CARD_filename_list:	
	data = ReadByteData(filename)
	data = DecryptData(data, m_iCryptoKey)
	WriteDecByteData(filename, data)
	print('Decrypted file "' + filename + '".')

# B4. Split CARD_Name + CARD_Desc

print('Splitting files...')

if __name__ == '__main__':	
	ProgressiveProcessing1(CARD_Indx_filename, CARD_Name_filename, 0)	
	ProgressiveProcessing1(CARD_Indx_filename, CARD_Desc_filename, 4)

print('Finished splitting files.')

# B5. Check if CARD_Prop_* files exist:

filenames_to_check = [game_files_dir + 'CARD_Prop', game_files_dir + 'CARD_Prop.bytes', game_files_dir + 'CARD_Prop.txt']
check_counter = -1
CARD_Prop_filename = ''

for i in filenames_to_check:
	check_counter += 1		
	if FileCheck(i) == 1 and i.find(game_files_dir + 'CARD_Prop') != -1 and CARD_Prop_filename == '':
		CARD_Prop_filename = i
	if check_counter == len(filenames_to_check)-1 and CARD_Prop_filename == '':
		print('CARD_Prop file not found. The file name must be \"CARD_Prop\", \"CARD_Prop.bytes\" or \"CARD_Prop.txt\".\nPress <ENTER> to exit.')
		input()
		sys.exit()

# B6. Decrypt CARD_Prop

filenames = [CARD_Prop_filename]

print('Decrypting files...')

for name in filenames:
	if FileCheck(name) == 1:
		DecryptFile(name)
		print('Decrypted file "' + name + '".')	
	else:
		print("Could not decrypt file " + name + " because it does not appear to exist.")

# B7. Split CARD_Prop

def WriteJSON(l: list, json_file_path: str):
	with open(json_file_path, 'w', encoding='utf8') as f:
		json.dump(l, f, ensure_ascii=False, indent=4)

filenames = [CARD_Prop_filename]

# The start of CARD_Prop is 8.
def ProgressiveProcessing2(filename):
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
	ProgressiveProcessing2(filenames[0])

print('Finished splitting files.')

#Check if file CARD Name json file exists:
filenames_to_check = [game_files_dir + 'CARD_Name.dec.json', game_files_dir + 'CARD_Name.bytes.dec.json', game_files_dir + 'CARD_Name.txt.dec.json']
check_counter = -1
CARD_Name_filename = ''

for i in filenames_to_check:
	check_counter += 1
	if FileCheck(i) == 1 and i.find('CARD_Name') != -1 and CARD_Name_filename == '':
		CARD_Name_filename = i
		print('Using file "' + CARD_Name_filename + '".')
	if check_counter == len(filenames_to_check)-1 and CARD_Name_filename == '':
		print('CARD_Name file not found. The file name must be \"CARD_Name.dec.json\", \"CARD_Name.bytes.dec.json\" or \"CARD_Name.txt.dec.json\".\nPress <ENTER> to exit.')
		input()
		sys.exit()

#Create list for string replacement instructions:
R_list=['[\n','','    "','','",\n','\n','"\n]','','\\"',"\""]

#Apply string replacement instructions to CARD_Name JSON file:
with open(CARD_Name_filename, 'rt', encoding="utf8") as f_CARD_Name:
	CARD_Name_content = f_CARD_Name.read() #read file content into string variable
	for i in range(0,len(R_list)-1,2): #use list entries for simple string replacement
		CARD_Name_content = CARD_Name_content.replace(R_list[i],R_list[i+1])
	f_CARD_Name.close()

#Write changes to CARD Name JSON text file:
with open(CARD_Name_filename + '.txt', 'wt', encoding="utf8") as f_CARD_Name:
	f_CARD_Name.write(CARD_Name_content)
	f_CARD_Name.close()
print('File "' + CARD_Name_filename + '.txt" written.')

#Move CARD Name JSON text file to output dir
MoveFile(CARD_Name_filename + '.txt', output_dir)

#Check if CARD Prop JSON file exists:
filenames_to_check = [game_files_dir + 'CARD_Prop.Card_IDs.dec.json', game_files_dir + 'CARD_Prop.bytes.Card_IDs.dec.json', game_files_dir + 'CARD_Prop.txt.Card_IDs.dec.json']
check_counter = -1
CARD_Prop_filename = ''

for i in filenames_to_check:
	check_counter += 1
	if FileCheck(i) == 1 and i.find(game_files_dir + 'CARD_Prop') != -1 and CARD_Prop_filename == '':
		CARD_Prop_filename = i
		print('Using file "' + CARD_Prop_filename + '".')
	if check_counter == len(filenames_to_check)-1 and CARD_Prop_filename == '':
		print('CARD_Prop file not found. The file name must be \"CARD_Prop.Card_IDs.dec.json\", \"CARD_Prop.bytes.Card_IDs.dec.json\" or \"CARD_Prop.txt.Card_IDs.dec.json\".\nPress <ENTER> to exit.')
		input()
		sys.exit()

#Create list for string replacement instructions:
R_list=['[\n','','    ','',',\n','\n',']','']
		
#Apply string replacement instructions to CARD_Prop JSON file:
with open(CARD_Prop_filename, 'rt', encoding="utf8") as f_CARD_Prop:
	CARD_Prop_content = f_CARD_Prop.read() #read file content into string variable
	for i in range(0,len(R_list)-1,2): #use list entries for simple string replacement
		CARD_Prop_content = CARD_Prop_content.replace(R_list[i],R_list[i+1])
	f_CARD_Prop.close()

#Write changes to CARD_Prop JSON text file:
with open(CARD_Prop_filename + '.txt', 'wt', encoding="utf8") as f_CARD_Prop:
	f_CARD_Prop.write(CARD_Prop_content)
	f_CARD_Prop.close()
print('File "' + CARD_Prop_filename + '.txt" written.')

#Move CARD_Prop JSON text file to output dir
MoveFile(CARD_Prop_filename + '.txt', output_dir)