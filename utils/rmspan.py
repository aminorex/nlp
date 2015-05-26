#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys

ch=u'＃'

for line in sys.stdin:
    line = line.strip().decode('utf-8')
    op = 0
    cl = 0
    while op > -1 and cl > -1 and line:
        op = line.find(ch)
        if op < 0:
            break
        cl = line.find(ch,op+1)
        if cl < 0:
            break
        line = line[:op]+line[cl+1:]
    print line.encode('utf-8')
        
