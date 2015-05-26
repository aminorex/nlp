#! /usr/bin/env python

import os
import sys
import copy

infiles=[]

langs=[]

inpaths=[]
outpaths=[]

MAX_ERRS = 10

div="\t"

for arg in sys.argv[1:]:
    if arg == '-v':
        verbosity += 1
    elif arg == '-p':
        div='|||'
    elif len(arg) == 2:
        langs.append(arg)
    elif os.access(arg,os.R_OK):
        inpaths.append(arg)
        sys.stderr.write('add input '+arg+"\n")
    else:
        outpaths.append(arg)
        sys.stderr.write('add output '+arg+"\n")

if not inpaths:
    inpaths.append('/dev/stdin')

nfiles = 0
status = 0

for path in inpaths:
    nfiles += 1

    print path

    parts = path.split('.')

    plangs = copy.copy(langs)
    if len(plangs) != 2:
        if len(parts) >= 2:
            clues = parts[-1].split('-')
            if len(clues) == 2 and all(map(lambda x: len(x)==2,clues)):
                plangs = clues
    if len(plangs) != 2 and len(outpaths) == 2:
        clues = map(lambda x: x.split('.')[-1],outpaths)
        if len(clues) == 2 and all(map(lambda x: len(x)==2,clues)):
            plangs = clues
    if len(plangs) != 2:
        sys.stderr.write('Requires two languages specified.'+"\n")
        sys.exit(1)

    inf = open(path,'r')

    if not outpaths:
        base = parts[0]
        if base == '/dev/stdin':
            base = 'split'
        apath = base+'.'+plangs[0]
        bpath = base+'.'+plangs[1]
    elif len(outpaths) == 1:
        apath = outpaths[0]+'.'+plangs[0]
        bpath = outpaths[0]+'.'+plangs[1]
    else:
        apath = outpaths[0]
        bpath = outpaths[1]

    print apath,bpath

    a = open(apath,'a')
    b = open(bpath,'a')

    lno = 0
    nerrs = 0

    for line in inf:
        parts = line.strip().split(div)
        if len(parts) != 2:
            if nerrs < MAX_ERRS:
                print path,'line',lno,'invalid!'
                nerrs += 1
            elif nerrs == MAX_ERRS:
                print '...'
                nerrs += 1
            else:
                nerrs += 1
        a.write(parts[0]+"\n")
        b.write(parts[1]+"\n")

    a.close()
    b.close()
    if nerrs:
        print nerrs,'errors in',lno,'lines of',path
    else:
        status += 1

sys.exit(0 if status == nfiles else 1)

