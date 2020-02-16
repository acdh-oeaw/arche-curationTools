# -*- coding: utf8 -*-
# Filename: extractPLYmetadata.py
#
########################################################################
# This is a program to extract basic information from PLY files
# Information extracted: number of vertices and number of faces
#
# Martina Trognitz (martina.trognitz@oeaw.ac.at)
#
# Specify the path with first variable
#
########################################################################
from __future__ import unicode_literals

import os, os.path

if __name__=="__main__":
    # set path
    # ensure that root folder name is unique in collection
    path = r'..\Collections'
    print ("Working with directory: "+path+"\n")

    allMeta = []

    # walk through path and find ply files
    for root, dirs, files in os.walk(path):
        for file in files:
            fileExtension = file.rsplit('.', 1)[1].lower()
            fileNamePath = os.path.join(root, file)
            if fileExtension == 'ply':
                print ("Found this ply: " +fileNamePath)
                # open and read ply
                with open(fileNamePath, 'rb') as plyfile:
                    fileLines = plyfile.readlines()
                fileMeta = []
                # read each line and check for element vertex and element face
                for line in fileLines:
                    if b'element vertex' in line:
                        plyVertices = line.split(b' vertex ')[1].strip()
                        fileMeta.append(fileNamePath.encode('utf-8'))
                        # extra bit, if file names already contain hint to
                        # resolution used. Might be commented out
                        if 'lowRes-data' in fileNamePath:
                            fileMeta.append(b'Low Resolution')
                        else:
                            fileMeta.append(b'Higher Resolution')
                        fileMeta.append(plyVertices)
                    if b'element face' in line:
                        plyFaces = line.split(b' face ')[1].strip()
                        fileMeta.append(plyFaces)
                        allMeta.append(fileMeta)
                        break

    # write file with list of files and number of vertices and faces
    # if extra resolution bit was not commented out this is also added
    outMetaFile = open('plyMetaList.csv','wb')
    for meta in allMeta:
        writeLine = b';'.join(meta).decode('utf-8')
        outMetaFile.write((writeLine+'\n').encode('utf-8'))
    outMetaFile.close()
