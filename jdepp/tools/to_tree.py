#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: to_tree.py [-p, -prob] < in.JDP
#   translate parser output into human-readable dependency tree structure
import sys, re, os
from unicodedata import east_asian_width as width

if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
    sys.exit ("Usage: %s\n  -v, --verbose\tshow lattice output as well\n  -p, --prob\tshow dependency probability\n  -i, --ignore STR\tignore line starting with STR\n  -q, --quiet\tshow only wrongly parsed sentences" % sys.argv[0])
verbose  = "-v" in sys.argv[1:] or "--verbose"  in sys.argv[1:]
prob     = "-p" in sys.argv[1:] or "--prob"     in sys.argv[1:]
quiet    = "-q" in sys.argv[1:] or "--quiet"    in sys.argv[1:]
ignore   = ("-i" in sys.argv[1:] and sys.argv[sys.argv.index ('-i') + 1]) or \
           ("--ignore" in sys.argv[1:] and sys.argv[sys.argv.index ('--ignore') + 1]) or \
            ""

# customizable parameters
indent = prob and 4 or 3 # for one dependency arc
offset = 2               # offset from the left

def set_charset (data): # input coding
    for codec in ['shift_jis','utf-8','euc_jp','iso2022-jp']:
        try:
            data.decode (codec)
            return codec
        except:
            continue;
    else:
        sys.exit ("to_tree.py: cannot decide input coding.")

class Binfo:
    """ bunsetsu infomation """
    def __init__ (self, *args):
        self.id, self.head, self.prob, self.fail, self.gold = args
        self.morph, self.len, self.depth, self.first_child = "", 0, 0, -1
    def str    (self)         : return self.morph + (self.len % 2 and " " or "")
    def width  (self)         : return (self.len + 1) / 2;
    def offset (self, offset) : return offset - self.width () - self.depth

def treeify (binfo):
    tree = ''
    for c in reversed (binfo[:-1]):
        c.depth = binfo[c.head].depth + indent
        binfo[c.head].first_child = c.id
    width = offset + max (b.width () + b.depth for b in binfo) # tree width
    for b in binfo:
        if b.head == -1:
            if b.id != len (binfo) - 1:
                sys.exit ("no head information; chunking output [-I 1]?")
            tree += "% 3d:%s%s" % (b.id, "　" * b.offset (width), b.str ())
        else:
            if b.fail:
                tree += b.head > int (b.gold[:-1]) and "\033[31m" or "\033[36m"
            tree += "% 3d:%s%s" % (b.id, "　" * b.offset (width), b.str ())
            h = binfo[b.head]
            tree += "━" * (b.depth - h.depth - (b.prob and 3 or 1))
            tree += b.prob # "─"
            tree += b.id == h.first_child and "┓" or "┫" # "┐" or "┤"
            tree += b.fail and "%-4s\033[0m" % b.gold or ""
            while h.head != -1: # draw arcs spanning from x < b to y > h
                c, h = h, binfo[h.head]
                tree += "　" * (c.depth - h.depth - (b.fail and 3 or 1))
                tree += h.first_child < b.id and "┃" or "　" # "│" or "　" 
                b.fail = False
            tree += "\n"
    return tree

binfo   = []
header  = ''
text    = ''
charset = ''
wrong   = False
pat_s = re.compile (r'[\t\s]')
pat_i = re.compile (re.escape (ignore))
tag = set (["D", "A", "P", "I"])
ww ={'Na':1, 'W':2, 'F':2, 'H':1, 'A':2, 'N':1}
for line in iter (sys.stdin.readline, ""): # no buffering
    if verbose:
        sys.stdout.write (line)
    if line[:7] == '# S-ID:' or (ignore and pat_i.match (line)):
        header += line
    elif line[:-1] == 'EOS': # EOS
        if not charset: # set charset
            charset = set_charset (text)
        if charset != 'utf-8':
            text = text.decode (charset).encode ('utf-8')
        for line_ in text[:-1].split ('\n'):
            if line_[0] == '*':
                gold, auto = line_[2:].split (' ', 3)[-2:] # [1:3]
                p = ""
                pos = auto.find ('@')
                if pos != -1:
                    if prob: p = "%.2f" % float (auto[pos + 1:])
                    auto = auto[:pos]
                fail = gold[-1] in tag and auto[:-1] != gold[:-1]
                wrong |= fail
                binfo.append (Binfo (len (binfo), int (auto[:-1]), p, fail, gold))
            else:
                binfo[-1].morph += pat_s.split (line_, 1)[0]
        for b in binfo:
            b.len = sum (ww[width (x)] for x in unicode (b.morph, 'utf-8'))
        if not quiet or wrong:
            text = treeify (binfo)
            if charset != 'utf-8':
                text = text.decode ('utf-8').encode (charset)
            sys.stdout.write (header)
            sys.stdout.write (text)
            sys.stdout.write (line)
            sys.stdout.flush ()
        binfo[:] = []
        header = ""
        text  = ""
        wrong = False
    else:
        text += line
