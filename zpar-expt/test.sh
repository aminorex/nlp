#!/bin/bash
#=====Bascic information (need to be customized)=========
bstrn=64 #training beamsize
#tstst=64 # testing beamsize, can be specified outside
itr=60 #number of iterations
ver_trn=0.5 #zpar version
lang=spanish #target language
type=spanish #spanish or generic
proj=head #projectivize strategy
#usage=tst #tst or dev, can be specified outside
misc=standard #other information
#======System information (need to be customized)========
path=/proj/mlnlp/wdd/depParsing #working directory
tester=${path}/runable/${lang}/${type}${bstst}/depparser #testing executable
test_f=${path}/data/${lang}/${usage}.sent #input testing file
gold_f=${path}/data/${lang}/${usage}.sp #gold standard
model_dir=${path}/workspace/${type}.${misc}.train.${proj}.bstrn${bstrn}.ver${ver_trn}.${lang}.itr${itr}/model #the directory of the model, this needs to be consistent to the training folder
output_path=${path}/workspace #directory for the output
evaluate=${path}/evaluation/evaluate.py #the evaluator 
if [ $usage = tst ]
then
	nwords=58551 #number of words in testing file
else
	nwords=58733 #number of words in development file
fi
#======No need to customized===========================
config=${type}.${misc}.${usage}.bstrn${bstrn}.bstst${bstst}.ver${ver_trn}.${lang}.itr${itr}
local_path=${path}/workspace/${config}
tmp_dir=${local_path}/tmp
output_dir=${local_path}/parser_output
log_dir=${local_path}/log
summary=${local_path}/summary
#Work==============================================================
cp ${proj}.mco pproj.mco
if [ ! -d ${local_path} ]
then
	mkdir ${local_path}
	mkdir ${tmp_dir}
	mkdir ${output_dir}
	mkdir ${log_dir}
	mkdir ${summary}
fi
echo ${config}
for i in `seq 1 ${itr}`;
do
	echo Iteration $i
	echo Iteration $i >> ${log_dir}/eval_proj.txt 
	echo Iteration $i >> ${log_dir}/eval_deproj.txt 
	echo Iteration $i >> ${log_dir}/tst_log.txt 
	date_start=$(date +%s)
	echo "Start Time:"$(date)
	echo "Start Time:"$(date) >> ${log_dir}/tst_log.txt
	${tester} ${test_f} ${tmp_dir}/zparout.tagged ${model_dir}/model.${i} > ${tmp_dir}/tst_log.txt 
	cat ${tmp_dir}/tst_log.txt >> ${log_dir}/tst_log.txt
	tld=$(perl -n -e '/Loading scores... done. \((.*)s\)/ && print "$1"'< ${tmp_dir}/tst_log.txt)
	echo -n ${tld}, >> ${summary}/time_load.csv
	tt=$(perl -n -e '/Parsing has finished successfully. Total time taken is: (.*)/ && print $1'< ${tmp_dir}/tst_log.txt)
	echo -n ${tt}, >> ${summary}/time_total.csv
	echo -n $(echo "scale=2;(${tt}-${tld})"|bc), >> ${summary}/time_parse.csv
	echo -n $(echo "scale=2;${nwords}/(${tt}-${tld})"|bc), >> ${summary}/avg_time_parse.csv
	echo -n $(echo "scale=2;${nwords}/${tld}"|bc), >> ${summary}/avg_time_load.csv
	echo -n $(echo "scale=2;${nwords}/${tt}"|bc), >> ${summary}/avg_time_total.csv
	export dpath=${tmp_dir}
	./deprojectivize.sh ${tmp_dir}/zparout.tagged ${output_dir}/$i.zparout.deproj #>> ${log_dir}/tst_log.txt 
	date_end=$(date +%s)
	echo "End Time:"$(date) 
	echo "End Time:"$(date) >> ${log_dir}/tst_log.txt
	echo "System Parsing Time:$((date_end-date_start))sec" 
	echo "System Parsing Time:$((date_end-date_start))sec" >> ${log_dir}/tst_log.txt 
	echo -n $((date_end-date_start)), >> ${summary}/time_system.csv	
	echo -n $(echo "scale=2;${nwords}/$((date_end-date_start))"|bc), >> ${summary}/avg_time_system.csv	
	cat ${tmp_dir}/zparout.tagged | sed 's/\t/ /g' > ${output_dir}/$i.zparout.proj 
	#======================Projective=============================================================================
	python ${evaluate} ${output_dir}/$i.zparout.proj ${gold_f} > ${tmp_dir}/log.txt
	cat ${tmp_dir}/log.txt
	cat ${tmp_dir}/log.txt >> ${log_dir}/eval_proj.txt
	perl -n -e '/Dependency precision without punctuations: (.*) .* .*/ && print "$1,"'< ${tmp_dir}/log.txt >>${summary}/eval_word_proj.csv
	perl -n -e '/Sent precisions: (.*)/ && print "$1,"'< ${tmp_dir}/log.txt >>${summary}/eval_sent_proj.csv
	#======================Deprojective=============================================================================
	python ${evaluate} ${output_dir}/$i.zparout.deproj ${gold_f} > ${tmp_dir}/log.txt
	cat ${tmp_dir}/log.txt
	cat ${tmp_dir}/log.txt >> ${log_dir}/eval_deproj.txt
	perl -n -e '/Dependency precision without punctuations: (.*) .* .*/ && print "$1,"'< ${tmp_dir}/log.txt >>${summary}/eval_word_deproj.csv
	perl -n -e '/Sent precisions: (.*)/ && print "$1,"'< ${tmp_dir}/log.txt >>${summary}/eval_sent_deproj.csv
done
