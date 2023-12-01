import numpy as np

def Cp(p_top: np.array, p_bot: np.array, p_err_bot: np.array, p_err_top: np.array, top_p_pos: np.array, bot_p_pos: np.array):
    '''
    Returns the Coefficient of pressure distribution.

    Parameters:
    -----------   
    p_top : np.array
        top airfoil pressure distribution
    p_bot : np.array
        bottom airfoil pressure distribution
    p_err_top : np.array
        top airfoil perssure error
    p_err_bot : np.array
        bottom airfoil perssure error
    top_p_pos : list
        top airfoil pressure tap positions [x; y]
    bot_p_pos : list
        bottom airfoil pressure tap positions [x; y]

    Returns:
    --------
    N: Normal Force
    dN: Normal Force uncertainty
    '''
    