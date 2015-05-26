#!/usr/bin/env python
# Usage: replace_pos.py path_to_tagger [tagger_options] < in.KNP > out.JDP
#   replace gold POS in Kyoto Univ. Text Corpus w/ auto POS given by POS tagger
#   * you may want to set tagger_options for MeCab to '-d your_target_dict'
#
#   NOTE: the below code is free from mecab-python module
import sys, re, subprocess, tempfile

if len (sys.argv) < 2:
    sys.exit ("Usage: %s tagger_command [tagger_options] < in.KNP > out.JDP"
              % (sys.argv[0], sys.argv[0]))

# identify charset of tagger input/output
charset = 'utf-8'
dummy = subprocess.Popen ('echo "X" | %s' % ' '.join (sys.argv[1:]), shell=True, stdout=subprocess.PIPE).communicate ()[0]
for codec in ['shift_jis','utf-8','euc_jp','iso2022-jp']:
    try:
        dummy.decode (codec)
        charset = codec
        break
    except:
        continue;
else:
    sys.exit ("replace_pos.py: cannot decide input coding.")

corpus  = []

header  = sent =''
bpos    = [] # id -> start position of gold bunsetsu
hi      = [] # id -> head id
ht      = [] # id -> dependency type
stat    = { 'success': 0, 'failed': 0 }
error   = False
convert = charset != 'euc_jp'

raw    = tempfile.TemporaryFile ()
for line in sys.stdin:
    if not error and convert: # decode appropriately
        try:
            line = line.decode ('euc_jp').encode (charset)
        except:
            sys.stderr.write ("failed to decode: %s" % line)
            error = True
            continue
    if line[:-1] == 'EOS': # EOS
        if error:
            stat['failed'] += 1
            error = False
        else:
            raw.write (sent + "\n")
            bpos.append (len (sent)) # dummy
            corpus.append ([header, bpos, hi, ht])
        header = sent = ''
        bpos, hi, ht = [], [], []
    elif not error:
        if line[0] == '#':
            header = line
        elif line[0] == '*':
            h = line[:-1].split (' ')[2]
            bpos.append (len (sent))
            hi.append (int (h[:-1]))
            ht.append (h[-1])
        else:
            sent += line.split (' ')[0] # surface

raw.seek (0)
tagged = iter (subprocess.Popen (sys.argv[1:], stdin=raw, stdout=subprocess.PIPE).communicate ()[0].splitlines ())

pat = re.compile (r'[\s\t]')
for header, bpos, hi, ht in corpus:
    i = offset = 0
    cgold, cauto, bi, result = [], [], [], []
    for m in tagged:
        while offset > bpos[i]:
            bi.append (len (cgold) - 1)
            cgold[-1].append (i)
            i += 1
        if m == "EOS":
            break
        if offset == bpos[i]:
            bi.append (len (cgold))
            cgold.append ([i])
            cauto.append ([m])
            i += 1
        elif offset < bpos[i]:
            cauto[-1].append (m)
        offset += len (pat.split (m, 1)[0])
    for i, cs in enumerate (cgold):
        h_ = hi[cs[-1]]
        if i == len (cgold) - 1:
            result.append ("* %d -1%s" % (i, ht[cs[-1]]))
        else:
            if len (cs) > 1:
                # discard compounded bunsetsu with multiple heads
                if len (set (bi[hi[x]]
                             for x in cs if bi[hi[x]] != bi[h_])) >= 2:
                    stat['failed'] += 1
                    sys.stderr.write ("multiple heads: %s\n" % header)
                    break
            result.append ("* %d %d%s" % (i, bi[h_], ht[cs[-1]]))
        result.extend (cauto[i])
    else:
        output = header + '\n'.join (result) + '\nEOS\n'
        try:
            if convert:
                output = output.decode (charset).encode ('euc_jp', 'replace')
        except:
            stat['failed'] += 1
            sys.stderr.write ("failed to decode: %s" % header)
        else:
            stat['success'] += 1
            sys.stdout.write (output)

sys.stderr.write ("(success, failed) = (%d, %d)\n"
                  % (stat['success'], stat['failed']))
