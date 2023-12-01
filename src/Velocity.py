import numpy as np

def Velocity(p_r1: np.array, p_r2: np.array):
    #, p_r1_err: np.array, p_r2_err: np.array, pos_r1: np.array, pos_r2: np.array
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
    V: velocity distribution
    V_pos: y-axis positions of the velocities
    U_inf: Freestream Velocity
    '''

    rho = 1.225

    v_r1 = np.sqrt(2*p_r1/rho)
    v_r2 = np.sqrt(2*p_r2/rho)
    
    return v_r1, v_r2