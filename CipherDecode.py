# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from sys import argv
import pandas as pd
import openpyxl


def MakeHexstring(sheet, codes_workbook):
    """
    Takes in excel sheet with templated LC/MS data and converts this first to
    it's hexadecimal format, and then to binary

    Parameters
    ----------
    sheet : xlsx reader object
        Templated LC/MS data in an excel sheet.

    Returns
    -------
    encoded_bitstring : string
        binary digits (0s and 1s) in string format.

    """
    encoded_bitstring = ""
    for i in range(sheet.nrows):
        for j in range(sheet.ncols):
            if len(sheet.cell_value(i, j)) > 3:
                cells = sheet.cell_value(i, j).strip(" ")
                cells = sheet.cell_value(i, j).split(",")
                for k in range(0, len(cells)):
                    value1 = cells[k]
                    if k == len(cells) - 1:
                        value2 = 0
                    else:
                        value2 = cells[k + 1]
                    hex_value = str(MassToHex(value1, value2))[0]
                    
                    # skipping over starting index monomer!
                    if hex_value == "e" and k == 0:
                        continue

                    print(hex_value)
                    encoded_bitstring += hex_value

    return encoded_bitstring

def MassToHex(value1, value2, hex_codes):
    """
    Match LC/MS Masses to Monomers

    Parameters
    ----------
    value1 : int
        Parent mass.
    value2 : int
        Mass after loss of one unknown monomer.

    Returns
    -------
    hexadecimal character from list : string
        Gets the difference between value1 and value2 to see which monomer was
        lost, then returns monomer that matches this mass difference.

    """
    
    
    mass_match = float(value1) - float(value2)

    if (i[0] + 1.5 >= mass_match and i[0] - 1.5 <= mass_match) or (
        i[1] + 1.5 >= mass_match and i[1] - 1.5 <= mass_match
    ):
        print(value1, value2, mass_match)
            
        return () 
    
    else:
        print("MONOMER NOT FOUND")



def ConvertToFloat(mass_list):
    total_list = []
    for x in mass_list:
        temp_list = []
        for y in x:
            print(y)
            y = float(y)
            temp_list.append(y)
        total_list.append(temp_list)
    return total_list


def main ():
    # get name of csv to read in and write out
    script, encrypted_file, monomer_hex_assignment, LCMS_template = argv

    # open and parse file to be decrypted
    encrypted_text = open(encrypted_file, "rb")
    nonce, tag, ciphertext = [ encrypted_text.read(x) for x in (16, 16, -1) ]
    
    codes_workbook = pd.read_excel(monomer_hex_assignment, index_col=None, header=0, dtype={'Monomer':str, "Mass":float, "NBDMass":float})
    s = (codes_workbook['Monomer'].loc[codes_workbook['Mass'] == 103.06]).iloc[0]
    d = codes_workbook['Mass'][0]
    e = codes_workbook['NBDMass']
    print(d)
    print(103.06 in codes_workbook.Mass.values)
    print(103.06 in codes_workbook.NBDMass.values)
    


    # DELETE THIS LATER
    key = b'\xa5\xe9\x8f$\x0e\x0f\x13\xe9\xf34\xee\xe10\x17\xa7o{\xe1\x8f\\H\xd8\\0\xb7T3\x98\xc9[oH'

    masses = []


    '''
    lcms_mass_workbook = pd.read_excel(LCMS_template, index_col = 0, header = 0)
    print(lcms_mass_workbook)
    for index, row in lcms_mass_workbook.iterrows():
        print(row)
    
    template_workbook = xlrd.open_workbook(LCMS_template)
    LCMSsheet = template_workbook.sheet_by_index(0)

    # convert hex codes to binary representation
    encoded_bitstring = MakeHexstring(LCMSsheet, codes_workbook)
            

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        data = data.decode('utf-8')
        decrypted_file = open("decrypted_file.txt", 'w+')
        decrypted_file.write(data)
        decrypted_file.close()
    except ValueError:
        print("Incorrect Key")
    '''

main ()