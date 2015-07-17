#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import urllib
import urllib2
import codecs
import re
from HTMLParser import HTMLParser

def translate(text, twitter=False, to_language="auto", from_language="auto", tag=''):
    '''Return the translation using google translate'''
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    if twitter: # code for handling username/hashtag capture
        username = re.compile(r'(@ _ .+?\b|@ .+? _\b|@ \S+?\b) ')
        hashtag = re.compile(r'(# \S+?\b)', re.U)
        usrs = re.findall(username, text)
        tags = re.findall(hashtag, text)
        if len(usrs) > 0:
            for i in range(0, len(usrs)-1):
                sys.stderr.write('Username ' + str(i) + ': ' + usrs[i] + '\n')
                text = text.replace(usrs[i], '@'+str(i))
            sys.stderr.write(text + '\n')
        else:
            sys.stderr.write('No usernames found on line: ' + text + '\n')
        if len(tags) > 0:
            for i in range(0, len(tags)-1):
                sys.stderr.write('Hashtag ' + str(i) + ': ' + tags[i] + '\n')
#                text = text.replace(tags[i], '#'+str(i))
            sys.stderr.write(text + '\n')

    line = text.decode('utf-8').strip()
    line = map(lambda x: '_' if ord(x) > 0xfff0 else x, line)
    text = u''.join(line)
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_language, from_language, urllib.quote_plus(text.encode('utf-8')))
    if tag:
        sys.stderr.write(tag+':: '+link+"\n")
    request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    if twitter and len(usrs) > 0:
        for i in range(0, len(usrs)-1):
            result.replace('@'+str(i), usrs[i].replace(' ', ''))
    if twitter and len(tags) > 0:
        for i in range(0, len(usrs)-1):
            result.replace('#'+str(i), tags[i].replace(' ', ''))
    return result

if __name__ == '__main__':
    lin = ''
    lout = ''
    verbosity = 0
    prog = sys.argv[0]
    start=0
    end=0
    twitter = False # twitter behavior control

    parser = argparse.ArgumentParser(description="Will run all (or specified) lines of stdin through Google Translate with source and target languages specified, then output the result to stdout.")
    parser.add_argument('-v', '--verbosity', action='count', help='Increases verbosity of output.')
    parser.add_argument('-t', '--twitter', action='store_true', help='Enables Twitter-specific behavior.')
    parser.add_argument('-i', '--infile', help='Source file path.')
    parser.add_argument('-o', '--outfile', help='Target file path.')
    parser.add_argument('-s', '--start', type=int, help='Starting target (line number).')
    parser.add_argument('-e', '--end', type=int, help='Ending target (line number).')
    parser.add_argument('lin', help='Input language (ISO639-3 code)')
    parser.add_argument('lout', help='Output language (ISO639-3 code)')
    args = parser.parse_args()
    
    if args.start and not args.end:
        sys.stderr.write(prog+': Start line given without end line.\n')
        sys.exit(1)
    if args.end and not args.start:
        sys.stderr.write(prog+': End line given without start line.\n')
        sys.exit(1)
    if args.start or args.end:
        start = args.start
        end = args.end

    if args.twitter:
        twitter = True

    if args.infile:
        fin = codecs.open(args.infile,encoding='utf-8')
    else:
        fin = sys.stdin
    if args.outfile:
        fout = codecs.open(args.outfile,'w',encoding='utf-8')
    else:
        fout = sys.stdout

    if args.verbosity:
        verbosity = args.verbosity
        sys.stderr.write(prog+': from '+lin+' to '+lout+"\n")

    lin = args.lin
    lout = args.lout

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
            if twitter:
                h = HTMLParser()
                line = line.decode('utf-8')
                line = h.unescape(line)
                line = line.encode('utf-8')
                line = line.replace('@-@','-')
                text = translate(line,twitter=True,to_language=lout,from_language=lin,tag=(repr(nlines) if verbosity > 1 else ''))
            else:
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





















