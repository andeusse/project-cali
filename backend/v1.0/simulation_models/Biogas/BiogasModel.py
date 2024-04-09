from tools import DBManager
import pandas as pd
import time
from datetime import datetime
import ThermoProperties as TP
from scipy.integrate import odeint
from scipy.optimize import minimize
import numpy as np
import statistics as st

class BiogasPlant:

    def __init__(self, Operation=1, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, t_prediction = 1, timetrain=1, K_ini=1):

        #Interface Inputs
        self.Operation = Operation
        self.VR1 = VR1
        self.VR2 = VR2
        self.VG1 = VG1
        self.VG2 = VG2
        self.VG3 = VG3
        self.databaseConnection_df = pd.read_excel(r'.\tools\DB_Mapping.xlsx', sheet_name='ConexionDB')
        self.database_df = pd.read_excel(r'.\tools\DB_Mapping.xlsx', sheet_name='InfluxDBVariables')
        self.InfluxDB = DBManager.InfluxDBmodel(server = 'http://' + str(self.databaseConnection_df['IP'][3])+':'+str(self.databaseConnection_df['Port'][3])+'/', org = self.databaseConnection_df['Organization'][3], bucket = self.databaseConnection_df['Bucket'][3], token = self.databaseConnection_df['Token'][3])
        self.Thermo = TP.ThermoProperties()
        self.tp = tp
        self.t_prediction = t_prediction * 3600
        self.timetrain = timetrain * 3600
        self.validation_time = timetrain * 3600
        self.K_ini = K_ini
        
        #Initial values
        self.TotalTime = 0
        self.TimeCounterPump = 0
        self.Pacum = 0
        self.P_ini = 0

    def GetValuesFromBiogasPlant (self):
        
        self.msg = self.InfluxDB.InfluxDBconnection()

        #Get total solids from real biogas plant interface (HMI)
        self.queryST = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-ST", location=1, type=0, forecastTime=1) 
        self.ST = self.InfluxDB.InfluxDBreader(self.queryST)

        #Get volatile solids from real biogas plant interface (HMI)
        self.querySV = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-SV", location=1, type=0, forecastTime=1) 
        self.SV = self.InfluxDB.InfluxDBreader(self.querySV)

        #Get Carbon concentration from real biogas plant interface (HMI)
        self.queryCc = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Cc", location=1, type=0, forecastTime=1) 
        self.Cc = self.InfluxDB.InfluxDBreader(self.queryCc)

        #Get Hydrogen concentration from real biogas plant interface (HMI)
        self.queryCh = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Ch", location=1, type=0, forecastTime=1)
        self.Ch = self.InfluxDB.InfluxDBreader(self.queryCh)

        #Get Oxygen concentration from real biogas plant interface (HMI)
        self.queryCo = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Co", location=1, type=0, forecastTime=1)
        self.Co = self.InfluxDB.InfluxDBreader(self.queryCo)

        #Get nitrogen concentration from real biogas plant interface (HMI)
        self.queryCn = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Cn", location=1, type=0, forecastTime=1)
        self.Cn = self.InfluxDB.InfluxDBreader(self.queryCn)

        #Get sulfide concentration from real biogas plant interface (HMI)
        self.queryCs = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Cs", location=1, type=0, forecastTime=1)
        self.Cs = self.InfluxDB.InfluxDBreader(self.queryCs)

        #Get density of substract from real biogas plant interface (HMI)
        self.query_rho = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-d", location=1, type=0, forecastTime=1)
        self.rho = self.InfluxDB.InfluxDBreader(self.query_rho)
        
        #Get pump-104 flow from real biogas plant
        self.query_SE104 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SE-104", location=1, type=0, forecastTime=1)
        self.SE104v = self.InfluxDB.InfluxDBreader(self.query_SE104)
        
        #Get Temperature from TE101A from real biogas plant
        self.query_TE101A = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TE-101A", location=1, type=0, forecastTime=1)
        self.TE_101Av = self.InfluxDB.InfluxDBreader(self.query_TE101A)
        
        #Get Temperature from TE101B from real biogas plant
        self.query_TE101B = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TE-101B", location=1, type=0, forecastTime=1)
        self.TE_101Bv = self.InfluxDB.InfluxDBreader(self.query_TE101B)
        
        #Get pump-101 flow from real biogas plant
        self.query_SE101 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SE-101", location=1, type=0, forecastTime=1)
        self.SE101v = self.InfluxDB.InfluxDBreader(self.query_SE101)
        
        #get pump-102 flow from real biogas plant
        self.query_SE102 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SE-102", location=1, type=0, forecastTime=1)
        self.SE102v = self.InfluxDB.InfluxDBreader(self.query_SE102)
        
        #get methane concentration from real biogas plant
        self.query_AT103A1 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A1", location=1, type=0, forecastTime=1)
        self.AT103A1v = self.InfluxDB.InfluxDBreader(self.query_AT103A1)
        
        #get pressure from V-101 in real biogas plant
        self.query_PT103 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "PT-103", location=1, type=0, forecastTime=1)
        self.PT103v = self.InfluxDB.InfluxDBreader(self.query_PT103)
        
        #get Temperature from V-101 in real biogas plant
        self.query_TT103 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TT-103", location=1, type=0, forecastTime=1)
        self.TT103v = self.InfluxDB.InfluxDBreader(self.query_TT103)

        #get valve V-101 state
        self.query_SV103 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SV-103", location=1, type=0, forecastTime=1)
        self.SV103v = self.InfluxDB.InfluxDBreader(self.query_SV103)

        #get valve V-102 state
        self.query_SV108 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SV-108", location=1, type=0, forecastTime=1)
        self.SV108v = self.InfluxDB.InfluxDBreader(self.query_SV108)

        #get valve V-107 state
        self.query_SV109 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SV-109", location=1, type=0, forecastTime=1)
        self.SV109v = self.InfluxDB.InfluxDBreader(self.query_SV109)

    def RxnParameters (self,  Online = 1, manual_sustrate=0, ST=10, SV=1, Cc=40.48, Ch=5.29, Co=29.66, Cn=1.37, Cs=0.211, rho = 1000): 
        
        #Get from interface if entrances are manual or auto
        self.Online = Online
        self.manual_sustrate = manual_sustrate

        if self.Online == 0 or self.manual_sustrate == 1:
            
            self.ST = ST/100
            self.SV = SV/100
            self.Cc = Cc
            self.Ch = Ch
            self.Co = Co
            self.Cn = Cn
            self.Cs = Cs
            self.rho = rho 
        
        else:

            self.ST = self.ST["M-ST"].iloc[-1]/100
            self.SV = self.SV["M-SV"].iloc[-1]/100
            self.Cc = self.Cc["M-Cc"].iloc[-1]
            self.Ch = self.Ch["M-Ch"].iloc[-1]
            self.Co = self.Co["M-Co"].iloc[-1]
            self.Cn = self.Cn["M-Cn"].iloc[-1]
            self.Cs = self.Cs["M-Cs"].iloc[-1]
            self.rho = self.rho["M-d"].iloc[-1]
        
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
        self.Ch2o_ini = (self.rho*(1-self.ST))/18

    def DTOperationModel1 (self, manual_P104=0, manual_temp_R101=0,  TRH=30, FT_P104=5, TTO_P104=10, Temp_R101 = 35):
        self.manual_P104 = manual_P104
        self.manual_temp_R101 = manual_temp_R101

        if  self.Online == 0 or self.manual_P104 == 1:
            self.TRH = TRH
            self.FT_P104 = FT_P104
            self.TTO_P104 = TTO_P104
            
            self.TurnOnDailyStep = 24/self.FT_P104
        
            self.Q_daily = self.VR1/self.TRH
            self.Q_time = self.Q_daily/self.FT_P104

            if self.TimeCounterPump<self.TTO_P104*60:
                self.Q_P104 = (self.Q_time/self.TTO_P104)*60
            
            else:
                self.Q_P104= float(0)
            
            self.TimeCounterPump = self.TimeCounterPump + self.tp

            if self.TimeCounterPump>=self.TurnOnDailyStep*3600:
                self.TimeCounterPump = 0

            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            
            #save pump - 104 flow for manual operation in InfluxDB
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][91], variable = self.database_df["Tag"][91], value = self.Q_P104, timestamp = self.timestamp)

            #testing model    
            print("Tiempo de encendido de la bomba"+str(self.TimeCounterPump))
            print("Caudal de la bomba"+ str(self.Q_P104))
                    
            #Get data from DT
            self.query_SE104v = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "SE-104v", location=1, type=0, forecastTime=1) 
            self.SE104v = self.InfluxDB.InfluxDBreader(self.query_SE104v)
            self.SE104v = self.SE104v["SE-104v"].tolist()
        
        else:

            self.SE104v = self.SE104v["SE-104"].tolist()
        
        if (self.Online == 0 or self.manual_temp_R101 == 1):

            self.Temp_R101 = Temp_R101
            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][92], variable = self.database_df["Tag"][92], value = self.Temp_R101, timestamp = self.timestamp)
            
            self.query_TE101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "TE-101v", location=1, type=0, forecastTime=1) 
            self.TE_101v = self.InfluxDB.InfluxDBreader(self.query_TE101)
            self.TE_101v = self.TE_101v["TE-101v"]
        
        else:

            self.TE_101Av = self.TE_101Av["TE-101A"].tolist()
            self.TE_101Bv = self.TE_101Bv["TE-101B"].tolist()

            T1 = self.TE_101Av[-1]
            T2 = self.TE_101Bv[-1]
            Tf = (T1 + T2)/2

            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][92], variable = self.database_df["Tag"][92], value = Tf, timestamp = self.timestamp)

            self.query_TE101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "TE-101v", location=1, type=1, forecastTime=1) 
            self.TE_101v = self.InfluxDB.InfluxDBreader(self.query_TE101)
            self.TE_101v = self.TE_101v["TE-101v"]

        self.AT103A1v = self.AT103A1v["AT-103A1"]
        self.PT103v = self.PT103v["PT-103"]
        self.TT103v = self.TT103v["TT-103"]
        self.SV103v = self.SV103v["SV-103"]

        self.P_std = 100
        self.T_std = 273.15 

        self.V_normal = ((self.PT103v.iloc[-1]*6.89476)*self.VG1*self.T_std)/(self.P_std*(self.TT103v.iloc[-1]+273.15))
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][93], variable = self.database_df["Tag"][93], value = self.V_normal, timestamp = self.timestamp)
        
        self.V_normal_CH4 = self.AT103A1v.iloc[-1]/100*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][94], variable = self.database_df["Tag"][94], value = self.V_normal_CH4, timestamp = self.timestamp)
        
        self.V_mol_CH4 = self.Thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
       
        self.mol_CH4 = self.V_normal_CH4/self.V_mol_CH4     
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][95], variable = self.database_df["Tag"][95], value = self.mol_CH4, timestamp = self.timestamp)

        P_iniv = []
        if len(self.PT103v)>1:
            if self.SV103v.iloc[-1] == 1 or self.PT103v.iloc[-1] < (self.PT103v.iloc[-2]-0.5):
                P_iniv.append(self.PT103v.iloc[-1])
                
        if len(P_iniv)>0:
            self.P_ini =self.Pacum + max(P_iniv)
        
        self.Pacum = self.PT103v.iloc[-1] + self.P_ini
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][96], variable = self.database_df["Tag"][96], value = self.Pacum, timestamp = self.timestamp)
        
        self.Vnormal_acum = ((self.Pacum*6.89476)*self.VG1*self.T_std)/(self.P_std*(self.TT103v.iloc[-1]+273.15))
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][97], variable = self.database_df["Tag"][97], value = self.Vnormal_acum, timestamp = self.timestamp)
        
        if self.SE104v.iloc[-1] == 0:
            self.Msus_exp = (self.Csus_ini*self.VR1 - (1/self.s_CH4)*self.mol_CH4)
        else:
            self.Msus_exp = (self.SE104v.iloc[-1]*self.Csus_ini*self.tp/60)-(self.SE104v.iloc[-1]*(self.Csus_ini*self.VR1 - (1/self.s_CH4)*self.mol_CH4)*self.tp/60) + (self.Csus_ini*self.VR1 - (1/self.s_CH4)*self.mol_CH4)
        
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][98], variable = self.database_df["Tag"][98], value = self.Msus_exp, timestamp = self.timestamp)
       
        self.Csus_exp = self.Msus_exp/self.VR1
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][99], variable = self.database_df["Tag"][99], value = self.Csus_exp, timestamp = self.timestamp)
      
        self.query_Msus_exp = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "Msus_exp", location=1, type=0, forecastTime=1)
        self.Msus_expv = self.InfluxDB.InfluxDBreader(self.query_Msus_exp)
        self.Msus_expv = self.Msus_expv["Msus_exp"].tolist()

        self.Q_P104v = self.SE104v

        self.query_molCH4 = self.InfluxDB.QueryCreator(device = "DTPlantaBiogas", variable = "M-molA_CH4", location=1, type=0, forecastTime=1)
        self.mol_CH4v = self.InfluxDB.InfluxDBreader(self.query_molCH4)
        self.mol_CH4v = self.mol_CH4v["M-mol_CH4"].tolist()
        
        self.query_VN_biogas = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable="M-VGA", location=1, type=0, forecastTime=1)
        self.VN_biogasV = self.InfluxDB.InfluxDBreader(self.query_VN_biogas)
        self.VN_biogasv = self.VN_biogasv["M-VG"].tolist()
        
        self.points = int(round(2*(self.timetrain/self.tp),0))

        #Model train        
        if len(self.Msus_expv) >= self.points:

            if len(self.Msus_expv) % 2 == 0:
                self.Msus_exp_train = self.Msus_expv[0 : int(len(self.Msus_expv)/2)]
                self.Csus_exp_train = [x / self.VR1 for x in self.Msus_exp_train]
                self.Q_P104_train = self.Q_P104v[0 : int(len(self.Msus_expv)/2)]
                self.molCH4_exp_train = self.mol_CH4v[0 : int(len(self.Msus_expv)/2)]
                self.VN_biogas_exp_train = self.VN_biogasv[0 : int(len(self.Msus_expv)/2)]

                self.Msus_exp_val = self.Msus_expv[int(len(self.Msus_expv)/2) :]
                self.Csus_exp_val = [x / self.VR1 for x in self.Msus_exp_val]
                self.Q_P104_val = self.Q_P104v[int(len(self.Msus_expv)/2) :]
                self.molCH4_exp_val = self.mol_CH4v[int(len(self.Msus_expv)/2) :]
                self.VN_biogas_exp_val =  self.VN_biogasv[int(len(self.Msus_expv)/2) :]
            else:
                self.Msus_exp_train = self.Msus_expv[0 : int((len(self.Msus_expv)+1)/2)]
                self.Csus_exp_train = [x / self.VR1 for x in self.Msus_exp_train]
                self.Q_P104_train = self.Q_P104v[0 : int((len(self.Msus_expv)+1)/2)]
                self.molCH4_exp_train = self.mol_CH4v[0 : int((len(self.Msus_expv)+1)/2)]
                self.VN_biogas_exp_train = self.VN_biogasv[0 : int((len(self.Msus_expv)+1)/2)]
                
                self.Msus_exp_val = self.Msus_expv[int((len(self.Msus_expv)+1)/2) :]
                self.Csus_exp_val = [x / self.VR1 for x in self.Msus_exp_val]
                self.Q_P104_val = self.Q_P104v[int((len(self.Msus_expv)+1)/2) :]
                self.molCH4_exp_val = self.mol_CH4v[int((len(self.Msus_expv)+1)/2) :]
                self.VN_biogas_exp_val =  self.VN_biogasv[int((len(self.Msus_expv)+1)/2) :]

            self.t_train = np.linspace(self.TotalTime, self.TotalTime+self.timetrain, int(round(len(self.Msus_exp_train),0)))
            self.t_val = np.linspace(self.TotalTime+self.timetrain+self.tp, self.TotalTime+self.timetrain+self.validation_time, int(round(len(self.Msus_exp_val),0)))
              
            #Train function
            def Optimization (K, t, Csus_exp, Q):
                Q = Q[0]
                def Model1 (K, t, Csus_exp):
                    
                    def DiferentialEquation (C, t):
                        self.dCsus_dt = (Q/self.VR1)*(self.Csus_ini-C)-K
                        
                        return self.dCsus_dt
                    
                    Co = Csus_exp[0]
                    self.Csus = odeint(DiferentialEquation, Co, t)
                    self.obj = np.sum((self.Csus-Csus_exp)**2)
                    return self.obj
                
                self.Optimization = minimize(Model1, K, args=(t, Csus_exp))
                self.K = self.Optimization.x
                return self.K, self.Csus
            
            #Validation and predictiion function
            def ValidationModel1 (K, t, Q, C):
                Q = Q[0]
                
                def DiferentialEquation (C,t):
                    self.CsusVal_dt = Q/self.VR1*(self.Csus_ini-C)-K
                    return self.CsusVal_dt
                
                Co = C[0]
                self.res_val = odeint(DiferentialEquation, Co, t)
                return self.res_val

