# -*- coding: utf8 -*-
# Filename: metadatacrawler_puzzle4d.py
#
########################################################################
# This is a program to create metadata for
# a given folder and its contents
#
# Martina Trognitz (martina.trognitz@oeaw.ac.at)
#
# Variables to adjust
# * path for folder location
# * rename: set it to true if renaming should be done
# * ttlHeader path to file with ttl header
# * metalangtag to set language of metadata
# * collectionName to set name for toplevel collection
#
# TODO: https://redmine.acdh.oeaw.ac.at/issues/16811
# TODO: langTags
# TODO: PID for public resources & for TopCollection
#######################################################################
from __future__ import unicode_literals

from builtins import list, str
from io import open

import os, os.path
import unicodedata
import re

import metadataAttributes

#TODO: make this an individual file
# list of metadata attributes that are object properties (point to stuff in ARCHE)
# and requiere angle brackets around URIs
urlAttrList = ['acdh:isMemberOf', 'acdh:hasLanguage', 'acdh:hasLifeCycleStatus', 'acdh:hasCategory', 'acdh:hasPrincipalInvestigator', 
'acdh:hasContact', 'acdh:hasCreator', 'acdh:hasAuthor', 'acdh:hasEditor', 'acdh:hasContributor', 'acdh:hasDigitisingAgent',
'acdh:hasPublisher', 'acdh:hasFunder', 'acdh:hasMetadataCreator', 'acdh:hasRelatedDiscipline', 'acdh:hasActor', 'acdh:hasSpatialCoverage',
'acdh:hasOwner', 'hasRightsHolder', 'acdh:hasLicensor', 'acdh:hasLicense', 'acdh:hasAccessRestriction', 'acdh:relation',
'acdh:hasRelatedProject', 'acdh:hasRelatedCollection', 'acdh:isTitleImageOf', 'acdh:continues', 'acdh:documents', 'acdh:isDerivedPublicationOf',
'acdh:isMetadataFor', 'acdh:isObjectMetadataFor', 'acdh:isSourceOf', 'acdh:isNewVersionOf', 'acdh:isPartOf', 'acdh:hasOaiSet',
'acdh:hasDepositor', 'acdh:hasCurator', 'acdh:hasHosting']

# list of files that should be ignored, such as system files like 'Thumbs.db' or '.DS_Store'
ignoreFiles = ['Thumbs.db', '.DS_Store']

# list of file formats that should be ignored, for example add 'xlsx'
ignoreFileExtensions = []

# match file formats to file category/ resource type
# TODO: make this an individual file
# this would allow use by other applications as well
resourceType = {
'zip':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/collection>',
'tif':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/image>',
'tiff': 'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/image>',
'jpg':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/image>',
'png':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/image>',
'svg':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/image>',
'dxf':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/image>',
'mtl':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/3dData>',
'xyzi': 'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/3dData>',
'mtl':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/3dData>',
'obj':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/3dData>',
'ply':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/3dData>',
'x3d':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/3dData>',
'pdf':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/text>',
'txt':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/text>',
'html': 'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/text>',
'csv':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'gfs':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'gml':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'tab':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'kml':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'geojson': 'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'kmz':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'osm':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'gpx':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'tfw':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'prj':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'xml':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'tfwx': 'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'points': 'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'qpj':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'asc':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'qgs':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'siard': 'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'cpg':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>', # long term?
'dbf':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>', # long term?
'sbn':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>', # long term?
'sbx':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>', # long term?
'shp':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>', # long term?
'shx':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>', # long term?
'mkv':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/audioVisual>',
#'gif': 'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/audioVisual>', #exception for P4D
'bib':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/dataset>',
'tex':  'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/text>',
'md':   'acdh:hasCategory <https://vocabs.acdh.oeaw.ac.at/archecategory/text>'
}

