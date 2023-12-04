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

def CpGraph(a: np.int32, Cp_top: np.array, Cp_bot: np.array, Cp_top_err: np.array, Cp_bot_err: np.array):
    '''
    PLots the Coefficient of pressure distribution.

    Parameters:
    -----------   
    a : np.int32
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

    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    plt.rcParams.update({'font.size': 12})

    plt.plot(xfoil_x, xfoil_cp, color = 'r')
    plt.errorbar(air_top_tap_pos, Cp_top, yerr=Cp_top_err, color = 'c', marker = 'o')
    plt.errorbar(air_bot_tap_pos, Cp_bot, yerr=Cp_bot_err, color = 'c', marker = 'o')
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    plt.title('$C_{P}$ vs x/c: $α$ = ' + str(a) + u'\N{DEGREE SIGN}')
    plt.xlabel('x/c')
    plt.ylabel('$C_{P}$')
    plt.legend(['Theoretical XFoil Data', 'Experimental $C_{P}$'])
    plt.gca().invert_yaxis()
    plt.grid()
    plt.savefig('results\C_p-graphs\C_p-a%d.png'%a)
    # plt.show()
    plt.clf()

def VelGraph(a: np.int32, V_r: np.array, V_r_err: np.array, V_pos: np.array):
    '''
    PLots the velocity wake distribution.

    Parameters:
    -----------   
    a : np.int32
        angle of attack
    V_r : np.array
        vel dist
    V_r_err : np.array
        error in vel dist
    V_pos : np.array
        tap positions
    '''

    plt.errorbar(V_r, V_pos, xerr=V_r_err, color = 'c', marker = 'o')
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    plt.title('Wake velocity profile: $α$ = ' + str(a) + u'\N{DEGREE SIGN}')
    plt.xlabel('velocity (m/s)')
    plt.ylabel('tap y-pos (cm)')
    plt.legend(['Experimental velocity'])
    # plt.gca().invert_xaxis()
    plt.grid()
    plt.savefig('results\\vel-graphs\\vel-a%d.png'%a)
    # plt.show()
    plt.clf()

def CoeffGraph(a: np.int32, V_r: np.array, V_r_err: np.array, V_pos: np.array):
    '''
    PLots the Coefficient of L and D and M distribution.

    Parameters:
    -----------   
    a : np.int32
        angle of attack
    V_r : np.array
        vel dist
    V_r_err : np.array
        error in vel dist
    V_pos : np.array
        tap positions
    '''

    Xfoil_parsed = []
    with open("data\XFOIL\clarky_coeff.txt") as X:
        data = (X.read())
        data = data.split('\n')[12:]
        for i in data:
            Xfoil_parsed.append(i.strip().split('  '))
    
    xfoil_a = []
    xfoil_cl = []
    xfoil_cd = []
    xfoil_cm = []

    for line in Xfoil_parsed[:-1]:
        xfoil_a.append(float(line[0]))
        xfoil_cl.append(float(line[1]))
        xfoil_cd.append(float(line[2]))
        xfoil_cm.append(float(line[4]))

    plt.rcParams['mathtext.fontset'] = 'stix'
    plt.rcParams['font.family'] = 'STIXGeneral'
    plt.rcParams.update({'font.size': 12})

    plt.plot(xfoil_a, xfoil_cl, color = 'r')
    # plt.errorbar(air_top_tap_pos, Cp_top, yerr=Cp_top_err, color = 'c', marker = 'o')
    # plt.errorbar(air_bot_tap_pos, Cp_bot, yerr=Cp_bot_err, color = 'c', marker = 'o')
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    plt.title('$C_{L}$ vs $α$')
    plt.xlabel('$α$')
    plt.ylabel('$C_{L}$')
    plt.legend(['Theoretical XFoil Data', 'Experimental $C_{L}$'])
    plt.grid()
    # plt.savefig('results\C_p-graphs\C_p-a%d.png'%a)
    plt.show()
    plt.clf()