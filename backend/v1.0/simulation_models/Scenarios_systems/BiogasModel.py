# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 11:03:11 2023

@author: Sergio
"""
import numpy as np
import ThermoProperties as Thermo
from scipy.integrate import odeint
import pandas as pd
import importlib


class biogas_model:
    # iniciamos la planta de biogás con los parámetros constructivos y el tiempo de simulación
    def __init__(self, tp=1.0, dias=30, V1=30, V2=70, L_H1=2, L_H2=2, U1=0.05, U2=0.05, name = "Biogas"):
        self.tp = tp  # Tamano de paso en horas, ejemplo 0.1 horas = 6 minutos
        self.dias = dias  # dias simulados ejemplo = 30 dias
        self.V1 = V1  # Volumen del reactor de la etapa 1 en litros
        self.V2 = V2  # Volumen del reactor de la etapa 2 en litros
        self.L_H1 = L_H1  # Relacion altura diametros del reactor 1
        self.L_H2 = L_H2  # Relacion altura diametro del reactor 2
        self.U1 = U1  # Coeficiente global de transferencia de calor Reactor 1
        self.U2 = U2  # Coeficiente global de transferencia de calor Reactor 2
        self.name = name # Nombre del sistema      

        #return self.tp, self.dias, self.V1, self.V2, self.L_H1, self.L_H2,  self.U1, self.U2

    # Parametros del controlador de temperatura
    def TemperatureControlParameters(self, Tset1=35, tolerancia1=3, Tset2=35, tolerancia2=3):
        self.Tset1 = Tset1  # Set-Point de temperatura reactor 1 (°c)
        # tolerancia del controlador On-Off de Temperatura del R1
        self.tolerancia1 = tolerancia1
        self.Tset2 = Tset2  # Set-Point de temperatura reactor 2 (°c)
        # tolernacia del controlador On-Off de Temperatura del R2
        self.tolerancia2 = tolerancia2

        #return self.Tset1, self.tolerancia1, self.Tset2, self.tolerancia2

    # Parametros de la corriente del sustrato
    def SubstrateProperties(self, Cci=0.4, Chi=0.05, Coi=0.2, Csi=0.01, ST=0.1, rho_sus=998, Tin_sus=20, Pin_sus=350, vin_sus=0.139, DeltaP=5):
        # Concentracion de carbono atomico en el sustrato en base seca (%)
        self.Cci = Cci
        # Concentracion de hidrogeno atomico en el sustrato en base seca (%)
        self.Chi = Chi
        # Concentracion de oxigeno atomico en el sustrato en base seca (%)
        self.Coi = Coi
        # Concentracion de azufre o sulfuro atomico en el sustrato en base seca (%)
        self.Csi = Csi
        # Estimaciin de la concentracion de nitrogeno atomico a partir de balance masico (%)
        self.Cni = 1-self.Cci-self.Chi-self.Coi-self.Csi
        self.ST = ST  # Concentracion de solidos totales en el sustrato (%)
        self.rho_sus = rho_sus  # Densidad del sustrato (gramos/Litro)
        # Temperatura de entrada del sustrato al sistema (°c)
        self.Tin_sus = Tin_sus
        # Presion de entrada del sustrato al sistema (kPa)
        self.Pin_sus = Pin_sus
        # Caida de presión del sustrato en el reactor 1 (kPa)
        self.DeltaP = DeltaP
        self.vin_sus = vin_sus  # Flujo volumetrico de sustrato (Litros/hora)

        #return self.Cci, self.Chi, self.Coi, self.Csi, self.Cni, self.ST, self.rho_sus, self.Tin_sus, self.Pin_sus, self.vin_sus, self.DeltaP

    # Parametros cineticos de las reacciones de descomposicion
    def KineticsParameters(self, k_c=0.05, k_h=0.01, k_o=0.01, k_s=0.001, k_n=0.001, k_ch4=0.015, k_co2=0.035, k_h2s=0.002, k_nh3=0.002, Ea_c=100000, Ea_h=100000, Ea_o=20000, Ea_s=200000, Ea_n=200000, Ea_ch4=500, Ea_co2=100, Ea_h2s=1500, Ea_nh3=1000):
        # Constantes cineticas
        self.k_c_new = k_c/24  # Constante cinetica para el gasto de carbono (L/h)
        # constante cinetica para el gasto de hidrogeno (L/h)
        self.k_h_new = k_h/24
        self.k_o_new = k_o/24  # constante cinetica para el gasto de oxigeno (L/h)
        self.k_s_new = k_s/24  # constante cinetica para el gasto de sulfuro (L/h)
        # constante cinetica para el gasto de nitrogeno (L/h)
        self.k_n_new = k_n/24
        # constante cinetica para la produccion de metano (L^2*mol/h)
        self.k_ch4_new = k_ch4/24
        # constante cinetica para la produccion de dioxido de carbono (L^2*mol/h)
        self.k_co2_new = k_co2/24
        # constante cinetica para la produccion de sulfuro de hidrogeno (L^2*mol/h)
        self.k_h2s_new = k_h2s/24
        # constante cinetica para la produccion de amonio (L^2*mol/h)
        self.k_nh3_new = k_nh3/24
        # Energias de activacion
        # energia de activacion para el gasto de carbono (J/mol)
        self.Ea_c = Ea_c
        # energia de activacion para el gasto de hidrogeno (J/mol)
        self.Ea_h = Ea_h
        # energia de activacion para el gasto de oxigeno (J/mol)
        self.Ea_o = Ea_o
        # energia de activacion para el gasto de sulfuro (J/mol)
        self.Ea_s = Ea_s
        # energia de activacion para el gasto de nitrogeno (J/mol)
        self.Ea_n = Ea_n
        # energia de activacion para la produccion de metano (J/mol)
        self.Ea_ch4 = Ea_ch4
        # energia de activacion para la produccion de dioxido de carbono (J/mol)
        self.Ea_co2 = Ea_co2
        # energia de activacion para la produccion de sulfuro de hidrogeno (J/mol)
        self.Ea_h2s = Ea_h2s
        # energia de activacion para la produccion de sulfuro de hidrogeno (J/mol)
        self.Ea_nh3 = Ea_nh3

        #return self.k_c, self.k_h, self.k_o, self.k_s, self.k_n, self.k_ch4, self.k_co2, self.k_h2s, self.k_nh3, self.Ea_c, self.Ea_h, self.Ea_o, self.Ea_s, self.Ea_n, self.Ea_ch4, self.Ea_co2, self.Ea_h2s, self.Ea_nh3

    # Parametros de operacion del flujo de entrada del fluido termico que va por las chaquetas de los reactores
    def TermicFluidParameters(self, vin_termico1=600, vin_termico2=600, Tin_termico=60, Pin_termico=35, DT_termico1=0.1, DT_termico2=0.1, DP_termico1=5, DP_termico2=7):
        # Caudal de fluido termico a la entrada de la chaqueta del reactor 1 (L/h)
        self.vin_termico1 = vin_termico1
        # Caudal de fluido termico a la entrada de la chaqueta del reactor 2 (L/h)
        self.vin_termico2 = vin_termico2
        self.Tin_termico = Tin_termico  # Temperatura del fluido térmico (°c)
        # Presion de entrada del fluido termico a la chaqueta (kPa)
        self.Pin_termico = Pin_termico
        # Delta temperatura del fluido termico en la chaqueta del reactor 1
        self.DT_termico1 = DT_termico1
        # Delta temperatura del fluido termico en la chaqueta del reactor 2
        self.DT_termico2 = DT_termico2
        # Caida de presion del fluido termico en la chaqueta del reactor 1
        self.DP_termico1 = DP_termico1
        # caida de presion del fluido termico en la cahquera del reactor 2
        self.DP_termico2 = DP_termico2

        #return self.vin_termico1, self.vin_termico2, self.Tin_termico, self.Pin_termico, self.DT_termico1, self.DT_termico2, self.DP_termico1, self.DP_termico2

    # Parámetros medio ambientales
    def AmbientalParameters(self, Patm=100, Tamb=15):
        self.Patm = Patm  # Presion ambiente (kPa)
        self.Tamb = Tamb  # Temperatura ambiente (°c)

        #return self.Patm, self.Tamb
    # Estimacion de variables absolutas para los modelos masicos y termodinamicos

    def AbsoluteVariables(self):
        self.MW_sus = (self.Cci*self.ST)*12+(self.Chi*self.ST)+(self.Coi*self.ST)*16+(self.Csi*self.ST)*32+(self.Cni*self.ST)*14+(1-self.ST)*18  # estimacion del peso molecular del sustrato (g/mol)
        # Temperatura absoluta del sustrato a la entrada del reactor (K)
        self.Tin_sus_K = self.Tin_sus+273.15
        # moles de sustrato acumulados en el reactor 1 (mol)
        self.n_sus1 = (self.V1*self.rho_sus)/self.MW_sus
        # moles de sustrato acumulados en el reactor 2 (mol)
        self.n_sus2 = (self.V2*self.rho_sus)/self.MW_sus
        # moles de sustrato que ingresan al sistema (mol/h)
        self.nin_sus = (self.vin_sus*self.rho_sus)/self.MW_sus
        # Concentracion molar de carbono en el sustrato (mol/L)
        self.Cci_new = ((self.Cci*self.ST)/12)*self.rho_sus
        # Concentracion molar de hidrogeno en el sustrato (mol/L)
        self.Chi_new = (self.Chi*self.ST)*self.rho_sus
        # Concentracion molar de oxigeno en el sustrato (mol/L)
        self.Coi_new = ((self.Coi*self.ST)/16)*self.rho_sus
        # Concentracion molar de sulfuro en el sustrato (mol/L)
        self.Csi_new = ((self.Csi*self.ST)/32)*self.rho_sus
        # Concentracion molar de nitrogeno en el sustrato (mol/L)
        self.Cni_new = ((self.Cni*self.ST)/14)*self.rho_sus
        # Temperatura absoluta del fluido termico (K)
        self.Tin_termico_K = self.Tin_termico+273.15
        # Flujo molar de entrada del fluido termico a la chaqueta del reactor 1 (mol/h)
        self.n_termico1 = (self.vin_termico1*1000)/18
        # Flujo molar de entrada del fluido termico a la chaqueta del reactor 2 (mol/h)
        self.n_termico2 = (self.vin_termico2*1000)/18

        # Tupla de flujos para controlador de temperatura del reactor 1
        self.n_termico1 = (self.n_termico1, 0)
        # Tupla de flujos para controlador de temperatura del reactor 2
        self.n_termico2 = (self.n_termico2, 0)

        # Temperatura absoluta medio ambiental (K)
        self.Tamb_K = self.Tamb+273.15
        # Temperatura absoluta del Set-Point reactor 1 (K)
        self.Tset1_K = self.Tset1+273.15
        # Temperatura absoluta del Set-Point reactor 2 (K)
        self.Tset2_K = self.Tset2+273.15

        #return self.MW_sus, self.Tin_sus, self.n_sus1, self.n_sus2, self.nin_sus, self.Cci, self.Chi, self.Coi, self.Csi, self.Cni, self.Tin_termico, self.n_termico1, self.n_termico2,  self.Tamb, self.Tset1, self.Tset2

    # Estimacion de areas de intercambio de calor para balance energetico
    def HeatExchangeAreas(self):
        # Reactor 1
        self.D1 = ((self.V1/1000)*4/(np.pi*self.L_H1))**(1/3)  # Diametro del reactor 1 (m)
        self.L1 = self.L_H1*self.D1  # Altura del reactor 1 (m)
        self.A1 = 2*np.pi*(self.D1/2)*self.L1  # Area del reactor 1 (m^2)
        # Area de intercambio con los alrededores (m^2)
        self.A11 = 2*np.pi*((self.D1*1.2)/2)*self.L1
        # Reactor 2
        self.D2 = ((self.V2/1000)*4/(np.pi*self.L_H2)
                   )**(1/3)  # Diametro del reactor 2 (m)
        self.L2 = self.L_H2*self.D2  # Altura del reactor 2 (m)
        self.A2 = 2*np.pi*(self.D2/2)*self.L2  # Area del reactor 2 (m^2)
        # Area de intercambio con los alrededores (m^2)
        self.A22 = 2*np.pi*((self.D2*1.2)/2)*self.L2

        #return self.A11, self.A22

    # estimacion del vector de tiempo para la simulacion
    def TimeVectorEstimation(self):
        # Calculos del numero de puntos en el tiempo a simular
        self.Puntos = int((self.dias*24)/self.tp)
        self.t = []  # Lista donde se almacenan los puntos en el tiempo
        self.tini = 0  # Tiempo inicial siempre 0
        for i in range(self.Puntos):  # iteracion para llenar el vector de tiempo
            self.t.append(self.tini)  # agregar los puntos al vector de tiempo
            self.tini = self.tini+self.tp
        #return self.t

    def BoundaryConditionsR1(self):
        self.Pint = 0  # Presion inicial del sistema (kPa)
        # La temperatura inicial del sistema es la misma que la temperatura Ambiente
        self.Tsis1 = self.Tamb_K

        self.Cci_ini = self.Cci_new  # La concentracion inicial de carbono en el sustrato
        self.Chi_ini = self.Chi_new  # La concentracion inicial del hidrogeno atomico en el sustrato
        self.Coi_ini = self.Coi_new  # La concentracion inicial del oxigeno atomico en el sustrato
        self.Csi_ini = self.Csi_new  # La concentracion inicial del azufre atomico en el sustrato
        self.Cni_ini = self.Cni_new  # La concentracion inicial del nitrogeno atomico en el sustrato

        self.Cch4i_ini = 0  # En el tiempo 0 la concentracion de metano es 0
        self.Cco2i_ini = 0  # En el tiempo 0 la concentracion de dioxido de carbono es 0
        self.Ch2si_ini = 0  # En el tiempo 0 la concentracion de sulfuro de hidrogeno es 0
        self.Cnh3i_ini = 0  # En el tiempo 0 la concentracion de amonio es 0

        self.T1 = []
        self.T1.append(self.Tsis1)

        self.C1 = []
        self.C1.append(self.Cci_ini)

        self.H11 = []
        self.H11.append(self.Chi_ini)

        self.O1 = []
        self.O1.append(self.Coi_ini)

        self.S1 = []
        self.S1.append(self.Csi_ini)

        self.N1 = []
        self.N1.append(self.Cni_ini)

        self.CH41 = []
        self.CH41.append(self.Cch4i_ini)

        self.CO21 = []
        self.CO21.append(self.Cco2i_ini)

        self.H2S1 = []
        self.H2S1.append(self.Ch2si_ini)

        self.NH31 = []
        self.NH31.append(self.Cnh3i_ini)

        # Crear las listas para almacenar los datos del reactor 2

        #return self.Pint, self.Tsis1, self.Cci_ini, self.Chi_ini, self.Coi_ini, self.Csi_ini, self.Cni_ini, self.Cch4i_ini, self.Cco2i_ini, self.Ch2si_ini, self.Cnh3i_ini, self.T1, self.C1, self.H11, self.O1, self.S1, self.N1, self.CH41, self.CO21, self.H2S1, self.NH31

    def BoundaryConditionsR2(self):
        self.Pint = 0  # Presion inicial del sistema (kPa)
        # La temperatura inicial del reactor 2 es la misma que la temperatura Ambiente
        self.Tsis2 = self.Tamb_K

        self.Cci_ini2 = self.Cci_new  # La concentracion inicial de carbono en el sustrato
        self.Chi_ini2 = self.Chi_new  # La concentracion inicial del hidrogeno atomico en el sustrato
        self.Coi_ini2 = self.Coi_new  # La concentracion inicial del oxigeno atomico en el sustrato
        self.Csi_ini2 = self.Csi_new  # La concentracion inicial del azufre atomico en el sustrato
        self.Cni_ini2 = self.Cni_new  # La concentracion inicial del nitrogeno atomico en el sustrato        

        self.Cch4i_ini2 = 0  # Condicion de frontera para la concentracion de metano en el reactor 2
        self.Cco2i_ini2 = 0  # Condicion de frontera para la concentracion de dioxido de carbono en el reactor 2
        self.Ch2si_ini2 = 0  # Condicion de frontera para la concentracion de sulfuro de hidrogeno en el reactor 2
        self.Cnh3i_ini2 = 0  # Condicion de frontera para la concentracion de amonio en el reactor 2

        # Definir las condiciones y listas para el reactor 2
        self.T2 = []
        self.T2.append(self.Tsis2)

        self.C2 = []
        self.C2.append(self.Cci_ini2)

        self.H22 = []
        self.H22.append(self.Chi_ini2)

        self.O2 = []
        self.O2.append(self.Coi_ini2)

        self.S2 = []
        self.S2.append(self.Csi_ini2)

        self.N2 = []
        self.N2.append(self.Cni_ini2)

        self.CH42 = []
        self.CH42.append(self.Cch4i_ini2)

        self.CO22 = []
        self.CO22.append(self.Cco2i_ini2)

        self.H2S2 = []
        self.H2S2.append(self.Ch2si_ini2)

        self.NH32 = []
        self.NH32.append(self.Cnh3i_ini2)

        # Crear las listas para almacenar los datos del reactor 2

        #return self.Pint, self.Tsis2, self.Cch4i_ini2, self.Cco2i_ini2, self.Ch2si_ini2, self.Cnh3i_ini2, self.T2, self.C2, self.H2, self.O2, self.S2, self.N2, self.CH42, self.CO22, self.H2S2, self.NH32

    def Reactor1Simulation(self):
        self.TP = Thermo.ThermoProperties()
        self.R = 9.314
        for i in self.t:  # Partición de los limites de la integral de acuerdo al tamano de paso del tiempo
            if i > 1 - len(self.t):
                self.tv = [i, i+self.tp]
            if i < 1-len(self.t):
                self.tv = [i, i+self.tp]

            if self.Tsis1 <= self.Tset1_K - self.tolerancia1:  # Controlador de temperatura del reactor 1
                self.nin_termico1 = self.n_termico1[0]
            if self.Tsis1 >= self.Tset1_K + self.tolerancia1:
                self.nin_termico1 = self.n_termico1[1]
    
            def R1Simulation(C, t):
                
                self.H1 = self.TP.Hliq(self.Tin_sus_K, self.Pin_sus, self.Patm) # Entalpia de entrada para el sustrato
                self.H2 = self.TP.Hliq(C[0], self.Pint, self.Patm)  # Entalpia del sustrato a la salida
                self.H1_termico = self.TP.Hliq(self.Tin_termico_K, self.Pin_termico, self.Patm) # Entalpia del fluido termico a la entrada
                self.H2_termico = self.TP.Hliq(self.Tin_termico_K-self.DT_termico1, self.Pin_termico-self.DP_termico1, self.Patm)  # Entalpia del fluido termico a la salida del reactor
                
                #Balance de energia
                self.dH_dt = ((self.nin_sus/self.n_sus1))*(self.H1-self.H2)+(self.nin_termico1/self.n_sus1)*(self.H1_termico-self.H2_termico)*((self.Tin_termico_K-C[0])/self.Tin_termico_K) - ((self.U1*self.A11)/self.n_sus1)*(C[0]-self.Tamb_K)  # balance de energia
    
                # Cinetica para el carbono
                self.r_c = self.k_c_new*np.exp(-self.Ea_c/(self.R*C[0]))*C[1]
                self.dCc_dt = (self.vin_sus*self.Cci_new)/self.V1 - (self.vin_sus*C[1])/self.V1 - self.r_c  # Balance masa carbono
    
                # Cinetica para el hidrogeno
                self.r_h = self.k_h_new*np.exp(-self.Ea_h/(self.R*C[0]))*C[2]
                self.dCh_dt = (self.vin_sus*self.Chi_new)/self.V1 - (self.vin_sus*C[2])/self.V1 - self.r_h  # Balance masa hidrogeno
    
                # Cinetica para el oxigeno
                self.r_o = self.k_o_new*np.exp(-self.Ea_o/(self.R*C[0]))*C[3]
                self.dCo_dt = (self.vin_sus*self.Coi_new)/self.V1 - (self.vin_sus*C[3])/self.V1 - self.r_o  # Balance masa oxigeno
    
                # Cinetica para el azufre
                self.r_s = self.k_s_new*np.exp(-self.Ea_s/(self.R*C[0]))*C[4]
                self.dCs_dt = (self.vin_sus*self.Csi_new)/self.V1 - (self.vin_sus*C[4])/self.V1 - self.r_s  # Balance masa azufre
    
                # Cinetica para el nitrogeno
                self.r_n = self.k_n_new*np.exp(-self.Ea_n/(self.R*C[0]))*C[5]
                self.dCn_dt = (self.vin_sus*self.Cni_new)/self.V1 - (self.vin_sus*C[5])/self.V1 - self.r_n  # Balance masa nitrogeno
    
                # Cinetica para el metano
                self.r_ch4 = self.k_ch4_new*np.exp(-self.Ea_ch4/(self.R*C[0]))*C[1]*C[2]
                # Balance masa metano
                self.dCch4_dt = -(self.vin_sus*C[6])/self.V1 + self.r_ch4
    
                # Cinetica para el dioxido de carbono
                self.r_co2 = self.k_co2_new*np.exp(-self.Ea_co2/(self.R*C[0]))*C[1]*C[3]
                # Balance de masa dioxodo de carbono
                self.dCco2_dt = -(self.vin_sus*C[7])/self.V1 + self.r_co2
    
                # Cinetica para el sulfuro de hidrogeno
                self.r_h2s = self.k_h2s_new*np.exp(-self.Ea_h2s/(self.R*C[0]))*C[2]*C[4]
                # Balance de masa sulfuro de hidrogeno
                self.dCh2s_dt = -(self.vin_sus*C[8])/self.V1 + self.r_h2s
    
                # Cinetica para amonio
                self.r_nh3 = self.k_nh3_new*np.exp(-self.Ea_nh3/(self.R*C[0]))*C[2]*C[5]
                # Balance de masa amonio
                self.dCnh3_dt = -(self.vin_sus*C[9])/self.V1 + self.r_nh3
    
                return [self.dH_dt, self.dCc_dt, self.dCh_dt, self.dCo_dt, self.dCs_dt, self.dCn_dt, self.dCch4_dt, self.dCco2_dt, self.dCh2s_dt, self.dCnh3_dt]
    
            self.Initial_Values1 = [self.Tsis1, self.Cci_ini, self.Chi_ini, self.Coi_ini, self.Csi_ini, self.Cni_ini, self.Cch4i_ini, self.Cco2i_ini, self.Ch2si_ini, self.Cnh3i_ini]  # Condiciones de frontera de la funcion boundary conditions
    
            # Solucionamos el sistema de ecuaciones para el reactor 1
            self.SolutionR1 = odeint(R1Simulation, self.Initial_Values1, self.tv)
    
            # almaceno la Temperatura del reactor 1 en una lista para ese periodo de tiempo
            self.T1.append(float(self.SolutionR1[-1, 0]))
    
            # almaceno la concentracion de carbono a la salida del R1
            self.C1.append(float(self.SolutionR1[-1, 1]))
    
            # almaceno la concentracion de hidrogeno a la salida de R1
            self.H11.append(float(self.SolutionR1[-1, 2]))
    
            # almaceno la concentracion de oxigeno a la salida de R1
            self.O1.append(float(self.SolutionR1[-1, 3]))
    
            # almaceno la concentracion de sulfuro a la salida de R1
            self.S1.append(float(self.SolutionR1[-1, 4]))
    
            # almaceno la concentracion de nitrogeno a la salida de R1
            self.N1.append(float(self.SolutionR1[-1, 5]))
    
            # almaceno moles de metano a la salida de R1
            self.CH41.append(float(self.SolutionR1[-1, 6]))
    
            # almaceno moles de dioxido de carbono a la salida de R1
            self.CO21.append(float(self.SolutionR1[-1, 7]))
    
            # almaceno moles de sulfuro de hidrogeno a la salida de R1
            self.H2S1.append(float(self.SolutionR1[-1, 8]))
    
            # almaceno moles de amonio a la salida de R1
            self.NH31.append(float(self.SolutionR1[-1, 9]))
    
            # actualizacion del valor inicial de la temperatura inicial para la siguiente iteracion
            self.Tsis1 = self.SolutionR1[-1, 0]
            # actualización del valor inicial de la conentracion de carbono para la siguiente iteracion
            self.Cci_ini = self.SolutionR1[-1, 1]
            # actualización del valor inicial de la conentracion de hidrogeno para la siguiente iteracion
            self.Chi_ini = self.SolutionR1[-1, 2]
            # actualizacion del valor inicial de la concentracion de oxigeno para la siguiente iteracion
            self.Coi_ini = self.SolutionR1[-1, 3]
            # actualizacion del valor inicial de la concentracion de sulfuro para la siguiente iteracion
            self.Csi_ini = self.SolutionR1[-1, 4]
            # actualizacion del valor inicial de la concentracion de nitrogeno para la siguiente iteracion
            self.Cni_ini = self.SolutionR1[-1, 5]
            # actualizacion del valor inicial de la concentracion de metano para la siguiente iteracion
            self.Cch4i_ini = self.SolutionR1[-1, 6]
            # actualizacion del valor inicial de la concentracion de dioxido de carbono para la siguiente iteracion
            self.Cco2i_ini = self.SolutionR1[-1, 7]
            # actualizacion del valor inicial de la concentracion de sulfuro de hidrogeno para la siguiente iteracion
            self.Ch2si_ini = self.SolutionR1[-1, 8]
            # actualizacion del valor inicial de la concentracion de amonio para la siguiente iteracion
            self.Cnh3i_ini = self.SolutionR1[-1, 9]

        #return self.T1, self.CH41, self.CO21, self.H2S1, self.NH31

    def Reactor2Simulation(self):
        self.TP = Thermo.ThermoProperties()
        self.R = 9.314
        j=0
        for i in self.t:  # Partición de los limites de la integral de acuerdo al tamano de paso del tiempo
            if i > 1 - len(self.t):
                self.tv = [i, i+self.tp]
            if i < 1-len(self.t):
                self.tv = [i, i+self.tp]

            if self.Tsis2 <= self.Tset2_K - self.tolerancia2:  # Controlador de temperatura del reactor 2
                self.nin_termico2 = self.n_termico2[0]
            if self.Tsis2 >= self.Tset2_K + self.tolerancia2:
                self.nin_termico2 = self.n_termico2[1]
    
            # Concentración de entrada a la segunda etapa
            self.Cci2 = self.C1[j]
            self.Chi2 = self.H11[j]
            self.Coi2 = self.O1[j]
            self.Csi2 = self.S1[j]
            self.Cni2 = self.N1[j]
            self.Tin_sus_K = self.T1[j]
            j=j+1
    
            def R2Simulation(C, t):
               
                self.H1 = self.TP.Hliq(self.Tin_sus_K, self.Pin_sus, self.Patm)  # Entalpia de entrada para el sustrato
                self.H2 = self.TP.Hliq(C[0], self.Pint, self.Patm) # Entalpia del sustrato a la salida
                self.H1_termico = self.TP.Hliq(self.Tin_termico_K, self.Pin_termico, self.Patm)  # Entalpia del fluido termico a la entrada
                self.H2_termico = self.TP.Hliq(self.Tin_termico_K-self.DT_termico2, self.Pin_termico-self.DP_termico2, self.Patm)  # Entalpia del fluido termico a la salida del reactor
                
                #Balance de energia
                self.dH_dt = ((self.nin_sus/self.n_sus2))*(self.H1-self.H2)+(self.nin_termico2/self.n_sus2)*(self.H1_termico-self.H2_termico)*((self.Tin_termico_K-C[0])/self.Tin_termico_K) - ((self.U2*self.A22)/self.n_sus2)*(C[0]-self.Tamb_K)  # balance de energia
    
                # Cinetica para el carbono
                self.r_c = self.k_c_new*np.exp(-self.Ea_c/(self.R*C[0]))*C[1]
                self.dCc_dt = (self.vin_sus*self.Cci2)/self.V2 - (self.vin_sus * C[1])/self.V2 - self.r_c  # Balance masa carbono
    
                # Cinetica para el hidrogeno
                self.r_h = self.k_h_new*np.exp(-self.Ea_h/(self.R*C[0]))*C[2]
                self.dCh_dt = (self.vin_sus*self.Chi2)/self.V2 - (self.vin_sus * C[2])/self.V2 - self.r_h  # Balance masa hidrogeno
    
                # Cinetica para el oxigeno
                self.r_o = self.k_o_new*np.exp(-self.Ea_o/(self.R*C[0]))*C[3]
                self.dCo_dt = (self.vin_sus*self.Coi2)/self.V2 - (self.vin_sus * C[3])/self.V2 - self.r_o  # Balance masa oxigeno
    
                # Cinetica para el azufre
                self.r_s = self.k_s_new*np.exp(-self.Ea_s/(self.R*C[0]))*C[4]
                self.dCs_dt = (self.vin_sus*self.Csi2)/self.V2 - (self.vin_sus * C[4])/self.V2 - self.r_s  # Balance masa azufre
    
                # Cinetica para el nitrogeno
                self.r_n = self.k_n_new*np.exp(-self.Ea_n/(self.R*C[0]))*C[5]
                self.dCn_dt = (self.vin_sus*self.Cni2)/self.V2 - (self.vin_sus * C[5])/self.V2 - self.r_n  # Balance masa nitrogeno
    
                # Cinetica para el metano
                self.r_ch4 = self.k_ch4_new * np.exp(-self.Ea_ch4/(self.R*C[0]))*C[1]*C[2]
                # Balance masa metano
                self.dCch4_dt = -(self.vin_sus*C[6])/self.V2 + self.r_ch4
    
                # Cinetica para el dioxido de carbono
                self.r_co2 = self.k_co2_new * np.exp(-self.Ea_co2/(self.R*C[0]))*C[1]*C[3]
                # Balance de masa dioxodo de carbono
                self.dCco2_dt = -(self.vin_sus*C[7])/self.V2 + self.r_co2
    
                # Cinetica para el sulfuro de hidrogeno
                self.r_h2s = self.k_h2s_new *np.exp(-self.Ea_h2s/(self.R*C[0]))*C[2]*C[4]
                # Balance de masa sulfuro de hidrogeno
                self.dCh2s_dt = -(self.vin_sus*C[8])/self.V2 + self.r_h2s
    
                # Cinetica para amonio
                self.r_nh3 = self.k_nh3_new *np.exp(-self.Ea_nh3/(self.R*C[0]))*C[2]*C[5]
                # Balance de masa amonio
                self.dCnh3_dt = -(self.vin_sus*C[9])/self.V2 + self.r_nh3
    
                return [self.dH_dt, self.dCc_dt, self.dCh_dt, self.dCo_dt, self.dCs_dt, self.dCn_dt, self.dCch4_dt, self.dCco2_dt, self.dCh2s_dt, self.dCnh3_dt]
    
            self.Initial_Values1 = [self.Tsis2, self.Cci_ini2, self.Chi_ini2, self.Coi_ini2, self.Csi_ini2, self.Cni_ini2, self.Cch4i_ini2, self.Cco2i_ini2, self.Ch2si_ini2, self.Cnh3i_ini2]  # Condiciones de frontera de la funcion boundary conditions
    
            # Solucionamos el sistema de ecuaciones para el reactor 2
            self.SolutionR2 = odeint(R2Simulation, self.Initial_Values1, self.tv)
    
            # almaceno la Temperatura del reactor 2 en una lista para ese periodo de tiempo
            self.T2.append(float(self.SolutionR2[-1, 0]))
    
            # almaceno la concentracion de carbono a la salida del R2
            self.C2.append(float(self.SolutionR2[-1, 1]))
    
            # almaceno la concentracion de hidrogeno a la salida de R2
            self.H22.append(float(self.SolutionR2[-1, 2]))
    
            # almaceno la concentracion de oxigeno a la salida de R2
            self.O2.append(float(self.SolutionR2[-1, 3]))
    
            # almaceno la concentracion de sulfuro a la salida de R2
            self.S2.append(float(self.SolutionR2[-1, 4]))
    
            # almaceno la concentracion de nitrogeno a la salida de R2
            self.N2.append(float(self.SolutionR2[-1, 5]))
    
            # almaceno moles de metano a la salida de R2
            self.CH42.append(float(self.SolutionR2[-1, 6]))
    
            # almaceno moles de dioxido de carbono a la salida de R2
            self.CO22.append(float(self.SolutionR2[-1, 7]))
    
            # almaceno moles de sulfuro de hidrogeno a la salida de R2
            self.H2S2.append(float(self.SolutionR2[-1, 8]))
    
            # almaceno moles de amonio a la salida de R2
            self.NH32.append(float(self.SolutionR2[-1, 9]))
    
            # actualizacion del valor inicial de la temperatura inicial para la siguiente iteracion
            self.Tsis2 = self.SolutionR2[-1, 0]
            # actualización del valor inicial de la conentracion de carbono para la siguiente iteracion
            self.Cci_ini2 = self.SolutionR2[-1, 1]
            # actualización del valor inicial de la conentracion de hidrogeno para la siguiente iteracion
            self.Chi_ini2 = self.SolutionR2[-1, 2]
            # actualizacion del valor inicial de la concentracion de oxigeno para la siguiente iteracion
            self.Coi_ini2 = self.SolutionR2[-1, 3]
            # actualizacion del valor inicial de la concentracion de sulfuro para la siguiente iteracion
            self.Csi_ini2 = self.SolutionR2[-1, 4]
            # actualizacion del valor inicial de la concentracion de nitrogeno para la siguiente iteracion
            self.Cni_ini2 = self.SolutionR2[-1, 5]
            # actualizacion del valor inicial de la concentracion de metano para la siguiente iteracion
            self.Cch4i_ini2 = self.SolutionR2[-1, 6]
            # actualizacion del valor inicial de la concentracion de dioxido de carbono para la siguiente iteracion
            self.Cco2i_ini2 = self.SolutionR2[-1, 7]
            # actualizacion del valor inicial de la concentracion de sulfuro de hidrogeno para la siguiente iteracion
            self.Ch2si_ini2 = self.SolutionR2[-1, 8]
            # actualizacion del valor inicial de la concentracion de amonio para la siguiente iteracion
            self.Cnh3i_ini2 = self.SolutionR2[-1, 9]

        #return self.T2, self.CH42, self.CO22, self.H2S2, self.NH3
        
    def ScenariosResults(self):
        
        if len(self.CH42) <= 1:
            self.Results=pd.DataFrame()
            self.Results['MethaneR1']=self.CH41
            self.Results['Carbon dioxideR1']=self.CO21
            self.Results['hydrogen sulphideR1']=self.H2S1
            self.Results['AmmoniumR1']=self.NH31
            self.Results['Total BiogasR1']=self.Results['MethaneR1']+self.Results['Carbon dioxideR1']+self.Results['hydrogen sulphideR1']+self.Results['AmmoniumR1']
            self.BiogasMolarFlow = self.Results['Total BiogasR1'].copy()
            self.BiogasVolFlow = self.BiogasMolarFlow*22.4  #[L/h]
            
            #Estimacion del LHV
            self.xCH4=self.Results['MethaneR1']/self.BiogasMolarFlow
            self.xCO2=self.Results['Carbon dioxideR1']/self.BiogasMolarFlow
            #Balance carbono
            self.nCO2 = self.xCH4 + self.xCO2
            #Balance de hidrogeno
            self.nH2O = 2*self.xCH4
            #Balance de oxígeno
            self.alfa = (2*self.nCO2+self.nH2O-2*self.xCO2)/2
            #Balance de nitrogeno
            self.nN2 = self.alfa*2*3.76
            
            self.LHV = ((self.xCH4*(-74520)+self.xCO2*(-393510))+(self.alfa*0+3.76*self.alfa*0)-(self.nCO2*(-393510)+self.nH2O*(-241810)+self.nN2*0))/(3600*22.4)  #[Wh/L]
            
        else:
            self.Results=pd.DataFrame()
            self.Results['MethaneR1']=self.CH41
            self.Results['MethaneR2']=self.CH42
            self.Results['Carbon dioxideR1']=self.CO21
            self.Results['Carbon dioxideR2']=self.CO22
            self.Results['hydrogen sulphideR1']=self.H2S1
            self.Results['hydrogen sulphideR2']=self.H2S2
            self.Results['AmmoniumR1']=self.NH31
            self.Results['AmmoniumR2']=self.NH32
            self.Results['Total BiogasR1'] = self.Results['MethaneR1']+self.Results['Carbon dioxideR1']+self.Results['hydrogen sulphideR1']+self.Results['AmmoniumR1']
            self.Results['Total BiogasR2'] = self.Results['MethaneR2']+self.Results['Carbon dioxideR2']+self.Results['hydrogen sulphideR2']+self.Results['AmmoniumR2']
            self.BiogasMolarFlow = (self.Results['Total BiogasR1'] + self.Results['Total BiogasR2']).copy()
            self.BiogasVolFlow = self.BiogasMolarFlow*22.4  #[L/h]
            
            #Estimacion del LHV
            self.xCH4=(self.Results['MethaneR1']+self.Results['MethaneR2'])/self.BiogasMolarFlow
            self.xCO2=(self.Results['Carbon dioxideR1']+self.Results['Carbon dioxideR2'])/self.BiogasMolarFlow
            
            #Balance carbono
            self.nCO2 = self.xCH4 +self.xCO2
            #Balance de hidrogeno
            self.nH2O = 2*self.xCH4
            #Balance de oxígeno
            self.alfa = (2*self.nCO2+self.nH2O-2*self.xCO2)/2
            #Balance de nitrogeno
            self.nN2 = self.alfa*2*3.76
            
            self.LHV = ((self.xCH4*(-74520)+self.xCO2*(-393510))+(self.alfa*0+3.76*self.alfa*0)-(self.nCO2*(-393510)+self.nH2O*(-241810)+self.nN2*0))/(3600*22.4)  #[Wh/L]
        self.LHV[0] = self.LHV[1]

    def GeneratorParameters(self, genEfficiency, ratedPower):
        self.genEfficiency = genEfficiency
        self.P_max = ratedPower
        self.P_min = 0.0
    
    def PowerOutput(self):
        
        P_b = self.LHV * self.BiogasVolFlow * (self.genEfficiency/100) / 1000 # Potencia eléctrica generada en kW
        P_b[0] = 0.0
        P_b.where(cond=P_b<self.P_max, other=self.P_max, inplace=True)
        P_b_list = P_b.tolist()

        return P_b_list
    
    def ReloadThermo(self):
        importlib.reload(Thermo)
        
    
   