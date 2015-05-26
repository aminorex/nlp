#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unicodedata as u

japanese=0
words=True
verbosity = 0
quiet = False
p = [ 4 ]
ppos = 0
iarg = 1
enumerated=False
suffix='ja'
postop=False
infiles = []

while iarg < len(sys.argv):
    arg = sys.argv[iarg]
    if arg == '-w':
        words=True
    elif arg == '-n':
        enumerated = True
    elif arg == '-v':
        verbosity += 1
    elif arg == '-p':
        postop = True
    elif arg == '-q':
        quiet = True
    elif arg[0].isdigit() and ppos < len(p):
        p[ppos] = int(arg[0])
        ppos += 1
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

nout=0
ncset=0
fno = 0
tno = 0
eno = 0
processed = []
prefix = ''

if not infiles:
    infiles = os.listdir('.')

infiles.sort()

for fn in infiles:
    if fn[-3:] != '.'+suffix:
        continue
    hasOkay = os.access(fn+'.okay',os.R_OK)
    if postop:
        if hasOkay:
            if not os.access(fn+'.orig',os.R_OK):
                os.rename(fn,fn+'.orig')
            else:
                os.unlink(fn)
            os.rename(fn+'.okay',fn)
        continue

    if hasOkay:
        continue

    processed.append(fn)
    fno += 1

    ja = open(fn)
    if not quiet:
        sys.stderr.write('File '+repr(fno)+': '+fn+"\n")
    out = open(fn+'.okay','w')
    bad = open(fn+'.fail','a')

    lno = 0

    for j in ja:
        lno += 1
        tno += 1
        err = False
        if words:
            j = ' '.join(map(lambda x: x.split('|')[0],j.split(' ')))
            
        j = j.strip()
        j = j.replace('<P>','')
        j = j.replace('<p>','')

        if enumerated:
            prefix = fn+':'+repr(lno)+"\t"

        if not j:
            if verbosity:
                sys.stderr.write('empty line: '+fn+':'+repr(lno)+"\n")
            bad.write(prefix+j+"\n")
            continue
        try:
            jd = j.decode('utf-8')
        except:
            if verbosity:
                sys.stderr.write('bad encoding: '+fn+':'+repr(lno)+" ja: "+j+"\n")
            bad.write(prefix+j+"\n")
            eno += 1            
            continue

        jx = counts(jd)
        # nlpunc+nletter+ndigit,nkana,nkanji,njpunc
        jj = sum(jx[2:]) # include latin digits as typical japanese codepoints
        je = sum(jx[:3])
        if je > jj * p[0] or je > (jj - jx[2])*2*p[0] :
            bad.write(prefix+j+"\n")
            if verbosity > 1:
                r=float(jj)/float(jj+je)
                sys.stderr.write('cset imbalance('+repr(jx)+'): '+fn+repr(lno)+" ja: "+j+" "+repr(r)[:6]+"\n")
            ncset += 1
            continue
        if verbosity > 3:
            r=float(jj)/float(jj+je)
            sys.stderr.write('cset balance('+repr(jx)+'): '+fn+repr(lno)+" ja: "+j+" "+repr(r)[:6]+"\n")

        out.write(prefix+j+"\n")
        nout += 1

        if (not quiet) and (tno % 50000) == 0:
            r=float(jj)/float(jj+je)
            sys.stderr.write('file '+repr(fno)+', cumm. line no. '+repr(lno)+' :: '+repr([tno,nout,ncset,eno])+"\n")

    out.close()
    bad.close()

if not postop:
    sys.stderr.write(repr(tno)+" "+repr(nout)+" "+repr(ncset)+" "+repr(eno)+"\n")

sys.exit(0)
