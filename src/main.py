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
from Graphing import *


# DEFINITIONS
########################
# airfoil tap positions: 
air_top_tap_pos = [0, 0.03, 0.06, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00]
air_bot_tap_pos = [0.90, 0.60, 0.40, 0.30, 0.20, 0.10, 0.05]

# airfoil cord length
c = 0.1 #m

# Angles of Attack
alpha = [0, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17] #12
dalpha = 1 #deg uncertainty in AoA

# calibration data
gain = 115 # From in lab calibration code
offset = 50 # From in lab calibration code
Hg2Pa = 9.80665 #inHg to Pa convertion factor

# baselines of rake positions:
y_0 = np.array([12, 12, 11.5, 11, 11.5, 11, 11.5, 12.5, 11.5, 12, 12.4, 12]) - 3.33 # inital position of the bottom port
dir = [1, -1, -1, 1, -1, 1, 1, -1, -2, 1, -1, 1] #direction rake was moved -1 = down 1 = up

print("Loading Clark Y Airfoil Coordinates...")
# LOADING CLARK_Y_AIRFOIL COORDINATES
##############################
with open(".\data\Clark_Y_Airfoil.csv", newline='') as f:
    points = csv.reader(f, delimiter=';')
    data = list(points)
    data.pop(0)

# Converting to float
i = 0
for row in data:
    data[i] = list(map(float, row))
    i += 1

is_top = True
airfoil_top = []
airfoil_bot = []
for i in range(0,len(data)):
    if i != 0 and float(data[i][0]) == float(0.0):
        is_top = False
    if is_top and float(data[i][0]) in air_top_tap_pos:
        airfoil_top.append([float(data[i][0]), float(data[i][1])])
    elif not is_top and float(data[i][0]) in air_bot_tap_pos:
        airfoil_bot.append([float(data[i][0]), float(data[i][1])])

print(len(airfoil_top))
print(len(airfoil_bot))
# Convert to np.array
airfoil_top = np.array(airfoil_top)*0.1  # Multiplying values by cord length (values given are per unit cord)
airfoil_bot = np.array(airfoil_bot)*0.1 # Multiplying values by cord length (values given are per unit cord)

print("Loading Experimental Data...")

# Data array initialization
pressure_data = []
rake_press = []
y_rake_pos = []
Cl_list = []
dCl_list = []
Cd_list = []
dCd_list = []
Cm_list = []
dCm_list = []
Cdt_list = []
dCdt_list = []

# PROCESSING DATA
########################
print("=========================================")
print("Beginning Analysis...")
print("=========================================")
for i,a in enumerate(alpha):
    print("Processing AoA = %d..."%a)

    # this data was pre-filtered in matlab
    # errors were calculated in errcalc.py
    data_raw = io.loadmat(".\data\Filtered\Experimental_data_%d.mat"%a)
    # ['__header__', '__version__', '__globals__', 'AoA', 'ask', 'None', 
    # 'f_s', 'i', 'k', 'p_airfoil', 'p_rake1', 'p_rake2', 'prompt', 'spdata', 'sptime', 
    # 't_s', 'wpdata', 'wpdata2', 'wptime1', 'wptime2', 'x', 'y', 'y2', '__function_workspace__']



    # data calibration:
    p_top = (data_raw['p_airfoil'][0][0:12]*gain + offset)*Hg2Pa
    p_bot = (data_raw['p_airfoil'][0][12:19]*gain + offset)*Hg2Pa
    p_r1 = (data_raw['p_rake1']*gain + offset)*Hg2Pa
    p_r2 = (data_raw['p_rake2']*gain + offset)*Hg2Pa
    
    p = (data_raw['p_airfoil'][0]*gain + offset)*Hg2Pa
    pressure_data.append(list(map(float, p)))
    


    # Initializing error arrays
    p_r1_err = np.zeros_like(p_r1) #temp
    p_r2_err = np.zeros_like(p_r2) #temp
    p_top_err = np.zeros_like(p_top) #temp
    p_bot_err = np.zeros_like(p_bot) #temp
    
    # Parsing error data from CSV files
    with open('data\CSV\dP_airfoil.csv') as f:
        reader = csv.reader(f)
        data_err_a = list(reader)
        data_err_a = [eval(e) for e in data_err_a[i]]
        p_top_err = data_err_a[0:12]
        p_bot_err = data_err_a[12:19]
    with open('data\CSV\dP_rakepos1.csv') as f:
        reader = csv.reader(f)
        data_err_r1 = list(map(np.float64,reader))
        p_r1_err = np.array(data_err_r1)[i]

    with open('data\CSV\dP_rakepos2.csv') as f:
        reader = csv.reader(f)
        data_err_r2 = list(map(np.float64,reader))
        p_r2_err = np.array(data_err_r2)[i]

    
    # finding the wake velocity distribution:
    pos_r1 = y_0[i]
    pos_r2 = y_0[i] + dir[i]*0.5
    
    U_inf, U_inf_err, V_r, V_r_err, V_pos, P_comb, P_comb_err = Velocity(p_r1, p_r2, p_r1_err, p_r2_err, pos_r1, pos_r2)

    rake_press.append(list(map(float, P_comb)))
    y_rake_pos.append(list(map(float, V_pos)))

    # Plotting velocity distribution
    VelGraph(a, V_r, V_r_err, V_pos)


    #finding the dynamic freestream pressure
    q_inf, q_inf_err = DynPressure(U_inf, U_inf_err)


    #finding the Cp distribution over the airfoil

    #finding the lift and total drag
    Dt, Dt_err = TotalDrag(V_pos/100, V_r, V_r_err, U_inf, U_inf_err)

    # Finding normal, axial forces and moment forces
    N, dN = NormalForce(p_top, p_bot, p_top_err, p_bot_err, airfoil_top, airfoil_bot)
    A, dA = AxialForce(p_top, p_bot, p_top_err, p_bot_err, airfoil_top, airfoil_bot)
    M, dM = MomentLE(p_top, p_bot, p_top_err, p_bot_err, airfoil_top, airfoil_bot)

    # Finding lift and drag forces
    L, dL = LiftForce(a, dalpha, N, dN, A, dA)
    D, dD = PressureDragForce(a, dalpha, N, dN, A, dA)

    # Finding pressure coefficients
    Cp_top, Cp_bot, Cp_top_err, Cp_bot_err = Cpressure(p_top, p_bot, p_top_err, p_bot_err, q_inf, q_inf_err)

    # total drag coefficient
    Cdt, dCdt = Ctotaldrag(Dt, Dt_err, q_inf, q_inf_err, c)

    # finding remaining Coefficients
    Cl, dCl, Cd, dCd, Cm, dCm =Coefficients(L, dL, D, dD, M, dM, q_inf, q_inf_err, c)

    # Plotting Cp distribution
    CpGraph(a, Cp_top, Cp_bot, Cp_top_err, Cp_bot_err)

    # Storing data
    Cl_list.append(Cl)
    Cd_list.append(Cd)
    Cm_list.append(Cm)
    Cdt_list.append(Cdt)
    dCl_list.append(dCl)
    dCd_list.append(dCd)
    dCm_list.append(dCm)
    dCdt_list.append(dCdt)



print("Analysis Complete...")
print("=========================================")
# Plotting data
CoeffGraph(alpha, Cl_list, dCl_list, Cd_list, dCd_list, Cm_list, dCm_list, Cdt_list, dCdt_list)

print("Saving Data...")
# Saving data raw data to CSV
PressuretoCSV(alpha, np.array(pressure_data))
RakePressuretoCSV(alpha, np.array(rake_press), np.array(y_rake_pos))