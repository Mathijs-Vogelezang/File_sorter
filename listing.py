import os


def listfiles(rootfolder):
    '''List all files in directory and subdirectories'''
    dirs = os.listdir(rootfolder)

    files = []
    folders = []
    for dir in dirs:
        fullpath = os.path.join(rootfolder, dir)
        if os.path.isfile(fullpath):
            files.append(fullpath)
        else:
            folders.append(fullpath)

    for folder in folders:
        files.extend(listfiles(folder))

    return files


def listsubfolders(rootfolder):
    '''List all subdirectories and their subdirectories of folder'''
    dirs = os.listdir(rootfolder)

    folders = []
    for dir in dirs:
        fullpath = os.path.join(rootfolder, dir)
        if os.path.isdir(fullpath):
            folders.append(fullpath)

    for folder in folders:
        folders.extend(listsubfolders(folder))

    return folders


def listfolders(rootfolder):
    '''List all subdirectories of folder, but not their subdirectories'''
    dirs = os.listdir(rootfolder)

    folders = []
    for dir in dirs:
        fullpath = os.path.join(rootfolder, dir)
        if os.path.isdir(fullpath):
            folders.append(dir)

    return folders
