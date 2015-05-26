#! /usr/bin/env python

import sys
import re

kdigs=U"○一二三四五六七八九十"
wdigs=U"０１２３４５６７８９‐"

def urepr(n,digs):
    r=U''
    while True:
        r = digs[n % 10] + r
        n = n / 10
        if not n:
            break
    return r
            
def krepr(n):
    return urepr(n,kdigs)

def wrepr(n):
    return urepr(n,wdigs)



id_x=re.compile(r' id="(\d+):(\d+)"')
vs_x=re.compile(r'<p>(.*)</p>')

state=0
lno=0
ch=0
vs=0
nv=0
ne=0
for line in sys.stdin:
    lno += 1
    if ch == 0:
        m = re.search(id_x,line)
        if not m:
            continue
        ch=int(m.group(1))
        vs=int(m.group(2))
    else:
        m = re.search(vs_x,line)
        if not m:
            sys.stderr.write('vs_x not matched at line '+str(lno)+' '+str(ch)+':'+str(vs)+"\n")
            txt = 'ERR'
            ne += 1
        else:    
            txt=m.group(1)
            if not txt: 
                sys.stderr.write('vs_x empty at line '+str(lno)+' '+str(ch)+':'+str(vs)+"\n")
                sys.exit(1)
        print txt
        nv += 1
        ch = 0
sys.stderr.write('extracted '+str(nv)+' verses in '+str(lno)+' lines with '+str(ne)+' errors'+"\n")
sys.exit(0)


    
