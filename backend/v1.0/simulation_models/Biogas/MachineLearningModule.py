import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import minimize
import numpy as np
import time
from datetime import datetime
import statistics as st


class BiogasModelTrain:
    def __init__ (self, t_train, OperationMode, Model, A_R101=1, B_R101=1, C_R101=1, A_R102=1, B_R102=1, C_R102=1, VR1=30, VR2=70): 
        self.t_train = t_train
        self.points = int(round((self.t_train*3600)/30))
        self.OperationMode = OperationMode
        self.Model = Model
    
        if self.OperationMode == 1 or self.OperationMode == 2:
            self.VR1 = VR1
            if Model == "Gompertz":
                self.ymini_R101 = A_R101
                self.Uini_R101 = B_R101
                self.Lini_R101 = C_R101
                variables = ["timestamp", "ym_R101", "U_R101", "L_R101"]
            elif Model == "Arrhenius": 
                self.Kini_R101 = A_R101
                self.Eaini_R101 = B_R101  
                variables = ["timestamp", "K_R101", "Ea_R101"]
            elif Model == "ADM1":
                self.Kini_R101 = A_R101
                variables = ["timestamp", "K_R101"]
        elif self.OperationMode == 3 or self.OperationMode == 4 or self.OperationMode == 5:
            self.VR1 = VR1
            self.VR2 = VR2
            if Model == "Gompertz":
                self.ymini_R101 = A_R101
                self.Uini_R101 = B_R101
                self.Lini_R101 = C_R101
                self.ymini_R102 = A_R102
                self.Uini_R102 = B_R102
                self.Lini_R102 = C_R102
                variables = ["timestamp", "ym_R101", "U_R101", "L_R101", "ym_R102", "U_R102", "L_R102"]
            elif Model == "Arrhenius": 
                self.Kini_R101 = A_R101
                self.Eaini_R101 = B_R101
                self.Kini_R102 = A_R102
                self.Eaini_R102 = B_R102  
                variables = ["timestamp", "K_R101", "Ea_R101", "K_R102", "Ea_R102"]
            elif Model == "ADM1":
                self.Kini_R101 = A_R101
                self.Kini_R101 = A_R102
                variables = ["timestamp", "K_R101", "K_R102"]
        
        self.train_data = pd.DataFrame(columns=variables)
            
    def Get_data_DT (self, DataBase):
        
        variables = ["timestamp", 
                     "mol_sus_int_ini_R101",
                     "Csus_ini_R101",
                     "Q_P104",
                     "Temp_R101"]
        
        if self.OperationMode == 2:
            variables.append("Q_P101")
            
        elif self.OperationMode == 3:
            variables = variables + ["mol_sus_int_ini_R102",
                                     "Csus_ini_R102",
                                     "Q_P101",
                                     "Temp_R102"]

        elif self.OperationMode == 4 or self.OperationMode == 5:
            variables = variables + ["mol_sus_int_ini_R102",
                                     "Csus_ini_R102",
                                     "Q_P101",
                                     "Q_P¨102"
                                     "Temp_R102"]
    
        self.Data_set = DataBase[variables].tail(self.points)
                    
    def DT_time_and_data (self):
        self.t_train = (self.Data_set.timestamp - self.Data_set.timestamp[0]).dt.total_seconds()
        self.train_set = self.Data_set
       
    def Optimization(self, t_predict=1):
        self.t_predict = t_predict

        def model_Arrehenius(C, t, K, Ea, VR, T_func, Q_func, Csus_ini_func):
            R = 8.314
            T=T_func(t)
            Q=Q_func(t)
            Csus_ini = Csus_ini_func(t)
            dCsus_dt = ((Q / VR) * (Csus_ini - C)) - (C * K * np.exp(-Ea/(R*T))) / VR
            return dCsus_dt

        def model_ADM1(C, t, K, VR, Q_func, Csus_ini):
            R = 8.314
            Q=Q_func(t)
            dCsus_dt = ((Q / VR) * (Csus_ini - C)) - (C * K) / VR
            return dCsus_dt
        
        def model_Gompertz(t, ym, U, L):
            y_t = ym * np.exp(-np.exp((U * np.e) / ym * (L - t) + 1))
            return y_t
        
        def Optimization(t, C_exp, y0, VR, temperatures, Qi, Csus_ini_i, K=1, Ea=1):
            # Define the objective function to minimize
            def objective(params):
                K, Ea = params
                total_squared_diff = 0
                for i in range (len(temperatures)):
                    T = temperatures[i]
                    Q = Qi[i]
                    Csus_ini = Csus_ini_i[i]
                    T_func = lambda t: np.interp(t, self.t_train, temperatures)
                    Q_func = lambda t: np.interp(t, self.t_train, Qi)
                    Csus_ini_func = lambda t: np.interp(t, self.t_train, Csus_ini_i)
                    # Integrate the model with the current values of K and Ea
                    if self.Model== "Arrhenius":
                        C_model = odeint(model_Arrehenius, y0, t, args=(K, Ea, VR, T_func, Q_func, Csus_ini_func)).flatten()
                    elif self.Model == "ADM1":
                        C_model = odeint(model_ADM1, y0, t, args=(K, VR, T_func, Q_func, Csus_ini_func)).flatten()
                    # Calculate the sum of squared differences for this temperature
                    squared_diff = np.sum((C_exp - C_model) ** 2)
                    total_squared_diff += squared_diff
                return total_squared_diff
            
            # Perform the optimization
            if self.Model == "Arrhenius":
                result = minimize(objective, [K, Ea], method='Nelder-Mead')
            elif self.Model == "ADM1":
                result = minimize(objective,[K], method= 'Nelder-Mead') 
            return result
        
        def Optimization_Gompertz(params, t, y_exp):
            ym, U, L = params
            y_pred = model_Gompertz(t, ym, U, L)
            residuals = y_exp - y_pred
            return np.sum(residuals**2)
            
        if self.Model == "Arrhenius" or self.Model == "ADM1":
            if len (self.train_data)>0:
                self.Kini_R101 = self.K_R101
                if self.Model == "Arrhenius":self.Eaini_R101 = self.Ea_R101
            
            #R_101 general Conditions
            Csus_exp_train_R101 = self.train_set.Csus_ini_R101.tolist()
            TE101_train = (self.train_set.Temp_R101 + 273.15).tolist()
            
            if self.OperationMode == 1:
                #R_101 Conditions
                Csus_in_R101 = self.train_set.Csus_ini.tolist()
                Q_in_R101 = (self.train_set.Q_P104/60).tolist()
            
            elif self.OperationMode == 2:
                #R_101 Conditions
                Csus_in_R101 = (self.train_set.Csus_ini + self.train_set.Csus_ini_R101).tolist()
                Q_in_R101 = ((self.train_set.Q_P104 + self.train_set.Q_P101)/60).tolist()

            elif self.OperationMode == 3:
                #R_101 Conditions
                Csus_in_R101 = self.train_set.Csus_ini.tolist()
                Q_in_R101 = (self.train_set.Q_P104/60).tolist()

                #R_102 conditions and solution
                if len (self.train_data)>0:
                    self.Kini_R102 = self.K_R102
                    if self.Model == "Arrhenius": self.Eaini_R102 = self.Ea_R102

                Csus_exp_train_R102 = self.train_set.Csus_ini_R102.tolist() 
                TE102_train = (self.train_set.Temp_102 + 273.15).tolist()
                Q_in_R102 = (self.train_set.Q_P101/60).tolist()
                self.Optimization_R101 = Optimization(t = self.t_train, C_exp=Csus_exp_train_R102, y0 = Csus_exp_train_R102[0], VR = self.VR2, temperatures=TE102_train, Qi=Q_in_R102, Csus_ini=Csus_exp_train_R101, K = self.Kini_R102, Ea = self.Eaini_R102) 
                
            elif self.OperationMode == 4:
                #R_101 Conditions
                Csus_in_R101 = (self.train_set.Csus_ini + self.train_set.Csus_ini_R102).tolist()
                Q_in_R101 = ((self.train_set.Q_P104 + self.train_set.Q_P102)/60).tolist

                #R_102 conditions and solution
                if len (self.train_data)>0:
                    self.Kini_R102 = self.K_R102
                    if self.Model == "Arrhenius": self.Eaini_R102 = self.Ea_R102

                Csus_exp_train_R102 = self.train_set.Csus_ini_R102.tolist() 
                TE102_train = (self.train_set.Temp_102 + 273.15).tolist()
                Q_in_R102 = (self.train_set.Q_P101/60).tolist()
                self.Optimization_R101 = Optimization(t = self.t_train, C_exp=Csus_exp_train_R102, y0 = Csus_exp_train_R102[0], VR = self.VR2, temperatures=TE102_train, Qi=Q_in_R102, Csus_ini=Csus_exp_train_R101, K = self.Kini_R102, Ea = self.Eaini_R102) 
                self.K_R102 = float(self.Optimization_R102.x[0])
                if self.Model == "Arrhenius": self.Ea_R102 = float(self.Optimization_R102.x[1])

            elif self.OperationMode == 5:
                #R_101 Conditions
                Csus_in_R101 = (self.train_set.Csus_ini).tolist()
                Q_in_R101 = (self.train_set.Q_P104/60).tolist

                #R_102 conditions and solution
                if len (self.train_data)>0:
                    self.Kini_R102 = self.K_R102
                    if self.Model == "Arrhenius": self.Eaini_R102 = self.Ea_R102

                Csus_exp_train_R102 = self.train_set.Csus_ini_R102.tolist() 
                TE102_train = (self.train_set.Temp_102 + 273.15).tolist()
                Q_in_R102 = ((self.train_set.Q_P101 + self.train_set.Q_P102)/60).tolist()
                Csus_in_R102 = (self.train_data.Csus_ini_R101 + self.train_data.Csus_ini_R102).tolist()
                self.Optimization_R101 = Optimization(t = self.t_train, C_exp=Csus_exp_train_R102, y0 = Csus_exp_train_R102[0], VR = self.VR2, temperatures=TE102_train, Qi=Q_in_R102, Csus_ini=Csus_in_R102, K = self.Kini_R102, Ea = self.Eaini_R102) 

            #R_101 solution    
            self.Optimization_R101 = Optimization(t = self.t_train, C_exp=Csus_exp_train_R101, y0 = Csus_exp_train_R101[0], VR = self.VR1, temperatures=TE101_train, Qi=Q_in_R101, Csus_ini_i=Csus_in_R101, K = self.Kini_R101, Ea = self.Eaini_R101) 
            self.K_R101 = float(self.Optimization_R101.x[0])
            if self.Model == "Arrhenius": self.Ea_R101 = float(self.Optimization_R101.x[1])     
                
        elif self.Model == "Gompertz":
            if len (self.train_data)>0:
                self.ymini_R101 = self.ym_R101
                self.Uini_R101 = self.U_R101
                self.Lini_R101 = self.L_R101
            
            Initial_values_R101 = [self.ymini_R101, self.Uini_R101, self.Lini_R101]
            y_exp_R101 = self.train_set.yt_R101.tolist()
            self.Optimization_R101 = minimize(Optimization_Gompertz, Initial_values_R101, args=(self.t_train, y_exp_R101), method = 'Nelder-Mead')
            self.ym_R101, self.U_R101, self.L_R101 = self.Optimization_R101.x

            if self.OperationMode in [3, 4, 5]:
                if len (self.train_data)>0:
                    self.ymini_R102 = self.ym_R102
                    self.Uini_R102 = self.U_R102
                    self.Lini_R102 = self.L_R102
                
                Initial_values_R102 = [self.ymini_R101, self.Uini_R101, self.Lini_R101]
                y_exp_R102 = self.train_set.yt_R102.tolist()
                self.Optimization_R102 = minimize(Optimization_Gompertz, Initial_values_R102, args=(self.t_train, y_exp_R102), method = 'Nelder-Mead')
                self.ym_R102, self.U_R102, self.L_R102 = self.Optimization_R102.x
     
    def StorageData (self):
        self.timestamp = datetime.now()
        if self.OperationMode == 1 or self.OperationMode == 2:
            if self.Model == "Gompertz":
                new_row = pd.DataFrame({"timestamp": [self.timestamp],
                                    "ym_R101" : [self.ym_R101],
                                    "U_R101": [self.U_R101],
                                    "L_R101": [self.L_R101]})
                
            elif self.Model == "Arrhenius":
                new_row = pd.DataFrame({"timestamp": [self.timestamp],
                                    "K_R101" : [self.K_R101],
                                    "Ea_R101": [self.Ea_R101]})
            
            elif self.Model == "ADM1":
                new_row = pd.DataFrame({"timestamp": [self.timestamp],
                                    "K_R101" : [self.K_R101]})
        
        elif self.OperationMode == 3 or self.OperationMode == 4 or self.OperationMode == 5: 
            if self.Model == "Gompertz":
                new_row = pd.DataFrame({"timestamp": [self.timestamp],
                                        "ym_R101" : [self.ym_R101],
                                        "U_R101": [self.U_R101],
                                        "L_R101": [self.L_R101],
                                        "ym_R102" : [self.ym_R102],
                                        "U_R102": [self.U_R102],
                                        "L_R102": [self.L_R102]})
                
            elif self.Model == "Arrhenius":
                new_row = pd.DataFrame({"timestamp": [self.timestamp],
                                        "K_R101" : [self.K_R101],
                                        "Ea_R101": [self.Ea_R101],
                                        "K_R102": [self.K_R102],
                                        "Ea_R102" : [self.Ea_R102]})
            
            elif self.Model == "Arrhenius":
                new_row = pd.DataFrame({"timestamp": [self.timestamp],
                                        "K_R101" : [self.K_R101],
                                        "Ea_R101": [self.Ea_R101],
                                        "K_R102": [self.K_R102],
                                        "Ea_R102" : [self.Ea_R102]})
                        
        self.train_data = pd.concat([self.train_data, new_row], ignore_index=True)
    

            




        

    
        
        
            
            

    