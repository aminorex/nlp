// opal -- online perceptron-like algorithm library
//  $Id: opal.cc 1874 2015-01-29 11:47:40Z ynaga $
// Copyright (c) 2009-2015 Naoki Yoshinaga <ynaga@tkl.iis.u-tokyo.ac.jp>
#include <cstring>
#include "pa.h"
#include "timer.h"

int main (int argc, char* argv[]) {

  opal::option opt (argc, argv);
  opal::Model* m = new opal::Model (opt);

#ifdef USE_TIMER
  ny::TimerPool timer_pool;
  ny::Timer* train_t = timer_pool.push ("train");
  ny::Timer* test_t  = timer_pool.push ("test");
#endif
  bool instant = std::strcmp (opt.model, "-") == 0;
  if (opt.mode == opal::option::TRAIN || opt.mode == opal::option::BOTH) {
    TIMER (train_t->startTimer ());
    if (std::strcmp (opt.model0, "-") != 0) m->load (opt.model0);
    m->train_from_file (opt.train, opt.iter, opt.output == 1 ? opt.test : "", instant);
    if (! instant) m->save (opt.model);
    TIMER (train_t->stopTimer ());
  }
  if (opt.mode == opal::option::TEST || opt.mode == opal::option::BOTH) {
    TIMER (test_t->startTimer ());
    if (opt.mode == opal::option::BOTH && ! instant)
      { delete m; m = new opal::Model (opt); }
    if (! instant) m->load (opt.model);
    m->test_on_file (opt.test, opt.output);
    TIMER (test_t->stopTimer ());
  }
#ifdef USE_ARRAY_TRIE
  if (opt.mode == opal::option::DUMP) {
    m->load (opt.model);
    m->dump ();
  }
#endif
  delete m;
  TIMER (timer_pool.print ());
  return 0;
}
