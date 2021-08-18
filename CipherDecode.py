# -*- coding: utf-8 -*-

from Cryptodome.Cipher import AES
from sys import argv
import pandas as pd


def main ():
    # get name of csv to read in and write out
    script, encrypted_file, monomer_hex_assignment, LCMS_template = argv

    # open and parse file to be decrypted
    encrypted_text = open(encrypted_file, "rb")
    nonce, tag, ciphertext = [ encrypted_text.read(x) for x in (16, 16, -1) ]

    # DELETE THIS LATER
    key = b'\xa5\xe9\x8f$\x0e\x0f\x13\xe9\xf34\xee\xe10\x17\xa7o{\xe1\x8f\\H\xd8\\0\xb7T3\x98\xc9[oH'

    masses = []

    lcms_mass_workbook = pd.read_excel(LCMS_template, index_col = 0, header = 0)
    for index, row in lcms_mass_workbook.iterrows():
        for x in range (len(lcms_mass_workbook.columns)):
            if (len(row.iloc[x]) > 4):
                masses.append(row.iloc[x])
            else:
                continue
            
    print(masses)


    codes_workbook = pd.read_excel(monomer_hex_assignment, index_col=None, header=0, dtype={'Monomer':str, "Mass":float, "NBD Mass":float})
    s = (codes_workbook['Monomer'].loc[codes_workbook['Mass'] == 103.06]).iloc[0]

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