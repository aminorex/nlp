#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

op=u"≪"
sc=u"｜"
cl=u"≫ "

for line in sys.stdin:
    line = line.strip().decode('utf-8')
    nop = 0
    nsc = 1
    ncl = 2
    while -1 < nop < nsc < ncl < len(line):
        nop = line.find(op)
        if nop < 0:
            break
        ncl = line.find(cl,nop+1)
        if ncl < 0:
            break
        nsc = line.find(sc,nop+1)
        if nsc > ncl or nsc < nop:
            break
        line = line[:nop]+line[nop+1:nsc]+line[ncl+1:]
    print line.encode('utf-8')
        
