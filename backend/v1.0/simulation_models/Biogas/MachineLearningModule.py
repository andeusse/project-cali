import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
current_directory = os.getcwd()
excel_file_path = os.path.join(os.path.abspath(os.path.join(current_directory, '..', '..')), "tools", "DB_Mapping.xlsx")
print(excel_file_path)

from  tools import DBManager
import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import minimize
import numpy as np
import time
from datetime import datetime
from pmdarima import ARIMA
from pmdarima import auto_arima



class BiogasModelTrain:
    def __init__ (self, index_database, VR1, Kini):
        self.databaseConnection_df = pd.read_excel(excel_file_path, sheet_name='ConexionDB')
        self.database_df = pd.read_excel(excel_file_path, sheet_name='InfluxDBVariables')
        self.InfluxDB = DBManager.InfluxDBmodel(server = 'http://' + str(self.databaseConnection_df['IP'][index_database])+':'+str(self.databaseConnection_df['Port'][index_database])+'/', org = self.databaseConnection_df['Organization'][index_database], bucket = self.databaseConnection_df['Bucket'][index_database], token = self.databaseConnection_df['Token'][index_database])
        
        self.query_Csus_exp_R101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "Csus_exp_R101", location=1, type=1, forecastTime=1)
        self.Csus_exp_R101 = self.InfluxDB.InfluxDBreader(self.query_Csus_exp_R101)
        self.initial_time = self.Csus_exp_R101["_time"][0]
        self.Csus_ini = self.Csus_exp_R101["Csus_exp_R101"][0]
        
        self.VR1 = VR1
        self.Kini = Kini

    def Get_data_DT (self):
        self.msg = self.InfluxDB.InfluxDBconnection()

        self.query_Msus_exp_R101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "Msus_exp_R102", location=1, type=1, forecastTime=1)
        self.Msus_exp_R101 = self.InfluxDB.InfluxDBreader(self.query_Msus_exp_R101)
        
        self.query_Csus_exp_R101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "Csus_exp_R101", location=1, type=1, forecastTime=1)
        self.Csus_exp_R101 = self.InfluxDB.InfluxDBreader(self.query_Csus_exp_R101)

        self.query_P104 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "SE-104v", location=1, type=1, forecastTime=1) 
        self.Q_P104 = self.InfluxDB.InfluxDBreader(self.query_P104)
    
    def DT_time_and_data (self):
        self.t_DT = []
        t_i = self.Csus_exp_R101["_time"].tolist()
        self.Data = self.Csus_exp_R101[['_time', 'Csus_exp_R101']]
        
        for i in range (len(self.Csus_exp_R101["_time"].tolist())):
            t = t_i[i] - self.initial_time 
            self.t_DT.append(t.total_seconds())
        
        if len(self.t_DT) % 2 == 0:
            self.n = len(self.t_DT)/2 
        else:
            self.n = (len(self.t_DT)+1)/2

        #end date to train
        self.end_train_date = t_i[self.n]
        #Train Data    
        self.t_train = self.t_DT[: self.n]       #Vector time in seconds without date
        self.data_train = self.Data[: self.n]    #Vector with dates
        self.Csus_exp_train = self.Data['Csus_exp_R101'][: self.n]
        self.Q_P104_train = self.Q_P104["SE-104v"][: self.n]
        self.Date_train = t_i[: self.n]
        #Test Data
        self.t_val = self.t_DT[self.n + 1 :]         #Vector time in seconds without date
        self.data_val = self.Data[self.n + 1 :]      #Vector with dates    
    
    def Operation_1_Optimization(self):

        def Optimization(K, t, Csus_exp, Q):
            Q = Q[0]

            def Model (K, t, Csus_exp):

                def DiferentialEquation (C, t):
                    self.dCsusR101_dt = (Q/self.VR1)*(self.Csus_ini-C)-K
                    return self.dCsusR101_dt
                Co = Csus_exp[0]
                self.Csus_R101 = odeint (DiferentialEquation, Co, t)
                self.obj = np.sum((self.Csus_R101 - Csus_exp)**2)
                return self.obj
            
            self.Optimization = minimize(Model, K, arg=(t, Csus_exp))
            self.K_R101 = self.Optimization.x
            return self.K_R101, self.Csus_R101
        
        self.K_optimizada = []
        self.C_sus_model_train = []
        for i in range (len(self.t_DT)):
            self.tv = self.t_DT[i : i+1]
            self.C_train = self.Data['Csus_exp_R101'][i : i+1]
            self.Q_train = self.Q_P104["SE-104v"][i : i+1]
            self.Ko = self.Kini

            self.Optimizacion = Optimization(K = self.Ko, t = self.tv, Csus_exp=self.C_train, Q = self.Q_train)
            self.K_optimizada.append(float(self.Optimizacion[0]))
            self.Kini = float(self.Optimizacion[0])
            self.C_sus_model_train.append(float(self.Optimizacion[1][0]))
            timestamp = int(self.Date_train[i].timestamp())
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][155], variable = self.database_df["Tag"][155], value = self.Kini, timestamp = timestamp)

    def Kinetic_Forecasting (self):
        self.K_train = self.K_optimizada[: self.n]
        self.K_test = self.K_optimizada[self.n+1 :]
        
        
        
            
            

    