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
    n: Normal Force
    dn: Normal Force uncertainty
    '''
    x_upper = [row[0] for row in top_p_pos]
    x_lower = [row[0] for row in bot_p_pos]
    y_upper = [row[1] for row in top_p_pos]
    y_lower = [row[1] for row in bot_p_pos]

    theta_upper= np.arctan(np.diff(y_upper)/np.diff(x_upper))
    theta_lower= np.arctan(np.diff(y_lower)/np.diff(x_lower))
    
    ds_upper = np.sqrt(np.diff(x_upper)**2 + np.diff(y_upper)**2)
    ds_lower = np.sqrt(np.diff(x_lower)**2 + np.diff(y_lower)**2)
    
    n = 0
    dn = 0
    # Trapezoidal numerical integration
    for i in range(len(ds_upper)):
        n += -0.5 * (p_top[i] + p_top[i+1]) * np.cos(theta_upper[i]) * ds_upper[i]
        dn += (-0.5*p_err_top[i]*np.cos(theta_upper[i])*ds_upper[i])**2 + (-0.5*p_err_top[i+1]*np.cos(theta_upper[i])*ds_upper[i])**2
    
    for i in range(len(ds_lower)):
        n += 0.5 * (p_bot[i] + p_bot[i+1]) * np.cos(theta_lower[i]) * ds_lower[i]
        dn += (0.5*p_err_bot[i]*np.cos(theta_lower[i])*ds_lower[i])**2 + (0.5*p_err_bot[i+1]*np.cos(theta_lower[i])*ds_lower[i])**2
    
    # Calculating error (position error assumed to be 0)
    dn = np.sqrt(dn)
    
    return n, dn

def AxialForce(p_top: np.array, p_bot: np.array, p_err_top: np.array, p_err_bot: np.array, top_p_pos: np.array, bot_p_pos: np.array):
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
    a: Axial Force
    da: Axial Force uncertainty
    '''
    x_upper = [row[0] for row in top_p_pos]
    x_lower = [row[0] for row in bot_p_pos]
    y_upper = [row[1] for row in top_p_pos]
    y_lower = [row[1] for row in bot_p_pos]
    
    theta_upper= np.arctan(np.diff(y_upper)/np.diff(x_upper))
    theta_lower= np.arctan(np.diff(y_lower)/np.diff(x_lower))
    
    ds_upper = np.sqrt(np.diff(x_upper)**2 + np.diff(y_upper)**2)
    ds_lower = np.sqrt(np.diff(x_lower)**2 + np.diff(y_lower)**2)
    
    a = 0
    da = 0

    # Trapezoidal numerical integration
    for i in range(len(ds_upper)):
        a += -0.5 * (p_top[i] + p_top[i+1]) * np.sin(theta_upper[i]) * ds_upper[i]
        da += (-0.5*p_err_top[i]*np.sin(theta_upper[i])*ds_upper[i])**2 + (-0.5*p_err_top[i+1]*np.sin(theta_upper[i])*ds_upper[i])**2
    
    for i in range(len(ds_lower)):
        a += 0.5 * (p_bot[i] + p_bot[i+1]) * np.sin(theta_lower[i]) * ds_lower[i]
        da += (0.5*p_err_bot[i]*np.sin(theta_lower[i])*ds_lower[i])**2 + (0.5*p_err_bot[i+1]*np.sin(theta_lower[i])*ds_lower[i])**2
    
    # Calculating error (position error assumed to be 0)
    da = np.sqrt(da)
    
    return a, da

def LiftForce(alpha: float, dalpha: float, n: float, dn: float, a: float, da: float):
    '''
    Returns the Lift force for given normal and axial forces at given AoA.

    Parameters:
    -----------   
    alpha : float
        angle of attack (degrees)
    dalpha : float
        angle of attack uncertainty (degrees)
    n : float
        Normal force (Newtons)
    dn : float
        Normal force uncertainty (Newtons)
    a : float
        Axial force (Newtons)
    da : float
        Axial force uncertainty (Newtons)
    Returns:
    --------
    l: Lift Force
    dl: Lift Force uncertainty
    '''

    l = n * np.cos(np.deg2rad(alpha)) - a * np.sin(np.deg2rad(alpha))
    dl =  np.sqrt((np.cos(np.deg2rad(alpha)) * dn)**2 + (np.sin(np.deg2rad(alpha)) * da)**2 + ((-n*np.sin(np.deg2rad(alpha)) - a*np.cos(np.deg2rad(alpha)))*np.deg2rad(dalpha))**2)

    return l, dl

