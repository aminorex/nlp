#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unicodedata as u

japanese=0
words=True
infiles = []
outfile = '/dev/stdout'
badfile = None
hardfail = False
report = None
verbosity = 0
p = [ 4, 12, 6, 18, 8 ]
ppos = 0
iarg = 1
div="\t"
swap=False
bitext=False
fixups=True
enumerated=False

while iarg < len(sys.argv):
    arg = sys.argv[iarg]
    if arg == '-j':
        japanese += 1
    elif arg == '-J':
        japanese += 2
    elif arg == '-w':
        words=True
    elif arg == '-f':
        fixups=False
    elif arg == '-e':
        iarg += 1
        badfile = sys.argv[iarg]
    elif arg == '-o':
        iarg += 1
        outfile = sys.argv[iarg]
    elif arg == '-r':
        iarg += 1
        report = sys.argv[iarg]
    elif arg == '-p':
        div='|||'
    elif arg == '-n':
        enumerated = True
    elif arg == '-s':
        swap = True
    elif arg == '-H':
        hardfail = True
    elif arg == '-v':
        verbosity += 1
    elif arg[0].isdigit() and ppos < len(p):
        p[ppos] = int(arg[0])
        ppos += 1
    elif len(infiles) < 2 and os.access(arg,os.R_OK):
        infiles.append(arg)
    else:
        sys.stderr.write("bad arg at "+arg+"\n")
        sys.exit(1)
    iarg += 1

if verbosity:
    sys.stderr.write('parameters: '+repr(p)+"\n")

if swap and len(infiles) != 1:
    sys.stderr.write("can not swap unless bitext is input\n")
    sys.exit(1)
if len(infiles) == 0:
    sys.stderr.write("no input files\n");
    sys.exit(1)
if len(infiles) > 2:
    sys.stderr.write("too many input files\n");
    sys.exit(1)
        
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

lno=0
nout=0
badtabs=0
badsize=0
badchars=0

if len(infiles) == 1:
    bitext = True
    inp = open(infiles[0])
else:
    en = open(infiles[0])
    ja = open(infiles[1])

out = open(outfile,'w')
bad = open(badfile,'w') if badfile else None
rpt = open(report,'w') if report else None

if swap:
    j,e = inp.readline().strip().split(div)
elif bitext:
    e,j = inp.readline().strip().split(div)
else:
    e = en.readline().strip()
    j = ja.readline().strip()

p0, p1, p2, p3, p4 = p[0], p[1], p[2], p[3], p[4]


def fixup(l,e,j):
    olde = e
    if e.find('_') > -1:
        e = e.replace('_ _','__')
        e = e.replace('_ cbrace _','_cbrace_')
        e = e.replace('_ obrace _','_obrace_')
        e = e.replace('_ gt _','_gt_')
        e = e.replace('_ lt _','_lt_')
        e = e.replace('_ pipe _','_pipe_')
        if verbosity and olde != e:
            sys.stderr.write('e mod '+repr(l)+' '+olde+' -> '+e+"\n")
    oldj = j
    if j.find('_') > -1:
        j = j.replace('_ _','__')
        j = j.replace('_ cbrace _','_cbrace_')
        j = j.replace('_ obrace _','_obrace_')
        j = j.replace('_ gt _','_gt_')
        j = j.replace('_ lt _','_lt_')
        j = j.replace('_ pipe _','_pipe_')
        if verbosity and oldj != j:
            sys.stderr.write('j mod '+repr(l)+' '+oldj+' -> '+j+"\n")
    if len(j) > len(e) and j[:len(e)] == len(e):
        j = j[len(e):]
        if verbosity and oldj != j:
            sys.stderr.write('drop e->j prefix at '+repr(l)+"\n")
        
    op = e.find('(')
    if op > -1 and op < len(e)-2 and e[op+1:].find('(') > -1:
        cp = e.find(')')
        if cp > op:
            if (j.find('(') < 0 and j.find('（') < 0) or (j.find(')') < 0 and j.find('）') < 0): 
                e = e[:op].strip()+' '+e[cp+1:].strip()
                sys.stderr.write('strip e '+repr(l)+' '+olde+' -> '+e+"\n")
    oldj = j
    op = j.find('（')
    if op > -1 and op < len(j)-2 and  j[op+1].find('（') > -1:
        cp = j.find('）')
        if cp > op:
            if e.find('(') < 0 and e.find(')') < 0:
                ex = counts((j[:op]+j[cp+1:]).decode('utf-8'))
                ne = sum(ex[:3])
                nj = sum(jx[2:]) # include latin digits as typical japanese codepoints
                if ne > nj*4:
                    ex = counts(j[op+1:cp].decode('utf-8'))
                    ne = sum(ex[:3])
                    nj = sum(jx[2:]) # include latin digits as typical japanese codepoints
                    if nj > ne*2:
                        j = j[op+1:cp]
                        sys.stderr.write('strip j '+repr(l)+' '+oldj+' -> '+j+"\n")
                j = j[:op+1]
    return e,j

