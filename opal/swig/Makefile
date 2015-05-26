all: perl-bindings ruby-bindings python-bindings lua-bindings
all-multi: perl-bindings-multi ruby-bindings-multi python-bindings-multi lua-bindings-multi

perl-bindings:
	swig -Wall -perl -outdir perl -c++ opal.i
	ln -sf ../../src/timer.cc perl
	ln -sf ../../test/tl.{train,dev,test} perl
	mv -f opal_wrap.cxx perl

python-bindings: 
	swig -Wall -python -builtin -outdir python -c++ opal.i
	ln -sf ../../test/tl.{train,dev,test} python
	mv -f opal_wrap.cxx python

ruby-bindings:
	swig -Wall -ruby -c++ -outdir ruby opal.i
	ln -sf ../../src/timer.cc ruby
	ln -sf ../../test/tl.{train,dev,test} ruby
	mv -f opal_wrap.cxx ruby/opal_wrap.cpp

lua-bindings:
	swig -Wall -lua -c++ -outdir lua opal.i
	ln -sf ../../src/timer.cc lua
	ln -sf ../../test/tl.{train,dev,test} lua
	mv -f opal_wrap.cxx lua/opal_wrap.cc

perl-bindings-multi:
	swig -Wall -DUSE_MULTICLASS -perl -outdir perl -c++ opal.i
	ln -sf ../../src/timer.cc perl
	ln -sf ../../test/tl.{train,dev,test} perl
	mv -f opal_wrap.cxx perl

python-bindings-multi: 
	swig -Wall -DUSE_MULTICLASS -python -builtin -outdir python -c++ opal.i
	ln -sf ../../test/tl.{train,dev,test} python
	mv -f opal_wrap.cxx python

ruby-bindings-multi:
	swig -Wall -DUSE_MULTICLASS -ruby -c++ -outdir ruby opal.i
	ln -sf ../../src/timer.cc ruby
	ln -sf ../../test/tl.{train,dev,test} ruby
	mv -f opal_wrap.cxx ruby/opal_wrap.cpp

lua-bindings-multi:
	swig -Wall -DUSE_MULTICLASS -lua -c++ -outdir lua opal.i
	ln -sf ../../src/timer.cc lua
	ln -sf ../../test/tl.{train,dev,test} lua
	mv -f opal_wrap.cxx lua/opal_wrap.cc

clean:
	cd perl	  && perl Makefile.PL && make distclean && cd ..
	cd python && python setup.py clean --all	&& cd ..
	cd ruby	  && ruby extconf.rb  && make distclean && cd ..
	cd lua	  && make clean && cd ..
	rm -rf */opal* */*.cc */src */tl.*
