# Yu-Gi-Oh Master Duel - Scripts for processing Card_* files

## _CARD_decrypt.py
* Decrypts the file specified in the parameter
* You can drag'n'drop an encrypted file on this script in Windows Explorer or use the command line for that, for example "_CARD_decrypt.py CARD_Desc.bytes"

## _CARD_encrypt.py
* Encrypts the file specified in the parameter
* You can drag'n'drop an unencrypted file on this script in Windows Explorer or use the command line for that, for example "_CARD_encrypt.py CARD_Desc.bytes.dec"
* The output file name is the original one plus the extension ".enc".

## _CARD_decrypt_Desc+Indx+Name.py
* Decrypts the CARD_Name, CARD_Desc and CARD_Indx files in one go.

## _CARD_Name+Desc_split.py
* Splits the CARD_Name and CARD_Desc files, so that every name and description is in one line, and converts them to JSON.

## _CARD_merge+calc_index.py
* Merges the CARD_Name and CARD_Desc JSON files and calculates the CARD_Indx file. The original files will be overwritten by this, so make a backup beforehand.

## _find_crypto_key.py
* Brute-forces the crypto key using the file "CARD_Indx" from the same directory
* Writes the found key to the file "!CryptoKey.txt"

## Credits
* [akintos](https://gist.github.com/akintos) for [the original decryption script](https://gist.github.com/akintos/04e2494c62184d2d4384078b0511673b)
* [crazydoomy](https://github.com/crazydoomy) for [the original encryption script](https://discord.com/channels/747402959117353022/938180052984659979/959192997667422228)
* [timelic](https://github.com/timelic) for [the JSON split and merge scripts](https://github.com/timelic/master-duel-chinese-translation-switch)
