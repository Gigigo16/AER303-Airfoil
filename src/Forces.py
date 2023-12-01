from scipy import integrate
import pandas as pd
import numpy as np
import math

def NormalForce(p_top: np.array, p_bot: np.array, top_p_pos: list, bot_p_pos: list, airfoil: np.array):
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
    for i in range(1,len(top_p_pos)):
        math.acos()

    integrate.trapezoid()
