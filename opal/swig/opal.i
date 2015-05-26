%module opal

#ifdef USE_MULTICLASS
%{ #define USE_MULTICLASS 1 %}
#endif

%{
#undef vwarn
#include "timer.h"
#include "pa.h"
%}

#ifdef SWIGPERL
%typemap (typecheck) (opal::fv_t &) {
  if (! SvROK ($input) || SvTYPE (SvRV ($input)) != SVt_PVAV)
    croak ("not a list");
}

%typemap (in) (opal::fv_t &) (opal::fv_t fv) {
  if (! SvROK ($input) || SvTYPE (SvRV ($input)) != SVt_PVAV)
    croak ("not a list");
  int len = av_len (reinterpret_cast <AV *> (SvRV ($input))) + 1;
  fv.reserve (len);
  for (int i = 0; i < len; ++i) {
    SV **aval = av_fetch (reinterpret_cast <AV *> (SvRV ($input)), i, 0);
    fv.push_back (SvUV (reinterpret_cast <SV *> (*aval)));
  }
  $1 = &fv;
}

%typemap (typecheck) (std::vector <const char*> &) {
  if (! SvROK ($input) || SvTYPE (SvRV ($input)) != SVt_PVAV)
    croak ("not a list");
}

%typemap (in) (std::vector <const char*> &) (std::vector <const char*> fv) {
  if (! SvROK ($input) || SvTYPE (SvRV ($input)) != SVt_PVAV)
    croak ("not a list");
  int len = av_len (reinterpret_cast <AV *> (SvRV ($input))) + 1;
  fv.reserve (len);
  for (int i = 0; i < len; ++i) {
    SV **aval = av_fetch (reinterpret_cast <AV *> (SvRV ($input)), i, 0);
    fv.push_back (reinterpret_cast <char*> (SvPV (reinterpret_cast <SV *> (*aval), PL_na)));
  }
  $1 = &fv;
}

%typemap (typecheck) (char **) {
  if (! SvROK ($input) || SvTYPE (SvRV ($input)) != SVt_PVAV)
    croak ("not a list");
}

%typemap (in) (char **) {
  if (! SvROK ($input) || SvTYPE (SvRV ($input)) != SVt_PVAV)
    croak ("not a list");
  int len = av_len (reinterpret_cast <AV *> (SvRV ($input))) + 1;
  $1 = new char*[len + 1];
  int i = 0;
  for (; i < len; ++i) {
    SV ** aval = av_fetch (reinterpret_cast <AV *> (SvRV ($input)), i, 0);
    $1[i] = reinterpret_cast <char *> (SvPV (*aval, PL_na));
  }
  $1[i] = 0;
}
#endif

#ifdef SWIGPYTHON
%typemap (typecheck) (opal::fv_t &) {
  if (! PyList_Check ($input))
    { PyErr_SetString (PyExc_TypeError, "not a list"); return 0; }
}

%typemap (in) (opal::fv_t &) (opal::fv_t fv) {
  if (! PyList_Check ($input))
    { PyErr_SetString (PyExc_TypeError, "not a list"); return 0; }
  int len = PyList_Size ($input);
  fv.reserve (len);
  for (int i = 0; i < len; ++i) {
    PyObject *po = PyList_GetItem ($input, i);
    if (! PyInt_Check (po))
      { PyErr_SetString (PyExc_TypeError, "not an int"); return 0; }
    fv.push_back (PyInt_AsLong (po));
  }
  $1 = &fv;
}

%typemap (in) (std::vector <const char*> &) (std::vector <const char*> fv) {
  if (! PyList_Check ($input))
    { PyErr_SetString (PyExc_TypeError, "not a list"); return 0; }
  int len = PyList_Size ($input);
  fv.reserve (len);
  for (int i = 0; i < len; ++i) {
    PyObject *po = PyList_GetItem ($input, i);
    if (! PyString_Check (po))
      { PyErr_SetString (PyExc_TypeError, "not a string"); return 0; }
    fv.push_back (PyString_AsString (po));
  }
  $1 = &fv;
}

%typemap (typecheck) (char **) {
  if (! PyList_Check ($input))
    { PyErr_SetString (PyExc_TypeError, "not a list"); return 0; }
}

%typemap (in) (char **) {
  if (! PyList_Check ($input))
    { PyErr_SetString (PyExc_TypeError, "not a list"); return 0; }
  int len = PyList_Size ($input);
  $1 = new char*[len + 1];
  int i = 0;
  for (; i < len; ++i) {
    PyObject *po = PyList_GetItem ($input, i);
    if (! PyString_Check (po))
      { PyErr_SetString (PyExc_TypeError, "not a string"); delete [] $1; return 0; }
    $1[i] = PyString_AsString (po);
  }
  $1[i] = 0;
}
#endif

#ifdef SWIGRUBY
%typemap (typecheck) (opal::fv_t &) {
  Check_Type ($input, T_ARRAY);
}

%typemap (in) (opal::fv_t &) (opal::fv_t fv) {
  Check_Type ($input, T_ARRAY);
  int len = RARRAY_LEN ($input);
  fv.reserve (len);
  for (int i = 0; i < len; ++i) {
    VALUE ro = rb_ary_entry ($input, i);
    Check_Type (ro, T_FIXNUM);
    fv.push_back (FIX2UINT (ro));
  }
  $1 = &fv;
}

%typemap (in) (std::vector <const char*> &) (std::vector <const char*> fv) {
  Check_Type ($input, T_ARRAY);
  int len = RARRAY_LEN ($input);
  fv.reserve (len);
  for (int i = 0; i < len; ++i) {
    VALUE ro = rb_ary_entry ($input, i);
    Check_Type (ro, T_STRING);
    fv.push_back (StringValuePtr (ro));
  }
  $1 = &fv;
}

%typemap (typecheck) (char **) {
  Check_Type ($input, T_ARRAY);
}

%typemap (in) (char **) {
  Check_Type ($input, T_ARRAY);
  int len = RARRAY_LEN ($input);
  $1 = new char*[len + 1];
  int i = 0;
  for (i = 0; i < len; ++i) {
    VALUE ro = rb_ary_entry ($input, i);
    Check_Type (ro, T_STRING);
    $1[i]= StringValuePtr (ro);
  }
  $1[i] = 0;
}
#endif

#ifdef SWIGLUA
%typemap (typecheck) (opal::fv_t &) {
  if (! lua_istable (L, $input))
    { std::fprintf (stderr, "not a list\n"); return 0; }
}

%typemap (in) (opal::fv_t &) (opal::fv_t fv) {
  if (! lua_istable (L, $input))
    { std::fprintf (stderr, "not a list\n"); return 0; }
  int i = 1;
  while (1) {
    lua_rawgeti (L, $input, i);
    if (lua_isnil (L, -1)) { lua_pop (L, 1); break; }
    if (! lua_isnumber (L, -1))
      { std::fprintf (stderr, "not a int\n"); lua_pop (L, 1); return 0; }
    fv.push_back (static_cast <opal::uint> (lua_tonumber (L, -1)));
    lua_pop (L, 1);
    ++i;
  }
  $1 = &fv;
}

%typemap (in) (std::vector <const char*> &) (std::vector <const char*> fv) {
  if (! lua_istable (L, $input))
    { std::fprintf (stderr, "not a list\n"); return 0; }
  int i = 1;
  while (1) {
    lua_rawgeti (L, $input, i);
    if (lua_isnil (L, -1)) { lua_pop (L, 1); break; }
    if (! lua_isstring (L, -1))
      { std::fprintf (stderr, "not a string\n"); lua_pop (L, 1); return 0; }
    fv.push_back (lua_tostring (L, -1));
    lua_pop (L, 1);
    ++i;
  }
  $1 = &fv;
}

%typemap (typecheck) (char **) {
  if (! lua_istable (L, $input))
    { std::fprintf (stderr, "not a list\n"); return 0; }
}

%typemap (in) (char **) {
  if (! lua_istable (L, $input))
    { std::fprintf (stderr, "not a list\n"); return 0; }
  int i = 1;
  while (1) {
    lua_rawgeti (L, $input, i);
    if (lua_isnil (L, -1)) { lua_pop (L, 1); break; }
    lua_pop (L, 1);
    ++i;
  }
  int len = i - 1;
  $1 = new char*[len + 1];
  for (i = 0; i < len; ++i) {
    lua_rawgeti (L, $input, i + 1);
    if (! lua_isstring (L, -1))
      { std::fprintf (stderr, "not a string\n"); lua_pop (L, 1); return 0; }
    $1[i] = const_cast <char *> (lua_tostring (L, -1));
    lua_pop (L, 1);
  }
  $1[i] = 0;
}
#endif

%typemap(freearg) (char **) { delete [] $1; }

%include "../config.h"
%include "../src/timer.h"
%include "../src/pa.h"
