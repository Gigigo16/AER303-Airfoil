import numpy as np

def Velocity(p_r1: np.array, p_r2: np.array, p_r1_err: np.array, p_r2_err: np.array, pos_r1: np.array, pos_r2: np.array):
    '''
    Returns the Velocity Distribution over the rake and the free stream velocity.

    Parameters:
    -----------   
    p_r1 : np.array
        pressure from rake in config 1
    p_r2 : np.array
        pressure from rake in config 2
    p_r1_err : np.array
        error in pressure from rake in config 1
    p_r2_err : np.array
        error in pressure from rake in config 2
    pos_r1 : np.array
        positions of the pressure taps in config 1
    pos_r2 : np.array
        positions of the pressure taps in config 2

    Returns:
    --------    
    U_inf: Freestream Velocity
    U_inf_err: Freestream Velocity error
    V_r: velocity distribution in combined config
    V_r_err: velocity distribution error in combined config
    V_pos: y-axis positions of the velocities
    P_combined: combined pressure distribution
    P_combined_err: combined pressure distribution error
    '''
    rake_pos = np.array([0, 1.67, 3.33, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16.67, 18.33, 20])
    pos_r1 = pos_r1 + rake_pos
    pos_r2 = pos_r2 + rake_pos
    V_pos = np.sort(np.concatenate((pos_r1, pos_r2)))

    rho = 1.225

    v_r1 = np.sqrt(2*p_r1/rho)
    v_r2 = np.sqrt(2*p_r2/rho)

    #using the most stable and largest measurements points
    U_inf = np.average([v_r1[0][1], v_r1[0][-2], v_r2[0][1], v_r2[0][-2]]) 

    v_r1_err = 0.5*U_inf*p_r1_err/p_r1
    v_r2_err = 0.5*U_inf*p_r2_err/p_r2

    # it was found that one port in the rake was outputting abnormally high. interpolating over it:
    k = 14 #index of bad port 
    v_r1[0][k] = 0.5*(v_r1[0][k+1] + v_r1[0][k-1])
    v_r2[0][k] = 0.5*(v_r2[0][k+1] + v_r2[0][k-1])

    U_inf_err = 0.5*np.sqrt(np.sum(np.square([v_r1_err[0][1], v_r1_err[0][-2], v_r2_err[0][1], v_r2_err[0][-2]])))

    V_r = []
    P_combined = []
    P_combined_err = []
    V_r_err = []
    
    if pos_r1[0]<pos_r2[0]:
        for i in range(len(V_pos)):
            if i%2 == 0:
                P_combined.append(p_r1[0][int(i/2)])
                P_combined_err.append(p_r1_err[0][int(i/2)])
                V_r.append(v_r1[0][int(i/2)])
                V_r_err.append(v_r1_err[0][int(i/2)])
            else:
                V_r.append(v_r2[0][int((i-1)/2)])
                P_combined.append(p_r2[0][int((i-1)/2)])
                P_combined_err.append(p_r2_err[0][int((i-1)/2)])
                V_r_err.append(v_r2_err[0][int((i-1)/2)])
    else:
        for i in range(len(V_pos)):
            if i%2 == 0:
                V_r.append(v_r2[0][int(i/2)])
                P_combined.append(p_r2[0][int(i/2)])
                P_combined_err.append(p_r2_err[0][int(i/2)])
                V_r_err.append(v_r2_err[0][int(i/2)])
            else:
                V_r.append(v_r1[0][int((i-1)/2)])
                P_combined.append(p_r1[0][int((i-1)/2)])
                P_combined_err.append(p_r1_err[0][int((i-1)/2)])
                V_r_err.append(v_r1_err[0][int((i-1)/2)])

    return U_inf, U_inf_err, V_r, V_r_err, V_pos, v_r1, v_r2, pos_r1, pos_r2, P_combined, P_combined_err

def DynPressure(U_inf: np.float64, U_inf_err: np.float64):

    '''
    Returns the Dynamic pressure and error.

    Parameters:
    -----------   
    U_inf : np.float
        the freestream velocity
    U_inf_err : np.float
        the freestream velocity error

    Returns:
    --------    
    q_inf: Dynamic Pressure
    q_inf_err: Dynamic Pressure error
    '''

    rho = 1.225

    q_inf = 0.5*rho*(U_inf**2)

    q_inf_err = rho*U_inf*U_inf_err
    
    return q_inf, q_inf_err