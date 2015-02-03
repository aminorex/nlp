#/bin/bash
path=/proj/mlnlp/wdd/depParsing/workspace
array=($(ls ${path}| egrep "^spanish\.standard\.(:?tst|dev).*"))
outdir=${path}/analysis/spanish
mkdir ${outdir}
for d in ${array[*]}
do
	array_item=($(ls ${path}/$d/summary/))
	for item in ${array_item[*]}
	do 
		output=${outdir}/${item}
		echo -n $d,>> ${output}
		cat ${path}/$d/summary/${item} >> ${output}
		echo >> ${output}
	done
done