while e and j:
    lno += 1
    efail = False
    jfail = False
    mode = None

    if words:
        e = ' '.join(map(lambda x: x.split('|')[0],e.split(' ')))
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
            mode = 'e bad utf8'

    if fixups:
        e,j = fixup(lno,e,j)

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
            mode = 'f bad utf8'

    prefix = repr(lno)+"\t"

    if not mode:
        if ed == jd:
            mode = 'no translation'
        elif not e.strip():
            mode = 'e empty'
        elif not j.strip():
            mode = 'f empty'
        elif len(jd) > p0 * len(ed) + p1:
            badsize += 1
            mode = 'a: |f|>'+repr(p0)+'|e|+'+repr(p1)
            mode += ': |f|='+repr(len(jd))+', |e|='+repr(len(ed))+' -> '+repr(p0*len(ed)+p1)
        elif len(ed) > p2 * len(jd) + p3:
            badsize += 1
            mode = 'b: |e|>'+repr(p2)+'|f|+'+repr(p3)
            mode += ': |e|='+repr(len(ed))+', |f|='+repr(len(jd))+' -> '+repr(p2*len(jd)+p3)
        elif japanese:
            ex = counts(ed)
            jx = counts(jd)
            # nlpunc+nletter+ndigit,nkana,nkanji,njpunc
            ej = sum(ex[3:])
            ee = sum(ex[:3])
            jj = sum(jx[2:]) # include latin digits as typical japanese codepoints
            je = sum(jx[:3])
            if ej > jj or je > ee:
                badchars += 1
                mode = 'c: ej>jj='+repr(ej>jj)+' ; je>ee='+repr(je>ee)
                mode += ' ; ej='+repr(ej)+',jj='+repr(jj)+',je='+repr(je)+',ee='+repr(ee)
                mode += ' :: ' + repr(ex) + ' ' + repr(jx)
            elif japanese > 1:
                if ej > ee or je > jj*p4:
                    badchars += 1
                    mode = 'd: ej>ee='+repr(ej>ee)+' ; je>jj*'+repr(p4)+'='+repr(je>jj*p4)
                    mode += ' ; ej='+repr(ej)+',jj='+repr(jj)+',je='+repr(je)+',ee='+repr(ee)
                    mode += ' :: ' + repr(ex) + ' ' + repr(jx)

    if not mode:
        out.write((prefix if enumerated else '')+e+div+j+"\n")
        nout += 1
    elif bad:
        bad.write((prefix if enumerated else '')+e+div+j+"\n")
        if rpt or (verbosity > 1):
            errstr = prefix+mode+"\n"
            if rpt:
                rpt.write(errstr)
            if verbosity > 1:
                sys.stderr.write(errstr)
                if mode != 'no translation':
                    sys.stderr.write(prefix+'e: '+e+"\n")
                    sys.stderr.write(prefix+'j: '+j+"\n")
    if swap:
        try:
            s = inp.readline()
            j,e = s.strip().split(div) if s else (None,None)
        except:
            sys.stderr.write('split error at line'+repr(lno+1)+"\n")
            sys.exit(1)

    elif bitext:
        e,j = inp.readline().strip().split(div)
    else:
        e = en.readline().strip()
        j = ja.readline().strip()

    if verbosity and (lno % 1000) == 0:
        sys.stderr.write('line '+repr(lno)+"\n")

out.close()
if bad:
    bad.close()
if rpt:
    rpt.close()

sys.stderr.write(repr(lno)+" "+repr(nout)+" "+repr(badsize)+" "+repr(badchars)+"\n")
sys.exit(0)
