"""
an implementation of a projective dependency parsing decoder using the Eisner algorithm.

The implementation follows that one of MstParser.

By Yoav Goldberg, (2009)

GPL
"""
from heapq import heappush, heappop
from collections import defaultdict

class ParseForestItem:#{{{
   def __init__(self,s,r=0,t=None,dir=0,comp=0,score=float("-inf"),left=None,right=None):
      self.s=s
      self.r=r
      self.t=t if t is not None else s
      self.dir=dir
      self.comp=comp
      self.score=score
      self.left=left
      self.right=right
      assert(isinstance(s,int)),s
      assert(isinstance(t,int)),t

   def __str__(self):
      return "<%s:%s:%s>" % (self.s,self.t,self.dir)
   def __repr__(self):
      return "<%s:%s:%s:%s>" % (self.s,self.t,self.dir,self.score)

   def deps(self):
      if not self.left: return []
      if self.comp==0:
         return self.left.deps()+self.right.deps()
      elif self.dir==0:
         return self.left.deps()+self.right.deps()+[(self.s,self.t)]
      else:
         return [(self.t,self.s)]+self.left.deps()+self.right.deps()
#}}}

class KBestParseForest: #{{{
   #@@@ TODO: see mstparser.KBestParseForest

   def __init__(self, length, K=1):
      pass
      self.length=length   
      self.K=K             

      self.chart = defaultdict(list)  # [(source,target,direction,complete)][K]
                                 # [K] is ordered: bigger to smaller
                                 # change to from list to deque?
      #@@ TODO

   def add_pre_production(self,source,direction,score): #{{{
      """
      add (source,source,direction,0) to chart with score=score
      
      if there are already K items at this location, and score < smallest, don't add
      if there are already K items and score > smallest, add to place and dicard last

      return: True if added, False otherwise
      """
      chart=self.chart
      K=self.K
      items = self.chart[(source,source,direction,0)]
      if not items: items.append(ParseForestItem(s=source,t=source,dir=direction,score=float("-inf")))
      if items[-1].score > score: 
         return False # TODO: < or <= ?

      # add new item in order, discard last one if too many
      for i,item in enumerate(items):
         if score > item.score: ## NOTE: I put >= and not > so I definitely add something
            items.insert(i,ParseForestItem(s=source,t=source,dir=direction,score=score))
            if len(items)>K:
               items.pop()
            return True
      assert(False,"should not get here -- something should be added if I entered the loop")
      #}}}

   def add(self, src,r,target,dir,comp,score,item1,item2): #{{{
      """
      add (src,target,dir,comp) to chart with score=score [and also R, item1, item2]
      @@ TODO what am I using these R, item1, item2 for??  [R is actually k in i,j,k in eisner]
      
      if there are already K items at this location, and score < smallest, don't add
      if there are already K items and score > smallest, add to place and dicard last

      return: True if added, False otherwise
      """
      added = False;
      chart=self.chart
      K=self.K
      idx=(src,target,dir,comp)

      items = chart[idx]
      if not items: items.append(ParseForestItem(s=src,r=r,t=target,dir=dir,comp=comp,score=float("-inf"))) # null,null,null
      if items[-1].score > score: return False # TODO: < or <= ?

      for i,item in enumerate(items):
         if score > item.score: ## NOTE: I put >= and not > so I definitely add something : whe moving to >=, I got 2 roots. for some reason removing it solved the prob. Not sure why..
            toAdd = ParseForestItem(s=src,r=r,t=target,dir=dir,comp=comp,score=score,left=item1,right=item2);
            items.insert(i,toAdd)
            if len(items) > K: items.pop()
            return True
      assert(False,"should not get here -- something should be added if I entered the loop")
   #}}}

   def get_items(self,source,target,direction,complete): #{{{
      ## @@ TODO: change chart to defaultdict(list) ??
      if (source,target,direction,complete) in self.chart:
         return self.chart[(source,target,direction,complete)]  
      return []
   #}}}
   
   def get_kbest_pairs(self, items1, items2): #{{{
      #items1, items2 are sorted (big to small)
      #want to yield at most K (best) combinations items1[i],items2[j] sorted by the sum items1[i]+items2[i]
      if (not items1) or (not items2): return 
      K = min(self.K,len(items1),len(items2))
      K = min(self.K,len(items1),len(items2))
      items1 = [-i.score for i in items1]
      items2 = [-i.score for i in items2]

      seen = set()
      heap=[]
      n = 0
      scored=((items1[0]+items2[0]),0,0)
      heappush(heap,scored)
      seen.add((0,0))

      while True:
         score,i1,i2 = heappop(heap)
         if score == float("inf"): return
         yield i1,i2
         n+=1
         if n >= K: break

         if i1+1 < len(items1) and not (i1+1,i2) in seen:
            heappush(heap, ((items1[i1+1]+items2[i2]),i1+1,i2) )
            seen.add((i1+1,i2))
         if i2 < len(items2) and not (i1,i2+1) in seen:
            heappush(heap, ((items1[i1]+items2[i2+1]),i1,i2+1) )
            seen.add((i1,i2+1))
   #}}}

   def get_best_parses(self): #{{{
      for item in self.chart[(0,self.length,0,0)]:
         if item.score != float("-inf"):
            yield item.deps()
   #}}}
