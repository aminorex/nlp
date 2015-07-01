#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2
import codecs

def translate(text, to_language="auto", from_language="auto", tag=''):
    '''Return the translation using google translate'''
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_language, from_language, urllib.quote_plus(text.encode('utf-8')))
    if tag:
        sys.stderr.write(tag+':: '+link+"\n")
    request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return result

if __name__ == '__main__':
    lin = ''
    lout = ''
    verbosity = 0
    prog = sys.argv[0]
    start=0
    end=0
    iarg = 1

    # parse flags and line ranges
    while iarg < len(sys.argv):
        if sys.argv[iarg][0] == '-':
            if sys.argv[iarg][1] == 'v':
                verbosity += 1
            elif str.isdigit(sys.argv[iarg][1:]):
                if start:
                    end=int(sys.argv[iarg][1:])
                else:
                    start=int(sys.argv[iarg][1:])
        elif str.isdigit(sys.argv[iarg]):
            if start:
                end=int(sys.argv[iarg])
            else:
                start=int(sys.argv[iarg])
        else:
            break
        iarg += 1

    if len(sys.argv) < iarg + 2:
        sys.stderr.write(prog+': Require I1 and I2 input and output iso639-3 codes' + "\n");
        sys.exit(1)

    # input language
    if len(sys.argv[iarg]) == 2:
        lin = sys.argv[iarg]
        iarg += 1
    else:
        sys.stderr.write(prog+': Invalid input language '+sys.argv[iarg]+"\n");
        sys.exit(1)

    # output language
    if len(sys.argv[iarg]) == 2 and iarg < len(sys.argv):
        lout = sys.argv[iarg]
        iarg += 1
    else:
        sys.stderr.write(prog+': Invalid output language '+sys.argv[iarg]+"\n");
        sys.exit(1)

    # input,output files
    nfiles = len(sys.argv) - iarg
    if nfiles > 2:
        sys.stderr.write(prog,': only two paths allowed, input and output'+"\n")
        sys.exit(1)
    if nfiles > 0:
        fin = codecs.open(sys.argv[iarg],encoding='utf-8')
        iarg += 1
    else:
        fin = sys.stdin
    if nfiles > 1:
        fout = codecs.open(sys.argv[iarg],'w',encoding='utf-8')
        iarg += 1
    else:
        fout = sys.stdout

    if verbosity:
        sys.stderr.write(prog+': from '+lin+' to '+lout+"\n")

    # translation loop
    nlines = 0
    for line in fin:
        try:
            nlines += 1
            line.strip()
            if start > nlines:
                continue
            elif end and end < nlines:
                break
            text = translate(line,to_language=lout,from_language=lin,tag=(repr(nlines) if verbosity > 1 else ''))
            fout.write(text+"\n")
        except:
            ty,ob,tr = sys.exc_info()
            sys.stderr.write(repr(ty)+" at line " + repr(nlines)+"\n");
            sys.stderr.write(repr(ob)+"\n")
            sys.excepthook(ty,ob,tr)
            sys.exit(1)

    if verbosity:
        sys.stderr.write(repr(nlines)+" lines translated\n")

    sys.exit(0)





















