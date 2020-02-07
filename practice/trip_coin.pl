#!/usr/bin/perl


# Use a tree to find what combination
# of coins yields the desired sum
# written by David Theriault

use strict;
use warnings;
use Node;
use Tree;

use Data::Dumper;

my $first = shift || .17;
my $second = shift || .07;
my $third = shift || .05;
my $fourth = shift || .01;
my $target = shift || .21;

my @coins = [$first, $second, $third, $fourth];
#print "head:". Dumper($head);
my $tree = new Tree();
$tree->build(@coins, $target);
print "total nodes".$tree->{tree_stats}{children_count}."\n";
print "total depth".$tree->{tree_stats}{depth_count}."\n";
$tree->print();
#print "tree:\n";
#print Dumper($tree);

