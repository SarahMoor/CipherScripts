# -*- coding: utf-8 -*-

from Cryptodome.Cipher import AES
from sys import argv
import xlrd


def main ():
    # get name of csv to read in and write out
    # script, encrypted_file, LCMS_template, monomer_hex_assignment = argv
    script, encrypted_file = argv
    encrypted_text = open(encrypted_file, "rb")
    nonce, tag, ciphertext = [ encrypted_text.read(x) for x in (16, 16, -1) ]
    key = b'\xa5\xe9\x8f$\x0e\x0f\x13\xe9\xf34\xee\xe10\x17\xa7o{\xe1\x8f\\H\xd8\\0\xb7T3\x98\xc9[oH'
    
    '''
    codes_workbook = xlrd.open_workbook(monomer_hex_assignment)
    sheet1 = codes_workbook.sheet_by_index(0)
    sheet1.cell_value(0, 0)
    hex_codes = {}

    for j in range(1, sheet1.nrows):
        hex_codes[(sheet1.cell_value(j, 0))] = (
            sheet1.cell_value(j, 1),
            sheet1.cell_value(j, 2),
        )
    '''
    
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        data = data.decode('utf-8')
        decrypted_file = open("decrypted_file.txt", 'w+')
        decrypted_file.write(data)
        decrypted_file.close()
    except ValueError:
        print("Incorrect Key")
    
main ()