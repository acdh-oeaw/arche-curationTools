#!/usr/bin/php
<?php
use \zozlak\argparse\ArgumentParser;
use \zozlak\logging\Log;
use \whikloj\BagItTools\Bag;

include __DIR__ . '/vendor/autoload.php';

$parser = new ArgumentParser();
$parser->addArgument('targetFile');
$parser->addArgument('sourceDirectory');
$parser->addArgument('--skip', help: 'Regex pattern skipping files from the created bagit');
$parser->addArgument('--match', help: 'Regex pattern matching files for the created bagit');
$parser->addArgument('--checksums', default: 'sha512', help: 'Comma-separated list of hashing algorithms, e.g. md5, sha1, sha256 (default %(default)s)');
$parser->addArgument('--tmpDir', default: sys_get_temp_dir());
$args = $parser->parseArgs(array_slice($argv, 1));

$log = new Log('php://stdout');
if (file_exists($args->targetFile)) {
    $log->error("Target file $args->targetFile already exists");
    exit(1);
}
if (!is_dir(dirname($args->targetFile))) {
    $log->error("Target file location (" . dirname($args->targetFile) . ") doesn't exists");
    exit(2);
}
$log->info("Creating $args->targetFile bag with $args->checksums checksums for $args->sourceDirectory");

$tmpDir = $args->tmpDir . '/'. rand();
$stem = preg_replace('/[.][^.]+/', '', basename($args->targetFile));
try {
    $log->info("Using $tmpDir temporary data location");
    $bag = Bag::create("$tmpDir/$stem");
    foreach (explode(',', $args->checksums) as $i) {
        $bag->addAlgorithm($i);
    }
    $srcDir = realpath($args->sourceDirectory) . '/';
    $srcDirLen = strlen($srcDir);
    $iter = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($srcDir));
    foreach($iter as $file) {
        if (!$file->isFile()) {
            continue;
        }
        $pathFrom = $file->getPathName();
        $pathTo = substr($pathFrom, $srcDirLen);
        if (!empty($args->match) && !preg_match('`' . $args->match . '`', $pathTo)) {
            $log->info("Skipping $pathFrom - doesn't match the --match parameter");
            continue;
        }
        if (!empty($args->skip) && preg_match('`' . $args->skip . '`', $pathTo)) {
            $log->info("Skipping $pathFrom - matches the --skip parameter");
            continue;
        }
        $log->info("Adding $pathFrom as $pathTo");
        $bag->addFile($pathFrom, $pathTo);
    }
    $log->info("Creating $args->targetFile");
    $bag->package($args->targetFile);
    $log->info("$args->targetFile created");
} finally {
    if (file_exists($tmpDir)) {
        system("rm -fR '$tmpDir'");
    }
}

