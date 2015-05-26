require 'mkmf'

$libs   = '-lstdc++'
$defs   = ['-DHAVE_CONFIG_H']
$INCFLAGS += ' -I../.. -I../../src'

# add SSE4.2 CXXFLAGS; dirty bit
$CFLAGS += ' -msse4.2' if File.read('../../config.h') =~ /^#define USE_SSE4_2_POPCNT 1$/

create_makefile('pecco')
