#! /usr/bin/env python
import sys

enl='\xe2\x80\xa8'
if len(sys.argv) > 1:
    for x in sys.argv[1:]:
        u=x.decode('utf-8')
        for uch in u:
            print uch.encode('utf-8'),ord(uch),hex(ord(uch))
    sys.exit(0)
ordval = ord(enl.decode('utf-8'))
print enl,ordval,hex(ordval)
sys.exit(0)
