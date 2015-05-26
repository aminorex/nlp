#!/usr/bin/env python
import re
from distutils.core import setup, Extension

cflags = ['-DHAVE_CONFIG_H']
if re.search (r'^#define USE_SSE4_2_POPCNT 1$', open ("../../config.h").read (), re.MULTILINE):
    cflags += ['-msse4.2']

setup (name = "opal-python",
       py_modules = ['opal'],
       ext_modules = [Extension ('_opal',
                                 ['opal_wrap.cxx', '../../src/timer.cc'],
                                 include_dirs=['../..', '../../src'],
                                 extra_compile_args=cflags)])
