"""
Functions related to plotting results
"""
# IMPORTS
#####################
# Dependancies
from scipy import io
import matplotlib.pyplot as plt
import numpy as np
import csv

def CpGraph(a, Cp_top: np.array, Cp_bot: np.array, Cp_top_err: np.array, Cp_bot_err: np.array):
    '''
    PLots the Coefficient of pressure distribution.

    Parameters:
    -----------   
    a : np.int
        angle of attack
    p_top : np.array
        top airfoil pressure distribution
    p_bot : np.array
        bottom airfoil pressure distribution
    p_top_err : np.array
        top airfoil perssure error
    p_bot_err : np.array
        bottom airfoil perssure error
    
    '''
    air_top_tap_pos = [0, 0.03, 0.06, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00]
    air_bot_tap_pos = [0.90, 0.60, 0.40, 0.30, 0.20, 0.10, 0.05]
        
    Xfoil_parsed = []
    with open("data\XFOIL\\a%d.txt"%a) as X:
        data = (X.read())
        data = data.replace('-', ' -').split('\n')[3:]
        for i in data:
            Xfoil_parsed.append(i.strip().split('  '))
    
    xfoil_x = []
    xfoil_cp = []

    for line in Xfoil_parsed[:-1]:
        xfoil_x.append(float(line[0]))
        xfoil_cp.append(float(line[2]))

    Cp_top_err = Cp_top_err/30
    Cp_bot_err = Cp_bot_err/30

    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    plt.rcParams.update({'font.size': 12})

    plt.plot(xfoil_x, xfoil_cp, color = 'r')
    plt.errorbar(air_top_tap_pos, Cp_top, yerr=Cp_top_err, color = 'c', marker = 'o')
    plt.errorbar(air_bot_tap_pos, Cp_bot, yerr=Cp_bot_err, color = 'c', marker = 'o')
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    plt.title('$C_{P}$ vs x/c: AoA = ' + str(a) + u'\N{DEGREE SIGN}')
    plt.xlabel('x/c')
    plt.ylabel('$C_{P}$')
    plt.legend(['Theoretical XFoil Data', 'Experimental $C_{P}$'])
    plt.gca().invert_yaxis()
    plt.grid()
    plt.savefig('results\C_p-graphs\C_p-a%d.png'%a)
    # plt.show()
    plt.clf()