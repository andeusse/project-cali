# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 10:52:31 2024

@author: Sergio
"""

import CoolingTower as CT


L = 1                       #Longitud de la torre en metros
D = 0.2                     #diametros de la torre en metros
epsilon = 0.4               #Porosidad de la torre adimnesional
dp = 0.005                  #diametro de partícula de la torre
Tower = CT.coolingtower(L, D, epsilon, dp)
T_Lin = 40+273.15           #Temperatura de agua caliente en kelvin
P_atm = 101325              #Presion atmosferica en Pascales
Fv_Lin = 1.05/60/1000       #Flujo volumétrico de agua en m3/s
T_vin = 30+273.15           #Temperatura de aire a la entrada en kelvin
Fv_vin = 2.04/60            #Flujo volumétrico de aire en m3/s
RH_air_in = 1    


Tower.TowerBalance(T_Lin, P_atm, Fv_Lin, T_vin, Fv_vin, RH_air_in)
print(Tower.solution)

