#! /usr/bin/env python
import sys

args=[]
pstart,pend=0,1
quiet=False
for arg in sys.argv[1:]:
    if arg == '-q':
        quiet = True
        continue
    for carg in arg.split(','):
        parts = carg.split('-') if '-' in carg else carg.split(':')
        start = 1 if not parts[0] else int(parts[0])
        stride = 1 if len(parts) < 3 or not parts[2] else int(parts[2])
        end = start if len(parts) < 2 else 0 if not parts[1] else int(parts[1])
        if start <= pstart or not pend:
            sys.stderr.write('overlapping range '+carg+"\n");
            sys.exit(1)
        if (end and end < start) or stride < 1:
            sys.stderr.write('malformed range '+carg+"\n");
            sys.exit(1)
        pstart,pend=start,end
        args.append((start,end,stride))
args.sort()

lno=0
nout=0
sys.stderr.write(repr(args)+"\n")
start,end,stride = args.pop(0) if args else (1,0,1)
for line in sys.stdin:
    #print start,end,stride
    lno += 1
    if end and lno > end:
        if not args:
            #print 'break',lno,end
            break
        start,end,stride=args.pop(0)
        sys.stderr.write(repr((start,end,stride))+"\n")
    if lno >= start and (not end or lno <= end):
        if lno == start:
            start += stride
        print line.strip()
        nout += 1
    else:
        #print 'skip',lno,start,end
        pass
    
print nout,'of',lno,'passed'
sys.exit(0)
