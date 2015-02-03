#! /usr/bin/python
# --------------------------------------- 
# File Name : genSent.py
# Creation Date : 06-02-2014
# Last Modified : Thu Feb  6 19:50:28 2014
# Created By : wdd 
# --------------------------------------- 
import sys, re, string, pickle
from itertools import *

def procSent(input_f):
	old_sent = ""
	for l in input_f:
		if l == "\n":
			yield old_sent.strip()
			old_sent = ""
		else:
			lt = l.split()
			old_sent += lt[0]+"/"+lt[1]+" "
	if len(old_sent) > 0:
		yield old_sent.strip()

def main():
	for sent in procSent(sys.stdin):
		print sent
	
if __name__ == "__main__": main()
