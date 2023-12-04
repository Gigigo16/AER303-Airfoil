"""
Script for calculating all measured data uncertainties at all AoAs and ports.
    {Depenancies}: scipy, matplotlib, numpy
"""
# IMPORTS
#####################
# Dependancies
from scipy import io
import matplotlib.pyplot as plt
import numpy as np
import csv

# Custom Functions/libraies
from Uncertainty import *


# DEFINITIONS
########################
# airfoil tap positions: 
air_top_tap_pos = [0, 0.03, 0.06, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00]
air_bot_tap_pos = [0.90, 0.60, 0.40, 0.30, 0.20, 0.10, 0.05]
gain = 115 # From in lab calibration code
offset = 50 # From in lab calibration code
Hg2Pa = 9.80665 #inHg to Pa convertion factor

# Angles of Attack
alpha = [0, 4, 6, 8, 9, 10, 11, 12, 14, 15, 17]

dP_a = np.zeros((len(alpha), 19))
dP_r1 = np.zeros((len(alpha), 17))
dP_r2 = np.zeros((len(alpha), 17))

for i, a in enumerate(alpha):

    data = io.loadmat(".\data\Filtered\Experimental_data_%d.mat"%a)
    # ['__header__', '__version__', '__globals__', 'AoA', 'ask', 'None', 
    # 'f_s', 'i', 'k', 'p_airfoil', 'p_rake1', 'p_rake2', 'prompt', 'spdata', 'sptime', 
    # 't_s', 'wpdata', 'wpdata2', 'wptime1', 'wptime2', 'x', 'y', 'y2', '__function_workspace__']

    #error calcs:
    for k in range(1, 20):
        dP_a[i, k-1] = DataErr((data['spdata'][k-1]*gain + offset)*Hg2Pa)
        # Bxx = DataErr((data['spdata'][0]*gain + offset)*Hg2Pa)
        if (k < 18):
            dP_r1[i, k-1] = DataErr((data['wpdata'][k-1]*gain + offset)*Hg2Pa)
            dP_r2[i, k-1] = DataErr((data['wpdata2'][k-1]*gain + offset)*Hg2Pa)

    if i == 0:
        break

np.savetxt("data\CSV\dP_airfoil.csv", dP_a, delimiter=",")
np.savetxt("data\CSV\dP_rakepos1.csv", dP_r1, delimiter=",")
np.savetxt("data\CSV\dP_rakepos2.csv", dP_r2, delimiter=",")