#! /bin/bash
for USAGE in dev tst 
do
	for BSTST in 1 2 4 8 16 32 64 
#	for BSTST in 64 #32 16 8 4 2 1 
	do
		export bstst=${BSTST}
		export usage=${USAGE}
		./test.sh
	done
done
