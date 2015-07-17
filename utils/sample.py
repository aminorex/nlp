#! /usr/bin/env python

import os
import sys
import random
from codecs import open

rate=0.0
count=0
seed=0

for arg in sys.argv[1:]:
    if arg[0].isdigit():
        if arg.find('.') > 0:
            rate = float(arg)
        elif count:
            seed = int(arg)
        else:
            count = int(arg)
        continue

if not rate:
    print 'Missing rate argument.'
    sys.exit(1)

if not seed:
    seed = os.getpid()
random.seed(seed)

with open('/dev/stdin','r',encoding='utf-8') as inf:
    with open('/dev/stdout','a',encoding='utf-8') as outf:
        lno = 0
        for line in inf:
            lno += 1
            rval = random.random()
            if rval <= rate:
                outf.write(line)
                if count > 0:
                    count -= 1
                    if not count:
                        break
                    

