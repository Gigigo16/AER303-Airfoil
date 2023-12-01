"""
Main script for running all data processing and plotting.
    {Depenancies}: scipy, matplotlib, numpy
"""
#imports:
from scipy import io
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from ReynoldsNumber import *
#from Forces import *

# DEFINITIONS
########################
# airfoil tap positions: 
air_top_tap_pos = [0, 0.03, 0.06, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00]
air_bot_tap_pos = [0.90, 0.60, 0.40, 0.30, 0.20, 0.10, 0.05]

# Angles of Attack
alpha = [0, 4, 6, 8, 9, 10, 11, 12, 14, 15, 17]

for i in alpha:
    data = io.loadmat(".\data\Filtered\F-Experimental_data_%d.mat"%i)
    p_foil_top = data['p_airfoil'][0][0:12]
    p_foil_bot = data['p_airfoil'][0][12:18]


Re = ReynoldsNumber(L=0.1)





####################################################################
# TOO BE REMOVED BEFORE SUBMISSION TEST ONLY
mat = io.loadmat("data\Filtered\F-Experimental_data_0.mat")

p_foil_top = data['p_airfoil'][0][0:12]
p_foil_bot = data['p_airfoil'][0][12:19]

plt.plot(air_top_tap_pos, p_foil_top)
plt.plot(air_bot_tap_pos, p_foil_bot)
plt.show()
####################################################################