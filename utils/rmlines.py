#! /usr/bin/env python

from codecs import open
import sys

nums=[]
with open(sys.argv[1],'r') as numf:
    for line in numf:
        nums.append(int(line.strip()))
if not nums:
    sys.stderr.write("no line numbers read in!\n")
    sys.exit(1)

if len(sys.argv) > 2:
    fbad = open(sys.argv[2],'w')
else:
    fbad = None
nnums=len(nums)
lno = 0
npassed=0
nremoved=0
nextno = nums.pop(0)
for line in sys.stdin:
    lno += 1
    if lno == nextno:
        if fbad:
            fbad.write(line)
        nremoved += 1
        if not nums:
            nextno = -1
        else:
            nextno = nums.pop(0)
    else:
        npassed += 1
        sys.stdout.write(line)

sys.stderr.write("saved "+str(npassed)+", dropped "+str(nremoved)+" of "+str(nnums)+" provided.\n")
