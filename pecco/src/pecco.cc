// pecco -- please enjoy classification with conjunctive features
//  $Id: pecco.cc 1852 2014-06-20 15:02:49Z ynaga $
// Copyright (c) 2008-2014 Naoki Yoshinaga <ynaga@tkl.iis.u-tokyo.ac.jp>
#include "pecco.h"

int main (int argc, char * argv[]) {

  pecco::option opt (argc, argv);
  pecco::pecco * pecco = 0;
  switch (opt.type) {
#ifdef USE_KERNEL
    case pecco::KERNEL:
      pecco = new pecco::pecco (static_cast <pecco::kernel_model *> (0), opt);
      break;
#endif
#ifdef USE_LINEAR
    case pecco::LINEAR:
      pecco = new pecco::pecco (static_cast <pecco::linear_model *> (0), opt);
      break;
#endif
  }
  pecco->load (opt.model);
  pecco->batch ();
  delete pecco;
  return 0;
}
