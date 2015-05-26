#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([jdepp], [2015-02-08], [ynaga@tkl.iis.u-tokyo.ac.jp])
AM_INIT_AUTOMAKE([-Wall foreign])
AC_CONFIG_SRCDIR([config.h.in])
AC_CONFIG_HEADERS([config.h])
AC_LANG([C++])

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC
AC_PROG_AWK
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_MKDIR_P

# Checks for libraries.

# Checks for header files.
AC_CHECK_HEADERS([fcntl.h stdint.h sys/time.h unistd.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL
AC_C_INLINE
AC_TYPE_INT64_T
AC_TYPE_MODE_T
AC_TYPE_SIZE_T
AC_TYPE_SSIZE_T
AC_TYPE_UINT16_T
AC_TYPE_UINT64_T
AC_TYPE_UINT8_T

# Checks for library functions.
AC_FUNC_STRTOD
AC_CHECK_FUNCS([floor gettimeofday memchr memmove memset pow strstr strtol strtoul])
AC_PATH_PROG(CURL,   curl,   no)
AC_PATH_PROG(WGET,   wget,   no)
AC_PATH_PROG(ICONV,  iconv,  no)
AC_PATH_PROG(PYTHON, python, no)

AC_ARG_ENABLE(64bit,
        [AS_HELP_STRING([--enable-64bit],
            [build 64bit version (default=yes)])],
        [],
        [enable_64bit="yes"])

if [test "x$enable_64bit" = "xyes"]; then
  orig_cflags=$CXXFLAGS
  CXXFLAGS=-m64
  AC_RUN_IFELSE([AC_LANG_PROGRAM([],
     [return sizeof (void*) == 8 ? 0 : 1;])],
     [CXXFLAGS="-m64 $orig_cflags"],
     [AC_MSG_ERROR([Don't know how to build a 64-bit object; try --disable-64bit])])
fi

# IO Buffer Size
AC_ARG_WITH([iobuf-size],
        [AS_HELP_STRING([--with-iobuf-size=[bytes]],
                    [set the maximum size of IO buffer (default=262144)])],
        [IOBUF_SIZE=$withval],
        [IOBUF_SIZE=262144]
)
AC_DEFINE_UNQUOTED([IOBUF_SIZE], [$IOBUF_SIZE], [the size of IO buffer])

# data structure for weight trie
AC_ARG_WITH([trie-impl],
        [AS_HELP_STRING([--with-trie-impl=[IMPL]],
            [set implementation of weight trie (cedar|darts|darts-clone)])],
        [TRIE_IMPL=$withval],
        [TRIE_IMPL="cedar"])

if [test $TRIE_IMPL = "darts-clone"]; then
  AC_CHECK_HEADER([darts.h],
    [AC_DEFINE([USE_DARTS_CLONE], [1], [darts-clone as double array library])],
    [AC_MSG_ERROR(cannot find darts.h)])
  AC_DEFINE([TRIE_SUFFIX], ["dac"], [suffix of trie])
elif [test $TRIE_IMPL = "darts"]; then
  AC_CHECK_HEADER([darts.h],
    [AC_DEFINE([USE_DARTS], [1], [darts as double array library])],
    [AC_MSG_ERROR(cannot find darts.h)])
  AC_DEFINE([TRIE_SUFFIX], ["da"], [suffix of trie])
elif [test $TRIE_IMPL = "cedar"]; then
  AC_DEFINE([USE_CEDAR], [1], [cedar as double array library])
  AC_DEFINE([TRIE_SUFFIX], ["cda"], [suffix of trie])
else
  AC_MSG_ERROR(unknown trie implementation: ${TRIE_IMPL})
fi

# enable training with auto pos tags
AC_ARG_ENABLE([autopos-train],
        [AS_HELP_STRING([--enable-autopos-train],
            [train a model with auto POS tags (default=yes)])],
        [],
        [enable_autopos_train="yes"])

# pos tagger
AC_ARG_WITH([postagger],
       [AS_HELP_STRING([--with-postagger=[PATH]],
           [set path to frontend POS tagger (condara, mecab or juman)])],
       [AC_PATH_PROG(POS_TAGGER, [$withval], no)],
       [AC_PATH_PROG(POS_TAGGER, mecab, no)])

# mecab-config
AC_ARG_WITH([mecab-config],
       [AS_HELP_STRING([--with-mecab-config=[PATH]],
           [set path to mecab-config])],
       [AC_PATH_PROG(MECAB_CONFIG, [$withval], no)],
       [AC_PATH_PROG(MECAB_CONFIG, mecab-config, no)])

# posset
AC_ARG_WITH([mecab-dict],
        [AS_HELP_STRING([--with-mecab-dict=[DICT]],
            [set the MeCab dict id to train a parser (JUMAN|IPA|NAIST-J|UNI)])],
        [DICT_ID=$withval],
        [DICT_ID="JUMAN"])

AS_IF([test "x$enable_autopos_train" = "xno"] && [test "$DICT_ID" != "JUMAN"],
  [AC_MSG_ERROR(Only JUMAN gold POSs are provided in Kyoto or KNB Corpus)])

KNBC_CONV=
KYOTO_CONV=
UNIVERSAL_CONV=
JDEPP_CPPFLAGS=
MECAB_DICT=
POS_TAGGER_ID=mecab
if [test "x$enable_autopos_train" = "xyes"]; then
  AS_IF([test "x$POS_TAGGER" = "xno"],
      [AC_MSG_ERROR(cannot find executable POS tagger: ${POS_TAGGER}
                  set --disable-autopos-train for testing a parser)])
  if [test $POS_TAGGER = "./condara"]; then
    POS_TAGGER_ID=condara
    REPLACE="${PYTHON} \$(abs_top_srcdir)/tools/replace_pos.py ${POS_TAGGER}"
  else
    POS_TAGGER_ID=`2>&1 $POS_TAGGER -v | $AWK 'NR == 1 { print $1 }'`
    REPLACE="${PYTHON} \$(abs_top_srcdir)/tools/replace_pos.py ${POS_TAGGER}"
  fi
  KNBC_CONV="${PYTHON} \$(abs_top_srcdir)/tools/knbc2kyoto.py KNP | "
  UNIVERSAL_CONV="${PYTHON} \$(abs_top_srcdir)/tools/conll2kyoto.py KNP | ${ICONV} -f UTF-8 -t EUC-JP --unicode-subst=〓 | "
  if [test "$POS_TAGGER_ID" = "mecab"]; then
    AS_IF([test "x$MECAB_CONFIG" = "xno"],
      [AC_MSG_ERROR(cannot find executable mecab-config: ${MECAB_CONFIG})])
    AC_DEFINE([USE_MECAB],   [1],    [MeCab as morphological analyzer])
    MECAB_DICT=`$MECAB_CONFIG --dicdir`/`echo $DICT_ID | tr "A-Z" "a-z"`dic
    AS_IF([! test -e $MECAB_DICT],
      [AC_MSG_ERROR("${MECAB_DICT}" not found)])
    if [test "$DICT_ID" = "UNI"]; then
      AC_DEFINE([USE_UNI_POS], [1], [UNI POS set])
      AC_DEFINE([SURFACE_END], ['\t'], [MeCab separater after surface string])
      AC_DEFINE([FEATURE_SEP], ['\t'], [MeCab separater between features])
      AC_DEFINE([FEATURE_SEP_UNI], ['-'], [separater between POS1-4])
    else
      if [test "$DICT_ID" = "JUMAN"]; then
        AC_DEFINE([USE_JUMAN_POS], [1], [JUMAN POS set])
      elif [test "$DICT_ID" = "IPA"] || [test "$DICT_ID" = "NAIST-J"]; then
        AC_DEFINE([USE_IPA_POS], [1], [IPA POS set])
      else
        AC_MSG_ERROR(unknown dict: ${DICT_ID})]
      fi
      AC_DEFINE([SURFACE_END], ['\t'], [MeCab separater after surface string])
      AC_DEFINE([FEATURE_SEP], [','],  [MeCab separater between features])
    fi
    REPLACE+=" -d ${MECAB_DICT}"
  elif [test $POS_TAGGER_ID = "juman"]; then
    AC_DEFINE([USE_JUMAN],     [1], [JUMAN as morphological analyzer])
    AC_DEFINE([USE_JUMAN_POS], [1], [JUMAN POS set])
    AC_DEFINE([SURFACE_END], [' '], [JUMAN separater after surface string])
    AC_DEFINE([FEATURE_SEP], [' '], [JUMAN separater between features])
    REPLACE+=" -b"
  elif [test $POS_TAGGER_ID = "condara"]; then
    AC_DEFINE([USE_CONDARA],   [1], [CONDARA as morphological analyzer])
    AC_DEFINE([USE_JUMAN_POS], [1], [JUMAN POS set])
    AC_DEFINE([SURFACE_END], ['\t'], [CONDARA separater after surface string])
    AC_DEFINE([FEATURE_SEP], [','],  [CONDARA separater between features])
    REPLACE+=" -m condara_model"
  else
    AC_MSG_ERROR([unsupported POS tagger: ${POS_TAGGER_ID}])
  fi
  KNBC_CONV+=$REPLACE
  KYOTO_CONV+=$REPLACE
  UNIVERSAL_CONV+=$REPLACE
else
  AC_DEFINE([USE_MECAB],     [1],    [MeCab as morphological analyzer])
  AC_DEFINE([USE_JUMAN_POS], [1],    [JUMAN POS set])
  AC_DEFINE([SURFACE_END],   ['\t'], [MeCab separater after surface string])
  AC_DEFINE([FEATURE_SEP],   [','],  [MeCab separater between features])
  KNBC_CONV="${PYTHON} \$(abs_top_srcdir)/tools/knbc2kyoto.py"
  KYOTO_CONV="${AWK} '!/^(\#|\*|E)/ {\$\$0 = \$\$1\"\t\"\$\$4\",\"\$\$5\",\"\$\$6\",\"\$\$7\",\"(\$\$3 == \"*\" ? \$\$1 : \$\$3)\",\"\$\$2\",*\"}; 1'"
fi
AC_SUBST(KNBC_CONV)
AC_SUBST(UNIVERSAL_CONV)

JDEPP_LDFLAGS=
# enable a stand alone parser
AC_ARG_ENABLE([standalone],
        [AS_HELP_STRING([--enable-standalone],
            [build a standalone parser (default=no)])],
        [],
        [enable_standalone="no"])
if [test "x$enable_standalone" != "xno"]; then
  if [test "$POS_TAGGER_ID" = "mecab"]; then
    AC_DEFINE([USE_AS_STANDALONE], [1], [standalone parser])
    MECAB_DICT=`$MECAB_CONFIG --dicdir`/`echo $DICT_ID | tr "A-Z" "a-z"`dic
    JDEPP_CPPFLAGS+=" -DMECAB_DICT=\\\"${MECAB_DICT}\\\""
    JDEPP_LDFLAGS+=" -lmecab"
  else
    AC_MSG_ERROR(J.DepP cannot integrate CONDARA|JUMAN to build a standalone parser.)
  fi
fi

# default classifier
AC_ARG_WITH([default-classifier],
        [AS_HELP_STRING([--with-default-classifier=[IMPL]],
            [set implementation of weight trie (PKE|FST|PMT)])],
        [DEFAULT_CLASSIFIER=$withval],
        [DEFAULT_CLASSIFIER="FST"])

# classifiers
CHUNKER_LEARNER_OPT=
CHUNKER_CLASSIFIER_OPT=
PARSER_LEARNER_OPT=
PARSER_CLASSIFIER_OPT=
AC_ARG_WITH([classifier],
        [AS_HELP_STRING([--with-classifier=[type]],
            [use classifier training/testing option (Linear|2ndPolyFST|3rdPolyPMT)])],
        [CLASSIFIER=$withval],
        [CLASSIFIER=2ndPolyFST])

if [test "$CLASSIFIER" = "Linear"]; then
  AC_DEFINE([USE_PKE_AS_DEFAULT], [1], [PKE as default classifier]) # dummy
  AC_DEFINE_UNQUOTED([DEFAULT_CLASSIFIER], PKE, [default classifier])
  CHUNKER_LEARNER_OPT="-t 0 -c 0.01 -i 40 -P"
  PARSER_LEARNER_OPT="-t 0 -c 0.002 -i 40 -P"
elif [test "$CLASSIFIER" = "2ndPolyFST"]; then
  AC_DEFINE([USE_FST_AS_DEFAULT], [1], [FST as default classifier])
  AC_DEFINE_UNQUOTED([DEFAULT_CLASSIFIER], FST, [default classifier])
  CHUNKER_LEARNER_OPT="-t 1 -d 2 -c 0.0008 -i 40 -p"
  PARSER_LEARNER_OPT="-t 1 -d 2 -c 0.00005 -i 40 -p"
elif [test "$CLASSIFIER" = "3rdPolyPMT"]; then
  AC_DEFINE([USE_PMT_AS_DEFAULT], [1], [PMT as default classifier])
  AC_DEFINE_UNQUOTED([DEFAULT_CLASSIFIER], PMT, [default classifier])
  AS_IF([test $TRIE_IMPL != "cedar"],
        [AC_MSG_ERROR(3rdPolyPMT classifier needs cedar as trie implementation)])
  CHUNKER_LEARNER_OPT="-t 1 -d 3 -c 0.00002 -i 40 -kp"
  PARSER_LEARNER_OPT="-t 1 -d 3 -c 0.000002 -i 40 -kp"
else
  AC_MSG_ERROR(unsupported classifier: ${DEFAULT_CLASSIFIER})
fi

# training corpus (default model)
AC_ARG_WITH([corpus],
        [AS_HELP_STRING([--with-corpus=[corpus]],
            [set the training corpus (kyoto|kyoto-partial|knbc|universal|kyoto+knbc)])],
        [CORPUS=$withval],
        [CORPUS=knbc])

KYOTO_CORPUS_DIR=${PWD}/KyotoCorpus4.0
KNBC_CORPUS_DIR=${PWD}/KNBC_v1.0_090925
UNIVERSAL_CORPUS_DIR=${PWD}/universal_treebanks_v2.0

if [test "$CORPUS" = "kyoto"] || [test "$CORPUS" = "kyoto-partial"] || [test "$CORPUS" = "kyoto+knbc"]; then
  if [test "$CLASSIFIER" = "2ndPolyFST"]; then
    CHUNKER_CLASSIFIER_OPT="-s 0.02 -i 7"
    PARSER_CLASSIFIER_OPT="-s 0.015 -i 7"
  elif [test "$CLASSIFIER" = "3rdPolyPMT"]; then
    CHUNKER_CLASSIFIER_OPT="-t 3 -s 0.005 -p 20"
    PARSER_CLASSIFIER_OPT="-t 3 -s 0.002 -p 20"
  fi
  if [test "$CORPUS" = "kyoto-partial"]; then
    KYOTO_CONV="${AWK} '!/^(\#|\*|E)/ {\$\$0 = \$\$2\"\t\"\$\$4\",\"\$\$5\",\"\$\$6\",\"\$\$7\",\"(\$\$3 == \"*\" ? \$\$2 : \$\$3)\",\"\$\$2\",*\"}; 1'"
    AC_DEFINE([USE_KYOTO_PARTIAL], [1], [USE KyotoCorpus4.0 without Maichini news articles])
    AS_IF([test "x$enable_autopos_train" = "xyes"],
      [AC_MSG_ERROR(cannot assign auto POSs for --with-corpus=kyoto-partial)])
  fi
elif [test "$CORPUS" = "knbc"] || [test "$CORPUS" = "universal"]; then
  if [test "$CLASSIFIER" = "2ndPolyFST"]; then
    CHUNKER_CLASSIFIER_OPT="-s 0.02 -i 5"
    PARSER_CLASSIFIER_OPT="-s 0.005 -i 5"
  elif [test "$CLASSIFIER" = "3rdPolyPMT"]; then
    CHUNKER_CLASSIFIER_OPT="-s 0.005 -p 20"
    PARSER_CLASSIFIER_OPT="-s 0.002 -p 20"
  fi
  if [test "$CORPUS" = "universal"]; then
    AS_IF([test "x$enable_autopos_train" = "xno"],
      [AC_MSG_ERROR(cannot use gold POSs in --with-corpus=universal)])
  fi
else
  AC_MSG_ERROR(unsupported corpus: ${CORPUS})
fi
AC_SUBST(CLASSIFIER)

AC_SUBST(KYOTO_CONV)
AC_SUBST(CHUNKER_LEARNER_OPT)
AC_SUBST(CHUNKER_CLASSIFIER_OPT)
AC_SUBST(PARSER_LEARNER_OPT)
AC_SUBST(PARSER_CLASSIFIER_OPT)

JDEPP_MODEL_DIR="${libdir}/jdepp/model"
JDEPP_CPPFLAGS+=" -DJDEPP_DEFAULT_MODEL=\\\"${JDEPP_MODEL_DIR}/${CORPUS}\\\""
AC_SUBST(CORPUS)
AC_SUBST(KYOTO_CORPUS_DIR)
AC_SUBST(KNBC_CORPUS_DIR)
AC_SUBST(UNIVERSAL_CORPUS_DIR)
AC_SUBST(JDEPP_CPPFLAGS)
AC_SUBST(JDEPP_MODEL_DIR)

JDEPP_OBJ=
# RTDSC timer
AC_ARG_ENABLE([timer],
        [AS_HELP_STRING([--enable-timer],
            [use RDTSC timer (default=yes)])],
        [],
        [enable_timer="yes"])
if [test "x$enable_timer" != "xno"]; then
  AC_DEFINE([USE_TIMER], [1], [timer support])
  JDEPP_OBJ+=" timer.${OBJEXT}"
fi

# C++11 unordered_map
AC_ARG_ENABLE([hash],
        [AS_HELP_STRING([--enable-hash],
            [use C++11 unordered_map (default=yes)])],
        [],
        [enable_hash="yes"])
AS_IF([test "x$enable_hash" != "xno" || test "$TRIE_IMPL" = "hash"],
  [AC_CHECK_HEADERS([unordered_map],
    [AC_DEFINE([USE_HASH], [1], [hash support])],
    [AC_CHECK_HEADERS([tr1/unordered_map],
      [AC_DEFINE([USE_TR1_HASH], [1], [hash support (TR1)])],
      [AC_MSG_WARN(cannot find unordered_map; disabled)])])])

# C++11 mt19937
AC_ARG_ENABLE([mt19937],
        [AS_HELP_STRING([--enable-mt19937],
            [use C++11 mt19937 to shuffle examples (default=no)])],
        [],
        [enable_mt19937="no"])
AS_IF([test "x$enable_mt19937" != "xno"],
  [AC_CHECK_HEADERS([random],
    [AC_DEFINE([USE_MT19937], [1], [mt19937 support])],
    [AC_CHECK_HEADERS([tr1/random],
      [AC_DEFINE([USE_TR1_MT19937], [1], [mt19937 support])],
      [AC_MSG_ERROR(cannot find random; try --disable-mt19937)])])])

# abuse trie to encode feature (sequence) weight (22-bit precision)
AC_ARG_ENABLE([abuse-trie],
        [AS_HELP_STRING([--enable-abuse-trie],
            [abuse trie to store feature weights (default=no)])],
        [],
        [enable_abuse_trie="no"])
AS_IF([test "x$enable_abuse_trie" != "xno"],
    [AC_DEFINE([ABUSE_TRIE], [1], [abuse trie to store feature weights])])

# use float as floating-point numbers
AC_ARG_ENABLE([float],
        [AS_HELP_STRING([--enable-float],
            [use float as floating-point numbers (default=no)])],
        [],
        [enable_float="no"])
AS_IF([test "x$enable_float" != "xno"],
    [AC_DEFINE([USE_FLOAT], [1], [float as floating-point numbers])])

# enable model suffixes
AC_ARG_ENABLE([model-suffix],
        [AS_HELP_STRING([--enable-model-suffix],
            [add unique suffixes to kernel models (default=yes)])],
        [],
        [enable_model_suffix="no"])
AS_IF([test "x$enable_model_suffix" != "xno"],
  [AC_DEFINE([USE_MODEL_SUFFIX], [1], [suffix for approximated kernel models])])

# enable popcnt (SSE4.2)
AC_ARG_ENABLE([popcnt],
              [AS_HELP_STRING([--enable-popcnt],
                              [use popcnt (SSE4.2) [default=yes]])],
              [],
              [enable_popcnt="yes"])
if [test "x${enable_popcnt}" != "xno"]; then
  orig_cflags=$CXXFLAGS
  CXXFLAGS="-msse4.2 $orig_cflags -O0"
  AC_RUN_IFELSE([AC_LANG_PROGRAM([#include <smmintrin.h>],
                                 [return _mm_popcnt_u64 (0);])],
     [AC_DEFINE([USE_SSE4_2_POPCNT], [1], [use SSE 4.2 popcnt])
      CXXFLAGS="-msse4.2 $orig_cflags"],
     [AC_MSG_WARN([16bit table-driven popcount is used instead of SSE4.2.])
      CXXFLAGS=$orig_cflags])
fi

# enable pruning
AC_ARG_ENABLE([pruning],
        [AS_HELP_STRING([--enable-pruning],
            [enable pruning (default=yes)])],
        [],
        [enable_pruning="yes"])
AS_IF([test "x$enable_pruning" != "xno"],
  [AC_DEFINE([USE_PRUNING], [1], [enable pruning])])

# enable array trie
AC_ARG_ENABLE([array-trie],
        [AS_HELP_STRING([--enable-array-trie],
            [enable array trie (default=yes)])],
        [],
        [enable_array_trie="yes"])
AS_IF([test "x$enable_array_trie" != "xno"],
  [AC_DEFINE([USE_ARRAY_TRIE], [1], [enable array trie])])

# enable lfu pmt type
AC_ARG_ENABLE([lfu-pmt],
        [AS_HELP_STRING([--enable-lfu-pmt],
            [enable lfu pmt (default=no)])],
        [],
        [enable_lfu_pmt="no"])
AS_IF([test "x$enable_lfu_pmt" != "xno"],
  [AC_DEFINE([USE_LFU_PMT], [1], [enable LFU PMT])])

# enable profiling
AC_ARG_ENABLE([profiling],
        [AS_HELP_STRING([--enable-profiling],
            [enable profiling (default=no)])],
        [],
        [enable_profiling="no"])
AS_IF([test "x$enable_profiling" != "xno"],
    [AC_DEFINE([USE_PROFILING], [1], [enable profiling])])

# enable debug
AC_ARG_ENABLE([debug],
        [AS_HELP_STRING([--enable-debug],
            [enable debug (default=no)])],
        [],
        [enable_debug="no"])
AS_IF([test "x$enable_debug" = "xno"],
    [AC_DEFINE([NDEBUG], [1], [disable debug])])

# enable opal training
AC_ARG_ENABLE([opal],
        [AS_HELP_STRING([--enable-opal],
            [enable training with opal (default=yes)])],
        [],
        [enable_opal="yes"])
if [test "x$enable_opal" != "xno"]; then
  AC_DEFINE([USE_OPAL], [1], [enable training with opal])
  AC_DEFINE([MAX_NUM_CLASSES], [1024], [the number of classes])
fi

# enable svm training
AC_ARG_ENABLE([svm],
        [AS_HELP_STRING([--enable-svm],
            [enable training with TinySVM (default=no)])],
        [],
        [enable_svm="no"])
if [test "x$enable_svm" != "xno"]; then
  orig_cflags=$CXXFLAGS
  CXXFLAGS=-ltinysvm
    AC_LINK_IFELSE([AC_LANG_PROGRAM([#include <tinysvm.h>],
        [TinySVM::Model dummy;])],
      [AC_DEFINE([USE_SVM], [1], [enable training with TinySVM])],
      [AC_MSG_ERROR(cannot link -ltinysvm)])
  JDEPP_LDFLAGS+=" -ltinysvm"
fi

if [test "x$enable_opal" != "xno"] || [test "x$enable_svm" != "xno"]; then
  AC_DEFINE([USE_KERNEL], [1], [support kernel model])
  JDEPP_OBJ+=" kernel.${OBJEXT}"
fi
AC_SUBST(JDEPP_LDFLAGS)
AC_SUBST(JDEPP_OBJ)

# enable maxent training; partially disabled
AC_ARG_ENABLE([maxent],
        [AS_HELP_STRING([--enable-maxent],
            [enable training with Tsuruoka's MaxEnt (default=no)])],
        [],
        [enable_maxent="no"])
if [test "x$enable_maxent" != "xno"]; then
  AC_DEFINE([USE_MAXENT], [1], [enable training with Tsuruoka's maxent])
  AC_DEFINE([USE_LINEAR], [1], [support linear model])
  JDEPP_OBJ+=" maxent.o lbfgs.o owlqn.o sgd.o linear.${OBJEXT}"
fi

if [test "x$enable_opal" == "xno"] && [test "x$enable_svm" == "xno"] && [test "x$enable_maxent" == "xno"]; then
  AC_MSG_ERROR(specify the library to train a parser.)
fi

AC_CONFIG_FILES([Makefile
                 src/Makefile
                 tools/Makefile])
AC_OUTPUT
