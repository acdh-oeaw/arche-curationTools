# -*- coding: utf8 -*-
# Filename: renameFiles.py
#
########################################################################
# This is a program to rename files and folders in
# a given folder by applying a set of renaming rules
#
# Martina Trognitz (martina.trognitz@oeaw.ac.at)
#
# Specify the path with the variable path
# To see if rules work without actually renaming, set rename to false
#
########################################################################
from __future__ import unicode_literals

from builtins import list, str
from io import open

import os, os.path
import unicodedata
import re

# list of files that should be ignored, such as system files like 'Thumbs.db'
ignoreFiles = ['Thumbs.db', '.DS_Store']

# list of file formats in lower case that should be ignored, such as 'xlsx'
ignoreFileExtensions = []

def normaliseName(value):
    """
    Normalises or renames a string, replaces 'something' with 'something else'
    add anything else you need; examples are commented

    Order of rules does matter for custom replacements.

    At the end all remaining invalid characters are removed (i.e. replaced with '')
    """
    # split into name and extension
    newValue, fileExt = os.path.splitext(value)
    # replace umlauts with two letters
    newValue = newValue.replace('ä','ae')
    newValue = newValue.replace('ö','oe')
    newValue = newValue.replace('ü','ue')
    newValue = newValue.replace('Ä','Ae')
    newValue = newValue.replace('Ö','Oe')
    newValue = newValue.replace('Ü','Ue')
    newValue = newValue.replace('ß','ss')
    # replace all other special characters
    # normalise, i. e. replace e.g. é with e
    newValue = unicodedata.normalize('NFKD', newValue).encode('ascii', 'ignore')
    newValue = newValue.decode('utf-8')
    # some custom rules to serve as example
#    newValue = newValue.replace(', ','_')
#    newValue = newValue.replace(',','_')
#    newValue = newValue.replace('+','_')
#    newValue = newValue.replace(' - ','-')
#    newValue = newValue.replace(' ','_')
    # you can also use regular expressions e. g.:
    # newValue = str(re.sub(r'(\()([\d]\))', r'-\2', newValue))
    # '( one number )' becomes '-number)'

    # all remaining invalid characters are removed
    # \ and / are kept to keep the path
    newValue = str(re.sub('[^a-zA-Z0-9_\-/\\\]', '', newValue))

    return newValue+fileExt


if __name__=="__main__":
    # set path
    #path = u'../data'
    #path = u'../../testData'
    # set rename to 'true' if renaming should be done
    rename = 'false'
    print ("######################################################")
    print ("Working with directory: "+path+"\n")

    # scan full directory and create list with files and list with
    # directories, that serve as basis for further processing.
    # the lists are saved in files for later reference.
    fileDirList = []
    dirList = []

    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dirList.append(os.path.join(root,dir).encode('utf-8'))
        for file in files:
            fileDirList.append(os.path.join(root,file).encode('utf-8'))

    # write file with list of files
    outFile1 = open('filelist.csv','wb')
    for line in fileDirList:
        writeLine = line.decode('utf-8')
        outFile1.write((writeLine+'\n').encode('utf-8'))
    outFile1.close()

    # write file with list of directories
    outFile2 = open('dirlist.csv','wb')
    for line in dirList:
        writeLine = line.decode('utf-8')
        outFile2.write((writeLine+'\n').encode('utf-8'))
    outFile2.close()

    # rename files
    # has to be done before directories are renamed,
    # otherwise they won't be found anymore
    fileCounter = 0
    fileRenameCounter = 0
    exceptedFiles = []
    renamedFiles = []
    decoded_fileDirList = [x.decode('utf-8') for x in fileDirList]
    for file in fileDirList:
        oldPath, origFileName = os.path.split(file)
        fileCounter+= 1

        # ignore system files according to list
        if origFileName.decode('utf-8') in ignoreFiles:
            print('ignoring: '+os.path.join(oldPath.decode('utf-8'),origFileName.decode('utf-8')))
            continue

        # ignore files with extension according to list
        # can only be done when there is an extension
        origFileNamePart, origFileExtension = os.path.splitext(origFileName.decode('utf-8'))
        if len(origFileExtension) == 0:
            print('File does not have extension:',  origFileName.decode('utf-8'))
        else:
            if origFileName.decode('utf-8').rsplit('.', 1)[1].lower() in ignoreFileExtensions:
                print('ignoring: '+os.path.join(oldPath.decode('utf-8'),origFileName.decode('utf-8')))
                continue

        # get normalised (renamed) file name
        newFile = normaliseName(origFileName.decode('utf-8'))
        newFilePath = os.path.join(oldPath.decode('utf-8'), newFile)
        # append old file with path and new file with path to list
        # new file path might be same as before, also append new file name
        renamedFiles.append([file.decode('utf-8'), newFilePath, newFile])

        if newFile != origFileName.decode('utf-8'):
            fileRenameCounter+=1
            print('Normalised "', origFileName.decode('utf-8'), '" to ', newFile)
            if newFilePath in decoded_fileDirList:
                print('The file could not be renamed, because a file with the same name already exists!')
                exceptedFiles.append(file)

        # rename file if rename was set to true
        # collect files that cannot be renamed due to file name duplication
        if rename == 'true':
            try:
                os.rename(file, newFilePath)
            except FileExistsError:
                continue

    # rename directories, starting from within, i.e. reverse order of dirList
    dirCounter = 0
    dirRenameCounter = 0
    renamedDirs = []
    for dir in dirList[::-1]:
        dirCounter+= 1
        oldPath, oldDir = os.path.split(dir)
        newDir = normaliseName(oldDir.decode('utf-8'))
        newDirPath = os.path.join(oldPath.decode('utf-8'), newDir)
        # append old directories with path and new directories with path to list
        # new path might be same as before, also append new directory name
        renamedDirs.append([dir.decode('utf-8'), newDirPath, newDir])

        if newDir != oldDir.decode('utf-8'):
            dirRenameCounter+=1
            print('Normalised "', oldDir.decode('utf-8'), '" to ', newDir)

        if rename == 'true':
            os.rename(dir, newDirPath)

    actualFileRenameCounter = fileRenameCounter - len(exceptedFiles)
    print('Renamed ', actualFileRenameCounter, ' files of a total of ', fileCounter, 'files.')
    print('Renamed ', dirRenameCounter, ' directories of a total of ', dirCounter, 'directories.')
    if len(exceptedFiles)<1:
        print('No errors in renaming.')
    else:
        print('Some files could not be renamed. Manual action is required.')
        str_exceptedFiles = [x.decode('utf-8') for x in exceptedFiles]
        print('\n'.join(str_exceptedFiles))

    print('Creating file and directory list with new names')
    # write file with list of files and new names
    outFile3 = open('renamedFilelist.csv','wb')
    outFile3.write(('Old file;New file;New file name'+'\n').encode('utf-8'))
    for entry in renamedFiles:
        writeLine = ';'.join(entry) #entry.decode('utf-8')
        outFile3.write((writeLine+'\n').encode('utf-8'))
    outFile3.close()

    # write file with list of directories and new names
    # writing reverse order of renamedDirs
    outFile4 = open('renamedDirlist.csv','wb')
    outFile4.write(('Old path;New path;New folder name'+'\n').encode('utf-8'))
    for entry in renamedDirs[::-1]:
        writeLine = ';'.join(entry)
        outFile4.write((writeLine+'\n').encode('utf-8'))
    outFile4.close()
    print('Done')
