# curationTools
A collection of scripts and tools for curation of data. Used e.g. for ARCHE
A description on what each script does is provided in the sections below.

All tools were mainly developed in an Windows environment. Though interoperability across operating systems has been kept in mind and should be given. If not so, please open an issue.

## How to use
You will need Python (3, but 2 might work as well). Save the script on your local machine. Open it with a text editor (or a dedicated Python editor) and change the variables for folder or file locaction. Which variables should be adapted is stated at the top documentation section of each file. Save your changes and then execute the script from your favourite CLI with `python scriptname.py`.

## chopttl.py
Cuts up a large ttl file into smaller pieces of a maximum amout of lines. Files might get a bit longer if end of an entity was not reached yet.

## deleteSystemFiles.py
A program to delete system files as e.g. thumbs.db or .DS_Store

## extractPLYmetadata.py
A program to extract basic information from PLY files. Currently this information is extracted: number of vertices and number of faces

## generateFolders.py
A program to create folders for grouping files with similar names together. For example create a folder `038_FJB_1904-001` to group the files `038_FJB_1904-001a.tif` and `038_FJB_1904-001b.tif`
The rule(s) to determine similarity of names is specified within a dedicated function and can be adapted to any user's needs.

## renameFiles.py
A program to rename files and folders in a given folder by applying a set of renaming rules. The set of rules can be expanded, either with Python string replace operations or by using regular expressions.

When executed as is Umlauts and ß will be replaced with ae, ss etc. all other special characters are normalised with the normalize function from unicodedata. Thus e.g. é will become e. Currently the mode 'NFKD' is used. What the mode means and what other modes are available is nicely described in this article on [towards data science](https://towardsdatascience.com/difference-between-nfd-nfc-nfkd-and-nfkc-explained-with-python-code-e2631f96ae6c)

Finally all characters that are not alphanumeric or not an underscore (_) or a hyphen (-) are removed.

This set of rules ensures that file names comply with the requirements of the [digital archive ARCHE](https://arche.acdh.oeaw.ac.at/browser/formats-filenames-and-metadata)
