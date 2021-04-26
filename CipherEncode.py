# -*- coding: utf-8 -*-

from Cryptodome.Cipher import AES


def main():
    #### Need to figure out how they generate key from that string
    key = b'1fbf74bbc74a4bde'
    cipher = AES.new(key, AES.MODE_EAX)
    
    
    ### need to 
    ciphertext, tag = cipher.encrypt_and_digest(b'SECRETSECTRETSSECRETS')
    
    file_out = open("encrypted.bin", "wb")
    [ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
    file_out.close()
    
    
main ()
