#! /usr/bin/env python

import sys
import re

page=0
book=0
title=None
ch=0
vs=0
nv=0
ne=0
state=0
lno=0
last_br = 0
last_pb = 0
last_bc = 0
last_cc = 0
last_num = 0
foot = False
lines = []
anchors=[]

def where():
    global title
    global book
    global ch
    global vs
    global page
    global lno
    global lines
    global anchors
    global foot
    tag = 'title:'+title+'; book:'+repr(book)+'; ch:'+repr(ch)+'; vs:'+repr(vs)+'; line:'+repr(lno)
    tag += '; nlines: '+repr(len(lines))+'; nanchors: '+repr(len(anchors))+'; foot='+repr(foot)
    return tag

args = sys.argv[1:]
verbose = 0
while args and args[0] == '-v':
    verbose += 1
    args.pop(0)
 
max_ne = int(args.pop(0)) if args and args[0].isdigit() else 0
prefix = args.pop(0) if args else 'x-'
suffix = args.pop(0) if args else 'txt'
path = 'None'

def make_path(n):
    global prefix
    global suffix
    global path
    path = prefix + ("%02d" % n) + '.' + suffix
    return path

out = sys.stdout
line = ''
verse = ''

def emitter(out,lines,anchors):
    for line in lines:
        for tag in map(repr,anchors):
            line.replace(tag,' ')
            line.replace('  ',' ')
        out.write(line+'\n')
    
while True:
    line = sys.stdin.readline()
    if not line:
        break
    lno += 1

    if line[0] == '\x0c':

        if verse:
            lines.append(verse)
            verse = ''
        if  lines:
            nv += len(lines)
            emitter(out,lines,anchors)
            lines = []
        anchors = []
        foot = False
        last_pb = lno

        title = line.strip()
        if title.find('Testament') == -1:
            if title[-1].isdigit():
                nch = int(title.split()[-1])
                last_num = nch
                if nch != ch and nch != ch + 1 and nch != 1:
                    sys.stderr.write('#title chapter skew: '+repr(nch)+' '+where()+'\n')
                title=title.replace(' ','')
            else:
                title=''.join(title.split())
                book += 1
                ch = 0
                out = open(make_path(book),'w')
                last_bc = lno
                sys.stderr.write('### open '+path+' '+title+'\n')
        continue
    
    lead_sp = line[0].isspace()    
    line = line.strip()
    if not line:
        last_br = lno
        continue

    if line[:8] == 'Chapter ':
        nch = int(line[8:])
        last_num = nch
        if nch != ch + 1 and nch != 1:
            sys.stderr.write('#chapter sequence: '+repr(nch)+' '+where()+'\n')
        else:
            ch = nch
            vs = 0
            last_cc = lno
        continue    

    if line[0].isdigit():
        try: 
            nvs = int(line.split()[0])
        except:
            if verbose:
                sys.stderr.write('# skip non-int digit: '+line.split()[0]+' '+where()+'\n')
            continue
        last_num = nvs

        if page == 0:
            page = nvs
            if verbose:
                sys.stderr.write('# set page 1: '+repr(nvs)+' '+where()+'\n')
            continue

        if last_cc == lno - 1 and nvs != 1:
            if verbose:
                sys.stderr.write('# skip bare anchor: '+repr(nvs)+' '+where()+'\n')
                sys.stderr.write(repr((last_br, lno, last_num, page))+'\n')                
            continue

        if last_num == page + 1:
            page = last_num
            if verbose:
                sys.stderr.write('# set page 2: '+repr(last_num)+' '+where()+'\n')
            continue

        if last_br == lno - 1 and nvs != vs + 1:
            foot = True
            anchors.append(nvs)
            if verbose > 0:
                sys.stderr.write('#foot sequence: '+repr(nvs)+' '+where()+'\n')
                sys.stderr.write(repr((last_br, lno, last_num, page))+'\n')
        elif nvs == vs + 1 and not foot:
            if verbose > 1:
                sys.stderr.write('# vs 1: '+repr(nvs)+' '+where()+'\n')
            vs = nvs
            if verse:
                lines.append(verse)
                verse = ''
        elif nvs <= vs and not foot: 
            pass
        elif foot:
            anchors.append(nvs)
        elif nvs > vs:
            if verbose > 1:
                sys.stderr.write('# vs 2: '+repr(nvs)+' '+where()+'\n')
            if verse:
                span = nvs - vs
                if span > 1 and span < 4:
                    ndots = verse.count('.')
                    if ndots > 1 and ndots <= span:
                        for vv in verse.split('.'):
                            vv = vv.strip()
                            if vv:
                                lines.append(vv+'.')
                        verse = ''
                if verse:
                    lines.append(verse)
                verse = ''
            vs = nvs
        else:
            sys.stderr.write('# unknown: '+repr(nvs)+' '+where()+'\n')
            sys.exit(1)

        continue

    if foot:
        continue

    if vs == 0 or ch == 0 or last_br == lno:
        continue

    if lead_sp:
        if verse:
            verse += ' / '
        else:
            verse = ' '
    if verse and verse[-1] != ' ':
        verse += ' ' + line
    else:
        verse += line

if verse:
    lines.append(verse)
if lines:
    nv += len(lines)
    emitter(out,lines,anchors)

sys.stderr.write('extracted '+str(nv)+' verses in '+str(lno)+' lines with '+str(ne)+' errors'+"\n")
sys.exit(0)


    
