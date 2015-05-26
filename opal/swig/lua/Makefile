CXX=g++
CFLAGS=-msse4.2

all: lua-bindings

lua-bindings: opal_wrap.o timer.o
	$(CXX) -shared -O2 opal_wrap.o timer.o -llua -o opal.so

luajit-bindings: opal_wrap.o timer.o
	$(CXX) -shared -O2 opal_wrap.o timer.o -lluajit-5.1 -o opal.so

.cc.o:
	$(CXX) -DHAVE_CONFIG_H -I../.. -I../../src -fPIC -O2 $(CFLAGS) -c $<

clean:
	rm -f *.o opal.so
