#! /usr/bin/env python
import sys
import os

inpaths = []
verbosity = 0
chunklines=1000000

for arg in sys.argv[1:]:
    if arg[0] == '-':
        if arg[1] == 'v':
            verbosity += 1
        else:
            print 'Unknown option:',arg
            sys.exit(1)
    else:
        print 'Use stdin at ',arg
        sys.exit(1)

base=os.getenv('TMPDIR')
if base[-1] != '/':
    base += '/'
pid=os.getpid()
base += 'dedupe-'+repr(pid)+'.'

def output_temp(lines,fno):
    global base
    path = base+repr(fno)
    outf = open(path,'w')
    lines.sort()
    lno = 0
    try:
        for line in lines:
            lno += 1
            outf.write(line)
    except:
        print 'Failed writing',path,'line',lno
        return False
    return True
        
def del_temp(fno):
    global base
    path = base+repr(fno)
    try:
        return os.unlink(path)
    except:
        return False

for path in [ '/dev/stdin' ]:
    lines=[]
    lno = 0
    ono = 0
    inf = open(path,'r')

    tno = 0
    for line in inf:
        lines.append(line)
        lno += 1
        tno += 1
        if tno >= chunklines:
            if not output_temp(lines,ono):
                map(del_temp,xrange(0,ono+1))
                sys.exit(1)
            lines = []
            ono += 1
            tno = 0

    if lines and not output_temp(lines,ono):
        map(del_temp,xrange(0,ono+1))
    elif lines:
        ono += 1
    lines = []
    inf.close()

fps = []
for tno in xrange(0,ono):
    try:
        fps.append(open(base+repr(tno),'r'))
    except:
        sys.stderr.write('Error opening '+base+repr(tno)+"\n")
        map(del_temp,xrange(0,ono))
        sys.exit(1)

flast = [None] * len(fps)
seq = range(0,len(fps))
nlout = 0
ndupe = 0
opath='/dev/stdin'
fout=sys.stdout
nerr = 0
prev = None

while seq:
    remov = set()
    minpos = -1
    minval = None
    for pos in seq:
        if not flast[pos]:
            flast[pos] = fps[pos].readline()
        if not flast[pos]:
            fps[pos].close()
            del_temp(pos)
            remov.add(pos)
            continue
        if minpos < 0:
            minpos = pos
            minval = flast[pos]
        elif minval > flast[pos]:
            minpos = pos
            minval = flast[pos]
    if remov:
        seq = filter(lambda x: not x in remov,seq)
    if prev and minval == prev:
        flast[minpos] = None
        ndupe += 1
        continue
    try:
        prev = flast[minpos]
        flast[minpos] = None
        nlout += 1
        if minval[-1] != "\n":
            minval += "\n"
        fout.write(minval)
    except:
        print 'Error writing line',nlout,'to file',opath
        nerr += 1
        break

sys.stderr.write(repr(nlout)+' lines written to '+opath+' after removing '+repr(ndupe)+" duplicates\n")
map(del_temp,xrange(0,ono))
if nerr:
    sys.stderr.write(repr(nerr)+' errors.'+"\n")
    sys.exit(1)

sys.exit(0)

        



                
