# AM_CXXFLAGS = -Wall -Wextra -Wformat=2 -Wcast-qual -Wcast-align -Wwrite-strings -Wconversion -Wpointer-arith -Wshadow -pedantic
AM_CXXFLAGS = -Wall
bin_PROGRAMS = opal @OPAL_MULTI@ @OPALK@ @OPALK_MULTI@ rand_shuf
EXTRA_PROGRAMS = opalk opal-multi opalk-multi

opal_SOURCES = pa.h opal.cc
EXTRA_opal_SOURCES = timer.cc timer.h \
		     cedar.h
opal_multi_SOURCES  = pa.h opal.cc
EXTRA_opal_multi_SOURCES = timer.cc timer.h \
			   cedar.h
opal_multi_CXXFLAGS = -DUSE_MULTICLASS

opalk_SOURCES = pa.h opal.cc
EXTRA_opalk_SOURCES = timer.cc timer.h 
opalk_CXXFLAGS = -DUSE_POLYK
opalk_multi_SOURCES  = pa.h opal.cc
EXTRA_opalk_multi_SOURCES = timer.cc timer.h
opalk_multi_CXXFLAGS = -DUSE_MULTICLASS -DUSE_POLYK

opal_DEPENDENCIES = @OPAL_OBJ@
opal_LDADD = @OPAL_OBJ@
opal_multi_DEPENDENCIES = @OPAL_OBJ@
opal_multi_LDADD = @OPAL_OBJ@

opalk_DEPENDENCIES = @OPAL_OBJ@
opalk_LDADD = @OPAL_OBJ@
opalk_multi_DEPENDENCIES = @OPAL_OBJ@
opalk_multi_LDADD = @OPAL_OBJ@

rand_shuf_SOURCES = rand_shuf.cc
