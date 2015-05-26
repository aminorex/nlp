#!/usr/bin/python
"""minimalign.py: minimal version of anymalign.py

Adrien Lardilleux <Adrien.Lardilleux@limsi.fr>
http://users.info.unicaen.fr/~alardill/anymalign/
"""

import sys
import random

NB_SAMPLES = 10 # The larger, the more alignments

# Read input file and load bicorpus into memory, as a list of pairs of
# sentences (1 sentence = 1 list of words)
sourceFile = open(sys.argv[1], 'r')
targetFile = open(sys.argv[2], 'r')
corpus = zip((line.split() for line in sourceFile),
             (line.split() for line in targetFile))
sourceFile.close()
targetFile.close()

allAlignments = {} # Simple counter {alignmentString: integerCount, ...}

# Main loop
for i in xrange(NB_SAMPLES):
    # Select a random subcorpus
    subcorpusSize = random.randrange(0, len(corpus))
    selection = random.sample(xrange(len(corpus)), subcorpusSize)

    # Assign to each word of the subcorpus the line ids it appears on
    sourceWord_vec = {} # {string: [lineNo, ...], ...}
    targetWord_vec = {}
    for lineId in selection:
        sourceSentence, targetSentence = corpus[lineId]
        for word in sourceSentence:
            if word not in sourceWord_vec:
                sourceWord_vec[word] = []
            sourceWord_vec[word].append(lineId)
        for word in targetSentence:
            if word not in targetWord_vec:
                targetWord_vec[word] = []
            targetWord_vec[word].append(lineId)

    # Group words according to the lines they appear on
    vec_words = {} # {tupleOfLineNos: ([srcWord, ...], [tgtWord, ...]), ...}
    for word in sourceWord_vec:
        vec = tuple(sourceWord_vec[word])
        if vec not in vec_words:
            vec_words[vec] = ([], [])
        vec_words[vec][0].append(word)
    for word in targetWord_vec:
        vec = tuple(targetWord_vec[word])
        if vec in vec_words:
            vec_words[vec][1].append(word)
        # else: there will not be any alignment since the source part is empty

    # For each group of words, make a new pass on the subcorpus to extract
    # alignments and their contexts
    for vec in vec_words:
        sourceWords, targetWords = vec_words[vec]
        if not targetWords: # target part is empty -> no alignment
            continue

        sourceSet = set(sourceWords) # Speed up searches
        targetSet = set(targetWords)

        for lineId in vec:
            sourceSentence, targetSentence = corpus[lineId]
            sourceAl = [] # Same words as in <sourceSet>, but ordered
            targetAl = []
            sourceCont = [] # Complementary of <sourceAl> on the line
            targetCont = []
            for word in sourceSentence:
                if word in sourceSet:
                    sourceAl.append(word)
                else:
                    sourceCont.append(word)
            for word in targetSentence:
                if word in targetSet:
                    targetAl.append(word)
                else:
                    targetCont.append(word)

            # We get alignments only if both the source and the target parts
            # actually contain words. If so, increase alignment's count.
            if sourceAl and targetAl:
                alignment = "%s\t%s" % (" ".join(sourceAl), " ".join(targetAl))
                if alignment not in allAlignments:
                    allAlignments[alignment] = 0
                allAlignments[alignment] += 1
            if sourceCont and targetCont:
                alignment = "%s\t%s" % (" ".join(sourceCont),
                                        " ".join(targetCont))
                if alignment not in allAlignments:
                    allAlignments[alignment] = 0
                allAlignments[alignment] += 1
# End of main loop

# Sort all alignments according to their count and output everything
allAlignments = allAlignments.items()
allAlignments.sort(key=lambda x:x[1], reverse=True)
for alignment, count in allAlignments:
    print "%s\t%i" % (alignment, count)
