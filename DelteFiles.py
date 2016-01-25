import os, fnmatch

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))

    return result


list_of_files = find('*.*', 'C:\\Users\\radiactivo\\Desktop\\EncriptedFiles\\')
for filename in list_of_files:
    os.remove(filename)
