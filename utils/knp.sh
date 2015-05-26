#! /usr/bin/env bash

opt=dpnd
ext=dpnd
for arg in $@; do
  case $arg in
  -d)
   opt=dpnd
   ext=dpnd
   ;;
  -s)
   opt=sexp -normal
   ext=sexp
   ;;
  -b)
   opt=both
   ;;
  -*)
   echo $0: Unknown option \"$arg\" ignored. 1>&2
   ;;
  *)
   files="$files $arg"
   ;;
  esac
done

parse() {
 file=$1
 shift
 ext=$1
 opt=$@
 echo "juman < $file | knp -$opt"
 eval "juman < $file | knp -$opt"
 return $?
}

if [ $opt = "both" ]; then
  for f in $files; do
    parse $f dpnd > $f.dpnd 2> $f.dpnd.err
    parse $f sexp -normal > $f.sexp 2> $f.sexp.err
  done
else
  for f in $files; do
    parse $f $opt > $f.$ext 2> $f.$ext.err
  done
fi

exit 0

