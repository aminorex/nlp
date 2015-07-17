#! /usr/bin/env python

import sys
import os
from codecs import open

rf=None
invert=False

for arg in sys.argv[1:]:
    if os.access(arg,os.R_OK):
        if rf:
            print 'Only one path argument please.'
            sys.exit(1)
        rf=open(arg,'r',encoding='utf-8')
    elif arg == '-i':
        invert = True
    else:
        print 'Bad argument',arg
        sys.exit(1)

if not rf:
    print 'Retain list argument required'
    sys.exit(1)

rno = int(rf.readline().strip())
lno = 0

with open('/dev/stdin','r',encoding='utf-8') as inf:
    with open('/dev/stdout','a',encoding='utf-8') as outf:
            while rno:
                for line in inf:
                    lno += 1
                    if invert:
                        if lno == rno:
                            break
                        outf.write(line)
                    elif lno == rno:
                        outf.write(line)
                        break
                if lno != rno:
                    sys.stderr.write("Premature end at line {0:d}\n"
                                     .format(lno))
                    break
                try:
                    rno = int(rf.readline().strip())
                except:
                    rno = 0
