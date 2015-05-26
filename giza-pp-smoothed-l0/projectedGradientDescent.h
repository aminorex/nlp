#include <algorithm>
#include <vector>
#include <iostream>
#include "defs.h"

//declaring the global parameters for em with smoothed l0
/*
GLOBAL_PARAMETER(double, ARMIJO_BETA,"armijo_beta","pgd optimization parameter beta used in armijo line search",PARAM_SMOOTHED_LO,0.1);
GLOBAL_PARAMETER(double, ARMIJO_SIGMA,"armijo_sigma","pgd optimization parameter sigma used in armijo line search",PARAM_SMOOTHED_LO,0.0001);
GLOBAL_PARAMETER(double, L0_BETA,"smoothed_l0_beta","optimiztion parameter beta that controls the sharpness of the smoothed l0 prior",PARAM_SMOOTHED_LO,0.5);
GLOBAL_PARAMETER(double, L0_ALPHA,"smoothed_l0_alpha","optimization parameter beta that controls the sharpness of the smoothed l0 prior",PARAM_SMOOTHED_LO,0.0);
*/


using namespace std;


//template <class PROB>
bool descending (double i,double j) { return (i>j); }

//typedef double PROB ;
//typedef double COUNT ;

void projectOntoSimplex(vector<double> &v,vector<double> &projection)
{
	vector<double> mu_vector (v.begin(),v.end());
	sort(mu_vector.begin(),mu_vector.end(),descending);
	//vector<double>  projection_step;		
	vector<double> sum_vector (mu_vector.size(),0.0);
	double sum = 0;
	//double max = -99999999;
	vector<double>::iterator it;
	int counter = 1;
	int max_index  = -1;
	double max_index_sum = -99999999;
	for (it = mu_vector.begin() ;it != mu_vector.end(); it++)
	{
		sum += *it;
		double temp_rho = *it - (1/(double)counter)*(sum-1);
		if (temp_rho > 0)
		{
			max_index = counter;
			max_index_sum = sum;
		}
		counter++;
	}
	
	double theta = 1/(double) max_index *(max_index_sum -1);
	//vector <double> projection ;
	
	for (it = v.begin() ;it != v.end(); it++)
	{
		double value = max((*it)-theta,(double)0.0);
		projection.push_back(value);
//		cout<<value<<endl;
	}
	//cout<<"the size of final ector is "<<projection.size()<<endl;
	return;
}



//evaluates the value of the function and returns the function value
inline double evalFunction(vector<double> & expected_counts ,vector<double> & current_point)
{
 	int num_elements = expected_counts.size();
	double func_value = 0.0;
	for (int i =0 ;i<num_elements;i++)
	{
		if (current_point[i] == 0.0 && expected_counts[i] != 0.0)
		{
			cout<<"the probability in position "<<i<<" was 0"<<" and the fractional count was not 0"<<endl;
			exit(0);
		}
		if (current_point[i] != 0.0)
		{
			func_value += expected_counts[i] * log(current_point[i]) + L0_ALPHA * exp(-current_point[i]/L0_BETA);
		}
		else
		{
			func_value += L0_ALPHA * exp(-current_point[i]/L0_BETA);
		}
	}
	
	return(-func_value);
}

//template <class COUNT,class PROB>
void inline evalGradient(vector<double> & expected_counts, vector<double> & current_point, vector<double> & gradient)
{
	int num_elements = expected_counts.size();
	for (int i =0 ;i<num_elements;i++)
	{
		if (current_point[i] == 0 && expected_counts[i] != 0.0 )
		{
			cout<<"the probability in position "<<i<<" was 0"<<" and the fractional count was not 0"<<endl;
			exit(0);
		}
		if (current_point[i] != 0.0)
		{
			gradient[i] = -1 *(expected_counts[i] / current_point[i] - L0_ALPHA * exp(-current_point[i]/L0_BETA)/L0_BETA	);
		}
		else
		{
			gradient[i] = -1 *(- L0_ALPHA * exp(-current_point[i]/L0_BETA)/L0_BETA	);
		}
		//printf ("the gradient is %.16f\n",gradient[i]);
	}
}


