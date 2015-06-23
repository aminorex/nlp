#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# tokenizer for wat2014-based experiments
# $0 en is the default english
# $0 ja is the default japanese
#
# defaults are for travatar wat2014
# options are for experiments, repair operations
#

import os
import sys
import re
import time
from pexpect import spawn
from unicodedata import category, normalize
from jctconv import h2z,z2h
 
luser = os.getenv('USER')
lhome = os.getenv('HOME')

ja_top=os.getenv('JA_HOME')
if not ja_top:
    if os.path.isdir(lhome+'/u/ja/.'):
        ja_top = lhome + '/u/ja'
    else:
        ja_top='/bb/news/translation/users/'+luser+'/ja'

tool_top=os.getenv('JA_TOOL')
if not tool_top:
    tool_top = ja_top +'/wat2014/tools/.'

na_tool=os.getenv('NA_TOOL')
if not na_tool:
    na_tool = '/bb/news/analytics/tools'
    if not os.path.isdir(na_tool):
        na_tool = '/usr/local'

td=os.getenv('TRAVATAR')
if not td:
    td = tool_top + '/travatar'

kd=os.getenv('KYTEA')
if not kd:
    kd = tool_top + '/kytea'
    if not os.path.isdir(kd):
        kd = na_tool+'/share/kytea'

md=os.getenv('MECAB')
if not md:
    md = na_tool + '/bin'

train=ja_top+'/wat2014/ja-en/preproc/train'
casemodel=train+'/truecaser/en.truecaser'
kyteamodel=kd+'/data/model.bin'

# how to normalize unicode
normalization='NFC'

quiet=False
verbose=0

# whether to break as bunsetsu
bunsetsu=False
# whether to keep spaces between ascii
keepintera=True
# whether to keep spaces between non-ascii
keepinterx=False
# whether to filter control characters and meta sequences
metafilter=True
# whether to insure escape tokens are separated
pipefilter=True
# whether to fix broken escape tokens before pipefilter
unbreak = False
# whether to remove spaces subject to -a, -k
despacing = False
# whether to truecase 
truecase=True
# whether to downcase
lowercase=False
# whether to widen narrow kana,ascii,syms
widecase=False
# whether to narrow wide kana,ascii,syms
narrowcase=False
# to which cases the wide/narrow operation applies
jctkana=False
jctalpha=False
jctsym=False
# characters which force a token split
split='(-|\\/)'

lang='en'

def jctopts(str,default):
    ni = 0
    ns = len(str)
    kana = default
    alpha = default
    sym = default
    while ni < ns and str[ni] in [ 'k', 'a', 'n' ]:
        if str[ni] == 'k':
            kana = not kana
        elif str[ni] == 'a':
            alpha = not alpha
        elif str[ni] == 'n':
            sym = not sym
        ni += 1
    return kana, alpha, sym, ni
        

for arg in sys.argv[1:]:
    if arg[0] == '-':
        while arg[0] == '-':
            arg = arg[1:]
        ii = 0
        while ii < len(arg):
            cc = arg[ii]
            if cc == 'c':
                truecase = False
                narrowcase = False
                widecase = False
                lowercase = False
                jctkana = False
                jctalpha = False
                jctsym = False
            elif cc == 'a':
                keepintera = False
            elif cc == 'B':
                bunsetsu = True
            elif cc == 'd':
                despacing = False
            elif cc == 'D':
                despacing = True
            elif cc == 'K':
                keepinterx = True
            elif cc == 'L':
                lowercase = True
            elif cc == 'm':
                metafilter = False
            elif cc == 'p':
                pipefilter = False
            elif cc == 'q':
                quiet = True
            elif cc == 'n':
                normalization = False
            elif cc == 'N':
                narrowcase = True
                jctkana, jctalpa, jctsym = jctopts(arg[ii+1:],True)
            elif cc == 's':
                split = False
            elif cc == 't':
                truecase = False
            elif cc == 'T':
                truecase = True
            elif cc == 'U':
                unbreak = True
            elif cc == 'v':
                verbose += 1
            elif cc == 'w':
                jctkana, jctalpha, jctsym, ni = jctopts(arg[ii+1:],False)
                widecase = jctkana or jctalpha or jctsym
                ii += ni
            elif cc == 'W':
                widecase = True
                jctkana, jctalpha, jctsym, ni = jctopts(arg[ii+1:],True)                
                ii += ni
            else:
                sys.stderr.write(sys.argv[0]+': Unknown option "'+cc+'"\n')
                sys.exit(1)
            ii += 1
    elif arg.lower() == 'nfc' or arg.lower() == 'c' or arg.lower() == 'nfd' or arg.lower() == 'd':
        narg = 'NF'+arg[-1].upper()
    elif arg.lower() == 'nfkc' or arg.lower() == 'kc' or arg.lower() == 'nfkd' or arg.lower() == 'kd':
        narg = 'NF'+arg[-2:].upper()
    elif arg[-4:] == '.tcm':
        casemodel = arg
    elif arg[:2] == 'ja':
        lang=arg
        despacing = True
        truecase = False
        lowercase = False
        widecase = True
        jctkana = True
        jctalpha = True
        jctsym = True
        narrowcase = False
        split = False
        if arg[-1] == '.b':
            bunsetsu=True
    elif arg == 'en':
        lang=arg
        despacing = False
        truecase = True
        lowercase = False
        widecase = False
        narrowcase = True
        jctkana = True
        jctalpha = True
        jctsym = True
    else:
        sys.stderr.write(sys.argv[0]+': Bad argument "'+arg+'"\n')
        sys.exit(1)

