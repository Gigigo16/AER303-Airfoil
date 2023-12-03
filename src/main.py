"""
Main script for running all data processing and plotting.
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
from ReynoldsNumber import *
from Forces import *
from Velocity import *
from Coefficients import *


# DEFINITIONS
########################
# airfoil tap positions: 
air_top_tap_pos = [0, 0.03, 0.06, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00]
air_bot_tap_pos = [0.90, 0.60, 0.40, 0.30, 0.20, 0.10, 0.05]

# Angles of Attack
alpha = [0, 4, 6, 8, 9, 10, 11, 12, 14, 15, 17]

# LOADING CLARK_Y_AIRFOIL COORDINATES
##############################
with open(".\data\Clark_Y_Airfoil.csv", newline='') as f:
    points = csv.reader(f, delimiter=';')
    data = list(points)

is_top = True
airfoil_top = []
airfoil_bot = []
for i in range(1,len(data)):
    if i != 0 and float(data[i][0]) == float(0.0):
        is_top = False
    if is_top and float(data[i][0]) in air_top_tap_pos:
        airfoil_top.append([float(data[i][0]), float(data[i][1])])
    elif float(data[i][0]) in air_bot_tap_pos:
        airfoil_bot.append([float(data[i][0]), float(data[i][1])])
# Convert to np.array
airfoil_top = np.array(airfoil_top)*0.1  # Multiplying values by cord length (values given are per unit cord)
airfoil_bot = np.array(airfoil_bot)*0.1 # Multiplying values by cord length (values given are per unit cord)


# PROCESSING DATA
########################
for i in alpha:

    data = io.loadmat(".\data\Filtered\Experimental_data_%d.mat"%i)

    # data calibration:
    gain = 115
    offset = 50
    Hg2Pa = 9.80665
    p_top = (data['p_airfoil'][0][0:12]*gain + offset)*Hg2Pa
    p_bot = (data['p_airfoil'][0][12:19]*gain + offset)*Hg2Pa
    p_r1 = (data['p_rake1']*gain + offset)*Hg2Pa
    p_r2 = (data['p_rake2']*gain + offset)*Hg2Pa

    #print((data['p_airfoil'][0]*gain + offset)*Hg2Pa)
    #print(p_top, p_bot)

    p_r1_err = np.zeros_like(p_r1) #temp
    p_r2_err = np.zeros_like(p_r2) #temp
    p_top_err = np.zeros_like(p_top) #temp
    p_bot_err = np.zeros_like(p_bot) #temp

    # finding the wake velocity distribution:
    U_inf, U_inf_err, v_r1, v_r2, v_r1_err, v_r2_err = Velocity(p_r1, p_r2, p_r1_err, p_r2_err)
    print(U_inf, U_inf_err)
    
    #finding the dynamic freestream pressure
    q_inf, q_inf_err = DynPressure(U_inf, U_inf_err)
    # print(q_inf)

    #finding the Cp distribution over the airfoil
    Cp_top, Cp_bot, Cp_top_err, Cp_bot_err = Cpressure(p_top, p_bot, p_top_err, p_bot_err, q_inf, q_inf_err)
    # print(Cp_top)

    #print(p_bot, Cp_bot, air_bot_tap_pos)

    ##TEST:
    y = [0, 1.67, 3.33, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16.67, 18.33, 20]
    #plt.plot(v_r1[0], y)
    #plt.plot(air_top_tap_pos, Cp_top)
    #plt.plot(air_bot_tap_pos, Cp_bot)
    #plt.gca().invert_yaxis()
    #plt.title(i)
    #plt.show()



    





####################################################################
# TOO BE REMOVED BEFORE SUBMISSION TEST ONLY
#mat = io.loadmat("data\Filtered\Experimental_data_0.mat")

# p_foil_top = data['p_airfoil'][0][0:12]
# p_foil_bot = data['p_airfoil'][0][12:19]

# plt.plot(air_top_tap_pos, p_foil_top)
# plt.plot(air_bot_tap_pos, p_foil_bot)
# plt.show()
####################################################################
