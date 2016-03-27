##########################################################################################
#
# What: Run_me_with_down_sample.py
#
# Pair: Give_me_n_best_periods_Function.py
# 
# Date : Mar 14, 2016
##########################################################################################

'''
Utilises a function to run down-sampled light curves and give you 'n' best periods

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
l_curves : <type 'list'> containing <type 'tuple'>  
    Each tuple will contain : 
    
l_curves[index][0] : snobs : <type 'int'>
    The Number of Observations/Nights that has been downsampled
    	
l_curves[index][1] : tze_periods : <type 'numpy.ndarray'> of <type 'numpy.float32'>
    A numpy array of the 'n' best periods 
    			
l_curves[index][2] : metadata['P'] : <type 'numpy.float32'>	
    The system's best average period ie Vandplas periods
    	
'''

# Project
import Give_me_n_best_periods_Function as Give_Func
from gatspy import periodic
from gatspy.datasets import fetch_rrlyrae

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
	metadata = rrlyrae.get_metadata(lcid)

	# Number of observations - original size
	nobs = t.size
	
	return t,mag,dmag,metadata,nobs

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

# The Miniminum threshold so that we don't pick up periods too close to one another
threshold = 5E-3

# This other threshold refers to the min threshold for power 
threshold_Pow = 3

# Let's run it !
def main():
	for i in list_of_index:
	
		# Gets all the information of the rr_lyrae
		t,mag,dmag,metadata,nobs = rr_info(i)
		
		# The Down sampled array
		d_array = Give_Func.Give_Me_Down_Sample(nobs)
		
		# Returns
		l_curves = Give_Func.Give_Me_Light_Curves_Down_Sampled(i,model,n,t,mag,dmag,
								  metadata,d_array,threshold)
		print(l_curves)
    	
main()
