#!/bin/bash
#=====Bascic information (need to be customized)=========
bstrn=64 #training beamsize
itr=60 #number of iterations
lang=spanish #target language
ver_trn=0.5 #zpar version
usage=train #usage
type=spanish #spanish or generic
proj=head #projectivize strategy
misc=standard #other information
#======System information (need to be customized)========
path=/proj/mlnlp/wdd/depParsing #working directory
trainer=${path}/runable/${lang}/${type}${bstrn}/train #training executable
train_f=${path}/data/${lang}/trn.${proj} #input training file
output_path=${path}/workspace #directory for the output
#======No need to customized===========================
config=${type}.${misc}.${usage}.${proj}.bstrn${bstrn}.ver${ver_trn}.${lang}.itr${itr}
local_path=${output_path}/${config}
model_dir=${local_path}/model
tmp_dir=${local_path}/tmp
log_dir=${local_path}/log
if [ ! -d ${local_path} ]
then
	mkdir ${local_path}
	mkdir ${model_dir}
	mkdir ${tmp_dir}
	mkdir ${log_dir}
fi
echo ${config}
for i in `seq 1 ${itr}`;
do
	if [ -f ${model_dir}/model.$i ]
	then
		continue
	fi
	echo Iteration $i
	echo Iteration $i >> ${log_dir}/log.txt 
	echo "${trainer} ${train_f} ${tmp_dir}/model 1"
	${trainer} ${train_f} ${tmp_dir}/model 1 > ${tmp_dir}/log.txt 
	cp ${tmp_dir}/model ${model_dir}/model.$i
	cat ${tmp_dir}/log.txt
	cat ${tmp_dir}/log.txt >> ${log_dir}/log.txt
done
