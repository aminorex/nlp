#! /usr/bin/env bash
set -e +o pipefail
sed -e 's,\t, ,g; s,\xe3\x80\x80, ,g; s,  , ,g; s,^ ,,; s, $,,g; /^$/d'| \
  tokenizer -T ja | preprocess-ja.sh | \
  pcregrep --buffer-size 100000 -u -v '([^ ]+ ){199,}' |\
  pcregrep --buffer-size 100000 -u '([\p{Han}\p{Katakana}\p{Hiragana}]){2,}'
