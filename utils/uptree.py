#! /usr/bin/env python

# convert a ROOT-wrapped lower-case and/or binarized tree to something 
# acceptable for pennconverter 
#
# as a pipe element, converts one tree per line of input
# with an integer argument, selects only that line
#

import os,sys,getopt

def upconvert(line):
    out = ""
    ii = 0
    prev = False
    line = line[6:-1] #  omit /(ROOT /.../)/ wrapper
    ll = len(line)
    while ii < ll:
        if line[ii] == '(':
            out += '('
            prev = True
            ii += 1
        elif prev and line[ii].isalpha():
            jj = ii + 1
            while jj < ll and line[jj].isalpha():
                jj += 1
            tag = line[ii:jj].upper()
            out += tag
            if jj < ll and line[jj] == "'":
                jj += 1
            prev = False
            ii = jj
        else:
            out += line[ii]
            prev = False
            ii += 1
    return out

if __name__ == '__main__':
    lno = 0
    sel = 0
    if len(sys.argv) > 1:
        sel = int(sys.argv[1])
    for line in sys.stdin:
        lno += 1
        if sel < 1 or sel == lno:
            print upconvert(line.strip())
            if sel == lno:
                break
    sys.exit(0)

                
