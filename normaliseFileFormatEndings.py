#!/usr/bin/python3
# -*- coding: utf8 -*-
# Filename: renameFiles.py
#
########################################################################
# This is a naive program to normalise file format endings 
# (those after the dot) to lowercase format, i.e. TIF to tif
# It might be expanded later on to normalise further, e.g. tif to tiff
#
# Martina Trognitz (martina.trognitz@oeaw.ac.at)
#
# Specify the path with the variable path
# To see if normalising works, set normalise to false
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

# list of file extension in lower case that should be ignored, such as 'xlsx'
ignoreFileExtensions = []

def normaliseName(value):
    """
    Normalises file extesion to all lower case.
    """
    # split into name and extension
    fileName, fileExt = os.path.splitext(value)
    newFileExt = fileExt.lower()

    return fileName+newFileExt


if __name__=="__main__":
    # set path
    #path = u'../data'
    #path = u'../../testData'
    # set rename to 'true' if renaming should be done
    rename = 'false'
    print ("######################################################")
    print ("Renaming set to: "+rename+"\n")
    # TODO: introduce a pause here, asking for continuation
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

    # normalise file extension
    # has to be done before directories are renamed,
    # otherwise they won't be found anymore
    fileCounter = 0
    fileRenameCounter = 0
    exceptedFiles = []
    renamedFiles = []
    for file in fileDirList:
        oldPath, origFileName = os.path.split(file)
        fileCounter+= 1

        # ignore files with extension according to list
        # can only be done when there is an extension
        origFileNamePart, origFileExtension = os.path.splitext(origFileName.decode('utf-8'))
        if len(origFileExtension) == 0:
            print('File does not have extension:',  origFileName.decode('utf-8'))
        else:
            if origFileName.decode('utf-8').rsplit('.', 1)[1].lower() in ignoreFileExtensions:
                print('ignoring: '+os.path.join(oldPath.decode('utf-8'),origFileName.decode('utf-8')))
                continue

        # get file name with normalised file extesion
        newFile = normaliseName(origFileName.decode('utf-8'))
        newFilePath = os.path.join(oldPath.decode('utf-8'), newFile)
        # append old file with path and new file with path to list
        # new file path might be same as before, also append new file name
        renamedFiles.append([file.decode('utf-8'), newFilePath, newFile])

        if newFile != origFileName.decode('utf-8'):
            fileRenameCounter+=1
            print('Normalised "', origFileName.decode('utf-8'), '" to ', newFile)

        # rename file if rename was set to true
        # collect files that cannot be renamed due to file name duplication
        if rename == 'true':
            try:
                os.rename(file, newFilePath)
            except FileExistsError:
                print('The file could not be renamed, because a file with the same name already exists!')
                exceptedFiles.append(file)

    actualFileRenameCounter = fileRenameCounter - len(exceptedFiles)
    print('Renamed ', actualFileRenameCounter, ' files of a total of ', fileCounter, 'files.')
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

    print('Done')
