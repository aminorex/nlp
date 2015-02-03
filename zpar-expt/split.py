# /usr/bin/python
# --------------------------------------- 
# File Name : preprocess.py
# Creation Date : 06-02-2014
# Last Modified : Thu Feb  6 18:45:13 2014
# Created By : wdd 
# --------------------------------------- 
import sys, re, string, pickle, random
from itertools import *

def procSent(input_f):
	old_sent = ""
	for l in input_f:
		if l == "\n":
			yield old_sent
			old_sent = ""
		else:
			old_sent += l
	yield old_sent

def main():
	sents = []
	trn_f = open(sys.argv[1], 'w')
	dev_f = open(sys.argv[2], 'w')
	tst_f = open(sys.argv[3], 'w')
	for sent in procSent(sys.stdin):
		sents += [sent]
	random.shuffle(sents)
	print >> trn_f, "\n".join([l for l in sents[0:int(0.8*len(sents))]]) 
	print >> dev_f, "\n".join([l for l in sents[int(0.8*len(sents))+1:int(0.9*len(sents))]]) 
	print >> tst_f, "\n".join([l for l in sents[int(0.9*len(sents))+1:]])
	trn_f.close()
	dev_f.close()
	tst_f.close()
	
if __name__ == "__main__": main()
