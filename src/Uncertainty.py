"""
Functions related to finding the autocorrelation 
    and resultant uncertainties in the measured data
    {Depenancies}: scipy, matplotlib, numpy, pandas
"""
# IMPORTS
#####################
# Dependancies
from scipy import io
import matplotlib.pyplot as plt
import numpy as np
import csv


def DataErr(raw_p: np.array):

    '''
    Returns the uncertainty in measured pressure data.

    Parameters:
    -----------   
    raw_p : np.array
        raw, filtered pressure data for single AoA and single port

    Returns:
    --------    
    dP: uncertainty in measurements for input series
    '''

    mu = raw_p.mean()
    var = np.var(raw_p)
    x = raw_p - mu

    # we use the correlate function to determine self correlation for xp
    # it is subsequently normalized
    # first half is also truncated since it is symmetric
    Bxx = np.correlate(x, x, mode='full')[len(raw_p)-1:]/var/len(raw_p)
     
    #find index of first root:
    lim = np.where(Bxx < 0)[0][0]
    print(Bxx)
    #finding the integral time scale:
    dt = 1/30000\
    T = np.trapz(Bxx[:lim], dx=dt) 
    #T = sum(Bxx[:lim]) * dt
    N = len(raw_p)/(2*T) * dt
    std = np.std(raw_p)
    dP = 1.96*std/np.sqrt(N)

    return dP