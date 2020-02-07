#!/usr/bin/perl
use strict;
use warnings;

use Data::Dumper;

package TreeStats;

sub new {
    my $class = shift || die "no class";
    my $children_count = 0;
    my $depth_count    = 0;
    my $visited = {};
    my $self = bless({
            children_count => $children_count,
            depth_count => $depth_count,
            visited     => $visited,
        }, $class);
    return $self;
}


package Tree;
use strict;
use warnings;

use Data::Dumper;


sub new {
    my $class = shift || die "no class";
    my $head_node = undef;
    my $tree_stats = new TreeStats();
    my $self = bless({
            tree => $head_node,
            tree_stats => $tree_stats,
        }, $class);
    return $self;
}

sub build {
    my $self = shift || die "no class";
    my $coins = shift || die "no coins";
    my @coins = reverse sort @{$coins};
    my $target = shift || die "no target";
    $self->{treetop} = new Node(\@coins, $target, undef, $self->{tree_stats});
    $self->{treetop}->build_child();
}

sub print {
    my $self = shift || die "no self";
    my $tree = $self->{treetop};
    #print "tree:".Dumper($tree);
    my $depth = 1;
    my $children = $tree->{children};
    my $next_row;
    sanity_check: {
        do {
            print "\ndepth $depth\n";
            foreach my $child (@$children) {
                #print "child:".Dumper($child);
                print "coin:".$child->{coin}."\t";
                push @$next_row, @{$child->{children}} if($child->{children});
            }
            $depth++;
            $children = $next_row;
            $next_row = undef;
            last if($depth > 25); # temp sanity check
        } while($children);
    }
    

}

1;
