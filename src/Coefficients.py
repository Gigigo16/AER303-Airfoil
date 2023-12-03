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

def Coefficients(L: np.array, L_err: np.array, D: np.array, D_err: np.array, M: np.array, M_err: np.array, q_inf: np.array, q_inf_err: np.array, c: float):
    """
    Return the lift, drag, and moment coefficients.

    Parameters
    ----------
    L : np.array
        Array containg lift force for each AoA in Newtons.
    L_err : np.array
        Array containg lift force uncertainty for each AoA in Newtons.
    D : np.array
        Array containg drag force for each AoA in Newtons.
    D_err : np.array
        Array containg drag force uncertainty for each AoA in Newtons.
    M : np.array
        Array containg moment for each AoA in Newtons.
    M_err : np.array
        Array containg moment uncertainty for each AoA in Newtons.
    q_inf : np.array
        Array containing the dynamic pressure at a given AoA.
    q_inf_err : np.array
        Array containing the dynamic pressure uncertainty at a given AoA.
    c : float
        chord length in meters
        
    Returns
    -------
    cl : np.array
    dcl : np.array
    cd : np.array
    dcd : np.array
    cm : np.array
    dcm : np.array
    """

    cl = L / (q_inf*c)
    cd = D / (q_inf*c)
    cm = M / (q_inf*c**2)

    dcl = np.sqrt((L_err/(q_inf*c))**2+(q_inf_err*L/(q_inf**2*c))**2)
    dcd = np.sqrt((D_err/(q_inf*c))**2+(q_inf_err*D/(q_inf**2*c))**2)
    dcm = np.sqrt((M_err/(q_inf*c**2))**2+(q_inf_err*M/(q_inf**2*c**2))**2)

    return cl, dcl, cd, dcd, cm, dcm

def Ctotaldrag(Dt: np.array, Dt_err: np.array, q_inf: np.array, q_inf_err: np.array, c: float):
    """
    returns total drag. (note can also be used for pressure drag)

    Parameters
    ----------
    Dt : np.array
        Array containg total drag force for each AoA in Newtons.
    Dt_err : np.array
        Array containg total drag force uncertainty for each AoA in Newtons.
    q_inf : np.array
        Array containing the dynamic pressure at a given AoA.
    q_inf_err : np.array
        Array containing the dynamic pressure uncertainty at a given AoA.
    c : float
        chord length in meters

    Returns
    -------
    cdt : np.array
    dcdt : np.array
    """
    cdt = Dt / (q_inf*c)
    dcdt = np.sqrt((Dt_err/(q_inf*c))**2+(q_inf_err*Dt/(q_inf**2*c))**2)

    return cdt, dcdt

    