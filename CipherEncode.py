# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
import binascii
import secrets
from sys import argv

def main():
    
    # get name of csv to read in and write out
    script, txt_file_name = argv
    txt_to_encrypt = open(txt_file_name, "r", encoding="utf-8-sig")
    txt_to_encrypt = txt_to_encrypt.read()
    txt_to_encrypt = txt_to_encrypt.encode("utf-8")
    
    key = secrets.token_bytes(32)
    print(key)
    monomer_string = str(binascii.b2a_hex(key))
    monomer_string = monomer_string[2:(len(monomer_string) - 1)]
    
    key_file = open("secret_key.txt", 'w+')
    key_file.write(monomer_string)
    key_file.close()

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(txt_to_encrypt)
    
    file_out = open("encrypted.bin", "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()
    
main ()
