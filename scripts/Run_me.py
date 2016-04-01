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
	There are 2 main functions:
		main_no 	===> gives you light curves with no down-sampling
		main_yes 	===> gives you light curves with down-sampling

------------------------------------------------------------------------------------------

Function
--------
main_no :  <type 'function'>
	The main function will take the following parameters and give the following returns :

Parameters
----------
  
i : <type 'int'>
    The index number of light curve you want to examine
    	
model : <class 'gatspy.periodic.lomb_scargle_multiband.LombScargleMultiband'>
    The Lomb Scargle fit model you want
    	
n : <type 'int'>
    How many best fit periods you want 

t: <type 'numpy.ndarray'>
	The time/period of each of the light curve of each RR_Lyrae

mag: <type 'numpy.ndarray'>
	The magnitude of each of the light curve of each RR_Lyrae

dmag: <type 'numpy.ndarray'>
	The error in magnitude of each of the light curve of each RR_Lyrae

nobs: <type 'int'>
	The number of observations

metadata: <type 'numpy.void'>
	All the information of each RR_Lyrae. Most important is metadata['P'] = Period
	
threshold: <type 'int'>
	A minimum threshold so that the periods we pick are not too close 
    
Returns
-------  
nobs : <type 'int'>
    The Number of Observations/Nights
    	
period_n : <type 'numpy.ndarray'> of <type 'numpy.float32'>
    A numpy array of the 'n' best periods 
    			
period_true : metadata['P'] : <type 'numpy.float32'>	
    The system's best average period ie Vandplas periods

------------------------------------------------------------------------------------------

Function
--------
main_yes :  <type 'function'>
	The main function will take the following parameters and give the following returns :

Parameters
----------
i : <type 'int'>
	The index number of light curve you want to examine
	
model : <class 'gatspy.periodic.lomb_scargle_multiband.LombScargleMultiband'>
	The Lomb Scargle fit model you want
	
n : <type 'int'>
	How many best fit periods you want 

t: <type 'numpy.ndarray'>
	The time/period of each of the light curve of each RR_Lyrae

mag: <type 'numpy.ndarray'>
	The magnitude of each of the light curve of each RR_Lyrae

dmag: <type 'numpy.ndarray'>
	The error in magnitude of each of the light curve of each RR_Lyrae

metadata: <type 'numpy.void'>
	All the information of each RR_Lyrae. Most important is metadata['P'] = Period

d_array : <type 'numpy.ndarray'> of <type 'int'>	
	A numpy array of numbers of the powers of base 2...up to and including nobs 
		
threshold: <type 'int'>
	A minimum threshold so that the periods we pick are not too close 

Returns
-------
l_curves : <type 'list'> containing many <type 'tuple'>  
	A list of sequentially down-sampled info of each each star.	
	Each tuple will contain :
    
		snobs : <type 'int'>
    		The Number of Observations/Nights that's been down-sampled, in a number of the 
    			power of base 2...up to and including nobs
    	
		period_n : <type 'numpy.ndarray'> of <type 'numpy.float32'>
   		 	A numpy array of the 'n' best periods 
    			
		period_true : metadata['P'] : <type 'numpy.float32'>	
   		 	The system's best average period ie Vandplas periods
    
'''

# Project
import Give_me_n_best_periods_Function as Give_Func
from gatspy import periodic
from gatspy.datasets import fetch_rrlyrae
import numpy as np

# The specific RR Lyrae package you want to get information from
def rr_info(i):
	'''
	This function takes all the rr_lyrae info in one convenient package

	Parameters
	----------  
	i : <type 'int'>
		The index number of light curve you want to examine
	
	Returns
	-------
	t: <type 'numpy.ndarray'>
		The time/period of each of the light curve of each RR_Lyrae

	mag: <type 'numpy.ndarray'>
		The magnitude of each of the light curve of each RR_Lyrae

	dmag: <type 'numpy.ndarray'>
		The error in magnitude of each of the light curve of each RR_Lyrae

	nobs: <type 'int'>
		The number of observations

	metadata: <type 'numpy.void'>
		All the information of each RR_Lyrae. Most important is metadata['P'] = Period

	'''
	# It's finding the rr_lyraes by index + fit that you specify
	rrlyrae = fetch_rrlyrae()
	lcid = rrlyrae.ids[i]
	t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)

	# Number of observations - original size
	nobs = t.size
	
	# The data with all the magnitude in different filter bands + Period
	metadata = rrlyrae.get_metadata(lcid)
		
	
	return t,mag,dmag,metadata,nobs

# This is my fitting parameters :
nterms_base = 2
nterms_band = 1

# This is it, this is your LombScargle code ! Pick one of the 2 below
model = periodic.LombScargleMultiband(Nterms_base=nterms_base, Nterms_band=nterms_band)
##model = periodic.SuperSmoother(fit_period=True)

# How many n best periods do you want from the fit?
n = 6

# The list of light curves 
list_of_index = [82,173]
##list_of_index = [101,26,11,334,33,289,14,59,82,173]

# The Miniminum threshold so that we don't pick up periods too close to one another
threshold = 5E-3

# This other threshold refers to the min threshold for power 
threshold_pow = 0.1398

# Do you want your light_curves down-sampled ?
choice = 'Yes' 		# Down-sample it !!
##choice = 'No' 	# Do not down-sample it !!

# Defining 'No' choice
def main_no():

	# This is NOT down-sampled
	for i in list_of_index:
		
		# Gets all the information of the rr_lyrae
		t,mag,dmag,metadata,nobs = rr_info(i)
	
	    # Returns 
		nobs,period_n,period_true = Give_Func.give_me_n_best_periods(i,model,n,t,mag,dmag,
																metadata,nobs,threshold)
		
		# The n best periods' power as <type 'numpy.ndarray'> of <type 'numpy.float64'>
		power = model.score(period_n)
		print('power:',power)
		
		# Comparing power with the threshold
		for j,significance in enumerate(power):
			if significance > threshold_pow:
				if period_n[j] < 1 :
					print('fit template')
					print('signififnace',significance)
					print('period',period_n[j])
								
# Defining you 'Yes' choice
def main_yes():

	# This IS down-sampled
	for i in list_of_index:
		
		# Gets all the information of the rr_lyrae
		t,mag,dmag,metadata,nobs = rr_info(i)
		
		# The Down sampled array
		d_array = Give_Func.Give_Me_Down_Sample(nobs)
		
	    # Returns
		l_curves = Give_Func.Give_Me_Light_Curves_Down_Sampled(i,model,n,t,mag,dmag,
															   metadata,d_array,threshold)
		
		# Individual items in l_curves contains snobs, period_n + period_true
		for items in l_curves:
			snobs,period_n,period_true = items
			
			# n best periods' power as <type 'numpy.ndarray'> of <type 'numpy.float64'>
			power = model.score(period_n)
			print('power:',power)
		
			# Comparing power with the threshold
			for j,significance in enumerate(power):
				if significance > threshold_pow:
					if period_n[j] < 1 :
						print('fit template')
						print('signififnace',significance)
						print('period',period_n[j])

# It will run for you the program, depending whether you want it down-sampled or not.			
if choice =='Yes':
	main_yes()		# Down-sample it !!
else:
	main_no()		# Do not down-sample it !!

	
	
	