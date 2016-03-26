##########################################################################################
#
# What: Run_me_with_down_sample.py
#
# Pair: Give_me_n_best_periods_Function.py
# 
# Date : Mar 14, 2016
##########################################################################################

'''
Utilises a function to run down sampled light curves and give you 'n' best periods
	
Parameters
----------   
i : <type 'int'>
    The index number of light curve you want to examine
    	
model : <class 'gatspy.periodic.lomb_scargle_multiband.LombScargleMultiband'>
    The Lomb Scargle fit model you want
    	
n : <type 'int'>
    How many best fit periods you want 
    
d_array : <type 'numpy.ndarray'> of <type 'int'>	
    A numpy array of numbers of the powers of base 2...up to and including nobs 

Returns
-------
l_cruves : <type 'list'> containing <type 'tuple'>  
    Each tuple will contain : 
    
returned_list[index][0] : snobs : <type 'int'>
    The Number of Observations/Nights that has been downsampled
    	
returned_list[index][1] : tze_periods : <type 'numpy.ndarray'> of <type 'numpy.float32'>
    A numpy array of the 'n' best periods 
    			
returned_list[index][2] : metadata['P'] : <type 'numpy.float32'>	
    The system's best average period ie Vandplas periods
    	
'''

# Project
import Give_me_n_best_periods_Function as Give_Func
from gatspy import periodic

# This is my fitting parameters :
nterms_base=2
nterms_band=1

# This is your LombScargle code ! Pick one of the 2 below
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
		# The number of observations
		nobs = Give_Func.give_me_nobs(i,model,n)
		
		# The Down sampled array
		d_array = Give_Func.Give_Me_Down_Sample(nobs)
		
		# Returns No. observations, 'n' number of periods, and system's best ave
		l_curves = Give_Func.Give_Me_Light_Curves_Down_Sampled(i,nobs,model,n,d_array)
    	
main()