def findParentName(parentCollection, parentCollectionName):
    """
    Recursive function to find the containing parent collections of a
    collection or resource.
    """
    if os.path.split(parentCollection)[1] == os.path.split(path)[1]:
       # print (os.path.split(parentCollection))
        return parentCollectionName
    else:
        ttlSubCollection = os.path.split(parentCollection)
        subCollectionName = ttlSubCollection[1]
        parentCollection = ttlSubCollection[0]
        parentCollectionName=findParentName(parentCollection, parentCollectionName)+'/'+subCollectionName
        return parentCollectionName

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
#    newValue = newValue.replace(' - ','-')
#    newValue = newValue.replace(' ','_')
    # you can also use regular expressions e. g.:
    # newValue = str(re.sub(r'(\()([\d]\))', r'-\2', newValue))
    # '( one number )' becomes '-number)'

    # all remaining invalid characters are removed
    # \ and / are kept to keep the path
    newValue = str(re.sub('[^a-zA-Z0-9_\-/\\\]', '', newValue))

    return newValue+fileExt

# isoDate is currently not used, but left for convenience
def isoDate(date):
    """
    Function to convert a string in the format dd.mm.yyyy hh:mm:ss
    into a string in the format yyyy-mm-dd
    """
    if len(date) <= 5:
        date = ''
    else:
        date = date.split(' ')[0]
        date = date.split('.')[::-1]
        date = '-'.join(date)
    return date

def extractValue(value, attrVal, attrLang, ttlList):
    """
    Helper for getAttributes. It decides which characters are added to the value.
    For data properties: ""; for object properties: <>; for language tags: ""@<lang>
    """
    if 'acdhi:' in value:
        ttlList.append(' '.join([attrVal, value]))
    elif attrVal in objPropList:
# not needed anymore
#        # for automatic creation of hasPID the value has to be a string
#        if value == 'create':
#            ttlList.append(' "'.join([attrVal, value])+'"')
#        else:
        ttlList.append(' <'.join([attrVal, value])+'>')
    elif len(attrLang) > 0 :
        ttlList.append('"@'.join([' "'.join([attrVal, value]), attrLang]))
    else:
        ttlList.append(' "'.join([attrVal, value])+'"')
    return ttlList

def getAttributes(ttlList, attributeDict):
    """
    Extracts all attribute and value pairs from a given dictionary and
    appends them in correct ttl notation to a given list.
    """
    titleValue = 0
    for attr in attributeDict:
        attrVal, attrPair = (attr, attributeDict[attr])
        if '-' in attrVal:
            attrVal, attrLang = attrVal.split('-')
        else:
            attrLang = ''

        if 'acdh:hasTitle' in attrVal:
            titleValue = 1

        if str(type(attrPair)) == "<class 'str'>":
            value = attrPair
            if (value == 'null') or (value == ''):
                continue
            ttlList = extractValue(value, attrVal, attrLang, ttlList)
        else:
            for value in attrPair:
                #value = value.decode('utf-8')
                if (value == 'null') or (value == ''):
                    continue
                ttlList = extractValue(value, attrVal, attrLang, ttlList)
    return ttlList, titleValue

def writeAttributes(ttlList, ttlFile):
    """
    Writes lines from a list into a given and already open fileself.
    It assumes the lines are already in correct ttl syntax.
    """
    for i, attr in enumerate(ttlList):
        ttlFile.write(('    '+attr).encode('utf-8'))
        if i < len(ttlList)-1:
            ttlFile.write(';\n'.encode())
        else:
            ttlFile.write('.\n\n'.encode())



