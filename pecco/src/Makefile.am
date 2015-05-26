# AM_CXXFLAGS = -Wall -Wextra -Wformat=2 -Wcast-qual -Wcast-align -Wwrite-strings -Wconversion -Wpointer-arith -Wshadow -pedantic
AM_CXXFLAGS = -Wall
bin_PROGRAMS = pecco

pecco_SOURCES = typedef.h \
		classify.cc classify.h \
		pecco.cc pecco.h
EXTRA_pecco_SOURCES = timer.cc timer.h \
		      kernel.cc kernel.h \
		      linear.cc linear.h \
		      cedar.h

pecco_DEPENDENCIES = @PECCO_OBJ@
pecco_LDADD = @PECCO_OBJ@
