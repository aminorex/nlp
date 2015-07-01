#!/usr/bin/perl

use strict;
use warnings;
use utf8;
use List::Util qw(sum min max shuffle);
use Getopt::Long;
binmode STDIN, ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";

my $NOHYPHEN = 0;
my $NOSPACE = 0;
my $REMTAB = 0;
my $REVERSE = 0;
my $AGGRESSIVEHYPHEN = 0;

GetOptions(
    "aggressive" => \$AGGRESSIVEHYPHEN,
    "nohyphen" => \$NOHYPHEN,
    "nospace" => \$NOSPACE,
    "remtab" => \$REMTAB,
    "reverse" => \$REVERSE,
);

if(@ARGV != 0) {
    print STDERR "Usage: han2zen.pl < INPUT > OUTPUT\n";
    exit 1;
}

if ($REVERSE) {
  while(<STDIN>) {
    tr/ａ-ｚＡ-Ｚ０-９（）［］｛｝＜＞．，＿％「」、”？・＋：。！＆＊/a-zA-Z0-9()[]{}<>.,_%｢｣､"?･+:｡!&*/;
    s/－/-/g if not $NOHYPHEN;
    s/ - /-/g if $AGGRESSIVEHYPHEN;
    s/　/ /g if not $NOSPACE;
    s/\t/ /g if $REMTAB;
    s/／/\//g;
    s/ \/ /\//g if $AGGRESSIVEHYPHEN;
    print $_;
  }
} else {
  while(<STDIN>) {
    tr/a-zA-Z0-9()[]{}<>.,_%｢｣､"?･+:｡!&*/ａ-ｚＡ-Ｚ０-９（）［］｛｝＜＞．，＿％「」、”？・＋：。！＆＊/;
    s/\([^ ]\)-\([^ ]\)/$1 - $2/g if $AGGRESSIVEHYPHEN;
    s/-/－/g if not $NOHYPHEN;
    s/\t/ /g if $REMTAB;
    s/ /　/g if not $NOSPACE;
    s/\([^ ]\)\/\([^ ]\)/$1 \/ $2/g if $AGGRESSIVEHYPHEN;
    s/\//／/g;
    print $_;
  }
}

