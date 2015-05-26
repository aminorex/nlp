/*

EGYPT Toolkit for Statistical Machine Translation
Written by Yaser Al-Onaizan, Jan Curin, Michael Jahr, Kevin Knight, John Lafferty, Dan Melamed, David Purdy, Franz Och, Noah Smith, and David Yarowsky.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, 
USA.
 
*/
#include "TTables.h"
#include "Parameter.h"
#include "projectedGradientDescent.h"

GLOBAL_PARAMETER(float,PROB_CUTOFF,"PROB CUTOFF","Probability cutoff threshold for lexicon probabilities",PARLEV_OPTHEUR,0.0);
GLOBAL_PARAMETER2(float, COUNTINCREASE_CUTOFF,"COUNTINCREASE CUTOFF","countCutoff","Counts increment cutoff threshold",PARLEV_OPTHEUR,1e-6);

#ifdef BINARY_SEARCH_FOR_TTABLE
template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printCountTable(const char *, 
					 const Vector<WordEntry>&, 
					 const Vector<WordEntry>&,
					 const bool) const
{
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printProbTable(const char *filename, 
					 const Vector<WordEntry>& evlist, 
					 const Vector<WordEntry>& fvlist,
					 const bool actual) const
{
  ofstream of(filename);
  /*  for(unsigned int i=0;i<es.size()-1;++i)
    for(unsigned int j=es[i];j<es[i+1];++j)
      {
	const CPPair&x=fs[j].second;
	WordIndex e=i,f=fs[j].first;
	if( actual )
	  of << evlist[e].word << ' ' << fvlist[f].word << ' ' << x.prob << '\n';
	else
	  of << e << ' ' << f << ' ' << x.prob << '\n';
	  }*/
  for(unsigned int i=0;i<lexmat.size();++i)
    {
      if( lexmat[i] )
	for(unsigned int j=0;j<lexmat[i]->size();++j)
	  {
	    const CPPair&x=(*lexmat[i])[j].second;
	    WordIndex e=i,f=(*lexmat[i])[j].first;
	    if( x.prob>PROB_SMOOTH )
	      if( actual )
		of << evlist[e].word << ' ' << fvlist[f].word << ' ' << x.prob << '\n';
	      else
		of << e << ' ' << f << ' ' << x.prob << '\n';
	  }
    }
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printProbTableInverse(const char *, 
				   const Vector<WordEntry>&, 
				   const Vector<WordEntry>&, 
				   const double, 
				   const double, 
				   const bool ) const
{
}
template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::normalizeTable(const vcbList&, const vcbList&, int)
{

	//cout<<"we are in normalize table number 1"<<endl;
  for(unsigned int i=0;i<lexmat.size();++i)
    {
      double c=0.0;
      if( lexmat[i] )
	{
	  unsigned int lSize=lexmat[i]->size();
	  for(unsigned int j=0;j<lSize;++j)
	    c+=(*lexmat[i])[j].second.count;
		//cout<<"the expected count sum was "<<c<<endl;
	  for(unsigned int j=0;j<lSize;++j)
	    {
				//cout<<"the probability of "<<i<<" and "<<j<<" is "<<(*lexmat[i])[j].second.prob<<endl;
				//if (i==2)
				//{
				//cout<<"The expected count of "<<i<<" and "<<" j "<<j<<" before optimizing was "<<(*lexmat[i])[j].second.count<<endl;
				//cout<<"The probability of "<<i<<" and "<<" j "<<j<<" before optimizing was "<<(*lexmat[i])[j].second.prob<<endl;
				//}
	      if( c==0 )
				{
		(*lexmat[i])[j].second.prob=1.0/(lSize);
				}
	      else
			{
		(*lexmat[i])[j].second.prob=(*lexmat[i])[j].second.count/c;
			}
				//if (i==2)
				//{
				//cout<<"The expected count of "<<i<<" and "<<" j "<<j<<" after optimizing was "<<(*lexmat[i])[j].second.count<<endl;
				//cout<<"The probability of "<<i<<" and "<<" j "<<j<<" after optimizing was "<<(*lexmat[i])[j].second.prob<<endl;
				//}
	      (*lexmat[i])[j].second.count=0;
	    }
	}
    }
}

//in the first iteration of model 1 or in the iterations of model 3 and above, its possible that the probability will be 0 and the expected count
//will be greater than 0. in particular in model 3 and able where pegging is done. In that case, we will first normalize and take that as the 
//starting point for projected gradient descent
template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::smoothedL0NormalizeTable(const vcbList&engl, const vcbList&french ,bool getGoodStartingPoint)
  // normalize conditional probability P(fj/ei):
  // i.e. make sure that Sum over all j of P(fj/e) = 1  
  // this method reads the counts portion of the table and normalize into
  // the probability portion. Then the counts are cleared (i.e. zeroed)
  // if the resulting probability of an entry is below a threshold, then 
  // remove it .
{

	//cout<<"we are in smoothed l0"<<endl;	
	//normalizeTable(engl, french, 2);
	//return;
  //typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;

	//vector<vector<double>*> fractional_counts(engl.uniqTokens(),NULL) ;
	//vector<vector<double>*> probabilities(engl.uniqTokens(),NULL);
	//vector<vector<double>*> probabilities_optimized(engl.uniqTokens(),NULL);
	//vector<vector<LpPair<COUNT,PROB> *>*> parameter_addresses(engl.uniqTokens(),NULL); //this will hold the addresses of the parameters
	//vector<vector<WordIndex>*> french_word_indices (engl.uniqTokens(),NULL);
	//first we have to initialize the fractional counts vectors and the probability vectors	
	//cout<<"the number of uniq english tokens is "<<engl.uniqTokens()<<endl;
	//cout<<" are are about to initialize the arrays"<<endl;

	//cout<<"we are in normalize table number 1"<<endl;
  for(unsigned int i=0;i<lexmat.size();++i)
  {
  	  //cout<<"optimizing "<<i<<endl;
      double c=0.0;
  if( lexmat[i] )
	{
//		vector<double> * fractional_counts = new vector<double>;
	//	vector<double> * probabilities = new vector<double>;
		//vector<double> * probabilities_optimized = new vector<double>;

		vector<double>  fractional_counts = vector<double>();
		vector<double>  probabilities = vector<double>();
		vector<double>  probabilities_optimized = vector<double> ();

		//cout<<"the size of fractional_counts is "<<fractional_counts.size()<<endl;
		//cout<<"the size of probabilities_vector is"<<probabilities.size()<<endl;
		//cout<<"the size of probabilities_optimized is "<<probabilities_optimized.size()<<endl;
	  unsigned int lSize=lexmat[i]->size();	
		//cout<<"the size of index "<<i<<" is "<<lSize<<endl;
		//creating the vector that we will need
	  if (getGoodStartingPoint == 1)
	  {
		//first storing the expected counts
		for(unsigned int j=0;j<lSize;++j)
		{
		  fractional_counts.push_back((double) (*lexmat[i])[j].second.count);
		}
		normalizeTable(engl,french);  
		
	  }
	  for(unsigned int j=0;j<lSize;++j)
		{
			if (getGoodStartingPoint == 0 && (((*lexmat[i])[j].second.prob) == 0.0 && ((*lexmat[i])[j].second.count) != 0.0))
			{
				cout<<"the english word index of zero probability was "<<i<<endl;
				cout<<" the french word index of zero probability was "<<j<<endl;
				cout<<"the probability was zero "<<endl;
				cout<<"the fractional count was "<<(*lexmat[i])[j].second.count<<endl;
				exit(1);
			}
			if (getGoodStartingPoint == 0)
			{
			  fractional_counts.push_back((double) (*lexmat[i])[j].second.count);
			}  
			//cout<<"the probability of "<<i<<" and "<<j<<" is "<<(*lexmat[i])[j].second.prob<<endl;
			probabilities.push_back((double)(*lexmat[i])[j].second.prob);
	    c+=(*lexmat[i])[j].second.count;
		
		}
		//cout<<"the expected count sum was "<<c<<endl;
		if (c == 0) //then we smoothe just like in normalize table
		{
			//cout<<"the count c was 0"<<endl;

		  for(unsigned int j=0;j<lSize;++j)
	    {	
				//cout<<" we are smoothing"<<endl;
				(*lexmat[i])[j].second.prob=1.0/(lSize);
			}
			continue;
		}
		//cout<<"we are optimizing the index "<<i<<endl;
		//now sending off to projected gradient descent to optimize
		projectedGradientDescentWithArmijoRule(fractional_counts,probabilities,probabilities_optimized )	;

		//now that we have the probabilities, we need ot replace them back
	  for(unsigned int j=0;j<lSize;++j)
	  {
				
	      //if( c==0 ) //if the sum of the fractional counts was 0. wow. how can that happen ? 
		//(*lexmat[i])[j].second.prob=1.0/(lSize);
	   //   else
			//if (i==2)
				//{
			//cout<<"The expected count of "<<i<<" and "<<" j "<<j<<" before optimizing was "<<(*lexmat[i])[j].second.count<<endl;
			//cout<<"The probability of "<<i<<" and "<<" j "<<j<<" before optimizing was "<<(*lexmat[i])[j].second.prob<<endl;
				//}
			 (*lexmat[i])[j].second.prob=(PROB) probabilities_optimized[j];
	    //			if (i==2)
			//	{
			//cout<<"The expected count of "<<i<<" and "<<" j "<<j<<" after optimizing was "<<(*lexmat[i])[j].second.count<<endl;
			//cout<<"The probability of "<<i<<" and "<<" j "<<j<<" after optimizing was "<<(*lexmat[i])[j].second.prob<<endl;
				//}
			/*
			if ((*lexmat[i])[j].second.prob == 0)
			{
				cout<<"the probability of "<<i<<" and "<<j<<" after smoothed l0 optimization was 0"<<probabilities_optimized[j]<<endl;
			}
			*/
			(*lexmat[i])[j].second.count= 0.0;//(COUNT) probabilities_optimized[j];

	   }
		//deleting the vectors created to aviod memory leaks
		
	}
    }
	
	//now calling normalize table to account for smoothing 
	//cout<<"calling normalized table"<<endl;
	//return normalizeTable(engl, french,2);
	return ;
 	
}


template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::readProbTable(const char *){
}

template class tmodel<COUNT,PROB> ; 

#else

/* ------------------ Method Definiotns for Class tmodel --------------------*/

#
template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printCountTable(const char *filename, 
					 const Vector<WordEntry>& evlist, 
					 const Vector<WordEntry>& fvlist,
					 const bool actual) const
     // this function dumps the t table. Each line is of the following format:
     //
     // c(target_word/source_word) source_word target_word
{
  ofstream of(filename);
  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  for(i = ef.begin(); i != ef.end();++i){
    if ( ((*i).second).count >  COUNTINCREASE_CUTOFF)
      if (actual)
	of <<  ((*i).second).count << ' ' << evlist[ ((*i).first).first ].word << ' ' << fvlist[((*i).first).second].word << ' ' << (*i).second.prob << '\n';
      else 
	of << ((*i).second).count << ' ' <<  ((*i).first).first  << ' ' << ((*i).first).second << ' ' << (*i).second.prob << '\n';
  }
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printProbTable(const char *filename, 
					 const Vector<WordEntry>& evlist, 
					 const Vector<WordEntry>& fvlist,
					 const bool actual) const
     // this function dumps the t table. Each line is of the following format:
     //
     // source_word target_word p(target_word/source_word)
{
	cout<<"we are about to print the prob table"<<endl;
  ofstream of(filename);
  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  for(i = ef.begin(); i != ef.end();++i)
    if( actual )
      of << evlist[((*i).first).first].word << ' ' << 
	fvlist[((*i).first).second].word << ' ' << (*i).second.prob << '\n';
    else
      of << ((*i).first).first << ' ' << ((*i).first).second << ' ' << 
	(*i).second.prob << '\n';
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::printProbTableInverse(const char *filename, 
				   const Vector<WordEntry>& evlist, 
				   const Vector<WordEntry>& fvlist, 
				   const double, 
				   const double, 
				   const bool actual) const
  // this function dumps the inverse t table. Each line is of the format:
  //
  // target_word_id source_word_id p(source_word/target_word)
  //
  // if flag "actual " is true then print actual word entries instead of 
  // token ids
{
  cerr << "Dumping the t table inverse to file: " << filename << '\n';
  ofstream of(filename);
  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  PROB p_inv = 0 ;
  //  static const PROB ratio(double(fTotal)/eTotal);
  WordIndex e, f ;
  int no_errors(0);
  vector<PROB> total(fvlist.size(),PROB(0)) ; // Sum over all e of P(f/e) * p(e) - needed for normalization
 
  for(i = ef.begin(); i != ef.end(); i++){
    e = ((*i).first).first ;
    f = ((*i).first).second ;
    total[f] += (PROB) evlist[e].freq * ((*i).second.prob); //add P(f/ei) * F(ei) 
  }
  
  for(i = ef.begin(); i != ef.end(); i++){
    e = ((*i).first).first ;
    f = ((*i).first).second ;
    p_inv = ((*i).second.prob) * (PROB) evlist[e].freq / total[f] ;
    if (p_inv > 1.0001 || p_inv < 0){
      no_errors++;
      if (no_errors <= 10){
	cerr << "printProbTableInverse(): Error - P("<<evlist[e].word<<"("<<
	  e<<") / "<<fvlist[f].word << "("<<f<<")) = " << p_inv <<'\n';
	cerr << "f(e) = "<<evlist[e].freq << " Sum(p(f/e).f(e)) = " << total[f] <<
	  " P(f/e) = " <<((*i).second.prob)  <<'\n';
	if (no_errors == 10)
	  cerr<<"printProbTableInverse(): Too many P inverse errors ..\n";
      }
    }
    if (actual)
      of << fvlist[f].word << ' ' << evlist[e].word << ' ' << p_inv << '\n';
    else 
      of << f << ' ' << e << ' ' << p_inv <<  '\n';
  }
}
/*



{
  cerr << "Dumping the t table inverse to file: " << filename << '\n';
  ofstream of(filename);
  hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  PROB p_inv = 0 ;
  static const PROB ratio(double(fTotal)/eTotal);
  WordIndex e, f ;
  for(i = ef.begin(); i != ef.end(); i++){
    e = ((*i).first).first ;
    f = ((*i).first).second ;
    p_inv = ((*i).second.prob) * ratio * (PROB) evlist[e].freq / 
      (PROB) fvlist[f].freq ;
    if (actual)
      of << fvlist[f].word << ' ' << evlist[e].word << ' ' << p_inv << '\n';
    else 
      of << f << ' ' << e << ' ' << p_inv <<  '\n';
  }
}
*/
template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::normalizeTable(const vcbList&engl, const vcbList&french, int iter)
  // normalize conditional probability P(fj/ei):
  // i.e. make sure that Sum over all j of P(fj/e) = 1  
  // this method reads the counts portion of the table and normalize into
  // the probability portion. Then the counts are cleared (i.e. zeroed)
  // if the resulting probability of an entry is below a threshold, then 
  // remove it .
{
	//cout<<"we are in normalize table number 2"<<" and the iteration number is "<<iter<<endl;
  if( iter==2 )
    {
      total2.resize(engl.uniqTokens());for(unsigned int i=0;i<total2.size();i++)total2[i]=0.0;
    }
  nFrench.resize(engl.uniqTokens());for(unsigned int i=0;i<nFrench.size();i++)nFrench[i]=0;
  nEng.resize(french.uniqTokens());for(unsigned int i=0;i<nEng.size();i++)nEng[i]=0;
  Vector<double> total(engl.uniqTokens(),0.0);
  //Vector<int> nFrench(engl.uniqTokens(), 0);
  //Vector<int> nEng(french.uniqTokens(), 0);

  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;
  for(i = ef.begin(); i != ef.end(); i++){ // for all possible source words e
    if( iter==2 ) 
		{
      total2[((*i).first).first] += (*i).second.count; //if this is the second iteration, only the second total is updated
		}
    total[((*i).first).first] += (*i).second.count; //"(*i).first" returns the english_id, french_id word pair and  "((*i).first).first" returns the english id and 
						    // (*i).second returns the structure that contains the count and the log prob. from there, we get the count	
    nFrench[((*i).first).first]++; //this probably stores the number of french words for the english word given by the id (*i).first
    nEng[((*i).first).second]++;  //this probably stores the number of english words for the french word given by the id (*i).second
  }
  for(unsigned int k=0;k<engl.uniqTokens();++k)
	{
    if( nFrench[k] ) // if the number of french words seen with this english word is not zero. I wonder if this will ever be not satisfied
      {
				//cout <<"the total number of french words for "<<k<<" is "<<nFrench[k]<<endl;
				//cout<<"the number of uniq french tokens in the copur is "<<french.uniqTokensInCorpus()<<endl;
				double probMass=(french.uniqTokensInCorpus()-nFrench[k])*PROB_SMOOTH; //this is how much smoothign probability mass you will assign to the french words not seen with  this word
				if( probMass<0.0 )
				{
				  cout << k << " french.uniqTokensInCorpus(): " << french.uniqTokensInCorpus() << "  nFrench[k]:"<< nFrench[k] << '\n';
				}
				//cout <<" the value of total for "<<k<<" before adding the probability mass for unseen words in iteration "<<iter<<" is "<<total[k]<<endl;
				total[k]+= total[k]*probMass/(1-probMass);	
				//cout <<" the value of total for "<<k<<" after adding the probability mass for unseen words is in iteration "<<iter<<" is "<<total[k]<<endl;
      }
	}
  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::iterator j, k;
  PROB p ;
  int nParams=0;
  for(j = ef.begin(); j != ef.end(); ){
    k = j;
    k++ ;
		//cout<<"The total fractional count for english word "<< ((*j).first).first<< " is "<<total[((*j).first).first]<<" and the iteration number is "<<iter<<endl;
		//cout<<"The count of the french word "<<((*j).first).second<<" with the english word "<<((*j).first).first<<" is "<<((*j).second).count<<endl;
    if( (total[((*j).first).first])>0.0 )
      p = ((((*j).second).count) /(total[((*j).first).first])) ;
    else
      p= 0.0;
    if (p > PROB_CUTOFF)
			//if (1)
      {
	if( iter>0 ) //#in iter = 2 , some of the e,f pairs might get erased,so, we have to go through normalizeTable again to recollect the counts as the number of ef pairs have reduced. When iter = 0, we do the final normalization step . That is why, here, the probabilities are still 0 while the count is updated to the newly calculated probability
	  {
	    ((*j).second).prob = 0 ;
	    ((*j).second).count = p ;
	  }
	else //when iter = 0, we are ready to assign probabilities
	  {
			if ((*j).first.first == 0 && (*j).first.second == 14 )
			{
				cout<<" the probability of 0 and 14 is "<<((*j).second).prob<<endl;
			}
	    ((*j).second).prob = p ;
	    ((*j).second).count = 0 ;
	  }
	nParams++;
      }
    else {
			cout<<"we are erasing english"<<(*j).first.first<<"and french word"<<(*j).first.second<<endl;
      erase(((*j).first).first, ((*j).first).second);
			cout<<"the probability is "<<(*j).second.prob<<" and the fractional count is "<<(*j).second.count<<endl;
    }
    j = k ;
  }
  if( iter>0 )
    return normalizeTable(engl, french, iter-1);
  else
    {
    }
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::smoothedL0NormalizeTable(const vcbList&engl, const vcbList&french )
  // normalize conditional probability P(fj/ei):
  // i.e. make sure that Sum over all j of P(fj/e) = 1  
  // this method reads the counts portion of the table and normalize into
  // the probability portion. Then the counts are cleared (i.e. zeroed)
  // if the resulting probability of an entry is below a threshold, then 
  // remove it .
{
	//cout<<"we are in smoothed l0"<<endl;	
  typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::const_iterator i;

	vector<vector<double>*> fractional_counts(engl.uniqTokens(),NULL) ;
	vector<vector<double>*> probabilities(engl.uniqTokens(),NULL);
	vector<vector<double>*> probabilities_optimized(engl.uniqTokens(),NULL);
	//vector<vector<LpPair<COUNT,PROB> *>*> parameter_addresses(engl.uniqTokens(),NULL); //this will hold the addresses of the parameters
	vector<vector<WordIndex>*> french_word_indices (engl.uniqTokens(),NULL);
	//first we have to initialize the fractional counts vectors and the probability vectors	
	//cout<<"the number of uniq english tokens is "<<engl.uniqTokens()<<endl;
	//cout<<" are are about to initialize the arrays"<<endl;
	
  for(i = ef.begin(); i != ef.end(); i++)
	{ // for all possible source words e
		//cout<<"in the loop"<<endl;
		//cout<<"the index is "<<(*i).first.first<<endl;
		if (fractional_counts[(int) (*i).first.first] == NULL)	//this vector of fractional counts is empty
		{
			//cout<<"it was null"<<endl;
			fractional_counts[(*i).first.first] = new vector<double> ;	
			probabilities[(*i).first.first] = new vector<double> ;
			probabilities_optimized[(*i).first.first] = new vector<double> ;
			//parameter_addresses.push_back(new vector<LpPair<COUNT,PROB> *> );
			french_word_indices[(*i).first.first]=  new vector<WordIndex>;
			//cout<<"finished creating"<<endl;
		}
			//cout<<" we are outside "<<endl;
			//filling in the values
			//cout<<(*i).second.count<<endl;
			//cout<<(*i).second.prob<<endl;
			//cout<<"about to populate probabilities"<<endl;
			//cout<<"the size of the vector in fractional counts is "<<fractional_counts[(*i).first.first]->size()<<endl;
			fractional_counts[(*i).first.first]->push_back((double)(*i).second.count);
			probabilities[(*i).first.first]->push_back((double)(*i).second.prob);
			if (((*i).second.prob) == 0 && ((*i).second.count) != 0)
			{
				cout<<"the english word index of zero probability was "<<(*i).first.first<<endl;
				cout<<" the french word index of zero probability was "<<(*i).first.second<<endl;
				cout<<"the probability was zero "<<endl;
				cout<<"the fractional count was "<<(*i).second.count<<endl;
				exit(1);
			}
			//probabilities_optimized[(*i).first.first]
			//parameter_addresses[(*i).first.first]->push_back( &((*i).second));
			//cout<<"we are here 1"<<endl;
			french_word_indices[(*i).first.first]->push_back((*i).first.second);

  }
	//cout<<" are are done initializing the arrays"<<endl;
	
	//now, I need to go over all the parameters and optimize them with projected gradient descent

	//int num_english_words = engl.uniqTokens();
	for (unsigned int counter = 0;counter < engl.uniqTokens();counter++)
	{
		if (fractional_counts[counter] == NULL) //if the english word has at least some non zero french words that it was seen in expectation with
		{
			continue;
		}
		else
		{
			//cout <<"we are now optimizing for tag "<<counter<<endl;
			projectedGradientDescentWithArmijoRule(*fractional_counts[counter],*probabilities[counter],*probabilities_optimized[counter] )	;
		}

	}
	//we're doine optimizing so we need to add the add the probabilities back into the hash_map

	for (unsigned int counter = 0;counter < engl.uniqTokens();counter++)
	{
		if (fractional_counts[counter] == NULL) //if the english word has at least some non zero french words that it was seen in expectation with
		{
			continue;
		}
		else
		{
			if (fractional_counts[counter]->size() == probabilities_optimized[counter]->size())
			{
				//cout<<"after optimization, the number of expected counts in "<<counter<<" did not match the number of optimized probabilities"<<endl;
				for (unsigned int j = 0 ;j< fractional_counts[counter]->size();j++)
				{
					//(*((*parameter_addresses[counter])[j])).prob = (PROB) (*probabilities_optimized[counter])[j];
					//(*(*parameter_addresses[counter])[j]).count = (COUNT) (*probabilities_optimized[counter])[j];			
					//first find the index where it lies
					//LpPair<COUNT,PROB> * pairPtr = tTable.getPtr((WordIndex)counter, (*french_word_indices[counter])[j]);
      		typename hash_map<wordPairIds, CPPair, hashpair, equal_to<wordPairIds> >::iterator i = ef.find(wordPairIds((WordIndex)counter,(*french_word_indices[counter])[j] )); 
      		if(i == ef.end())  // if it exists, return a pointer to it.
					{
						cout<<"the word should have been found in the hash map"<<endl;
						exit(1);
						//return(&((*i).second));

					}
					else
					{
						if ((*i).first.first == 0 && (*i).first.second == 14)
						{		
							cout<<"the probability after optimizing of 0,14 is "<<(*probabilities_optimized[counter])[j]<<endl;
						}	
						if ((*probabilities_optimized[counter])[j] == 0)
						{	
							cout<<"the probability of "<<(*i).first.first<<", "<<(*i).first.first<<"after optimizing is 0"<<endl;
						}
						//cout<<"probabilities optimized is "<<(*probabilities_optimized[counter])[j]<<endl;
						(*i).second.prob = (PROB) (*probabilities_optimized[counter])[j];
						(*i).second.count = (COUNT) (*probabilities_optimized[counter])[j];
					}
					//(*pairPtr).prob = (PROB) (*probabilities_optimized[counter])[j];
					//(*pairPtr).prob = (COUNT) (*probabilities_optimized[counter])[j];
	
				}
			}
			else
			{
				//cout<<"the size of fractional counts is not equal to the size of optimized probabilities"<<endl;
				cout<<"after optimization, the number of expected counts in "<<counter<<" did not match the number of optimized probabilities"<<endl;
				exit(1);
			}
		}

	}
	//now calling normalize table to account for smoothing 
	//return normalizeTable(engl, french,2);

	return;
 
}

template <class COUNT, class PROB>
void tmodel<COUNT, PROB>::readProbTable(const char *filename){
  /* This function reads the t table from a file.
     Each line is of the format:  source_word_id target_word_id p(target_word|source_word)
     This is the inverse operation of the printTable function.
     NAS, 7/11/99
  */
  ifstream inf(filename);
  cerr << "Reading t prob. table from " << filename << "\n";
  if(!inf){
    cerr << "\nERROR: Cannot open " << filename << "\n";
    return;
  }
  WordIndex src_id, trg_id;
  PROB prob;
  int nEntry=0;
  while(    inf >> src_id  >> trg_id  >> prob){
    insert(src_id, trg_id, 0.0, prob);
    nEntry++;
  }
  cerr << "Read " << nEntry << " entries in prob. table.\n";
}

template class tmodel<COUNT,PROB> ; 

/* ---------------- End of Method Definitions of class tmodel ---------------*/


#endif
