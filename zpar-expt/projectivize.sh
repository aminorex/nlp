#!/bin/bash
maltparser=../../maltparser-1.7.1/maltparser-1.7.1.jar
for pproj in baseline head path head+path 
do
	mkfifo pipe_in pipe_out
	cat $1 | awk '{if(NF==4) {$3=$3+1;print} else printf("\n")}' | sed 's/ /\t/g' | sed 's/\t\t\t//g' > pipe_in &
	java -jar ${maltparser} -c pproj -m proj -i pipe_in -o pipe_out -pp ${pproj} -of malttab -if malttab &
	awk < pipe_out '{if(NF==4) {$3=$3-1;print} else printf("\n")}' > $1.${pproj}
	rm pipe_in pipe_out
	mv pproj.mco ${pproj}.mco
done
