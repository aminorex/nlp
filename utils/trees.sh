#! /usr/bin/env bash

tool_dir=$HOME/u/ja/wat2014/tools
for f in $@; do
  $tool_dir/travatar/script/preprocess/preprocess.pl \
  -program-dir $tool_dir -split-words-trg '(-|\\\\/)' \
  -egret-src-model $tool_dir/egret/jpn_grammar \
  -egret-trg-model $tool_dir/egret/eng_grammar \
  -nile-model $tool_dir/nile/model/nile-en-ja.model \
  -nile-segments $(nproc) -nile-gizatype union -nile-order trgsrc \
  -align -clean-len 80 \
  -threads $(nproc) -src ja -trg en \
  $f.ja $f.en $f >& $f.log
done
