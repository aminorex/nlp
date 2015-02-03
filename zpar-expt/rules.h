// Copyright (C) University of Oxford 2010
/****************************************************************
 *                                                              *
 * penn.h - the penn treebank style dependency labels           *
 *                                                              *
 * Author: Yue Zhang                                            *
 *                                                              *
 * Computing Laboratory, Oxford. 2008.07                        *
 *                                                              *
 ****************************************************************/

#ifndef _DEPENDENCY_RUL_PENN
#define _DEPENDENCY_RUL_PENN

#include "tags.h"
#include "dependency/label/penn.h"

namespace english {

/*==============================================================
 *
 * dependency constraints
 *
 *==============================================================*/

#ifdef LABELED
inline bool canAssignLabel(const std::vector< CTaggedWord<CTag,TAG_SEPARATOR> > &sent, const int &head, const int &dep, const CDependencyLabel&lab) {
     return true;
}
#endif

inline bool hasLeftHead(const unsigned &tag) {
     return true;
}

inline bool hasRightHead(const unsigned &tag) {
     return true;
}

inline bool canBeRoot(const unsigned &tag) {
     return true;
}

};

#endif
