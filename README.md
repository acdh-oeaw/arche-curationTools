# arche-curationTools

A collection of scripts and tools for curation of data in the ARCHE repository.

## How to use

Log into the arche-ingestion environment and folow instructions below.

### How to log into the arche-ingestion environment

First time:

* Login into https://rancher.acdh-dev.oeaw.ac.at
* Open https://rancher.acdh-dev.oeaw.ac.at/dashboard/c/_/manager/provisioning.cattle.io.cluster
* Click three vertical dots button on the right side of the *acdh-ch-cluster-2* table row
  and choose *Download KubeConfig* from the list.
* Install kubectl - https://kubernetes.io/docs/tasks/tools/.
* Download the ssh.sh script from this repository - [link](https://raw.githubusercontent.com/acdh-oeaw/arche-curationTools/refs/heads/master/ssh.sh).
* [Windows only] Install git - https://git-scm.com/install/.
* Move the downloaded `acdh-ch-cluster-2.yaml` and `ssh.sh` (on Windows also the kubectl.exe) files into your home directory,
  e.g. on Windows open the git-bash (click on the start menu, type *git-bash*, hit enter):
  ```bash
  mv Downloads/kubectl* Downloads/acdh-ch-cluster-2.yaml Downloads/ssh.sh .
  ```

Everyday:

* Open console (on Windows *git-bash*) and run:
  ```bash
  ./ssh.sh arche-ingestion
  ```
* If you see error messages indicating authorization failure, then most probably you need to refresh your cdh-ch-cluster-2.yaml file:
  * Login into https://rancher.acdh-dev.oeaw.ac.at.
  * Open https://rancher.acdh-dev.oeaw.ac.at/dashboard/c/_/manager/provisioning.cattle.io.cluster.
  * Click three vertical dots button on the right side of the *acdh-ch-cluster-2* table row.
    and choose *Download KubeConfig* from the list.
  * Move the downloaded `acdh-ch-cluster-2.yaml` and `ssh.sh` (on Windows also the kubectl.exe) files into your home directory,
    e.g. on Windows open the git-bash (click on the start menu, type *git-bash*, hit enter):
    ```bash
    mv Downloads/acdh-ch-cluster-2.yaml . 
    ```

## Provided scripts

Detailed description of scripts is provided below.

* `ssh.sh` - connects to the arche-ingestion cluster environment where all othere scripts can be run
* `tif_lzw.sh` - assures TIF images are LZW-compressed
* `goobi_mets_extract.php` - extracts metadata from a Goobi METS/MODS metadata export provided by the Pfaﬀenberg Archiv
* scripts without CLI interface (you might need to adjust their code to make them do what you want):
  * `chopttl.py` - splits a large ttl file into smaller chunks of a maximum amout of lines
  * `extractPLYmetadata.py` - extracts basic information from PLY files
  * `generateFolders.py` - creates folders for grouping files with similar names together
  * `renameFiles.py` - renames files so that they follow ARCHE file naming requirements
* other
  `openrefine/*` - some openrefine recipes - ask Martina

Deprecated scripts/data:

* `metadataCrawler` - deprecated in favor of the https://github.com/acdh-oeaw/arche-metadata-crawler
* `metahead.py` - deprecated in favor of the https://github.com/acdh-oeaw/arche-metadata-crawler
* `deleteSystemFiles.py` - deprecated in favor of the https://github.com/acdh-oeaw/repo-file-checker/
* `staticFiles/formats.json` - now lives in the [in the arche-assets repository](https://github.com/acdh-oeaw/arche-assets/blob/master/AcdhArcheAssets/formats.json)

### tif_lzw.sh

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

### goobi_mets_extract.php

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

### chopttl.py

Cuts up a large ttl file into smaller pieces of a maximum amout of lines. Files might get a bit longer if end of an entity was not reached yet.

### extractPLYmetadata.py

A program to extract basic information from PLY files. Currently this information is extracted: number of vertices and number of faces

### generateFolders.py

A program to create folders for grouping files with similar names together. For example create a folder `038_FJB_1904-001` to group the files `038_FJB_1904-001a.tif` and `038_FJB_1904-001b.tif`
The rule(s) to determine similarity of names is specified within a dedicated function and can be adapted to any user's needs.

### renameFiles.py

A program to rename files and folders in a given folder by applying a set of renaming rules. The set of rules can be expanded, either with Python string replace operations or by using regular expressions.

When executed as is Umlauts and ß will be replaced with ae, ss etc. all other special characters are normalised with the normalize function from unicodedata. Thus e.g. é will become e. Currently the mode 'NFKD' is used. What the mode means and what other modes are available is nicely described in this article on [towards data science](https://towardsdatascience.com/difference-between-nfd-nfc-nfkd-and-nfkc-explained-with-python-code-e2631f96ae6c)

Finally all characters that are not alphanumeric or not an underscore (_) or a hyphen (-) are removed.

This set of rules ensures that file names comply with the requirements of the [digital archive ARCHE](https://arche.acdh.oeaw.ac.at/browser/formats-filenames-and-metadata)
