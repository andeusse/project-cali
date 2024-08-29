# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 10:52:31 2024

@author: Sergio
"""

import CoolingTower as CT

L = 0.56                    #Longitud de la torre en metros
A = 0.0225                  #Area transversal de la torre en metros
epsilon = 0.85              #Porosidad de la torre adimnesional
dp = 0.005                  #diametro de partícula de la torre
T_Lin = 41.4+273.15         #Temperatura de agua caliente en kelvin
P_atm = 90394.8             #Presion atmosferica en Pascales
Fv_Lin = 1.44/60/1000       #Flujo volumétrico de agua en m3/s
T_vin = 26.1+273.15           #Temperatura de aire a la entrada en kelvin
Fv_vin = 2.84/60            #Flujo volumétrico de aire en m3/s

Tower = CT.coolingTowerModel(L, A, epsilon, dp)

RH_air_in = 0.604  

Tower.towerBalance(T_Lin, P_atm, Fv_Lin, T_vin, Fv_vin, RH_air_in)
print("Flujo molar H20 líquida [mol/s] : "+str(Tower.solution[0]))
print("Flujo molar H20 en aire [mol/s] : "+str(Tower.solution[1]))
print("Flujo molar O2 en líquido [mol/s] : "+str(Tower.solution[2]))
print("Flujo molar O2 en aire [mol/s] : "+str(Tower.solution[3]))
print("Flujo molar N2 en líquido [mol/s] : "+str(Tower.solution[4]))
print("Flujo molar N2 en aire [mol/s] : "+str(Tower.solution[5]))
print("Temperatura de agua salida [K] : "+str(Tower.solution[6]))
print("Radio de humedad : ", Tower.w_v_out)
print("Humedad relativa del aire a la salida (%): ", Tower.RH_v_out)
print(Tower.solution)
