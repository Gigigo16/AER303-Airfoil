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
    plt.errorbar(air_top_tap_pos, Cp_top, yerr=Cp_top_err, color = 'c', marker = 'o', capsize=2, elinewidth=1, markeredgewidth=2)
    plt.errorbar(air_bot_tap_pos, Cp_bot, yerr=Cp_bot_err, color = 'c', marker = 'o', capsize=2, elinewidth=1, markeredgewidth=2)
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    plt.title('$C_{P}$ vs x/c: $α$ = ' + str(a) + u'\N{DEGREE SIGN}')
    plt.xlabel('x/c')
    plt.ylabel('$C_{P}$')
    plt.legend(['Theoretical XFoil Data', 'Experimental $C_{P}$'])
    plt.grid()
    plt.ylim(-7.5, 1.5)
    plt.gca().invert_yaxis()
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

    plt.errorbar(V_r, V_pos, xerr=V_r_err, color = 'c', marker = 'o', capsize=2, elinewidth=1, markeredgewidth=2)
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    plt.title('Wake velocity profile: $α$ = ' + str(a) + u'\N{DEGREE SIGN}')
    plt.xlabel('velocity (m/s)')
    plt.ylabel('tap y-pos (cm)')
    plt.legend(['Experimental velocity'])
    # plt.gca().invert_xaxis()
    plt.grid()
    plt.ylim(5,30)
    plt.savefig('results\\vel-graphs\\vel-a%d.png'%a)
    # plt.show()
    plt.clf()

