#!/usr/bin/env python
import sys, re, pecco

timer = pecco.Timer ("pecco", "classify")
opt   = pecco.option (len (sys.argv), sys.argv)
c     = pecco.kernel_model (opt)
c.load (opt.model);

pp, np, pn, nn = 0, 0, 0, 0
for line in open (opt.test):
    m = re.match (r'(\S+) ', line)
    if m:
        label, fstr = m.group (1), line[m.end ():-1]
        timer.startTimer ()
        fv = [int (x[:-2]) for x in fstr.split(' ')]
        sign = c.binClassify (fv)
        margin = 0
        timer.stopTimer ()
        if label == "+1":
            if sign: pp += 1
            else:    pn += 1
        else:
            if sign: np += 1
            else:    nn += 1

sys.stderr.write ("acc. %.4f (pp %d) (pn %d) (np %d) (nn %d)\n" % \
                      ((pp + nn) * 1.0 / (pp + pn + np + nn), pp, pn, np, nn))

timer.printElapsed ();
