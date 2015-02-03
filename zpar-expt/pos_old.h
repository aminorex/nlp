

#ifndef _ENGLISH_PENN_POS_H
#define _ENGLISH_PENN_POS_H 1

namespace english {



// the penn tag set
// Modify the following three constants together, keeping consistency!
const std::string PENN_TAG_STRINGS[] = {};

enum PENN_TAG_CONSTANTS {};

const bool PENN_TAG_CLOSED[] = {};

const int PENN_TAG_FIRST = 3;
const int PENN_TAG_COUNT_BITS = 6;

/*
const unsigned long long PENN_TAG_MUST_SEE = (static_cast<unsigned long long>(1)<<PENN_TAG_SYM) | \
                                        (static_cast<unsigned long long>(1)<<PENN_TAG_FW) | \
                                        (static_cast<unsigned long long>(1)<<PENN_TAG_CD) | \
                                        (static_cast<unsigned long long>(1)<<PENN_TAG_LS) | \
                                        (static_cast<unsigned long long>(1)<<PENN_TAG_NOUN_PROPER) | \
                                        (static_cast<unsigned long long>(1)<<PENN_TAG_NOUN_PROPER_PLURAL) ;
*/
//===============================================================

class CTag {
public:
   enum {SENTENCE_BEGIN = PENN_TAG_BEGIN};
   enum {SENTENCE_END = PENN_TAG_END};
   enum {COUNT = PENN_TAG_COUNT};
   enum {MAX_COUNT = PENN_TAG_COUNT};
   enum {NONE = PENN_TAG_NONE};
   enum {SIZE = PENN_TAG_COUNT_BITS};
   enum {FIRST = PENN_TAG_FIRST};
   enum {LAST = PENN_TAG_COUNT-1};

protected:
   unsigned long m_code;

public:
   CTag() : m_code(NONE) {}
   CTag(PENN_TAG_CONSTANTS t) : m_code(t) { }
   CTag(int t) : m_code(t) { }
   CTag(const std::string &s) { load(s); }
   virtual ~CTag() {}

public:
   unsigned long code() const { return m_code; }
   unsigned long hash() const { return m_code; }
   void copy(const CTag &t) { m_code = t.m_code; }
   std::string str() const { assert(m_code<PENN_TAG_COUNT) ; return PENN_TAG_STRINGS[m_code]; }
   void load(const std::string &s) {
      m_code = PENN_TAG_NONE ;
      for (int i=1; i<PENN_TAG_COUNT; ++i)
         if (PENN_TAG_STRINGS[i] == s)
            m_code = i;
   }
   void load(const unsigned &i) {
      m_code = i;
   }
//   bool closed() const { return PENN_TAG_CLOSED[m_code]; }
   bool closed() const { return false; }

public:
   bool operator == (const CTag &t1) const { return m_code == t1.m_code; }
   bool operator != (const CTag &t1) const { return m_code != t1.m_code; }
   bool operator < (const CTag &t1) const { return m_code < t1.m_code; }
   bool operator > (const CTag &t1) const { return m_code > t1.m_code; }
   bool operator <= (const CTag &t1) const { return m_code <= t1.m_code; }
   bool operator >= (const CTag &t1) const { return m_code >= t1.m_code; }
};

//===============================================================
/*
inline unsigned matchPunctuation(const CTag &tag) {
   if (tag==PENN_TAG_L_QUOTE) return 1;
   else if (tag == PENN_TAG_L_BRACKET) return 2;
   else if (tag==PENN_TAG_R_BRACKET) return 4;
   else if (tag == PENN_TAG_COMMA) return 8;
   else if (tag == PENN_TAG_PERIOD) return 16;
   else if (tag == PENN_TAG_COLUM) return 32;
   else if (tag == PENN_TAG_R_QUOTE) return 64;
   else return 0;
}
*/
}; // namespace english

#endif