//template <class COUNT,class double>
void projectedGradientDescentWithArmijoRule(vector<double> & expected_counts ,vector<double> & current_prob, vector<double> & new_prob)
{
	//cout<<" we are in projected grad"<<endl;
	int num_elements = expected_counts.size();
	//cout<<"projected gradient descent here"<<endl;
	vector<double> current_point(current_prob);
	//cout <<"the number of PGD iterations is "<<NUM_PGD_ITERATIONS<<endl;
	for (int time = 1; time <= NUM_PGD_ITERATIONS; time++)
	{
		//cout<<"time is"<<time<<endl;
		double current_function_value = evalFunction(expected_counts,current_point);
		vector<double> gradient (num_elements,(double) 0.0);
		evalGradient(expected_counts,current_point,gradient);
		//getchar();
		vector<double> new_point (num_elements,(double) 0.0);
		//moving in the opposite direction of the gradient
		for (int i =0 ;i<num_elements;i++)
		{
			new_point[i] = current_point[i] - ETA * gradient[i];	
		}
		vector<double> new_feasible_point ;//(num_elements,(double) 0.0);
		// now projecting on the simplex
		projectOntoSimplex(new_point,new_feasible_point);
		//cout<<"armijo beta is "<<ARMIJO_BETA<<endl;
		//cout<<"armijo sigma is "<<ARMIJO_SIGMA<<endl;
		double armijo_bound = 0.0;
		for (int i =0 ;i<num_elements;i++)
		{
			double bound_term = ARMIJO_SIGMA * ARMIJO_BETA * gradient[i] * (new_feasible_point[i] - current_point[i]); 	
			//cout<<"the grad is "<<gradient[i]<<" the new feasible point is "<<new_feasible_point[i]<<" current point is "<<current_point[i]<<endl;
			//cout<<"the bound term is "<<bound_term<<endl;
			armijo_bound -= bound_term;
			//cout<<"temp armijo bound "<<armijo_bound<<endl;
		}
		
		//getchar();
		bool terminate_line_srch = 0;
		int num_steps = 1;
		double current_alpha = ARMIJO_BETA ;
		double final_alpha = 0.0 ; //if the function value does not improve at all, then the armijo beta should be 1
		double current_armijo_bound = armijo_bound;
		double best_func_value = current_function_value;
		bool no_update = 1;
		//cout<<"current function value is "<<current_function_value<<endl;
		//printf ("current function value is %.15f\n",current_function_value);
		while(terminate_line_srch != 1 && num_steps <= 20)
		{	
			//cout<<"current armijo bound is "<<current_armijo_bound<<endl;
			//cout<<"we are in teh while loop"<<endl;
			//cout<<"num steps is "<<num_steps<<endl;
		//	current_beta = 
			vector<double> temp_point (num_elements,(double) 0.0);
			for (int i =0 ;i<num_elements;i++)		
			{
				temp_point[i] = (1.0 - current_alpha) * current_point[i] + current_alpha * new_feasible_point[i];
			}
			double func_value_at_temp_point = evalFunction(expected_counts,temp_point);
			//cout<<"function value at temp point is "<<func_value_at_temp_point<<endl;
			//printf ("function value at temp point is %.15f and the iteration number is %d \n",func_value_at_temp_point,num_steps);
			//printf ("current alpha is %.15f\n",current_alpha);
			//getchar();
			if (func_value_at_temp_point < best_func_value)
			{
				best_func_value = func_value_at_temp_point;
				final_alpha = current_alpha;
				no_update = 0;
				//cout<<"we arrived at a better function value"<<endl;
				//getchar();
			}
			
			if (current_function_value - func_value_at_temp_point >= current_armijo_bound)
			{
				//cout<<"the terminate line src condition was met "<<endl;
				terminate_line_srch = 1;
			}
			current_alpha *= ARMIJO_BETA;
			current_armijo_bound *= ARMIJO_BETA;
			num_steps += 1;
			//getchar();
		}
		//printf ("final alpha was %f\n",final_alpha);
		//cout<<"the value of not update was "<<no_update<<endl;
		//getchar();
	
		//vector<double> next_point ;
		if (no_update == 0)
		{
			//next_point.resize(num_elements);
			for (int i =0 ;i<num_elements;i++)
			{
				double coordinate_point = (1.0 - final_alpha)*current_point[i] + final_alpha * new_feasible_point[i];
				//next_point.push_back(coordinate_point);
				current_point[i] = coordinate_point;
			}
			//current_point = next_point;
		}
		else
		{
			//cout<<" not update was true"<<endl;
			break;
		}

	}		
	new_prob = current_point;
}

void inline printVector(vector<double> & v)
{
	for (int i = 0; i< v.size();i++)
	{
		cout<<v[i]<<" ";
	}
	cout<<endl;
}