lowercaser=td+'/script/tree/lowercase.pl'
truecaser=td+'/script/recaser/truecase.pl'
converter=td+'/src/bin/tree-converter -input_format word -output_format word'

# select tokenizer
if lang == 'en':
    tokenizer = os.getenv("TOKENIZER")
    if not tokenizer:
        tokenizer = td + '/src/bin/tokenizer'
        if truecase:
            truecaser += " --model " + casemodel
    elif truecase:
        sys.stderr.write("truecasing undefined for environment TOKENIZER\n");
        sys.exit(1)
elif lang == 'ja':
    if bunsetsu:
        tokenizer = md + '/mecab -Owakati'
    else:
        tokenizer = kd + '/src/bin/kytea -wsconst D -notags -model ' + kyteamodel
    
# high unicode meta characters to be converted to whitespace:
# 00A0 = nbsp
# 00AD = soft hyphen
# 2008 = zero-width space
# 200C = zero-width non-joiner
# 200D = zero-width joiner
# 2028 = high unicode line separator
# 2060 = word join
# 3000 = high unicode whitespace
# FEFF = native-endian byte order mark
# FFFE = other-endian byte order mark
# FEFE = uniformly bad ucs-2
x_whit = re.compile(ur'([\r\t]|\\[rnt]|  |'+unichr(0x2028)+'|'+unichr(0x3000)+'|'+unichr(0xFEFE)+'|'+unichr(0xFEFF)+'|'+unichr(0xFFFE)+'|\{#\}|\|\|\|)+')
x_null = re.compile(ur''+unichr(0x00A0)+'|'+unichr(0x00AD)+'|'+unichr(0x2008)+'|'+unichr(0x200C)+'|'+unichr(0x200D)+'|'+unichr(0x2060))
x_pipe = re.compile(ur'(__[a-z][a-z]*__)')
x_unbr = re.compile(ur' __ ([ocp][bracketpin]*__) __ ')

def despace(line):
    if not keepintera or keepinterx:
        line = line.replace(u' ',u'').replace(u'、',u'，')
    else:
        tmps = u''
        pcat = None
        pending = False
        for ii in range(0,len(line)):
            uch = line[ii]
            if uch == u'、':
                uch = u'，'
            tcat = category(uch)
            if tcat[0] == 'Z':
                pending = pcat is not None
                continue
            if not pending or pcat[0] != 'L' or tcat[0] != 'L':
                pass
            elif keepintera and pcat[1] in [ 'u', 'l' ] and tcat[1] in [ 'u', 'l' ]:
                tmps += u' '
            elif keepinterx:
                tmps += u' '
            pcat = tcat
            tmps += uch
            pending = False
        line = tmps
    return line

# converter pexpect
if split:
    converter += ' -split "'+split+'"'
pcon = spawn("/bin/bash -c '"+converter+" 2>/dev/null'")
if verbose:
    sys.stderr.write('spawned: '+converter+'\n')
pcon.setecho(False)

# caser pexpect
if truecase:
    pcas = spawn("/bin/bash -c '"+truecaser+" 2>/dev/null'")
    pcas.setecho(False)
    if verbose:
        sys.stderr.write('spawned: '+truecaser+'\n')
