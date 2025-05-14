# Deprecation notice

This script has been deprecated in favor of the https://github.com/acdh-oeaw/arche-metadata-crawler.

# metadataCrawler
A script (metadatacrawler.py) to create metadata for a given folder and its contents. It is accompanied by metadataAttributes.py and metahead.ttl

## How to use
You will need Python (3, but 2 might work as well).
Copy the files to your local machine. Then first make adjustments to metahead.ttl. It should contain basic metadata describing anything but Collections or Resources. This means Places, Publications, Organisations, Projects, and Image (usually only one for title image) are described here.

In the next step edit metadataAttributes.py. It contains a set of Python dictionaries into which information for the top level collection, folders (Collections) and files (Resources) can be entered. Several modes are possible and described in the comments:
* Metadata for a specific folder
* Metadata for a specific file
* Metadata for all files contained in a specific folder
* Metadata for a folder with a specific name that is used multiple times in the collection

After setting up metadata metadatacrawler.py needs to be adapted for the folder it should crawl through. Open it and change the variables to indicate folder locaction. Which variables should be adapted is stated at the top documentation section of the file. Save all your changes and execute metadataCrawler from your favourite CLI with `python metadatacrawler.py`.
