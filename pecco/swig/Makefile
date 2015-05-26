all: perl-bindings ruby-bindings python-bindings lua-bindings

perl-bindings:
	swig -Wall -perl -outdir perl -c++ pecco.i
	ln -sf ../../src/{timer,classify,kernel,linear}.cc .
	mv {timer,classify,kernel,linear}.cc perl
	mv -f pecco_wrap.cxx perl

python-bindings: 
	swig -Wall -python -builtin -outdir python -c++ pecco.i
	mv -f pecco_wrap.cxx python

ruby-bindings:
	swig -Wall -ruby -outdir ruby -c++ pecco.i
	ln -sf ../../src/{timer,classify,kernel,linear}.cc .
	mv {timer,classify,kernel,linear}.cc ruby
	mv -f pecco_wrap.cxx ruby/pecco_wrap.cpp

lua-bindings:
	swig -Wall -lua -outdir lua -c++ pecco.i
	ln -sf ../../src/{timer,classify,kernel,linear}.cc .
	mv {timer,classify,kernel,linear}.cc lua
	mv -f pecco_wrap.cxx lua/pecco_wrap.cc

clean:
	cd perl	  && perl Makefile.PL && make distclean && cd ..
	cd python && python setup.py clean --all	&& cd ..
	cd ruby	  && ruby extconf.rb  && make distclean && cd ..
	cd lua	  && make clean && cd ..
	rm -rf */pecco* */*.cc */src
