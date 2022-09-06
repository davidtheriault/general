#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
#print "doing vimdiff stuff ".Dumper(\@ARGV);
my $old_file = $ARGV[0] || '';
my $new_file = $ARGV[1] || '';
my $valid = 0;
if((not -e $old_file) or $old_file eq '/dev/null'  ) {
    print "Original file does not exist in this repo:$old_file\n";
    if($new_file =~ m/\.html$/) {
        $old_file = $new_file;
        $old_file =~ s/\.html/\.bml/;
        $old_file = $ENV{pbiz} . $old_file;
        print "checking against prod for $old_file rename\n";
        if(-e $old_file) {
            $valid = 1;
        }
    }
} elsif ((not -e $new_file ) or $new_file eq '/dev/null') {
    print "new file $new_file does not exist in this repo, old file:$old_file\n";
} elsif(-e $old_file and -e $new_file) {
    $valid = 1;
}

if($valid) {
    #vimdiff -R "+windo set wrap" "+windo set nu" $*
    my $cmd = "vimdiff -R '+windo set wrap' '+windo set nu' '$old_file' '$new_file'";
    #my $cmd = "vimdiff -o -R '+windo set wrap' '+windo set nu' '$old_file' '$new_file'";
    #print "executing:$cmd\n";
    system($cmd);
    exit 0;
} else {
    exit 1;
}
