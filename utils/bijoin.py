#! /usr/bin/env python

import os
import sys

args = sys.argv[1:]

if args[0] == '-p':
    args.pop(0)
    div='|||'
else:
    div="\t"

if len(args) < 2:
    print "2 input and 1 output path required"
    sys.exit(1)

outpath = args[2] if len(args) > 2 else '/dev/stdout'

try:
    a = open(args[0],'r')
    b = open(args[1],'r')
    c = open(outpath,'w')
except:
    ty,ob,ms = sys.exc_info()
    sys.excepthook(ty,ob,ms)
    sys.exit(1)

empty = 0
lno = 0
nout = 0
abad = 0
bbad = 0

try:
    while True:
        ain = a.readline().strip()
        bin = b.readline().strip()
        if not ain and not bin:
            break
        lno += 1
        if not ain and not bin:
            empty += 1
            continue
        if not ain:
            sys.stderr.write("Mismatched input A line "+repr(lno)+"\n")
            abad += 1
            continue
        if not bin:
            sys.stderr.write("Mismatched input B line "+repr(lno)+"\n")
            bbad += 1
            continue
        c.write(ain+div+bin+"\n")
        nout+=1
except:
    sys.stderr.write("Exception writing "+outpath+' at input line '+repr(lno)+"\n")
    ty,ob,ms = sys.exc_info()
    sys.excepthook(ty,ob,ms)
    sys.exit(1)

sys.stderr.write('output '+repr(nout)+' lines of '+repr(lno)+"\n")
sys.exit(0)


