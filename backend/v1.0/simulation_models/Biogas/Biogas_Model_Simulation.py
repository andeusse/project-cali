# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:21:50 2025

@author: Sergio
"""

import pandas as pd
from datetime import datetime
import numpy as np
from scipy.integrate import odeint
import requests
from fractions import Fraction
from math import gcd
from functools import reduce
from simulation_models.Biogas import ThermoProperties as TP
from scipy.integrate import odeint
import time

class BiogasPlantSimulation:
    def __init__ (self, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, 
                 ST_R101=10, SV_R101=1, Cc_R101=40.48, Ch_R101=5.29, Co_R101=29.66, Cn_R101=1.37, Cs_R101=0.211, rho_R101=1000,
                 ST_R102=10, SV_R102=1, Cc_R102=40.48, Ch_R102=5.29, Co_R102=29.66, Cn_R102=1.37, Cs_R102=0.211, rho_R102=1000,
                 OperationMode="Modo1"):
        
        #Interface Inputs
        self.VR1 = VR1
        self.VR2 = VR2
        self.VG1 = VG1
        self.VG2 = VG2
        self.VG3 = VG3
        self.tp = tp
        self.OperationMode = OperationMode

        # Thermodynamic model for gases estimations
        self.thermo = TP.ThermoProperties()
        
        #----- initial values

        #Global time
        self.GlobalTime = 0

        #Pumps
        self.TimeCounterPump_P104 = 0
        self.TimeCounterPump_P101 = 0
        self.TimeCounterPump_P102 = 0
        
        #mixers
        self.TimeCounterMixer_TK100 = 0
        self.TimeCounterMixer_R101 = 0
        self.TimeCounterMixer_R102 = 0

        #----Reactor R101 conditions
        #Reactor 101 initial conditions
        self.ST_R101 = ST_R101
        self.SV_R101 = SV_R101
        self.Cc_R101 = Cc_R101
        self.Ch_R101 = Ch_R101
        self.Co_R101 = Co_R101
        self.Cn_R101 = Cn_R101
        self.Cs_R101 = Cs_R101
        self.rho_R101 = rho_R101
        self.Vinj_R101 = 0
        self.x_substrate_R101 = 0
        self.x_inoculum_R101 = 1
        self.SV_R101_gompertz = SV_R101

        # Find empiric formula for initial conditions in reactor 101 
        if self.ST_R101 == 0:
            self.Csus_ini_R101 = 0
            self.Csus_ini_ST_R101 = 0
        
        else:
            self.molC_R101 = self.Cc_R101*(1/12.01)
            self.molH_R101 = self.Ch_R101*(1/1.01)
            self.molO_R101 = self.Co_R101*(1/16)
            self.molN_R101 = self.Cn_R101*(1/14)
            self.molS_R101 = self.Cs_R101*(1/32)

            n_R101 = self.molC_R101
            a_R101 = self.molH_R101
            b_R101 = self.molO_R101
            c_R101 = self.molN_R101
            d_R101 = self.molS_R101

            def lcm(a,b):
                return a * b // gcd(a, b)

            numbers_R101 = [n_R101, a_R101, b_R101, c_R101, d_R101]
            denominators_R101 = [Fraction(num).limit_denominator(10).denominator for num in numbers_R101]
            common_denominator_R101 = reduce(lcm, denominators_R101)
            subindex_R101 = [int(num * common_denominator_R101) for num in numbers_R101]

            self.n_R101 = subindex_R101[0]
            self.a_R101 = subindex_R101[1]
            self.b_R101 = subindex_R101[2]
            self.c_R101 = subindex_R101[3]
            self.d_R101 = subindex_R101[4]

            self.s_H2O_R101 = self.n_R101-(self.a_R101/4)-(self.b_R101/2)+(3/4)*self.c_R101+(self.d_R101/2)
            self.s_CH4_R101 = (self.n_R101/2)+(self.a_R101/8)-(self.b_R101/4)-(3/8)*self.c_R101-(self.d_R101/4)
            self.s_CO2_R101 = (self.n_R101/2)-(self.a_R101/8)+(self.b_R101/4)+(3/8)*self.c_R101-(self.d_R101/4)
            self.s_NH3_R101 = self.c_R101
            self.s_H2S_R101 = self.d_R101

            self.MW_sustrato_R101 = self.n_R101*12.01+self.a_R101*1.01+self.b_R101*16+self.c_R101*14+self.d_R101*32   #[g/mol]
            self.Csus_ini_R101 = (self.rho_R101*(self.SV_R101/100))/self.MW_sustrato_R101                                   #[mol/L]  
            self.Csus_ini_ST_R101 = (self.rho_R101*(self.ST_R101/100))/self.MW_sustrato_R101                                #[mol/L]
            self.Csus_fixed_R101 = self.Csus_ini_ST_R101 - self.Csus_ini_R101                                         #[mol/L]
             
            
        #----Reactor R102 conditions
        #Reactor 102 initial conditions
        if OperationMode in ["Modo3", "Modo4", "Modo5"]:
            self.ST_R102 = ST_R102
            self.SV_R102 = SV_R102
            self.Cc_R102 = Cc_R102
            self.Ch_R102 = Ch_R102
            self.Co_R102 = Co_R102
            self.Cn_R102 = Cn_R102
            self.Cs_R102 = Cs_R102
            self.rho_R102 = rho_R102
            self.Vinj_R102 = 0
            self.x_substrate_R102 = 0
            self.x_inoculum_R102 = 1
            self.SV_R102_gompertz = SV_R102

            # Find empiric formula for initial conditions in reactor 102
            if self.ST_R102 == 0:
                self.Csus_ini_R102 = 0
                self.Csus_ini_ST_R102 = 0
            
            else:
                self.molC_R102 = self.Cc_R102*(1/12.01)
                self.molH_R102 = self.Ch_R102*(1/1.01)
                self.molO_R102 = self.Co_R102*(1/16)
                self.molN_R102 = self.Cn_R102*(1/14)
                self.molS_R102 = self.Cs_R102*(1/32)

                n_R102 = self.molC_R102
                a_R102 = self.molH_R102
                b_R102 = self.molO_R102
                c_R102 = self.molN_R102
                d_R102 = self.molS_R102

                numbers_R102 = [n_R102, a_R102, b_R102, c_R102, d_R102]
                denominators_R102 = [Fraction(num).limit_denominator(10).denominator for num in numbers_R102]
                common_denominator_R102 = reduce(lcm, denominators_R102)
                subindex_R102 = [int(num * common_denominator_R102) for num in numbers_R102]

                self.n_R102 = subindex_R102[0]
                self.a_R102 = subindex_R102[1]
                self.b_R102 = subindex_R102[2]
                self.c_R102 = subindex_R102[3]
                self.d_R102 = subindex_R102[4]
                
                self.s_H2O_R102 = self.n_R102-(self.a_R102/4)-(self.b_R102/2)+(3/4)*self.c_R102+(self.d_R102/2)
                self.s_CH4_R102 = (self.n_R102/2)+(self.a_R102/8)-(self.b_R102/4)-(3/8)*self.c_R102-(self.d_R102/4)
                self.s_CO2_R102 = (self.n_R102/2)-(self.a_R102/8)+(self.b_R102/4)+(3/8)*self.c_R102-(self.d_R102/4)
                self.s_NH3_R102 = self.c_R102
                self.s_H2S_R102 = self.d_R102
                
                self.MW_sustrato_R102 = self.n_R102*12.01+self.a_R102*1.01+self.b_R102*16+self.c_R102*14+self.d_R102*32
                self.Csus_ini_R102 = (self.rho_R102*(self.SV_R102/100))/self.MW_sustrato_R102
                self.Csus_ini_ST_R102 = (self.rho_R102*(self.ST_R102/100))/self.MW_sustrato_R102
                self.Csus_fixed_R102 = self.Csus_ini_ST_R102 - self.Csus_ini_R102

                #gompertz
                self.mol_ini_R102 = (self.SV_R102/100)/(self.MW_sustrato_R102)*(self.rho_R102)*self.VR2
                self.biogas_mol_R102 = 0
                self.mol_sus_expended_R102 = 0
        
        #V101 gas storage initial conditions
        self.molCH4_acum_V101 = 0
        self.molCO2_acum_V101 = 0
        self.molO2_acum_V101 = 0
        self.molH2O_acum_V101 = 0
        self.molH2S_acum_V101 = 0
        self.molNH3_acum_V101 = 0
        self.molH2_acum_V101 = 0
        self.Pstorage_V101 = 0
        self.Pacum_V101 = 0
        
        #V102 gas storage initial conditions
        self.molCH4_acum_V102 = 0
        self.molCO2_acum_V102 = 0
        self.molO2_acum_V102 = 0
        self.molH2O_acum_V102 = 0
        self.molH2S_acum_V102 = 0
        self.molNH3_acum_V102 = 0
        self.molH2_acum_V102 = 0
        self.Pstorage_V102 = 0
        self.Pacum_V102 = 0
        self.biogasmol_storage_V102 = 0
        
        #Biogas_treatment
        self.xH2S_V107_wet = 0
        self.mol_H2S_ads_acum = 0
        self.xNH3_V107_wet = 0
        self.mol_NH3_ads_acum = 0
        self.xH2O_V107_wet = 0
        self.mol_H2O_ads_acum = 0
        self.mol_H2O_transfertoV107_i = 0
        self.molH2O_acum_V107_i = 0
        self.molH2S_acum_V107_i = 0
        self.molNH3_acum_V107_i  = 0 
             
        #V107 gas storage initial conditions
        self.molCH4_acum_V107 = 0
        self.molCO2_acum_V107 = 0
        self.molO2_acum_V107 = 0
        self.molH2O_acum_V107 = 0
        self.molH2S_acum_V107 = 0
        self.molNH3_acum_V107 = 0
        self.molH2_acum_V107 = 0
        self.Pstorage_V107 = 0
        self.Pacum_V107 = 0
        self.biogasmol_storage_V107 = 0

        #gompertz
        self.mol_ini_R101 = (self.SV_R101/100)/(self.MW_sustrato_R101)*(self.rho_R101)*self.VR1
        self.biogas_mol_R101 = 0
        self.mol_sus_expended_R101 = 0
                
    def Substrate_conditions (self, Cc, Ch, Co, Cn, Cs, ST, SV, rho):
        self.ST = ST
        self.SV = SV
        self.Cc = Cc
        self.Ch = Ch
        self.Co = Co
        self.Cn = Cn
        self.Cs = Cs
        self.rho = rho

        self.molC = self.Cc*(1/12.01)
        self.molH = self.Ch*(1/1.01)
        self.molO = self.Co*(1/16)
        self.molN = self.Cn*(1/14)
        self.molS = self.Cs*(1/32)

        n = self.molC
        a = self.molH
        b = self.molO
        c = self.molN
        d = self.molS

        def lcm(a,b):
                return a * b // gcd(a, b)
        
        numbers = [n, a, b, c, d]
        denominators = [Fraction(num).limit_denominator(10).denominator for num in numbers]
        common_denominator = reduce(lcm, denominators)
        subindex = [int(num * common_denominator) for num in numbers]

        self.n = subindex[0]
        self.a = subindex[1]
        self.b = subindex[2]
        self.c = subindex[3]
        self.d = subindex[4]
        
        self.s_H2O = self.n-(self.a/4)-(self.b/2)+(3/4)*self.c+(self.d/2)
        self.s_CH4 = (self.n/2)+(self.a/8)-(self.b/4)-(3/8)*self.c-(self.d/4)
        self.s_CO2 = (self.n/2)-(self.a/8)+(self.b/4)+(3/8)*self.c-(self.d/4)
        self.s_NH3 = self.c
        self.s_H2S = self.d
        
        #molar concentration
        self.MW_sustrato = self.n*12.01+self.a*1.01+self.b*16+self.c*14+self.d*32      #[g/mol]
        self.Csus_ini = (self.rho*(self.SV/100))/self.MW_sustrato                      #[mol/L] 
        self.Csus_ini_ST = (self.rho*(self.ST/100))/self.MW_sustrato                         #[mol/L]
        self.Csus_fixed = self.Csus_ini_ST - self.Csus_ini                             #[mol/L] 

        self.Csv = (self.rho*(self.SV/100))                                            #[g/L] 
        self.Cst = (self.rho*(self.ST/100))                                            #[g/L] 

           
    def Pump104 (self, TRH = 30, FT_P104 = 5, TTO_P104 = 10, time_accelerator = 1):  #TRH: hydraulic retention time, FT_P104: Feed times per day, TTO_P104: time per feeding event.
        
        self.time_accelerator = time_accelerator
        self.TRH = TRH
        self.FT_P104 = FT_P104
        self.TTO_P104 = TTO_P104
        try:
            self.TurnOnDailyStep_P104 = 24/self.FT_P104
        except ZeroDivisionError:
            self.TurnOnDailyStep_P104=0
        
        if self.OperationMode == "Modo1" or self.OperationMode == "Modo2":
            self.Q_daily = self.VR1/self.TRH
        
        elif self.OperationMode == "Modo3" or self.OperationMode == "Modo4" or self.OperationMode == "Modo5":
            self.Q_daily = (self.VR1 + self.VR2)/self.TRH
        
        self.Q_time = self.Q_daily/self.FT_P104
        
        self.Q_P104 = (self.Q_time/self.TTO_P104)/60

        #Flow correction according the pump datasheet
        if self.Q_P104 < 0.005:
            self.TTO_P104 = (self.Q_time/0.005)/60
            self.Q_P104 = 0.005
            if self.TTO_P104 < 60:
                self.TTO_P104 = 1
                self.FT_P104 = self.FT_P104 - 1
            
        self.Q_P104v = []
        if self.TimeCounterPump_P104<self.TTO_P104*60:
            self.Q_P104 = (self.Q_time/self.TTO_P104)/60 
            if self.tp*self.time_accelerator > self.TTO_P104:
                seconds = int(self.tp*self.time_accelerator)
                for i in range (seconds):
                    if i < self.TTO_P104*60:
                        self.Q_P104v.append(self.Q_P104)
                    else:
                        self.Q_P104v.append(0)
            else:
                self.Q_P104v.append(self.Q_P104)  
        else:
            self.Q_P104= float(0)
            self.Q_P104v.append(0)
        
        self.Q_P104_Lh = self.Q_P104 * 3600
        
        self.TimeCounterPump_P104 = self.TimeCounterPump_P104 + (self.tp * self.time_accelerator)

        if self.TimeCounterPump_P104>=self.TurnOnDailyStep_P104*3600:
            self.TimeCounterPump_P104 = 0
        
    def Pump101 (self, FT_P101=5, TTO_P101=10, Q_P101 = 2.4):
        
        if self.OperationMode == "Modo1":
            self.Q_P101 = 0

        elif self.OperationMode == "Modo2":
            self.FT_P101= FT_P101
            self.TTO_P101 = TTO_P101

            try:
                self.TurnOnDailyStep_P101 = 24/self.FT_P101
            except ZeroDivisionError:
                self.TurnOnDailyStep_P101 = 0


            if self.TimeCounterPump_P101<self.TTO_P101*60:
                self.Q_P101 = Q_P101
            else:
                self.Q_P101= float(0)
            
            self.TimeCounterPump_P101 = self.TimeCounterPump_P101 + self.tp
        
            if self.TimeCounterPump_P101>=self.TurnOnDailyStep_P101*3600:
                self.TimeCounterPump_P101 = 0

        elif self.OperationMode == "Modo3" or self.OperationMode == "Modo5":
            self.Q_P101 = self.Q_P104

        elif self.OperationMode == "Modo4":
            
            try:
                self.Q_P102 = self.Q_P102
            except:
                self.Q_P102 = 0

            self.Q_P101 = self.Q_P104 + self.Q_P102
    
    def Pump102 (self, FT_P102=5, TTO_P102=10, Q_P102 = 2.4): #FT_P102: feeds times per day, TTO_P102: turn on per time, Q_P102: Flow rate [L/h]
        
        if self.OperationMode == "Modo1" or self.OperationMode == "Modo2" or self.OperationMode == "Modo3":
            self.Q_P102 = 0

        elif self.OperationMode == "Modo4" or self.OperationMode == "Modo5":
            self.FT_P102= FT_P102
            self.TTO_P102 = TTO_P102

            try:
                self.TurnOnDailyStep_P102 = 24/self.FT_P102
            except ZeroDivisionError:
                self.TurnOnDailyStep_P102 = 0

            self.Q_P102v = []
            if self.TimeCounterPump_P102<self.TTO_P102*60:
                self.Q_P102 = Q_P102
                if self.tp*self.time_accelerator > self.TTO_P102:
                    seconds = int(self.tp*self.time_accelerator)
                    for i in range (seconds):
                        if i < self.TTO_P102*60:
                            self.Q_P102v.append(self.Q_P102/3600)
                        else:
                            self.Q_P102v.append(0)
                else:
                    self.Q_P102v.append(self.Q_P102)         
            else:
                self.Q_P102= float(0)
                self.Q_P102v.append(0)
            
            self.TimeCounterPump_P102 = self.TimeCounterPump_P102 + self.tp

            if self.TimeCounterPump_P102>=self.TurnOnDailyStep_P102*3600:
                self.TimeCounterPump_P102 = 0

    def Mixing_TK100 (self, FT_mixin_TK100=5, TTO_mixing_TK100 = 10, RPM_TK100 = 50):
        self.FT_mixing_TK100 = FT_mixin_TK100
        self.TTO_mixing_TK100 = TTO_mixing_TK100
        try:
            self.TurnOnDailyStep_Mixing_TK100 = 24/self.FT_mixing_TK100
        except ZeroDivisionError:
            self.TurnOnDailyStep_Mixing_TK100 = 0
        
        if self.TimeCounterMixer_TK100<self.TTO_mixing_TK100*60:
            self.RPM_TK100 = RPM_TK100
        else:
            self.RPM_TK100 = 0
        
        self.TimeCounterMixer_TK100 = self.TimeCounterMixer_TK100 + self.tp

        if self.TimeCounterMixer_TK100>=self.TurnOnDailyStep_Mixing_TK100*3600:
            self.TimeCounterMixer_TK100 = 0
    
    def Mixing_R101 (self, FT_mixin_R101=5, TTO_mixing_R101 = 10, RPM_R101 = 50):
        self.FT_mixing_R101 = FT_mixin_R101
        self.TTO_mixing_R101 = TTO_mixing_R101
        try:
            self.TurnOnDailyStep_Mixing_R101 = 24/self.FT_mixing_R101
        except ZeroDivisionError:
            self.TurnOnDailyStep_Mixing_R101 = 0
        
        if self.TimeCounterMixer_R101<self.TTO_mixing_R101*60:
            self.RPM_R101 = RPM_R101
        else:
            self.RPM_R101 = 0
        
        self.TimeCounterMixer_R101 = self.TimeCounterMixer_R101 + self.tp

        if self.TimeCounterMixer_R101>=self.TurnOnDailyStep_Mixing_R101*3600:
            self.TimeCounterMixer_R101 = 0
    
    def Mixing_R102 (self, FT_mixin_R102=5, TTO_mixing_R102 = 10, RPM_R102 = 50):
        if self.OperationMode in ["Modo1", "Modo2"]:
            self.RPM_R102 = 0
        else:
            self.FT_mixing_R102 = FT_mixin_R102
            self.TTO_mixing_R102 = TTO_mixing_R102
            try:
                self.TurnOnDailyStep_Mixing_R102 = 24/self.FT_mixing_R102
            except ZeroDivisionError:
                self.TurnOnDailyStep_Mixing_R102 = 0
            
            if self.TimeCounterMixer_R102<self.TTO_mixing_R102*60:
                self.RPM_R102 = RPM_R102
            else:
                self.RPM_R102 = 0
            
            self.TimeCounterMixer_R102 = self.TimeCounterMixer_R102 + self.tp

            if self.TimeCounterMixer_R102>=self.TurnOnDailyStep_Mixing_R102*3600:
                self.TimeCounterMixer_R102 = 0
                   
    def Reactor101Simulation_ArrheniusModel (self, Operation, VR, Qin_1, Csus_in1,
                                            K, Ea, T, pH, Qin_2=[0], Csus_in2 = 0.0):
        
        #Operation 1: one inlet, 2: Two inlet
        #VR: Reactor Volume (L)
        #Qin_1: Volumetric Flow rate [L/s], inlet 1
        #Csus_in1: Substrate concentration [mol/L], inlet 1
        #K: Preexponential factor Arrhenius [1/s]
        #Ea: Energy activation, Arrhenius parameter [J/molK]
        #T: Temperature operation [K]
        #pH: pH of the reactor
        #Mix: Mix velocity of the reactor [RPM]         
        #Qin_2: Volumetric Flow rate [L/s], inlet 2
        #Csus_in2: Substrate concentration [mol/L], inlet 2    
        
        def pH_effect (parameter):
            variable = np.exp(-((float(parameter)-7)**2)/(2*5**2))
            return variable
        
        def differential_Equation (C, t):
            R = 8.314
            pH_R = pH_effect(pH)
            if Operation == 1:
                if len(Qin_1)>1:
                    Q1 = np.interp(t, time, Qin_1)
                else:
                    Q1 = Qin_1[-1]
                dCsus_dt = ((Q1/VR) * (Csus_in1 - C)) - ((C * K * np.exp(-(Ea)/(R*(T+273.15)))) / VR)
            elif Operation == 2:
                if len(Qin_1)>1:
                    Q1 = np.interp(t, time, Qin_1)
                    Q2 = np.interp(t, time, Qin_2)
                else:
                    Q1 = Qin_1[-1]
                    Q2 = Qin_2[-1]
                dCsus_dt = (Q1 * Csus_in1)/VR + (Q2 * Csus_in2)/VR - ((Q1+Q2)*C)/VR - (C * K * np.exp(-Ea/(R*(T+273.15)))) / VR
            return dCsus_dt
    
        if len(Qin_1)>1:
            seconds = int(self.tp*self.time_accelerator)
            time = np.linspace(self.GlobalTime, self.GlobalTime + (self.tp*self.time_accelerator), seconds)
            y0 = self.Csus_ini_R101
            Csus_int_i = odeint(differential_Equation, y0, time)
            self.Csus_ini_R101 = float(Csus_int_i[-1])
        else:
            time = [self.GlobalTime, self.GlobalTime + (self.tp*self.time_accelerator)]
            y0 = self.Csus_ini_R101
            Csus_int_i = odeint(differential_Equation, y0, time)
            self.Csus_ini_R101 = float(Csus_int_i[-1])
        
        #Conversion
        self.x_R101 = abs(self.Csus_ini - self.Csus_ini_R101)/self.Csus_ini
        
        #Volatile Solids
        self.SV_R101_p = ((self.Csus_ini_R101 * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)) / (self.rho*self.x_substrate_R101 + self.rho_R101*self.x_inoculum_R101))    #[%]
        self.SV_R101_gl = self.Csus_ini_R101 * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)                     #[gSV/L]
        
        #Total Solids
        self.ST_R101_p = (((self.Csus_ini_R101 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)) / (self.rho*self.x_substrate_R101 + self.rho_R101*self.x_inoculum_R101))
        self.ST_R101_gl = (self.Csus_ini_R101 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)
        
        for i,j in zip(Qin_1, Qin_2):
            self.Vinj_R101 = self.Vinj_R101 + (i * self.tp) + (j * self.tp)
            if self.Vinj_R101 > self.VR1:
                self.x_substrate_R101 = 1
                self.x_inoculum_R101 = 0
            else:
                # Vtotal_R101 =  self.Vinj_R101 + self.VR1
                self.x_substrate_R101 = self.Vinj_R101 / self.VR1
                self.x_inoculum_R101 = (1 - self.x_substrate_R101)
        
        #Organic Charge
        try:
            if self.GlobalTime == 0:
                self.Organic_Charge_R101 = 0                                        #[gSV/L.dia]
            else:
                self.Organic_Charge_R101 =  self.SV_R101_gl/(self.GlobalTime/86400) #[gSV/L.dia]    
        except (ZeroDivisionError, ValueError):
            self.Organic_Charge_R101 = 0
        
        #Expenditure mass of limit reagent
        self.mol_expen_R101 = abs(float(Csus_int_i[0]) - float(Csus_int_i[-1]))   #mol/s
        
        #biogas produced by R101
        self.molCH4_R101 = (self.mol_expen_R101 * self.s_CH4)                     #mol/s        
        self.molCO2_R101 = (self.mol_expen_R101 * self.s_CO2)
        self.molH2S_R101 = (self.mol_expen_R101 * self.s_H2S)
        self.molNH3_R101 = (self.mol_expen_R101 * self.s_NH3)
        self.molH2_R101 = np.random.uniform(0.0001, 0.00015) * self.mol_expen_R101
        self.biogas_R101_dry = self.molCH4_R101 + self.molCO2_R101 + self.molH2S_R101 + self.molNH3_R101
        self.molO2_R101 = np.random.uniform(0.02, 0.05) * self.biogas_R101_dry
        self.biogas_R101_dry = self.molO2_R101 + self.molH2_R101 + self.biogas_R101_dry
        self.molH2O_R101 = np.random.uniform(0.005, 0.01)*self.biogas_R101_dry
        self.biogas_R101_wet = self.biogas_R101_dry + self.molH2O_R101
    
    def Reactor101Simulation_ADM1 (self, Operation, VR, Qin_1, Csus_in1,
                                    K, Qin_2=[0], Csus_in2 = 0.0):
        
        #Operation 1: one inlet, 2: Two inlet
        #VR: Reactor Volume (L)
        #Qin_1: Volumetric Flow rate [L/s], inlet 1
        #Csus_in1: Substrate concentration [mol/L], inlet 1
        #K: Preexponential factor Arrhenius [L/s]        
        #Qin_2: Volumetric Flow rate [L/s], inlet 2
        #Csus_in2: Substrate concentration [mol/L], inlet 2    
        
        def differential_Equation (C, t):
            R = 8.314
            if Operation == 1:
                if len(Qin_1)>1:
                    Q1 = np.interp(t, time, Qin_1)
                else:
                    Q1 = Qin_1[-1]
                dCsus_dt = ((Q1/VR) * (Csus_in1 - C)) - ((C * K) / VR)
            elif Operation == 2:
                if len(Qin_1)>1:
                    Q1 = np.interp(t, time, Qin_1)
                else:
                    Q1 = Qin_1[-1]
                if len(Qin_2)>1:
                    Q2 = np.interp(t, time, Qin_2)
                else:
                    Q2 = Qin_2[-1]
                dCsus_dt = (Q1 * Csus_in1)/VR + (Q2 * Csus_in2)/VR - ((Q1+Q2)*C)/VR - (C * K) / VR
            return dCsus_dt
    
        if len(Qin_1)>1 or len(Qin_2)>1:
            seconds = int(self.tp*self.time_accelerator)
            time = np.linspace(self.GlobalTime, self.GlobalTime + (self.tp*self.time_accelerator), seconds)
            y0 = self.Csus_ini_R101
            Csus_int_i = odeint(differential_Equation, y0, time)
            self.Csus_ini_R101 = float(Csus_int_i[-1])
        else:
            time = [self.GlobalTime, self.GlobalTime + (self.tp*self.time_accelerator)]
            y0 = self.Csus_ini_R101
            Csus_int_i = odeint(differential_Equation, y0, time)
            self.Csus_ini_R101 = float(Csus_int_i[-1])
        
        #Conversion
        self.x_R101 = abs(Csus_in1 - self.Csus_ini_R101)/Csus_in1
        
        #Volatile Solids
        self.SV_R101_p = ((self.Csus_ini_R101 * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)) / (self.rho*self.x_substrate_R101 + self.rho_R101*self.x_inoculum_R101))    #[%]
        self.SV_R101_gl = self.Csus_ini_R101 * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)                     #[gSV/L]
        
        #Total Solids
        self.ST_R101_p = (((self.Csus_ini_R101 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)) / (self.rho*self.x_substrate_R101 + self.rho_R101*self.x_inoculum_R101))
        self.ST_R101_gl = (self.Csus_ini_R101 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)
        
        for i,j in zip(Qin_1, Qin_2):
            self.Vinj_R101 = self.Vinj_R101 + (i * self.tp) + (j * self.tp)
            if self.Vinj_R101 > self.VR1:
                self.x_substrate_R101 = 1
                self.x_inoculum_R101 = 0
            else:
                # Vtotal_R101 =  self.Vinj_R101 + self.VR1
                self.x_substrate_R101 = self.Vinj_R101 / self.VR1
                # self.x_inoculum_R101 = (self.VG1 - self.Vinj_R101) / self.VR1 
                self.x_inoculum_R101 = 1 - self.x_substrate_R101  
        #Organic Charge
        try:
            if self.GlobalTime == 0:
                self.Organic_Charge_R101 = 0                                        #[gSV/L.dia]
            else:
                self.Organic_Charge_R101 =  self.SV_R101_gl/(self.GlobalTime/86400) #[gSV/L.dia]    
        except (ZeroDivisionError, ValueError):
            self.Organic_Charge_R101 = 0
        
        #Expenditure mass of limit reagent
        self.mol_expen_R101 = abs(float(Csus_int_i[0]) - float(Csus_int_i[-1]))   #mol/s
        
        #biogas produced by R101
        self.molCH4_R101 = (self.mol_expen_R101 * self.s_CH4*self.x_substrate_R101)                     #mol/s        
        self.molCO2_R101 = (self.mol_expen_R101 * self.s_CO2*self.x_substrate_R101)
        self.molH2S_R101 = (self.mol_expen_R101 * self.s_H2S*self.x_substrate_R101)
        self.molNH3_R101 = (self.mol_expen_R101 * self.s_NH3*self.x_substrate_R101)
        self.molH2_R101 = np.random.uniform(0.0001, 0.00015) * self.mol_expen_R101
        self.biogas_R101_dry = self.molCH4_R101 + self.molCO2_R101 + self.molH2S_R101 + self.molNH3_R101
        self.molO2_R101 = np.random.uniform(0.02, 0.05) * self.biogas_R101_dry
        self.biogas_R101_dry = self.molO2_R101 + self.molH2_R101 + self.biogas_R101_dry
        self.molH2O_R101 = np.random.uniform(0.004, 0.009)*self.biogas_R101_dry
        self.biogas_R101_wet = self.biogas_R101_dry + self.molH2O_R101
        
    def Reactor101Simulation_Gompertz (self, Operation, ym, U, Lambda, Qin_1, Qin_2 = [0]):
        # ------ function parameters
        # operation: Operation Mode 1: 1 inlet, 2 inlets
        # ym: Biogas production potential [L/gVS]
        # U: Maximum biogas production rate [L/gSV-second]
        # Lambda: lag phase period or minimum time to produce biogas biogas [seconds]
        # Q_in1: FLow rate by P104
        # Q_in2: flow rate by P101
        # y_t = ym*np.exp(np.exp(-((U/ym*self.GlobalTime)+Lambda)))    # Accumulative biogas yield [L/gSV]
        y_t = ym*np.exp(-np.exp(((U*np.e/ym)*(Lambda - (self.GlobalTime/60)))+1))
        
        for i,j in zip(Qin_1, Qin_2):
            self.Vinj_R101 = self.Vinj_R101 + (i * self.tp) + (j * self.tp)
            molinv = []
            if Operation == 1:
                mol_in1 = (i * self.tp * self.Csus_ini)
                mol_in2 = 0
                mol_in = mol_in1 + mol_in2
                mol_out = (i * self.tp * self.Csus_ini_R101)
            elif Operation == 2:
                mol_in1 = (i * self.tp * self.Csus_ini)
                mol_in2 = (j * self.tp * self.Csus_ini_R102)
                mol_in = mol_in1 + mol_in2
                mol_out = ((i + j) * self.tp * self.Csus_ini_R101)
            molinv.append(mol_in)    
            if self.Vinj_R101 > self.VR1:
                self.x_substrate_R101 = 1
                self.x_inoculum_R101 = 0
            else:
                # Vtotal_R101 =  self.Vinj_R101 + self.VR1
                self.x_substrate_R101 = self.Vinj_R101 / self.VR1
                self.x_inoculum_R101 = (1 - self.x_substrate_R101) 
        mol_in = sum(molinv)
        
        #Biogas Volume estimation
        biogas_Normal_volume = y_t * (self.SV_R101/100) * (self.x_substrate_R101*self.rho + self.x_inoculum_R101*self.rho_R101) * self.VR1
        self.rho_R101_out = self.x_substrate_R101*self.rho + self.x_inoculum_R101*self.rho_R101
        biogas_mol_R101 = ((biogas_Normal_volume/1000)*100000)/(8.314*273.15)
        self.Csus_ini_R101 = (self.mol_ini_R101 + mol_in - self.mol_sus_expended_R101 - mol_out)/self.VR1
        self.mol_ini_R101 = self.Csus_ini_R101 * self.VR1
        s_biogas = (self.s_CH4 + self.s_CO2 + self.s_H2S + self.s_NH3)
        biogas_prod = biogas_mol_R101 - self.biogas_mol_R101
        self.biogas_mol_R101 = biogas_mol_R101
        self.mol_sus_expended_R101 = biogas_prod * (1/s_biogas)
        
        
        self.x_R101 = abs(self.Csus_ini - self.Csus_ini_R101)/self.Csus_ini
        self.SV_R101 = ((self.Csus_ini_R101 * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)) / (self.rho*self.x_substrate_R101 + self.rho_R101*self.x_inoculum_R101))*100    #[%]
        
        #Volatile solids
        self.SV_R101_p = (self.SV_R101/3)/100
        self.SV_R101_gl = self.Csus_ini_R101 * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)

        #Total Solids
        self.ST_R101_p = (((self.Csus_ini_R101 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)) / (self.rho*self.x_substrate_R101 + self.rho_R101*self.x_inoculum_R101))
        self.ST_R101_gl = (self.Csus_ini_R101 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R101 + self.MW_sustrato_R101*self.x_inoculum_R101)

        #Organic Charge
        try:
            if self.GlobalTime == 0:
                self.Organic_Charge_R101 = 0                                        #[gSV/L.dia]
            else:
                self.Organic_Charge_R101 =  self.SV_R101_gl/(self.GlobalTime/86400) #[gSV/L.dia]    
        except (ZeroDivisionError, ValueError):
            self.Organic_Charge_R101 = 0

        self.molCH4_R101 = (self.mol_sus_expended_R101 * self.s_CH4)
        self.molCO2_R101 = (self.mol_sus_expended_R101 * self.s_CO2)
        self.molH2S_R101 = (self.mol_sus_expended_R101 * self.s_H2S)
        self.molNH3_R101 = (self.mol_sus_expended_R101 * self.s_NH3)
        self.molO2_R101 = np.random.uniform(0.02, 0.05) * self.mol_sus_expended_R101
        self.molH2_R101 = np.random.uniform(0.0001, 0.00015) * self.mol_sus_expended_R101
        self.molH2O_R101 = np.random.uniform(0.6, 1)* self.mol_sus_expended_R101
        
    def V101_mode1 (self, Pset, Model):
        
        #Accumulated mol of coompounds by the time 
        self.molCH4_acum_V101 = self.molCH4_acum_V101 + self.molCH4_R101                     #accumulated mol (integral)
        self.molCO2_acum_V101 = self.molCO2_acum_V101 + self.molCO2_R101 
        self.molH2S_acum_V101 = self.molH2S_acum_V101 + self.molH2S_R101
        self.molNH3_acum_V101 = self.molNH3_acum_V101 + self.molNH3_R101
        self.molH2O_acum_V101 = self.molH2O_acum_V101 + self.molH2O_R101
        self.molO2_acum_V101 = self.molO2_acum_V101 + self.molO2_R101
        self.molH2_acum_V101 = self.molH2_acum_V101 + self.molH2_R101
        
        self.biogas_acum_V101_dry = self.molCH4_acum_V101 + self.molCO2_acum_V101 + self.molH2S_acum_V101 + self.molNH3_acum_V101 + self.molO2_acum_V101
        self.biogas_acum_V101_wet = self.biogas_acum_V101_dry + self.molH2O_acum_V101

        #Biogas compound Concentration
        try: 
            if self.biogas_acum_V101_dry == 0:
                self.xCH4_V101 = 0
                self.xCO2_V101 = 0
                self.xH2S_V101 = 0
                self.xNH3_V101 = 0
                self.xH2O_V101 = 0
                self.xO2_V101 = 0
                self.xH2_V101 = 0
            else:
                self.xCH4_V101_wet = self.molCH4_acum_V101/self.biogas_acum_V101_wet
                self.xCO2_V101_wet = self.molCO2_acum_V101/self.biogas_acum_V101_wet
                self.xH2S_V101_wet = self.molH2S_acum_V101/self.biogas_acum_V101_wet
                self.xNH3_V101_wet = self.molNH3_acum_V101/self.biogas_acum_V101_wet
                self.xH2O_V101_wet = self.molH2O_acum_V101/self.biogas_acum_V101_wet
                self.xO2_V101_wet = self.molO2_acum_V101/self.biogas_acum_V101_wet
                self.xH2_V101_wet = self.molH2_acum_V101/self.biogas_acum_V101_wet
                
                self.xCH4_V101 = self.molCH4_acum_V101/self.biogas_acum_V101_dry
                self.xCO2_V101 = self.molCO2_acum_V101/self.biogas_acum_V101_dry
                self.xH2S_V101 = self.molH2S_acum_V101/self.biogas_acum_V101_dry
                self.xNH3_V101 = self.molNH3_acum_V101/self.biogas_acum_V101_dry
                self.xH2O_V101 = self.molH2O_acum_V101/self.biogas_acum_V101_wet
                self.xO2_V101 = self.molO2_acum_V101/self.biogas_acum_V101_dry
                self.xH2_V101 = self.molH2_acum_V101/self.biogas_acum_V101_dry
        except ZeroDivisionError:
            self.xCH4_V101 = 0
            self.xCO2_V101 = 0
            self.xH2S_V101 = 0
            self.xNH3_V101 = 0
            self.xH2O_V101 = 0
            self.xO2_V101 = 0
            self.xH2_V101 = 0
        
        #Preddure estimation 
        # Get temperature from API
        # lat = 3.40330   
        # lon = -76.54708  
        # api_key = "cd9cc586c0098f719bf013730d2d081e"
        # url =   f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        # response = requests.get(url)
           
        # if response.status_code == 200:
        #     self.Temperature = response.json()['main']['temp']
        # else:
        #   self.Temperature = np.random.normal(25, 5)
        self.Temperature = np.random.normal(25, 1)

        p_i = (((self.biogas_acum_V101_wet * 8.314 * (self.Temperature+273.15))/(self.VG1/1000))/6894.76) - self.Pacum_V101 
        if self.Pacum_V101 < Pset:
            self.Pstorage_V101 = self.Pacum_V101
        else:
            self.Pstorage_V101 = p_i + self.Pstorage_V101                                                                   #psig
        self.Pacum_V101 = ((self.biogas_acum_V101_wet * 8.314 * (self.Temperature+273.15))/(self.VG1/1000))/6894.76     #psig
        #Storage biogas moles
        self.biogas_storage_mol_V101 = ((self.Pstorage_V101*6894.76) * (self.VG1/1000))/(8.314*(self.Temperature+273.15))               #mol
        
        #Standard volume estimation for storage and accumulated biogas
        #Standard conditions
        self.Tstd = 273.15            #[K]
        self.Pstd = 14.5038           #[Psi]  
        #Standard volume estimation for accumulated biogas
        self.Vacum_std_V101 = (self.Pacum_V101*self.VG1*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        #Standard colume estimation for storage biogas
        self.Vstorage_std_V101 = (self.Pstorage_V101*self.VG1*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        
        #Accumulated volume of compounds by the time
        self.Vol_esp_CH4 = self.thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_CO2 = self.thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_O2 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2S = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_NH3 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V101, Patm=100, T=self.Temperature, xNH3=1)[2]
        self.Vol_acum_CH4_V101 = self.Vol_esp_CH4 * self.molCH4_acum_V101
        self.Vol_acum_CO2_V101 = self.Vol_esp_CO2 * self.molCO2_acum_V101
        self.Vol_acum_O2_V101 = self.Vol_esp_O2 * self.molO2_acum_V101
        self.Vol_acum_H2S_V101 = self.Vol_esp_H2S * self.molH2S_acum_V101
        self.Vol_acum_H2_V101 = self.Vol_esp_H2 * self.molH2_acum_V101
        self.Vol_acum_NH3_V101 = self.Vol_esp_NH3 * self.molNH3_acum_V101 
        
        #Relative Humidity estimation
        self.RH_V101 = self.thermo.BiogasRelativeHumidity(nH2O=self.biogas_storage_mol_V101*self.xH2O_V101, VnormalTotal=self.Vstorage_std_V101/1000, T=self.Temperature, P=self.Pstorage_V101)

        #Energy storage
        self.Energy_V101 = self.thermo.LHV(molCH4=self.molCH4_acum_V101, molCO2=self.molCO2_acum_V101, molH2S=self.molH2S_acum_V101,
                                           molO2=self.molO2_acum_V101, molH2=self.molH2_acum_V101)[1]

        #Pressure control
        if self.Pstorage_V101 > Pset:
            P_storage_V101_pres = ((self.biogas_storage_mol_V101 *8.314 * (self.Temperature+273.15)) / ((self.VG1)/1000))/6894.76   #pressure before trnasfer
            self.Pstorage_V101 = (((self.biogas_storage_mol_V101+self.biogas_storage_mol_V102) * 8.314 * (self.Temperature+273.15))/((self.VG1 + self. VG2)/1000))/6894.76      #equilibrium pressure between V101 and V102
            # if self.Pstorage_V102 == 0:
            #     self.Pstorage_V102 = self.Pstorage_V101
            #     print(self.Pstorage_V102)
            self.biogasmol_storage_V101 = ((self.Pstorage_V101*6894.76) * ((self.VG1)/1000))/(8.314*(self.Temperature+273.15)) 
            biogasmol_storage_V101_pres = ((P_storage_V101_pres*6894.76) * ((self.VG1)/1000))/(8.314*(self.Temperature+273.15))
 
            self.mol_CH4_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xCH4_V101_wet
            self.mol_CO2_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xCO2_V101_wet
            self.mol_O2_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xO2_V101_wet
            self.mol_H2S_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xH2S_V101_wet
            self.mol_NH3_transferToV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xNH3_V101_wet
            self.mol_H2O_transfertoV102 = (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xH2O_V101_wet
            self.mol_H2_transfertoV102 =  (biogasmol_storage_V101_pres - self.biogasmol_storage_V101)*self.xH2_V101_wet                                                 
        else:
            self.mol_CH4_transferToV102 = 0
            self.mol_CO2_transferToV102 = 0
            self.mol_O2_transferToV102 =  0
            self.mol_H2S_transferToV102 = 0
            self.mol_NH3_transferToV102 = 0
            self.mol_H2O_transfertoV102 = 0
            self.mol_H2_transfertoV102 = 0
            
    def V102_mode1 (self, Pset):
        self.molCH4_acum_V102 = self.molCH4_acum_V102 + self.mol_CH4_transferToV102
        self.molCO2_acum_V102 = self.molCO2_acum_V102 + self.mol_CO2_transferToV102
        self.molO2_acum_V102 = self.molO2_acum_V102 + self.mol_O2_transferToV102
        self.molH2O_acum_V102 = self.molH2O_acum_V102 + self.mol_H2O_transfertoV102
        self.molH2S_acum_V102 = self.molH2S_acum_V102 + self.mol_H2S_transferToV102 
        self.molNH3_acum_V102 = self.molNH3_acum_V102 + self.mol_NH3_transferToV102
        self.molH2_acum_V102 = self.molH2_acum_V102 + self.mol_H2_transfertoV102
        self.biogas_acum_V102_dry = self.molCH4_acum_V102 + self.molCO2_acum_V102 + self.molH2S_acum_V102 + self.molNH3_acum_V102 + self.molO2_acum_V102
        self.biogas_acum_V102_wet = self.biogas_acum_V102_dry + self.molH2O_acum_V102
        
        #Biogas compound Concentration
        try:
            if self.biogas_acum_V102_dry == 0:
                self.xCH4_V102 = 0
                self.xCO2_V102 = 0
                self.xH2S_V102 = 0
                self.xNH3_V102 = 0
                self.xH2O_V102 = 0
                self.xO2_V102 = 0
                self.xH2_V102 = 0
            else:
                self.xCH4_V102_wet = self.molCH4_acum_V102/self.biogas_acum_V102_wet
                self.xCO2_V102_wet = self.molCO2_acum_V102/self.biogas_acum_V102_wet
                self.xH2S_V102_wet = self.molH2S_acum_V102/self.biogas_acum_V102_wet
                self.xNH3_V102_wet = self.molNH3_acum_V102/self.biogas_acum_V102_wet
                self.xH2O_V102_wet = self.molH2O_acum_V102/self.biogas_acum_V102_wet
                self.xO2_V102_wet = self.molO2_acum_V102/self.biogas_acum_V102_wet
                self.xH2_V102_wet = self.molH2_acum_V102/self.biogas_acum_V102_wet
                
                self.xCH4_V102 = self.molCH4_acum_V102/self.biogas_acum_V102_dry
                self.xCO2_V102 = self.molCO2_acum_V102/self.biogas_acum_V102_dry
                self.xH2S_V102 = self.molH2S_acum_V102/self.biogas_acum_V102_dry
                self.xNH3_V102 = self.molNH3_acum_V102/self.biogas_acum_V102_dry
                self.xH2O_V102 = self.molH2O_acum_V102/self.biogas_acum_V102_wet
                self.xO2_V102 = self.molO2_acum_V102/self.biogas_acum_V102_dry
                self.xH2_V102 = self.molH2_acum_V102/self.biogas_acum_V102_dry
        except ZeroDivisionError:
                self.xCH4_V102 = 0
                self.xCO2_V102 = 0
                self.xH2S_V102 = 0
                self.xNH3_V102 = 0
                self.xH2O_V102 = 0
                self.xO2_V102 = 0
                self.xH2_V102 = 0

        p_i = ((self.biogas_acum_V102_wet * 8.314 * (self.Temperature+273.15))/((self.VG2)/1000))/6894.76 - self.Pacum_V102
        self.Pstorage_V102 = p_i + self.Pstorage_V102
        self.Pacum_V102 = ((self.biogas_acum_V102_wet * 8.314 * (self.Temperature+273.15))/((self.VG2)/1000))/6894.76
        
        #Storage biogas moles
        self.biogas_storage_mol_V102 = ((self.Pstorage_V102*6894.76) * (self.VG2/1000))/(8.314*(self.Temperature+273.15))

        #Standard volume estimation for storage and accumulated biogas
        #Standard volume estimation for accumulated biogas
        self.Vacum_std_V102 = (self.Pacum_V102*self.VG2*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        #Standard Volume estimation for storage biogas
        self.Vstorage_std_V102 = (self.Pstorage_V102*self.VG2*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        
        #Accumulated volume of compounds by the time
        self.Vol_esp_CH4_V102 = self.thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_CO2_V102 = self.thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_O2_V102 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2S_V102 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2_V102 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_NH3_V102 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=1)[2]
        self.Vol_acum_CH4_V102 = self.Vol_esp_CH4_V102 * self.molCH4_acum_V102
        self.Vol_acum_CO2_V102 = self.Vol_esp_CO2_V102 * self.molCO2_acum_V102
        self.Vol_acum_O2_V102 = self.Vol_esp_O2_V102 * self.molO2_acum_V102
        self.Vol_acum_H2S_V102 = self.Vol_esp_H2S_V102 * self.molH2S_acum_V102
        self.Vol_acum_H2_V102 = self.Vol_esp_H2_V102 * self.molH2_acum_V102
        self.Vol_acum_NH3_V102 = self.Vol_esp_NH3_V102 * self.molNH3_acum_V102 
        
        #Energy storage
        self.Energy_V102 = self.thermo.LHV(molCH4=self.molCH4_acum_V102, molCO2=self.molCO2_acum_V102, molH2S=self.molH2S_acum_V102,
                                           molO2=self.molO2_acum_V102, molH2=self.molH2_acum_V102)[1]

        #Relative Humidity estimation
        self.RH_V102 = self.thermo.BiogasRelativeHumidity(nH2O=self.biogas_storage_mol_V102 * self.xH2O_V102, VnormalTotal=self.Vstorage_std_V102/1000, T=self.Temperature, P=self.Pstorage_V102)
        
        #Pressure control
        if self.Pstorage_V102 > Pset:
            P_storage_V102_pres = ((self.biogas_storage_mol_V102 *8.314 * (self.Temperature+273.15)) / ((self.VG2)/1000))/6894.76   #pressure before trnasfer
            self.Pstorage_V102 = (((self.biogas_storage_mol_V102 + self.biogas_storage_mol_V107) * 8.314 * (self.Temperature+273.15))/((self.VG3 + self.VG2)/1000))/6894.76      #equilibrium pressure between V102 and V102  
            # if self.Pstorage_V107 != 0:
            #     self.Pstorage_V107 = self.Pstorage_V102
            
            self.biogasmol_storage_V102= ((self.Pstorage_V102*6894.76) * ((self.VG2)/1000))/(8.314*(self.Temperature+273.15))                 #mol trnasfer since V102 to V102
            biogasmol_storage_V102_pres = ((P_storage_V102_pres*6894.76) * ((self.VG2)/1000))/(8.314*(self.Temperature+273.15)) 

            self.mol_CH4_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xCH4_V102_wet
            self.mol_CO2_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xCO2_V102_wet
            self.mol_O2_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xO2_V102_wet
            self.mol_H2S_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2S_V102_wet
            self.mol_NH3_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xNH3_V102_wet
            self.mol_H2O_transfertoV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2O_V102_wet
            self.mol_H2_transfertoV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2_V102_wet
            
        else:
            self.mol_CH4_transferToV107 = 0
            self.mol_CO2_transferToV107 = 0
            self.mol_O2_transferToV107 =  0
            self.mol_H2S_transferToV107 = 0
            self.mol_NH3_transferToV107 = 0
            self.mol_H2O_transfertoV107 = 0
            self.mol_H2_transfertoV107 = 0
            
    def V107_mode1(self, Pset, Pmin = 0):
        self.molCH4_acum_V107 = self.molCH4_acum_V107 + self.mol_CH4_transferToV107
        self.molCO2_acum_V107 = self.molCO2_acum_V107 + self.mol_CO2_transferToV107
        self.molO2_acum_V107 = self.molO2_acum_V107 + self.mol_O2_transferToV107
        self.molH2O_acum_V107 = self.molH2O_acum_V107 + self.mol_H2O_transfertoV107
        self.molH2S_acum_V107 = self.molH2S_acum_V107 + self.mol_H2S_transferToV107 
        self.molNH3_acum_V107 = self.molNH3_acum_V107 + self.mol_NH3_transferToV107
        self.molH2_acum_V107 = self.molH2_acum_V107 + self.mol_H2_transfertoV107
        self.biogas_acum_V107_dry = self.molCH4_acum_V107 + self.molCO2_acum_V107 + self.molH2S_acum_V107 + self.molNH3_acum_V107 + self.molO2_acum_V107
        self.biogas_acum_V107_wet = self.biogas_acum_V107_dry + self.molH2O_acum_V107

        #Biogas compound Concentration
        try:
            if self.biogas_acum_V101_dry == 0:
                self.xCH4_V107 = 0
                self.xCO2_V107 = 0
                self.xH2S_V107 = 0
                self.xNH3_V107 = 0
                self.xH2O_V107 = 0
                self.xO2_V107 = 0
                self.xH2_V107 = 0
            else:
                self.xCH4_V107_wet = self.molCH4_acum_V107/self.biogas_acum_V107_wet
                self.xCO2_V107_wet = self.molCO2_acum_V107/self.biogas_acum_V107_wet
                self.xH2S_V107_wet = self.molH2S_acum_V107/self.biogas_acum_V107_wet
                self.xNH3_V107_wet = self.molNH3_acum_V107/self.biogas_acum_V107_wet
                self.xH2O_V107_wet = self.molH2O_acum_V107/self.biogas_acum_V107_wet
                self.xO2_V107_wet = self.molO2_acum_V107/self.biogas_acum_V107_wet
                
                self.xCH4_V107 = self.molCH4_acum_V107/self.biogas_acum_V107_dry
                self.xCO2_V107 = self.molCO2_acum_V107/self.biogas_acum_V107_dry
                self.xH2S_V107 = self.molH2S_acum_V107/self.biogas_acum_V107_dry
                self.xNH3_V107 = self.molNH3_acum_V107/self.biogas_acum_V107_dry
                self.xH2O_V107 = self.molH2O_acum_V107/self.biogas_acum_V107_wet
                self.xO2_V107 = self.molO2_acum_V107/self.biogas_acum_V107_dry  
                self.xH2_V107 = self.molH2_acum_V107/self.biogas_acum_V107_dry    
        except ZeroDivisionError:
            self.xCH4_V107 = 0
            self.xCO2_V107 = 0
            self.xH2S_V107 = 0
            self.xNH3_V107 = 0
            self.xH2O_V107 = 0
            self.xO2_V107 = 0
            self.xH2_V107 = 0
            
        p_i = (((self.biogas_acum_V107_wet * 8.314 * (self.Temperature+273.15))/((self.VG3)/1000))/6894.76) - self.Pacum_V107
        self.Pstorage_V107 = p_i + self.Pstorage_V107
        self.Pacum_V107 = ((self.biogas_acum_V107_wet * 8.314 * (self.Temperature+273.15))/((self.VG3)/1000))/6894.76        
        
        #Storage biogas moles
        self.biogas_storage_mol_V107 = ((self.Pstorage_V107*6894.76) * (self.VG3/1000))/(8.314*(self.Temperature+273.15))

        #Standard volume estimation for storage and accumulated biogas
        #Standard volume estimation for accumulated biogas
        self.Vacum_std_V107 = (self.Pacum_V107*self.VG3*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        #Standard colume estimation for storage biogas
        self.Vstorage_std_V107 = (self.Pstorage_V107*self.VG3*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        
        #Accumulated volume of compounds by the time
        self.Vol_esp_CH4_V107 = self.thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_CO2_V107 = self.thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_O2_V107 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2S_V107 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2_V107 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_NH3_V107 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V107, Patm=100, T=self.Temperature, xNH3=1)[2]
        self.Vol_acum_CH4_V107 = self.Vol_esp_CH4_V107 * self.molCH4_acum_V107
        self.Vol_acum_CO2_V107 = self.Vol_esp_CO2_V107 * self.molCO2_acum_V107
        self.Vol_acum_O2_V107 = self.Vol_esp_O2_V107 * self.molO2_acum_V107
        self.Vol_acum_H2S_V107 = self.Vol_esp_H2S_V107 * self.molH2S_acum_V107
        self.Vol_acum_H2_V107 = self.Vol_esp_H2_V107 * self.molH2_acum_V107
        self.Vol_acum_NH3_V107 = self.Vol_esp_NH3_V107 * self.molNH3_acum_V107
        
        #Energy storage
        self.Energy_V107 = self.thermo.LHV(molCH4=self.molCH4_acum_V107, molCO2=self.molCO2_acum_V107, molH2S=self.molH2S_acum_V107,
                                           molO2=self.molO2_acum_V107, molH2=self.molH2_acum_V107)[1]
 
        #Relative Humidity estimation
        self.RH_V107 = self.thermo.BiogasRelativeHumidity(nH2O=self.molH2O_acum_V107, VnormalTotal=self.Vacum_std_V107/1000, T=self.Temperature, P=self.Pstorage_V107)
        
        #Pressure control
        if self.Pstorage_V107 > Pset:
            self.biogas_transferToEnv = ((self.Pstorage_V107*6894.76) * (self.VG3/1000))/(8.314*(self.Temperature+273.15))                 #mol trnasfer since V102 to V102
            self.mol_CH4_transferToEnv = self.biogas_transferToEnv*self.xCH4_V107
            self.mol_CO2_transferToEnv = self.biogas_transferToEnv*self.xCO2_V107
            self.mol_O2_transferToEnv = self.biogas_transferToEnv*self.xO2_V107
            self.mol_H2S_transferToEnv = self.biogas_transferToEnv*self.xH2S_V107
            self.mol_NH3_transferToEnv = self.biogas_transferToEnv*self.xNH3_V107
            self.mol_H2O_transfertoEnv = self.biogas_transferToEnv*self.xH2O_V107
            self.Pstorage_V107 = Pmin 
             
        else:
            self.mol_CH4_transferToEnv = 0
            self.mol_CO2_transferToEnv = 0
            self.mol_O2_transferToEnv =  0
            self.mol_H2S_transferToEnv = 0
            self.mol_NH3_transferToEnv = 0
            self.mol_H2O_transfertoEnv = 0
            self.mol_H2_transfertoEnv = 0

    def biogas_treatment_model1 (self, W_fe2O3, K_H2S, K_NH3, K_H2O, w_carbon = 1.0, w_silica = 1.0, qmax_H2S = 0.0188,
                                 qmax_NH3 = 0.1, qmax_H2O = 0.1, k2_H2O = 0.1, k2_NH3 = 0.1, k2_H2S = 0.1): #w in grams, qmax = [mol/g]
        #-------H2S--------
        q_H2S = (qmax_H2S * K_H2S * (self.Pacum_V107*self.xH2S_V107_wet))/(1+(K_H2S*self.Pacum_V107*self.xH2S_V107_wet))
        self.mol_H2S_ads_acum_i = self.mol_H2S_ads_acum
        self.mol_H2S_ads_acum = W_fe2O3 * (q_H2S**2 * k2_H2S * self.GlobalTime)/(1+q_H2S*k2_H2S*self.GlobalTime)
        # self.mol_H2S_ads_acum = q_H2S * W_fe2O3
        self.mol_H2S_transferToV107_i = self.mol_H2S_ads_acum - self.mol_H2S_ads_acum_i
        self.molH2S_acum_V107_i = self.molH2S_acum_V107_i + self.mol_H2S_transferToV107_i 
        
        #------NH3---------
        q_NH3 = (qmax_NH3 * K_NH3 * (self.Pacum_V107*self.xNH3_V107_wet))/(1+(K_NH3*self.Pacum_V107*self.xNH3_V107_wet))
        self.mol_NH3_ads_acum_i = self.mol_NH3_ads_acum
        self.mol_NH3_ads_acum = w_carbon * (q_NH3**2 * k2_NH3 * self.GlobalTime)/(1+q_NH3*k2_NH3*self.GlobalTime)
        # self.mol_NH3_ads_acum = q_NH3 * w_carbon
        self.mol_NH3_transferToV107_i = self.mol_NH3_ads_acum - self.mol_NH3_ads_acum_i
        self.molNH3_acum_V107_i = self.molNH3_acum_V107_i + self.mol_NH3_transferToV107_i
        
        #------H2O-------- 
        q_H2O = (qmax_H2O * K_H2O * (self.Pacum_V107*self.xH2O_V107_wet))/(1+(K_H2O+self.Pacum_V107*self.xH2O_V107_wet))
        self.mol_H2O_ads_acum_i = self.mol_H2O_ads_acum
        self.mol_H2O_ads_acum = w_silica * (q_H2O**2 * k2_H2O * self.GlobalTime)/(1+q_H2O*k2_H2O*self.GlobalTime)
        # self.mol_H2O_ads_acum = q_H2O * w_silica
        self.mol_H2O_transfertoV107_i = self.mol_H2O_ads_acum - self.mol_H2O_ads_acum_i 
        self.molH2O_acum_V107_i = self.molH2O_acum_V107_i + self.mol_H2O_transfertoV107_i
        
        try:
            if self.biogas_acum_V107_wet == 0:
                x_H2O_V107 = 0
            else:
                x_H2O_V107 = self.molH2O_acum_V107_i/self.biogas_acum_V107_wet
        except ZeroDivisionError:
            x_H2O_V107 = 0
        
        self.RH_V107 = self.thermo.BiogasRelativeHumidity(nH2O=self.biogas_storage_mol_V107*x_H2O_V107, VnormalTotal=self.Vstorage_std_V107/1000, T=self.Temperature, P=self.Pstorage_V107)
                       
        #Adsorptia percentage
        if (self.molH2S_acum_V101 + self.molH2S_acum_V102) > self.molH2S_acum_V107:
            self.x_H2S_ads = ((self.molH2S_acum_V101 + self.molH2S_acum_V102)-self.molH2S_acum_V107)/(self.molH2S_acum_V101 + self.molH2S_acum_V102)
        else: 
            self.x_H2S_ads = 0
        
        if (self.molNH3_acum_V101 + self.molNH3_acum_V102) > self.molNH3_acum_V107:
            self.x_NH3_ads = ((self.molNH3_acum_V101 + self.molNH3_acum_V102)-self.molNH3_acum_V107)/(self.molNH3_acum_V101 + self.molNH3_acum_V102)
        else: 
            self.x_NH3_ads = 0
        
        if (self.molH2O_acum_V101 + self.molH2O_acum_V102) > self.molH2O_acum_V107:
            self.x_H2O_ads = ((self.molH2O_acum_V101 + self.molH2O_acum_V102)-self.molH2O_acum_V107)/(self.molH2O_acum_V101 + self.molH2O_acum_V102)
        else: 
            self.x_H2O_ads = 0
        
        self.Xglobal = (self.x_H2S_ads + self.x_NH3_ads + self.x_H2O_ads)/3 
    
    def Reactor102Simulation_ArrheniusModel (self, Operation, VR, Qin_1, Csus_in1,
                                            K, Ea, T, pH, Qin_2=[0], Csus_in2 = 0.0):
        
        #Operation 1: one inlet, 2: Two inlet
        #VR: Reactor Volume (L)
        #Qin_1: Volumetric Flow rate [L/s], inlet 1
        #Csus_in1: Substrate concentration [mol/L], inlet 1
        #K: Preexponential factor Arrhenius [1/s]
        #Ea: Energy activation, Arrhenius parameter [J/molK]
        #T: Temperature operation [K]
        #pH: pH of the reactor
        #Mix: Mix velocity of the reactor [RPM]         
        #Qin_2: Volumetric Flow rate [L/s], inlet 2
        #Csus_in2: Substrate concentration [mol/L], inlet 2    
        
        def pH_effect (parameter):
            variable = np.exp(-((float(parameter)-7)**2)/(2*5**2))
            return variable
        
        def differential_Equation (C, t):
            R = 8.314
            pH_R = pH_effect(pH)
            if Operation == 1:
                if len(Qin_1)>1:
                    Q1 = np.interp(t, time, Qin_1)
                else:
                    Q1 = Qin_1[-1]
                dCsus_dt = ((Q1/VR) * (Csus_in1 - C)) - ((C * K * np.exp(-(Ea)/(R*T))) / VR)
            elif Operation == 2:
                if len(Qin_1)>1:
                    Q1 = np.interp(t, time, Qin_1)
                    Q2 = np.interp(t, time, Qin_2)
                else:
                    Q1 = Qin_1[-1]
                    Q2 = Qin_2[-1]
                dCsus_dt = (Q1 * Csus_in1)/VR + (Q2 * Csus_in2)/VR - ((Q1+Q2)*C)/VR - (C * K * np.exp(-Ea/(R*T))) / VR
            return dCsus_dt
    
        if len(Qin_1)>1:
            seconds = int(self.tp*self.time_accelerator)
            time = np.linspace(self.GlobalTime, self.GlobalTime + (self.tp*self.time_accelerator), seconds)
            y0 = self.Csus_ini_R102
            Csus_int_i = odeint(differential_Equation, y0, time)
            self.Csus_ini_R102 = float(Csus_int_i[-1])
        else:
            time = [self.GlobalTime, self.GlobalTime + (self.tp*self.time_accelerator)]
            y0 = self.Csus_ini_R102
            Csus_int_i = odeint(differential_Equation, y0, time)
            self.Csus_ini_R102 = float(Csus_int_i[-1])
        
        #Conversion
        self.x_R102 = abs(self.Csus_ini_R101 - self.Csus_ini_R102)/self.Csus_ini_R101
        
        #Volatile Solids
        self.SV_R102_p = ((self.Csus_ini_R102 * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)) / (self.rho*self.x_substrate_R102 + self.rho_R102*self.x_inoculum_R102))    #[%]
        self.SV_R102_gl = self.Csus_ini_R102 * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)                     #[gSV/L]
        
        #Total Solids
        self.ST_R102_p = (((self.Csus_ini_R102 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)) / (self.rho*self.x_substrate_R102 + self.rho_R102*self.x_inoculum_R102))
        self.ST_R102_gl = (self.Csus_ini_R102 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)
        
        for i,j in zip(Qin_1, Qin_2):
            self.Vinj_R102 = self.Vinj_R102 + (i * self.tp) + (j * self.tp)
            if self.Vinj_R102 > self.VR2:
                self.x_substrate_R102 = 1
                self.x_inoculum_R102 = 0
            else:
                # Vtotal_R102 =  self.Vinj_R102 + self.VR1
                self.x_substrate_R102 = self.Vinj_R102 / self.VR2
                self.x_inoculum_R102 = (1 - self.x_substrate_R102)
        
        #Organic Charge
        try:
            if self.GlobalTime == 0:
                self.Organic_Charge_R102 = 0                                        #[gSV/L.dia]
            else:
                self.Organic_Charge_R102 =  self.SV_R102_gl/(self.GlobalTime/86400) #[gSV/L.dia]    
        except (ZeroDivisionError, ValueError):
            self.Organic_Charge_R102 = 0
        
        #Expenditure mass of limit reagent
        self.mol_expen_R102 = abs(float(Csus_int_i[0]) - float(Csus_int_i[-1]))   #mol/s
        
        #biogas produced by R102
        self.molCH4_R102 = (self.mol_expen_R102 * self.s_CH4)                     #mol/s        
        self.molCO2_R102 = (self.mol_expen_R102 * self.s_CO2)
        self.molH2S_R102 = (self.mol_expen_R102 * self.s_H2S)
        self.molNH3_R102 = (self.mol_expen_R102 * self.s_NH3)
        self.molH2_R102 = np.random.uniform(0.0001, 0.00015) * self.mol_expen_R102
        self.biogas_R102_dry = self.molCH4_R102 + self.molCO2_R102 + self.molH2S_R102 + self.molNH3_R102
        self.molO2_R102 = np.random.uniform(0.02, 0.05) * self.biogas_R102_dry
        self.biogas_R102_dry = self.molO2_R102 + self.molH2_R102 + self.biogas_R102_dry
        self.molH2O_R102 = np.random.uniform(0.01, 0.015)*self.biogas_R102_dry
        self.biogas_R102_wet = self.biogas_R102_dry + self.molH2O_R102
    
    def Reactor102Simulation_ADM1 (self, Operation, VR, Qin_1, Csus_in1,
                                    K, Qin_2=[0], Csus_in2 = 0.0):
        
        #Operation 1: one inlet, 2: Two inlet
        #VR: Reactor Volume (L)
        #Qin_1: Volumetric Flow rate [L/s], inlet 1
        #Csus_in1: Substrate concentration [mol/L], inlet 1
        #K: Preexponential factor Arrhenius [L/s]        
        #Qin_2: Volumetric Flow rate [L/s], inlet 2
        #Csus_in2: Substrate concentration [mol/L], inlet 2    
        
        def differential_Equation (C, t):
            R = 8.314
            if Operation == 1:
                if len(Qin_1)>1:
                    Q1 = np.interp(t, time, Qin_1)
                else:
                    Q1 = Qin_1[-1]
                dCsus_dt = ((Q1/VR) * (Csus_in1 - C)) - ((C * K) / VR)
            elif Operation == 2:
                if len(Qin_1)>1:
                    Q1 = np.interp(t, time, Qin_1)
                else:
                    Q1 = Qin_1[-1]
                if len(Qin_2)>1:
                    Q2 = np.interp(t, time, Qin_2)
                else:
                    Q2 = Qin_2[-1]
                dCsus_dt = (Q1 * Csus_in1)/VR + (Q2 * Csus_in2)/VR - ((Q1+Q2)*C)/VR - (C * K) / VR
            return dCsus_dt
    
        if len(Qin_1)>1:
            seconds = int(self.tp*self.time_accelerator)
            time = np.linspace(self.GlobalTime, self.GlobalTime + (self.tp*self.time_accelerator), seconds)
            y0 = self.Csus_ini_R102
            Csus_int_i = odeint(differential_Equation, y0, time)
            self.Csus_ini_R102 = float(Csus_int_i[-1])
        else:
            time = [self.GlobalTime, self.GlobalTime + (self.tp*self.time_accelerator)]
            y0 = self.Csus_ini_R102
            Csus_int_i = odeint(differential_Equation, y0, time)
            self.Csus_ini_R102 = float(Csus_int_i[-1])
        
        #Conversion
        self.x_R102 = abs(self.Csus_ini_R101 - self.Csus_ini_R102)/self.Csus_ini_R101
        
        #Volatile Solids
        self.SV_R102_p = ((self.Csus_ini_R102 * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)) / (self.rho*self.x_substrate_R102 + self.rho_R102*self.x_inoculum_R102))    #[%]
        self.SV_R102_gl = self.Csus_ini_R102 * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)                     #[gSV/L]
        
        #Total Solids
        self.ST_R102_p = (((self.Csus_ini_R102 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)) / (self.rho*self.x_substrate_R102 + self.rho_R102*self.x_inoculum_R102))
        self.ST_R102_gl = (self.Csus_ini_R102 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)
        
        for i,j in zip(Qin_1, Qin_2):
            self.Vinj_R102 = self.Vinj_R102 + (i * self.tp) + (j * self.tp)
            if self.Vinj_R102 > self.VR1:
                self.x_substrate_R102 = 1
                self.x_inoculum_R102 = 0
            else:
                # Vtotal_R102 =  self.Vinj_R102 + self.VR1
                self.x_substrate_R102 = self.Vinj_R102 / self.VR2
                # self.x_inoculum_R101 = (self.VG1 - self.Vinj_R101) / self.VR1 
                self.x_inoculum_R102 = 1 - self.x_substrate_R102  
        #Organic Charge
        try:
            if self.GlobalTime == 0:
                self.Organic_Charge_R102 = 0                                        #[gSV/L.dia]
            else:
                self.Organic_Charge_R102 =  self.SV_R102_gl/(self.GlobalTime/86400) #[gSV/L.dia]    
        except (ZeroDivisionError, ValueError):
            self.Organic_Charge_R102 = 0
        
        #Expenditure mass of limit reagent
        self.mol_expen_R102 = abs(float(Csus_int_i[0]) - float(Csus_int_i[-1]))   #mol/s
        
        #biogas produced by R102
        self.molCH4_R102 = (self.mol_expen_R102 * self.s_CH4*self.x_substrate_R102)                     #mol/s        
        self.molCO2_R102 = (self.mol_expen_R102 * self.s_CO2*self.x_substrate_R102)
        self.molH2S_R102 = (self.mol_expen_R102 * self.s_H2S*self.x_substrate_R102)
        self.molNH3_R102 = (self.mol_expen_R102 * self.s_NH3*self.x_substrate_R102)
        self.molH2_R102 = np.random.uniform(0.0001, 0.00015) * self.mol_expen_R102
        self.biogas_R102_dry = self.molCH4_R102 + self.molCO2_R102 + self.molH2S_R102 + self.molNH3_R102
        self.molO2_R102 = np.random.uniform(0.02, 0.05) * self.biogas_R102_dry
        self.biogas_R102_dry = self.molO2_R102 + self.molH2_R102 + self.biogas_R102_dry
        self.molH2O_R102 = np.random.uniform(0.004, 0.009)*self.biogas_R102_dry
        self.biogas_R102_wet = self.biogas_R102_dry + self.molH2O_R102
    
    def Reactor102Simulation_Gompertz (self, Operation, ym, U, Lambda, Qin_1, Qin_2 = [0]):
        # ------ function parameters
        # operation: Operation Mode 1: 1 inlet, 2 inlets
        # ym: Biogas production potential [L/gVS]
        # U: Maximum biogas production rate [L/gSV-second]
        # Lambda: lag phase period or minimum time to produce biogas biogas [seconds]
        # Q_in1: FLow rate by P104
        # Q_in2: flow rate by P101
        # y_t = ym*np.exp(np.exp(-((U/ym*self.GlobalTime)+Lambda)))    # Accumulative biogas yield [L/gSV]
        y_t = ym*np.exp(-np.exp(((U*np.e/ym)*(Lambda - (self.GlobalTime/60)))+1))
        
        for i,j in zip(Qin_1, Qin_2):
            self.Vinj_R102 = self.Vinj_R102 + (i * self.tp) + (j * self.tp)
            molinv = []
            if Operation == 1:
                mol_in1 = (i * self.tp * self.Csus_ini_R101)
                mol_in2 = 0
                mol_in = mol_in1 + mol_in2
                mol_out = (i * self.tp * self.Csus_ini_R102)
            elif Operation == 2:
                mol_in1 = (i * self.tp * self.Csus_ini_R101)
                mol_in2 = (j * self.tp * self.Csus_ini_R102)
                mol_in = mol_in1 + mol_in2
                mol_out = ((i + j) * self.tp * self.Csus_ini_R102)
            molinv.append(mol_in)   
            if self.Vinj_R102 > self.VR2:
                self.x_substrate_R102 = 1
                self.x_inoculum_R102 = 0
            else:
                # Vtotal_R101 =  self.Vinj_R101 + self.VR1
                self.x_substrate_R102 = self.Vinj_R102 / self.VR2
                self.x_inoculum_R102 = (1 - self.x_substrate_R102) 
        
        mol_in =sum(molinv) 
        #Biogas Volume estimation
        biogas_Normal_volume = y_t * (self.SV_R102/100) * (self.x_substrate_R102*self.rho_R101_out + self.x_inoculum_R102*self.rho_R102) * self.VR2
        biogas_mol_R102 = ((biogas_Normal_volume/1000)*100000)/(8.314*273.15)
        self.Csus_ini_R102 = (self.mol_ini_R102 + mol_in - self.mol_sus_expended_R102 - mol_out)/self.VR2
        self.mol_ini_R102 = self.Csus_ini_R102 * self.VR2
        s_biogas = (self.s_CH4 + self.s_CO2 + self.s_H2S + self.s_NH3)
        biogas_prod = biogas_mol_R102 - self.biogas_mol_R102
        self.biogas_mol_R102 = biogas_mol_R102
        self.mol_sus_expended_R102 = biogas_prod * (1/s_biogas)
        
        self.x_R102 = abs(self.Csus_ini_R101 - self.Csus_ini_R102)/self.Csus_ini_R101
        self.SV_R102 = ((self.Csus_ini_R102 * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)) / (self.rho_R101_out*self.x_substrate_R102 + self.rho_R102*self.x_inoculum_R102))*100    #[%]
        
        #Volatile solids
        self.SV_R102_p = (self.SV_R102/3)/100
        self.SV_R102_gl = self.Csus_ini_R102 * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)

        #Total Solids
        self.ST_R102_p = (((self.Csus_ini_R102 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)) / (self.rho_R101_out*self.x_substrate_R102 + self.rho_R102*self.x_inoculum_R102))
        self.ST_R102_gl = (self.Csus_ini_R102 + self.Csus_fixed) * (self.MW_sustrato*self.x_substrate_R102 + self.MW_sustrato_R102*self.x_inoculum_R102)

        #Organic Charge
        try:
            if self.GlobalTime == 0:
                self.Organic_Charge_R102 = 0                                        #[gSV/L.dia]
            else:
                self.Organic_Charge_R102 =  self.SV_R102_gl/(self.GlobalTime/86400) #[gSV/L.dia]    
        except (ZeroDivisionError, ValueError):
            self.Organic_Charge_R102 = 0

        self.molCH4_R102 = (self.mol_sus_expended_R102 * self.s_CH4)
        self.molCO2_R102 = (self.mol_sus_expended_R102 * self.s_CO2)
        self.molH2S_R102 = (self.mol_sus_expended_R102 * self.s_H2S)
        self.molNH3_R102 = (self.mol_sus_expended_R102 * self.s_NH3)
        self.molO2_R102 = np.random.uniform(0.02, 0.05) * self.mol_sus_expended_R102
        self.molH2_R102 = np.random.uniform(0.0001, 0.00015) * self.mol_sus_expended_R102
        self.molH2O_R102 = np.random.uniform(0.6, 1)* self.mol_sus_expended_R102
    
    def V102_mode2 (self, Pset):
        self.molCH4_acum_V102 = self.molCH4_acum_V102 + self.molCH4_R102 + self.mol_CH4_transferToV102
        self.molCO2_acum_V102 = self.molCO2_acum_V102 + self.molCO2_R102 + self.mol_CO2_transferToV102
        self.molO2_acum_V102 = self.molO2_acum_V102 + self.molO2_R102 + self.mol_O2_transferToV102
        self.molH2O_acum_V102 = self.molH2O_acum_V102 + self.molH2O_R102 + self.mol_H2O_transfertoV102
        self.molH2S_acum_V102 = self.molH2S_acum_V102 + self.molH2S_R102 + self.mol_H2S_transferToV102 
        self.molNH3_acum_V102 = self.molNH3_acum_V102 + self.molNH3_R102 + self.mol_NH3_transferToV102
        self.molH2_acum_V102 = self.molH2_acum_V102 + self.molH2_R102 + self.mol_H2_transfertoV102
        self.biogas_acum_V102_dry = self.molCH4_acum_V102 + self.molCO2_acum_V102 + self.molH2S_acum_V102 + self.molNH3_acum_V102 + self.molO2_acum_V102
        self.biogas_acum_V102_wet = self.biogas_acum_V102_dry + self.molH2O_acum_V102

        #Biogas compound Concentration
        try:
            if self.biogas_acum_V102_dry == 0:
                self.xCH4_V102 = 0
                self.xCO2_V102 = 0
                self.xH2S_V102 = 0
                self.xNH3_V102 = 0
                self.xH2O_V102 = 0
                self.xO2_V102 = 0
                self.xH2_V102 = 0
            else:
                self.xCH4_V102_wet = self.molCH4_acum_V102/self.biogas_acum_V102_wet
                self.xCO2_V102_wet = self.molCO2_acum_V102/self.biogas_acum_V102_wet
                self.xH2S_V102_wet = self.molH2S_acum_V102/self.biogas_acum_V102_wet
                self.xNH3_V102_wet = self.molNH3_acum_V102/self.biogas_acum_V102_wet
                self.xH2O_V102_wet = self.molH2O_acum_V102/self.biogas_acum_V102_wet
                self.xO2_V102_wet = self.molO2_acum_V102/self.biogas_acum_V102_wet
                self.xH2_V102_wet = self.molH2_acum_V102/self.biogas_acum_V102_wet
                
                self.xCH4_V102 = self.molCH4_acum_V102/self.biogas_acum_V102_dry
                self.xCO2_V102 = self.molCO2_acum_V102/self.biogas_acum_V102_dry
                self.xH2S_V102 = self.molH2S_acum_V102/self.biogas_acum_V102_dry
                self.xNH3_V102 = self.molNH3_acum_V102/self.biogas_acum_V102_dry
                self.xH2O_V102 = self.molH2O_acum_V102/self.biogas_acum_V102_wet
                self.xO2_V102 = self.molO2_acum_V102/self.biogas_acum_V102_dry
                self.xH2_V102 = self.molH2_acum_V102/self.biogas_acum_V102_dry
        except ZeroDivisionError:
                self.xCH4_V102 = 0
                self.xCO2_V102 = 0
                self.xH2S_V102 = 0
                self.xNH3_V102 = 0
                self.xH2O_V102 = 0
                self.xO2_V102 = 0
                self.xH2_V102 = 0

        p_i = ((self.biogas_acum_V102_wet * 8.314 * (self.Temperature+273.15))/((self.VG2)/1000))/6894.76 - self.Pacum_V102
        self.Pstorage_V102 = p_i + self.Pstorage_V102
        self.Pacum_V102 = ((self.biogas_acum_V102_wet * 8.314 * (self.Temperature+273.15))/((self.VG2)/1000))/6894.76
        
        #Storage biogas moles
        self.biogas_storage_mol_V102 = ((self.Pstorage_V102*6894.76) * (self.VG2/1000))/(8.314*(self.Temperature+273.15))

        #Standard volume estimation for storage and accumulated biogas
        #Standard volume estimation for accumulated biogas
        self.Vacum_std_V102 = (self.Pacum_V102*self.VG2*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        #Standard colume estimation for storage biogas
        self.Vstorage_std_V102 = (self.Pstorage_V102*self.VG2*self.Tstd)/(self.Pstd*(self.Temperature+273.15))
        
        #Accumulated volume of compounds by the time
        self.Vol_esp_CH4_V102 = self.thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_CO2_V102 = self.thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_O2_V102 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2S_V102 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_H2_V102 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=0)[2]
        self.Vol_esp_NH3_V102 = self.thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.Pacum_V102, Patm=100, T=self.Temperature, xNH3=1)[2]
        self.Vol_acum_CH4_V102 = self.Vol_esp_CH4_V102 * self.molCH4_acum_V102
        self.Vol_acum_CO2_V102 = self.Vol_esp_CO2_V102 * self.molCO2_acum_V102
        self.Vol_acum_O2_V102 = self.Vol_esp_O2_V102 * self.molO2_acum_V102
        self.Vol_acum_H2S_V102 = self.Vol_esp_H2S_V102 * self.molH2S_acum_V102
        self.Vol_acum_H2_V102 = self.Vol_esp_H2_V102 * self.molH2_acum_V102
        self.Vol_acum_NH3_V102 = self.Vol_esp_NH3_V102 * self.molNH3_acum_V102 
        
        #Energy storage
        self.Energy_V102 = self.thermo.LHV(molCH4=self.molCH4_acum_V102, molCO2=self.molCO2_acum_V102, molH2S=self.molH2S_acum_V102,
                                           molO2=self.molO2_acum_V102, molH2=self.molH2_acum_V102)[1]

        #Relative Humidity estimation
        self.RH_V102 = self.thermo.BiogasRelativeHumidity(nH2O=self.biogas_storage_mol_V102 * self.xH2O_V102, VnormalTotal=self.Vstorage_std_V102/1000, T=self.Temperature, P=self.Pstorage_V102)
        
        #Pressure control
        if self.Pstorage_V102 > Pset:
            P_storage_V102_pres = ((self.biogas_storage_mol_V102 *8.314 * (self.Temperature+273.15)) / ((self.VG2)/1000))/6894.76   #pressure before trnasfer
            self.Pstorage_V102 = (((self.biogas_storage_mol_V102 + self.biogas_storage_mol_V107) * 8.314 * (self.Temperature+273.15))/((self.VG3 + self.VG2)/1000))/6894.76      #equilibrium pressure between V102 and V102  
            # if self.Pstorage_V107 != 0:
            #     self.Pstorage_V107 = self.Pstorage_V102
            
            self.biogasmol_storage_V102= ((self.Pstorage_V102*6894.76) * ((self.VG2)/1000))/(8.314*(self.Temperature+273.15))                 #mol trnasfer since V102 to V102
            biogasmol_storage_V102_pres = ((P_storage_V102_pres*6894.76) * ((self.VG2)/1000))/(8.314*(self.Temperature+273.15)) 

            self.mol_CH4_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xCH4_V102_wet
            self.mol_CO2_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xCO2_V102_wet
            self.mol_O2_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xO2_V102_wet
            self.mol_H2S_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2S_V102_wet
            self.mol_NH3_transferToV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xNH3_V102_wet
            self.mol_H2O_transfertoV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2O_V102_wet
            self.mol_H2_transfertoV107 = (biogasmol_storage_V102_pres - self.biogasmol_storage_V102)*self.xH2_V102_wet
            
        else:
            self.mol_CH4_transferToV107 = 0
            self.mol_CO2_transferToV107 = 0
            self.mol_O2_transferToV107 =  0
            self.mol_H2S_transferToV107 = 0
            self.mol_NH3_transferToV107 = 0
            self.mol_H2O_transfertoV107 = 0
            self.mol_H2_transfertoV107 = 0
            
    def time_counter (self):
        self.GlobalTime = self.GlobalTime + (self.tp*self.time_accelerator)