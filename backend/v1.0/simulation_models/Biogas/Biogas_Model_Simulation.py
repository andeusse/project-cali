import pandas as pd
from datetime import datetime
from simulation_models.Biogas import ThermoProperties as TP
from  tools import DBManager
import numpy as np
from scipy.integrate import odeint


class BiogasPlantSimulation:

    def __init__(self, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, 
                 ST_R101=10, SV_R101=1, Cc_R101=40.48, Ch_R101=5.29, Co_R101=29.66, Cn_R101=1.37, Cs_R101=0.211, rho_R101=1000,
                 ST_R102=10, SV_R102=1, Cc_R102=40.48, Ch_R102=5.29, Co_R102=29.66, Cn_R102=1.37, Cs_R102=0.211, rho_R102=1000, OperationMode=1):

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
        #Biogas V_101
        self.Pacum_V101 = 0
        self.P_ini_V101 = 0
        #Biogas V_102
        self.Pacum_V102 = 0
        self.P_ini_V102 = 0
        #Biogas V_107
        self.Pacum_V107 = 0
        self.P_ini_V107 = 0
        
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

            self.mol_min_R101 = min(self.molC_R101, self.molH_R101, self.molO_R101, self.molN_R101, self.molS_R101)

            self.n_R101 = self.molC_R101/self.mol_min_R101
            self.a_R101 = self.molH_R101/self.mol_min_R101
            self.b_R101 = self.molO_R101/self.mol_min_R101
            self.c_R101 = self.molN_R101/self.mol_min_R101
            self.d_R101 = self.molS_R101/self.mol_min_R101
            
            self.s_H2O_R101 = self.n_R101-(self.a_R101/4)-(self.b_R101/2)+(3/4)*self.c_R101+(self.d_R101/2)
            self.s_CH4_R101 = (self.n_R101/2)+(self.a_R101/8)-(self.b_R101/4)-(3/8)*self.c_R101-(self.d_R101/4)
            self.s_CO2_R101 = (self.n_R101/2)-(self.a_R101/8)+(self.b_R101/4)+(3/8)*self.c_R101-(self.d_R101/4)
            self.s_NH3_R101 = self.c_R101
            self.s_H2S_R101 = self.d_R101
            
            self.MW_sustrato_R101 = self.n_R101*12.01+self.a_R101*1.01+self.b_R101*16+self.c_R101*14+self.d_R101*32
            self.Csus_ini_R101 = (self.rho_R101*self.SV_R101)/self.MW_sustrato_R101
            self.Csus_ini_ST_R101 = (self.rho_R101*self.ST_R101)/self.MW_sustrato_R101
            self.Csus_fixed_R101 = self.Csus_ini_ST_R101 - self.Csus_ini_R101
            
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

            self.mol_min_R102 = min(self.molC_R102, self.molH_R102, self.molO_R102, self.molN_R102, self.molS_R102)

            self.n_R102 = self.molC_R102/self.mol_min_R102
            self.a_R102 = self.molH_R102/self.mol_min_R102
            self.b_R102 = self.molO_R102/self.mol_min_R102
            self.c_R102 = self.molN_R102/self.mol_min_R102
            self.d_R102 = self.molS_R102/self.mol_min_R102
            
            self.s_H2O_R102 = self.n_R102-(self.a_R102/4)-(self.b_R102/2)+(3/4)*self.c_R102+(self.d_R102/2)
            self.s_CH4_R102 = (self.n_R102/2)+(self.a_R102/8)-(self.b_R102/4)-(3/8)*self.c_R102-(self.d_R102/4)
            self.s_CO2_R102 = (self.n_R102/2)-(self.a_R102/8)+(self.b_R102/4)+(3/8)*self.c_R102-(self.d_R102/4)
            self.s_NH3_R102 = self.c_R102
            self.s_H2S_R102 = self.d_R102
            
            self.MW_sustrato_R102 = self.n_R102*12.01+self.a_R102*1.01+self.b_R102*16+self.c_R102*14+self.d_R102*32
            self.Csus_ini_R102 = (self.rho_R102*self.SV_R102)/self.MW_sustrato_R102
            self.Csus_ini_ST_R102 = (self.rho_R102*self.ST_R102)/self.MW_sustrato_R102
            self.Csus_fixed_R102 = self.Csus_ini_ST_R102 - self.Csus_ini_R102
        
        if self.OperationMode ==1:
            columns = ["time"
                    , "Q_P104"
                    , "Temp_R101"
                    , "Csus_ini"
                    , "Csus_ini_R101"]
        elif self.OperationMode ==2:
            columns = ["time"
                    , "Q_P104"
                    , "Q_P101"
                    , "Temp_R101"
                    , "Csus_ini"
                    , "Csus_ini_R101"]
        elif self.OperationMode ==3:
            columns = ["time"
                    , "Q_P104"
                    , "Q_P101"
                    , "Temp_R101"
                    , "Temp_R102"
                    , "Csus_ini"
                    , "Csus_ini_R101"
                    , "Csus_ini_R102"]
        elif self.OperationMode in [4,5]:
            columns = ["time"
                    , "Q_P104"
                    , "Q_P101"
                    , "Q_P102"
                    , "Temp_R101"
                    , "Temp_R102"
                    , "Csus_ini"
                    , "Csus_ini_R101"
                    , "Csus_ini_R102"]
            
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

        self.mol_min = min(self.molC, self.molH, self.molO, self.molN, self.molS)

        self.n = self.molC/self.mol_min
        self.a = self.molH/self.mol_min
        self.b = self.molO/self.mol_min
        self.c = self.molN/self.mol_min
        self.d = self.molS/self.mol_min
        
        self.s_H2O = self.n-(self.a/4)-(self.b/2)+(3/4)*self.c+(self.d/2)
        self.s_CH4 = (self.n/2)+(self.a/8)-(self.b/4)-(3/8)*self.c-(self.d/4)
        self.s_CO2 = (self.n/2)-(self.a/8)+(self.b/4)+(3/8)*self.c-(self.d/4)
        self.s_NH3 = self.c
        self.s_H2S = self.d
        
        self.MW_sustrato = self.n*12.01+self.a*1.01+self.b*16+self.c*14+self.d*32
        self.Csus_ini = (self.rho*self.SV)/self.MW_sustrato
        self.Csus_ini_ST = (self.rho*self.ST)/self.MW_sustrato
        self.Csus_fixed = self.Csus_ini_ST - self.Csus_ini
    
    def Pump104 (self, TRH=30, FT_P104=5, TTO_P104=10):    
        
        self.TRH = TRH
        self.FT_P104 = FT_P104
        self.TTO_P104 = TTO_P104
        try:
            self.TurnOnDailyStep_P104 = 24/self.FT_P104
        except ZeroDivisionError:
            self.TurnOnDailyStep_P104=0
        
        if self.OperationMode == 1 or self.OperationMode == 2:
            self.Q_daily = self.VR1/self.TRH
        
        elif self.OperationMode == 3 or self.OperationMode == 4 or self.OperationMode == 5:
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
        

        #testing model    
        print("Tiempo de encendido de la bomba P_104: "+str(self.TimeCounterPump_P104))
        print("Caudal de la bomba P_104: "+ str(self.Q_P104))
        
    def Pump101 (self, FT_P101=5, TTO_P101=10, Q_P101 = 2.4):
        
        if self.OperationMode == 1:
            pass

        elif self.OperationMode == 2:
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

        elif self.OperationMode == 3 or self.OperationMode == 5:
            self.Q_P101 = self.Q_P104

        elif self.OperationMode == 4:
            
            try:
                self.Q_P102 = self.Q_P102
            except:
                self.Q_P102 = 0

            self.Q_P101 = self.Q_P104 + self.Q_P102
    
    def Pump102 (self, FT_P102=5, TTO_P102=10, Q_P102 = 2.4):
        
        if self.OperationMode == 1 or self.OperationMode == 2 or self.OperationMode == 3:
            pass

        elif self.OperationMode == 4 or self.OperationMode == 5:
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
    
    def Data_simulation(self, Temperature_R101=35, Temperature_R102=35):
        self.Temp_R101=Temperature_R101
        self.Temp_R102=Temperature_R102
        if self.OperationMode == 1:
            new_row = pd.DataFrame({"time": [self.GlobalTime],
                                    "Q_P104" : [self.Q_P104],
                                    "Temp_R101": [self.Temp_R101],
                                    "Csus_ini" : [self.Csus_ini],
                                    "Csus_ini_R101" : [self.Csus_ini_R101]})
        elif self.OperationMode == 2:
             new_row = pd.DataFrame({"time": [self.GlobalTime],
                                    "Q_P104" : [self.Q_P104],
                                    "Q_P101" : [self.Q_P101],
                                    "Temp_R101": [self.Temp_R101],
                                    "Csus_ini" : [self.Csus_ini],
                                    "Csus_ini_R101" : [self.Csus_ini_R101]})
        
        elif self.OperationMode == 3:
            new_row = pd.DataFrame({"time": [self.GlobalTime],
                                    "Q_P104" : [self.Q_P104],
                                    "Q_P101" : [self.Q_P101],
                                    "Temp_R101": [self.Temp_R101],
                                    "Temp_R102":[self.Temp_R102],
                                    "Csus_ini" : [self.Csus_ini],
                                    "Csus_ini_R101" : [self.Csus_ini_R101],
                                    "Csus_ini_R102" : [self.Csus_ini_R102]})

        elif self.OperationMode in [3,4,5]:
            new_row = pd.DataFrame({"time": [self.GlobalTime],
                                    "Q_P104" : [self.Q_P104],
                                    "Q_P101" : [self.Q_P101],
                                    "Q_P102" : [self.Q_P102],
                                    "Temp_R101": [self.Temp_R101],
                                    "Temp_R102":[self.Temp_R102],
                                    "Csus_ini" : [self.Csus_ini],
                                    "Csus_ini_R101" : [self.Csus_ini_R101],
                                    "Csus_ini_R102" : [self.Csus_ini_R102]})
        
        self.Operation_Data = pd.concat([self.Operation_Data, new_row], ignore_index=True)

    def ReactorSimulation(self, Model, A_R101, B_R101, C_R101, A_R102=1, B_R102=1, C_R102=1):
        self.Model = Model

        def model_Arrehenius(C, t, K, Ea, VR, T_func, Q_func_1, Q_func_2, Csus_ini_func_1, Csus_ini_func_2, Operation):
            R = 8.314
            T=T_func(t)
            Q_1=Q_func_1(t)
            Q_2=Q_func_2(t)
            Csus_ini_1 = Csus_ini_func_1(t)
            Csus_ini_2 = Csus_ini_func_2(t)
            if Operation == 1:         #Sin recirculación
                dCsus_dt = ((Q_1 / VR) * (Csus_ini_1 - C)) - (C * K * np.exp(-Ea/(R*T))) / VR
            elif Operation == 2:       #dos entradas 
                dCsus_dt = (Q_1 * Csus_ini_1)/VR + (Q_2 * Csus_ini_2)/VR - ((Q_1+Q_2)*C)/VR - (C * K * np.exp(-Ea/(R*T))) / VR
            elif Operation == 3:       #Recirculación interna
                dCsus_dt = (Q_1 * Csus_ini_1)/VR + (Q_2 * C)/VR - ((Q_1)*C)/VR - (C * K * np.exp(-Ea/(R*T))) / VR
            return dCsus_dt
        
        def model_ADM1(C, t, K, VR,  Q_func_1, Q_func_2, Csus_ini_func_1, Csus_ini_func_2, Operation):
            R = 8.314
            Q_1=Q_func_1(t)
            Q_2=Q_func_2(t)
            Csus_ini_1 = Csus_ini_func_1(t)
            Csus_ini_2 = Csus_ini_func_2(t)
            if Operation == 1:         #Sin recirculación
                dCsus_dt = ((Q_1 / VR) * (Csus_ini_1 - C)) - (C * K) / VR
            elif Operation == 2:       #dos entradas 
                dCsus_dt = (Q_1 * Csus_ini_1)/VR + (Q_2 * Csus_ini_2)/VR - ((Q_1 + Q_2)*C)/VR - (C * K) / VR
            elif Operation == 3:       #Recirculación interna
                dCsus_dt = (Q_1 * Csus_ini_1)/VR + (Q_2 * C)/VR - ((Q_1 + Q_2)*C)/VR - (C * K) / VR
            return dCsus_dt
        
        def model_Gompertz(t, ym, U, L):
            y_t = ym * np.exp(-np.exp((U * np.e) / ym * (L - t) + 1))
            return y_t

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

            if self.OperationMode in [1,2] :
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume
                T_R101 = self.Operation_Data.Temp_R101.astype(float)                                   #Temperatures Vector
                T_func_R101 = lambda t: np.interp(t, time, T_R101)                                     #Temperatures in time vector                
                Qin_R101_1 = (self.Operation_Data.Q_P104/60).astype(float).tolist()                    #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector
                
                #R_101 Solution
                self.Csus_ini_R101 = odeint(model_Arrehenius, y0_R101, time, args=(self.K_R101, self.Ea_R101, VR_R101, T_func_R101, Q_func_R101_1, Q_func_R101_1, Csus_in_func_R101_1, Csus_in_func_R101_1, 1)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                try:
                    self.x_R101 = (max(self.Operation_Data.Csus_ini_R101) - self.Operation_Data.Csus_ini_R101.iloc[-1])/max(self.Operation_Data.Csus_ini_R101)
                except ZeroDivisionError:
                    self.x_R101 = 0
                
            elif self.OperationMode in [3,5] :
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume
                T_R101 = self.Operation_Data.Temp_R101.astype(float)                                   #Temperatures Vector
                T_func_R101 = lambda t: np.interp(t, time, T_R101)                                     #Temperatures in time vector                
                Qin_R101_1 = (self.Operation_Data.Q_P104/60).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector
                
                #R101 Solution
                self.Csus_ini_R101 = odeint(model_Arrehenius, y0_R101, time, args=(self.K_R101, self.Ea_R101, VR_R101, T_func_R101, Q_func_R101_1, Q_func_R101_1, Csus_in_func_R101_1, Csus_in_func_R101_1, 1)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                try:
                    self.x_R101 = (max(self.Operation_Data.Csus_ini_R101) - self.Operation_Data.Csus_ini_R101.iloc[-1])/max(self.Operation_Data.Csus_ini_R101)
                except ZeroDivisionError:
                    self.x_R101 = 0
                
                #R_102 Conditions
                y0_R102 = float(self.Operation_Data.Csus_ini_R102[0])                                  #intital condition
                VR_R102 = self.VR2                                                                     #Reactor volume
                T_R102 = self.Operation_Data.Temp_R102.astype(float)                                   #Temperatures Vector
                T_func_R102 = lambda t: np.interp(t, time, T_R102)                                     #Temperatures in time vector                
                Qin_R102_1 = (self.Operation_Data.Q_P101/60).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R102_1 = lambda t: np.interp(t, time, Qin_R102_1)                               #flow in time vector
                Csus_in_R102_1 = self.Operation_Data.Csus_ini_R101.astype(float)                       #Inlet substrate concentration
                Csus_in_func_R102_1 = lambda t: np.interp(t, time, Csus_in_R102_1)                     #Concentration in time vector
                
                #R102 Solution
                self.Csus_ini_R102 = odeint(model_Arrehenius, y0_R102, time, args=(self.K_R102, self.Ea_R102, VR_R102, T_func_R102, Q_func_R102_1, Q_func_R101_1, Csus_in_func_R102_1, Csus_in_func_R102_1, 1)).flatten()
                self.Csus_ini_R102 = self.Csus_ini_R102[-1]
                try:
                    self.x_R102 = (max(self.Operation_Data.Csus_ini_R102) - self.Operation_Data.Csus_ini_R102.iloc[-1])/max(self.Operation_Data.Csus_ini_R102)
                except ZeroDivisionError:
                    self.x_R102 = 0
            
            elif self.OperationMode == 4:
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume
                T_R101 = self.Operation_Data.Temp_R101.astype(float)                                   #Temperatures Vector
                T_func_R101 = lambda t: np.interp(t, time, T_R101)                                     #Temperatures in time vector                
                Qin_R101_1 = (self.Operation_Data.Q_P104/60).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Qin_R101_2 = (self.Operation_Data.Q_P102/60).astype(float).tolist()
                Q_func_R101_2 = lambda t: np.interp(t, time, Qin_R101_2)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector
                Csus_in_R101_2 = self.Operation_Data.Csus_ini_R102.tolist()
                Csus_in_func_R101_2 = lambda t: np.interp(t, time, Csus_in_R101_2)                     #Concentration in time vector

                #R101 Solution
                self.Csus_ini_R101 = odeint(model_Arrehenius, y0_R101, time, args=(self.K_R101, self.Ea_R101, VR_R101, T_func_R101, Q_func_R101_1, Q_func_R101_2, Csus_in_func_R101_1, Csus_in_func_R101_2, 2)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                try:
                    self.x_R101 = (max(self.Operation_Data.Csus_ini_R101) - self.Operation_Data.Csus_ini_R101.iloc[-1])/max(self.Operation_Data.Csus_ini_R101)
                except ZeroDivisionError:
                    self.x_R101 = 0

                #R_102 Conditions
                y0_R102 = float(self.Operation_Data.Csus_ini_R102[0])                                  #intital condition
                VR_R102 = self.VR2                                                                     #Reactor volume
                T_R102 = self.Operation_Data.Temp_R102.astype(float)                                   #Temperatures Vector
                T_func_R102 = lambda t: np.interp(t, time, T_R102)                                     #Temperatures in time vector                
                Qin_R102_1 = (self.Operation_Data.Q_P101/60).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R102_1 = lambda t: np.interp(t, time, Qin_R102_1)                               #flow in time vector
                Csus_in_R102_1 = self.Operation_Data.Csus_ini_R101.astype(float)                       #Inlet substrate concentration
                Csus_in_func_R102_1 = lambda t: np.interp(t, time, Csus_in_R102_1)                     #Concentration in time vector
                
                #R102 Solution
                self.Csus_ini_R102 = odeint(model_Arrehenius, y0_R102, time, args=(self.K_R102, self.Ea_R102, VR_R102, T_func_R102, Q_func_R102_1, Q_func_R101_1, Csus_in_func_R102_1, Csus_in_func_R102_1, 1)).flatten()
                self.Csus_ini_R102 = self.Csus_ini_R102[-1]
                try:
                    self.x_R102 = (max(self.Operation_Data.Csus_ini_R102) - self.Operation_Data.Csus_ini_R102.iloc[-1])/max(self.Operation_Data.Csus_ini_R102)
                except ZeroDivisionError:
                    self.x_R102 = 0
        
        # Model ADM1
        elif self.Model == "ADM1":

            if self.OperationMode in [1,2] :
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume  
                Qin_R101_1 = (self.Operation_Data.Q_P104/60).astype(float).tolist()                    #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector
                
                #R_101 Solution
                self.Csus_ini_R101 = odeint(model_ADM1, y0_R101, time, args=(self.K_R101, VR_R101, Q_func_R101_1, Q_func_R101_1, Csus_in_func_R101_1, Csus_in_func_R101_1, 1)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                try:
                    self.x_R101 = (max(self.Operation_Data.Csus_ini_R101) - self.Operation_Data.Csus_ini_R101.iloc[-1])/max(self.Operation_Data.Csus_ini_R101)
                except ZeroDivisionError:
                    self.x_R101 = 0
            
            elif self.OperationMode in [3,5]:

                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume
                Qin_R101_1 = (self.Operation_Data.Q_P104/60).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector
                
                #R_101 Solution
                self.Csus_ini_R101 = odeint(model_ADM1, y0_R101, time, args=(self.K_R101, VR_R101, Q_func_R101_1, Q_func_R101_1, Csus_in_func_R101_1, Csus_in_func_R101_1, 1)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                try:
                    self.x_R101 = (max(self.Operation_Data.Csus_ini_R101) - self.Operation_Data.Csus_ini_R101.iloc[-1])/max(self.Operation_Data.Csus_ini_R101)
                except ZeroDivisionError:
                    self.x_R101 = 0
                
                #R_102 Conditions
                y0_R102 = float(self.Operation_Data.Csus_ini_R102[0])                                  #intital condition
                VR_R102 = self.VR2                                                                     #Reactor volume               
                Qin_R102_1 = (self.Operation_Data.Q_P101/60).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R102_1 = lambda t: np.interp(t, time, Qin_R102_1)                               #flow in time vector
                Csus_in_R102_1 = self.Operation_Data.Csus_ini_R101.astype(float)                       #Inlet substrate concentration
                Csus_in_func_R102_1 = lambda t: np.interp(t, time, Csus_in_R102_1)                     #Concentration in time vector
                
                #R102 Solution
                self.Csus_ini_R102 = odeint(model_ADM1, y0_R102, time, args=(self.K_R102, VR_R102, Q_func_R102_1, Q_func_R102_1, Csus_in_func_R102_1, Csus_in_func_R102_1, 1)).flatten()
                self.Csus_ini_R102 = self.Csus_ini_R102[-1]
                try:
                    self.x_R102 = (max(self.Operation_Data.Csus_ini_R102) - self.Operation_Data.Csus_ini_R102.iloc[-1])/max(self.Operation_Data.Csus_ini_R102)
                except ZeroDivisionError:
                    self.x_R102 = 0
            
            elif self.OperationMode == 4:
                # R_101 Conditions
                time = self.Operation_Data.time.astype(float).tolist()
                y0_R101 = float(self.Operation_Data.Csus_ini_R101[0])                                  #intital condition
                VR_R101 = self.VR1                                                                     #Reactor volume       
                Qin_R101_1 = (self.Operation_Data.Q_P104/60).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R101_1 = lambda t: np.interp(t, time, Qin_R101_1)                               #flow in time vector
                Qin_R101_2 = (self.Operation_Data.Q_P102/60).astype(float).tolist()
                Q_func_R101_2 = lambda t: np.interp(t, time, Qin_R101_2)                               #flow in time vector
                Csus_in_R101_1 = self.Operation_Data.Csus_ini.astype(float)                            #Inlet substrate concentration
                Csus_in_func_R101_1 = lambda t: np.interp(t, time, Csus_in_R101_1)                     #Concentration in time vector
                Csus_in_R101_2 = self.Operation_Data.Csus_ini_R102.tolist()
                Csus_in_func_R101_2 = lambda t: np.interp(t, time, Csus_in_R101_2)                     #Concentration in time vector

                #R101 Solution
                self.Csus_ini_R101 = odeint(model_ADM1, y0_R101, time, args=(self.K_R101, VR_R101, Q_func_R101_1, Q_func_R101_2, Csus_in_func_R101_1, Csus_in_func_R101_2, 2)).flatten()
                self.Csus_ini_R101 = self.Csus_ini_R101[-1]
                try:
                    self.x_R101 = (max(self.Operation_Data.Csus_ini_R101) - self.Operation_Data.Csus_ini_R101.iloc[-1])/max(self.Operation_Data.Csus_ini_R101)
                except ZeroDivisionError:
                    self.x_R101 = 0

                #R_102 Conditions
                y0_R102 = float(self.Operation_Data.Csus_ini_R102[0])                                  #intital condition
                VR_R102 = self.VR2                                                                     #Reactor volume                
                Qin_R102_1 = (self.Operation_Data.Q_P101/60).astype(float).tolist()                         #flow in 1 Vector            
                Q_func_R102_1 = lambda t: np.interp(t, time, Qin_R102_1)                               #flow in time vector
                Csus_in_R102_1 = self.Operation_Data.Csus_ini_R101.astype(float)                       #Inlet substrate concentration
                Csus_in_func_R102_1 = lambda t: np.interp(t, time, Csus_in_R102_1)                     #Concentration in time vector
                
                #R102 Solution
                self.Csus_ini_R102 = odeint(model_ADM1, y0_R102, time, args=(self.K_R102, VR_R102, Q_func_R102_1, Q_func_R101_1, Csus_in_func_R102_1, Csus_in_func_R102_1, 1)).flatten()
                self.Csus_ini_R102 = self.Csus_ini_R102[-1]
                try:
                    self.x_R102 = (max(self.Operation_Data.Csus_ini_R102) - self.Operation_Data.Csus_ini_R102.iloc[-1])/max(self.Operation_Data.Csus_ini_R102)
                except ZeroDivisionError:
                    self.x_R102 = 0
                

            

            
        self.GlobalTime = self.GlobalTime + self.tp        
            
           

            
            