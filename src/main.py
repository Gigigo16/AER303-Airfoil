# main file for running all data processing and plotting

#imports: 

import scipy.io
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# airfoil tap positions: 
air_top_tap_pos = [0, 0.03, 0.06, 0.10, 0.15, 0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00]
air_bot_tap_pos = [0.90, 0.60, 0.40, 0.30, 0.20, 0.10, 0.05]

mat = scipy.io.loadmat("data\Filtered\F-Experimental_data_0.mat")

a = mat['p_airfoil'][0][0:len(air_top_tap_pos)]
b = mat['p_airfoil'][0][0:len(air_bot_tap_pos)]

plt.plot(air_top_tap_pos, a)
plt.plot(air_bot_tap_pos, b)
plt.show()