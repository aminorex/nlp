#! /usr/bin/python
# --------------------------------------- 
# File Name : analysis.py
# Creation Date : 28-02-2014
# Last Modified : Fri May  9 13:05:49 2014
# Created By : wdd 
# --------------------------------------- 
import sys, re, string, pickle, numpy
from itertools import *

p = re.compile(r'^spanish.standard.(\S+).bstrn64.bstst(\d+).ver0.5.spanish.itr60,(.*),$')
summary = {}

def main():
	acc_f = open(sys.argv[1], 'r')
	for l in acc_f:
		m = p.match(l)
		t, b, res_l = m.group(1), int(m.group(2)), m.group(3).split(',')
		numLst =[100*float(v) for v in res_l] 
		if t == 'dev':
			maxv = max(numLst)
			itr = numLst.index(maxv) + 1
			summary[b] = [itr, maxv, 0, 0]
		if t == 'tst':
			idx = summary[b][0] - 1
			summary[b][2] = numLst[idx] 
	acc_f.close()
	spe_f = open(sys.argv[2], 'r')
	for l in spe_f:
		m = p.match(l)
		t, b, res_l = m.group(1), int(m.group(2)), m.group(3).split(',')
		if t == 'dev': continue
		numLst =[float(v) for v in res_l] 
		avg = numpy.mean(numLst)
		summary[b][3] = avg
	spe_f.close()
	for b in summary:
		lst = summary[b]
		print str(b) + ',' + str(lst[0]) + ',' + str("%.0f" % lst[3]) + ',' + str("%.2f" % lst[2]) + ',' + str("%.2f" % lst[1])

if __name__ == "__main__": main()