#}}}

class EisnerDecoder: #{{{
   def __init__(self, length, default=float("-inf")):
      self.length = length
      self.probs = defaultdict(lambda:default) #@@ really?
      pass #@@@@ TODO

   @classmethod
   def from_sent(cls, sent,default=float("-inf")):
      return cls(len(sent)+1,default)

   def set_score(self, parent, child, score=1.0): #{{{
      # @@ TODO: verify
      if parent < child:
         self.probs[(parent,child,0)]=score
      else:
         self.probs[(child,parent,1)]=score
   #}}}
   def add_score(self, parent, child, score=1.0): #{{{
      # @@ TODO: verify
      probs=self.probs
      if parent < child:
         if probs[(parent,child,0)]==float("-inf"):
            probs[(parent,child,0)]=0
         probs[(parent,child,0)]+=score
      else:
         if probs[(child,parent,1)]==float("-inf"):
            probs[(child,parent,1)]=0.0
         probs[(child,parent,1)]+=score
   #}}}

   def decode(self,K=1): #{{{
      """
      yield the k-best answers for the current probs.
      each answer is a list of (parent,child) pairs.
      """
      probs=self.probs
      length=self.length
      pf = KBestParseForest(length-1,K)

      # initialize #{{{
      for s in xrange(length):
         # pf.add_pre_production(source,direction,prob) TODO [why 0.0 as prob?]
         pf.add_pre_production(s,0,0.0)  
         pf.add_pre_production(s,1,0.0)  
      #}}}

      for j in xrange(1,length): #{{{
         for s in xrange(0,length): #{{{
            if s+j >= length: break
            t=s+j
            if t>length: continue

            assert(s<t)
            prob_st = probs[(s,t,0)]
            prob_ts = probs[(s,t,1)]

            ##prodProb = 0.0 ## can remove?

            for r in xrange(s,t+1): #{{{  #@@ why this t+1 combined with the r!=t check?
               #/** first is direction, second is complete*/
               #/** _s means s is the parent*/
               if(r == t): continue
               b1 = pf.get_items(s,r,0,0)     # b1: list of pf
               c1 = pf.get_items(r+1,t,1,0)   # c1: list of pf

               if b1 and c1: ## @@ TODO can I remove the check?
                  pairs = pf.get_kbest_pairs(b1,c1) # list of pairs (idx1,idx2)
                  for comp1,comp2 in pf.get_kbest_pairs(b1,c1):
                     bc = b1[comp1].score+c1[comp2].score ## float
                     pf.add(s,r,t,0,1,bc+prob_st,b1[comp1],c1[comp2])
                     pf.add(s,r,t,1,1,bc+prob_ts,b1[comp1],c1[comp2])
            #}}}

            for r in xrange(s,t+1): #{{{ #@@ why this t+1 combined with the r!=t check?
               if r != s: #{{{
                  b1 = pf.get_items(s,r,0,1) ##
                  c1 = pf.get_items(r,t,0,0) ##
                  if b1 and c1:  ## @@ TODO can I remove the check?
                     for comp1,comp2 in pf.get_kbest_pairs(b1,c1): 
                        bc = b1[comp1].score+c1[comp2].score ## float
                        ## @@ understand this line!
                        if not pf.add(s,r,t,0,0,bc,b1[comp1],c1[comp2]): break
               #}}}

               if r != t: #{{{
                  b1 = pf.get_items(s,r,1,0)
                  c1 = pf.get_items(r,t,1,1)
                  if b1 and c1: ## @@TODO can I remove the check?
                     for comp1, comp2 in pf.get_kbest_pairs(b1,c1):
                        bc = b1[comp1].score+c1[comp2].score ## float
                        ## @@ understand this line!
                        if not pf.add(s,r,t,1,0,bc,b1[comp1],c1[comp2]): break
               #}}}
            #}}}
         #}}}
      #}}}
      
      return pf.get_best_parses()
   #}}}
#}}}


