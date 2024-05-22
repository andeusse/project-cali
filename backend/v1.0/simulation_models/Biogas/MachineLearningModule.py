import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
current_directory = os.getcwd()
print(current_directory)
excel_file_path = os.path.join(os.path.abspath(os.path.join(current_directory)), "v1.0", "tools", "DB_Mapping.xlsx")
print(excel_file_path)

from  tools import DBManager
import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import minimize
import numpy as np
import time
from datetime import datetime
import statistics as st



class BiogasModelTrain:
    def __init__ (self, VR1, Kini, Eaini, DatabaseConnection_df, database_df, Influx ):
        self.databaseConnection_df = DatabaseConnection_df
        self.database_df = database_df
        self.InfluxDB = Influx
        self.query_Csus_exp_R101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "Csus_exp_R101", location=1, type=1, forecastTime=1)
        self.Csus_exp_R101 = self.InfluxDB.InfluxDBreader(self.query_Csus_exp_R101)
        self.initial_time = self.Csus_exp_R101["_time"][0]
                
        self.VR1 = VR1
        self.Kini = Kini
        self.Eaini =Eaini
        self.Csus_ini = self.Csus_exp_R101["Csus_exp_R101"][0]
        
        self.VR1 = VR1
        self.Kini = Kini
        self.Eaini = Eaini

    def Get_data_DT (self):
        self.msg = self.InfluxDB.InfluxDBconnection()

        self.query_Msus_exp_R101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "Msus_exp_R102", location=1, type=1, forecastTime=1)
        self.Msus_exp_R101 = self.InfluxDB.InfluxDBreader(self.query_Msus_exp_R101)
        
        self.query_Csus_exp_R101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "Csus_exp_R101", location=1, type=1, forecastTime=1)
        self.Csus_exp_R101 = self.InfluxDB.InfluxDBreader(self.query_Csus_exp_R101)

        self.query_P104 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "SE-104v", location=1, type=1, forecastTime=1) 
        self.Q_P104 = self.InfluxDB.InfluxDBreader(self.query_P104)
        
        self.query_TE101 =self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "TE-101v", location=1, type=1, forecastTime=1)
        self.TE101 = self.InfluxDB.InfluxDBreader(self.query_TE101)
    
    def DT_time_and_data (self):
        self.t_DT = []
        t_i = self.Csus_exp_R101["_time"].tolist()
        self.Data = self.Csus_exp_R101[['_time', 'Csus_exp_R101']]
        
        for i in range (len(self.Csus_exp_R101["_time"].tolist())):
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
        self.data_train = self.Data[: self.n]    #Vector with dates
        self.Csus_exp_train = self.Data['Csus_exp_R101'][: self.n]
        self.Q_P104_train = self.Q_P104["SE-104v"][: self.n]
        self.TE101_train = self.TE101["TE-101v"][: self.n]
        self.Date_train = t_i[: self.n]
        #Test Data
        self.t_val = self.t_DT[self.n + 1 :]         #Vector time in seconds without date
        self.data_val = self.Data[self.n + 1 :]      #Vector with dates 
        self.Csus_exp_val = self.Data['Csus_exp_R101'][self.n + 1 :] 
        self.Q_P104_val = self.Q_P104["SE-104v"][self.n + 1 :]
        self.TE101_val = self.TE101["TE-101v"][self.n + 1 :]  

        self.Csus_ini = self.Csus_exp_train[0]
        
    def Operation_1_Optimization(self):

        def model(C, t, K, Ea, VR, T):
            R = 8.314
            dCsus_dt = -(K * C * np.exp(-Ea/(R*T))) / VR
            return dCsus_dt
        
        def Optimization(K, Ea, t, C_exp, y0, VR, temperatures):
            # Define the objective function to minimize
            def objective(params):
                K, Ea = params
                total_squared_diff = 0
                for T in temperatures:
                    # Integrate the model with the current values of K and Ea
                    C_model = odeint(model, y0, t, args=(K, Ea, VR, T)).flatten()
                    # Calculate the sum of squared differences for this temperature
                    squared_diff = np.sum((C_exp - C_model) ** 2)
                    total_squared_diff += squared_diff
                return total_squared_diff
            
            # Perform the optimization
            result = minimize(objective, [K, Ea], method='Nelder-Mead')
            return result
        
        self.Optimization_R101 = Optimization(K = self.Kini, Ea = self.Eaini, t = self.t_train, C_exp=self.Csus_exp_train, y0 = self.Csus_exp_train[0], VR = self.VR1, temperatures=self.TE101_train) 
        self.K_R101 = float(self.Optimization_R101.x[0])
        self.Ea_R101 = float(self.Optimization_R101.x[1])

        self.timestamp = self.Date_train[-1]
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][155], variable = self.database_df["Tag"][155], value = self.K_R101, timestamp = self.timestamp) 
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][156], variable = self.database_df["Tag"][156], value = self.Ea_R101, timestamp = self.timestamp)            

        self.Csus_model_train = odeint(model, self.Csus_exp_train[0], self.t_train, args=(self.K_R101, self.Ea_R101, self.VR1, st.mean(self.TE101_train)))
        self.Csus_model_val = odeint(model, self.Csus_exp_val[self.n +1], self.t_val, args=(self.K_R101, self.Ea_R101, self.VR1, st.mean(self.TE101_val)))
        


            




        

    
        
        
            
            

    