def PressureDragForce(alpha: float, dalpha: float, n: float, dn: float, a: float, da: float):
    '''
    Returns the Pressure drag force for given normal and axial forces at given AoA.

    Parameters:
    -----------   
    alpha : float
        angle of attack (degrees)
    dalpha : float
        angle of attack uncertainty (degrees)
    n : float
        Normal force (Newtons)
    dn : float
        Normal force uncertainty (Newtons)
    a : float
        Axial force (Newtons)
    da : float
        Axial force uncertainty (Newtons)
    Returns:
    --------
    dp: Pressure Drag Force
    ddp: Pressure Drag Force uncertainty
    '''

    dp = n * np.sin(np.deg2rad(alpha)) + a * np.cos(np.deg2rad(alpha))
    ddp =  np.sqrt((np.sin(np.deg2rad(alpha)) * dn)**2 + (np.cos(np.deg2rad(alpha)) * da)**2 + ((n*np.cos(np.deg2rad(alpha)) - a*np.sin(np.deg2rad(alpha)))*np.deg2rad(alpha))**2)

    return dp, ddp

def MomentLE(p_top: np.array, p_bot: np.array, p_err_top: np.array, p_err_bot: np.array, top_p_pos: np.array, bot_p_pos: np.array):
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
    m: Moment 
    dm: Moment uncertainty
    '''
    x_upper = [row[0] for row in top_p_pos]
    x_lower = [row[0] for row in bot_p_pos]
    y_upper = [row[1] for row in top_p_pos]
    y_lower = [row[1] for row in bot_p_pos]
    
    theta_upper= np.arctan(np.diff(y_upper)/np.diff(x_upper))
    theta_lower= np.arctan(np.diff(y_lower)/np.diff(x_lower))
    
    ds_upper = np.sqrt(np.diff(x_upper)**2 + np.diff(y_upper)**2)
    ds_lower = np.sqrt(np.diff(x_lower)**2 + np.diff(y_lower)**2)   

    m = 0
    dm = 0

    for i in range(len(ds_upper)):
        m += 0.5*(p_top[i] + p_top[i+1])*np.cos(theta_upper[i])*x_upper[i]*ds_upper[i]
        m += -0.5*(p_top[i] + p_top[i+1])*np.sin(theta_upper[i])*y_upper[i]*ds_upper[i]

        dm += (0.5*np.cos(theta_upper[i])*x_upper[i]*ds_upper[i]-0.5*np.sin(theta_upper[i])*y_upper[i]*ds_upper[i]*p_err_top[i])**2

    for i in range(len(ds_lower)):
        m += 0.5*(p_bot[i] + p_bot[i+1])*np.cos(theta_lower[i])*x_lower[i]*ds_lower[i]
        m += 0.5*(p_bot[i] + p_bot[i+1])*np.sin(theta_lower[i])*y_lower[i]*ds_lower[i]

        dm += (0.5*np.cos(theta_lower[i])*x_lower[i]*ds_lower[i]+0.5*np.sin(theta_lower[i])*y_lower[i]*ds_lower[i]*p_err_bot[i])**2
    
    dm = np.sqrt(dm)
    return m, dm

def TotalDrag(y: np.array, v:np.array, v_err: np.array, u_inf: float, u_inf_err: float, rho: float=1.29):
    '''
    Returns the total drag force as a result of momentum loss of air.

    Parameters:
    -----------   
    y : np.array
        y position of measurement points (m)
    v : float
        air velocity at measurement points (m/s)
    v_err : float
        air velocity uncertainty (m/s)
    u_inf : float
        free stream air velocity (m/s)
    u_inf_err : float
        free stream air velocity uncertainty (m/s)
    rho : float
        air density (kg/m^3)

    Returns:
    --------
    dt: total drag
    ddt: total drag uncertainty
    '''
    dt = 0
    ddt = 0
    delta_y = np.diff(y)
    for i in range(len(y)-1):
        dt += rho * 0.5 * ((v[i]*(u_inf-v[i]))+(v[i+1]*(u_inf-v[i+1])))*delta_y[i]
        ddt += (rho*0.5*delta_y[i]*(u_inf-2*v[i])*v_err[i])**2 + (rho*0.5*delta_y[i]*(v[i+1]+v[i])*u_inf_err)**2

    ddt = np.sqrt(ddt)
    return dt, ddt