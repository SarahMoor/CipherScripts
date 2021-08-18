# -*- coding: utf-8 -*-

from Cryptodome.Cipher import AES
from sys import argv
import xlrd

global hex_codes
global huff_dict

def HexToDecimal(hex_string):
    """
    Convert Hexadecimal numbers to Binary.

    Parameters
    ----------
    hex_string : string
        Takes in formatted hexstring derived from mass data.

    Returns
    -------
    res : string
        returns the resulting binary string.

    """
    n = int(hex_string, 16)
    bStr = ""
    while n > 0:
        bStr = str(n % 2) + bStr
        n = n >> 1
    res = bStr

    return res

def MassToHex(value1, value2):
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
    for i in hex_codes.values():
        if (i[0] + 1.5 >= mass_match and i[0] - 1.5 <= mass_match) or (
            i[1] + 1.5 >= mass_match and i[1] - 1.5 <= mass_match
        ):
            print(value1, value2, mass_match)
            return list(hex_codes.keys())[list(hex_codes.values()).index(i)]
    print(mass_match, "NOT MATCHED")


def MakeBitstring(sheet):
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
    hex_padding = "000"
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
                    else:
                        if hex_value == "0":
                            num = "0000"
                        else:
                            num = HexToDecimal(str(hex_value))
                        print(hex_value, hex_padding[len(str(num)) - 1 :] + str(num))
                        encoded_bitstring += hex_padding[len(str(num)) - 1 :] + str(num)

    return encoded_bitstring


def main ():
    # get name of csv to read in and write out
    script, huff_codes, hex_code, LCMS_template = argv
    file_in = open("encrypted.bin", "rb")
    nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]
    
    key = b'1fbf74bbc74a4bda'
    
    
    ### MONOMER TO HEX CODES ####
    # open workbook with hex_codes
    codes_workbook = xlrd.open_workbook(hex_code)
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