#!/usr/bin/env python
# -*- coding: utf-8 -*-
# convert universal dependency corpus in CoNLL format
#  to Kyoto-University Text Corpus format
# right-to-left dependency (mainly, comma) is attached to previous chunk
import sys, jctconv

offset  = 0
reduced = []
surface = []
feature = []
deptype = []
head    = []
for line in sys.stdin:
    if line[:-1]:
        f = line[:-1].split("\t")
        reduced.append (offset)
        if f[7] != 'ROOT' and int (f[0]) > int (f[6]):
            surface[-1] += f[1]
            feature[-1][0] += "=" + f[3]
            feature[-1][1] += "=" + f[4]
            deptype[-1] += f[7]
            offset += 1
        else:
            surface.append (f[1])
            feature.append ([f[3], f[4]])
            deptype.append (f[7])
            head.append    (int (f[6]) - 1)
    else:
        for i in range (0, len (surface)):
            h = head[i] - reduced[head[i]]
            sys.stdout.write ("* %d %dD %s\n" % (i, h, deptype[h]))
            sys.stdout.write ("%s * * %s\n" % (jctconv.h2z (surface[i].decode ('utf-8'), 'ALL').encode ('utf-8'), ' '.join (feature[i])))
        sys.stdout.write ("EOS\n")
        offset = 0
        reduced = []
        surface = []
        feature = []
        deptype = []
        head    = []
