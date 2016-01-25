# -*- coding: utf-8 -*-
import os, fnmatch, hashlib, base64, re, hashlib
from Crypto.Cipher import DES
from pyPdf import PdfFileReader

#############################################################################
# NAME: encrypt()                                                           #
# DESCRIPTION: This function encrypts a bunch of data (text),               #
#           based on a key received.                                        #
# RETURN: It returns the encrypted data (cipher).                           #
#############################################################################
def encrypt(text):
    b = 8 - len(text)%8
    padd = ""
    if b:
        padd =  "." + "X" * (b - 1)
    des = DES.new(key, DES.MODE_ECB)
    cipher = des.encrypt(text + padd)
    encoded_cipher = base64.b64encode(cipher)
    print "Length encoded cipher: ",len(encoded_cipher)
    return encoded_cipher

#############################################################################
# NAME: decrypt()                                                           #
# DESCRIPTION: This function decrypts a bunch of data (text),               #
#           based on a key received.                                        #
# RETURN: It returns the plain data.                                        #
#############################################################################
def decrypt(encoded_cipher):
    des = DES.new(key, DES.MODE_ECB)
    cipher = base64.b64decode(encoded_cipher)
    text = des.decrypt(cipher)
    charref = re.compile("\.X{0,7}" , re.VERBOSE)
    match_str = re.sub(charref , "" , text[len(text) - 8:])
    text_corrected = text[:len(text) - 8] + match_str
    print "Length decoded cipher: ", len(text_corrected )
    return text_corrected

#############################################################################
# NAME: find()                                                              #
# DESCRIPTION: This function finds a regex pattern in a list of files       #
#            of a directory.                                                #
# RETURN: It returns the set of files matching the pattern                  #
#############################################################################
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))

    return result

def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), ""):
            hash.update(chunk)
    return hash.hexdigest()

checkCondition = lambda: os.path.exists("C:\\Program Files\\CrypTool\\") & os.path.isfile("C:\\Program Files\\CrypTool\\CrypTool.exe") & os.path.isfile("C:\\Users\\radiactivo\\Desktop\\sample.pdf")

key = lambda: hashlib.sha256(PdfFileReader(file("C:\\Users\\radiactivo\\Desktop\\sample.pdf" , "rb")).getDocumentInfo()['/CreationDate']).digest()[:8]

if checkCondition() == False:
    exit()

key = key()
list_of_files = find('*.*', 'C:\\Users\\radiactivo\\Desktop\\CryptoTest\\')

for filename in list_of_files:
    hash_orig_file = md5(filename)
    with open(filename, 'rb+') as fd:
        # simplemente hacer "for line in f", lo que te daria "line"
        # Además, esto te cierra solo el objeto.
        buffer = fd.read()
        print "Length original: ", len(buffer)
        fd.seek(0)
        fd.write(encrypt(buffer))
    with open(filename, 'rb+') as fd:
        buffer = fd.read()
        fd.seek(0)
        fd.write(decrypt(buffer))
    hash_recovered_file = md5(filename)
    if hash_recovered_file == hash_orig_file:
        print "MATCH:", hash_orig_file," = ", hash_recovered_file
