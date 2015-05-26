#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([pecco], [2014-06-22], [ynaga@tkl.iis.u-tokyo.ac.jp])
AM_INIT_AUTOMAKE([-Wall foreign])
AC_CONFIG_SRCDIR([config.h.in])
AC_CONFIG_HEADERS([config.h])
AC_LANG([C++])

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC

# Checks for libraries.

# Checks for header files.
AC_CHECK_HEADERS([stdint.h sys/time.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL
AC_C_INLINE
AC_TYPE_INT64_T
AC_TYPE_SIZE_T
AC_TYPE_SSIZE_T
AC_TYPE_UINT16_T
AC_TYPE_UINT64_T
AC_TYPE_UINT8_T

# Checks for library functions.
AC_FUNC_STRTOD
AC_CHECK_FUNCS([gettimeofday memset pow strstr strtol strtoul])

AC_ARG_ENABLE(64bit,
        [AS_HELP_STRING([--enable-64bit],
            [build 64bit version])],
        [],
        [enable_64bit="yes"])

if [test "x$enable_64bit" = "xyes"]; then
  orig_cflags=$CXXFLAGS
  CXXFLAGS=-m64
  AC_RUN_IFELSE([AC_LANG_PROGRAM([],
     [return sizeof (void*) == 8 ? 0 : 1;])],
     [CXXFLAGS="-m64 $orig_cflags"],
     [AC_MSG_ERROR([Don't know how to build a 64-bit object; try --disable-64bit])
      CXXFLAGS=$orig_cflags])
fi

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

# default classifier
AC_ARG_WITH([default-classifier],
        [AS_HELP_STRING([--with-default-classifier=[IMPL]],
            [set implementation of weight trie (PKE|FST|PMT)])],
        [DEFAULT_CLASSIFIER=$withval],
        [DEFAULT_CLASSIFIER="FST"])

if [test $DEFAULT_CLASSIFIER = "PKE"]; then
  AC_DEFINE([USE_PKE_AS_DEFAULT], [1], [PKE as default classifier])
elif [test $DEFAULT_CLASSIFIER = "FST"]; then
  AC_DEFINE([USE_FST_AS_DEFAULT], [1], [FST as default classifier])
elif [test $DEFAULT_CLASSIFIER = "PMT"]; then
  AC_DEFINE([USE_PMT_AS_DEFAULT], [1], [PMT as default classifier])
  AS_IF([test "x$TRIE_IMPL" != "xcedar"] && [test "x$DEFAULT_CLASSIFIER" = "xPMT"],
    [AC_MSG_ERROR(PMT requires cedar as trie implementation)])
else
  AC_MSG_ERROR(unknown classifier: ${DEFAULT_CLASSIFIER})
fi

AC_DEFINE_UNQUOTED([DEFAULT_CLASSIFIER], $DEFAULT_CLASSIFIER, [default classifier])

# RTDSC timer
PECCO_OBJ=
PECCO_SRC=
AC_ARG_ENABLE([timer],
        [AS_HELP_STRING([--enable-timer],
            [use RDTSC timer (default=yes)])],
        [],
        [enable_timer="yes"])
if [test "x$enable_timer" != "xno"]; then
  AC_DEFINE([USE_TIMER], [1], [timer support])
  PECCO_OBJ+=" timer.${OBJEXT}"
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

# support kernel model
AC_ARG_ENABLE([kernel],
        [AS_HELP_STRING([--enable-kernel],
            [support kernel model (default=yes)])],
        [],
        [enable_kernel="yes"])
if [test "x$enable_kernel" != "xno"]; then
  AC_DEFINE([USE_KERNEL], [1], [support kernel model])
  PECCO_OBJ+=" kernel.${OBJEXT}"
fi

# support linear model
AC_ARG_ENABLE([linear],
        [AS_HELP_STRING([--enable-linear],
            [support linear model (default=yes)])],
        [],
        [enable_float="yes"])
if [test "x$enable_linear" != "xno"]; then
  AC_DEFINE([USE_LINEAR], [1], [support linear model])
  PECCO_OBJ+=" linear.${OBJEXT}"
fi
AC_SUBST(PECCO_OBJ)

AS_IF([test "x$enable_kernel" = "xno"] && [test "x$enable_linear" = "xno"],
  [AC_MSG_ERROR(need to enable at least either kernel or linear model)])

# enable model suffixes
AC_ARG_ENABLE([model-suffix],
        [AS_HELP_STRING([--enable-model-suffix],
            [add unique suffixes to kernel models (default=yes)])],
        [],
        [enable_model_suffix="yes"])
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
            [enable array trie (default=no)])],
        [],
        [enable_array_trie="no"])
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

AC_CONFIG_FILES([Makefile
                 src/Makefile
                 tools/Makefile])
AC_OUTPUT
