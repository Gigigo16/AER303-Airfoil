import numpy as np
import pandas as pd

def PressuretoCSV(alpha: np.array, p: np.array):
    """
    exports given pressure data to CSV files for each AoA

    Parameters
    ----------
    alpha : np.array
        array containing AoA values
    p : np.array (2D)
        array containing pressure data for each AoA where each row 
        is a different AoA and each column is a different port
    
    Returns
    -------
    0
    """
    for i in range(len(alpha)):
        df = pd.DataFrame(p[i].T, 
                          index=['1', 
                                 '2', 
                                 '3',
                                 '4', 
                                 '5', 
                                 '6', 
                                 '7', 
                                 '8', 
                                 '9', 
                                 '10', 
                                 '11', 
                                 '12', 
                                 '13', 
                                 '14', 
                                 '15', 
                                 '16', 
                                 '17', 
                                 '18',
                                 '19'], columns=['Pressure (Pa)'])
        df.index.name = 'Port #'
        
        df.to_csv('.\data\CSV\Pressure_AoA%d.csv'%alpha[i], index=True)
    return 0

def RakePressuretoCSV(alpha: np.array, p_rake: np.array , y: np.array):
    """
    exports given rake pressure data to CSV files for each AoA

    Parameters
    ----------
    alpha : np.array
        array containing AoA values
    p_rake : np.array (2D)
        array containing rake pressure data for each AoA where each row 
        is a different AoA and each column is a different port
    y : np.array (cm)
        array containing rake port positions with same structure as p_rake
    Returns
    -------
    0
    """
    for i in range(len(alpha)):
        df = pd.DataFrame(p_rake[i].T, 
                          index=y[i].T, columns=['Pressure (Pa)'])
        df.index.name = 'y Position (cm)'
        
        df.to_csv('.\data\CSV\Rake_Pressure_AoA%d.csv'%alpha[i], index=True)

def RakeUncertaintytoCSV(alpha: np.array, dp_rake: np.array , y: np.array):
    """
    exports given rake pressure uncertainty data to CSV files for each AoA

    Parameters
    ----------
    alpha : np.array
        array containing AoA values
    dp_rake : np.array (2D)
        array containing rake pressure uncertainty data for each AoA where each row 
        is a different AoA and each column is a different port
    y : np.array (cm)
        array containing rake port positions with same structure as dp_rake
    Returns
    -------
    0
    """
    for i in range(len(alpha)):
        df = pd.DataFrame(dp_rake[i].T, 
                          index=y[i].T, columns=['Pressure Uncertainty (Pa)'])
        df.index.name = 'y Position (cm)'
        
        df.to_csv('.\data\CSV\Rake_Pressure_Uncertainty_AoA%d.csv'%alpha[i], index=True)