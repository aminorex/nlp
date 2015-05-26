CXX=g++
CFLAGS=-msse4.2
LIBS=-lmecab

all: lua-bindings

lua-bindings: jdepp_wrap.o timer.o classify.o kernel.o pdep.o
	$(CXX) -shared -O2 jdepp_wrap.o timer.o classify.o kernel.o pdep.o $(LIBS) -llua -o jdepp.so

luajit-bindings: jdepp_wrap.o timer.o classify.o kernel.o pdep.o
	$(CXX) -shared -O2 jdepp_wrap.o timer.o classify.o kernel.o pdep.o $(LIBS) -lluajit-5.1 -o jdepp.so

.cc.o:
	$(CXX) -DHAVE_CONFIG_H -I../.. -I../../src -fPIC -O2 $(CFLAGS) -c $<

clean:
	rm -f *.o jdepp.so
