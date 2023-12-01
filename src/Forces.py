from scipy import integrate
import pandas as pd
import numpy as np

def NormalForce(p_top: np.array, p_bot: np.array, top_p_pos: np.array, bot_p_pos: np.array):
    '''
    Returns the Normal force for pressure distribution.

    Parameters:
    -----------   
    p_top : np.array
        top airfoil pressure distribution
    p_bot : np.array
        bottom airfoil pressure distribution
    top_p_pos : list
        top airfoil pressure tap positions
    bot_p_pos : list
        bottom airfoil pressure tap positions

    Returns:
    --------
    N: Normal Force
    dN: Normal Force uncertainty
    '''
    x_upper = top_p_pos[:, 0]
    x_lower = bot_p_pos[:, 0]
    y_upper = top_p_pos[:, 1]
    y_lower = bot_p_pos[:, 1]
    
    theta_upper= np.arctan(np.diff(y_upper)/np.diff(x_upper))
    theta_lower= np.arctan(np.diff(y_lower)/np.diff(x_lower))
    
    ds_upper = np.sqrt(np.diff(x_upper)**2 + np.diff(y_upper)**2)
    ds_lower = np.sqrt(np.diff(x_lower)**2 + np.diff(y_lower)**2)
    
    # Trapezoidal numerical integration
    for i in range(len(ds_upper)):
        N += -0.5 * (p_top[i] + p_top[i+1]) * np.cos(theta_upper[i]) * ds_upper[i]
    
    for i in range(len(ds_lower)):
        N += 0.5 * (p_bot[i] + p_bot[i+1]) * np.cos(theta_lower[i]) * ds_lower[i]
    
    
    dN = 0 #TODO
    
    
    return N, dN