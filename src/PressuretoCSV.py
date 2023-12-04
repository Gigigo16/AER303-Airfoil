import numpy as np

def PressuretoCSV(alpha: np.array, p: np.array):
    array = [[9999]]
    for i in range(0,19):
        array[0].append(np.float32(i+1))
    
    j = 0
    for i in alpha:
        a = [i]
        array.append(np.concatenate([a, p[j]],  axis=None))
        j += 1
    
    array = np.array(array)
    np.savetxt("./data/CSV/Pressure.csv", array, delimiter=';', fmt='%.18e')
