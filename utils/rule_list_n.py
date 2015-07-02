#! /usr/bin/env python
# takes a travatar rule-table as arg1
# outputs enumerated rule summary in 3 columns on arg2
# outputs line numbers of bad rules on arg3

from codecs import open
import sys

nin,nout,nbadl,nbadr = 0,0,0,0

with open(sys.argv[2],'w',encoding='utf-8') as good:
    with open(sys.argv[3],'w',encoding='utf-8') as bad:
        for line in open(sys.argv[1],'r',encoding='utf-8'):
            nin += 1
            r0,r1 = line.strip().split(' ||| ')[0:2]
            p0 = r0.split(' ')
            p1 = r1.split(' ')
            ll = []
            for p in p0:
                if p[0] == '"' and len(p) > 2 and p[-1] == '"':
                    ll.append(p[1:-1])
                elif p[0] == 'x':
                    ll.append("_")
            if not ll:
                bad.write(str(nin)+" 0\n")
                nbadl += 1
                continue
            l = len(ll)
            lr = []
            for p in p1:
                if p[0] == '"' and len(p) > 2 and p[-1] == '"':
                    lr.append(p[1:-1])
                elif p[0] == 'x':
                    lr.append("_")
            if not lr:
                bad.write(str(nin)+" 1\n")
                nbadr += 1
                continue
            good.write(" ".join(ll)+"\t"+" ".join(lr)+"\t"+str(nin)+"\n")
            nout += 1

sys.stderr.write("{0:d} in, {1:d} out, {2:d} lbad, {3:d} rbad\n"
                 .format(nin,nout,nbadl,nbadr))
