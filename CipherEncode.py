# -*- coding: utf-8 -*-
import os
import argparse
import binascii
import secrets
from Cryptodome.Cipher import AES


def GetArgs():
    '''
    parses script arguments to make running this script more intuitive

    Raises
    ------
    FileNotFoundError
        raises error if file cannot be found.

    Returns
    -------
    args : string
        returns the filename of the txt to be encrypted.

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', metavar='\b',
                        help="name of file to be encrypted", action="store", dest="filename")
    args = parser.parse_args()

    # Check if file exists
    if os.path.exists('{}'.format(args.filename)) is False:
        print('{}'.format(args.filename))
        raise FileNotFoundError('Cannot find {}'.format(args.filename))

    return args


def main():
    # get name of csv to read in and write out
    #script, txt_file_name = argv

    args = GetArgs()
    txt_file_name = args.filename

    # open txt to be encrypted
    txt_to_encrypt = open(txt_file_name, "r", encoding="utf-8-sig")
    txt_to_encrypt = txt_to_encrypt.read()
    txt_to_encrypt = txt_to_encrypt.encode("utf-8")

    # randomly generate 32 bytes to encrypt the file with
    key = secrets.token_bytes(32)

    # convert the files to monomers and output key as a txtfile to synthesize the key
    monomer_string = str(binascii.b2a_hex(key))
    monomer_string = monomer_string[2:(len(monomer_string) - 1)]
    key_file = open("secret_key.txt", 'w+')
    key_file.write(monomer_string)
    key_file.close()

    # create cipher and encrypt
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(txt_to_encrypt)

    # write out encrypted file as a .bin file
    file_out = open("encrypted.bin", "wb")
    [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    file_out.close()


main()
