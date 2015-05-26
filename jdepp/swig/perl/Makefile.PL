use ExtUtils::MakeMaker;
# See lib/ExtUtils/MakeMaker.pm for details of how to influence
# the contents of the Makefile that is written.

# add SSE4.2 CXXFLAGS; dirty bit
open (IN, "../../config.h");
$CCFLAGS = do { local $/ = under; <IN> } =~ /^#define USE_SSE4_2_POPCNT 1$/m ? '-msse4.2' : '';
close (IN);

WriteMakefile
  ('NAME'    => 'jdepp',
   'CC'      => 'g++',
   'LD'      => 'g++',
   'DEFINE'  => '-DHAVE_CONFIG_H',
   'CCFLAGS' => $CCFLAGS,
   'LIBS'    => '-lmecab',
   'INC'     => '-I../.. -I../../src',
   'OBJECT'  => 'jdepp_wrap.o timer.o classify.o kernel.o pdep.o'
);
