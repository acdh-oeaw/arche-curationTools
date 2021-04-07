# staticFiles
A collection of static files to be re-used in e.g. the ARCHE about pages, the metadataCrawler or other ARCHE libraries.

## Formats
A curated and growing list of file extensions. For each file extension mappings to the respective [ARCHE Resource Type Category]( 	https://vocabs.acdh.oeaw.ac.at/archecategory/Schema) (stored in `acdh:hasCategory`) and [Media Type (MIME type)](https://www.iana.org/assignments/media-types/media-types.xhtml) (stored in `acdh:hasFormat`) are given. The indicated Media Type should only be used as a fallback; it is best practice to rely on automated Media Type detection based on file signatures.

Further information is provided as well.

* name: Name(s) the format is known
* archeCategory": "https://vocabs.acdh.oeaw.ac.at/archecategory/dataset",
* pronomID: ID(s) assigned by [PRONOM](http://www.nationalarchives.gov.uk/PRONOM/Default.aspx)
* mimeType: Official Media Type(s) (formerly known as MIME types) registered at [IANA](https://www.iana.org/assignments/media-types/media-types.xhtml).
* informalMimeType: Other MIME types kown for the format
* magicNumber: A constant numerical or text value used to identify a file format, e.g. [Wikipedia list of file signatures](https://en.wikipedia.org/wiki/List_of_file_signatures)
* ianaTemplate: Link to template at IANA
* references: Link(s) to format specifications referenced by IANA and others
* longTerm: Indicates if a format is suitable for long-term preservation.
 * Possible values and their meaning
   * yes - long-term format
   * no - not suitable, another format should be used
   * restricted - can be used for long-term preservation in some cases (see comment)
   * unsure - status remains to be evaluated
* archeDocs: Link to a place with more information for the format.
* comment: Any other noteworthy information not stated elsewhere.


TODO: Include information on general data type and on preferred/accepted (for ARCHE about page)
