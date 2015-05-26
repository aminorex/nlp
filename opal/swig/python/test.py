#!/usr/bin/env python
import sys, re, opal

opt   = opal.option (len (sys.argv), sys.argv)

timer = opal.Timer ("train")
m = opal.Model (opt)

timer.startTimer ()
m.train_from_file (opt.train, opt.iter, opt.test if opt.output == 1 else "")
m.save (opt.model)
timer.stopTimer ()

timer.printElapsed ()

timer = opal.Timer ("test")
m = opal.Model (opt)
m.load (opt.model)

timer.startTimer ()
# m.test_on_file (opt.test, opt.output)
corr   = 0
incorr = 0
for line in open (opt.test):
    yx = line[:-1].split (" ")
    y = yx[0]
    x = [int (z.split(':')[0]) for z in yx[1:]]
    y_ = m.binClassify (x) and '+1' or '-1'
#    y_ = m.getLabel (x)
    if y == y_:
        corr += 1
    else:
        incorr += 1
sys.stdout.write ("acc. %.4f\n" % (float (corr) / (corr + incorr)))
timer.stopTimer ()

timer.printElapsed ()