if __name__=="__main__":
    # set path
    # ensure that root folder name is unique in collection
    path = u'../data'
    # path to tables with more metadata that is not included in
    # metadataAttributes.py
    # for use in individual parts
    # metaPath = u'../metadata'
    # set rename to 'true' if renaming should be done
    rename = 'false'
    print ("######################################################")
    print ("Working with directory: "+path+"\n")
    # set file with ttl header
    ttlHeader = u'metahead.ttl'
    # set language of metadata
    metalangtag = '@de'
    # set name for toplevel collection (can be different from title)
    collectionName = u'rti-nubianpottery'
    idPart = u'https://id.acdh.oeaw.ac.at/'

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

    # create ttl for collection with subcollections (= directories)
    # store header and repetitive elements
    with open(ttlHeader, encoding='utf-8') as file:
        ttlHead = file.read()

    topCollClass = '  a  acdh:TopCollection;'
    collClass = '  a  acdh:Collection;'

    # first create toplevel collection
    ttlTopCollection = []

    ttlTopCollection, titleVal = getAttributes(ttlTopCollection, metadataAttributes.collectionAttributes)

    ttlCollection = open(collectionName.lower()+'_collection.ttl', 'wb')
    ttlCollection.write(ttlHead.encode())
    ttlCollection.write('\n\n###############################################'
                        '\n############    metahead.ttl end    ############\n')
    ttlCollection.write(('\n'+'<'+idPart+collectionName+'>'+topCollClass+'\n').encode())

    writeAttributes(ttlTopCollection, ttlCollection)

    # then create child collections
    # first set some default values for properties
    # TODO: could be done with metadataAttributess.defaultAttributes
    owner = '<https://id.acdh.oeaw.ac.at/adittrich>'
    rightsholder = '<https://id.acdh.oeaw.ac.at/adittrich>'
    licensor = '<https://id.acdh.oeaw.ac.at/adittrich>'
    license = '<https://creativecommons.org/licenses/by/4.0>'
    accessRestriction = '<https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public>'
    metadataCreator = '<https://id.acdh.oeaw.ac.at/adittrich>'
    depositor = '<https://id.acdh.oeaw.ac.at/adittrich>'
    contact = '<https://id.acdh.oeaw.ac.at/adittrich>'
    curator = '<https://id.acdh.oeaw.ac.at/mtrognitz>, <https://id.acdh.oeaw.ac.at/uczeitschner>'

    # gather folder names where all files in it should get same metadata values
    foldernames = []
    for key in metadataAttributes.subcollectionsAttributes:
        if 'folderName_;' in key:
            foldernames.append(key.split('folderName_;')[1])
    print(foldernames)

    for dir in dirList:
        titleVal = 0
        ttlSubCollection = []
        # normalise name of parent collection
        parentCollectionName= normaliseName(collectionName)
        # get name of subcollection and normalise
        parentCollection, collTitle = os.path.split(dir)
        subCollectionName = normaliseName(collTitle.decode('utf-8'))
        parentCollection = normaliseName(parentCollection.decode('utf-8'))
        parentCollectionName= findParentName(parentCollection, parentCollectionName)
        parentCollectionName = normaliseName(parentCollectionName)

        # write into ttl file
        # print ('Parent: '+parentCollectionName)https://redmine.acdh.oeaw.ac.at/projects/arche-curation/wiki/Metadata_Guide
        ttlCollection.write(('<'+idPart+parentCollectionName).encode())
        ttlCollection.write(('/'+subCollectionName+'>'+collClass+'\n').encode())
        ttlCollection.write(('    acdh:isPartOf '+'<'+idPart+parentCollectionName+'>'+';\n').encode())
        if subCollectionName in metadataAttributes.subcollectionsAttributes:
            attrDict = metadataAttributes.subcollectionsAttributes[subCollectionName]
            print('############'+subCollectionName)
            ttlSubCollection, titleVal = getAttributes(ttlSubCollection, attrDict)
        # add specific metadata for subfolders, such as Images/somefolder
        elif parentCollectionName+';'+subCollectionName in metadataAttributes.subcollectionsAttributes:
            attrDict = metadataAttributes.subcollectionsAttributes[parentCollectionName+';'+subCollectionName]
            print('############'+parentCollectionName+';'+subCollectionName)
            ttlSubCollection, titleVal = getAttributes(ttlSubCollection, attrDict)
        # add specific metadata for subfolders with a specific name regardless of their parent
        elif 'folderName_;'+subCollectionName in metadataAttributes.subcollectionsAttributes:
            attrDict = metadataAttributes.subcollectionsAttributes['folderName_;'+subCollectionName]
            print('############  Folder '+subCollectionName)
            ttlSubCollection, titleVal = getAttributes(ttlSubCollection, attrDict)
        # add metadata for subfolders of a specific folder, regardless of parent, such as 'Photos'
        # folder names are gathered from metadataAttributes, they start with folderName_;
        ## similar to routine for files; not implemented here
        ## above works for some/path/specificfolder
        ## above does not work for some/path/specificfolder/anotherfolder

        # if no title is given in metadataAttributes use the name
        if titleVal == 0:
            collTitle = collTitle.decode('utf-8')
            ttlSubCollection.append('acdh:hasTitle "'+collTitle+'"'+metalangtag)
        # check for mandatory properties
        ownertrue = 0
        rightsholdertrue = 0
        licensortrue = 0
        licensetrue = 0
        contacttrue = 0
        metadatacreatortrue = 0
        depositortrue = 0
        curatortrue = 0
        for el in ttlSubCollection:
            if 'acdh:hasOwner' in el:
                ownertrue = 1
            if 'acdh:hasRightsHolder' in el:
                rightsholdertrue = 1
            if 'acdh:hasLicensor' in el:
                licensortrue = 1
            if 'acdh:hasLicense' in el:
                licensetrue = 1
            if 'acdh:hasContact' in el:
                contacttrue = 1
            if 'acdh:hasMetadataCreator' in el:
                metadatacreatortrue = 1
            if 'acdh:hasDepositor' in el:
                depositortrue = 1
            if 'acdh:hasCurator' in el:
                curatortrue = 1

        if ownertrue == 0:
            ttlSubCollection.append('acdh:hasOwner '+owner)
        if rightsholdertrue == 0:
            ttlSubCollection.append('acdh:hasRightsHolder '+rightsholder)
        if licensortrue == 0:
            ttlSubCollection.append('acdh:hasLicensor '+licensor)
        if licensetrue == 0:
            ttlSubCollection.append('acdh:hasLicense '+license)
        if contacttrue == 0:
            ttlSubCollection.append('acdh:hasContact '+contact)
        if metadatacreatortrue == 0:
            ttlSubCollection.append('acdh:hasMetadataCreator '+metadataCreator)
        if depositortrue == 0:
            ttlSubCollection.append('acdh:hasDepositor '+depositor)
        if curatortrue == 0:
            ttlSubCollection.append('acdh:hasCurator '+curator)

        # print (ttlSubCollection)
        writeAttributes(ttlSubCollection, ttlCollection)

    #######
    # individual part

    #
    #
    #### - end

    # now create ttl entries for the binaries
    # renaming is also done when parameter is set so
    resClass = '  a  acdh:Resource;'
    fileCounter = 0
    for file in fileDirList:
        titleVal = 0
        ttlFiles = []
        oldPath, origFileName = os.path.split(file)

        fileCounter+=1

        # ignore system files according to list
        if origFileName.decode('utf-8') in ignoreFiles:
            print('ignoring: '+os.path.join(oldPath.decode('utf-8'),origFileName.decode('utf-8')))
            continue

        # ignore files with ending according to list
        if origFileName.decode('utf-8').rsplit('.', 1)[1].lower() in ignoreFileExtensions:
            print('ignoring: '+os.path.join(oldPath.decode('utf-8'),origFileName.decode('utf-8')))
            continue

        newFile = normaliseName(origFileName.decode('utf-8'))
        newFilePath = os.path.join(oldPath.decode('utf-8'), newFile)

        # rename file, when this was set at beginning
        if rename == 'true':
            os.rename(file, newFilePath)

        parentCollectionName= normaliseName(collectionName)
        parentCollection, fileTitle = os.path.split(file)
        filename = normaliseName(fileTitle.decode('utf-8'))
        parentCollection = normaliseName(parentCollection.decode('utf-8'))

        parentCollectionName=findParentName(parentCollection, parentCollectionName)
        parentCollectionName = normaliseName(parentCollectionName)

        # set category according to listed formats in resourceType
        category = ''
        fileExtension = origFileName.decode('utf-8').rsplit('.', 1)[1].lower()
        if fileExtension in resourceType:
            category = resourceType[fileExtension]
        else:
            #TODO add this to a log
            print("No resourceType for: "+origFileName.decode('utf-8'))

        #######
        # individual part
        #
        ####### - end

        # collect attributes and values into a list
        ttlFiles.append('acdh:isPartOf '+'<'+idPart+parentCollectionName+'>')

        # add metadata for specific files, such as Images/somefolder/img01.tiff
        if parentCollectionName+';'+filename in metadataAttributes.subcollectionsAttributes:
            attrDict = metadataAttributes.subcollectionsAttributes[parentCollectionName+';'+filename]
            #print('######## File: '+parentCollectionName+';'+filename)
            ttlFiles, titleVal = getAttributes(ttlFiles, attrDict)
            if 'acdh:hasCategory' not in ttlFiles and category != '':
                ttlFiles.append(category)

        # add metadata for all files of specific parent, such as Images/somefolder/*
        elif parentCollectionName+'-files' in metadataAttributes.subcollectionsAttributes:
            attrDict = metadataAttributes.subcollectionsAttributes[parentCollectionName+'-files']
            #print('######## Files in directory: '+parentCollectionName+'-files')
            ttlFiles, titleVal = getAttributes(ttlFiles, attrDict)
            if 'acdh:hasCategory' not in ttlFiles and category != '':
                ttlFiles.append(category)
        # add metadata for all files part of a specific folder, regardless of parent, such as 'Photos'
        # folder names are gathered from metadataAttributes, they start with folderName_;
        elif any(foldername in parentCollectionName for foldername in foldernames):
            for foldername in foldernames:
                if foldername in parentCollectionName:
                    attrDict = metadataAttributes.subcollectionsAttributes['folderName_;'+foldername]
                    #print('######## Files in directory: '+'folderName_;'+'Photos')
                    ttlFiles, titleVal = getAttributes(ttlFiles, attrDict)
            if 'acdh:hasCategory' not in ttlFiles and category != '':
                ttlFiles.append(category)

        if titleVal == 0:
            fileTitle = fileTitle.decode('utf-8')
            ttlFiles.append('acdh:hasTitle "'+fileTitle+'"'+metalangtag)
        #ttlCollection.write(('    acdh:hasTitle "'+fileTitle+'";\n').encode('utf-8'))


        ## now check for the default values
        if not any('acdh:hasCategory' in attvalpair for attvalpair in ttlFiles) and category != '':
            #already comes with attribute name
            ttlFiles.append(category)
        #if 'acdh:Owner' not in ttlFiles and owner != '':
        if not any('acdh:hasOwner' in attvalpair for attvalpair in ttlFiles) and owner != '':
            ttlFiles.append('acdh:hasOwner '+owner)
        if not any('acdh:hasRightsHolder' in attvalpair for attvalpair in ttlFiles) and rightsholder != '':
            ttlFiles.append('acdh:hasRightsHolder '+rightsholder)
        if not any('acdh:hasLicensor' in attvalpair for attvalpair in ttlFiles) and licensor != '':
            ttlFiles.append('acdh:hasLicensor '+licensor)
        if not any('acdh:hasLicense' in attvalpair for attvalpair in ttlFiles) and license != '':
            ttlFiles.append('acdh:hasLicense '+license)
        if not any('acdh:hasAccessRestriction' in attvalpair for attvalpair in ttlFiles) and accessRestriction !='':
            ttlFiles.append('acdh:hasAccessRestriction '+accessRestriction)
        if not any('acdh:hasMetadataCreator' in attvalpair for attvalpair in ttlFiles) and metadataCreator !='':
            ttlFiles.append('acdh:hasMetadataCreator '+metadataCreator)
        if not any('acdh:hasDepositor' in attvalpair for attvalpair in ttlFiles) and depositor !='':
            ttlFiles.append('acdh:hasDepositor '+depositor)
        if not any('acdh:hasCurator' in attvalpair for attvalpair in ttlFiles) and curator !='':
            ttlFiles.append('acdh:hasCurator '+curator)


        # write first line into ttl
        ttlCollection.write(('\n<'+idPart+parentCollectionName+'/'+filename+'>'+resClass+'\n').encode())

        # write attritubes into ttl
        writeAttributes(ttlFiles, ttlCollection)

    ttlCollection.close()

    # rename directories, starting from within
    # only done when this was set to true at beginning
    if rename == 'true':
        dirListReverse = dirList
        for dir in dirList[::-1]:
            oldPath, newDir = os.path.split(dir)
            newDir = normaliseName(newDir.decode('utf-8'))
            newDirPath = os.path.join(oldPath.decode('utf-8'), newDir)
            os.rename(dir, newDirPath)
