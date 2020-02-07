#!/usr/bin/perl

# written by David Theriault

# replace a repeating character with [numeral]X
# where numeral is the number of times the character 
# repeats, for all characters repeating 4 or more times.

use strict;
use warnings;
use Data::Dumper;

sub remove_dup {
    my $list = shift or die "no list";
    print "list:@{$list}\n";
    my @short;
    my %items;
    foreach my $item (@$list) {
        print "item:$item\n";
        next if exists($items{$item});
        push @short, $item ;
        $items{$item} = 1;
    }
    print "returning @short\n";
    return @short;
}
#my @stuff = (5, 7, 2, 3, 0, 10, 2, 6);
#print "stuff: @stuff\n";
#remove_dup(\@stuff);


#my @result = remove_dup2([5, 7, 2, 3, 0, 10, 2, 6]);
#print "result:@result\n";
sub remove_dup2 {
    my $list = shift or die "no list";
    my %items;
    my @results = map  {  ($items{$_}++) ? '': $_ } @{$list};
    print "items:".Dumper(\%items);
    return @results;
}

sub mode {
    my @list = @_;
    my $most_value = $list[0];
    my $most_count = 1;
    my %counts;
    $counts{$most_value} = 1;
    foreach my $item (@list) {
        $counts{$item}++;
        if($counts{$item} > $most_count) {
            $most_count = $counts{$item};
            $most_value = $item;
        }
    }
    return $most_value;
}

#my $m = mode(1,1,4,1,5,7,9,9,9,9,9,23);
#print "mode:$m\n";
#

sub comp {
    my $uncomp = shift or die "no comp";
    my @chars = split( //,$uncomp);
    my $result = '';
    my $repeat_val=$chars[0];
    my $repeat_count=1;
    
    my $process = sub {
        if($repeat_count >= 4) {
            $result .= $repeat_count."X".$repeat_val;
        } else {
            $result .=  $repeat_val x $repeat_count;
        }
    };
    for(my $index = 1; $index < @chars; $index++) {
        my $char = $chars[$index];
        if($char eq $repeat_val) {
            $repeat_count++;
        } else {
            $process->();
            $repeat_count = 1;
            $repeat_val = $char;
        }
    }
    $process->();
    return $result;

}

my $uncomp = 'aabbggggggbbcaaabbccccccb';
my $comp = comp($uncomp);
print "uncomp:\n$uncomp\ncomp:\n$comp\n";
