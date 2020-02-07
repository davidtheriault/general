#!/usr/bin/env perl
use warnings;
use strict;

# Written by David Theriault
# This script tests a given regex
# to see if it can correctly match
# (and only match) a valid number.
# The purpose is to test someone's regex
# ability.

use constant PASS=>1;
use constant FAIL=>0;
my @reg_pass=(
'1', '99', '0', '00',
'100.32', '.32', '.3', '0.3', '1234.', '0.0',  '0.1234', '010.10');
my @neg_pass = map{'-'.$_} @reg_pass;
my @pass = (@reg_pass, @neg_pass);
my @reg_fail = ('0..3', '0.3.3', 'a0.3', 'a0.b3', 'a0b3', '.', ' ', '', 'a', 'abc');
my @neg_fail = map{'-'.$_} @reg_fail;
push(@neg_fail, ('--2', '-2-2', '.-', '0-')); 
my @fail = (@reg_fail, @neg_fail);


my $regexs = [
#    '^\d*(\d\.|\.\d)?\d*$',
#    '^\d*(\.)?\d+$'
#    Test to match positive and negative floating numbers or positive and negative integers.
    '^\-?\d*(\d|(\.\d)|(\d\.))\d*$',
    '^\-?\d*(\d|(.\d)|(\d.))\d*$',
    ];

print "\n--RegEx Tester--";
match(\@pass, $regexs, PASS);
match(\@fail, $regexs, FAIL);

sub match{
    my $tests       = shift || exit();
    my $regexs      = shift || qw( ^\d*(\d\.|\.\d)?\d*$ );
    my $should_pass = shift;
    $should_pass = PASS unless(defined($should_pass));
    my $fails = 0;
    my $regex  = undef;
    my @match_text = ("\t did NOT match\t ", "\t did match\t ");

    print "\nThese tests should ". ($should_pass ? "PASS (match)":"FAIL (not match)").":\n";
    foreach my $test (@$tests) {
        foreach my $pattern (@$regexs) {
            $regex = qr/$pattern/;
            if($should_pass == ($test =~ m/$regex/)) {
                print "PASS:\t" . $test . $match_text[$should_pass] . $pattern."\n";
            }
            else {
                print "FAILED:\t" . $test . $match_text[!$should_pass] . $pattern."\n";
                $fails++;
            }
        }
    }
    if($fails) {
        print "Failure, $fails tests did not pass\n";
    }
    else {
        print "Success, all tests passed\n";
    }
    return;
}
print "\n";
exit;

