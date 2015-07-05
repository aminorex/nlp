#! /usr/bin/env bash

casing=true
aggressive=false

EN_TRUECASER=/home/akimbal1/u/ja/wat2014/ja-en/preproc/train/truecaser/en.truecaser

for arg in $@; do
  if [ -d $arg ]; then
    TRAVATAR="$arg"
  elif [ -f $arg ]; then
    EN_TRUECASER=$arg
  else
    case $arg in
    -n)
      casing=false
      ;;
    -l)
      casing=lower
      ;;
    -t)
      casing=true
      ;;
    -a)
      aggressive=true
      ;;
    esac
  fi
done

if [ -z "$TRAVATAR" ]; then
  for d in $HOME/u/ja/wat2014/tools $HOME/u/ja/tools /bb/news/translation/ja/tools; do
    if [ -d $d/travatar ]; then
      TRAVATAR=$d/travatar
      break;
    fi
  done
fi

recase() {
  case $casing in
  false)
    cat
    ;;
  lower)
    $TRAVATAR/script/tree/lowercase.pl
    ;;
  *)
    $TRAVATAR/script/recaser/truecase.pl --model $EN_TRUECASER
    ;;
  esac
}

aggravate() {
  if $aggressive; then
    sed 's,\([a-zA-Z]\)-\([a-zA-Z]\),\1 - \2,g'
  else
    cat
  fi
}

$TRAVATAR/src/bin/tokenizer | \
  sed -e "s/[     ]+/ /g; s/^ +//g; s/ +$//g" | \
  $TRAVATAR/src/bin/tree-converter -input_format word -output_format word \
    -split '(-|\\/)' | \
  aggravate |\
  recase
