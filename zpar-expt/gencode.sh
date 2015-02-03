#!/bin/bash

#generate file and recompile
#input$1 is the training file
#command is ./sun.sh #trainingfile#
dir=../zpar_de
python genTag.py $1 pos_old.h label_old.h
mv pos.h ${dir}/src/english/pos/penn.h
mv label.h ${dir}/src/english/dependency/label/penn.h
cp rules.h ${dir}/src/english/dependency/rules/penn.h
cp tags.h ${dir}/src/english/tags.h
#make clean -C ../zpar_de
#make english.depparser -C ../zpar_de
