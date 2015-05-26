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

iarg = 1
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

def counts(x):
    ndigit = 0
    nlpunc = 0
    nletter = 0
    nkana = 0
    nkanji = 0
    njpunc = 0
    for uc in x:
        ou = ord(uc)
        if ou < 33:
            continue
        if uc.isdigit():
            ndigit += 1
        else:
            cat = u.category(uc)
            if cat == 'Lo':
                if iskana(uc):
                    nkana += 1
                else:
                    nkanji += 1
            elif cat[0] == 'L':
                if ou > 0x2fff:
                    nkanji += 1
                else:
                    nletter += 1
            elif ou > 0x2fff:
                njpunc += 1
            else:
                nlpunc += 1
    return nlpunc,nletter,ndigit,nkana,nkanji,njpunc

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
        newname = fn+'.dtok'
    fno += 1
    ja = open(fn)
    if not quiet:
        sys.stderr.write('File '+repr(fno)+': '+fn+"\n")
    out = open(newname,'w')
    nfo += 1
    lno = 0

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
        jx = j.split(' ')
        nj = len(jx)
        pc = u.category(jx[0][-1])
        os = jx[0]
        for ij in range(1,nj):
            nj = jx[ij]
            tc = u.category(nj[0])
            if pc != 'Lo' or tc != 'Lo':
                os += ' '
            os += nj
            pc = u.category(nj[-1])

        out.write(os+"\n")
        nout += 1
        
    out.close()
    ja.close()

sys.stderr.write(repr(len(infiles))+" "+repr(nfo)+" "+repr(tno)+" "+repr(nout)+"\n")

sys.exit(0)
