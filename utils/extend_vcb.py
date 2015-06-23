#! /usr/bin/env python
#
# usage: 		extendvcb.py file.vcb file.tok [-inplace|new.vcb]
# (extends vocabulary file "file.vcb" with oovs from file.tok, inplace or to stdout/new.vcb)
#

import sys
from codecs import open
from itertools import *

def extend_vcb(voc_f,txt_f,new_f=None,verbose=0):
    data = []
    dic = {}
    n_snt = 0
    n_wrd = 0
    for ii,txt in  enumerate(open(txt_f,'r',encoding='utf-8')):
        n_snt += 1
        words = txt.strip().split()
        for word in words:
            n_wrd += 1
            dic[word] = 0
        data.append(words)
    if verbose:
        sys.stderr.write("{0:d} sentences, {1:d} tokens\n" .format (n_snt,n_wrd))

    n_voc = 0
    max_voc = 0
    for ii,txt in enumerate(open(voc_f,'r',encoding='utf-8')):
        n_voc += 1
        a,w = txt.split()[:2]
        a = int(a)
        if a > max_voc:
            max_voc = a
        v = dic.get(w)
        if v is None:
            continue
        if v == 0:
            dic[w] = int(a)
            continue
    if verbose:
        sys.stderr.write("{0:d} known, {1:d} max\n" .format (n_voc,max_voc))

    oov = set()
    i_ext = max_voc + 1
    for w in dic:
        if dic[w] == 0:
            dic[w] = i_ext
            i_ext += 1
            oov.add(w)
    if verbose:
        sys.stderr.write("{0:d} oov, {1:d} total, {1:d} max\n" 
                         .format ((i_ext-max_voc),i_ext-max_voc+n_voc,i_ext))

    if new_f == '-' or new_f == '/dev/stdout':
        if verbose:
            sys.stderr.write("emit extension to stdout\n")
        out_f = open('/dev/stdout','a',encoding='utf-8')
    elif new_f:
        if verbose:
            sys.stderr.write("concatenate to {0:s}\n" .format (new_f));
        out_f = open(new_f,'w',encoding='utf-8')
        for line in open(voc_f,'r',encoding='utf-8'):
            out_f.write(line)
    else:
        if verbose:
            sys.stderr.write("append to {0:s} in place\n" .format (voc_f))
        out_f = open(voc_f,'a',encoding='utf-8')

    # emit extension
    for w in oov:
        out_f.write((u"{0:d} {1:s} 1\n" .format (dic[w],w)))

    out_f.close()
    return 0

def main(args):
    voc_f,txt_f,new_f,verbose,inplace = None,None,None,0,False
    
    for arg in args:
        if arg == '-i':
            inplace = True
        elif arg == '-v':
            verbose += 1
        elif arg.find('-inplace') > -1:
            inplace = True
        elif arg[-4:] == '.vcb':
            if not voc_f:
                voc_f = arg
            elif not new_f:
                new_f = arg
            else:
                return 1
        elif new_f:
            return 1
        elif txt_f:
            if new_f:
                return 1
            new_f = arg
        else:
            txt_f = arg

    if not txt_f or not voc_f:
        return 1

    if not new_f and not inplace:
        new_f = '/dev/stdout'

    if verbose:
        sys.stderr.write("{0:s} voc, {1:s} txt, {2:s} new\n"
                         .format(voc_f,txt_f,"NULL" if new_f is None else new_f))
    return extend_vcb(voc_f,txt_f,new_f,verbose=verbose)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
