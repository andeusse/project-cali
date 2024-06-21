import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import minimize
import numpy as np
import time
from datetime import datetime
import statistics as st


class BiogasModelTrain:
    def __init__ (self, t_train, OperationMode, Kini, Eaini, VR1): 
        self.t_train = t_train
        self.points = int(round((self.t_train*3600)/30))
        self.OperationMode = OperationMode
        self.Kini = Kini
        self.Eaini = Eaini    
        self.VR1 = VR1

        self.train_data = pd.DataFrame()
        if self.OperationMode == 1:
            self.train_data ["timestamp"] = None
            self.train_data ["Pre_exponential_factor"] = None
            self.train_data ["Energy_of_activation"] = None
            
    def Get_data_DT (self, DataBase):
        self.Database = DataBase
        if self.OperationMode == 1:    
            self.timestamp = self.Database["timestamp"].tail(self.points) 
            self.Msus_exp_R101 = self.Database["mol_sus_int_ini_R101"].tail(self.points)        
            self.Csus_exp_R101 = self.Database["Csus_ini_R101"].tail(self.points)
            self.Q_P104 = self.Database["Q_P104"].tail(self.points)
            self.TE101 = self.Database["Temp_R101"].tail(self.points)
        
    def DT_time_and_data (self):
        self.t_DT = []
        t_i = self.timestamp.tolist()
        self.initial_time = t_i[0]
                
        for i in range (len(t_i)):
            t = t_i[i] - self.initial_time 
            self.t_DT.append(t.total_seconds())
    
        if len(self.t_DT) % 2 == 0:
            self.n = int(len(self.t_DT)/2) 
        else:
            self.n = int((len(self.t_DT)+1)/2)

        #end date to train
        self.end_train_date = t_i[self.n]
        #Train Data    
        self.t_train = self.t_DT[: self.n]       #Vector time in seconds without date
        self.Csus_exp_train_R101 = self.Csus_exp_R101[: self.n].tolist()
        self.Q_P104_train = self.Q_P104[: self.n].tolist()
        self.TE101_train = self.TE101[: self.n].tolist()
        self.Date_train = t_i[: self.n]
        #Test Data
        self.t_val = self.t_DT[self.n + 1 :]         #Vector time in seconds without date
        self.Csus_exp_val_R101 = self.Csus_exp_R101[self.n + 1 :].tolist()
        self.Q_P104_val = self.Q_P104[self.n + 1 :].tolist()
        self.TE101_val = self.TE101[self.n + 1 :] .tolist()   
        self.Date_val = t_i[self.n + 1 :] 

        self.Csus_ini_R101 =  self.Csus_exp_train_R101[0]
        self.X_R101 = (self.Csus_ini_R101 - self.Csus_exp_val_R101[-1]) / self.Csus_ini_R101 
            
    def Operation_1_Optimization(self):

        def model(C, t, K, Ea, VR, T_func, Q_func):
            R = 8.314
            T=T_func(t)
            Q=Q_func(t)
            dCsus_dt = ((Q / VR) * (self.Csus_ini_R101 - C)) - (C * K * np.exp(-Ea/(R*T))) / VR
            return dCsus_dt
        
        def Optimization(K, Ea, t, C_exp, y0, VR, temperatures, Qi):
            # Define the objective function to minimize
            def objective(params):
                K, Ea = params
                total_squared_diff = 0
                for i in range (len(temperatures)):
                    T = temperatures[i]
                    Q = Qi[i]
                    T_func = lambda t: np.interp(t, self.t_train, temperatures)
                    Q_func = lambda t: np.interp(t, self.t_train, Qi)
                    # Integrate the model with the current values of K and Ea
                    C_model = odeint(model, y0, t, args=(K, Ea, VR, T_func, Q_func)).flatten()
                    # Calculate the sum of squared differences for this temperature
                    squared_diff = np.sum((C_exp - C_model) ** 2)
                    total_squared_diff += squared_diff
                return total_squared_diff
            
            # Perform the optimization
            result = minimize(objective, [K, Ea], method='Nelder-Mead')
            return result

        if len (self.train_data)>0:
            self.Kini = self.K_R101
            self.Eaini = self.Ea_R101

        self.Optimization_R101 = Optimization(K = self.Kini, Ea = self.Eaini, t = self.t_train, C_exp=self.Csus_exp_train_R101, y0 = self.Csus_exp_train_R101[0], VR = self.VR1, temperatures=self.TE101_train, Qi=self.Q_P104_train) 
        self.K_R101 = float(self.Optimization_R101.x[0])
        self.Ea_R101 = float(self.Optimization_R101.x[1])          

        T_train_R101 = lambda t: np.interp(t, self.t_train, self.TE101_train)
        Q_train_R101 = lambda t: np.interp(t, self.t_train, self.Q_P104_train)
        self.Csus_model_train = odeint(model, self.Csus_exp_train_R101[0], self.t_train, args=(self.K_R101, self.Ea_R101, self.VR1, T_train_R101, Q_train_R101))

        T_val_R101 = lambda t: np.interp(t, self.t_val, self.TE101_val)
        Q_val_R101 = lambda t: np.interp(t, self.t_val, self.Q_P104_val)
        self.Csus_model_val = odeint(model, self.Csus_exp_val_R101[0], self.t_val, args=(self.K_R101, self.Ea_R101, self.VR1, T_val_R101, Q_val_R101))

    def StorageData (self):
        self.timestamp = datetime.now()
        if self.OperationMode == 1:
             new_row = pd.DataFrame({"timestamp": [self.timestamp],
                                    "Pre_exponential_factor" : [self.K_R101],
                                    "Energy_of_activation": [self.Ea_R101],})
             self.train_data = pd.concat([self.train_data, new_row], ignore_index=True)
        
    

            




        

    
        
        
            
            

    