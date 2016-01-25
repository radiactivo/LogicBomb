import os
import win32file

dir_origen = 'C:\\Users\\radiactivo\\Desktop\\'
dir_destino = 'C:\\Users\\radiactivo\\Desktop\\CryptoTest\\'

files[
    'C:\\Users\\radiactivo\\Desktop\\gzip-1.3.12.tar',
    'C:\\Users\\radiactivo\\Desktop\\HelloWorld.exe',
    'C:\\Users\\radiactivo\\Desktop\\image.jpg',
    'C:\\Users\\radiactivo\\Desktop\\text.txt' ]

#
# Do a straight copy first, then try to copy without
# failing on collision, then try to copy and fail on
# collision. The first two should succeed; the third
# should fail.
#
def copy():
    win32file.CopyFile (orig_file, copy_file, 1)
    win32file.CopyFile (orig_file, copy_file, 0)
    win32file.CopyFile (orig_file, copy_file, 1)
    if os.path.isfile (copy_file): print "Success"


for orig_file in files:
    open(orig_file , "w").close()
    os.remove(dir_destino + orig_file[len(dir_origen):])
    copy_file = dir_destino + orig_file[len(dir_origen):]
    copy()
