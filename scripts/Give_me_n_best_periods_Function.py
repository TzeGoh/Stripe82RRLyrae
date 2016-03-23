##########################################################################################
#
# What: Give_me_n_best_periods_Function.py
#
# How : This will take in a model fit -- LombscargleMultibandFast or LombscargleMultiband 
#		(you have to specify)+ index from 0 to 483 , and return for you the 5 best periods
# 
# Date : Mar 14, 2016
##########################################################################################

from __future__ import print_function
import gatspy
import matplotlib.pyplot as plt
import matplotlib.pyplot as pl
import numpy as np
from gatspy import periodic
from gatspy.periodic import LombScargleMultiband
import astroML
import random
from gatspy.datasets import fetch_rrlyrae

def give_me_n_best_periods(i,model,n):
    '''This gives you n best periods but does not downsample for you'''
    
    # It's finding the rr_lyraes by index + fit that you specify
    rrlyrae = fetch_rrlyrae()
    lcid = rrlyrae.ids[i]
    t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)
    metadata = rrlyrae.get_metadata(lcid)
    
    # these are the ids of the rr lyrae
    idx_of_plot = i
    lcid = rrlyrae.ids[i]
    metadata = rrlyrae.get_metadata(lcid)
    t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)
    
    # Number of observations - original size
    nobs = t.size
    
    # Number of Observations + down-sampled n best periods to be returned
    returned_list=[]
    
    # Spelling out the number of periods that you gave
    no_of_periods_specified = n 
    
    # Let's fit it
    model.optimizer.period_range = (0.1, 1.) 
    
    # This is all fitted with 4.2 Truncated Fourier Models with VanderPlas paper
    model.fit(t,mag,dmag)
    model.best_period  
        
    # Finding the periods, and then sorting it by argument of the strongest power(score)
    periods = np.linspace(0.1, 1., 10000)
    scores = model.score(periods)
    idx = np.argsort(scores)
    ##tze_periods = periods[idx[-5:]]
    ##tze_scores = scores[idx[-5:]]
    tze_periods = np.array([])
    threshold = 5E-3
    for period in periods[idx][::-1]:
        if (np.abs(tze_periods - period) > threshold).all() or (len(tze_periods) < 1):
            tze_periods = np.append(tze_periods, [period])
        
        if len(tze_periods) >= no_of_periods_specified:
            break
    tze_periods = tze_periods[::-1]    
    ##print(tze_periods)
    ##print(tze_scores)
        
    # Getting the infomation to be returned
    ##No. of observations, 'n' number of periods, and the system's best ave
    combo = nobs,tze_periods,metadata['P']
    returned_list.append(combo)
    ##print(no_of_periods_specified,'no_of_periods_specified')
    
    return returned_list
    
    
    
    

def give_me_nobs(i,model,n):'''This gives you number of observations'''
	
    # It's finding the rr_lyraes by index + fit that you specify
    rrlyrae = fetch_rrlyrae()
    lcid = rrlyrae.ids[i]
    t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)
    metadata = rrlyrae.get_metadata(lcid)
    
    # these are the ids of the rr lyrae
    idx_of_plot = i
    lcid = rrlyrae.ids[i]
    metadata = rrlyrae.get_metadata(lcid)
    t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)
    
    # Number of observations - original size
    nobs = t.size
    
    return nobs

'''This will give you a down-sampled array based on log 2'''
def Give_Me_Down_Sample(nobs):
    down_sample_array = 2**np.arange(3,10)
    down_sample_array = down_sample_array[::-1]
    down_sample_array = np.insert(down_sample_array, 0, nobs) 
    down_sample_list = down_sample_array.tolist()
    down_sample_list[:] = (value for value in down_sample_list if value <= nobs)
    down_sample_array = np.asarray(down_sample_list)
    ##down_sample_array = [ 32 , 16,   8]
    return down_sample_array
  
  
  
  
''' You give index number, # observations, model of fit, # best periods, down-sampled array
  # You get No. of observations, 'n' number of periods, and the system's best ave'''            
def Give_Me_Light_Curves_Down_Sampled(i,nobs,model,n,d_array):

    # Number of Observations + down-sampled n best periods to be returned
    returned_list=[]
    
    # Spelling out the number of periods that you gave
    no_of_periods_specified = n 
    
    # It's finding the rr_lyraes by index + fit that you specify
    rrlyrae = fetch_rrlyrae()
    lcid = rrlyrae.ids[i]
    t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)
    metadata = rrlyrae.get_metadata(lcid)
    
    # these are the ids of the rr lyrae
    idx_of_plot = i
    lcid = rrlyrae.ids[i]
    metadata = rrlyrae.get_metadata(lcid)
    t, mag, dmag, filts = rrlyrae.get_lightcurve(lcid)
    
    for items in d_array:
        
        # Down-sampling the data !!
        nobs = items
        legend ='# of Observation:',nobs
        dd = random.sample(zip(t,mag,dmag), nobs)
        
        # Shuffling the random sample back to their respective houses 
        ee = []
        ff= []
        gg = []
        for i in range(len(dd)):
            ee.append(dd[i][0])
            ff.append(dd[i][1])
            gg.append(dd[i][2])
        t = np.asarray(ee)   
        mag = np.asarray(ff)
        dmag = np.asarray(gg)
            
        # Let's fit it
        model.optimizer.period_range = (0.1, 1.) 
    
        # This is all fitted with 4.2 Truncated Fourier Models with VanderPlas paper
        model.fit(t,mag,dmag)
        model.best_period  
        
        # Finding the periods, and then sorting it by argument of the strongest power(score)
        periods = np.linspace(0.1, 1., 10000)
        scores = model.score(periods)
        idx = np.argsort(scores)
        ##tze_periods = periods[idx[-5:]]
        ##tze_scores = scores[idx[-5:]]
        tze_periods = np.array([])
        threshold = 5E-3
        for period in periods[idx][::-1]:
            if (np.abs(tze_periods - period) > threshold).all() or (len(tze_periods) < 1):
                tze_periods = np.append(tze_periods, [period])
        
            if len(tze_periods) >= no_of_periods_specified:
                break
        tze_periods = tze_periods[::-1]    
        ##print(tze_periods)
        ##print(tze_scores)
        
        # Getting the infomation to be returned
        ##No. of observations, 'n' number of periods, and the system's best ave
        combo = nobs,tze_periods,metadata['P']
        returned_list.append(combo)
        ##print(no_of_periods_specified,'no_of_periods_specified')
 
    return returned_list
