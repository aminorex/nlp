#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([opal], [2015-02-08], [ynaga@tkl.iis.u-tokyo.ac.jp])
AM_INIT_AUTOMAKE([-Wall foreign])
AC_CONFIG_SRCDIR([config.h.in])
AC_CONFIG_HEADERS([config.h])
AC_LANG([C++])

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC

# Checks for libraries.

# Checks for header files.
AC_CHECK_HEADERS([stdint.h sys/time.h unistd.h])

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
AC_CHECK_FUNCS([floor gettimeofday memchr memset pow strstr strtol])

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
    ])
fi

# MAX_NUM_CLASSES
AC_ARG_WITH([max-num-classes],
        [AS_HELP_STRING([--with-num-classes=[NUM]],
                    [set the maximum number of classes (default=1024)])],
        [MAX_NUM_CLASSES=$withval],
        [MAX_NUM_CLASSES=65536]
)
AC_DEFINE_UNQUOTED([MAX_NUM_CLASSES], [$MAX_NUM_CLASSES], [the limit of the number of classes])

OPAL_OBJ=
OPAL_SRC=
# RTDSC timer
AC_ARG_ENABLE([timer],
        [AS_HELP_STRING([--enable-timer],
            [use RDTSC timer (default=yes)])],
        [],
        [enable_timer="yes"])
if [test "x$enable_timer" != "xno"]; then
  AC_DEFINE([USE_TIMER], [1], [timer support])
  OPAL_OBJ+=" timer.${OBJEXT}"
fi
AC_SUBST(OPAL_OBJ)

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

# OPENMP
AC_ARG_ENABLE([openmp],
        [AS_HELP_STRING([--enable-openmp],
            [use OPENMP for parallel training (default=no)])],
        [],
        [enable_openmp="no"])
if [test "x${enable_openmp}" != "xno"]; then
  orig_cflags=$CXXFLAGS
  CXXFLAGS="-fopenmp $orig_cflags -O0"
  AC_RUN_IFELSE([AC_LANG_PROGRAM([#include <omp.h>],
                                 [return 0;])],
     [CXXFLAGS="-fopenmp $orig_cflags"],
     [AC_MSG_ERROR([compiler doesn's support OpenMP; try --disable-openmp])])
fi

# data structure for weight trie
AC_ARG_WITH([trie-impl],
        [AS_HELP_STRING([--with-trie-impl=[IMPL]],
            [set implementation of weight trie (array|hash|map)])],
        [TRIE_IMPL=$withval],
        [TRIE_IMPL="array"])

if [test "$TRIE_IMPL" != "array"]; then
  AS_IF([test $TRIE_IMPL != "hash"] && test ["$TRIE_IMPL" != "map"],
    [AC_MSG_ERROR(unknown trie implementation: ${TRIE_IMPL})])
  AS_IF([test "$TRIE_IMPL" = "hash"],
    AS_IF([test "x$enable_hash" != "xno"],
      [AC_DEFINE([USE_HASH_TRIE], [1], [hash as implementation of weight trie])],
      [AC_MSG_ERROR(--with-trie-impl=hash requires --enable-hash)]),
    [AC_DEFINE([USE_MAP_TRIE], [1], [map as implementation of weight trie])])
fi

# use float as floating-point numbers
AC_ARG_ENABLE([float],
        [AS_HELP_STRING([--enable-float],
            [use float as floating-point numbers (default=no)])],
        [],
        [enable_float="no"])
AS_IF([test "x$enable_float" != "xno"],
  [AC_DEFINE([USE_FLOAT], [1], [float as floating-point numbers])])

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

# support string feature
AC_ARG_ENABLE([string-feature],
              [AS_HELP_STRING([--enable-string-feature],
                              [support string features (a bit slower) (default=no)])],
              [],
              [enable_string_feature="no"])
AS_IF([test "x$enable_string_feature" != "xno"],
  [AC_DEFINE([USE_STRING_FEATURE], [1], [use string feature])])

# kernel-based classifier with inverted indexing
AC_ARG_ENABLE([kernel-indexing],
        [AS_HELP_STRING([--enable-kernel-indexing],
            [build a classifier based on kernel indexing (default=no)])],
        [],
        [enable_kernel_indexing="no"])
if [test "x$enable_kernel_indexing" != "xno"]; then
  OPALK=opalk
  AC_SUBST(OPALK)
fi

# enable array trie
AC_ARG_ENABLE([array-trie],
        [AS_HELP_STRING([--enable-array-trie],
            [enable array trie (default=yes)])],
        [],
        [enable_array_trie="yes"])
AS_IF([test "x$enable_array_trie" != "xno"],
  [AC_DEFINE([USE_ARRAY_TRIE], [1], [enable array trie])])

# aggressive pruning (not so useful considering its space cost)
AC_ARG_ENABLE([aggressive-pruning],
              [AS_HELP_STRING([--enable-temporal-pruning],
                              [perform pruning using temporal bounds (default=no)])],
              [],
              [enable_temporal_pruning="no"])
AS_IF([test "x$enable_temporal_pruning" != "xno"],
  [AC_DEFINE([USE_AGGRESSIVE_PRUNING], [1], [use pruning using temporal bounds])])

# multi-class classifier
AC_ARG_ENABLE([multi],
        [AS_HELP_STRING([--enable-multi],
            [build a multi-class classifier as well (default=yes)])],
        [],
        [enable_multi="yes"])
if [test "x$enable_multi" != "xno"]; then
  OPAL_MULTI=opal-multi
  AC_SUBST(OPAL_MULTI)
  if [test "x$enable_kernel_indexing" != "xno"]; then
    OPALK_MULTI=opalk-multi
    AC_SUBST(OPALK_MULTI)
  fi
fi

AC_CONFIG_FILES([Makefile
                 src/Makefile])
AC_OUTPUT
