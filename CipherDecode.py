# -*- coding: utf-8 -*-

from Cryptodome.Cipher import AES

def main ():

    file_in = open("encrypted.bin", "rb")
    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
    
    # let's assume that the key is somehow available again
    key = b'1fbf74bbc74a4bda'
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    
    print (data)

main ()