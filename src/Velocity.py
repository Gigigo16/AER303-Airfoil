import numpy as np

def Velocity(p_r1: np.array, p_r2: np.array, p_r1_err: np.array, p_r2_err: np.array):
    #, pos_r1: np.array, pos_r2: np.array
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
    v_r1: velocity distribution in config 1
    v_r2: velocity distribution in config 2
    V_pos: y-axis positions of the velocities
    '''

    rho = 1.225

    v_r1 = np.sqrt(2*p_r1/rho)
    v_r2 = np.sqrt(2*p_r2/rho)

    U_inf = np.average([v_r1[0], v_r1[-1], v_r2[0], v_r2[-1]])

    v_r1_err = 0.5*U_inf*p_r1_err/U_inf
    v_r2_err = 0.5*U_inf*p_r2_err/U_inf
    
    return U_inf, v_r1, v_r2, v_r1_err, v_r2_err