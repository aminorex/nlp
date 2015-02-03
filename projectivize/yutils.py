## Copyright 2010 Yoav Goldberg
##

from collections import defaultdict

def tokenize_blanks(fh):
   stack = []
   for line in fh:
      line = line.strip().split()
      if not line:
         if stack: yield stack
         stack = []
      else:
         stack.append(line)
   if stack: yield stack

def ngrams(strm,n=2):
    stack = []
    for item in strm:
       if len(stack) == n:
          yield tuple(stack)
          stack = stack[1:]
       stack.append(item)
    if len(stack)==n: yield tuple(stack)

def count(strm,dct=False):
   d = defaultdict(int)
   for item in strm: d[item]+=1
   if dct: return d
   else: return sorted(d.items(),key=lambda x:x[1])
 
def read_words_from_raw_file(filename, tokenizer=lambda line:line.strip().split()):
   for line in file(filename):
      for item in tokenizer(line): 
         yield item

class frozendict(dict):
    def _blocked_attribute(obj):
        raise AttributeError, "A frozendict cannot be modified."
    _blocked_attribute = property(_blocked_attribute)

    __delitem__ = __setitem__ = clear = _blocked_attribute
    pop = popitem = setdefault = update = _blocked_attribute

    def __new__(cls, *args):
        new = dict.__new__(cls)
        dict.__init__(new, *args)
        return new

    def __init__(self, *args):
        pass

    def __hash__(self):
        try:
            return self._cached_hash
        except AttributeError:
            h = self._cached_hash = hash(tuple(sorted(self.items())))
            return h

    def __repr__(self):
        return "frozendict(%s)" % dict.__repr__(self)



class Group(defaultdict):
    def __init__(self, key=lambda x:x, val=lambda x:x, vals_in=Count, seq=[]):
       defaultdict.__init__(self, vals_in)
       self._keyf = key
       self._valf = val
       self._colltype = vals_in
       self.update(seq)
 
    def update(self, seq):
       for k,v in ( (self._keyf(item), self._valf(item)) for item in seq):
          self[k].add(v)
 
    def add(self, item):
       k = self._keyf(item)
       v = self._valf(item)
       self[k].add(v)
 
 
