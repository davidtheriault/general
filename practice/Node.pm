#!/usr/bin/perl

package Node;

use strict;
use warnings;

use Data::Dumper;


sub new {
    #print "new node, passed:\n";
    #print Dumper(@_);
    my $class = shift || die "no class";
    my $coins = shift || die "no coins";
    my $value = shift // die "no current value";
    my $parent = shift || undef;
    my $tree_stats   = shift || die "no tree stats";
    my $coin   = shift || 0;
    my $children;
    $parent = undef; #@

    my $self = bless({
            coins => $coins,
            value => $value,
            parent => $parent,
            children => $children,
            tree_stats     => $tree_stats,
            coin     => $coin,
        }, $class);

    return $self;
}

sub printResult {
    my $self = shift || die "no self";
    my @used_coins = ($self->{coin});
    my $parent = $self;
    while($parent = $parent->{parent}) {
        push @used_coins, $parent->{coin}
    }
    print "solved with these coins: @used_coins\n";

}

sub build_child {
    my $self = shift || die "no self";
    my $value = $self->{value};
    my $coins = $self->{coins};
    $self->{tree_stats}{children_count}+=1;
    print $self->{tree_stats}{children_count}." building a child $value\n";
    #print "coins:".Dumper($coins);
    if($value <= 0) {
        return 0;
    } else {
        foreach my $coin (@{$coins}) {
            #print "calling new from build child for coin:$coin\n";
            my $next_value = sprintf("%.2f",$value - $coin);
            if($next_value < 0 ) {
                #print "skipping\n";
                next;
            }
            if(exists($self->{tree_stats}{visited}{$next_value})) {
                next;
            } else {
                $self->{tree_stats}{visited}{$next_value} = 1;
            }
            my $node = new Node($coins, $next_value, $self, $self->{tree_stats}, $coin);
            if($next_value == 0) {
                #@$node->printResult();
                return 0;
            } else {
                last unless $node->build_child();
                print "pushing children to node\n";
                push @{$self->{children}}, $node;
            }
        }
        if($self->{children}) {
            $self->{tree_stats}{depth_count}+=1;
        }
            

    }
    return $value;
}



1;

