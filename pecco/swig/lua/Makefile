CXX=g++
CFLAGS+=-msse4.2

all: lua-bindings

lua-bindings: pecco_wrap.o timer.o classify.o kernel.o linear.o
	$(CXX) -shared -O2 -llua pecco_wrap.o timer.o classify.o kernel.o linear.o -o pecco.so

luajit-bindings: pecco_wrap.o timer.o classify.o kernel.o linear.o
	$(CXX) -shared -O2 -lluajit-5.1 pecco_wrap.o timer.o classify.o kernel.o linear.o -o pecco.so

.cc.o:
	$(CXX) -DHAVE_CONFIG_H -I../.. -I../../src -fPIC -O2 $(CFLAGS) -c $<

clean:
	rm -f *.o pecco.so
