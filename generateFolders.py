#!/usr/bin/python3
# -*- coding: utf8 -*-
# Filename: newGenerateFolders.py
#
########################################################################
# This is a program to create folders for grouping files with
# similar names together. For example create a folder 038_FJB_1904-001
# to group the files 038_FJB_1904-001a.tif and 038_FJB_1904-001b.tif
# Rule to determine similarity of names is specified within the function
# compareRule
#
# After folders were generated files are moved into them.
#
# Martina Trognitz (martina.trognitz@oeaw.ac.at)
#
# Specify the path with first variable
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

# list of file formats that should be ignored, such as 'xlsx'
ignoreFileExtensions = []

# Here rule for comparison is defined and applied
def compareRule(origFileName):
    """
    Function that applies a rule to a file name to be comparable to other file
    names. Basically it extracts the file name part to compare with others.
    Example: tif files that only differ in one character at the end, like
    038_FJB_1904-001a.tif and 038_FJB_1904-001b.tif
    """
    compareFileName = origFileName.decode('utf-8').rstrip('.tif')[:-1]
    return compareFileName

if __name__=="__main__":
    # set path
    # ensure that root folder name is unique in collection
    path = u'../data'
    #path = u'testScript'
    print ("######################################################")
    print ("Working with directory: "+path+"\n")

    # scan full directory and create list with files and list with
    # directories, that serve as basis for further processing.
    # the lists are saved in files for later reference.
    fileDirList = []
    dirList = []

    for root, dirs, files in os.walk(path):
        for file in files:
            fileDirList.append(os.path.join(root,file).encode('utf-8'))

    # write file with list of files
    outFile1 = open('filelistFolder.csv','wb')
    for line in fileDirList:
        writeLine = line.decode('utf-8')
        outFile1.write((writeLine+'\n').encode('utf-8'))
    outFile1.close()

    newFolderList = {}

    # append candidate folder to dictionary based on file name part being compared
    for file in fileDirList:
        oldPath, origFileName = os.path.split(file)

        # ignore system files according to list
        if origFileName.decode('utf-8') in ignoreFiles:
            print('ignoring: '+os.path.join(oldPath.decode('utf-8'),origFileName.decode('utf-8')))
            continue

        # ignore files with ending according to list
        if origFileName.decode('utf-8').rsplit('.', 1)[1].lower() in ignoreFileExtensions:
            print('ignoring: '+os.path.join(oldPath.decode('utf-8'),origFileName.decode('utf-8')))
            continue

        # select part of file name to be compared
        compareFileName = compareRule(origFileName)
        print(compareFileName, oldPath)

        # now check if the file is already in the list for folder creation
        if compareFileName not in newFolderList:
            newFolderList[compareFileName]=oldPath.decode('utf-8')

    print('Found',len(newFolderList),'unique name parts.')
    print('Proceeding to create respective folders')

    processedFiles = fileDirList
    failedCounter = 0
    failedList = []
    successCounter = 1

    # create folders for each of collected candidates in list
    for key in newFolderList:
        newFilePath = os.path.join(newFolderList[key],key)
        try:
            os.mkdir(newFilePath)
        except OSError:
            print ("Creation of the directory %s failed" % newFilePath)
            failedCounter+=1
            failedList.append(newFilePath)
        else:
            print ("Successfully created the directory %s " % newFilePath)
            successCounter+=1
            # now move respective files into the new folders
            for file in processedFiles:
                oldPath, origFileName = os.path.split(file)
                # select which file name part to compare (same rule as above)
                compareFileName = compareRule(origFileName)
                if compareFileName == key:
                    os.rename(file, os.path.join(newFilePath, origFileName.decode('utf-8')))

    if failedCounter > 0:
        print('Failed in creating %s directories' % failedCounter)
        print('\n'.join(failedList))
    print('Created %s directories. Done!' % successCounter)
