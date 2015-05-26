#! /usr/bin/env python
import sys
import math

col=0
fs=' '
idv=0.0
op='sum'

for arg in sys.argv[1:]:
    if fs is None:
        fs=arg
    elif arg == '-F':
        fs=None
    elif not col and arg[0].isdigit():
        col= int(arg)
    elif not idv and arg[0].isdigit():
        idv = float(arg)
    elif arg == '+' or arg == 'sum':
        op='sum'
    elif arg == '*' or arg[:4] == 'prod':
        op='product'
        idv=1.0
    elif arg == '!' or arg[:4] == 'max':
        op='max'
        idv=None
    elif arg == '_' or arg[:4] == 'min':
        op='min'
        idv=None
    elif arg[0] == 'l':
        op='length'
    else:
        sys.stderr.write(sys.argv[0]+': Bad option '+arg+"\n")
        sys.exit(1)

lno = 0
ret=idv
count = 0
for line in sys.stdin:
    lno += 1
    toks=line.strip().split(fs)
    if len(toks) < col + 1:
        sys.stderr.write('Bad line '+lno+"\n")
        continue
    try:
        val = float(toks[col])
    except:
        sys.stderr.write('Malformed token at line '+lno+"\n")
        continue
    if ret is None:
        ret = val
    elif op == 'max':
        ret = max(ret,val)
    elif op == 'min':
        ret = min(ret,val)
    elif op == 'product':
        ret *= val
    elif op == 'length':
        ret += val*val
    else:
        ret += val
    count += 1

if op == 'length':
    ret = sqrt(ret)

print ret
sys.exit(0)

    
