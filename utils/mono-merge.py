#! /usr/bin/env python
import os
import sys
import unicodedata as ud

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
            cat = ud.category(uc)
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


maxline = 1020
getword = False
detag = True
paths = []
japanese = False
scale = 4
splitting = 0

for arg in sys.argv[1:]:
    if arg[0] == '-':
        if arg == '-w':
            getword = not getword
        elif arg == '-j':
            japanese = True
        elif arg == '-d':
            detag = not detag
        elif arg[:2] == '-L':
            maxline = int(arg[2:])
        else:
            sys.stderr.write('unknown option: '+arg+"\n")
            sys.exit(1)
    elif arg[0].isdigit():
        ival = int(arg)
        if ival < 100:
            scale = ival
        else:
            splitting = ival
    elif os.access(arg,os.R_OK):
        paths.append(arg)
    else:
        sys.stderr.write('unknown arg: '+arg+"\n")
        sys.exit(1)
if not paths:
    paths.append('/dev/stdin')
paths.sort()

fds = [ open(x,'r') for x in paths ]
ixs = range(len(fds))
queue = [ fds[ii].readline() for ii in ixs ]

prevs = ''
prevu = u''
prevl = 0

while any(queue):
    try:
        val,pos = min([ (queue[ii].strip(),ii) for ii in ixs if queue[ii] ])
    except:
        val,pos = None,None
    if pos is None:

        if prevl:
            sys.stdout.write(prevs+"\n")
            prevl = 0
        break

    # remove tags from tokens
    if getword: 
        val = ' '.join(map(lambda x: x.split('|')[0],val.split(' ')))
    if detag:
        val = val.replace('<P>','')
        val = val.replace('<p>','')

    queue[pos] = fds[pos].readline() if fds[pos] else None
    if not queue[pos]:
        queue[pos] = None
        if fds[pos]:
            fds[pos].close()
            fds[pos] = None

    try:
        uval = val.decode('utf-8')
        vlen = len(uval)
    except:
        val = ''
        uval = u''
        vlen = 0

    nlen = 0
    nval = u''
    for ii in range(vlen):
        if ord(uval[ii]) > 31:
            nlen += 1
            nval += uval[ii]
    if nlen != vlen:
        vlen = nlen
        uval = nval
        val = uval.encode('utf-8')
            
    if prevl and (vlen < 2 or prevl <= vlen/2 or uval[:prevl] != prevu[:prevl]):
        sys.stdout.write(prevs+"\n")
    elif prevl:
        sys.stderr.write(prevs+"\n")

    prevu = uval
    prevs = val
    prevl = vlen
    
    if prevl > maxline:
        if prevs:
            sys.stderr.write(prevs+"\n")
        prevl = 0
        continue
    elif prevl:
        while prevl > 0:
            uch = prevu[prevl-1]
            if ord(uch) < 33:
                prevl -=1
                continue
            cat = ud.category(uch)
            if not cat or cat[0] == 'P':
                prevl -= 1
                continue
            break
        if (not prevl) and prevs:
            sys.stderr.write(prevs+"\n")
            continue
    else:
        continue

    if not japanese:
        continue

    # nlpunc+nletter+ndigit,nkana,nkanji,njpunc
    jx = counts(prevu)
    jj = sum(jx[3:])
    je = sum(jx[:3])
    if (je > (jj + jx[2]) * scale) or (je > jj * 2 * scale):
        sys.stderr.write(prevu+"\n")
        prevl = 0


sys.exit(0)
        
