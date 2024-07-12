#Find unicode characters in card descriptions
from _defs import *

CARD_Desc_JSON_filename = Check_files(['CARD_Desc.dec.json'])[0]

CARD_Desc_list = []

print('Reading CARD_Desc file into list...')

total_lines = CountFileLines(CARD_Desc_JSON_filename)

with open(CARD_Desc_JSON_filename, 'rt', encoding="utf8") as f_CARD_Desc_JSON:
	line_counter = 0	
	for line in f_CARD_Desc_JSON:
		line_counter += 1
		line = line.strip('\n') #remove line break
		if line_counter > 1 and line_counter < total_lines - 1:
			CARD_Desc_list.append(line[5:len(line)-2]) #Leave out the 4 leading spaces and quotation marks and comma at the end of the line
		elif line_counter == total_lines - 1:
			CARD_Desc_list.append(line[5:len(line)-1]) #Leave out the 4 leading spaces and quotation marks at the end of the line
f_CARD_Desc_JSON.close()

print('Completed.\nSearching for special characters in Card_Desc JSON')

Special_char_list = []

for i in range(len(CARD_Desc_list)):	
	for j in range(len(CARD_Desc_list[i])):
		if ord(CARD_Desc_list[i][j]) > 255:
			Special_char_list.append(CARD_Desc_list[i][j])

Special_char_list = sorted(list(set(Special_char_list)))

with open('Special_chars.txt', 'wt', encoding="utf8") as f:
	for i in range(len(Special_char_list)):			
		f.write(Special_char_list[i] + '\n')
f.close()
print('Completed.')