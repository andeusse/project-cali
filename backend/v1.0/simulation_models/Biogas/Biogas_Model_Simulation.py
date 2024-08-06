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
                 ST_R102=10, SV_R102=1, Cc_R102=40.48, Ch_R102=5.29, Co_R102=29.66, Cn_R102=1.37, Cs_R102=0.211, rho_R102=1000, OperationMode="Modo1"):

        #Interface Inputs
        self.VR1 = VR1
        self.VR2 = VR2
        self.VG1 = VG1
        self.VG2 = VG2
        self.VG3 = VG3
        self.Thermo = TP.ThermoProperties()
        self.tp = tp
        self.OperationMode = OperationMode
        #Initial values
        #Global time
        #Pumps
        self.GlobalTime = 0
        self.TimeCounterPump_P104 = 0
        self.TimeCounterPump_P101 = 0
        self.TimeCounterPump_P102 = 0
        #mixers
        self.TimeCounterMixer_TK100 = 0
        self.TimeCounterMixer_R101 = 0
        self.TimeCounterMixer_R102 = 0
                   
        #Reactor 101 initial conditions
        self.ST_R101 = ST_R101
        self.SV_R101 = SV_R101
        self.Cc_R101 = Cc_R101
        self.Ch_R101 = Ch_R101
        self.Co_R101 = Co_R101
        self.Cn_R101 = Cn_R101
        self.Cs_R101 = Cs_R101
        self.rho_R101 = rho_R101
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

            self.MW_sustrato_R101 = self.n_R101*12.01+self.a_R101*1.01+self.b_R101*16+self.c_R101*14+self.d_R101*32
            self.Csus_ini_R101 = (self.rho_R101*self.SV_R101)/self.MW_sustrato_R101
            self.Csus_ini_ST_R101 = (self.rho_R101*self.ST_R101)/self.MW_sustrato_R101
            self.Csus_fixed_R101 = self.Csus_ini_ST_R101 - self.Csus_ini_R101
        
        #initial for Arrhenius and ADM1
        self.mol_CH4_R101 = 0
        self.mol_CO2_R101 = 0
        self.mol_H2S_R101 = 0
        self.mol_O2_R101 = 0
        self.mol_NH3_R101 = 0
        self.mol_H2_R101 = 0
        self.mol_H2O_R101 = 0
        #initial for gompertz
        self.mol_ini_R101 = self.Csus_ini_R101*self.VR1
            
        #Reactor 102 initial conditions
        self.ST_R102 = ST_R102
        self.SV_R102 = SV_R102
        self.Cc_R102 = Cc_R102
        self.Ch_R102 = Ch_R102
        self.Co_R102 = Co_R102
        self.Cn_R102 = Cn_R102
        self.Cs_R102 = Cs_R102
        self.rho_R102 = rho_R102
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
            self.Csus_ini_R102 = (self.rho_R102*self.SV_R102)/self.MW_sustrato_R102
            self.Csus_ini_ST_R102 = (self.rho_R102*self.ST_R102)/self.MW_sustrato_R102
            self.Csus_fixed_R102 = self.Csus_ini_ST_R102 - self.Csus_ini_R102
        
        #initial for Arrhenius and ADM1
        self.mol_CH4_R102 = 0
        self.mol_CO2_R102 = 0
        self.mol_H2S_R102 = 0
        self.mol_NH3_R102 = 0
        self.mol_O2_R102 = 0
        self.mol_H2_R102 = 0
        self.mol_H2O_R102 = 0
        #initial for gompertz
        self.mol_ini_R102 = self.Csus_ini_R102*self.VR2

        #Initial for V101
        self.Pacum_bio_V101 = 0
        self.Pstorage_bio_V101 = 0
        self.Pini_V101 = 0
        self.mol_CH4ini_V101 = 0
        self.mol_CO2ini_V101 = 0
        self.mol_H2Sini_V101 = 0
        self.mol_O2ini_V101 = 0
        self.mol_NH3ini_V101 = 0
        self.mol_H2ini_V101 = 0
        self.mol_H2Oini_V101 = 0

        #Initial for V102
        self.Pacum_bio_V102 = 0
        self.Pstorage_bio_V102 = 0
        self.Pini_V102 = 0
        self.mol_CH4ini_V102 = 0
        self.mol_CO2ini_V102 = 0
        self.mol_H2Sini_V102 = 0
        self.mol_O2ini_V102 = 0
        self.mol_NH3ini_V102 = 0
        self.mol_H2ini_V102 = 0
        self.mol_H2Oini_V102 = 0

        self.mol_CH4_transfertoV102i = 0
        self.mol_CO2_transfertoV102i = 0
        self.mol_H2S_transfertoV102i = 0
        self.mol_O2_transfertoV102i = 0
        self.mol_NH3_transfertoV102i = 0
        self.mol_H2_transfertoV102i = 0
        self.mol_H2O_transfertoV102i = 0

        #adsortia tower
        self.N0_1 = 0
        self.N0_2 = 0
        self.N0_3 = 0

        #Initial for V107
        self.Pacum_bio_V107 = 0
        self.Pstorage_bio_V107 = 0
        self.Pini_V107 = 0
        self.mol_CH4ini_V107 = 0
        self.mol_CO2ini_V107 = 0
        self.mol_H2Sini_V107 = 0
        self.mol_O2ini_V107 = 0
        self.mol_NH3ini_V107 = 0
        self.mol_H2ini_V107 = 0
        self.mol_H2Oini_V107 = 0 

        self.mol_CH4_transfertoV107i = 0
        self.mol_CO2_transfertoV107i = 0
        self.mol_H2S_transfertoV107i = 0
        self.mol_O2_transfertoV107i = 0
        self.mol_NH3_transfertoV107i = 0
        self.mol_H2_transfertoV107i = 0
        self.mol_H2O_transfertoV107i = 0       
        
        #Propiedades del gas en condiciones estándas
        self.Vmolar_CH4 = self.Thermo.Hgases(xCH4 = 1, xCO2 = 0, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_CO2 = self.Thermo.Hgases(xCH4 = 0, xCO2 = 1, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_H2S = self.Thermo.Hgases(xCH4 = 0, xCO2 = 0, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 1, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_O2 = self.Thermo.Hgases(xCH4 = 0, xCO2 = 0, xH2O = 0, xO2 = 1, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_NH3 = self.Thermo.Hgases(xCH4 = 0, xCO2 = 0, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=1)[2]
        self.Vmolar_H2 = self.Thermo.Hgases(xCH4 = 0, xCO2 = 0, xH2O = 0, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 1, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]
        self.Vmolar_H2O = self.Thermo.Hgases(xCH4 = 0, xCO2 = 0, xH2O = 1, xO2 = 0, xN2 = 0, xH2S = 0, xH2 = 0, P = 0, Patm = 100, T = 273.15, xNH3=0)[2]

        if self.OperationMode == "Modo1":
            columns = ["time"
                    , "Q_P104"
                    , "Temp_R101"
                    , "pH_R101"
                    , "Csus_ini"
                    , "Csus_ini_R101"
                    , "mol_CH4_acum_R101"
                    , "mol_CO2_acum_R101"
                    , "mol_H2S_acum_R101"
                    , "mol_O2_acum_R101"
                    , "mol_NH3_acum_R101"
                    , "mol_H2_acum_R101"
                    , "mol_H2O_acum_R101"
                    , "Pacum_bio_V101"
                    , "Pacum_bio_V102"
                    , "Pacum_bio_V107"]
            
        elif self.OperationMode == "Modo2":
            columns = ["time"
                    , "Q_P104"
                    , "Q_P101"
                    , "Temp_R101"
                    , "pH_R101"
                    , "Csus_ini"
                    , "Csus_ini_R101"
                    , "mol_CH4_acum_R101"
                    , "mol_CO2_acum_R101"
                    , "mol_H2S_acum_R101"
                    , "mol_O2_acum_R101"
                    , "mol_NH3_acum_R101"
                    , "mol_H2_acum_R101"
                    , "mol_H2O_acum_R101"
                    , "Pacum_bio_V101"
                    , "Pacum_bio_V102"
                    , "Pacum_bio_V107"]
            
        elif self.OperationMode == "Modo3":
            columns = ["time"
                    , "Q_P104"
                    , "Q_P101"
                    , "Temp_R101"
                    , "Temp_R102"
                    , "pH_R101"
                    , "pH_R102"
                    , "Csus_ini"
                    , "Csus_ini_R101"
                    , "Csus_ini_R102"
                    , "mol_CH4_acum_R101"
                    , "mol_CO2_acum_R101"
                    , "mol_H2S_acum_R101"
                    , "mol_O2_acum_R101"
                    , "mol_NH3_acum_R101"
                    , "mol_H2_acum_R101"
                    , "mol_H2O_acum_R101"
                    , "mol_CH4_acum_R102"
                    , "mol_CO2_acum_R102"
                    , "mol_H2S_acum_R102"
                    , "mol_O2_acum_R102"
                    , "mol_NH3_acum_R102"
                    , "mol_H2_acum_R102"
                    , "mol_H2O_acum_R102"
                    , "Pacum_bio_V101"
                    , "Pacum_bio_V102"
                    , "Pacum_bio_V107"]

        elif self.OperationMode in ["Modo4", "Modo5"]:
            columns = ["time"
                    , "Q_P104"
                    , "Q_P101"
                    , "Q_P102"
                    , "Temp_R101"
                    , "Temp_R102"
                    , "pH_R101"
                    , "pH_R102"
                    , "Csus_ini"
                    , "Csus_ini_R101"
                    , "Csus_ini_R102"
                    , "mol_CH4_acum_R101"
                    , "mol_CO2_acum_R101"
                    , "mol_H2S_acum_R101"
                    , "mol_O2_acum_R101"
                    , "mol_NH3_acum_R101"
                    , "mol_H2_acum_R101"
                    , "mol_H2O_acum_R101"
                    , "mol_CH4_acum_R102"
                    , "mol_CO2_acum_R102"
                    , "mol_H2S_acum_R102"
                    , "mol_O2_acum_R102"
                    , "mol_NH3_acum_R102"
                    , "mol_H2_acum_R102"
                    , "mol_H2O_acum_R102"
                    , "Pacum_bio_V101"
                    , "Pacum_bio_V102"
                    , "Pacum_bio_V107"]
            
        self.Operation_Data = pd.DataFrame(columns= columns)

    
    def Substrate_conditions (self, Cc, Ch, Co, Cn, Cs, rho, ST, SV):

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
        
        self.MW_sustrato = self.n*12.01+self.a*1.01+self.b*16+self.c*14+self.d*32
        self.Csus_ini = (self.rho*(self.SV/100))/self.MW_sustrato
        self.Csus_ini_ST = (self.rho*self.ST)/self.MW_sustrato
        self.Csus_fixed = self.Csus_ini_ST - self.Csus_ini

        self.Csv = (self.rho*(self.SV/100))
        self.Cst = (self.rho*(self.ST/100))
    
    def Pump104 (self, TRH=30, FT_P104=5, TTO_P104=10):    
        
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

        if self.TimeCounterPump_P104<self.TTO_P104*60:
            self.Q_P104 = (self.Q_time/self.TTO_P104)*60
        else:
            self.Q_P104= float(0)
            #self.Csus_ini = 0
        
        self.TimeCounterPump_P104 = self.TimeCounterPump_P104 + self.tp

        if self.TimeCounterPump_P104>=self.TurnOnDailyStep_P104*3600:
            self.TimeCounterPump_P104 = 0
        
    def Pump101 (self, FT_P101=5, TTO_P101=10, Q_P101 = 2.4):
        
        if self.OperationMode == "Modo1":
            pass

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
    
    def Pump102 (self, FT_P102=5, TTO_P102=10, Q_P102 = 2.4):
        
        if self.OperationMode == "Modo1" or self.OperationMode == "Modo2" or self.OperationMode == "Modo3":
            pass

        elif self.OperationMode == "Modo4" or self.OperationMode == "Modo5":
            self.FT_P102= FT_P102
            self.TTO_P102 = TTO_P102

            try:
                self.TurnOnDailyStep_P102 = 24/self.FT_P102
            except ZeroDivisionError:
                self.TurnOnDailyStep_P102 = 0

            if self.TimeCounterPump_P102<self.TTO_P102*60:
                self.Q_P102 = Q_P102
            else:
                self.Q_P102= float(0)
            
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
            pass
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
    
    def Data_simulation(self, Temperature_R101=35, Temperature_R102=35, pH_R101 = 7, pH_R102 = 7):
        self.pH_R101 = pH_R101
        self.pH_R102 = pH_R102
        self.Temp_R101=Temperature_R101
        self.Temp_R102=Temperature_R102
        if self.OperationMode == "Modo1":
            new_row = pd.DataFrame({"time": [self.GlobalTime],
                                    "Q_P104" : [self.Q_P104],
                                    "Temp_R101": [self.Temp_R101],
                                    "pH_R101": [pH_R101],
                                    "Csus_ini" : [self.Csus_ini],
                                    "Csus_ini_R101" : [self.Csus_ini_R101],
                                    "mol_CH4_acum_R101":[self.mol_CH4_R101],
                                    "mol_CO2_acum_R101":[self.mol_CO2_R101],
                                    "mol_H2S_acum_R102":[self.mol_H2S_R101],
                                    "mol_O2_acum_R101":[self.mol_O2_R101],
                                    "mol_NH3_acum_R101":[self.mol_NH3_R101],
                                    "mol_H2_acum_R101":[self.mol_H2_R101],
                                    "mol_H2O_acum_R101":[self.mol_H2O_R101],
                                    "Pacum_bio_V101":[self.Pacum_bio_V101],
                                    "Pacum_bio_V102":[self.Pacum_bio_V102],
                                    "Pacum_bio_V107":[self.Pacum_bio_V107]})
        
        elif self.OperationMode == "Modo2":
             new_row = pd.DataFrame({"time": [self.GlobalTime],
                                    "Q_P104" : [self.Q_P104],
                                    "Q_P101" : [self.Q_P101],
                                    "Temp_R101": [self.Temp_R101],
                                    "pH_R101":[pH_R101],
                                    "Csus_ini" : [self.Csus_ini],
                                    "Csus_ini_R101" : [self.Csus_ini_R101],
                                    "mol_CH4_acum_R101":[self.mol_CH4_R101],
                                    "mol_CO2_acum_R101":[self.mol_CO2_R101],
                                    "mol_H2S_acum_R101":[self.mol_H2S_R101],
                                    "mol_O2_acum_R101":[self.mol_O2_R101],
                                    "mol_NH3_acum_R101":[self.mol_NH3_R101],
                                    "mol_H2_acum_R101":[self.mol_H2_R101],
                                    "mol_H2O_acum_R101":[self.mol_H2O_R101],
                                    "Pacum_bio_V101":[self.Pacum_bio_V101],
                                    "Pacum_bio_V102":[self.Pacum_bio_V102],
                                    "Pacum_bio_V107":[self.Pacum_bio_V107]})
        
        elif self.OperationMode == "Modo3":
            new_row = pd.DataFrame({"time": [self.GlobalTime],
                                    "Q_P104" : [self.Q_P104],
                                    "Q_P101" : [self.Q_P101],
                                    "Temp_R101": [self.Temp_R101],
                                    "Temp_R102":[self.Temp_R102],
                                    "pH_R101":[pH_R101],
                                    "pH_R102":[pH_R102],
                                    "Csus_ini" : [self.Csus_ini],
                                    "Csus_ini_R101" : [self.Csus_ini_R101],
                                    "Csus_ini_R102" : [self.Csus_ini_R102],
                                    "mol_CH4_acum_R101":[self.mol_CH4_R101],
                                    "mol_CO2_acum_R101":[self.mol_CO2_R101],
                                    "mol_H2S_acum_R101":[self.mol_H2S_R101],
                                    "mol_O2_acum_R101":[self.mol_O2_R101],
                                    "mol_NH3_acum_R101":[self.mol_NH3_R101],
                                    "mol_H2_acum_R101":[self.mol_H2_R101],
                                    "mol_H2O_acum_R101":[self.mol_H2O_R101],
                                    "mol_CH4_acum_R102":[self.mol_CH4_R102],
                                    "mol_CO2_acum_R102":[self.mol_CO2_R102],
                                    "mol_H2S_acum_R102":[self.mol_H2S_R102],
                                    "mol_O2_acum_R102":[self.mol_O2_R102],
                                    "mol_NH3_acum_R102":[self.mol_NH3_R102],
                                    "mol_H2_acum_R102":[self.mol_H2_R102],
                                    "mol_H2O_acum_R102":[self.mol_H2O_R102],
                                    "Pacum_bio_V101":[self.Pacum_bio_V101],
                                    "Pacum_bio_V102":[self.Pacum_bio_V102],
                                    "Pacum_bio_V107":[self.Pacum_bio_V107]})
        
        elif self.OperationMode in ["Modo4", "Modo5"]:
            new_row = pd.DataFrame({"time": [self.GlobalTime],
                                    "Q_P104" : [self.Q_P104],
                                    "Q_P101" : [self.Q_P101],
                                    "Q_P102" : [self.Q_P102],
                                    "Temp_R101": [self.Temp_R101],
                                    "Temp_R102":[self.Temp_R102],
                                    "pH_R101":[pH_R101],
                                    "pH_R102":[pH_R102],
                                    "Csus_ini" : [self.Csus_ini],
                                    "Csus_ini_R101" : [self.Csus_ini_R101],
                                    "Csus_ini_R102" : [self.Csus_ini_R102],
                                    "mol_CH4_acum_R101":[self.mol_CH4_R101],
                                    "mol_CO2_acum_R101":[self.mol_CO2_R101],
                                    "mol_H2S_acum_R101":[self.mol_H2S_R101],
                                    "mol_O2_acum_R101":[self.mol_O2_R101],
                                    "mol_NH3_acum_R101":[self.mol_NH3_R101],
                                    "mol_H2_acum_R101":[self.mol_H2_R101],
                                    "mol_H2O_acum_R101":[self.mol_H2O_R101],
                                    "mol_CH4_acum_R102":[self.mol_CH4_R102],
                                    "mol_CO2_acum_R102":[self.mol_CO2_R102],
                                    "mol_H2S_acum_R102":[self.mol_H2S_R102],
                                    "mol_O2_acum_R102":[self.mol_O2_R102],
                                    "mol_NH3_acum_R102":[self.mol_NH3_R102],
                                    "mol_H2_acum_R102":[self.mol_H2_R102],
                                    "mol_H2O_acum_R102":[self.mol_H2O_R102],
                                    "Pacum_bio_V101":[self.Pacum_bio_V101],
                                    "Pacum_bio_V102":[self.Pacum_bio_V102],
                                    "Pacum_bio_V107":[self.Pacum_bio_V107]})
        
        new_row_filtered = new_row.dropna(axis=1, how ='all')
        self.Operation_Data = self.Operation_Data.dropna(axis=1, how='all')
        self.Operation_Data = pd.concat([self.Operation_Data, new_row_filtered], ignore_index=True)

    def ReactorSimulation(self, Model, A_R101, B_R101, C_R101, A_R102=1, B_R102=1, C_R102=1):
        self.Model = Model

        def model_Arrehenius(C, t, K, Ea, VR, pH_effect_func, T_func, Q_func_1, Q_func_2, Csus_ini_func_1, Csus_ini_func_2, Operation):
            R = 8.314
            T=T_func(t)
            Q_1=Q_func_1(t)
            Q_2=Q_func_2(t)
            Csus_ini_1 = Csus_ini_func_1(t)
            Csus_ini_2 = Csus_ini_func_2(t)
            pH = pH_effect_func(t)
            if Operation == 1:         #Sin recirculación
                dCsus_dt = ((Q_1 / VR) * (Csus_ini_1 - C)) - (C * K * np.exp(-(Ea)/(R*T*pH))) / VR
            elif Operation == 2:       #dos entradas 
                dCsus_dt = (Q_1 * Csus_ini_1)/VR + (Q_2 * Csus_ini_2)/VR - ((Q_1+Q_2)*C)/VR - (C * K * np.exp(-Ea/(R*T*pH))) / VR
            elif Operation == 3:       #Recirculación interna
                dCsus_dt = (Q_1 * Csus_ini_1)/VR + (Q_2 * C)/VR - ((Q_1)*C)/VR - (C * K * np.exp(-Ea/(R*T*pH))) / VR
            return dCsus_dt
        
        def model_ADM1(C, t, K, VR, pH_effect_func, T_func, Q_func_1, Q_func_2, Csus_ini_func_1, Csus_ini_func_2, Operation):
            R = 8.314
            Q_1=Q_func_1(t)
            Q_2=Q_func_2(t)
            Csus_ini_1 = Csus_ini_func_1(t)
            Csus_ini_2 = Csus_ini_func_2(t)
            pH = pH_effect_func(t)
            T = T_func(t)
            if Operation == 1:         #Sin recirculación
                dCsus_dt = ((Q_1 / VR) * (Csus_ini_1 - C)) - (C * K * pH * T) / VR
            elif Operation == 2:       #dos entradas 
                dCsus_dt = (Q_1 * Csus_ini_1)/VR + (Q_2 * Csus_ini_2)/VR - ((Q_1 + Q_2)*C)/VR - (C * K * pH * T) / VR
            elif Operation == 3:       #Recirculación interna
                dCsus_dt = (Q_1 * Csus_ini_1)/VR + (Q_2 * C)/VR - ((Q_1 + Q_2)*C)/VR - (C * K * pH * T) / VR
            return dCsus_dt
        
        def model_Gompertz(t, ym, U, L):
            y_t = ym * np.exp(-np.exp((U * np.e) / ym * (L - t) + 1))
            return y_t

        def pH_effect (parameter):
            if self.Model == "Arrhenius":
                variable = np.exp(-((float(parameter)-7)**2)/(2*5**2))
            else:
                variable = np.exp(-((float(parameter)-7)**2)/(2*1**2))
            return variable
        
        def Temperature_effect (parameter):
            variable = np.exp(-((float(parameter)-45)**2)/(2*35**2))
            return variable
        
        def mixing_effect (parameter):
            if parameter < 10:
                variable = 1
            elif parameter >= 10:
                variable = np.random.uniform(0.99, 1)
            return float(variable)

        if Model == "Arrhenius":
            self.K_R101 = A_R101
            self.Ea_R101 = B_R101
            
            self.K_R102 = A_R102
            self.Ea_R102 = B_R102
        
        elif Model == "ADM1":
            self.K_R101 = A_R101
            self.K_R102 = A_R102
        
        elif Model == "Gompertz":
            self.ym_R101 = A_R101
            self.U_R101 = B_R101  
            self.L_R101 = C_R101

            self.ym_R102 = A_R102
            self.U_R102 = B_R102  
            self.L_R102 = C_R102    

        # Model Arrhenius    
        if self.Model == "Arrhenius":

            if self.OperationMode in ["Modo1", "Modo2"] :
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume
                pH_R101 = [pH_effect(p) for p in self.Operation_Data.pH_R101.tolist()]                 #Get Historic pH
                pH_func_R101 = lambda t: np.interp(t, time, pH_R101) 
                T_R101 = self.Operation_Data.Temp_R101.astype(float)                                   #Temperatures Vector
                T_func_R101 = lambda t: np.interp(t, time, T_R101)                                     #Temperatures in time vector                
                Qin_R101_1 = (self.Operation_Data.Q_P104/3600).astype(float).tolist()                    #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector
                
                #R_101 Solution
                self.Csus_ini_R101 = odeint(model_Arrehenius, y0_R101, time, args=(self.K_R101, self.Ea_R101, VR_R101, pH_func_R101, T_func_R101, Q_func_R101_1, Q_func_R101_1, Csus_in_func_R101_1, Csus_in_func_R101_1, 1)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                                                
                self.Csus_ini_R101 = self.Csus_ini_R101*mixing_effect(self.RPM_R101)         #molSV/L 
                
                #Solidos totales R101
                self.ST_R101 = ((self.ST_R101 * self.rho * self.VR1) + (self.Q_P104 * self.ST * self.rho * (self.tp/3600)) - ((self.K_R101 * np.exp(-self.Ea_R101 / (8.314 * T_R101.iloc[-1] * pH_R101[-1]))) * self.Csus_ini_R101 * (self.tp / 3600)))/(self.VR1+(self.Q_P104*(self.tp/3600)))/self.rho

            elif self.OperationMode in ["Modo3", "Modo5"] :
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume
                pH_R101 = [pH_effect(p) for p in self.Operation_Data.pH_R101.tolist()]                 #Get Historic pH
                pH_func_R101 = lambda t: np.interp(t, time, pH_R101) 
                T_R101 = self.Operation_Data.Temp_R101.astype(float)                                   #Temperatures Vector
                T_func_R101 = lambda t: np.interp(t, time, T_R101)                                     #Temperatures in time vector                
                Qin_R101_1 = (self.Operation_Data.Q_P104/3600).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector

                #R101 Solution
                self.Csus_ini_R101 = odeint(model_Arrehenius, y0_R101, time, args=(self.K_R101, self.Ea_R101, VR_R101, pH_func_R101, T_func_R101, Q_func_R101_1, Q_func_R101_1, Csus_in_func_R101_1, Csus_in_func_R101_1, 1)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                                
                self.Csus_ini_R101 = self.Csus_ini_R101*mixing_effect(self.RPM_R101)
                
                #Solidos totales R101
                self.ST_R101 = ((self.ST_R101 * self.rho * self.VR1) + (self.Q_P104 * self.ST * self.rho * (self.tp/3600)) - ((self.K_R101 * np.exp(-self.Ea_R101 / (8.314 * T_R101.iloc[-1] * pH_R101[-1]))) * self.Csus_ini_R101 * (self.tp / 3600)))/(self.VR1+(self.Q_P104*(self.tp/3600)))/self.rho

                #R_102 Conditions
                y0_R102 = float(self.Operation_Data.Csus_ini_R102[0])                                  #intital condition
                VR_R102 = self.VR2                                                                     #Reactor volume
                pH_R102 = [pH_effect(p) for p in self.Operation_Data.pH_R102.tolist()]                 #Get Historic pH
                pH_func_R102 = lambda t: np.interp(t, time, pH_R102) 
                T_R102 = self.Operation_Data.Temp_R102.astype(float)                                   #Temperatures Vector
                T_func_R102 = lambda t: np.interp(t, time, T_R102)                                     #Temperatures in time vector                
                Qin_R102_1 = (self.Operation_Data.Q_P101/3600).astype(float).tolist()                  #flow in 1 Vector            
                Q_func_R102_1 = lambda t: np.interp(t, time, Qin_R102_1)                               #flow in time vector
                Csus_in_R102_1 = self.Operation_Data.Csus_ini_R101.astype(float)                       #Inlet substrate concentration
                Csus_in_func_R102_1 = lambda t: np.interp(t, time, Csus_in_R102_1)                     #Concentration in time vector
                
                #R102 Solution
                self.Csus_ini_R102 = odeint(model_Arrehenius, y0_R102, time, args=(self.K_R102, self.Ea_R102, VR_R102, pH_func_R102, T_func_R102, Q_func_R102_1, Q_func_R102_1, Csus_in_func_R102_1, Csus_in_func_R102_1, 1)).flatten()
                self.Csus_ini_R102 = self.Csus_ini_R102[-1]
                                
                self.Csus_ini_R102 = self.Csus_ini_R102*mixing_effect(self.RPM_R102)

                # Solidos volátiles en porcentaje R102
                self.SV_R102_p = self.Csus_ini_R102 * self.MW_sustrato / self.rho        #gSV/gT  
                #Sólidos volátiles en gSV/L R102
                self.SV_R102_gL = self.Csus_ini_R102 * self.MW_sustrato                  #gSV/L
                #Carga orgánica en gSV/L.dia R102
                try:
                    if self.GlobalTime == 0:
                        self.Organic_charge_R102 = 0
                    else:
                        self.Organic_charge_R102 = self.SV_R102_gL/(self.GlobalTime*86400)   #gSV/L.dia
                except (ZeroDivisionError, ValueError):
                    self.Organic_charge_R102 = 0
                
                try:
                    if ((self.Csus_ini_R101 * self.MW_sustrato)) / self.rho == 0:
                        self.x_R102 = 0
                    else:
                        self.x_R102 = ((self.Csus_ini_R101 * self.MW_sustrato / self.rho) - self.SV_R102_p)/(self.Csus_ini_R101 * self.MW_sustrato / self.rho)
                except ZeroDivisionError:
                    self.x_R102 = 0
                
                #Solidos totales R102
                self.ST_R102 = ((self.ST_R102 * self.rho * self.VR2) + (self.Q_P101 * self.ST_R101 * self.rho * (self.tp/3600)) - ((self.K_R102 * np.exp(-self.Ea_R102 / (8.314 * T_R102.iloc[-1] * pH_R102[-1]))) * self.Csus_ini_R102 * (self.tp / 3600)))/(self.VR2+(self.Q_P101*(self.tp/3600)))/self.rho

                # Estimación de biogás producido por componente en moles R102
                self.mol_CH4_stoichometric_R102 = (self.K_R102*np.exp(-self.Ea_R102/(8.314*T_R102.iloc[-1]*pH_R102[-1]))) * self.Csus_ini_R102 * self.s_CH4 * (self.tp / 3600)
                self.mol_CH4_R102 = self.mol_CH4_R102 + self.mol_CH4_stoichometric_R102
                self.mol_CO2_R102 = self.mol_CH4_R102 * (self.s_CO2/self.s_CH4)
                self.mol_H2S_R102 = self.mol_CH4_R102*(self.s_H2S/self.s_CH4)
                self.mol_NH3_R102 = self.mol_CH4_R102*(self.s_NH3/self.s_CH4)
                self.mol_O2_R102 = self.mol_O2_R102 + self.mol_CH4_stoichometric_R102*np.random.uniform (0, 0.1) 
                self.mol_H2_R102 = self.mol_H2_R102 + self.mol_CH4_stoichometric_R102*np.random.uniform (0, 0.00001)
                self.mol_H2O_R102 = self.mol_H2O_R102 + abs(self.mol_CH4_stoichometric_R102*np.random.normal(0.4, 0.1))
            
            elif self.OperationMode == "Modo4":
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume
                pH_R101 = [pH_effect(p) for p in self.Operation_Data.pH_R101.tolist()]                 #Get Historic pH
                pH_func_R101 = lambda t: np.interp(t, time, pH_R101) 
                T_R101 = self.Operation_Data.Temp_R101.astype(float)                                   #Temperatures Vector
                T_func_R101 = lambda t: np.interp(t, time, T_R101)                                     #Temperatures in time vector                
                Qin_R101_1 = (self.Operation_Data.Q_P104/3600).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Qin_R101_2 = (self.Operation_Data.Q_P102/3600).astype(float).tolist()
                Q_func_R101_2 = lambda t: np.interp(t, time, Qin_R101_2)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector
                Csus_in_R101_2 = self.Operation_Data.Csus_ini_R102.tolist()
                Csus_in_func_R101_2 = lambda t: np.interp(t, time, Csus_in_R101_2)                     #Concentration in time vector
                
                #R101 Solution
                self.Csus_ini_R101 = odeint(model_Arrehenius, y0_R101, time, args=(self.K_R101, self.Ea_R101, VR_R101, pH_func_R101, T_func_R101, Q_func_R101_1, Q_func_R101_2, Csus_in_func_R101_1, Csus_in_func_R101_2, 2)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]

                self.Csus_ini_R101 = self.Csus_ini_R101*mixing_effect(self.RPM_R101)

                #Solidos totales R101
                self.ST_R101 = ((self.ST_R101 * self.rho * self.VR1) + (self.Q_P104 * self.ST * self.rho * (self.tp/3600)) + (self.Q_P102 * self.ST_R102 * self.rho * (self.tp/3600)) - ((self.K_R101 * np.exp(-self.Ea_R101 / (8.314 * T_R101.iloc[-1] * pH_R101[-1]))) * self.Csus_ini_R101 * (self.tp / 3600)))/(self.VR1+(self.Q_P101*(self.tp/3600)))/self.rho

                #R_102 Conditions
                y0_R102 = float(self.Operation_Data.Csus_ini_R102[0])                                  #intital condition
                VR_R102 = self.VR2                                                                     #Reactor volume
                pH_R102 = [pH_effect(p) for p in self.Operation_Data.pH_R102.tolist()]                 #Get Historic pH
                pH_func_R102 = lambda t: np.interp(t, time, pH_R102)
                T_R102 = self.Operation_Data.Temp_R102.astype(float)                                   #Temperatures Vector
                T_func_R102 = lambda t: np.interp(t, time, T_R102)                                     #Temperatures in time vector                
                Qin_R102_1 = (self.Operation_Data.Q_P101/3600).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R102_1 = lambda t: np.interp(t, time, Qin_R102_1)                               #flow in time vector
                Csus_in_R102_1 = self.Operation_Data.Csus_ini_R101.astype(float)                       #Inlet substrate concentration
                Csus_in_func_R102_1 = lambda t: np.interp(t, time, Csus_in_R102_1)                     #Concentration in time vector

                #R102 Solution
                self.Csus_ini_R102 = odeint(model_Arrehenius, y0_R102, time, args=(self.K_R102, self.Ea_R102, VR_R102, pH_func_R102, T_func_R102, Q_func_R102_1, Q_func_R101_1, Csus_in_func_R102_1, Csus_in_func_R102_1, 1)).flatten()
                self.Csus_ini_R102 = self.Csus_ini_R102[-1]
                                
                self.Csus_ini_R102 = self.Csus_ini_R102*mixing_effect(self.RPM_R102)

                # Solidos volátiles en porcentaje R102
                self.SV_R102_p = self.Csus_ini_R102 * self.MW_sustrato / self.rho        #gSV/gT  
                #Sólidos volátiles en gSV/L R102
                self.SV_R102_gL = self.Csus_ini_R102 * self.MW_sustrato                  #gSV/L
                #Carga orgánica en gSV/L.dia R102
                try:
                    if self.GlobalTime == 0:
                        self.Organic_charge_R102 = 0   #gSV/L.dia
                    else:
                        self.Organic_charge_R102 = self.SV_R102_gL/(self.GlobalTime*86400)   #gSV/L.dia 
                except (ZeroDivisionError, ValueError) :
                    self.Organic_charge_R102 = 0
                
                try:
                    if ((self.Csus_ini_R101 * self.MW_sustrato)) / self.rho == 0:
                        self.x_R102 = 0
                    else:
                        self.x_R102 = ((self.Csus_ini_R101 * self.MW_sustrato / self.rho) - self.SV_R102_p)/(self.Csus_ini_R101 * self.MW_sustrato / self.rho)
                except ZeroDivisionError:
                    self.x_R102 = 0

                #Solidos totales R102
                self.ST_R102 = ((self.ST_R102 * self.rho * self.VR2) + (self.Q_P101 * self.ST_R101 * self.rho * (self.tp/3600)) - ((self.K_R102 * np.exp(-self.Ea_R102 / (8.314 * T_R102.iloc[-1] * pH_R102[-1]))) * self.Csus_ini_R102 * (self.tp / 3600)))/(self.VR2+(self.Q_P101*(self.tp/3600)))/self.rho

                # Estimación de biogás producido por componente en moles R102
                self.mol_CH4_stoichometric_R102 = (self.K_R102*np.exp(-self.Ea_R102/(8.314*T_R102.iloc[-1]*pH_R102[-1]))) * self.Csus_ini_R102 * self.s_CH4 * (self.tp / 3600)
                self.mol_CH4_R102 = self.mol_CH4_R102 + self.mol_CH4_stoichometric_R102
                self.mol_CO2_R102 = self.mol_CH4_R102 * (self.s_CO2/self.s_CH4)
                self.mol_H2S_R102 = self.mol_CH4_R102*(self.s_H2S/self.s_CH4)
                self.mol_NH3_R102 = self.mol_CH4_R102*(self.s_NH3/self.s_CH4)
                self.mol_O2_R102 = self.mol_O2_R102 + self.mol_CH4_stoichometric_R102*np.random.uniform (0, 0.1) 
                self.mol_H2_R102 = self.mol_H2_R102 + self.mol_CH4_stoichometric_R102*np.random.uniform (0, 0.00001)
                self.mol_H2O_R102 = self.mol_H2O_R102 + abs(self.mol_CH4_stoichometric_R102*np.random.normal(0.4, 0.1))

            # Estimación de biogás producido por componente en moles R101
            self.mol_CH4_stoichometric_R101 = (self.K_R101*np.exp(-self.Ea_R101/(8.314*T_R101.iloc[-1]*pH_R101[-1]))) * self.Csus_ini_R101 * self.s_CH4 * (self.tp / 3600)
            self.mol_CH4_R101 = float(self.mol_CH4_R101 + self.mol_CH4_stoichometric_R101)
            self.mol_CO2_R101 = self.mol_CH4_R101 * (self.s_CO2/self.s_CH4)
            self.mol_H2S_R101 = self.mol_CH4_R101*(self.s_H2S/self.s_CH4)
            self.mol_NH3_R101 = self.mol_CH4_R101*(self.s_NH3/self.s_CH4)
            self.mol_O2_R101 = self.mol_O2_R101 + self.mol_CH4_stoichometric_R101*np.random.uniform (0, 0.1) 
            self.mol_H2_R101 = self.mol_H2_R101 + self.mol_CH4_stoichometric_R101*np.random.uniform (0, 0.00001)
            self.mol_H2O_R101 = self.mol_H2O_R101 + self.mol_CH4_stoichometric_R101*np.random.normal(0.01, 0.4)

            # Solidos volátiles en porcentaje R101
            self.SV_R101_p = self.Csus_ini_R101 * self.MW_sustrato / self.rho        #gSV/gT  
            #Sólidos volátiles en gSV/L R101
            self.SV_R101_gL = self.Csus_ini_R101 * self.MW_sustrato                  #gSV/L
            #Carga orgánica en gSV/L.dia R101
            
            try:
                if self.GlobalTime == 0:
                    self.Organic_charge_R101 = 0
                else:
                    self.Organic_charge_R101 = (self.SV_R101_gL/(self.GlobalTime*86400))   #gSV/L.dia
            except (ZeroDivisionError, ValueError):
                self.Organic_charge_R101 = 0
            
            try:
                if self.SV == 0:
                    self.x_R101 = 0
                else:
                    self.x_R101 = (self.SV - self.SV_R101_p)/self.SV
            except ZeroDivisionError:
                self.x_R101 = 0
            

        # Model ADM1
        elif self.Model == "ADM1":

            if self.OperationMode in ["Modo1", "Modo2"] :
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume  
                pH_R101 = [pH_effect(p) for p in self.Operation_Data.pH_R101.tolist()]
                pH_func_R101 = lambda t: np.interp(t, time, pH_R101)
                T_R101 = [Temperature_effect(p) for p in self.Operation_Data.Temp_R101.tolist()]       #Get Historic Temperature
                T_func_R101 = lambda t: np.interp(t, time, T_R101)                                      
                Qin_R101_1 = (self.Operation_Data.Q_P104/3600).astype(float).tolist()                  #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector

                #R_101 Solution
                self.Csus_ini_R101 = odeint(model_ADM1, y0_R101, time, args=(self.K_R101, VR_R101, pH_func_R101, T_func_R101, Q_func_R101_1, Q_func_R101_1, Csus_in_func_R101_1, Csus_in_func_R101_1, 1)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                                
                self.Csus_ini_R101 = self.Csus_ini_R101*mixing_effect(self.RPM_R101)

                #Solidos totales R101
                self.ST_R101 = ((self.ST_R101 * self.rho * self.VR1) + (self.Q_P104 * self.ST * self.rho * (self.tp/3600)) - (self.K_R101 * pH_R101[-1] * T_R101[-1] * self.Csus_ini_R101 * (self.tp / 3600)))/(self.VR1+(self.Q_P104*(self.tp/3600)))/self.rho

            elif self.OperationMode in ["Modo3", "Modo5"]:

                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume
                pH_R101 = [pH_effect(p) for p in self.Operation_Data.pH_R101.tolist()]
                pH_func_R101 = lambda t: np.interp(t, time, pH_R101)
                T_R101 = [Temperature_effect(p) for p in self.Operation_Data.Temp_R101.tolist()]       #Get Historic Temperature
                T_func_R101 = lambda t: np.interp(t, time, T_R101)                                      
                Qin_R101_1 = (self.Operation_Data.Q_P104/3600).astype(float).tolist()                    #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector

                #R_101 Solution
                self.Csus_ini_R101 = odeint(model_ADM1, y0_R101, time, args=(self.K_R101, VR_R101, pH_func_R101, T_func_R101, Q_func_R101_1, Q_func_R101_1, Csus_in_func_R101_1, Csus_in_func_R101_1, 1)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                                
                self.Csus_ini_R101 = self.Csus_ini_R101*mixing_effect(self.RPM_R101)

                #Solidos totales R101
                self.ST_R101 = ((self.ST_R101 * self.rho * self.VR1) + (self.Q_P104 * self.ST * self.rho * (self.tp/3600)) - (self.K_R101 * pH_R101[-1] * T_R101[-1] * self.Csus_ini_R101 * (self.tp / 3600)))/(self.VR1+(self.Q_P104*(self.tp/3600)))/self.rho
                
                #R_102 Conditions
                y0_R102 = float(self.Operation_Data.Csus_ini_R102[0])                                  #intital condition
                VR_R102 = self.VR2                                                                     #Reactor volume               
                pH_R102 = [pH_effect(p) for p in self.Operation_Data.pH_R102.tolist()]
                pH_func_R102 = lambda t: np.interp(t, time, pH_R102)
                T_R102 = [Temperature_effect(p) for p in self.Operation_Data.Temp_R102.tolist()]       #Get Historic Temperature
                T_func_R102 = lambda t: np.interp(t, time, T_R102)
                Qin_R102_1 = (self.Operation_Data.Q_P101/3600).astype(float).tolist()                    #flow in 1 Vector            
                Q_func_R102_1 = lambda t: np.interp(t, time, Qin_R102_1)                               #flow in time vector
                Csus_in_R102_1 = self.Operation_Data.Csus_ini_R101.astype(float)                       #Inlet substrate concentration
                Csus_in_func_R102_1 = lambda t: np.interp(t, time, Csus_in_R102_1)                     #Concentration in time vector

                #R102 Solution
                self.Csus_ini_R102 = odeint(model_ADM1, y0_R102, time, args=(self.K_R102, VR_R102, pH_func_R102, T_func_R102, Q_func_R102_1, Q_func_R102_1, Csus_in_func_R102_1, Csus_in_func_R102_1, 1)).flatten()
                self.Csus_ini_R102 = self.Csus_ini_R102[-1]
                                
                self.Csus_ini_R102 = self.Csus_ini_R102*mixing_effect(self.RPM_R102)

                # Solidos volátiles en porcentaje R102
                self.SV_R102_p = self.Csus_ini_R102 * self.MW_sustrato / self.rho        #gSV/gT  
                #Sólidos volátiles en gSV/L R102
                self.SV_R102_gL = self.Csus_ini_R102 * self.MW_sustrato                  #gSV/L
                #Carga orgánica en gSV/L.dia R102
                try:
                    if self.GlobalTime == 0:
                        self.Organic_charge_R102 = 0
                    else:    
                        self.Organic_charge_R102 = self.SV_R102_gL/(self.GlobalTime*86400)   #gSV/L.dia
                except ZeroDivisionError:
                    self.Organic_charge_R102 = 0
                
                try:
                    if ((self.Csus_ini_R101 * self.MW_sustrato)) / self.rho == 0:
                        self.x_R102 = 0
                    else:
                        self.x_R102 = ((self.Csus_ini_R101 * self.MW_sustrato / self.rho) - self.SV_R102_p)/(self.Csus_ini_R101 * self.MW_sustrato / self.rho)
                except ZeroDivisionError:
                    self.x_R102 = 0

                #Solidos totales R102
                self.ST_R102 = ((self.ST_R102 * self.rho * self.VR2) + (self.Q_P101 * self.ST_R101 * self.rho * (self.tp/3600)) - ((self.K_R102 *  pH_R102[-1] * T_R102[-1]) * self.Csus_ini_R102 * (self.tp / 3600)))/(self.VR2+(self.Q_P101*(self.tp/3600)))/self.rho
            
                # Estimación de biogás producido por componente en moles R102 operación 3 y 5
                self.mol_CH4_stoichometric_R102 = (self.K_R102 * pH_R102[-1] * T_R102[-1]) * self.Csus_ini_R102 * self.s_CH4 * (self.tp / 3600)
                self.mol_CH4_R102 = self.mol_CH4_R102 + self.mol_CH4_stoichometric_R102
                self.mol_CO2_R102 = self.mol_CH4_R102 * (self.s_CO2/self.s_CH4)
                self.mol_H2S_R102 = self.mol_CH4_R102*(self.s_H2S/self.s_CH4)
                self.mol_NH3_R102 = self.mol_CH4_R102*(self.s_NH3/self.s_CH4)
                self.mol_O2_R102 = self.mol_O2_R102 + self.mol_CH4_stoichometric_R102*np.random.uniform (0, 0.1) 
                self.mol_H2_R102 = self.mol_H2_R102 + self.mol_CH4_stoichometric_R102*np.random.uniform (0, 0.00001)
                self.mol_H2O_R102 = self.mol_H2O_R102 + abs(self.mol_CH4_stoichometric_R102*np.random.normal(0.4, 0.1))

            elif self.OperationMode == "Modo4":
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume       
                pH_R101 = [pH_effect(p) for p in self.Operation_Data.pH_R102.tolist()]
                pH_func_R101 = lambda t: np.interp(t, time, pH_R101)
                T_R101 = [Temperature_effect(p) for p in self.Operation_Data.Temp_R101.tolist()]       #Get Historic Temperature
                T_func_R101 = lambda t: np.interp(t, time, T_R101)
                Qin_R101_1 = (self.Operation_Data.Q_P104/3600).astype(float).tolist()                    #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Qin_R101_2 = (self.Operation_Data.Q_P102/3600).astype(float).tolist()
                Q_func_R101_2 = lambda t: np.interp(t, time, Qin_R101_2)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector
                Csus_in_R101_2 = self.Operation_Data.Csus_ini_R102.tolist()
                Csus_in_func_R101_2 = lambda t: np.interp(t, time, Csus_in_R101_2)                     #Concentration in time vector

                #R101 Solution
                self.Csus_ini_R101 = odeint(model_ADM1, y0_R101, time, args=(self.K_R101, VR_R101, pH_func_R101, T_func_R101, Q_func_R101_1, Q_func_R101_2, Csus_in_func_R101_1, Csus_in_func_R101_2, 2)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                                
                self.Csus_ini_R101 = self.Csus_ini_R101*mixing_effect(self.RPM_R101)

                #Solidos totales R101
                self.ST_R101 = ((self.ST_R101 * self.rho * self.VR1) + (self.Q_P104 * self.ST * self.rho * (self.tp/3600)) + (self.Q_P102 * self.ST_R102 * self.rho * (self.tp/3600)) - (self.K_R101 * pH_R101[-1] * T_R101[-1]  * self.Csus_ini_R101 * (self.tp / 3600)))/(self.VR1+(self.Q_P101*(self.tp/3600)))/self.rho

                #R_102 Conditions
                y0_R102 = float(self.Operation_Data.Csus_ini_R102[0])                                  #intital condition
                VR_R102 = self.VR2                                                                     #Reactor volume                
                pH_R102 = [pH_effect(p) for p in self.Operation_Data.pH_R102.tolist()]
                pH_func_R102 = lambda t: np.interp(t, time, pH_R102)
                T_R102 = [Temperature_effect(p) for p in self.Operation_Data.Temp_R102.tolist()]       #Get Historic Temperature
                T_func_R102 = lambda t: np.interp(t, time, T_R102)
                Qin_R102_1 = (self.Operation_Data.Q_P101/3600).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R102_1 = lambda t: np.interp(t, time, Qin_R102_1)                               #flow in time vector
                Csus_in_R102_1 = self.Operation_Data.Csus_ini_R101.astype(float)                       #Inlet substrate concentration
                Csus_in_func_R102_1 = lambda t: np.interp(t, time, Csus_in_R102_1)                     #Concentration in time vector
                
                #R102 Solution
                self.Csus_ini_R102 = odeint(model_ADM1, y0_R102, time, args=(self.K_R102, VR_R102, pH_func_R102, T_func_R102, Q_func_R102_1, Q_func_R101_1, Csus_in_func_R102_1, Csus_in_func_R102_1, 1)).flatten()
                self.Csus_ini_R102 = self.Csus_ini_R102[-1]
                                
                self.Csus_ini_R102 = self.Csus_ini_R102*mixing_effect(self.RPM_R102)

                # Solidos volátiles en porcentaje R102
                self.SV_R102_p = self.Csus_ini_R102 * self.MW_sustrato / self.rho        #gSV/gT  
                #Sólidos volátiles en gSV/L R102
                self.SV_R102_gL = self.Csus_ini_R102 * self.MW_sustrato                  #gSV/L
                #Carga orgánica en gSV/L.dia R102
                try:
                    if self.GlobalTime == 0:
                        self.Organic_charge_R102 = 0
                    else:
                        self.Organic_charge_R102 = self.SV_R102_gL/(self.GlobalTime*86400)   #gSV/L.dia
                except ZeroDivisionError:
                    self.Organic_charge_R102 = 0
                
                try:
                    if ((self.Csus_ini_R101 * self.MW_sustrato)) / self.rho == 0:
                        self.x_R102 = 0
                    else:
                        self.x_R102 = ((self.Csus_ini_R101 * self.MW_sustrato / self.rho) - self.SV_R102_p)/(self.Csus_ini_R101 * self.MW_sustrato / self.rho)
                except ZeroDivisionError:
                    self.x_R102 = 0

                #Solidos totales R102
                self.ST_R102 = ((self.ST_R102 * self.rho * self.VR2) + (self.Q_P101 * self.ST_R101 * self.rho * (self.tp/3600)) - (self.K_R102 *  T_R102[-1] * pH_R102[-1]) * self.Csus_ini_R102 * (self.tp / 3600))/(self.VR2+(self.Q_P101*(self.tp/3600)))/self.rho

                # Estimación de biogás producido por componente en moles R102 operación 4
                self.mol_CH4_stoichometric_R102 = (self.K_R102 * pH_R102[-1] * T_R102[-1]) * self.Csus_ini_R102 * self.s_CH4 * (self.tp / 3600)
                self.mol_CH4_R102 = self.mol_CH4_R102 + self.mol_CH4_stoichometric_R102
                self.mol_CO2_R102 = self.mol_CH4_R102 * (self.s_CO2/self.s_CH4)
                self.mol_H2S_R102 = self.mol_CH4_R102*(self.s_H2S/self.s_CH4)
                self.mol_NH3_R102 = self.mol_CH4_R102*(self.s_NH3/self.s_CH4)
                self.mol_O2_R102 = self.mol_O2_R102 + self.mol_CH4_stoichometric_R102*np.random.uniform (0, 0.1) 
                self.mol_H2_R102 = self.mol_H2_R102 + self.mol_CH4_stoichometric_R102*np.random.uniform (0, 0.00001)
                self.mol_H2O_R102 = self.mol_H2O_R102 + abs(self.mol_CH4_stoichometric_R102*np.random.normal(0.4, 0.1))
                
            # Estimación de biogás producido por componente en moles R101
            self.mol_CH4_stoichometric_R101 = (self.K_R101 * pH_R101[-1] * T_R101[-1]) * self.Csus_ini_R101 * self.s_CH4 * (self.tp / 3600)
            self.mol_CH4_R101 = self.mol_CH4_R101 + self.mol_CH4_stoichometric_R101
            self.mol_CO2_R101 = self.mol_CH4_R101 * (self.s_CO2/self.s_CH4)
            self.mol_H2S_R101 = self.mol_CH4_R101*(self.s_H2S/self.s_CH4)
            self.mol_NH3_R101 = self.mol_CH4_R101*(self.s_NH3/self.s_CH4)
            self.mol_O2_R101 = self.mol_O2_R101 + self.mol_CH4_stoichometric_R101*np.random.uniform (0, 0.1) 
            self.mol_H2_R101 = self.mol_H2_R101 + self.mol_CH4_stoichometric_R101*np.random.uniform (0, 0.00001)
            self.mol_H2O_R101 = self.mol_H2O_R101 + self.mol_CH4_stoichometric_R101*np.random.normal(0.4, 0.1)

            # Solidos volátiles en porcentaje R101
            self.SV_R101_p = self.Csus_ini_R101 * self.MW_sustrato / self.rho        #gSV/gT  
            #Sólidos volátiles en gSV/L R101
            self.SV_R101_gL = self.Csus_ini_R101 * self.MW_sustrato                  #gSV/L
            #Carga orgánica en gSV/L.dia R101
            try:
                if self.GlobalTime == 0:
                    self.Organic_charge_R101 = 0
                else:
                    self.Organic_charge_R101 = self.SV_R101_gL/(self.GlobalTime*86400)   #gSV/L.dia

            except ZeroDivisionError:
                self.Organic_charge_R101 = 0
            
            try:
                if self.SV == 0:
                    self.x_R101 = 0
                else:
                    self.x_R101 = (self.SV - self.SV_R101_p)/self.SV
            except ZeroDivisionError:
                self.x_R101 = 0

        elif self.Model == "Gompertz":

            time = self.Operation_Data.time.astype(float).tolist()
            pH_R101 = float(self.Operation_Data.pH_R101.iloc[-1])
            T_R101 = float(self.Operation_Data.Temp_R101.iloc[-1])

            if self.OperationMode in ["Modo1", "Modo2"]:
                # Solución de R101
                self.y_CH4_R101 = model_Gompertz(t=time[-1], ym = self.ym_R101, U = self.U_R101, L = self.L_R101)
                self.y_CH4_R101 = self.y_CH4_R101 * pH_effect(pH_R101) * mixing_effect(self.RPM_R101) * Temperature_effect(T_R101)

                # Estimación de biogás producido por componente en moles R101 (fase gaseosa)
                self.mol_CH4_R101 = (self.y_CH4_R101*self.SV*self.rho*self.VR1)/self.Vmolar_CH4
                self.mol_CO2_R101 = self.mol_CH4_R101*(self.s_CO2/self.s_CH4)
                self.mol_H2S_R101 = self.mol_CH4_R101*(self.s_H2S/self.s_CH4)
                self.mol_NH3_R101 = self.mol_CH4_R101*(self.s_NH3/self.s_CH4)
                self.mol_O2_R101 = self.mol_O2_R101 + (self.mol_CH4_R101 - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]) * np.random.uniform (0, 0.1) 
                self.mol_H2_R101 = self.mol_H2_R101 + (self.mol_CH4_R101 - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]) * np.random.uniform (0, 0.00001)
                self.mol_H2O_R101 = self.mol_H2O_R101 + (self.mol_CH4_R101 - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]) * np.random.normal(0.7, 0.1)


                #Estimación de gasto de reactivo límite
                if len (self.Operation_Data.mol_CH4_acum_R101) < 2:
                    self.mol_sus_stoichometric_R101 = self.mol_CH4_R101*(1/self.s_CH4)
                else:
                    self.mol_sus_stoichometric_R101 = self.mol_CH4_R101*(1/self.s_CH4) - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]*(1/self.s_CH4) 
                    if self.mol_sus_stoichometric_R101<0:
                        self.mol_sus_stoichometric_R101 = 0   

                self.Csus_ini_R101 = (self.mol_ini_R101 + (self.Q_P104*(self.tp/3600))*self.Csus_ini - self.mol_sus_stoichometric_R101)/(self.VR1 + self.Q_P104*(self.tp/3600))
                self.mol_ini_R101 = self.Csus_ini_R101*self.VR1

                # Solidos volátiles en porcentaje R101
                self.SV_R101_p = self.Csus_ini_R101 * self.MW_sustrato / self.rho        #gSV/gT  
                #Sólidos volátiles en gSV/L R101
                self.SV_R101_gL = self.Csus_ini_R101 * self.MW_sustrato                  #gSV/L
                #Carga orgánica en gSV/L.dia R101

                try:
                    if self.GlobalTime == 0:
                        self.Organic_charge_R101 = 0
                    else:
                        self.Organic_charge_R101 = self.SV_R101_gL/(self.GlobalTime*86400)   #gSV/L.dia
                except ZeroDivisionError:
                    self.Organic_charge_R101 = 0
                
                try:
                    if self.SV == 0:
                        self.x_R101 = 0
                    else:
                        self.x_R101 = (self.SV - self.SV_R101_p)/self.SV
                except ZeroDivisionError:
                    self.x_R101 = 0

                #Solidos totales R101
                self.ST_R101 = ((self.ST_R101 * self.rho * self.VR1) + (self.Q_P104 * self.ST * self.rho * (self.tp/3600)) - (self.mol_sus_stoichometric_R101 ))/(self.VR1+(self.Q_P104*(self.tp/3600)))/self.rho
            
            if self.OperationMode in ["Modo3", "Modo5"]:
                # Solución de R101
                self.y_CH4_R101 = model_Gompertz(t=time[-1], ym = self.ym_R101, U = self.U_R101, L = self.L_R101)
                self.y_CH4_R101 = self.y_CH4_R101 * pH_effect(pH_R101) * mixing_effect(self.RPM_R101) * Temperature_effect(T_R101)

                # Estimación de biogás producido por componente en moles R101 (fase gaseosa)
                self.mol_CH4_R101 = (self.y_CH4_R101*self.SV*self.rho*self.VR1)/self.Vmolar_CH4
                self.mol_CO2_R101 = self.mol_CH4_R101*(self.s_CO2/self.s_CH4)
                self.mol_H2S_R101 = self.mol_CH4_R101*(self.s_H2S/self.s_CH4)
                self.mol_NH3_R101 = self.mol_CH4_R101*(self.s_NH3/self.s_CH4)
                self.mol_O2_R101 = self.mol_O2_R101 + (self.mol_CH4_R101 - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]) * np.random.uniform (0, 0.1) 
                self.mol_H2_R101 = self.mol_H2_R101 + (self.mol_CH4_R101 - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]) * np.random.uniform (0, 0.00001)
                self.mol_H2O_R101 = self.mol_H2O_R101 + (self.mol_CH4_R101 - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]) * np.random.normal(0.7, 0.1)

                #Estimación de gasto de reactivo límite en R101
                if len (self.Operation_Data.mol_CH4_acum_R101) < 2:
                    self.mol_sus_stoichometric_R101 = self.mol_CH4_R101*(1/self.s_CH4)
                else:
                    self.mol_sus_stoichometric_R101 = self.Operation_Data.mol_CH4_acum_R101.iloc[-2]*(1/self.s_CH4) - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]*(1/self.s_CH4) 
                    if self.mol_sus_stoichometric_R101<0:
                        self.mol_sus_stoichometric_R101 = 0   

                self.Csus_ini_R101 = (self.mol_ini_R101 + (self.Q_P104*(self.tp/3600))*self.Csus_ini - self.mol_sus_stoichometric_R101)/(self.VR1 + self.Q_P104*(self.tp/3600))
                self.mol_ini_R101 = self.Csus_ini_R101*self.VR1

                # Solidos volátiles en porcentaje R101
                self.SV_R101_p = self.Csus_ini_R101 * self.MW_sustrato / self.rho        #gSV/gT  
                #Sólidos volátiles en gSV/L R101
                self.SV_R101_gL = self.Csus_ini_R101 * self.MW_sustrato                  #gSV/L
                #Carga orgánica en gSV/L.dia R101
                
                try:
                    if self.GlobalTime == 0:
                        self.Organic_charge_R101 = 0
                    else:
                        self.Organic_charge_R101 = self.SV_R101_gL/(self.GlobalTime*86400)   #gSV/L.dia
                except ZeroDivisionError:
                    self.Organic_charge_R101 = 0
                
                try:
                    if self.SV == 0:
                        self.x_R101 = 0
                    else:
                        self.x_R101 = (self.SV - self.SV_R101_p)/self.SV
                except ZeroDivisionError:
                    self.x_R101 = 0

                #Solidos totales R101
                self.ST_R101 = ((self.ST_R101 * self.rho * self.VR1) + (self.Q_P104 * self.ST * self.rho * (self.tp/3600)) - (self.mol_sus_stoichometric_R101 ))/(self.VR1+(self.Q_P104*(self.tp/3600)))/self.rho
            
                #entrada de R102
                pH_R102 = float(self.Operation_Data.pH_R102.iloc[-1])
                T_R102 = float(self.Operation_Data.Temp_R102.iloc[-1])

                #Solución de R102
                self.y_CH4_R102 = model_Gompertz(t=time[-1], ym = self.ym_R102, U = self.U_R102, L = self.U_R102)
                self.y_CH4_R102 = self.y_CH4_R102 * pH_effect(pH_R102) * mixing_effect(self.RPM_R102) * Temperature_effect(T_R102)
            
                # Estimación de biogás producido por componente en moles R102 (fase gaseosa)
                self.mol_CH4_R102 = (self.y_CH4_R102*self.SV*self.rho*self.VR1)/self.Vmolar_CH4
                self.mol_CO2_R102 = self.mol_CH4_R102*(self.s_CO2/self.s_CH4)
                self.mol_H2S_R102 = self.mol_CH4_R102*(self.s_H2S/self.s_CH4)
                self.mol_NH3_R102 = self.mol_CH4_R102*(self.s_NH3/self.s_CH4)
                self.mol_O2_R102 = self.mol_O2_R102 + (self.mol_CH4_R102 - self.Operation_Data.mol_CH4_acum_R102 .iloc[-1]) * np.random.uniform (0, 0.1) 
                self.mol_H2_R102 = self.mol_H2_R102 + (self.mol_CH4_R102 - self.Operation_Data.mol_CH4_acum_R102 .iloc[-1]) * np.random.uniform (0, 0.00001)
                self.mol_H2O_R102 = self.mol_H2O_R102 + abs(self.mol_CH4_R102 - self.Operation_Data.mol_CH4_acum_R102 .iloc[-1] * np.random.normal(0.4, 0.1))

                #Estimación de gasto de reactivo límite
                if len (self.Operation_Data.mol_CH4_acum_R102) < 2:
                    self.mol_sus_stoichometric_R102  = 0
                else:
                    self.mol_sus_stoichometric_R102  = self.mol_CH4_R102 *(1/self.s_CH4) - self.Operation_Data.mol_CH4_acum_R102.iloc[-1]*(1/self.s_CH4) 
                    if self.mol_sus_stoichometric_R102 < 0:
                        self.mol_sus_stoichometric_R102  = 0 

                self.Csus_ini_R102 = (self.mol_ini_R102 + (self.Q_P101*(self.tp/3600))*self.Csus_ini_R101 - self.mol_sus_stoichometric_R102)/(self.VR2 + (self.Q_P101*self.tp/3600))
                self.mol_ini_R102 = self.Csus_ini_R102 * self.VR2
        
                # Solidos volátiles en porcentaje R102
                self.SV_R102_p = self.Csus_ini_R102 * self.MW_sustrato / self.rho        #gSV/gT  
                #Sólidos volátiles en gSV/L R102
                self.SV_R102_gL = self.Csus_ini_R102 * self.MW_sustrato                  #gSV/L
                #Carga orgánica en gSV/L.dia R102
                try:
                    if self.GlobalTime == 0:
                        self.Organic_charge_R102 = 0
                    else:
                        self.Organic_charge_R102 = self.SV_R102_gL/(self.GlobalTime*86400)   #gSV/L.dia
                except ZeroDivisionError:
                    self.Organic_charge_R102 = 0
                
                try:
                    if ((self.Csus_ini_R101 * self.MW_sustrato)) / self.rho == 0:
                        self.x_R102 = 0
                    else:
                        self.x_R102 = ((self.Csus_ini_R101 * self.MW_sustrato / self.rho) - self.SV_R102_p)/(self.Csus_ini_R101 * self.MW_sustrato / self.rho)
                except ZeroDivisionError:
                    self.x_R102 = 0

                #Solidos totales R102
                self.ST_R102 = ((self.ST_R102 * self.rho * self.VR2) + (self.Q_P101 * self.ST_R101 * self.rho * (self.tp/3600)) - (self.mol_sus_stoichometric_R102))/(self.VR2+(self.Q_P101*(self.tp/3600)))/self.rho
            
            
            elif self.OperationMode == "Modo4":
                # Solución de R101
                self.y_CH4_R101 = model_Gompertz(t=time[-1], ym = self.ym_R101, U = self.U_R101, L = self.L_R101)
                self.y_CH4_R101 = self.y_CH4_R101 * pH_effect(pH_R101) * mixing_effect(self.RPM_R101) * Temperature_effect(T_R101)

                # Estimación de biogás producido por componente en moles R101 (fase gaseosa)
                self.mol_CH4_R101 = (self.y_CH4_R101*self.SV*self.rho*self.VR1)/self.Vmolar_CH4
                self.mol_CO2_R101 = self.mol_CH4_R101*(self.s_CO2/self.s_CH4)
                self.mol_H2S_R101 = self.mol_CH4_R101*(self.s_H2S/self.s_CH4)
                self.mol_NH3_R101 = self.mol_CH4_R101*(self.s_NH3/self.s_CH4)
                self.mol_O2_R101 = self.mol_O2_R101 + (self.mol_CH4_R101 - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]) * np.random.uniform (0, 0.1) 
                self.mol_H2_R101 = self.mol_H2_R101 + (self.mol_CH4_R101 - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]) * np.random.uniform (0, 0.00001)
                self.mol_H2O_R101 = self.mol_H2O_R101 + (self.mol_CH4_R101 - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]) * np.random.normal(0.7, 0.1)

                #Estimación de gasto de reactivo límite en R101
                if len (self.Operation_Data.mol_CH4_acum_R101) < 2:
                    self.mol_sus_stoichometric_R101 = 0
                else:
                    self.mol_sus_stoichometric_R101 = self.mol_CH4_R101*(1/self.s_CH4) - self.Operation_Data.mol_CH4_acum_R101.iloc[-1]*(1/self.s_CH4) 
                    if self.mol_sus_stoichometric_R101<0:
                        self.mol_sus_stoichometric_R101 = 0   

                self.Csus_ini_R101 = (self.mol_ini_R101 + (self.Q_P104*(self.tp/3600))*self.Csus_ini + (self.Q_P102*(self.tp/3600))*self.Operation_Data.Csus_ini_R102.iloc[-1] - self.mol_sus_stoichometric_R101)/(self.VR1 + self.Q_P101*(self.tp/3600))
                self.mol_ini_R101 = self.Csus_ini_R101*self.VR1

                 # Solidos volátiles en porcentaje R101
                self.SV_R101_p = self.Csus_ini_R101 * self.MW_sustrato / self.rho        #gSV/gT  
                #Sólidos volátiles en gSV/L R101
                self.SV_R101_gL = self.Csus_ini_R101 * self.MW_sustrato                  #gSV/L
                #Carga orgánica en gSV/L.dia R101

                try:
                    if self.GlobalTime == 0:
                        self.Organic_charge_R101 = 0
                    else:
                        self.Organic_charge_R101 = self.SV_R101_gL/(self.GlobalTime*86400)   #gSV/L.dia
                except ZeroDivisionError:
                    self.Organic_charge_R101 = 0
                
                try:
                    if self.SV == 0:
                        self.x_R101 = 0
                    else:
                        self.x_R101 = (self.SV - self.SV_R101_p)/self.SV
                except ZeroDivisionError:
                    self.x_R101 = 0

                #Solidos totales R101
                self.ST_R101 = ((self.ST_R101 * self.rho * self.VR1) + (self.Q_P104 * self.ST * self.rho * (self.tp/3600)) + (self.Q_P102 * self.ST_R102 * self.rho * (self.tp/3600))- (self.mol_sus_stoichometric_R101))/(self.VR1+self.Q_P101*(self.tp/3600))/self.rho

                #entrada de R102
                pH_R102 = float(self.Operation_Data.pH_R102.iloc[-1])
                T_R102 = float(self.Operation_Data.Temp_R102.iloc[-1])

                #Solución de R102
                self.y_CH4_R102 = model_Gompertz(t=time[-1], ym = self.ym_R102, U = self.U_R102, L = self.U_R102)
                self.y_CH4_R102 = self.y_CH4_R102 * pH_effect(pH_R102) * mixing_effect(self.RPM_R102) * Temperature_effect(T_R102)
            
                # Estimación de biogás producido por componente en moles R102 (fase gaseosa)
                self.mol_CH4_R102 = (self.y_CH4_R102*self.SV*self.rho*self.VR1)/self.Vmolar_CH4
                self.mol_CO2_R102 = self.mol_CH4_R102*(self.s_CO2/self.s_CH4)
                self.mol_H2S_R102 = self.mol_CH4_R102*(self.s_H2S/self.s_CH4)
                self.mol_NH3_R102 = self.mol_CH4_R102*(self.s_NH3/self.s_CH4)
                self.mol_O2_R102 = self.mol_O2_R102 + (self.mol_CH4_R102 - self.Operation_Data.mol_CH4_acum_R102 .iloc[-1]) * np.random.uniform (0, 0.1) 
                self.mol_H2_R102 = self.mol_H2_R102 + (self.mol_CH4_R102 - self.Operation_Data.mol_CH4_acum_R102 .iloc[-1]) * np.random.uniform (0, 0.00001)
                self.mol_H2O_R102 = self.mol_H2O_R102 + abs(self.mol_CH4_R102 - self.Operation_Data.mol_CH4_acum_R102 .iloc[-1] * np.random.normal(0.4, 0.1))

                #Estimación de gasto de reactivo límite en R102
                if len (self.Operation_Data.mol_CH4_acum_R102) < 2:
                    self.mol_sus_stoichometric_R102  = 0
                else:
                    self.mol_sus_stoichometric_R102  = self.mol_CH4_R102 *(1/self.s_CH4) - self.Operation_Data.mol_CH4_acum_R102 .iloc[-1]*(1/self.s_CH4) 
                    if self.mol_sus_stoichometric_R102 < 0:
                        self.mol_sus_stoichometric_R102  = 0 

                self.Csus_ini_R102 = (self.mol_ini_R102 + (self.Q_P101*(self.tp/3600))*self.Csus_ini_R101 - self.mol_sus_stoichometric_R102)/(self.VR2 + (self.Q_P101*self.tp/3600))
                self.mol_ini_R102 = self.Csus_ini_R102 * self.VR2

                # Solidos volátiles en porcentaje R102
                self.SV_R102_p = self.Csus_ini_R102 * self.MW_sustrato / self.rho        #gSV/gT  
                #Sólidos volátiles en gSV/L R102
                self.SV_R102_gL = self.Csus_ini_R102 * self.MW_sustrato                  #gSV/L
                #Carga orgánica en gSV/L.dia R102
                try:
                    if self.GlobalTime == 0:
                        self.Organic_charge_R102 = 0
                    else:
                        self.Organic_charge_R102 = self.SV_R102_gL/(self.GlobalTime*86400)   #gSV/L.dia
                except ZeroDivisionError:
                    self.Organic_charge_R102 = 0
                
                try:
                    if ((self.Csus_ini_R101 * self.MW_sustrato)) / self.rho == 0:
                        self.x_R102 = 0
                    else:
                        self.x_R102 = ((self.Csus_ini_R101 * self.MW_sustrato / self.rho) - self.SV_R102_p)/(self.Csus_ini_R101 * self.MW_sustrato / self.rho)
                except ZeroDivisionError:
                    self.x_R102 = 0

                #Solidos totales R102
                self.ST_R102 = ((self.ST_R102 * self.rho * self.VR2) + (self.Q_P101 * self.ST_R101 * self.rho * (self.tp/3600)) - (self.mol_sus_stoichometric_R102))/(self.VR2+(self.Q_P101*(self.tp/3600)))/self.rho
            
        self.GlobalTime = self.GlobalTime + self.tp  

    def V101(self):
        #Acumulated volume
        self.Vnormal_CH4_acum_V101 = self.Vmolar_CH4 * self.mol_CH4_R101
        self.Vnormal_CO2_acum_V101 = self.Vmolar_CO2 * self.mol_CO2_R101
        self.Vnormal_H2S_acum_V101 = self.Vmolar_H2S * self.mol_H2S_R101
        self.Vnormal_O2_acum_V101 = self.Vmolar_O2 * self.mol_O2_R101
        self.Vnormal_NH3_acum_V101 = self.Vmolar_NH3 * self.mol_NH3_R101
        self.Vnormal_H2_acum_V101 = self.Vmolar_H2 * self.mol_H2_R101
        self.Vnormal_H2O_acum_V101 = self.Vmolar_H2O * self.mol_H2O_R101
        
        #Volumen de biogás acumulado
        self.Vnormal_bio_acum_V101 = self.Vnormal_CH4_acum_V101 + self.Vnormal_CO2_acum_V101 + self.Vnormal_H2S_acum_V101 + self.Vnormal_O2_acum_V101 + self.Vnormal_NH3_acum_V101 + self.Vnormal_H2_acum_V101 + self.Vnormal_H2O_acum_V101
        self.mol_bio_acum_V101 = self.mol_CH4_R101 + self.mol_CO2_R101 + self.mol_H2S_R101 + self.mol_NH3_R101 + self.mol_H2_R101 + self.mol_H2O_R101

        # Get temperature from API
        lat = 3.40330   
        lon = -76.54708  
        api_key = "cd9cc586c0098f719bf013730d2d081e"
        url =   f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
           
        if response.status_code == 200:
            self.Temperature = response.json()['main']['temp']
        else:
            self.Temperature = np.random.normal(25, 5)
            
        #Acumulated biogas Pressure in V_101
        self.Pacum_bio_V101 = (((self.mol_bio_acum_V101 * 8.314 * (self.Temperature + 273.15)) / (self.VG1/1000))/6894.76)  #presion en psi

        #storage biogas in V_101
        if self.Pstorage_bio_V101 <= 50:
            
            #Presión biogás almacenada
            self.Pstorage_bio_V101 = self.Pacum_bio_V101 - self.Pini_V101     #Presion en psi
            
            #Moles almacenadas
            self.mol_CH4_V101 = self.mol_CH4_R101 - self.mol_CH4ini_V101
            self.mol_CO2_V101 = self.mol_CO2_R101 - self.mol_CO2ini_V101
            self.mol_H2S_V101 = self.mol_H2S_R101 - self.mol_H2Sini_V101
            self.mol_O2_V101 = self.mol_O2_R101 - self.mol_O2ini_V101
            self.mol_NH3_V101 = self.mol_NH3_R101 - self.mol_NH3ini_V101
            self.mol_H2_V101 = self.mol_H2_R101 - self.mol_H2ini_V101
            self.mol_H2O_V101 = self.mol_H2O_R101 - self.mol_H2Oini_V101
            self.molTotales_V101 = self.mol_CH4_V101 + self.mol_CO2_V101 + self.mol_H2S_V101 + self.mol_O2_V101 + self.mol_NH3_V101 + self.mol_H2_V101 + self.mol_H2O_V101

            #Volumen almacenado
            self.Vnormal_CH4_V101 = self.mol_CH4_V101 * self.Vmolar_CH4
            self.Vnormal_CO2_V101 = self.mol_CO2_V101 * self.Vmolar_CO2
            self.Vnormal_H2S_V101 = self.mol_H2S_V101 * self.Vmolar_H2S
            self.Vnormal_O2_V101 = self.mol_O2_V101 * self.Vmolar_O2
            self.Vnormal_NH3_V101 = self.mol_NH3_V101 * self.Vmolar_NH3
            self.Vnormal_H2_V101 = self.mol_H2_V101 * self.Vmolar_H2
            self.Vnormal_H2O_V101 = self.mol_H2O_V101 * self.Vmolar_H2O

            #Volumen biogás almacenado
            self.Vnormal_bio_V101 = self.Vnormal_CH4_V101 + self.Vnormal_CO2_V101 + self.Vnormal_H2S_V101 + self.Vnormal_O2_V101 + self.Vnormal_NH3_V101 + self.Vnormal_H2_V101 + self.Vnormal_H2O_V101

            #humedad relativa
            self.RH_V101 = self.Thermo.BiogasRelativeHumidity(nH2O = self.mol_H2O_V101, VnormalTotal = self.Vnormal_bio_V101, T = self.Temperature)

            #concentración
            try:
                if self.molTotales_V101 == 0 or np.isnan(self.molTotales_V101):
                    raise ValueError("Vnormal_bio_V101 is zero or NaN")
                self.x_CH4_V101 = self.mol_CH4_V101 / self.molTotales_V101
                self.x_CO2_V101 = self.mol_CO2_V101 / self.molTotales_V101
                self.x_H2S_V101 = self.mol_H2S_V101 / self.molTotales_V101
                self.x_O2_V101 = self.mol_O2_V101 / self.molTotales_V101
                self.x_NH3_V101 = self.mol_NH3_V101 / self.molTotales_V101
                self.x_H2_V101 = self.mol_H2_V101 / self.molTotales_V101
                self.x_H2O_V101 = self.mol_H2O_V101 / self.molTotales_V101
                if any(np.isnan(value) or np.isinf(value) for value in [
                    self.x_CH4_V101, self.x_CO2_V101, self.x_H2S_V101, 
                    self.x_O2_V101, self.x_NH3_V101, self.x_H2_V101, 
                    self.x_H2O_V101]):
                    raise ValueError("Invalid result encountered in gas composition calculations")
            except (ZeroDivisionError, ValueError):
                self.x_CH4_V101 = 0
                self.x_CO2_V101 = 0
                self.x_H2S_V101 = 0
                self.x_O2_V101 = 0
                self.x_NH3_V101 = 0
                self.x_H2_V101 = 0
                self.x_H2O_V101 = 0
            
            self.mol_CH4_transfertoV102 = 0
            self.mol_CO2_transfertoV102 = 0
            self.mol_H2S_transfertoV102 = 0
            self.mol_O2_transfertoV102 = 0
            self.mol_NH3_transfertoV102 = 0
            self.mol_H2_transfertoV102 = 0
            self.mol_H2O_transfertoV102 = 0

            #energía
            self.Energy_V101 = self.Thermo.LHV(molCH4 = self.mol_CH4_V101, molCO2 = self.mol_CO2_V101, molH2S = self.mol_H2S_V101,
                                               molO2 = self.mol_O2_V101, molH2 = self.mol_H2_V101)[1]

        else:

            self.Pini_V101 = self.Pstorage_bio_V101
            self.mol_CH4ini_V101 = self.mol_CH4_V101
            self.mol_CO2ini_V101 = self.mol_CO2_V101
            self.mol_H2Sini_V101 = self.mol_H2S_V101
            self.mol_O2ini_V101 = self.mol_O2_V101
            self.mol_NH3ini_V101 = self.mol_NH3_V101
            self.mol_H2ini_V101 = self.mol_H2_V101
            self.mol_H2Oini_V101 = self.mol_H2O_V101
            
            self.mol_CH4_transfertoV102 = self.mol_CH4_V101
            self.mol_CO2_transfertoV102 = self.mol_CO2_V101
            self.mol_H2S_transfertoV102 = self.mol_H2S_V101
            self.mol_O2_transfertoV102 = self.mol_O2_V101
            self.mol_NH3_transfertoV102 = self.mol_NH3_V101
            self.mol_H2_transfertoV102 = self.mol_H2_V101
            self.mol_H2O_transfertoV102 = self.mol_H2O_V101

            self.Pstorage_bio_V101 = 0
            self.mol_CH4_V101 = 0
            self.mol_CO2_V101 = 0
            self.mol_H2S_V101 = 0
            self.mol_O2_V101 = 0
            self.mol_NH3_V101 = 0
            self.mol_H2_V101 = 0
            self.mol_H2O_V101 = 0
            self.Vnormal_bio_V101 = 0

            self.Energy_V101 = 0
    
    def V102(self):

        #Accumulated trnasfer biogas
        self.mol_CH4_transfertoV102i = self.mol_CH4_transfertoV102i + self.mol_CH4_transfertoV102
        self.mol_CO2_transfertoV102i = self.mol_CO2_transfertoV102i + self.mol_CO2_transfertoV102
        self.mol_H2S_transfertoV102i = self.mol_H2S_transfertoV102i + self.mol_H2S_transfertoV102
        self.mol_O2_transfertoV102i = self.mol_O2_transfertoV102i + self.mol_O2_transfertoV102
        self.mol_NH3_transfertoV102i = self.mol_NH3_transfertoV102i + self.mol_NH3_transfertoV102
        self.mol_H2_transfertoV102i = self.mol_H2_transfertoV102i + self.mol_H2_transfertoV102
        self.mol_H2O_transfertoV102i = self.mol_H2O_transfertoV102i + self.mol_H2O_transfertoV102     

        #Acumulated volume
        self.Vnormal_CH4_acum_V102 = self.Vmolar_CH4 * (self.mol_CH4_R102 + self.mol_CH4_transfertoV102i)
        self.Vnormal_CO2_acum_V102 = self.Vmolar_CO2 * (self.mol_CO2_R102 + self.mol_CO2_transfertoV102i)
        self.Vnormal_H2S_acum_V102 = self.Vmolar_H2S * (self.mol_H2S_R102 + self.mol_H2S_transfertoV102i)
        self.Vnormal_O2_acum_V102 = self.Vmolar_O2 * (self.mol_O2_R102 + self.mol_O2_transfertoV102i)
        self.Vnormal_NH3_acum_V102 = self.Vmolar_NH3 * (self.mol_NH3_R102 + self.mol_NH3_transfertoV102i)
        self.Vnormal_H2_acum_V102 = self.Vmolar_H2 * (self.mol_H2_R102 + self.mol_H2_transfertoV102i)
        self.Vnormal_H2O_acum_V102 = self.Vmolar_H2O * (self.mol_H2O_R102 + self.mol_H2O_transfertoV102i)

        #Volumen de biogás acumulado
        self.Vnormal_bio_acum_V102 = self.Vnormal_CH4_acum_V102 + self.Vnormal_CO2_acum_V102 + self.Vnormal_H2S_acum_V102 + self.Vnormal_O2_acum_V102 + self.Vnormal_NH3_acum_V102 + self.Vnormal_H2_acum_V102 + self.Vnormal_H2O_acum_V102
        self.mol_bio_acum_V102 = ((self.mol_CH4_R102 + self.mol_CH4_transfertoV102) + (self.mol_CO2_R102 + self.mol_CO2_transfertoV102) + 
                                  (self.mol_H2S_R102 + self.mol_H2S_transfertoV102) + (self.mol_O2_R102 + self.mol_O2_transfertoV102) +
                                   (self.mol_NH3_R102 + self.mol_NH3_transfertoV102) + (self.mol_H2_R102 + self.mol_H2_transfertoV102) + 
                                   (self.mol_H2O_R102 + self.mol_H2O_transfertoV102))

        #Acumulated biogas Pressure in V_102
        self.Pacum_bio_V102 = (((self.mol_bio_acum_V102 * 8.314 * (self.Temperature + 273.15)) / (self.VG2/1000))/6894.76)  #presion en psi

        #storage biogas in V_102
        if self.Pstorage_bio_V102 <= 50:
            
            #Presión biogás almacenada
            self.Pstorage_bio_V102 = self.Pacum_bio_V102 - self.Pini_V102     #Presion en psi

            #Moles almacenadas
            self.mol_CH4_V102 = (self.mol_CH4_R102 + self.mol_CH4_transfertoV102) - self.mol_CH4ini_V102
            self.mol_CO2_V102 = (self.mol_CO2_R102 + self.mol_CO2_transfertoV102) - self.mol_CO2ini_V102
            self.mol_H2S_V102 = (self.mol_H2S_R102 + self.mol_H2S_transfertoV102) - self.mol_H2Sini_V102
            self.mol_O2_V102 = (self.mol_O2_R102 + self.mol_O2_transfertoV102) - self.mol_O2ini_V102
            self.mol_NH3_V102 = (self.mol_NH3_R102 + self.mol_NH3_transfertoV102) - self.mol_NH3ini_V102
            self.mol_H2_V102 = (self.mol_H2_R102 + self.mol_H2_transfertoV102) - self.mol_H2ini_V102
            self.mol_H2O_V102 = (self.mol_H2O_R102 + self.mol_H2O_transfertoV102) - self.mol_H2Oini_V102
            self.molTotales_V102 = self.mol_CH4_V102 + self.mol_CO2_V102 + self.mol_H2S_V102 + self.mol_O2_V102 + self.mol_NH3_V102 + self.mol_H2_V102 + self.mol_H2O_V102

            #Volumen almacenado
            self.Vnormal_CH4_V102 = self.mol_CH4_V102 * self.Vmolar_CH4
            self.Vnormal_CO2_V102 = self.mol_CO2_V102 * self.Vmolar_CO2
            self.Vnormal_H2S_V102 = self.mol_H2S_V102 * self.Vmolar_H2S
            self.Vnormal_O2_V102 = self.mol_O2_V102 * self.Vmolar_O2
            self.Vnormal_NH3_V102 = self.mol_NH3_V102 * self.Vmolar_NH3
            self.Vnormal_H2_V102 = self.mol_H2_V102 * self.Vmolar_H2
            self.Vnormal_H2O_V102 = self.mol_H2O_V102 * self.Vmolar_H2O

            #Volumen biogás almacenado
            self.Vnormal_bio_V102 = self.Vnormal_CH4_V102 + self.Vnormal_CO2_V102 + self.Vnormal_H2S_V102 + self.Vnormal_O2_V102 + self.Vnormal_NH3_V102 + self.Vnormal_H2_V102 + self.Vnormal_H2O_V102

            #humedad relativa
            self.RH_V102 = self.Thermo.BiogasRelativeHumidity(nH2O = self.mol_H2O_V102, VnormalTotal = self.Vnormal_bio_V102, T = self.Temperature)

            #concentración
            try:
                if self.molTotales_V102 == 0 or np.isnan(self.molTotales_V102):
                    raise ValueError("Vnormal_bio_V102 is zero or NaN")
                self.x_CH4_V102 = self.mol_CH4_V102 / self.molTotales_V102
                self.x_CO2_V102 = self.mol_CO2_V102 / self.molTotales_V102
                self.x_H2S_V102 = self.mol_H2S_V102 / self.molTotales_V102
                self.x_O2_V102 = self.mol_O2_V102 / self.molTotales_V102
                self.x_NH3_V102 = self.mol_NH3_V102 / self.molTotales_V102
                self.x_H2_V102 = self.mol_H2_V102 / self.molTotales_V102
                self.x_H2O_V102 = self.mol_H2O_V102 / self.molTotales_V102
                if any(np.isnan(value) or np.isinf(value) for value in [
                    self.x_CH4_V102, self.x_CO2_V102, self.x_H2S_V102, 
                    self.x_O2_V102, self.x_NH3_V102, self.x_H2_V102, 
                    self.x_H2O_V102]):
                    raise ValueError("Invalid result encountered in gas composition calculations")
            except (ZeroDivisionError, ValueError):
                self.x_CH4_V102 = 0
                self.x_CO2_V102 = 0
                self.x_H2S_V102 = 0
                self.x_O2_V102 = 0
                self.x_NH3_V102 = 0
                self.x_H2_V102 = 0
                self.x_H2O_V102 = 0
            
            self.mol_CH4_transfertoV107 = 0
            self.mol_CO2_transfertoV107 = 0
            self.mol_H2S_transfertoV107 = 0
            self.mol_O2_transfertoV107 = 0
            self.mol_NH3_transfertoV107 = 0
            self.mol_H2_transfertoV107 = 0
            self.mol_H2O_transfertoV107 = 0

            self.C_H2S = 0
            self.C_NH3 = 0
            self.C_H2O = 0

            #energía
            self.Energy_V102 = self.Thermo.LHV(molCH4 = self.mol_CH4_V102, molCO2 = self.mol_CO2_V102, molH2S = self.mol_H2S_V102,
                                               molO2 = self.mol_O2_V102, molH2 = self.mol_H2_V102)[1]
        
        else:

            self.Pini_V102 = self.Pstorage_bio_V102
            self.mol_CH4ini_V102 = self.mol_CH4_V102
            self.mol_CO2ini_V102 = self.mol_CO2_V102
            self.mol_H2Sini_V102 = self.mol_H2S_V102
            self.mol_O2ini_V102 = self.mol_O2_V102
            self.mol_NH3ini_V102 = self.mol_NH3_V102
            self.mol_H2ini_V102 = self.mol_H2_V102
            self.mol_H2Oini_V102 = self.mol_H2O_V102

            self.Pstorage_bio_V102 = 0

            self.mol_CH4_transfertoV107 = self.mol_CH4_V102
            self.mol_CO2_transfertoV107 = self.mol_CO2_V102
            self.mol_H2S_transfertoV107 = self.mol_H2S_V102
            self.mol_O2_transfertoV107 = self.mol_O2_V102
            self.mol_NH3_transfertoV107 = self.mol_NH3_V102
            self.mol_H2_transfertoV107 = self.mol_H2_V102
            self.mol_H2O_transfertoV107 = self.mol_H2O_V102

            try:
                if self.Vnormal_bio_acum_V102 == 0:
                    self.C_H2S = 0
                else:
                    self.C_H2S = self.mol_H2S_transfertoV107/self.Vnormal_bio_acum_V102
                    self.C_NH3 = self.mol_NH3_transfertoV107/self.Vnormal_bio_acum_V102
                    self.C_H2O = self.mol
            except ZeroDivisionError:
                self.C_H2S = 0

            self.mol_CH4_V102 = 0
            self.mol_CO2_V102 = 0
            self.mol_H2S_V102 = 0
            self.mol_O2_V102 = 0
            self.mol_NH3_V102 = 0
            self.mol_H2_V102 = 0
            self.mol_H2O_V102 = 0
            self.Vnormal_bio_V102 = 0

            self.Energy_V102 = 0
    
    def Biogas_treatment (self, D1, W1, L1, D2, W2, L2, D3, W3, L3):
        

        def AdsortiaTower (N, t, Nin, D, W, L):
            if W == 0:
                return 0
            else:
                dN_dt = D/(W*L**2)*(Nin - N) - (N / W)
            return dN_dt
        
        #time for all process
        t = np.linspace(self.GlobalTime, self.GlobalTime + self.tp, 5) 
        #Tower 1 - Hydrogen sulfur
        #in 
        N0_1 = self.N0_1
        Nin_1 = self.C_H2S
        #process
        results_T1 = odeint(AdsortiaTower, N0_1, t, args = (Nin_1, D1, W1, L1))
        #out
        self.N0_1 = float(results_T1[-1])
        self.C_H2S_out = Nin_1 - self.N0_1
        self.mol_H2S_ads = self.N0_1 * self.Vnormal_bio_V102
        self.mol_H2S_transfertoV107 = self.C_H2S_out * self.Vnormal_bio_V102

        #Tower 2 - Amonia
        #in   
        N0_2 = self.N0_2
        Nin_2 = self.C_NH3
        #process
        results_T2 = odeint(AdsortiaTower, N0_2, t, args = (Nin_2, D2, W2, L2))
        #out
        self.N0_2 = float(results_T2[-1])
        self.C_NH3_out = Nin_2 - self.N0_2
        self.mol_NH3_ads = self.N0_2 * self.Vnormal_bio_V102
        self.mol_NH3_transfertoV107 = self.C_NH3_out * self.Vnormal_bio_V102

        #Tower 3 - Agua
        #in   
        N0_3 = self.N0_3
        Nin_3 = self.C_H2O
        #process
        results_T3 = odeint(AdsortiaTower, N0_3, t, args = (Nin_3, D3, W3, L3))
        #out
        self.N0_3 = float(results_T3[-1])
        self.C_H2O_out = Nin_3 - self.N0_3
        self.mol_H2O_ads = self.N0_3 * self.Vnormal_bio_V102
        self.mol_H2O_transfertoV107 = self.C_H2O_out * self.Vnormal_bio_V102

        mol_ads = self.mol_H2S_ads + self.mol_NH3_ads + self.mol_H2O_ads
        mol_in = (self.mol_H2S_R102 + self.mol_H2S_transfertoV102) + (self.mol_NH3_R102 + self.mol_NH3_transfertoV102) + (self.mol_H2O_R102 + self.mol_H2O_transfertoV102)

        try:
            if mol_in == 0:
                self.x_tower = 0
            else:
                self.x_tower = (mol_ads/mol_in)
        except ZeroDivisionError:
            self.x_tower = 0 
    
    def V107 (self):
        #Acumulated trnasfer
        self.mol_CH4_transfertoV107i = self.mol_CH4_transfertoV107i + self.mol_CH4_transfertoV107
        self.mol_CO2_transfertoV107i = self.mol_CO2_transfertoV107i + self.mol_CO2_transfertoV107
        self.mol_H2S_transfertoV107i = self.mol_H2S_transfertoV107i + self.mol_H2S_transfertoV107
        self.mol_O2_transfertoV107i = self.mol_O2_transfertoV107i + self.mol_O2_transfertoV107
        self.mol_NH3_transfertoV107i = self.mol_NH3_transfertoV107i + self.mol_NH3_transfertoV107
        self.mol_H2_transfertoV107i = self.mol_H2_transfertoV107i + self.mol_H2_transfertoV107 
        self.mol_H2O_transfertoV107i = self.mol_H2O_transfertoV107i + self.mol_H2O_transfertoV107 

        #Acumulated Volume
        self.Vnormal_CH4_acum_V107 = self.Vmolar_CH4 * (self.mol_CH4_transfertoV107i)
        self.Vnormal_CO2_acum_V107 = self.Vmolar_CO2 * (self.mol_CO2_transfertoV107i)
        self.Vnormal_H2S_acum_V107 = self.Vmolar_H2S * (self.mol_H2S_transfertoV107i)
        self.Vnormal_O2_acum_V107 = self.Vmolar_O2 * (self.mol_O2_transfertoV107i)
        self.Vnormal_NH3_acum_V107 = self.Vmolar_NH3 * (self.mol_NH3_transfertoV107i)
        self.Vnormal_H2_acum_V107 = self.Vmolar_H2 * (self.mol_H2_transfertoV107i)
        self.Vnormal_H2O_acum_V107 = self.Vmolar_H2O * (self.mol_H2O_transfertoV107i)

        #Volumen de biogás acumulado
        self.Vnormal_bio_acum_V107 = self.Vnormal_CH4_acum_V107 + self.Vnormal_CO2_acum_V107 + self.Vnormal_H2S_acum_V107 + self.Vnormal_O2_acum_V107 + self.Vnormal_NH3_acum_V107 + self.Vnormal_H2_acum_V107 + self.Vnormal_H2O_acum_V107
        self.mol_bio_acum_V107 = (self.mol_CH4_transfertoV107 + self.mol_CO2_transfertoV107 + self.mol_H2S_transfertoV107 + self.mol_O2_transfertoV107 + self.mol_NH3_transfertoV107 + self.mol_H2_transfertoV107 + self.mol_H2O_transfertoV107)

        #Acumulated biogas Pressure in V_107
        self.Pacum_bio_V107 = (((self.mol_bio_acum_V107 * 8.314 * (self.Temperature + 273.15)) / (self.VG3/1000))/6894.76)  #presion en psi

        #storage biogas in V_107
        if self.Pstorage_bio_V107 <= 50:
            
            #Presión biogás almacenada
            self.Pstorage_bio_V107 = self.Pacum_bio_V107 - self.Pini_V107     #Presion en psi

            #Moles almacenadas
            self.mol_CH4_V107 = (self.mol_CH4_transfertoV107) - self.mol_CH4ini_V107
            self.mol_CO2_V107 = (self.mol_CO2_transfertoV107) - self.mol_CO2ini_V107
            self.mol_H2S_V107 = (self.mol_H2S_transfertoV107) - self.mol_H2Sini_V107
            self.mol_O2_V107 = (self.mol_O2_transfertoV107) - self.mol_O2ini_V107
            self.mol_NH3_V107 = (self.mol_NH3_transfertoV107) - self.mol_NH3ini_V107
            self.mol_H2_V107 = (self.mol_H2_transfertoV107) - self.mol_H2ini_V107
            self.mol_H2O_V107 = (self.mol_H2O_transfertoV107) - self.mol_H2Oini_V107
            self.molTotales_V107 = self.mol_CH4_V107 + self.mol_CO2_V107 + self.mol_H2S_V107 + self.mol_O2_V107 + self.mol_NH3_V107 + self.mol_H2_V107 + self.mol_H2O_V107

            #Volumen almacenado
            self.Vnormal_CH4_V107 = self.mol_CH4_V107 * self.Vmolar_CH4
            self.Vnormal_CO2_V107 = self.mol_CO2_V107 * self.Vmolar_CO2
            self.Vnormal_H2S_V107 = self.mol_H2S_V107 * self.Vmolar_H2S
            self.Vnormal_O2_V107 = self.mol_O2_V107 * self.Vmolar_O2
            self.Vnormal_NH3_V107 = self.mol_NH3_V107 * self.Vmolar_NH3
            self.Vnormal_H2_V107 = self.mol_H2_V107 * self.Vmolar_H2
            self.Vnormal_H2O_V107 = self.mol_H2O_V107 * self.Vmolar_H2O

            #Volumen biogás almacenado
            self.Vnormal_bio_V107 = self.Vnormal_CH4_V107 + self.Vnormal_CO2_V107 + self.Vnormal_H2S_V107 + self.Vnormal_O2_V107 + self.Vnormal_NH3_V107 + self.Vnormal_H2_V107 + self.Vnormal_H2O_V107

            #humedad relativa
            self.RH_V107 = self.Thermo.BiogasRelativeHumidity(nH2O = self.mol_H2O_V107, VnormalTotal = self.Vnormal_bio_V107, T = self.Temperature)

            #concentración
            try:
                if self.molTotales_V107 == 0 or np.isnan(self.molTotales_V107):
                    self.x_CH4_V107 = 0
                    self.x_CO2_V107 = 0
                    self.x_H2S_V107 = 0
                    self.x_O2_V107 = 0
                    self.x_NH3_V107 = 0
                    self.x_H2_V107 = 0
                    self.x_H2O_V107 = 0
                else:
                    self.x_CH4_V107 = self.mol_CH4_V107 / self.molTotales_V107
                    self.x_CO2_V107 = self.mol_CO2_V107 / self.molTotales_V107
                    self.x_H2S_V107 = self.mol_H2S_V107 / self.molTotales_V107
                    self.x_O2_V107 = self.mol_O2_V107 / self.molTotales_V107
                    self.x_NH3_V107 = self.mol_NH3_V107 / self.molTotales_V107
                    self.x_H2_V107 = self.mol_H2_V107 / self.molTotales_V107
                    self.x_H2O_V107 = self.mol_H2O_V107 / self.molTotales_V107
                if any(np.isnan(value) or np.isinf(value) for value in [
                    self.x_CH4_V107, self.x_CO2_V107, self.x_H2S_V107, 
                    self.x_O2_V107, self.x_NH3_V107, self.x_H2_V107, 
                    self.x_H2O_V107]):
                    raise ValueError("Invalid result encountered in gas composition calculations")
            except (ZeroDivisionError, ValueError):
                self.x_CH4_V107 = 0
                self.x_CO2_V107 = 0
                self.x_H2S_V107 = 0
                self.x_O2_V107 = 0
                self.x_NH3_V107 = 0
                self.x_H2_V107 = 0
                self.x_H2O_V107 = 0

            #energía
            self.Energy_V107 = self.Thermo.LHV(molCH4 = self.mol_CH4_V107, molCO2 = self.mol_CO2_V107, molH2S = self.mol_H2S_V107,
                                               molO2 = self.mol_O2_V107, molH2 = self.mol_H2_V107)[1]
        else:

            self.Pini_V107 = self.Pstorage_bio_V107
            self.mol_CH4ini_V107 = self.mol_CH4_V107
            self.mol_CO2ini_V107 = self.mol_CO2_V107
            self.mol_H2Sini_V107 = self.mol_H2S_V107
            self.mol_O2ini_V107 = self.mol_O2_V107
            self.mol_NH3ini_V107 = self.mol_NH3_V107
            self.mol_H2ini_V107 = self.mol_H2_V107
            self.mol_H2Oini_V107 = self.mol_H2O_V107

            self.Pstorage_bio_V107 = 0

            self.mol_CH4_V107 = 0
            self.mol_CO2_V107 = 0
            self.mol_H2S_V107 = 0
            self.mol_O2_V107 = 0
            self.mol_NH3_V107 = 0
            self.mol_H2_V107 = 0
            self.mol_H2O_V107 = 0
            self.Vnormal_bio_V107 = 0

            self.Energy_V107 = 0

        
        
        
        

                            

        





            