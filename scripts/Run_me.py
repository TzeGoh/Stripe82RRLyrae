##########################################################################################
#
# What: Run_me.py
#
# Pair: Give_me_n_best_periods_Function.py
# 
# Date : Mar 14, 2016
##########################################################################################

'''
Utilises a function to generate light curves and give you 'n' best periods.
This file will NOT down-sample for you


Parameters
----------
    
i : <type 'int'>
    The index number of light curve you want to examine
    	
model : <class 'gatspy.periodic.lomb_scargle_multiband.LombScargleMultiband'>
    The Lomb Scargle fit model you want
    	
n : <type 'int'>
    How many best fit periods you want 
    
Returns
-------
returned_list : <type 'list'> 
    This list will contains the following items: 
    
returned_list[0] : nobs : <type 'int'>
    The Number of Observations/Nights
    	
returned_list[1] : tze_periods : <type 'numpy.ndarray'> of <type 'numpy.float32'>
    	A numpy array of the 'n' best periods 
    			
returned_list[2] : metadata['P'] : <type 'numpy.float32'>	
    The system's best average period ie Vandplas periods

'''

# Project
import Give_me_n_best_periods_Function as Give_Func
from gatspy import periodic

# This is my fitting parameters :
nterms_base=2
nterms_band=1

# This is it, this is your LombScargle code ! Pick one of the 2 below
model = periodic.LombScargleMultiband(Nterms_base=nterms_base, Nterms_band=nterms_band)
##model = periodic.SuperSmoother(fit_period=True)

# The list of light curves 
list_of_index = [82,173]
##list_of_index = [101,26,11,334,33,289,14,59,82,173]

# How many n best periods do you want from the fit?
n = 6

# Let's run it !
def main():
	for i in list_of_index:
	# Returns No. of observations, 'n' number of periods, and the system's best ave
		l_curves = Give_Func.give_me_n_best_periods(i,model,n)
		
main()
