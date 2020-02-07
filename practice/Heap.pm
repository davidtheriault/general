#!/usr/local/bin/perl
# A Heap implementation.
package Heap;

use strict;
use warnings;

use POSIX;
use Data::Dumper;

sub new {
    my $class = shift || die "no class";
    my $tree = [undef];
    bless({ tree => $tree }, $class);
}

sub Print {
    my $self = shift || die "no self";
    print Dumper($self->{tree});
}


sub heapify {
    my $self = shift || die "no self";
    
}

sub heapbranch {
    my $self = shift || die "no self";
    my $index = shift || $self->lastIndex();
    if($index == 1) {
        return;
    } elsif($index < 1) {
        die "index out of bounds $index";
    } else {
        my $node = $self->{tree}[$index];
        my $parent_index = $self->parentIndex($index);
        my $parent = $self->{tree}[$parent_index];
        # MAX HEAP
        if($parent < $node) {
            $self->swap($index, $parent_index);
            $self->heapbranch($parent_index);
        } else {
            return;
        }
    }
}

sub lastIndex {
    my $self = shift || die "no self";
    return @{$self->{tree}} - 1;
}

sub insert {
    my $self = shift || die "no self";
    my $digits = shift || die "no digits";
    push @{$self->{tree}}, $digits;
    $self->heapbranch();
}

sub parentIndex {
    my $self = shift || die "no self";
    my $index = shift || return; # index 1 is root
    my $parent = floor($index / 2);
    return if($parent < 1);
    return $parent;
}

sub parent {
    my $self = shift || die "no self";
    my $index = shift || return; # index 1 is root
    return $self->{tree}[$self->parentIndex($index)];
}

sub leftChildIndex {
    my $self = shift || die "no self";
    my $index = shift || return; # index 1 is root
    return 2 * $index;
}

sub rightChildIndex {
    my $self = shift || die "no self";
    my $index = shift || return; # index 1 is root
    return  1 + $self->leftChildIndex($index);
}

sub swap {
    my $self = shift || die "no self";
    my $index_old  = shift || die "no index 1";
    my $index_new = shift || die "no index 2";
    my $tmp = $self->{tree}[$index_old];
    $self->{tree}[$index_old] =  $self->{tree}[$index_new];
    $self->{tree}[$index_new]  = $tmp;
    $tmp = undef;
    return;
}

1;
