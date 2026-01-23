#!/usr/bin/php
<?php
/*
 * Extracts ARCHE metadata from the Goobi METS/MODS export provided by the Pfaﬀenberg Archiv
 * (it's a good question if/to what extend it's reusable for other Goobi METS/MODS exports,
 * would probably require a little adjustments e.g. on the valid mods:mods sections detection)
 *
 * Usage: php -f goobi_mets_extract.php mappingFile.csv metaFile.xml output.trig acdhIdUriOfCollection
 *
 * Remarks:
 * - Can be run with a non-existing mapping file - in such a case the mapping file will be created
 *   and initialized with the spotted metadata property paths. So you can just make an initial run
 *   with a missing mapping file, then edit the mapping file and then run the script again so it
 *   applies the mapping.
 * - If a spotted property path is missing in the mapping file, it is added to the mapping file.
 *   Newly spotted Goobi metadata property paths are initliazed with the ARCHE metadata property
 *   mapping equal to the Goobi metadata property path. This is clearly generating an invalid 
 *   output :-) but it allows you to see extracted values in the output file along with the Gooobi
 *   metadata property path which should be helpful for defining the correct mapping in the mapping
 *   file.
 * - If you want a given Goobi metadata property path not to be mapped to any ARCHE metadata
 *   property, set the "arche" column to blank in the mapping file.
 * - The `acdhIdUriOfCollection` parameter is used to generate the acdh:hasNextItem sequence.
 *   The sequence goes as:
 *   ```
 *   <{acdhIdUriOfCollection}> acdh:hasNextItem <{acdhIdUriOfCollection}/{file name of the 1st tif image}>.
 *   <{acdhIdUriOfCollection}/{file name of the 1st tif image}> acdh:hasNextItem <{acdhIdUriOfCollection}/{file name of the 2nd tif image}>.
 *   (...)
 *   ```
 */

use quickRdfIo\Util as RdfUtil;
use quickRdf\Dataset;
use quickRdf\DataFactory as DF;
use quickRdf\RdfNamespace;
use zozlak\RdfConstants as RDF;

include __DIR__ . '/vendor/autoload.php';

if ($argc < 5) {
    echo "usage: php -f $argv[0] mappingFile.csv metaFile.xml output.trig acdhIdUriOfCollection\n";
    exit(1);
}
$mappingFile = $argv[1];
$metaFile = $argv[2];
$outFile = $argv[3];
$uriBase = preg_replace('`/$`', '', $argv[4]);
$acdh = 'https://vocabs.acdh.oeaw.ac.at/schema#';
$next = "$acdh:hasNextItem";

$mapping = read_mapping($mappingFile, $acdh);
$meta = [];

$doc = new DomDocument();
$doc->load($metaFile);
$xpath = new DOMXPath($doc);
$xpath->registerNamespace('goobi', 'http://meta.goobi.org/v1.5.1/');
$xpath->registerNamespace('mets', 'http://www.loc.gov/METS/');
$xpath->registerNamespace('mods', 'http://www.loc.gov/mods/v3');

$dataset = new Dataset();
$graphNode = DF::namedNode($uriBase);
$collNode = DF::namedNode($acdh . "Collection");
$resNode = DF::namedNode($acdh . "Resource");
$bothNode = DF::namedNode(RDF::OWL_THING);

// extracting metadata
foreach ($xpath->query('//mets:dmdSec/mets:mdWrap/mets:xmlData/mods:mods') as $i) {
    $dmsecId = $i->parentElement->parentElement->parentNode->getAttribute('ID');
    $section = $xpath->query('//mets:div[@DMDID="' . $dmsecId . '"]')->item(0);
    $label = (string) $section->getAttribute('LABEL');
    $type = (string) $section->getAttribute('TYPE');
    if ($type !== "manuscript") {
        echo "Skipping metadata for section $dmsecId of type $type with label $label\n";
        continue;
    }
    foreach ($i->childNodes as $j) {
        if (!($j instanceof DOMElement)) {
            continue;
        }
        process_child($j, '');
    }
}

