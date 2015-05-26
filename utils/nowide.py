#! /usr/bin/env python

# filter out wide lines, remove <p> tags, and narrow any fullwidth numerics

import sys
import unicodedata as u

maxlen = 1020
narrow = True
detag = True
verbosity = 0

for arg in sys.argv[1:]:
    if arg[0].isdigit():
        maxlen=int(arg)
    elif arg == '-n':
        narrow = not narrow
    elif arg == '-d':
        detag = not detag
    elif arg == '-v':
        verbosity += 1
    else:
        sys.stderr.write("Unknown argument ignored: "+arg+"\n");

lno = 0
maxwidth=0
nwide=0
nzero=0
nnarrow=0
ntagged=0

for line in sys.stdin:
    line = line.strip()
    lno += 1
    ll=len(line)
    if verbosity and (lno % 50000) == 0:
        sys.stderr.write('#'+repr(lno)+"\n")
    if ll > maxwidth:
        maxwidth=ll
    if ll > maxlen:
        if verbosity > 1:
            sys.stderr.write("Long line "+repr(lno)+": "+repr(len(line))+"\n")
        nwide += 1
        continue
    if detag and (line.find('<P>') > -1 or line.find('<p>') > -1):
        line = line.replace('<P>','')
        line = line.replace('<p>','')
    if not line:
        if verbosity > 1:
            sys.stderr.write("Empty line "+repr(lno)+"\n")
        nzero += 1
        continue
    nchanged = 0
    if narrow:
        nl = u''
        for ch in line.decode('utf-8'):
            oc = ord(ch)
            # only likley number chars are dealt with here
            # specifically dis-including wide versions of currency, pct, etc.
            if oc < 0xff0b or oc > 0xff19:
                nl += ch
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
    sys.stdout.write((nl.encode('utf-8') if nchanged else line)+"\n")

sys.stderr.write("Total lines "+repr(lno)+", max width "+repr(maxwidth)+"\n")
sys.stderr.write("Wide lines "+repr(nwide)+", empty lines "+repr(nzero)+"\n") 
if narrow:
    sys.stderr.write("Wide digits "+repr(nnarrow)+"\n") 
if detag:
    sys.stderr.write("Tags removed "+repr(ntagged)+"\n") 

sys.exit(0)
