#!/usr/bin/env perl
use strict;
use pecco;

my $timer = new pecco::Timer ("pecco", "classify");
unshift (@ARGV, '$0');
my $opt   = new pecco::option ($#ARGV + 1, \@ARGV);
my $c     = new pecco::kernel_model ($opt);
$c->load ($opt->{model});

my ($pp, $pn, $np, $nn) = 0, 0, 0, 0;
open (IN, $opt->{test});
while (<IN>) {
  chomp;
  m/^(\S+) /;
  my ($label, $fstr) = ($1, $'); # '
  $timer->startTimer ();
  my @fv = map { (split (':'))[0]; } split (' ', $fstr);
  my $sign = $c->binClassify (\@fv);
  $timer->stopTimer ();
  if ($label == "+1") {
    if ($sign) { $pp += 1; } else { $pn += 1; }
  } else {
    if ($sign) { $np += 1; } else { $nn += 1; }
  }
}
close (IN);

printf(STDERR "acc. %.4f (pp %d) (pn %d) (np %d) (nn %d)\n",
       ($pp + $nn) * 1.0 / ($pp + $pn + $np + $nn), $pp, $pn, $np, $nn);

$timer->printElapsed ();
