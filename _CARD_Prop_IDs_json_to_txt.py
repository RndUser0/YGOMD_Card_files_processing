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

#Check if CARD Prop json file exists:
filenames_to_check = ['CARD_Prop.Card_IDs.dec.json', 'CARD_Prop.bytes.Card_IDs.dec.json', 'CARD_Prop.txt.Card_IDs.dec.json']
check_counter = -1
CARD_Prop_filename = ''

for i in filenames_to_check:
	check_counter += 1
	if FileCheck(i) == 1 and i.find('CARD_Prop') != -1 and CARD_Prop_filename == '':
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

#Write changes to CARD Name JSON file:
with open(CARD_Prop_filename + '.txt', 'wt', encoding="utf8") as f_CARD_Prop:
	f_CARD_Prop.write(CARD_Prop_content)
	f_CARD_Prop.close()

print('File "' + CARD_Prop_filename + '.txt" written.')

'''
print("Press <ENTER> to continue")
input()
'''