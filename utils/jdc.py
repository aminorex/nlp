#! /usr/bin/env python
# -*- coding: utf-8 -*-

#
# read japanese dependecy corpus parses from distribution files
# -q : just read (validaate script)
# -i : prefix output (one sentence per line) with sentence id
# -d : add .tree file name prefix
#
import os, sys, getopt

JDC_TAGS = [
'',
'URL',
'代名詞',
'副詞',
'助動詞',
'助詞',
'動詞',
'名詞',
'形容詞',
'形状詞',
'感動詞',
'接尾辞',
'接続詞',
'接頭辞',
'空白',
'英単語',
'補助記号',
'言いよどみ',
'記号',
'語尾',
'連体詞',
]

JDC_TAG_NOS = {}
for ii,tag in enumerate(JDC_TAGS):
    JDC_TAG_NOS[tag] = ii

class parse_reader:
    def __init__(self,path,passurl=False,verbose=0):
        self.path = path
        self.tags = {}
        self.taglist = []
        self.lno = 0
        self.passurl = passurl
        self.verbose=verbose

    def __iter__(self):
        self.fp = open(self.path,'r')
        self.size = os.fstat(self.fp.fileno()).st_size
        return self

    def read(self):
        global JDC_TAG_NOS
        parse = [ "" ]
        nlines = 0
        nlead = 0
        nerrs = 0
        for line in self.fp:
            line=line.strip()
            if not line:
                if nlines:
                    break
                nlead += 1
                continue
            nlines += 1
            if line[:3] == 'ID=':
                parse[0] = line[3:]
                continue
            items = line.split()
            try:
                node = int(items[0].lstrip('0'))
                head = int(items[1].lstrip('0'))
                word = items[2]
                ptag = items[3]
                if ptag in JDC_TAG_NOS:
                    ptag = JDC_TAG_NOS[ptag]
                    if ptag == 1 and not self.passurl:
                        word = "__URL__"
                parse.append((node,head,word,ptag))
            except:
                if self.verbose:
                    msg = 'id="'+parse[0]+'" len='+str(len(parse)-1)+" line="+str(nlines)+"\n"
                    msg += '  malformed: '+line+"\n"
                    sys.stderr.write(msg)
                nerrs += 1
        return parse,nlines,nerrs,nlead

    def next(self):
        if not self.fp:
            raise StopIteration
        parse,nlines,nerrs,nlead = self.read()
        self.lno += nlines + nlead
        if self.verbose:
            print 'parse',self.path,self.lno,nlines,nerrs,nlead,len(parse)
        if len(parse) < 2:
            if self.fp.tell() >= self.size:
                if self.verbose:
                    print 'next',self.fp.tell(),self.size
                self.fp.close()
                self.fp = None
                raise StopIteration
            raise Exception("Empty parse at "+self.path+":"+str(self.lno))
        return parse,nlines,nerrs

def read_corpus(top,paths,passurl=False,verbose=0):
    nf,np,nw = 0,0,0
    parses = []
    if not paths:
        for r in ( "2012" , "ClassA-1-2014" ): 
            for f in os.listdir(top+"/"+r):
                if f[-5:] != '.tree':
                    continue
                paths.append(top+"/"+r+"/"+f)
    if paths:
        for ii,path in enumerate(paths):
            nf += 1
            pos = 0
            for p,nl,ne in parse_reader(path,passurl,verbose):
                pos += 1
                np += 1
                nw += len(p) - 1
                parses.append((p,ii,pos))
    return parses,paths,nf,np,nw

if __name__ == '__main__':
    top = '.'
    quiet = False
    ident = False
    detail = False
    passurl = True
    paths = []
    verbose = 0
    opts, args = getopt.getopt(sys.argv[1:],'diquv')
    for opt, arg in opts:
        if opt == '-q':
            quiet = True
        elif opt == '-i':
            ident = True
        elif opt == '-d':
            detail = True
        elif opt == '-u':
            passurl = False
        elif opt == '-v':
            verbose += 1
    if args:
        for arg in args:
            if os.path.isdir(arg):
                top = arg
            else:
                paths.append(arg)

    try:
        parses,paths,nf,np,nw = read_corpus(top,paths,passurl,verbose)
    except:
        ty,ob,tr = sys.exc_info()
        sys.stderr.write(repr(ty)+"\n");
        sys.stderr.write(repr(ob)+"\n")
        sys.excepthook(ty,ob,tr)
        sys.exit(1)
        
    if quiet:
        print nf,np,nw
    else:
        for parse,fileno,pos, in parses:
            if detail:
                print paths[fileno].split('/')[-1].replace('.tree','')+':'+str(pos)+' ',
            if ident:
                print 'id='+parse[0]+': ',
            for node,head,token,tagno in parse[1:]:
                print token,
            print

