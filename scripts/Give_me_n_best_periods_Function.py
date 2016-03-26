##########################################################################################
#
# What  : Give_me_n_best_periods_Function.py
#
# Pair  : Run_me.py
#		: Run_me_with_down_sample.py		 
# 
# Date  : Mar 14, 2016
##########################################################################################

'''
This will take in a model fit -- LombscargleMultibandFast or LombscargleMultiband 
#		(you have to specify)+ index from 0 to 483 , and return for you n best periods

'''

from __future__ import print_function
import gatspy
import matplotlib.pyplot as plt
import numpy as np
from gatspy import periodic
from gatspy.periodic import LombScargleMultiband
import astroML
import random
from gatspy.datasets import fetch_rrlyrae

def give_me_n_best_periods(i,model,n):
    '''
    This gives you n best periods but does NOT downsample for you
    
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
    
    # It's finding the rr_lyraes by index + fit that you specify
    rrlyrae = fetch_rrlyrae()
    lcid = rrlyrae.ids[i]
    t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)
    metadata = rrlyrae.get_metadata(lcid)
    
    # Number of observations - original size
    nobs = t.size
    
    # Number of Observations + down-sampled n best periods to be returned
    returned_list=[]
    
    # Let's fit it
    model.optimizer.period_range = (0.1, 1.) 
    
    # This is all fitted with 4.2 Truncated Fourier Models with VanderPlas paper
    model.fit(t,mag,dmag)
    model.best_period  
        
    # Finding the periods, and then sorting it by argument of the strongest power(score)
    periods = np.linspace(0.1, 1., 10000)
    scores = model.score(periods)
    idx = np.argsort(scores)
    tze_periods = np.array([])
    
    # The Miniminum threshold so that we don't pick up periods too close to one another
    threshold = 5E-3
    
    # Let's pick up those periods
    for period in periods[idx][::-1]:
        if (np.abs(tze_periods - period) > threshold).all() or (len(tze_periods) < 1):
            tze_periods = np.append(tze_periods, [period])
        
        if len(tze_periods) >= n:
            break
            
    tze_periods = tze_periods[::-1]    
        
    # Getting the infomation to be returned
    returned_list.append(nobs)
    returned_list.append(tze_periods)
    returned_list.append(metadata['P'])
    

    return returned_list
    
def give_me_nobs(i,model,n):
    '''
    This gives you the number of observations
    
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
    nobs : <type 'int'>
    	The Number of Observations/Nights
    
    '''
	
    # It's finding the rr_lyraes by index and feeding it with information
    rrlyrae = fetch_rrlyrae()
    lcid = rrlyrae.ids[i]
    t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)
    
    # Number of observations - original size
    nobs = t.size
    
    
    return nobs


def Give_Me_Down_Sample(nobs):
    '''
    This will give you a down-sampled array based on log 2
    It's downsampling the number of observations needed 
    
    Parameters
    ----------
    nobs : <type 'int'>
    	The Number of Observations/Nights 
    
    Returns
    -------
    down_sample_array : <type 'numpy.ndarray'> of <type 'int'>
    	Returns a down-sampled array with base 2 : eg 2^1, 2^2 ... up to # observations
   
    '''
    down_sample_array = 2**np.arange(3,10)
    down_sample_array = down_sample_array[::-1]
    down_sample_array = np.insert(down_sample_array, 0, nobs) 
    down_sample_list = down_sample_array.tolist()
    down_sample_list[:] = (value for value in down_sample_list if value <= nobs)
    down_sample_array = np.asarray(down_sample_list)
    
    
    return down_sample_array
  
             
def Give_Me_Light_Curves_Down_Sampled(i,nobs,model,n,d_array):
    '''
    This gives you n best periods AND it would have downsample it for you
   
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
    returned_list : <type 'list'> 
    	This list will contain <type 'tuple'>  
    	Each tuple will contain : 
    
    returned_list[index][0] : snobs : <type 'int'>
    	The Number of Observations/Nights that has been downsampled
    	
    returned_list[index][1] : tze_periods : <type 'numpy.ndarray'> of <type 'numpy.float32'>
    		A numpy array of the 'n' best periods 
    			
    returned_list[index][2] : metadata['P'] : <type 'numpy.float32'>	
    	The system's best average period ie Vandplas periods
    
    '''
    			 
    # Number of Observations + down-sampled n best periods to be returned
    returned_list=[]
    
    # It's finding the rr_lyraes by index and feeding it information
    rrlyrae = fetch_rrlyrae()
    lcid = rrlyrae.ids[i]
    t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)
    metadata = rrlyrae.get_metadata(lcid)
    
    # Down-sampling the data !!
    for items in d_array:
        
        # This is the downsampled number of observations
        snobs = items
        
        # Turning the information into a tuple
        zipped = zip(t,mag,dmag)
        
        # Randomly sampling the information as a tuple
        sam = random.sample(zipped, snobs)
        
        # Shuffling the random sample back to their respective houses 
        t2 = []
        mag2= []
        dmag2 = []
        for i in range(len(sam)):
            t2.append(sam[i][0])
            mag2.append(sam[i][1])
            dmag2.append(sam[i][2])
        
        # Turning the information into an array for use
        t = np.asarray(t2)   
        mag = np.asarray(mag2)
        dmag = np.asarray(dmag2)
            
        # Let's fit it
        model.optimizer.period_range = (0.1, 1.) 
    
        # This is all fitted with 4.2 Truncated Fourier Models with VanderPlas paper
        model.fit(t,mag,dmag)
        model.best_period  
        
        # Finding the periods, and then sorting it by argument of the strongest power(score)
        periods = np.linspace(0.1, 1., 10000)
        scores = model.score(periods)
        idx = np.argsort(scores)
        tze_periods = np.array([])
        
        # The Miniminum threshold so that we don't pick up periods too close to one another
        threshold = 5E-3
        
        # Let's pick up those periods
        for period in periods[idx][::-1]:
            if (np.abs(tze_periods - period) > threshold).all() or (len(tze_periods) < 1):
                tze_periods = np.append(tze_periods, [period])
        
            if len(tze_periods) >= n:
                break
                
        tze_periods = tze_periods[::-1]    
        
        # Getting the infomation to be returned
        combo = snobs, tze_periods, metadata['P']
    	returned_list.append(combo)
    
    
    return returned_list
