// rand_shuf -- in-place random shuffling for opal [event=Disk|Null]
//  $Id: rand_shuf.cc 1874 2015-01-29 11:47:40Z ynaga $
// Copyright (c) 2009-2015 Naoki Yoshinaga <ynaga@tkl.iis.u-tokyo.ac.jp>
#include <unistd.h>
#include <sys/resource.h>
#include <err.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>
#include <algorithm>

// random number generator
#ifdef USE_MT19937
#include <tr1/random>
struct rand_ {
  std::tr1::variate_generator <std::tr1::mt19937,
                               std::tr1::uniform_int <size_t> > gen;
  rand_ () : gen (std::tr1::mt19937 (), std::tr1::uniform_int <size_t> ()) {};
  long operator () (long max) { return gen (max); }
};
#else
struct rand_ { // Xorshift RNG; http://www.jstatsoft.org/v08/i14/paper
  size_t xor128 () {
    static size_t x (123456789), y (362436069), z (521288629), w (88675123);
    size_t t = (x ^ (x << 11)); x = y; y = z; z = w;
    return w = (w ^ (w >> 19)) ^ (t ^ (t >> 8));
  }
  size_t operator() (size_t max) { return xor128 () % max; }
};
#endif

#ifndef BUF_SIZE       // default chunk size for shuffling (1M)
#define BUF_SIZE (1 << 20)
#endif

#ifndef OPEN_MAX       // default # file descriptors
#define OPEN_MAX 20
#endif

#ifndef MAX_LINE_LEN   // maximum length of lines
#define MAX_LINE_LEN 65536
#endif

#ifndef TMP_DIR
#define TMP_DIR "/tmp" // default directory to store temporary files
#endif

static void shuffle_lines (FILE* fp, char* buf, size_t size, rand_& gen) {
  // load (partial) data on memory
  std::fseek (fp, 0, SEEK_SET); // flush here
  if (std::fread (&buf[0], sizeof (char), size, fp) == 0) std::exit (1);
  // shuffle
  std::vector <const char*> lns;
  for (char* p (&buf[0]), *end (&buf[size]); p != end; *p = '\0', ++p) {
    lns.push_back (p);
    while (*p != '\n') ++p;
  }
  std::random_shuffle (lns.begin (), lns.end (), gen);
  // overwrite & recover position
  for (std::vector <const char*>::iterator it = lns.begin ();
       it != lns.end (); ++it)
    std::fprintf (stdout, "%s\n", *it);
}

int main (int argc, char* argv[]) {
  // random number generator
  rand_ gen;
  // handle options
  size_t      buf_size = BUF_SIZE;
  const char* tmp_dir  = TMP_DIR;
  char*       in       = 0;
  for (int i = 1; i < argc; ++i) {
    if (std::strcmp (argv[i], "-h") == 0) {
      std::fprintf (stderr, "Usage: %s [-S size] [-T tmp_dir] [in]\n", argv[0]);
      return (0);
    } else if (std::strcmp (argv[i], "-S") == 0) {
      buf_size = 1;
      ++i; 
      char& c = argv[i][std::strlen (argv[i]) - 1];
      char* err;
      switch (c) {
        case 'G': buf_size <<= 10;
        case 'M': buf_size <<= 10;
        case 'K': buf_size <<= 10; c = '\0';
        default:  buf_size *= std::strtoul (argv[i], &err, 10);
          if (*err)
            errx (1, "invalid size in -S argument: %s", argv[i]);
      }
    } else if (std::strcmp (argv[i], "-T") == 0) {
      tmp_dir = argv[++i];
    } else {
      in = argv[i];
    }
  }
  char* tmp_fn = new char [std::strlen (tmp_dir) + 12];
  // divide & conquer
  // prepare bin
  FILE* fp = in ? std::fopen (in, "rb") : stdin;
  if (! fp)
    errx (1, "no such file: %s", in);
  struct rlimit rlim;
  size_t ntmp_limit
    = static_cast <size_t> ((getrlimit (RLIMIT_NOFILE, &rlim) == 0 ? rlim.rlim_cur : OPEN_MAX) - 4);
  // set # temporary files
  size_t ntmp = ntmp_limit;
  if (in) {
    std::fseek (fp, 0, SEEK_END);
    ntmp = std::min (static_cast <size_t> (std::ftell (fp)) / buf_size + 1, ntmp);
    std::fseek (fp, 0, SEEK_SET); // seek
    std::fclose (fp);
    fp = std::fopen (in, "r");
  }
  std::vector <FILE*> tmpfps;
  tmpfps.reserve (ntmp);
  for (size_t i = 0; i < ntmp; ++i) {
    std::sprintf (&tmp_fn[0], "%s/shufXXXXXX", tmp_dir);
    tmpfps.push_back (fdopen (mkstemp (tmp_fn), "w+"));
    unlink (tmp_fn);
  }
  delete [] tmp_fn;
  // divide & conquer
  char line[MAX_LINE_LEN];
  while ((std::fgets (&line[0], MAX_LINE_LEN, fp)) != NULL) {
    FILE* writer = tmpfps[gen (ntmp)];
    size_t read = std::strlen (&line[0]);
    if (line[read-1] != '\n') {
      if (std::feof (fp)) {
        std::fwrite (&line[0], sizeof (char), read, writer);
        std::fprintf (writer, "\n");
        warnx ("WARNING: line feeder is appended");
      } else {
        errx (1, "Buffer Overflow; increase MAX_LINE_LEN");
      }
    } else {
      std::fwrite (&line[0], sizeof (char), read, writer);
    }
  }
  std::fclose (fp);
  // conquer
  size_t size_max = 0;
  for (std::vector <FILE*>::iterator it = tmpfps.begin ();
       it != tmpfps.end (); ++it)
    size_max = std::max (size_max, static_cast <size_t> (std::ftell (*it)));
  char* buf = new char[size_max];
  for (std::vector <FILE*>::iterator it = tmpfps.begin ();
       it != tmpfps.end (); ++it)
    shuffle_lines (*it, &buf[0], static_cast <size_t> (std::ftell (*it)), gen);
  delete [] buf;
  return 0;
}
