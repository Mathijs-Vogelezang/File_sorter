import os
import shutil
import re


def sortfile(file, destinationfolder, subfolders=[]):
    '''Sorts files based on folders in destination folder'''
    folderpaths = []
    if subfolders == []:
        paths = os.listdir(destinationfolder)
        for path in paths:
            fullpath = os.path.join(destinationfolder, path)
            if os.path.isdir(fullpath):
                subfolders.append(path)
                folderpaths.append(fullpath)
    else:
        for folder in subfolders:
            fullpath = os.path.join(destinationfolder, folder)
            folderpaths.append(fullpath)

    sorted = False
    for i in range(len(subfolders)):
        searchterm = subfolders[i].replace(' ', '.+')
        if re.search(searchterm.lower(), os.path.basename(file).lower()):
            copy(file, folderpaths[i])
            sorted = True

    if not sorted:
        copy(file, destinationfolder)


def copy(file, destination):
    if os.path.exists(os.path.join(destination, os.path.basename(file))):
        indicator = 1  # Copy indicator
        name, extension = os.path.splitext(os.path.basename(file))
        while True:
            filename = name + ' (' + str(indicator) + ')' + extension
            if os.path.exists(os.path.join(destination, filename)):
                indicator += 1
            else:
                shutil.copy2(file, os.path.join(destination, filename))
                break
    else:
        shutil.copy2(file, destination)
