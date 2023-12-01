def ReynoldsNumber(L: float, u: float=50, mu: float=1.825e-5, rho: float=1.29):
    '''
     Returns the Reynolds number for given parameters.

    Parameters:
    -----------   
    L : float
        charectaristic length (m)
    u : float, optional
        free stream velocity (m/s)
    mu u : float, optional 
        dynamic viscosity (kg/m*s)
    rho u : float, optional 
        desnity (kg/m^3)

    Returns:
    --------
    Re (float): Reynolds Number
    '''
    Re = rho*u*L/mu
    
    return Re