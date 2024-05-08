import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
current_directory = os.getcwd()
excel_file_path = os.path.join(os.path.abspath(os.path.join(current_directory, '..', '..')), "tools", "DB_Mapping.xlsx")
print(excel_file_path)

import time
from datetime import datetime
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import minimize
import statistics as st


class BiogasModelTrain:
    def __init__ (self, Msus_exp_R101, C_sus_exp_R101, Q_P104, Initial_time, tp, VR1, Kini):  #iniital time es el tiempo que se registra cuando se envía el primer dato de Csus_exp_R101
        self.Msus_exp_R101 = Msus_exp_R101
        self.C_sus_exp_R101 = C_sus_exp_R101
        self.Q_P104 = Q_P104
        self.initial_time = Initial_time
        self.tp = tp
        self.VR1 = VR1
        self.Kini = Kini
        
    
    def vector_of_times (self):
        self.time = self.C_sus_exp_R101["_time"]

        if len(self.time) >= 240:      
            
            self.t_train = []
            Iteration = 0
            for i in range (120):
                t = self.time[Iteration] - self.initial_time
                t = t.total_seconds()
                self.t_train.append(t)
                Iteration = Iteration + 1
                self.last_time_train = self.time [Iteration]
                self.last_time_train = int(self.last_time_train.timestamp())
            
            self.t_train = np.asarray(self.t_train)

            self.t_val = []
            for i in range (120):
                t = self.time[Iteration] - self.initial_time
                t = t.total_seconds()
                self.t_val.append(t)
                Iteration = Iteration + 1
            
            self.t_val = np.asarray(self.t_val)

            self.t_pred = []
            last_t_val = self.t_val[-1]
            for i in range(120):
                t = last_t_val + self.tp
                self.t_pred.append(t)
            
            self.t_pred = np.asarray(self.t_pred)
    
    def R101_Operation1 (self):
        C_sus_ini = self.C_sus_exp_R101[0]
        self.C_sus_exp_train_R101 = self.C_sus_exp_R101 [: len(self.t_train)]
        self.C_sus_exp_val_R101 = self.C_sus_exp_R101 [len(self.t_train) + 1 : len(self.t_val)]

        def Optimization (K, t, C_sus_exp, Q):
            Q_P104 = Q[0]
            def Model (K , t, C_sus_exp):
                def DiferentialEquation (C, t):
                    self.Csus_R101_dt = (Q_P104/self.VR1)*(C_sus_ini - C)-K
                    return self.Csus_R101_dt
                Co = C_sus_exp[0]
                self.Csus = odeint(DiferentialEquation, Co, t)
                self.obj = np.sum((self.Csus - C_sus_exp)**2)
                return self.obj
            self.Optimization_R101 = minimize(Model, K, args=(t, C_sus_exp))
            self.K_R101 = self.Optimization_R101.x
            return self.K_R101, self.Csus
        
        self.K_optimizadav_R101 = []
        self.Csus_model_train_R101 = []

        for i in range (len(self.t_train)):
            self.tv = self.t_train[i : i+1]
            self.C_train_R101 = self.C_sus_exp_train_R101[i : i+1]
            self.Q_train_R101 = self.Q_P104[i : i+1] 

            self.Ko = self.Kini
            self.Optimization  = Optimization(K = self.Ko, t = self.tv, C_sus_exp= self.C_train_R101, Q = self.Q_train_R101)

            self.K_optimizadav_R101.append(float(self.Optimization[0]))
            self.Kini = float(self.Optimization[0])
            self.Csus_model_train_R101.append(float(self.Optimization[1][0]))
        
        self.K_mean = st.mean(self.K_optimizadav_R101)

        
        











             





        
        
    
        
            

