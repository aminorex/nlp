HOW:
   ./projectivize.py CONLL_INPUT_FILE > PROJECTIVE_FILE

WHAT:
   projectivization of non-projective dependency trees.

WHY:
   Useful for training a projective parser on non-projective data.

   NOTE that this is lossy conversion. 
   If you actually care about the non-projective relations, 
   you should use a non-projective parser.  
   
   This will just help you maximize the accuracy of the projective links
   of you projective parser.

HOW2:
   the algorithm uses Eisner's projective decoder, where links in the
   original tree are assigned a score of 1, and all other links a score
   of 0.  the decoder then finds the projective structure that has the
   maximum number of links from the original non-projective parse.

