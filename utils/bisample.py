#! /usr/bin/env python

import os
import sys
import random

args = sys.argv[1:]

prefixes=[]
suffixes=[]
files=[]

rate=0.0
seed=0
bases=[]

for arg in args:
    if arg[0].isdigit():
        if arg.find('.') > 0:
            rate = float(arg)
        else:
            seed = int(arg)
        continue
    parts=arg.split('.')
    if len(parts) > 1 and parts[1] == 'sample':
        print 'Error: cannot resample a sample file.  First, rename',arg
        sys.exit(1)
    prefix=parts[:-1]
    suffix=parts[-1]
    if prefix == suffix or not prefix:
        bases.append(suffix)
        continue
    files.append(arg)
    prefixes.append(parts[0])
    suffixes.append(suffix)

if len(files) != 2 or len(prefixes) != 2 or len(suffixes) != 2:
    print 'Error parsing arguments:',repr(files)
    sys.exit(1)

if suffixes[0] == suffixes[1]:
    print 'Error: collision in suffixes:',repr(suffixes)
    sys.exit(1)

if bases and len(bases) > 2:
    print 'Error: excess basename arguments:',repr(bases)
    sys.exit(1)

if not rate:
    print 'Missing rate argument.'
    sys.exit(1)
print 'rate =',rate

if not seed:
    seed = os.getpid()
print 'seed =',seed
random.seed(seed)

pout = []
qout = []
for ii in range(2):
    if not bases:
        pout.append(prefixes[ii]+'-sample.'+suffixes[ii])
        print pout[-1]
    else:
        pout.append(bases[0] + '.' + suffixes[ii])
        if len(bases) == 2:
            print pout[-1],
            qout.append(bases[1]+'.'+suffixes[ii])
            print qout[-1]
        else:
            print pout[-1]

a, b, c, d, e, f = None, None, None, None, None, None

try:
    a = open(files[0],'r')
    b = open(files[1],'r')
    c = open(pout[0],'w')
    d = open(pout[1],'w')
    if qout:
        e = open(qout[0],'w')
        f = open(qout[1],'w')
except:
    ty,ob,ms = sys.exc_info()
    sys.excepthook(ty,ob,ms)
    sys.exit(1)

empty = 0
lno = 0
nout = 0
nrem = 0
abad = 0
bbad = 0

try:
    while True:
        rval = random.random()
        a_in = a.readline().strip()
        b_in = b.readline().strip()
        if not a_in and not b_in:
            break
        lno += 1
        if not a_in and not b_in:
            empty += 1
            continue
        if not a_in:
            sys.stderr.write("Mismatched input A line "+repr(lno)+"\n")
            abad += 1
            continue
        if not b_in:
            sys.stderr.write("Mismatched input B line "+repr(lno)+"\n")
            bbad += 1
            continue
        if rval < rate:
            c.write(a_in+"\n")
            d.write(b_in+"\n")
            nout += 1
        elif qout:
            e.write(a_in+"\n")
            f.write(b_in+"\n")
            nrem += 1
except:
    sys.stderr.write("Exception writing "+outpath+' at input line '+repr(lno)+"\n")
    ty,ob,ms = sys.exc_info()
    sys.excepthook(ty,ob,ms)
    sys.exit(1)

sys.stderr.write('read total '+repr(lno)+' lines'+"\n")
if qout:
    sys.stderr.write('output remainders '+repr(nrem)+' lines'+"\n")
sys.stderr.write('output samples '+repr(nout)+' lines'+"\n")

sys.exit(0)


