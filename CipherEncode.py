# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import secrets

def main():
    
    key = secrets.token_bytes(32)
    print(binascii.b2a_hex(key))  

    cipher = AES.new(key, AES.MODE_EAX)
    
    
    ### need to 
    ciphertext, tag = cipher.encrypt_and_digest(b'SECRETSECTRETSSECRETS')
    
    file_out = open("encrypted.bin", "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()
    
main ()
