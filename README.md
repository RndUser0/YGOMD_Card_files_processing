# Yu-Gi-Oh Master Duel - Scripts for processing Card_* files

## Script descriptions

### _CARD_Desc_find_special_chars.py
* Finds special characters in the card descriptions JSON file and writes them to the file "!Special_chars.txt" in the same folder

### _CARD_Desc_json_to_txt.py
* Converts the card descriptions JSON file to a text file

### _CARD_Name_json_to_txt.py
* Converts the card names JSON file to a text file

### _CARD_Prop_decrypt_and_split_IDs.py
* Decrypts the CARD_Prop file in the same folder
* Extracts all card IDs from it
* Saves them to the original file name plus the extension ".Card_IDs.dec.json"

### _CARD_decrypt.py
* Decrypts the file specified in the parameter
* You can drag'n'drop an encrypted file on this script in Windows Explorer or use the command line for that, for example "_CARD_decrypt.py CARD_Desc.bytes"

### _CARD_encrypt.py
* Encrypts the file specified in the parameter
* You can drag'n'drop an unencrypted file on this script in Windows Explorer or use the command line for that, for example "_CARD_encrypt.py CARD_Desc.bytes.dec".
* The output file name is the original one plus the extension ".enc".

### _CARD_decrypt_Desc+Indx+Name_and_split_Desc+Name
* Decrypts the CARD_Name, CARD_Desc and CARD_Indx files in one go
* Splits the decrypted CARD_Name and CARD_Desc files, so that every name and description is in one line, and converts them to JSON

### _CARD_merge+calc_index.py
* Merges the CARD_Name and CARD_Desc JSON files
* Calculates the new CARD_Indx file
* Encrypts all 3 files
* The original files will be overwritten by this, so make a backup beforehand.

## Links
* [My modding guide with more info on the Card_* files on NexusMods](https://www.nexusmods.com/yugiohmasterduel/articles/3)
* [My Improve Card Text Readibility mod](https://github.com/RndUser0/YGOMD-Improve_Card_Text_Readibility)
 
## Credits
* [akintos](https://gist.github.com/akintos) for [the original decryption script](https://gist.github.com/akintos/04e2494c62184d2d4384078b0511673b)
* [crazydoomy](https://github.com/crazydoomy) for [the original encryption script](https://discord.com/channels/747402959117353022/938180052984659979/959192997667422228)
* [timelic](https://github.com/timelic) for [the JSON split and merge scripts](https://github.com/timelic/master-duel-chinese-translation-switch)
