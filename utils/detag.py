#! /usr/bin/env python
import sys

for x in sys.stdin:
    print " ".join(map(lambda x: x.split('|')[0],x.strip().split(' ')))
        
    
