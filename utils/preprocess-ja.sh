#! /usr/bin/env bash

if [ -z "$TRAVATAR" ]; then 
  for top in $HOME/u/ja $HOME/ja $HOME/u/ja/tools $HOME/u/ja/wat2014/tools; do
    if [ -d $top/travatar/. ]; then
      TRAVATAR=$top/travatar
      break
    fi
  done
fi

if [ -z "$KYTEA" ]; then
  for top in $HOME/u/ja $HOME/ja $HOME/u/ja/tools $HOME/u/ja/wat2014/tools; do
    if [ -d $top/kytea/. ]; then
      KYTEA=$top/kytea
      break
    fi
  done
fi

if [ -z "$MECAB" ]; then
  if [ -f $NA_TOOL/bin/mecab ]; then
    MECAB=$NA_TOOL/bin
  elif [ -f /usr/bin/mecab ]; then
    MECAB=/usr/bin
  fi
fi

wakati=false
for arg in $@; do
  if [ -d $arg ]; then
    if [ -f $arg/script/tree/han2zen.pl ]; then
       TRAVATAR=$arg
    elif [ -f $arg/src/bin/kytea ]; then
       KYTEA=$arg
    elif [ -f $arg/mecab ]; then
       MECAB=$arg
    else
       echo $0: Unknown directory type $arg 1>&2
       exit 1
    fi
  else
    case $arg in
    -m)
      wakati=true
      ;;
    -Owakati)
      wakati=true
      ;;
    *)
      echo $0: Unknown option $arg 1>&2
      exit 1
    esac
  fi
done

tokenize() {
  if $wakati; then
    $MECAB/mecab -Owakati -b 256000
  else
    $KYTEA/src/bin/kytea -model $KYTEA/data/model.bin -notags -wsconst D
  fi
}

sed -e "s/、/，/g;s/（）//g;s/ //g" | \
  $TRAVATAR/script/tree/han2zen.pl --nospace | \
    tokenize

