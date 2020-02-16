# -*- coding: utf8 -*-
# Filename: deleteSystemFiles.py
#
########################################################################
# This is a program to delete system files as e.g. thumbs.db or .DS_Store
#
# Martina Trognitz (martina.trognitz@oeaw.ac.at)
#
# Specify the path with first variable
# Specify further filenames in list
#
########################################################################
from __future__ import unicode_literals

import os, os.path

if __name__=="__main__":
    # set path
    # ensure that root folder name is unique in collection
    path = r'..\data'
    print ("Working with directory: "+path+"\n")
    # set files to be deleted
    fileList = ['Thumbs.db', '.DS_Store']

    # scan full directory and count and list files to be deleted
    deleteCounter = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            for filename in fileList:
                if str(file) == filename:
                    print ("File for deletion: " +str(file))
                    deleteCounter +=1
                    print (os.path.join(root, file))

    print ("Delete "+str(deleteCounter)+" files?\n")
    # will only delete listed files if 'yes'
    continueDeletion = input("...(enter yes or no): ")

    # if deletion shall be continued scan full directory
    # count and list files that are deleted
    if continueDeletion == 'yes':
        print ("Proceeding with deletion")
        deleteCounter = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                for filename in fileList:
                    if str(file) == filename:
                        print ("Deleting: " +str(file))
                        deleteCounter +=1
                        print (os.path.join(root, file))
                        os.remove(os.path.join(root, file))
        print ("Deleted "+str(deleteCounter)+" files")
    # do nothing if deletion not continued with input 'yes'
    else:
        print("Nothing left to do here. Bye!")
