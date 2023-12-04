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
from PressuretoCSV import *
from Uncertainty import *


# DEFINITIONS
########################
# airfoil tap positions: 
air_top_tap_pos = [0, 0.03, 0.06, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00]
air_bot_tap_pos = [0.90, 0.60, 0.40, 0.30, 0.20, 0.10, 0.05]

# Angles of Attack
alpha = [0, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17]

# calibration data
gain = 115 # From in lab calibration code
offset = 50 # From in lab calibration code
Hg2Pa = 9.80665 #inHg to Pa convertion factor

# baselines of rake positions:
y_0 = np.array([12, 11.5, 11.5, 11, 11, 11, 11.5, 11, 11.5, 12.4, 11.5, 12, 12.4, 12]) - 3.33 # inital position of the bottom port
dir = [1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1] #direction rake was moved -1 = down 1 = up

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

pressure_data = []
# PROCESSING DATA
########################
for i,a in enumerate(alpha):

    data = io.loadmat(".\data\Filtered\Experimental_data_%d.mat"%a)
    # ['__header__', '__version__', '__globals__', 'AoA', 'ask', 'None', 
    # 'f_s', 'i', 'k', 'p_airfoil', 'p_rake1', 'p_rake2', 'prompt', 'spdata', 'sptime', 
    # 't_s', 'wpdata', 'wpdata2', 'wptime1', 'wptime2', 'x', 'y', 'y2', '__function_workspace__']

    # data calibration:
    p_top = (data['p_airfoil'][0][0:12]*gain + offset)*Hg2Pa
    p_bot = (data['p_airfoil'][0][12:19]*gain + offset)*Hg2Pa
    p_r1 = (data['p_rake1']*gain + offset)*Hg2Pa
    p_r2 = (data['p_rake2']*gain + offset)*Hg2Pa
    
    p = (data['p_airfoil'][0]*gain + offset)*Hg2Pa
    pressure_data.append(list(map(float, p)))
    

    p_r1_err = np.zeros_like(p_r1) #temp
    p_r2_err = np.zeros_like(p_r2) #temp
    p_top_err = np.zeros_like(p_top) #temp
    p_bot_err = np.zeros_like(p_bot) #temp

    with open('data\Filtered\dP_a.csv') as f:
        reader = csv.reader(f)
        data = list(reader)
        data = [eval(e) for e in data[0]]
        # print(len(data))
    p_top_err = data[0:12]
    p_bot_err = data[12:19]

    # finding the wake velocity distribution:
    pos_r1 = y_0[i]
    pos_r2 = y_0[i] + dir[i]*0.5
    U_inf, U_inf_err, V_r, V_r_err, V_pos = Velocity(p_r1, p_r2, p_r1_err, p_r2_err, pos_r1, pos_r2)

    if i>7:
        plt.plot(V_r, V_pos)
        plt.title(i)
        plt.show()

    # print(U_inf, U_inf_err)
    
    #finding the dynamic freestream pressure
    q_inf, q_inf_err = DynPressure(U_inf, U_inf_err)

    #finding the Cp distribution over the airfoil
    Cp_top, Cp_bot, Cp_top_err, Cp_bot_err = Cpressure(p_top, p_bot, p_top_err, p_bot_err, q_inf, q_inf_err)
    # print((Cp_top_err))

PressuretoCSV(alpha, np.array(pressure_data))