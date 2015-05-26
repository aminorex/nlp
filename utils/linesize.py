#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unicodedata as u

lno=0
nout=0
badtabs=0
badsize=0

for x in open(sys.argv[1],'r'):
    lno += 1
    text = x.strip()

    parts = text.split("\t")
    if len(parts) != 2:
        badtabs += 1
        continue

    okay = True
    a = len(parts[0])
    b = len(parts[1])
    if not a or not b:
        if okay:
            badtabs += 1
            okay = False

    if a > b:
        if a > 2*b:
            badsize += 1
            okay = False
    else:
        if b > 2*a:
            badsize += 1
            okay = False
    try:
        ustr = text.decode('utf-8')
    except:
        sys.stderr.write(repr(lno)+"\n")
        sys.stderr.write(text+"\n")
        ty,ob,ms = sys.exc_info()
        sys.excepthook(ty,ob,ms)
        sys.exit(1)
    
    if okay:
        if any(map(lambda x: ord(x) > 255,ustr)):
            print text
            nout += 1

sys.stderr.write(repr(lno)+" "+repr(nout)+" "+repr(badtabs)+" "+repr(badsize)+"\n")

