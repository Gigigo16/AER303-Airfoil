import numpy as np

def NormalForce(p_top: np.array, p_bot: np.array, p_err_top: np.array, p_err_bot: np.array, top_p_pos: np.array, bot_p_pos: np.array):
    '''
    Returns the Normal force for pressure distribution.

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
        dN += (-0.5*p_err_top[i]*np.cos(theta_upper)*ds_upper[i])**2 + (-0.5*p_err_top[i+1]*np.cos(theta_upper[i])*ds_upper[i])**2
    
    for i in range(len(ds_lower)):
        N += 0.5 * (p_bot[i] + p_bot[i+1]) * np.cos(theta_lower[i]) * ds_lower[i]
        dN += (0.5*p_err_bot[i]*np.cos(theta_lower)*ds_lower[i])**2 + (0.5*p_err_bot[i+1]*np.cos(theta_lower[i])*ds_lower[i])**2
    
    # Calculating error (position error assumed to be 0)
    dN = np.sqrt(dN)
    
    return N, dN

def AxialForce(p_top: np.array, p_bot: np.array, p_err_bot: np.array, p_err_top: np.array, top_p_pos: np.array, bot_p_pos: np.array):
    '''
    Returns the Axial force for pressure distribution.

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
    A: Axial Force
    dN: Axial Force uncertainty
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
        A += -0.5 * (p_top[i] + p_top[i+1]) * np.sin(theta_upper[i]) * ds_upper[i]
        dA += (-0.5*p_err_top[i]*np.sin(theta_upper)*ds_upper[i])**2 + (-0.5*p_err_top[i+1]*np.sin(theta_upper[i])*ds_upper[i])**2
    
    for i in range(len(ds_lower)):
        N += 0.5 * (p_bot[i] + p_bot[i+1]) * np.sin(theta_lower[i]) * ds_lower[i]
        dA += (0.5*p_err_bot[i]*np.sin(theta_lower)*ds_lower[i])**2 + (0.5*p_err_bot[i+1]*np.sin(theta_lower[i])*ds_lower[i])**2
    
    # Calculating error (position error assumed to be 0)
    dN = np.sqrt(dN)
    
    return A, dA

def LiftForce(alpha: float, dalpha: float, N: float, dN: float, A: float, dA: float):
    '''
    Returns the Lift force for given normal and axial forces at given AoA.

    Parameters:
    -----------   
    alpha : float
        angle of attack (degrees)
    dalpha : float
        angle of attack uncertainty (degrees)
    N : float
        Normal force (Newtons)
    dN : float
        Normal force uncertainty (Newtons)
    A : float
        Axial force (Newtons)
    dA : float
        Axial force uncertainty (Newtons)
    Returns:
    --------
    L: Lift Force
    dL: Lift Force uncertainty
    '''

    L = N * np.cos(np.deg2rad(alpha)) - A * np.sin(np.deg2rad(alpha))
    dL =  np.sqrt((np.cos(np.deg2rad(alpha)) * dN)**2 + (np.sin(np.deg2rad(alpha)) * dA)**2 + ((-N*np.sin(np.deg2rad(alpha)) - A*np.cos(np.deg2rad(alpha)))*np.deg2rad(alpha))**2)

    return L, dL

def PressureDragForce(alpha: float, dalpha: float, N: float, dN: float, A: float, dA: float):
    '''
    Returns the Pressure drag force for given normal and axial forces at given AoA.

    Parameters:
    -----------   
    alpha : float
        angle of attack (degrees)
    dalpha : float
        angle of attack uncertainty (degrees)
    N : float
        Normal force (Newtons)
    dN : float
        Normal force uncertainty (Newtons)
    A : float
        Axial force (Newtons)
    dA : float
        Axial force uncertainty (Newtons)
    Returns:
    --------
    Dp: Pressure Drag Force
    dDp: Pressure Drag Force uncertainty
    '''

    Dp = N * np.sin(np.deg2rad(alpha)) + A * np.cos(np.deg2rad(alpha))
    dDp =  np.sqrt((np.sin(np.deg2rad(alpha)) * dN)**2 + (np.cos(np.deg2rad(alpha)) * dA)**2 + ((N*np.cos(np.deg2rad(alpha)) - A*np.sin(np.deg2rad(alpha)))*np.deg2rad(alpha))**2)

    return Dp, dDp

def MomentLE(p_top: np.array, p_bot: np.array, p_err_bot: np.array, p_err_top: np.array, top_p_pos: np.array, bot_p_pos: np.array):
    '''
    Returns the Moment about the leading edge 
    acting on the airfoil for given pressure distribution.

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
    M: Moment 
    dM: Moment uncertainty
    '''
    x_upper = top_p_pos[:, 0]
    x_lower = bot_p_pos[:, 0]
    y_upper = top_p_pos[:, 1]
    y_lower = bot_p_pos[:, 1]
    
    theta_upper= np.arctan(np.diff(y_upper)/np.diff(x_upper))
    theta_lower= np.arctan(np.diff(y_lower)/np.diff(x_lower))
    
    ds_upper = np.sqrt(np.diff(x_upper)**2 + np.diff(y_upper)**2)
    ds_lower = np.sqrt(np.diff(x_lower)**2 + np.diff(y_lower)**2)   

    for i in range(len(ds_upper)):
        M += 0.5*(p_top[i] + p_top[i+1])*np.cos(theta_upper[i])*x_upper[i]*ds_upper[i]
        M += -0.5*(p_top[i] + p_top[i+1])*np.sin(theta_upper[i])*y_upper[i]*ds_upper[i]

        dM += (0.5*np.cos(theta_upper[i])*x_upper[i]*ds_upper[i]-0.5*np.sin(theta_upper[i])*y_upper[i]*ds_upper[i])**2

    for i in range(len(ds_lower)):
        M += 0.5*(p_bot[i] + p_bot[i+1])*np.cos(theta_lower[i])*x_lower[i]*ds_lower[i]
        M += -0.5*(p_bot[i] + p_bot[i+1])*np.sin(theta_lower[i])*y_lower[i]*ds_lower[i]

        dM += (0.5*np.cos(theta_lower[i])*x_lower[i]*ds_lower[i]-0.5*np.sin(theta_lower[i])*y_lower[i]*ds_lower[i])**2
    
    dM = np.sqrt(dM)
    return M, dM
