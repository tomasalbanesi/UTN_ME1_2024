# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:53:03 2024

@author: Tomas Agustin Albanesi
"""

# Importación de libererias y modulos
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

# Importacion de datos de trazos
dataI=np.genfromtxt('Potencias_CH1.csv',delimiter=',', skip_header=16)
dataV=np.genfromtxt('Potencias_CH2.csv',delimiter=',', skip_header=16)

R=180 #
t=dataV[0:,0]
V=dataV[0:,1]  # tension de linea
I=dataI[0:,1]/R   # corriente
plt.figure(dpi=100)
ax1 = plt.gca()
ax2 = ax1.twinx()  
ax2.plot(t,V,"r",label="V")
ax1.plot(t,I,"g",label="I")
plt.legend(loc='upper right')

p=V*I # la potencia instantanea como el producto de la tension y la corriente en el primario
#pr=np.mean(10*I**2)  # potencia disipada por la resistencia
irms=np.sqrt(np.mean(I**2))
pr=(irms**2)*R
pactiva=np.mean(p)-pr  # potencia activa disipada por el transformador en vacio

print("potencia en la R= {} W".format(pr))
print("La perdida de potencia por el hierro= {} W".format(pactiva))

p_line=np.ones(len(p))*pactiva
plt.figure(dpi=100)
plt.plot(t,p,label="potencia instantanea")
plt.plot(t,p_line,label="potencia activa")
plt.legend(loc='upper right')
plt.title("Potencia instantanea")
plt.xlabel("s")
plt.ylabel("W")

print(np.mean(p))

