import pandas as pd
from datetime import datetime
from simulation_models.Biogas import ThermoProperties as TP
from  tools import DBManager
import numpy as np
from scipy.integrate import odeint
import requests
from fractions import Fraction
from math import gcd
from functools import reduce



class BiogasPlantSimulation:

    def __init__(self, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, 
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
        
        #V101 gas storage initial conditions
        self.molCH4_acum_V101 = 0
        self.molCO2_acum_V101 = 0
        self.molO2_acum_V101 = 0
        self.molH2O_acum_V101 = 0
        self.molH2S_acum_V101 = 0
        self.molNH3_acum_V101 = 0
        self.Pstorage_V101 = 0
        self.Pacum_V101 = 0
        
        #V102 gas storage initial conditions
        self.molCH4_acum_V102 = 0
        self.molCO2_acum_V102 = 0
        self.molO2_acum_V102 = 0
        self.molH2O_acum_V102 = 0
        self.molH2S_acum_V102 = 0
        self.molNH3_acum_V102 = 0
        self.Pstorage_V102 = 0
        self.Pacum_V102 = 0

        #V107 gas storage initial conditions
        self.molCH4_acum_V107 = 0
        self.molCO2_acum_V107 = 0
        self.molO2_acum_V107 = 0
        self.molH2O_acum_V107 = 0
        self.molH2S_acum_V107 = 0
        self.molNH3_acum_V107 = 0
        self.Pstorage_V107 = 0
        self.Pacum_V107 = 0
    
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
        self.Csus_ini_ST = (self.rho*self.ST)/self.MW_sustrato                         #[mol/L]
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
    
    def Pump101 (self, FT_P101=5, TTO_P101=10, Q_P101 = 18):
        
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
            self.Q_P101v = []

        elif self.OperationMode == "Modo4":
            
            try:
                self.Q_P102 = self.Q_P102
            except:
                self.Q_P102 = 0

            self.Q_P101 = self.Q_P104 + self.Q_P102 
    
    def Pump102 (self, FT_P102=5, TTO_P102=10, Q_P102 = 18):
        
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
                            self.Q_P102v.append(self.Q_P102)
                        else:
                            self.Q_P102v.append(0)
                else:
                    self.Q_P102v.append(self.Q_P102) 

            else:
                self.Q_P102= float(0)
            
            self.TimeCounterPump_P102 = self.TimeCounterPump_P102 + (self.tp * self.time_accelerator)

            if self.TimeCounterPump_P102>=self.TurnOnDailyStep_P102*3600:
                self.TimeCounterPump_P102 = 0


        
        
        
        

                            

        





            