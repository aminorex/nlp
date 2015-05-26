#! /usr/bin/env bash

tool_dir=~/u/ja/wat2014/tools
for f in $@; do
  $tool_dir/travatar/script/preprocess/preprocess.pl \
  -program-dir $tool_dir -split-words-trg '(-|\\\\/)' \
  -egret-src-model $tool_dir/egret/jpn_grammar \
  -egret-trg-model $tool_dir/egret/eng_grammar \
  -egret-forest-opt "-nbest4threshold=500" -forest-src -forest-trg \
  -threads $(nproc) -src ja -trg en \
  $f.ja $f.en $f >& $f.log
done