def CoeffGraph(a: np.int32, Cl: np.array, dCl: np.array, Cd: np.array, dCd: np.array, Cm: np.array, dCm: np.array, Cdt: np.array, dCdt: np.array):
    '''
    PLots the Coefficient of L and D and M distribution.

    Parameters:
    -----------   
    a : np.int32
        angle of attack
    Cl : np.array
        lift coefficient
    dCl : np.array
        lift coefficient error
    Cd : np.array
        drag coefficient
    dCd : np.array
        drag coefficient error
    Cm : np.array
        moment coefficient
    dCm : np.array
        moment coefficient error
    Cdt : np.array
        total drag coefficient
    dCdt : np.array
        total drag coefficient error
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
    xfoil_cdp = []
    xfoil_cm = []

    for line in Xfoil_parsed[:-1]:
        xfoil_a.append(float(line[0]))
        xfoil_cl.append(float(line[1]))
        xfoil_cd.append(float(line[2]))
        xfoil_cdp.append(float(line[3]))
        xfoil_cm.append(float(line[4]))

    uiuc_a = []
    uiuc_al = []
    uiuc_cl = []
    uiuc_cl2 = []
    uiuc_cd = []
    
    uiuc_am = []
    uiuc_cm = []


    with open(r"data\UIUC_Data\UIUC_Data.csv", newline='') as U:
        reader = csv.reader(U, delimiter=';')
        reader = list(reader)
        reader = reader[1:]
        for row in reader:
            uiuc_a.append(float(row[0]))
            uiuc_cl2.append(float(row[1]))
            uiuc_cd.append(float(row[2]))

    with open(r"data\UIUC_Data\UIUC_DataCm.csv", newline='') as U:
        reader = csv.reader(U, delimiter=';')
        reader = list(reader)
        reader = reader[1:]
        for row in reader:
            uiuc_al.append(float(row[0]))
            uiuc_cl.append(float(row[1]))
            uiuc_am.append(float(row[2]))
            uiuc_cm.append(float(row[3]))


    print(" Saving C_l-a.png..")
    plt.plot(xfoil_a, xfoil_cl, color = 'r')
    plt.errorbar(a, Cl, xerr=1, yerr=dCl, color = 'c', marker = '.', capsize=2, elinewidth=1, markeredgewidth=2)
    plt.plot(uiuc_al, uiuc_cl, color = 'g')
    params = {'mathtext.default': 'regular' }          
    plt.rcParams.update(params)
    plt.rcParams.update({'font.size': 12})
    plt.title('$C_{L}$ vs $α$')
    plt.xlabel('$α$')
    plt.ylabel('$C_{L}$')
    plt.legend(['Theoretical XFoil Data', 'UIUC Data', 'Experimental $C_{L}$'])
    plt.grid()
    plt.savefig('results\C_l-graphs\C_l-a.png')
    plt.clf()

    print(" Saving C_d-a.png..")
    plt.plot(xfoil_a, xfoil_cdp, color = 'r')
    plt.errorbar(a, Cd, xerr=1, yerr=dCd, color = 'c', marker = '.', capsize=2, elinewidth=1, markeredgewidth=2)
    plt.plot(uiuc_a, uiuc_cd, color = 'g')
    params = {'mathtext.default': 'regular' }
    plt.rcParams.update(params)
    plt.rcParams.update({'font.size': 12})
    plt.title('$C_{D}$ vs $α$')
    plt.xlabel('$α$')
    plt.ylabel('$C_{D}$')
    plt.legend(['Theoretical XFoil Data', 'UIUC Data', 'Experimental $C_{D}$'])
    plt.grid()
    plt.savefig('results\C_d-graphs\C_d-a.png')
    plt.clf()

    print(" Saving C_m-a.png..")
    plt.plot(xfoil_a, xfoil_cm, color = 'r')
    plt.errorbar(a, Cm, xerr=1, yerr=dCm, color = 'c', marker = '.', capsize=2, elinewidth=1, markeredgewidth=2)
    plt.plot(uiuc_am, uiuc_cm, color = 'g')
    params = {'mathtext.default': 'regular' }
    plt.rcParams.update(params)
    plt.rcParams.update({'font.size': 12})
    plt.title('$C_{M}$ vs $α$')
    plt.xlabel('$α$')
    plt.ylabel('$C_{M}$')
    plt.legend(['Theoretical XFoil Data', 'UIUC Data', 'Experimental $C_{M}$'])
    plt.grid()
    plt.savefig('results\C_m-graphs\C_m-a.png')
    plt.clf()
    
    print(" Saving C_Dt-a.png..")
    plt.plot(xfoil_a, xfoil_cd, color = 'r')
    plt.errorbar(a, Cdt, xerr=1, yerr=dCdt, color='c', marker='.', capsize=2, elinewidth=1, markeredgewidth=2)
    params = {'mathtext.default': 'regular'}
    plt.rcParams.update(params)
    plt.rcParams.update({'font.size': 12})
    plt.title('Total Drag ($C_{Dt}$) vs $α$')
    plt.xlabel('$α$')
    plt.ylabel('$C_{Dt}$')
    plt.legend(['Theoretical XFoil Data','Experimental $C_{Dt}$'])
    plt.grid()
    plt.savefig('results\C_Dt-graphs\C_Dt-a.png')
    plt.clf()

    print(" Saving C_l-C_d.png..")
    plt.plot(xfoil_cdp, xfoil_cl, color='r')
    plt.plot(uiuc_cd, uiuc_cl2, color='g')
    plt.errorbar(Cd, Cl, xerr=dCd, yerr=dCl, color='c', marker='.', capsize=2, elinewidth=1, markeredgewidth=2)
    params = {'mathtext.default': 'regular'}
    plt.rcParams.update(params)
    plt.rcParams.update({'font.size': 12})
    plt.title('$C_{D}$ vs $C_{L}$')
    plt.xlabel('$C_{D}$')
    plt.ylabel('$C_{L}$')
    plt.legend(['Theoretical XFoil Data', 'UIUC Data','Experimental $C_{L}$ vs $C_{D}$'])
    plt.grid()
    plt.savefig('results\C_l-vs-C_d-graphs\C_l-C_d.png')
    plt.clf()

    print(" Saving C_d-C_dt.png..")
    plt.plot(xfoil_a, xfoil_cdp, color='r')
    plt.plot(xfoil_a, xfoil_cd, color='g')
    plt.errorbar(a, Cd, xerr=1, yerr=dCd, color='c', marker='.', capsize=2, elinewidth=1, markeredgewidth=2)
    plt.errorbar(a, Cdt, xerr=1, yerr=dCdt, color='m', marker='.', capsize=2, elinewidth=1, markeredgewidth=2)
    params = {'mathtext.default': 'regular'}
    plt.rcParams.update(params)
    plt.rcParams.update({'font.size': 12})
    plt.title('Pressire Drag ($C_{D}$) vs Total Drag ($C_{Dt}$)')
    plt.xlabel('$α$')
    plt.ylabel('$C_{D}$')
    plt.legend(['Theoretical XFoil $C_{D}$ Data', 'Theoretical XFoil $C_{Dt}$ Data' ,'Experimental $C_{D}$', 'Experimental $C_{Dt}$'])
    plt.grid()
    plt.savefig('results\C_d-vs-C_dt-graphs\C_d-C_dt.png')
    
