#! /usr/bin/env python
import sys
import codecs
import unicodedata
normalization='NFC'
if len(sys.argv) > 1:
    if sys.argv[1][0] == 'n':
        normalization = sys.argv[1].upper()
    elif sys.argv[1][0] == 'N':
        normalization = sys.argv[1]
    else:
        sys.stderr.write(sys.argv[0]+': Bad argument '+sys.argv[1]+"\n")
        sys.exit(1)
(utf8_encode, utf8_decode, utf8_reader, utf8_writer) = codecs.lookup('utf-8')
outfile=utf8_writer(sys.stdout)
infile=utf8_reader(sys.stdin)
for line in infile:
    outfile.write(unicodedata.normalize(normalization,line))
sys.exit(0)
