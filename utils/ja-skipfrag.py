#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unicodedata as u

words=True
verbosity = 0
quiet = False
enumerated=False
suffix='ja'
infiles=[]

iarg=1
while iarg < len(sys.argv):
    arg = sys.argv[iarg]
    if arg == '-w':
        words=True
    elif arg == '-n':
        enumerated = True
    elif arg == '-v':
        verbosity += 1
    elif arg == '-q':
        quiet = True
    elif len(arg) == 2:
        suffix=arg
    elif os.access(arg,os.R_OK):
        infiles.append(arg)
    else:
        sys.stderr.write("bad arg at "+arg+"\n")
        sys.exit(1)
    iarg += 1

if verbosity:
    sys.stderr.write('parameters: '+repr(p)+"\n")

if not infiles:
    infiles = [ x for x in  os.listdir('.') if x[-3:] == '.'+suffix ]

if not infiles:
    infiles = ['/dev/stdin']
    sys.stderr.write('Reading from stdin'+"\n")

fno = 0
tno = 0
nfo = 0
nout = 0
for fn in infiles:
    if fn == '/dev/stdin':
        newname = '/dev/stdout'
    else:
        newname = fn+'.dfrag'
    fno += 1
    ja = open(fn)
    if not quiet:
        sys.stderr.write('File '+repr(fno)+': '+fn+"\n")
    out = open(newname,'w')
    nfo += 1
    lno = 0

    prevs = ''
    prevu = u''
    for j in ja:
        lno += 1
        tno += 1
        j = j.strip()
        if words:
            j = ' '.join(map(lambda x: x.split('|')[0],j.split(' ')))
        if enumerated:
            prefix = fn+':'+repr(lno)+"\t"
        if not j:
            if not quiet:
                sys.stderr.write('empty line: '+fn+':'+repr(lno)+"\n")
            continue
        try:
            jd = j.decode('utf-8')
        except:
            if not quiet:
                sys.stderr.write('bad encoding: '+fn+':'+repr(lno)+" ja: "+j+"\n")
            eno += 1            
            continue

        if len(prevu) > 10 and len(jd) < 2*len(prevu):
            if jd[:len(prevu)] == prevu:
                if not quiet:
                    sys.stderr.write('drop fragment from line '+repr(lno-1)+"\n")
                prevu = jd
                prevs = j
                continue
        
        if prevs:
            out.write(prevs+"\n")
            nout += 1

        prevu = jd
        prevs = j

    if prevs:
        out.write(prevs+"\n")
    out.close()
    ja.close()

sys.stderr.write(repr(len(infiles))+" "+repr(nfo)+" "+repr(tno)+" "+repr(nout)+"\n")

sys.exit(0)
