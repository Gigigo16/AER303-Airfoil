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
                          index=['Port 1', 
                                 'Port 2', 
                                 'Port 3',
                                 'Port 4', 
                                 'Port 5', 
                                 'Port 6', 
                                 'Port 7', 
                                 'Port 8', 
                                 'Port 9', 
                                 'Port 10', 
                                 'Port 11', 
                                 'Port 12', 
                                 'Port 13', 
                                 'Port 14', 
                                 'Port 15', 
                                 'Port 16', 
                                 'Port 17', 
                                 'Port 18',
                                 'Port 19'], columns=['Pressure (Pa)'])
        
        df.to_csv('.\data\CSV\Pressure_AoA%d.csv'%i, index=True)
    return 0
def RakePressuretoCSV(alpha: np.array, p_rake: np.array):
    print("eee")
