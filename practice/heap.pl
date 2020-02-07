#!/usr/bin/perl
# basic heap implementation check
use strict;
use warnings;
use Heap;

use Data::Dumper;
my $heap = new Heap();
$heap->Print();
$heap->insert(3);
$heap->Print();
$heap->insert(4);
$heap->Print();
$heap->insert(2);
$heap->Print();


