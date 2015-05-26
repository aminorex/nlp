#! /usr/bin/env bash

tool_dir=$HOME/u/ja/wat2014/tools
${tool_dir}/travatar/script/preprocess/preprocess.pl \
  -program-dir ${tool_dir} -truecase-trg -split-words-trg '(-|\\\\/)' \
  -egret-src-model ${tool_dir}/egret/jpn_grammar \
  -egret-trg-model ${tool_dir}/egret/eng_grammar \
  -nile-segments $(nproc) -nile-gizatype union \
  -nile-model ${tool_dir}/nile/model/nile-en-ja.model \
  -nile-order trgsrc -align -threads $(nproc) -clean-len 80 \
  -src ja -trg en train.ja train.en train >& train.log
