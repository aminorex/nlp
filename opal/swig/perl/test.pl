#!/usr/bin/env perl
use strict;
use opal;

unshift (@ARGV, '\$0');
my $opt   = new opal::option ($#ARGV + 1, \@ARGV);

my $timer = new opal::Timer ("train");
my $m = new opal::Model ($opt);

$timer->startTimer ();
$m->train_from_file ($opt->{train}, $opt->{iter}, $opt->{output} == 1 ? $opt->{test} : "");
$m->save ($opt->{model});
$timer->stopTimer ();

$timer->printElapsed ();

$timer = new opal::Timer ("test");
$m = new opal::Model ($opt);
$m->load ($opt->{model});

$timer->startTimer ();
# $m->test_on_file ($opt->{test}, $opt->{output});
my ($corr, $incorr) = 0, 0;
open (IN, $opt->{test});
while (<IN>) {
    chomp;
    m/^(\S+) /;
    my ($y, $xs) = ($1, $'); # '
    my @x = map { (split(':'))[0] } split (' ', $xs);
    my $y_ = $m->binClassify (\@x) ? '+1' : '-1';
#    my $y_ = $m->getLabel (\@x); # for multiclass
    if ($y eq $y_) { $corr++; } else { $incorr++; }
}
close (IN);
printf ("acc. %.4f\n", $corr / ($corr + $incorr));

$timer->stopTimer ();

$timer->printElapsed ();