elif lowercase:
    pcas = spawn("/bin/bash -c '"+lowercaser+" 2>/dev/null'")
    if verbose:
        sys.stderr.write('spawned: '+lowercaser+'\n')
    pcas.setecho(False)
else:
    pcas = False
    
# tokenizer pexpect
ptok = spawn("/bin/bash -c '"+tokenizer+" 2>/dev/null'")
if verbose:
    sys.stderr.write('spawned: '+tokenizer+'\n')
ptok.setecho(False)

if not quiet:
    sys.stderr.write('commandline: '+' '.join(sys.argv)+"\n");
if verbose:
    sys.stderr.write('tokenizer: '+tokenizer+"\n");
    sys.stderr.write('converter: '+converter+"\n")
    sys.stderr.write('caser: '+(truecaser if truecase else (lowercaser if lowercase else 'None'))+"\n")

lno = 0
while True:
    line = sys.stdin.readline()
    if not line:
        if verbose:
            sys.stderr.write('EOF input after line '+repr(lno)+"\n")
        break
    lno += 1
    if not quiet and lno % 100000 == 0:
        sys.stderr.write('.')
        sys.stderr.flush()

    # initial processing using python libraries:
    line = line.strip().decode('utf-8','replace')
    if verbose>1:
        sys.stderr.write('text '+repr(lno)+": "+line.encode('utf-8')+"\n");

    if normalization:
        line = normalize(normalization,line)
        if verbose>1:
            sys.stderr.write('normal '+repr(lno)+": "+line.encode('utf-8')+"\n");

    if pipefilter:
        if unbreak:
            # fix broken pipe escapes
            line = re.sub(x_unbr,r' __\1__ ',line)
        # isolate pipe escapes
        line = re.sub(x_pipe,r' \1 ',line)
        if verbose>1:
            sys.stderr.write('pipe '+repr(lno)+": "+line.encode('utf-8')+"\n");

    if metafilter:
        # normalize to white space
        line = re.sub(x_whit,r' ',line)
        if verbose>1:
            sys.stderr.write('whit '+repr(lno)+": "+line.encode('utf-8')+"\n");
        # normalize to null
        line = re.sub(x_null,r'',line)
        if verbose>1:
            sys.stderr.write('null '+repr(lno)+": "+line.encode('utf-8')+"\n");

    if despacing:
        # e.g. use case: before japanese tokenization, remove suspect white space
        # note that wide comma normalization occurs here
        despace(line)
        if verbose>1:
            sys.stderr.write('despace '+repr(lno)+": "+line.encode('utf-8')+"\n");

    if widecase:
        # wide-casing for specified classes
        line = h2z(line,kana=jctkana,digit=jctsym,ascii=jctalpha)
        if verbose>1:
            sys.stderr.write('wide '+repr(lno)+": "+line.encode('utf-8')+"\n");

    if narrowcase:
        # narrow-casing for specified classes
        line = z2h(line,kana=jctkana,digit=jctsym,ascii=jctalpha)
        if verbose>1:
            sys.stderr.write('narrow '+repr(lno)+": "+line.encode('utf-8')+"\n");


    # tokenize using pipe
    
    ptok.sendline(line.encode('utf-8'))
    if verbose>1:
        sys.stderr.write('reading...\n')
    line = ptok.readline()
    if not line:
        sys.stderr.write('tokenizer EOF unexpected at line '+repr(lno)+"\n")
        break
    if verbose>1:
        sys.stderr.write('tokenized '+repr(lno)+": "+line);

    # convert using pipe
    pcon.sendline(re.sub(x_whit,r' ',line.strip()))
    line = pcon.readline()
    if not line:
        sys.stderr.write('converter EOF unexpected at line '+repr(lno)+"\n")
        break
    if verbose>1:
        sys.stderr.write('converted '+repr(lno)+": "+repr(line)+"\n");

    # casing using pipe
    if pcas:
        pcas.sendline(line)
        line = pcas.readline()
        if not line:
            sys.stderr.write('recaser EOF unexpected at line '+repr(lno)+"\n")
            break
        if verbose>1:
            sys.stderr.write('converted '+repr(lno)+": "+line+"\n");

    # output
    sys.stdout.write(line.strip()+"\n")

ptok.sendeof()
pcon.sendeof()
if pcas:
    pcas.sendeof()

if not quiet:
    if lno > 99999:
        sys.stderr.write("\n")
    sys.stderr.write(repr(lno)+" lines\n")

sys.exit(0)
