# -*- coding: utf8 -*-
# Filename: chopttl.py
#
########################################################################
# This is a program to cut up a large ttl file into smaller pieces
#
# Martina Trognitz (martina.trognitz@oeaw.ac.at)
#
# Specify the file with variable fullFile.
# Specify maximum number of lines with maxLine. Files might get a bit
# longer if end of an entity was not reached yet.
# The resulting chopped files can then be found in ttlParts.
#
########################################################################
from __future__ import unicode_literals

from io import open

import sys
import errno
import os, os.path
import unicodedata

def printFilePart (headerPart, ttlLineList, fileName):
    """
    Function to write a ttl file.
    Arguments are the list with the header part, the line list to write,
    and the filename
    """
    outFile = open(fileName,'wb')
    for line in headerPart:
        outFile.write(line.encode('utf-8'))
    for line in ttlLineList:
        #writeLine = line.decode('utf-8')
        writeLine = line
        outFile.write((writeLine).encode('utf-8'))
    outFile.close()

if __name__=="__main__":
    # set file or file path
    fullFile = u'../p4d/puzzle4d_collection.ttl'
    # set maximum number of lines per ttl
    maxLine = 10000
    print ("######################################################")
    print ("Chopping file: "+fullFile+"\n")
    print ("Set maximum line numbers to: "+str(maxLine)+"\n")

    try:
        with open(fullFile, encoding='utf-8') as file:
            ttlfull = file.readlines()
    except IOError:
        print('Could not open or read file: %s. Was the name and path typed in correctly?' % fullFile)
        sys.exit()

    # get file name for output files from input path
    partPath, partFileName = os.path.split(fullFile)
    outFileName = partFileName.split('.')[0]

    headerPart = []
    ttlLineList = []
    lineCounter = 0
    fileCounter = 0
    startNewFile = 0

    # create folder 'ttlParts' for output files
    try:
        os.mkdir('ttlParts')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            print ("Could not create directory 'ttlParts'")
            raise
        pass
        print ("Writing output to 'ttlParts'")
    else:
        print ("Created directory 'ttlParts' for output files")

    # split up file into parts, but only split if an entity was done (. at end)
    for line in ttlfull:
        if '@prefix ' in line:
            headerPart.append(line)
            continue
        lineCounter += 1

        if lineCounter >= maxLine:
            startNewFile = 1
            lineCounter = 0

        ttlLineList.append(line)

        if line.strip().endswith('.') and startNewFile > 0:
            fileCounter += 1
            print ('Creating file number: {num:02d}'.format(num=fileCounter))
            fileName= os.path.join('ttlParts', '{0}_part{num:02d}.ttl'.format(outFileName, num=fileCounter))
            startNewFile = 0
            printFilePart(headerPart, ttlLineList, fileName)
            ttlLineList = []

    # last bit has to be writen into file as well
    fileName= os.path.join('ttlParts', '{0}_part{num:02d}.ttl'.format(outFileName, num=fileCounter+1))
    print ('Creating file number: {num:02d}'.format(num=fileCounter+1))
    printFilePart(headerPart, ttlLineList, fileName)
