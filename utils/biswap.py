#! /usr/bin/env python

import os
import sys

MAXERRS = 10

def biswap(inf,outf,nth,tag):
    lno = 0
    errs = 0

    for line in inf:
        lno += 1
        parallels = line.strip().split("\t")
        if not parallels:
            continue
        if len(parallels) != 2:
            if errs >= MAXERRS:
                sys.stderr.write("...\n")
            else:
                sys.stderr.write('wrong column count in file '+repr(nth)+', '+tag+' line '+repr(lno)+"\n")
                errs += 1
            continue
        outf.write(parallels[1]+"\t")
        outf.write(parallels[0]+"\n")

    return -lno if errs else lno
    

verbosity=0
errs = 0
infiles=[]
outpath = None

for arg in sys.argv[1:]:
    if arg == '-v':
        verbosity += 1
    elif arg == '-o':
        outpath = True
    if os.access(arg,os.R_OK):
        if outpath == True:
            outpath = arg
        else:
            infiles.append(arg)
    else:
        sys.stderr.write('Unknown object: '+arg+"\n")
        errs += 1

if errs:
    sys.exit(1)

if not infiles:
    infiles.append('/dev/stdin')

if not outpath:
    outpath = '/dev/stdout';

nfiles = 0
for path in infiles:
    inf = open(path,'r')
    nfiles += 1
    biswap(fobj,open(outpath,'w'),nfiles,path)

    
