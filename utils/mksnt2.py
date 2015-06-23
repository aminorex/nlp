#! /usr/bin/env python
#
# combine two monolingual .snt files (arguments) into a bilingual .snt file on stdout
#
import sys
from codecs import open

for s,t in zip(*map(lambda x: open(x,'r',encoding='utf-8'),sys.argv[1:3])):
    print 1
    print s.strip()
    print t.strip()
