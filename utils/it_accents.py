#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unicodedata
import itertools
import cPickle
import sys
from codecs import open

_it_path = 'it-20120608.pars'
_it_pickle = 'it-20120608.dic-lc.pkl'


# definitely not italian
_bad_set = set(u'ªµºßæçðñõöøãäåü')
# maybe some arent italian
_ext_set = set(u'àáâèéêëìíîïòóôùúû')
# just accented vowels, no other marks
_acc_set = set(u'àáèéìíòóùú') 
# these are italian for sure
_ita_set = set(u'àèéìòóù') 

_not_set = _bad_set
_not_set |= _ext_set
_not_set -= _acc_set

_nit_set = _bad_set
_nit_set |= _ext_set
_nit_set -= _ita_set

# single quote like 
_apo_set = set(u'’´`\'')

# double quote like
_dqt_set = set(u'“”»«')

# sentence terminators
_end_set = set(u'.!?')

# hyphen like
_hyp_set = set(u'-–—')

# map from unaccented vowels to their accented forms from _ita_set
_ita_map = { 
   u'a': u'à',
   u'e': u'èé', 
   u'i': u'ì',
   u'o': u'òó',
   u'u': u'ù' 
}


# true iff unich definitely breaks a token 
def terminal(unich):
   cat=unicodedata.category(unich)
   return cat[0] != 'L'


# should we split when at pos of len, and unich is at pos, nextch at pos+1?
def subsplit(pos,len,unich,nextch):
   cat=unicodedata.category(unich)
   if cat[0]=='L' and cat[1] != 'o':
     return False
   if cat[0]=='P':
     if pos == 0 or pos >= len-1 or nextch and pos == len-2 and unicodedata.category(nextch)[0]=='P':
       return True
     if unich in _apo_set or unich in _hyp_set:
       return False
     return True
   return True


# return list of tokens in str
def tokens(str):
   toks=[]
   for x in str.split():
     if x[0] in _dqt_set:
        x=x[1:]
     if x[-1] in _dqt_set:
        x=x[:-1]
     lx = len(x)
     start=0
     for y in xrange(lx):
       if subsplit(y,lx,unicode(x[y]),unicode(x[y+1]) if y < lx-1 else None):
         if start < y:
           toks.append(x[start:y])
         start=y+1
         toks.append(x[y:start])
     if start < lx:
       toks.append(x[start:(lx-1 if terminal(unicode(x[lx-1])) else lx)])
   return toks


# add to the count of word in dic
def tally_unigram(word,dic):
  n=dic.get(word)
  if not n:
    n=0
  n += 1
  dic[word] = n
  return n


# remove non-italian keys from dictionary d
# perform case folding if requested
def cleanse_dict(d,verbosity=0,casefold=True,exclusions=_nit_set):
  charset=set()
  nr=0
  last_nr=0
  ks=d.keys()
  kl=set()
  nk=0
  for k in ks:
    if verbosity > 0 and nr > last_nr and nr % 100 == 0:
      print nr
      last_nr = nr

    # check first character
    unich=unicode(k[0])

    # extreme unicode values indicate not italian lexical tokens
    if ord(unich) > ord(u'ü') or ord(unich) < ord('A'):
      if verbosity > 1:
        print cat,k,d[k]
      del d[k]
      nr += 1
      continue

    # anything not a latin upper or lower case or apostrophic is unacceptable
    cat=unicodedata.category(unich)
    mark=False
    if cat[0] != 'L' or cat[1] == 'o':
      mark=True
      if not unich in _apo_set:
        if verbosity > 1:
          print cat,k,d[k]
        del d[k]
        nr += 1
        continue

    if len(k) < 2:
      continue

    # successive apostrophics are unacceptable
    if mark:
      cat=unicodedata.category(unicode(k[1]))
      if cat[0] != 'L' or cat[1] == 'o':
        if verbosity > 1:
          print cat,k,d[k]
        del d[k]
        nr += 1
        continue

    # check last character
    unich=unicode(k[-1])

    cat=unicodedata.category(unich)
    if (cat[0] != 'L' or cat[1] == 'o') and not unich in _apo_set:
      if verbosity > 1:
        print cat,k,d[k]
      del d[k]
      nr += 1
      continue

    if not casefold:
      continue

    # do casefolding
    k2=k.lower()
    if k2 != k:
      if d.get(k2):
        d[k2] += d[k]
      else:
        d[k2] = d[k]
      del d[k]
      nr += 1
      continue

    # when casefolding, you also get internal token checks and charset building
    mark=False
    for c in k:
      unich=unicode(c)
      if unich in _apo_set or unich in _hyp_set:
         charset.add(unich)
      elif ord(unich) < ord('A') or ord(unich) > ord(u'ü') or unich in exclusions:
         mark=True
      else:
         charset.add(unich)
    if mark:
      nk += 1
      kl.add(k)
      del d[k]

  return nr,nk,charset,list(kl) 


# build a dictionary from a .pars file
def make_dict(path,verbose=0):
   f=open(path,encoding='utf-8')
   n=0
   d={}
   w=0
   # count unigram tokens
   for line in iter(f):
      n+=1
      for x in tokens(line.strip()):
         tally_unigram(x,d)
         w+=1
      if verbosity > 0 and n % 1000 == 0:
         print n,w,len(d)
   f.close()
   # remove bad tokens
   nr,nk,chars,deadkeys = cleanse_dict(d,casefold=True,exclusions=_nit_set,verbosity=verbose) 
   # report counts, save removed tokens
   if verbosity > 0:
      print nr,nk,len(chars),len(deadkeys)
      f=open(path+".dead","w","utf-8")
      for k in deadkeys:
         f.write(k+"\n")
      f.close()
   # return frequency dictionary
   return d


# return a version of word with vowels accented to match
# an entry pre-existing in dic, or fail with None
def find_accented(word,dic):
   lw = len(word)
   ks = set(_ita_map.keys())
   alts = [ word ]
   for ii in xrange(lw):
       avs = _ita_map.get(word[ii])
       if avs:
          for av in avs:
             x=word[:(ii-1)]+av+word[(ii+1):]
             if x in dic:
                return x
             alts.append(x)
   return None


# return a version of word with an apostrophe or accent merged to 
# an adjacent unaccented vowel to match a word pre-existing in dic
def normalize_apo(word,dic,accent_set=_apo_set):
   lw = len(word)
   alts=[word]
   for ii in xrange(lw):
      for w in alts:
         if w[ii] in accent_set:
            if ii > 0:
               avs = _ita_map.get(w[ii-1])
               if avs:
                  for av in avs:
                     x = w[:ii-2]+av+w[ii:]
                     if x in dic:
                        return x
                     alts.append(x)
            elif ii < lw-1:
               avs = _ita_map.get(w[ii+1])
               if avs:
                  for av in avs:
                     x = w[:ii]+av+w[ii+2:]
                     if x in dic:
                        return x
                     alts.append(x)

   return None            


# get best match for word in dic if possible, else None
def normalize_accents(word,dic,isolate_set=_apo_set):
   if word in dic:
      return word

   if not (set(word) & isolate_set):
      return find_accented(word,dic)

   return normalize_apo(word,dic,accent_set=isolate_set)



