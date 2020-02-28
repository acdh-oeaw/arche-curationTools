# -*- coding: utf8 -*-
# Filename: metadataAttributes.py
#
########################################################################
# Here lists for metadata attributes for each Class of the
# ACDH metadata schema for ARCHE are stored with default values
#
# for each property a list of values is given
# for different languages use this:
# 'acdh:property1-de': ['...'],
# 'acdh:property1-en': ['...']
#
# This file is for <insert collection name>
#
#
########################################################################

# Metadata for top collection
collectionAttributes = {
'acdh:hasTitle-de': '',
'acdh:hasTitle-en': '',
'acdh:hasAlternativeTitle-de': '',
'acdh:hasPid': ['create me'],
'acdh:hasLanguage': ['https://vocabs.acdh.oeaw.ac.at/iso6393/deu'],
'acdh:hasDescription-de': ['""Longt Text with \n linebreak""'],
'acdh:hasContact': ['acdhi:adittrich'],
'acdh:hasMetadataCreator': ['acdhi:adittrich'],
'acdh:hasPrincipalInvestigator': ['acdhi:adittrich'],
'acdh:hasRelatedDiscipline': ['https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/602002', 'https://vocabs.acdh.oeaw.ac.at/oefosdisciplines/601003'],
'acdh:hasCoverageStartDate': ['1954-09-01'],
'acdh:hasCoverageEndDate': ['2019-12-31'],
'acdh:hasActor': ['acdhi:iaichinger'],
'acdh:hasExtent-de': [''],
'acdh:hasOwner': ['acdhi:someInstitute'],
'acdh:hasRightsHolder': ['acdhi:oeaw'],
'acdh:hasLicensor': ['acdhi:someInstitute'],
'acdh:hasLicense': ['https://creativecommons.org/licenses/by/4.0'],
'acdh:hasLifeCycleStatus': ['https://vocabs.acdh.oeaw.ac.at/archelifecyclestatus/completed'],
'acdh:hasAccessRestriction': ['https://vocabs.acdh.oeaw.ac.at/archeaccessrestrictions/public'],
'acdh:hasCollectedStartDate': ['2016-01-11'],
'acdh:hasCollectedEndDate': ['2019-05-03'],
'acdh:hasDepositor': ['acdhi:adittrich']
}

# Metadata for everything inside the collection
subcollectionsAttributes = {
# Metadata for folders right on top of collection
#'Drawings' for <collID>/Drawings
#
'SYENE': {
'acdh:hasTitle-en': ['Daten zu SYENE'],
# ...
}


# Metadata for deeper nested folders. Note the use of ';' to separate
# the folder from its path:
# 'madraRiverDelta/Drawings;pottery' for MadraRiverDelta/Drawings/pottery
#
#'madraRiverDelta/Drawings;pottery': {
#'acdh:hasTitle-en': ['pottery'],
# ...
#},


# Metadata for individual files, similar pattern as for nested folders
# for files on upper most level: 'MadraRiverDelta;Catalogue_HUe-Su.csv'
#
#'traveldigital/Auxiliary_Files;traveldigital_persNames-termlabels.xml': {
#'acdh:hasTitle-en': ['travel!digital term labels'],
# ...
#},


# Metadata for all files in a folder. '-files' is used to mark them
#
#'ODeeg/Collections/AT-Vienna-PC-files': {
#'acdh:hasPid': ['create me'],
# ...
#}

# Metadata for a folder with a specific name regardless of the containing folders (e.g. if a folder structure with repetitive elements is used)
# Metadata also applies for all files in there
# 'folderName_;Photos' for a folder named 'Photos'
#
'folderName_;Photos': {
#'acdh:hasPid': ['create me'],
# ...
#}
}

### TODO: still supported???
# any basic metadata that should be applied to collections and files not accounted
# for in subcollectionsAttributes
#basicMetadata = {
#'acdh:hasLicensor': 'acdhi:ikant',
#'acdh:hasRightsHolder': 'acdhi:ikant',
#'acdh:hasOwner': 'acdhi:ikant',
#'acdh:hasAcceptedDate': "2017-02-09",
#'acdh:hasAvailableDate': "2018-02-26",
#'acdh:hasSubmissionDate': "2016-09-13"
#}
