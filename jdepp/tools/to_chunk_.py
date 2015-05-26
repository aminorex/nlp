#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Usage: to_chunk.py [-p, -prob] < in.JDP
#   translate chunker output into human-readable chunked sequences
import sys, re
if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
    sys.exit ("Usage: %s\n  -p, --prob\tshow chunking probability\n  -q, --quiet\tshow only wrongly chunked sentences" % sys.argv[0])
prob   = "-p" in sys.argv[1:] or "--prob"  in sys.argv[1:]
quiet  = "-q" in sys.argv[1:] or "--quiet" in sys.argv[1:]
ignore   = ("-i" in sys.argv[1:] and sys.argv[sys.argv.index ('-i') + 1]) or \
           ("--ignore" in sys.argv[1:] and sys.argv[sys.argv.index ('--ignore') + 1]) or \
            ""

text  = ''
fails = False
bid   = 0
pat_s = re.compile (r'[\t\s]')
pat_c = re.compile (r'^(B|I)@')
for line in iter (sys.stdin.readline, ""): # no buffering
    if line[:7] == '# S-ID:':
        text += line
        bid = 0
    elif ignore and re.match (ignore, line):
        text += line
    elif line == 'EOS\n':
        text += line
        if not quiet or fails:
            sys.stdout.write (text)
            sys.stdout.flush ()
        text  = ""
        fails = False
    elif line[0] == '*':
        flag = True
    else:
        field = pat_s.split (line[:-1])
        surf, (gold, auto) = field[0], field[-2:]
        p = prob and pat_c.match (auto) and "%.2f" % float (auto[2:]) or ""
        if bid > 0:
            if auto[0] == 'B' and gold == 'B':
                text += "│%s " % p # "┃"
            elif auto[0] == 'I' and gold == 'B': # false negative
                text += "\033[36m│%s \033[0m" % p
                fails |= True
            elif auto[0] == 'B' and gold == 'I': # false positive
                text += "\033[31m│%s \033[0m" % p
                fails |= True
            elif flag:
                text += "│%s " % p
        bid += flag and 1 or 0
        flag = False
        text += "%s " % surf
