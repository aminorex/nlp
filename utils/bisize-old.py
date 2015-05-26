#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unicodedata as u

japanese=0
words=True
infiles = []
outfile = '/dev/stdout'
badfile = '/dev/null'
hardfail = False

iarg = 1
while iarg < len(sys.argv):
    arg = sys.argv[iarg]
    if arg == '-j':
        japanese += 1
    elif arg == '-J':
        japanese += 2
    elif arg == '-w':
        words=True
    elif arg == '-e':
        iarg += 1
        badfile = sys.argv[iarg]
    elif arg == '-o':
        iarg += 1
        outfile = sys.argv[iarg]
    elif arg == '-H':
        hardfail = True
    elif len(infiles) < 2 and os.access(arg,os.R_OK):
        infiles.append(arg)
    else:
        sys.stderr.write("bad arg at "+arg+"\n")
        sys.exit(1)
    iarg += 1

if len(infiles) != 2:
    sys.stderr.write("too few input files\n");
    sys.exit(1)
        
import unicodedata as u

def iskana(x):
    if type(x) == int:
        x = unichr(x)
    if len(x) != 1 or type(x) != type(u' '):
        return False
    y = ord(x)
    if y < 0x3041:
        return False
    if y < 0x3097:
        return True
    if y < 0x3099:
        return False
    if y < 0x30FB:
        return True
    if y < 0x30FC:
        return False
    if y < 0x3100:
        return True
    if y < 0xFF66:
        return False
    if y < 0xFFA0:
        return True
    return False

def iskanji(x):
    if type(x) == int:
        x = unichr(x)
    if len(x) != 1 or type(x) != type(u' '):
        return False
    if u.category(x) == 'Lo':
        return not iskana(x)
    return False

def jcount(x):
    return sum(map(lambda x: 1 if iskana(x) or iskanji(x) else 0,x))

def ecount(x):
    return len(x) - jcount(x)

lno=0
nout=0
badtabs=0
badsize=0
badchars=0

en = open(infiles[0])
ja = open(infiles[1])

bad = open(badfile,'w')
out = open(outfile,'w')

e = en.readline().strip()
j = ja.readline().strip()

while e and j:
    lno += 1
    okay = True
    efail = False
    jfail = False

    if words:
        e = ' '.join(map(lambda x: x.split('|')[0],e.split(' ')))
    if words:
        j = ' '.join(map(lambda x: x.split('|')[0],j.split(' ')))

    try:
        ed = e.decode('utf-8')
    except:
        sys.stderr.write(repr(lno)+" en: "+e+"\n")
        if hardfail:
            ty,ob,ms = sys.exc_info()
            sys.excepthook(ty,ob,ms)
            sys.exit(1)
        else:
            efail = True
            okay = False

    try:
        jd = j.decode('utf-8')
    except:
        sys.stderr.write(repr(lno)+" ja: "+j+"\n")
        if hardfail:
            ty,ob,ms = sys.exc_info()
            sys.excepthook(ty,ob,ms)
            sys.exit(1)
        else:
            jfail = True
            okay = False

    if japanese and okay:
        ej = jcount(ed)
        ee = len(ed) - ej
        jj = jcount(jd)
        je = len(jd) - jj
        if japanese == 1:
            if ej > jj or je > ee:
                badchars += 1
                okay = False
        elif len(jd) > 3 * len(ed) + 8:
            badsize += 1
            okay = False
        elif len(ed) > 3 * len(jd) + 8:
            badsize += 1
            okay = False
        elif japanese == 2:
            if ej > jj or je > ee or ej > ee or je > jj:
                badchars += 1
                okay = False

    if okay:
        out.write(e+"\t"+j+"\n")
        nout += 1
    else:
        bad.write(e+"\t"+j+"\n")
        
    e = en.readline().strip()
    j = ja.readline().strip()

sys.stderr.write(repr(lno)+" "+repr(nout)+" "+repr(badsize)+" "+repr(badchars)+"\n")
sys.exit(0)
