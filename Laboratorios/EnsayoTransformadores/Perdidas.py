# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:19:48 2024

@author: Tomas Agustin Albanesi
"""

# Importación de libererias y modulos
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

plt.close('all')

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

# Importacion de datos de trazos
data_Hist_I=np.genfromtxt('Histeresis_CH1.csv',delimiter=',', skip_header=16)
data_Hist_V=np.genfromtxt('Histeresis_CH2.csv',delimiter=',', skip_header=16)

tHist=data_Hist_V[0:,0]
VHist=data_Hist_V[0:,1]  # tension de linea
IHist=data_Hist_I[0:,1]/R   # corriente
plt.figure(dpi=100)
ax1 = plt.gca()
# ax2 = ax1.twinx()  
# ax2.plot(t,V,"r",label="V")
ax1.plot(IHist,VHist,"g",label="I")
plt.legend(loc='upper right')

plt.figure(dpi=100)  # si queres el grafico con otro tamaño, descometa la linea
plt.plot(tHist,IHist,tHist,VHist)
plt.grid()
plt.ylabel("tension [V]")
plt.xlabel("tiempo [s]")
plt.title('XY en T')
plt.legend(['canal 1 - proporcional a la corriente en el primario', 'canal 2 - tension sobre C'])

from scipy import signal

ch1 = signal.savgol_filter(IHist, 59, 4) # 59 = ventana ; 4 = grado de polinomio
plt.figure(dpi=100)
ch2 = signal.savgol_filter(VHist, 59, 4)
plt.plot(ch2)
plt.plot(ch1)

plt.figure(dpi=100)
plt.plot(ch1,ch2)
plt.grid()

R1 = 180.0   # 10ohms
C = 470e-9 # 1uF
R2 = 470e3 # 
N = 220/48 #

k=R2*C*N/R1
print(k)

# Busco los cruces por cero, de la señal de tensión para dividir los ciclos
def get_zeros_signal(signal_in, delta_min = 5):

  zero_cross = list()
  cross_slope = list()
  i_last = 0
  for i in range(1, signal_in.shape[0]):

    if (signal_in[i-1] <= 0) and (signal_in[i] > 0):
      if (i_last == 0) or ((i-i_last)>delta_min):
        zero_cross.append(i)
        cross_slope.append(1)
        i_last = i
    if (signal_in[i-1] >= 0) and (signal_in[i] < 0):
      if (i_last == 0) or ((i-i_last)>delta_min):
        zero_cross.append(i)
        cross_slope.append(-1)
        i_last = i

  return zero_cross, cross_slope

cruces_list, slopes_list = get_zeros_signal(ch2)

#plt.figure(dpi=150)
plt.plot(t,ch2)

for cruce, slope in zip(cruces_list, slopes_list):
  if slope > 0:
    plt.axvline(t[cruce], color='black', linestyle='-', linewidth='1.0')
  elif slope < 0:
    plt.axvline(t[cruce], color='red', linestyle='-', linewidth='1.0')


plt.grid()
plt.ylabel("tension [V]")
plt.xlabel("tiempo [s]")
plt.title('XY en T')

# Separo las señales en ciclos
limits_ciclos = list()
trigger_slope = slopes_list[0] # Primera pendiente
current_limits = np.zeros(2, dtype=np.int32)
current_limits[0] = cruces_list[0] # Primer cruce
for cruce, slope in zip(cruces_list, slopes_list):
  # Ignoro el primero
  if current_limits[0] == cruce:
    continue

  # Si la pendiente es igual a la inicial quiere decir que arrancó de nuevo
  if (trigger_slope == slope):
    # Agrego el final del ciclo
    current_limits[1] = cruce
    limits_ciclos.append(current_limits)
    # Donde termina una empiza el siguiente...
    current_limits = np.zeros(2, dtype=np.int32)
    current_limits[0] = cruce

print('Ciclos completos: %d'%len(limits_ciclos))

# Armo una lista de ciclos completos (divido al señal de entrada en ciclos)
ciclos_ch1_list = list()
ciclos_ch2_list = list()
for lim_ciclo in limits_ciclos:
  ciclos_ch1_list.append(np.copy(ch1[lim_ciclo[0]:lim_ciclo[1]]))
  ciclos_ch2_list.append(np.copy(ch2[lim_ciclo[0]:lim_ciclo[1]]))

# Los ploteo
#plt.figure(dpi=150)
for ch1_this, ch2_this in zip(ciclos_ch1_list, ciclos_ch2_list):
  plt.plot(ch1_this,ch2_this)

  plt.plot(ch1_this[0], ch2_this[0], '.', color=plt.gca().lines[-1].get_color(), markersize=12)
  plt.plot(ch1_this[-1], ch2_this[-1], '*', color=plt.gca().lines[-1].get_color(), markersize=12)

plt.grid()
plt.ylabel("tension canal 2  - B")
plt.xlabel("tension canal 1  - H")
plt.title('XY')

# Finalmente tenemos una lista de ciclos de histéresis completos. 
# Ahora debemos sacar el area que esta dentro de la curva. Esto lo podemos
# hacer integrando el area bajo la curva que pasa por arriba y restarle el 
# área que pasa por debajo. 
# Pero por suerte numpy nos facilita la vida!

areas_medidas = list()
for ch1_this, ch2_this in zip(ciclos_ch1_list, ciclos_ch2_list):

  # Integramos con la regla del trapezoide (https://en.wikipedia.org/wiki/Trapezoidal_rule)
  # Que es, en pocas palabras, sumar el area de los trapzoides formados entre cada par de puntos
  # y usando el delta_x (que puede ser positivo o negativo)

  # Antes de integrar repetimos el punto final, para cerrar el ciclo
  ch2_aux = np.zeros(len(ch2_this)+1)
  ch2_aux[:-1] = ch2_this
  ch2_aux[-1] = ch2_this[0]
  ch1_aux = np.zeros(len(ch1_this)+1)
  ch1_aux[:-1] = ch1_this
  ch1_aux[-1] = ch1_this[0]

  # Integramos con np.trapz y agregamos el area a la lista
  areas_medidas.append(np.abs(np.trapz(ch2_aux, x=ch1_aux)))

print('Perdidas por ciclo = %g J'%(k*np.mean(areas_medidas)))
print("La potencia perdida (W=J/s) =%g W"%(k*np.mean(areas_medidas)/0.02))