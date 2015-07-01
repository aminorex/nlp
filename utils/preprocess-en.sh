#! /usr/bin/env bash

casing=true
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
    esac
  fi
done

recase() {
  case $casing in
  false)
    cat
    ;;
  lower)
    tr 'A-Z' 'a-z'
    ;;
  *)
    $TRAVATAR/script/recaser/truecase.pl --model $EN_TRUECASER
    ;;
  esac
}

$TRAVATAR/src/bin/tokenizer | \
  sed -e "s/[     ]+/ /g; s/^ +//g; s/ +$//g" | \
  $TRAVATAR/src/bin/tree-converter -input_format word -output_format word -split '(-|\\/)' | \
    recase
