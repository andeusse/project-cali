# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 10:52:31 2024

@author: Sergio
"""
import CoolingTower as CT

L = 1                       #Longitud de la torre en metros
A = 0.0225                    #Area transversal de la torre en metros
epsilon = 0.4               #Porosidad de la torre adimnesional
dp = 0.005                  #diametro de partícula de la torre
T_Lin = 50+273.15           #Temperatura de agua caliente en kelvin
P_atm = 101325              #Presion atmosferica en Pascales
Fv_Lin = 1.05/60/1000       #Flujo volumétrico de agua en m3/s
T_vin = 20+273.15           #Temperatura de aire a la entrada en kelvin
Fv_vin = 3.04/60            #Flujo volumétrico de aire en m3/s

Tower = CT.coolingTowerModel(L, A, epsilon, dp)

RH_air_in = 80    

Tower.towerBalance(T_Lin, P_atm, Fv_Lin, T_vin, Fv_vin, RH_air_in)
print("Flujo molar H20 líquida [mol/s] : "+str(Tower.solution[0]))
print("Flujo molar H20 en aire [mol/s] : "+str(Tower.solution[1]))
print("Flujo molar O2 en líquido [mol/s] : "+str(Tower.solution[2]))
print("Flujo molar O2 en aire [mol/s] : "+str(Tower.solution[3]))
print("Flujo molar N2 en líquido [mol/s] : "+str(Tower.solution[4]))
print("Flujo molar N2 en aire [mol/s] : "+str(Tower.solution[5]))
print("Temperatura de agua salida [K] : "+str(Tower.solution[6]))