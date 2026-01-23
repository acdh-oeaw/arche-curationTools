# arche-curationTools
A collection of scripts and tools for curation of data. Used e.g. for ARCHE
A description on what each script does is provided in the sections below.

All tools were mainly developed in an Windows environment. Though interoperability across operating systems has been kept in mind and should be given. If not so, please open an issue.

## How to use

You will need Python (3, but 2 might work as well). Save the script on your local machine. Open it with a text editor (or a dedicated Python editor) and change the variables for folder or file locaction. Which variables should be adapted is stated at the top documentation section of each file. Save your changes and then execute the script from your favourite CLI with `python scriptname.py`.

## tif_lzw.sh

Assures all TIFF files in a given directory are LZW-compressed.

Usage on the cluster:

* Login to the arche-ingestion environment on the cluster (see [here](https://github.com/acdh-oeaw/arche-ingest/blob/master/docs/acdh-cluster.md)).
* Run `screen -S myCompressionSessionName`
* Run
  ```bash
  bash /ARCHE/curationTools/tif_lzw.sh directoryToProcess 2>&1 | tee pathToLogFile
  ```
  * If you need to process all subdirectories of a given directory, then
    ```bash
    for i in `find directoryToProcess -type d` ; do bash /ARCHE/curationTools/tif_lzw.sh $i 2>&1 | tee -a pathToLogFile ; done
    ```
    e.g.
    ```bash
    for i in `find /ARCHE/staging/GlaserPhotos_20610/data/ -type d` ; do bash /ARCHE/curationTools/tif_lzw.sh $i 2>&1 | tee -a pathToLogFile ; done
    ```

Local usage - if you are a hacker, you will figure it out based on the instructions above. If not, do not run it locally.
(hint - you need gdal and exiftool binaries installed and in your PATH)

## goobi_mets_extract.php

Extracts ARCHE metadata from a Goobi METS/MODS metadata export provided by the Pfaﬀenberg Archiv.

When we have examples of Goobi METS/MODS metadata exports from other sources, we can make it work with them as well.

Usage on the cluster:

* Login to the arche-ingestion environment on the cluster (see [here](https://github.com/acdh-oeaw/arche-ingest/blob/master/docs/acdh-cluster.md)).
* Run `screen -S myCompressionSessionName`
* Run
  ```bash
  /ARCHE/curationTools/goobi_mets_extract.php mappingFile.csv goobiModsMetsMetaFile.xml output.trig acdhIdUriOfExtractedCollection
  ```
  * For the first run the mapping file may not exist - it will be created and filled in with spotted Goobi metadata property paths.
    Of course you should then open the mapping file, adjust the mapping and rerun the script.
  * If you are reusing the mapping file to process multiple Goobi METS/MODS metadata exports (which is probably the way you should do it,
    at least for exports from a single depositor) and any new Goobi metadata property paths are spotted in the just-processed Goobi
    METS/MODS export, then they are added to the mapping file. In such a case you should again edit the mapping file, provide desired
    ARCHE metadata property mappings and rerun the script.
  * If you want a given Goobi METS/MODS metadata property path not to be mapped to any ARCHE metadata property, set the `arche` column
    to an empty value in the mapping file.

## chopttl.py

Cuts up a large ttl file into smaller pieces of a maximum amout of lines. Files might get a bit longer if end of an entity was not reached yet.

## deleteSystemFiles.py

A program to delete system files as e.g. thumbs.db or .DS_Store

(This is also automatically done by the [repo-filechecker](https://github.com/acdh-oeaw/repo-file-checker))

## extractPLYmetadata.py

A program to extract basic information from PLY files. Currently this information is extracted: number of vertices and number of faces

## generateFolders.py

A program to create folders for grouping files with similar names together. For example create a folder `038_FJB_1904-001` to group the files `038_FJB_1904-001a.tif` and `038_FJB_1904-001b.tif`
The rule(s) to determine similarity of names is specified within a dedicated function and can be adapted to any user's needs.

## metadatacrawler

See readme inside of it.

(This script has been deprecated in favor of the [arche-metadata-crawler](https://github.com/acdh-oeaw/arche-metadata-crawler))

## metahead.py

A script sanitizing the metahead.ttl.

Currently it automatically generates missing `acdh:hasTitle` for resources of type `acdh:Person`.

## renameFiles.py

A program to rename files and folders in a given folder by applying a set of renaming rules. The set of rules can be expanded, either with Python string replace operations or by using regular expressions.

When executed as is Umlauts and ß will be replaced with ae, ss etc. all other special characters are normalised with the normalize function from unicodedata. Thus e.g. é will become e. Currently the mode 'NFKD' is used. What the mode means and what other modes are available is nicely described in this article on [towards data science](https://towardsdatascience.com/difference-between-nfd-nfc-nfkd-and-nfkc-explained-with-python-code-e2631f96ae6c)

Finally all characters that are not alphanumeric or not an underscore (_) or a hyphen (-) are removed.

This set of rules ensures that file names comply with the requirements of the [digital archive ARCHE](https://arche.acdh.oeaw.ac.at/browser/formats-filenames-and-metadata)
