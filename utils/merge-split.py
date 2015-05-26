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
ncrunch = False
pcrunch = False
acrunch = False
paths = []
japanese = False
scale = 4
splitting = 0
suffix = ''
verbosity = 0

for arg in sys.argv[1:]:
    if arg[0] == '-':
        if arg == '-a':
            acrunch = True
        elif arg == 'n':
            ncrunch = True
        elif arg == 'p':
            pcrunch = True
        elif arg == 'c':
            acrunch = True
            ncrunch = True
            pcrunch = True
        if arg == '-w':
            getword = not getword
        elif arg == '-v':
            verbosity += 1
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
    elif len(arg) == 2:
        suffix = '.'+arg
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
lnums = [ 1 ] * len(ixs)

prevs = ''
prevu = u''
prevl = 0

class emitter:

    def __init__(self,lang,errs=False,fmt="{:03d}",block=0,append=False):
        self.fout = None
        self.lout = 0
        self.prefix = 'e' if errstream is true else 'x' if errstream is False else errstream
        self.suffix = '.'+lang if lang else ''
        self.block = splitting
        self.fmt = fmt
        self.append = append
        
    def emit(self,str,nl="\n"):
        if isinstance(str,unistr):
            str = str.encode('utf-8')
        elif not isinstance(str,basestring):
            str = repr(str)

        if not self.fout or (self.block > 0 and self.lout % sp == 0):
            self.fout = open(prefix+fmt.format(self.lout/self.block)+suffix,'w')

        self.fout.write(str+nl)
        self.lout += 1
        return self.lout
        
    def close(self):
        if self.fout is not None:
            self.fout.close()
            self.fout = None


class recoder:
    def __init__(self,numbers=False,punct=False,letters=False):
        self.numbers = numbers
        self.punct = punct
        self.letters = letters
        self.any = numbers or punct or letters

    def recode(self,sval):
        us = filter(lambda x: ord(x) > 31,sval.decode('utf-8'))
        if self.any:
            pnumber = False
            pc = None
            for ii in range(len(us)):
                oc = ord(us[ii])
                if self.numbers:
                    # only likley number chars are dealt with here
                    # specifically dis-including wide versions of currency, pct, etc.
                    pnumber = number
                    if oc > 0xff0a and oc < 0xff20::
                        if oc > 0xff0f:
                            number = True
                            oc -= 0xff10
                    elif oc == 0xff0b:
                        oc = ord('+')
                    elif oc == 0xff0c:
                        oc = ord(',')
                    elif oc == 0xff0d:
                        oc = ord('-')
                    elif oc == 0xff0e:
                        oc = ord('.')
                        
                pnumber = 
                        
            elif oc > 0xff0f:
                nchanged += 1
                nl += unicode(repr(ord(ch)-0xff10))
            # here, 0xff0b to 0xff0f remain to be processed
            elif oc == 0xff0b:
                nchanged += 1
                nl += u'+'
            elif oc == 0xff0c:
                nchanged += 1
                nl += u','
            elif oc == 0xff0d:
                nchanged += 1
                nl += u'-'
            elif oc == 0xff0e:
                nchanged += 1
                nl += u'.'
            else: # 0xff0f
                nl += ch
    nnarrow += nchanged
    if nchanged and verbosity > 2:
        sys.stderr.write(nl.encode('utf-8')+"\n")

        return us,us.encode('utf-8'),len(us)


fout = emitter(suffix[1:],errs=False,block=splitting)
ferr = emitter(suffix[1:],errs=True,block=splitting)

while any(queue):

    try:
        val,pos = min([ (queue[ii].strip(),ii) for ii in ixs if queue[ii] ])
    except:
        val,pos = None,None

    if pos is None:
        if prevl:
            fout.emit(prevs)
            prevl = 0
        break

    # remove tags from tokens
    if getword: 
        val = ' '.join(map(lambda x: x.split('|')[0],val.split(' ')))
    if detag:
        val = val.replace('<P>','')
        val = val.replace('<p>','')
    uval,val,vlen = recode(val)

    queue[pos] = fds[pos].readline() if fds[pos] else None
    lnums[pos] += 1

    if not queue[pos]:
        queue[pos] = None
        if fds[pos]:
            fds[pos].close()
            fds[pos] = None

    if prevl:
        if vlen < 2 or prevl <= vlen/2 or uval[:prevl] != prevu[:prevl]:
            fout.emit(prevs)
        else:
            ferr.emit(prevs)
            if splitting and verbosity:
                sys.stderr.write("len at {0}:{1} {2}->{3}\n".format(paths[pos],lnums[pos],vlen,prevl))

    prevu = uval
    prevs = val
    prevl = vlen
    
    if prevl > maxline:
        if prevs:
            ferr.emit(prevs)
            if splitting and verbosity:
                sys.stderr.write("overflow at {0}:{1}\n".format(paths[pos],lnums[pos]))
        prevl = 0

    if not prevl:
        continue

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
        ferr.emit(prevs)
        if splitting and verbosity:
            sys.stderr.write("underflow at {0}:{1}\n".format(paths[pos],lnums[pos]))
        continue

    if japanese:
        # nlpunc+nletter+ndigit,nkana,nkanji,njpunc
        jx = counts(prevu)
        jj = sum(jx[3:])
        je = sum(jx[:3])
        if (je > (jj + jx[2]) * scale) or (je > jj * 2 * scale):
            ferr.emit(prevs)
            if splitting and verbosity:
                sys.stderr.write("bal at {0}:{1} - {2},{3},{4}\n".format(paths[pos],lnums[pos],je,jj,jx[2]))
            prevl = 0

sys.exit(0)