foreach ($meta as $key => $values) {
    $cfg = $mapping[$key];
    if (!in_array($cfg->scope, ['collection', 'resource', 'both'])) {
        throw new Exception("Unknown property scope $cfg->scope");
    }
    if (empty((string) $cfg->arche)) {
        continue;
    }

    $sbj = match($cfg->scope) {
        'both' => $bothNode,
        'collection' => $collNode,
        'resource' => $resNode,
        default => throw new Exception("Unknown property scope $cfg->scope"),
    };

    foreach ($values as $v) {
        $dataset->add(DF::quad($sbj, $cfg->arche, $v, $graphNode));
    }
}


// extracting next item
$fileIdx = [];
foreach ($xpath->query('//mets:fileGrp[@USE="ARCHIV"]/mets:file') as $i) {
    $uri = $i->firstElementChild->getAttributeNS('http://www.w3.org/1999/xlink', 'href');
    $uri = $uriBase . '/' . basename(str_replace('\\', '/', $uri));
    $fileIdx[$i->getAttribute('ID')] = $uri;
}

$toSort = [];
foreach ($xpath->query('//mets:structMap[@TYPE="PHYSICAL"]//mets:div[@ORDER]') as $i) {
    $order = (int) $i->getAttribute('ORDER');
    foreach ($i->childNodes as $j) {
        if ($j instanceof DOMElement) {
            $fileId = $j->getAttribute('FILEID');
            if (isset($fileIdx[$fileId])) {
                $toSort[$fileIdx[$fileId]] = $order;

            }
        }
    }
}
asort($toSort);
$nextProp = DF::namedNode($acdh . 'hasNextItem');
$sbj = $graphNode;
foreach (array_keys($toSort) as $i) {
    $i = DF::namedNode($i);
    $dataset->add(DF::quad($sbj, $nextProp, $i));
    $sbj = $i;
}

$nmsp = new RdfNamespace();
$nmsp->add($acdh, 'acdh');
$nmsp->add($uriBase . '/', 'id');
RdfUtil::serialize($dataset, 'trig', $outFile, $nmsp);
write_mapping($mappingFile, $mapping);

###################################################################################################

function process_child(DOMNode $el, string $propPath): void {
    if ($el instanceof DOMText) {
        $value = trim($el->textContent);
        if (empty($value)) {
            return;
        }
        add_meta_value($propPath, DF::literal($value));
        return;
    }

    if (!($el instanceof DOMElement)) {
        echo "Unprocessable DOM node type " . $el->nodeType . "\n";
        return;
    }
    $propPath = empty($propPath) ? '' : $propPath . '/';
    $propPath .= $el->nodeName;

    $uri = (string) $el->getAttribute('valueURI');
    if (!empty($uri)) {
        add_meta_value($propPath, DF::namedNode($uri));
        return;
    }

    foreach(['type', 'eventType', 'authority'] as $i) {
        $v = $el->getAttribute($i);
        $v = empty($v) ? '' : "@$v";
        $propPath .= $v;
    }
    foreach($el->childNodes as $i) {
        process_child($i, $propPath);
    }
}

function add_meta_value(string $name, rdfInterface\TermInterface $value): void {
    global $mapping, $meta;

    if (!isset($mapping[$name])) {
        $mapping[$name] = (object) [
            'goobi' => $name,
            'arche' => DF::namedNode($name),
            'scope' => 'collection',
        ];
    }
    $meta[$name][] = $value;
}

function read_mapping(string $path, string $acdh): array {
    if (!file_exists($path)) {
        return [];
    }

    $mapping = [];
    $f = fopen($path, 'r');
    $header = fgetcsv($f, null, ';');
    while($l = fgetcsv($f, null, ';')) {
        if (count($l) === count($header)) {
            $l = (object) array_combine($header, $l);
            $l->arche = DF::namedNode(str_replace('acdh:', $acdh, $l->arche));
            $mapping[$l->goobi] = $l;
        }
    }
    fclose($f);
    return $mapping;
}

function write_mapping(string $path, array $mapping): void {
    $f = fopen($path, 'w');
    fputcsv($f, ['goobi', 'arche', 'scope'], ';');
    foreach ($mapping as $i) {
        fputcsv($f, [$i->goobi, $i->arche, $i->scope], ';');
    }
    fclose($f);
}
