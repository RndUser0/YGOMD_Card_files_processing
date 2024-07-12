# python3
import fileinput
import re
import sys

def FileCheck(fn):
    try:
      open(fn, 'r')
      return 1
    except IOError:
      # print 'Error: File does not appear to exist.'
      return 0

#Check if file CARD Desc json file exists:
filenames_to_check = ['CARD_Desc.dec.json', 'CARD_Desc.bytes.dec.json', 'CARD_Desc.txt.dec.json']
check_counter = -1
CARD_Desc_filename = ''

for i in filenames_to_check:
	check_counter += 1
	if FileCheck(i) == 1 and i.find('CARD_Desc') != -1 and CARD_Desc_filename == '':
		CARD_Desc_filename = i
		print('Using file "' + CARD_Desc_filename + '".')
	if check_counter == len(filenames_to_check)-1 and CARD_Desc_filename == '':
		print('CARD_Desc file not found. The file name must be \"CARD_Desc.dec.json\", \"CARD_Desc.bytes.dec.json\" or \"CARD_Desc.txt.dec.json\".\nPress <ENTER> to exit.')
		input()
		sys.exit()

#Create list for string replacement instructions:
R_list=['[\n','','    "','','",\n','\n','"\n]','','\\"',"\""]
		
#Apply string replacement instructions to CARD_Desc JSON file:
with open(CARD_Desc_filename, 'rt', encoding="utf8") as f_CARD_Desc:
	CARD_Desc_content = f_CARD_Desc.read() #read file content into string variable
	for i in range(0,len(R_list)-1,2): #use list entries for simple string replacement
		CARD_Desc_content = CARD_Desc_content.replace(R_list[i],R_list[i+1])
	f_CARD_Desc.close()

#Write changes to CARD Desc JSON file:
with open(CARD_Desc_filename + '.txt', 'wt', encoding="utf8") as f_CARD_Desc:
	f_CARD_Desc.write(CARD_Desc_content)
	f_CARD_Desc.close()

print('File "' + CARD_Desc_filename + '.txt" written.')

'''
print("Press <ENTER> to continue")
input()
'''