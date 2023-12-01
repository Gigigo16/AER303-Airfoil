import numpy as np

def Cpressure(p_top: np.array, p_bot: np.array, p_top_err: np.array, p_bot_err: np.array, q_inf: np.float64, q_inf_err: np.float64):
    '''
    Returns the Coefficient of pressure distribution.

    Parameters:
    -----------   
    p_top : np.array
        top airfoil pressure distribution
    p_bot : np.array
        bottom airfoil pressure distribution
    p_top_err : np.array
        top airfoil perssure error
    p_bot_err : np.array
        bottom airfoil perssure error
    q_inf : np.float64
        Dynamic Pressure
    q_inf_err : np.float64
        Dynamic Pressure error

    Returns:
    --------
    Cp_top: Coefficient of pressure top
    Cp_top_err: Coefficient of pressure top error
    Cp_bot: Coefficient of pressure bottom
    Cp_bot_err: Coefficient of pressure bottom error
    '''

    Cp_top = p_top/q_inf
    Cp_bot = p_bot/q_inf

    Cp_top_err = Cp_top * (np.sqrt((np.square((p_top_err/p_top)) + np.square((q_inf_err/q_inf)))))
    Cp_bot_err = Cp_bot * (np.sqrt((np.square((p_bot_err/p_bot)) + np.square((q_inf_err/q_inf)))))

    # it was found that one port in the airfoil was outputting abnormally high. interpolating over it:
    k = 5 #index of bad port 
    Cp_top[k] = 0.5*(Cp_top[k+1] + Cp_top[k-1])

    return Cp_top, Cp_bot, Cp_top_err, Cp_bot_err

    