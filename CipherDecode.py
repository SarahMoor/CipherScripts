# -*- coding: utf-8 -*-

from Cryptodome.Cipher import AES
from sys import argv
import xlrd


def main ():
    # get name of csv to read in and write out
    script, encrypted_file, LCMS_template, monomer_hex_assignment = argv
    encrypted_text = open("encrypted_file", "rb")
    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
    

    codes_workbook = xlrd.open_workbook(monomer_hex_assignment)
    sheet1 = codes_workbook.sheet_by_index(0)
    sheet1.cell_value(0, 0)
    hex_codes = {}

    for j in range(1, sheet1.nrows):
        hex_codes[(sheet1.cell_value(j, 0))] = (
            sheet1.cell_value(j, 1),
            sheet1.cell_value(j, 2),
        )
    
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    
    print (data)

main ()