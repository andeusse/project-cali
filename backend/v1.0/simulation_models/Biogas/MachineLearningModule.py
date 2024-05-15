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



class BiogasModelTrain:
    def __init__ (self, index_database, VR1):
        self.databaseConnection_df = pd.read_excel(excel_file_path, sheet_name='ConexionDB')
        self.database_df = pd.read_excel(excel_file_path, sheet_name='InfluxDBVariables')
        self.InfluxDB = DBManager.InfluxDBmodel(server = 'http://' + str(self.databaseConnection_df['IP'][index_database])+':'+str(self.databaseConnection_df['Port'][index_database])+'/', org = self.databaseConnection_df['Organization'][index_database], bucket = self.databaseConnection_df['Bucket'][index_database], token = self.databaseConnection_df['Token'][index_database])
        
        self.query_Csus_exp_R101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "Csus_exp_R101", location=1, type=1, forecastTime=1)
        self.Csus_exp_R101 = self.InfluxDB.InfluxDBreader(self.query_Csus_exp_R101)
        self.initial_time = self.Csus_exp_R101["_time"][0]
        self.Csus_ini = self.Csus_exp_R101["Csus_exp_R101"][0]
        
        self.VR1 = VR1

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
            n = len(self.t_DT)/2
            self.t_train = self.t_DT[: n]
            self.end_train_date = t_i[n]
            self.data_train = self.Data[: n]
            self.t_val = self.t_DT[n :]
        
        else:
            n = (len(self.t_DT)+1)/2
            self.t_train = self.t_DT[: n]
    
    def Operation_1_Train(self):

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
        
        def ValidationAndPrediction (K, t, Q, C):
            Q = Q[0]

            def DiferentialEquation (C, t):
                self.CsusR101_val_dt = Q/self.VR1*(self.Csus_ini-C)-K
                return self.CsusR101_val_dt
            
            Co = C[0]
            self.res_val_R101 = odeint(DiferentialEquation, Co, t)
            return self.res_val_R101