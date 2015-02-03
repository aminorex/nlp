#!/usr/bin/python
"""
projectivization of non-projective dependency trees.
useful for training a projective parser on non-projective data.
(this is lossy conversion. if you actually care about the non-projective
links, use a non-projective parser.  this will just help you maximize the 
accuracy of the projective links of you projective parser.)

By Yoav Goldberg, (2009)

GPL
"""
from eisner import EisnerDecoder as ProjectiveDecoder

def projectivize_parents(parents):
   """
   input: a list of parents (assume childs are ordered). parents are ints
   output: a list of parents that form a projective tree.
   """
   parents = [-1]+parents # append ROOT
   decoder = ProjectiveDecoder.from_sent(parents,0) # default value is 0
   for i,p in enumerate(parents):
      decoder.set_score(p,i,1) # real parents get 1
   projective=decoder.decode(1).next()
   new_parents=[p for (p,c) in sorted(projective,key=lambda x:x[1])]
   return new_parents 

def projectivize_conll(conll_sent):
   parents = [int(tok[-4]) for tok in conll_sent]
   new_parents=projectivize_parents(parents)
   for tok,p in zip(conll_sent,new_parents):
      tok[-4]=str(p)


if __name__=='__main__':
   MODE = "parents"
   MODE = "conll"

   if MODE=="parents":
      for line in file(sys.argv[1]):
         parents = [int(x.split(":")[0]) for x in line.strip().split()]
         if not parents: continue
         print " ".join(map(str,projectivize_parents(parents)))
   if MODE=="conll":
      import yutils
      for sent in yutils.tokenize_blanks(file(sys.argv[1])):
         projectivize_conll(sent)
         for tok in sent:
            print " ".join(tok)
         print
         sys.stderr.write(".")
         sys.stderr.flush()

