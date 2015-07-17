#! /usr/bin/env python

# script to check for and optionally remove lines matching lines
# found in the first argument path.  ideographic and ascii spaces
# are first removed from the lines.  test target files may be bitexts
# which are checked in one column only. 
#
# pre-existing file arguments are assumed to be inputs.
# non-existing file arguments are clean, dirty output line sinks.
# without sinks, scanning stops for a given file when taint is detected.
# unless -q is specified, stats are reported and progress is painted.

from codecs import open
from copy import copy
import sys
import os

def packed_set(taint_path):
    taints=set()
    with open(taint_path,'r',encoding='utf-8') as taintf:
        for line in taintf:
            line = line.strip()
            line.replace(u"\u3000","")
            line.replace(u" ","")
            taints.add(line)
    return taints

def split_taint_p(taints,inf,cleanf,dirtyf,bitext,lines):
    ntaints = 0
    ncleans = 0
    for line in inf:
        save = copy(line)
        line = line.strip()
        if bitext:
            line = line.split('\t')[bitext-1]
        line.replace(u"\u3000","")
        line.replace(u" ","")
        if line in taints:
            ntaints += 1
            if dirtyf:
                dirtyf.write(save)
            elif not cleanf:
                return ncleans+ntaints, -1, lines
        else:
            ncleans += 1
            if cleanf:
                cleanf.write(save)
        if lines > -1:
            lines += 1
            if lines % 1000000 == 0:
                sys.stderr.write('!')
            elif lines % 100000 == 0:
                sys.stderr.write(':')
            elif lines % 10000 == 0:
                sys.stderr.write(',')
            sys.stderr.flush()
    return ncleans, ntaints, lines

def main(args):
    taint_path = None
    bitext = 0
    source_paths = []
    clean_path = None
    dirty_path = None
    dump = False
    dump_only = False
    quiet = False

    for arg in args:
        if arg == '-n':
            clean_path = None
        elif arg == '-d':
            if dump:
                dump_only = True
            dump = True
        elif arg == '-b1':
            bitext = 1
        elif arg == '-b2':
            bitext = 2
        elif arg == '-q':
            quiet = True
        elif os.access(arg,os.R_OK):
            if taint_path:
                source_paths.append(arg)
            else:
                taint_path = arg
        elif not clean_path:
            clean_path = arg
        elif not dirty_path:
            dirty_path = arg
        else:
            sys.stderr.write('Usage: script [-n|-b1|-b2|-q] TAINT IN* [CLEAN] [DIRTY]\n')
            sys.exit(1)

    if not taint_path:
        sys.stderr.write('No taint path specified.\n')
        sys.exit(1)
    if not source_paths:
        source_paths.append('/dev/stdin')

    taint_set = packed_set(taint_path)
    if dump:
        with open('/dev/stderr','a',encoding='utf-8') as err:
            for t in taint_set:
                err.write(t+"\n")
            err.write('# ' + repr(len(taint_set)) + " taint lines\n");
        if dump_only:
            sys.exit(0)

    cleanf = None
    dirtyf = None
    if clean_path:
        cleanf = open(clean_path,'w',encoding='utf-8')
    if dirty_path:
        dirtyf = open(dirty_path,'w',encoding='utf-8')

    ntainted = 0
    nclean = 0
    total_taint = 0
    total_clean = 0
    lines = -1 if quiet else 0

    for path in source_paths:
        with open(path,'r',encoding='utf-8') as inf:
            cleans, taints, lines = split_taint_p(taint_set,inf,cleanf,dirtyf,bitext,lines)
            if taints < 0:
                ntainted += 1
                sys.stdout.write('taint at '+path+':'+str(cleans)+'\n')
            elif taints == 0:
                nclean += 1
                total_clean += cleans
                if not quiet:
                    sys.stderr.write('clean file '+path+'\n')
            else:
                ntainted += 1
                total_taint += taints
                total_clean += cleans
                if not quiet:
                    sys.stderr.write('taint in '+path+' is '+str(taints)+' vs ' +str(cleans)+' clean lines\n')

    if not cleanf and not dirtyf:
        sys.stdout.write('sum: '+str(ntainted)+' tainted files'+', '+str(nclean)+' clean.\n')
    elif not quiet:
        sys.stderr.write(str(ntainted)+' tainted files, '+str(total_taint)+' lines\n')
        sys.stderr.write(str(nclean)+' clean files, '+str(total_clean)+' lines\n')
                
    return ntainted

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))


