# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:36:35 2024

@author: Tomas Agustin Albanesi
"""

# Importación de libererias y modulos
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

# Importacion de datos de trazos
data=np.genfromtxt('Histeresis_CH1.csv',delimiter=',', skip_header=16)
data2=np.genfromtxt('Histeresis_CH2.csv',delimiter=',', skip_header=16)

R=10 #
t=data[0:,0]
V=data2[0:,1]  # tension de linea
I=data[0:,1]/R   # corriente
plt.figure(dpi=100)
ax1 = plt.gca()
# ax2 = ax1.twinx()  
# ax2.plot(t,V,"r",label="V")
ax1.plot(I,V,"g",label="I")
plt.legend(loc='upper right')

