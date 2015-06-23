#! /usr/bin/env python
#
# usage: 		mksnt.py file.vcb file.tok > file.snt 2>> file.vcb
# (extends vocabulary file "file.vcb" with oovs from file.tok)
#
# alternatively: 	mksnt.py -x file.vcb file.tok > file.snt
# (does not emit vocabulary extension)
#

import sys
from codecs import open
from itertools import *

def mksnt(voc_f,txt_f,ext=True,verbose=0):
    voc = open(voc_f,'r',encoding='utf-8')
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
        sys.stderr.write(repr(n_snt)+' sents, '+repr(n_wrd)+' words, '+repr(len(dic))+' vocab\n')

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
        
        if verbose > 1:
            sys.stderr.write('collision: dic '+repr(v)+' vs. voc '+a+"\n")

    if verbose:
        sys.stderr.write('vsz = '+repr(n_voc)+"\n")
    
    oov = set()
    i_ext = max_voc + 1
    for w in dic:
        if dic[w] == 0:
            dic[w] = i_ext
            i_ext += 1
            oov.add(w)

    for words in data:
        for word in words:
            v = dic.get(word)
            print v,
        print

    if verbose:
        sys.stderr.write('oov = '+repr(n_ext-max_voc)+"\n")

    if ext:
        for w in oov:
            sys.stderr.write(repr(dic[w])+' '+w.encode('utf-8')+' 1\n')

    return 0

def main(args):
    voc_f,txt_f,extend,verbose = None,None,True,0
    for arg in args:
        if arg == '-x':
            extend = False
            continue
        if arg == '-v':
            verbose += 1
            continue
        if arg[-4:] == '.vcb':
            voc_f = arg
            continue
        if txt_f:
            return 1
        txt_f = arg
    if not txt_f or not voc_f:
        return 1
    return mksnt(voc_f,txt_f,ext=extend,verbose=verbose)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
