# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 14:31:38 2024

@author: Tomas Agustin Albanesi
"""

# Importación de librerias y módulos
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy import signal

# Valores medidos
tensiones = [5.007, 4.994, 5.005, 4.99, 4.999] # Mediciones de tension
error = 2 # En porcentaje

# Muestro las tensiones medidas
for tension in tensiones:
    print(tension)
    
# Calculo la media de los valores medidos
tensiones = np.array(tensiones) # Convierto la lista tensiones en array de NumPy
tension_media = tensiones.mean()
print("La tensión media es: " + str(tension_media) + " V")

# Calculo el desvio estandar
tension_std = tensiones.std()
print("El desvio estándar de la tensión es: " + str(tension_std) + " V")

# Incertidumbre Tipo A
tension_ui = tension_std / np.sqrt(tensiones.size)
print("La Incertidumbre Tipo A es: " + str(tension_ui) + " V")

# Incertidumbre Tipo B
tension_uj = ((error/100.0)/np.sqrt(3))*tension_media
print("La Incertidumbre Tipo B es: " + str(tension_uj) + " V")

# Incertidumbre Combinada
tension_uc = np.sqrt(tension_ui**2 + tension_uj**2)
print("La Incertidumbre Combinada es: " + str(tension_uc) + " V")

# uc es muy similar a uj --> domina incertidumbre tipo B (NO es gaussiana)
