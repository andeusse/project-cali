import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
current_directory = os.getcwd()
excel_file_path = os.path.join(os.path.abspath(os.path.join(current_directory, '..', '..')), "tools", "DB_Mapping.xlsx")
print(excel_file_path)

import pandas as pd
import time
from datetime import datetime
from simulation_models.Biogas import ThermoProperties as TP
from scipy.integrate import odeint
from scipy.optimize import minimize
import numpy as np
import statistics as st
from  tools import DBManager


class BiogasPlant:

    def __init__(self, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, t_prediction = 1, timetrain=1, Kini=1, DigitalTwin=1):

        #Interface Inputs
        self.VR1 = VR1
        self.VR2 = VR2
        self.VG1 = VG1
        self.VG2 = VG2
        self.VG3 = VG3
        self.databaseConnection_df = pd.read_excel(excel_file_path, sheet_name='ConexionDB')
        self.database_df = pd.read_excel(excel_file_path, sheet_name='InfluxDBVariables')
        self.InfluxDB = DBManager.InfluxDBmodel(server = 'http://' + str(self.databaseConnection_df['IP'][3])+':'+str(self.databaseConnection_df['Port'][3])+'/', org = self.databaseConnection_df['Organization'][3], bucket = self.databaseConnection_df['Bucket'][3], token = self.databaseConnection_df['Token'][3])
        self.Thermo = TP.ThermoProperties()
        self.tp = tp
        self.t_prediction = t_prediction * 3600
        self.timetrain = timetrain * 3600
        self.validation_time = timetrain * 3600
        self.Kini = Kini
        self.DigitalTwin = DigitalTwin
        #Initial values
        self.TotalTime = 0
        self.TimeCounterPump_P104 = 0
        self.TimeCounterPump_P101 = 0
        self.TimeCounterPump_P102 = 0
        self.Pacum_v101 = 0
        self.P_ini_V101 = 0

    def GetValuesFromBiogasPlant (self):
        
        self.msg = self.InfluxDB.InfluxDBconnection()

        #Get total solids from real biogas plant interface (HMI)
        self.queryST = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-ST", location=1, type=1, forecastTime=1) 
        self.ST = self.InfluxDB.InfluxDBreader(self.queryST)

        #Get volatile solids from real biogas plant interface (HMI)
        self.querySV = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-SV", location=1, type=1, forecastTime=1) 
        self.SV = self.InfluxDB.InfluxDBreader(self.querySV)

        #Get Carbon concentration from real biogas plant interface (HMI)
        self.queryCc = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Cc", location=1, type=1, forecastTime=1) 
        self.Cc = self.InfluxDB.InfluxDBreader(self.queryCc)

        #Get Hydrogen concentration from real biogas plant interface (HMI)
        self.queryCh = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Ch", location=1, type=1, forecastTime=1)
        self.Ch = self.InfluxDB.InfluxDBreader(self.queryCh)

        #Get Oxygen concentration from real biogas plant interface (HMI)
        self.queryCo = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Co", location=1, type=1, forecastTime=1)
        self.Co = self.InfluxDB.InfluxDBreader(self.queryCo)

        #Get nitrogen concentration from real biogas plant interface (HMI)
        self.queryCn = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Cn", location=1, type=1, forecastTime=1)
        self.Cn = self.InfluxDB.InfluxDBreader(self.queryCn)

        #Get sulfide concentration from real biogas plant interface (HMI)
        self.queryCs = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Cs", location=1, type=1, forecastTime=1)
        self.Cs = self.InfluxDB.InfluxDBreader(self.queryCs)

        #Get density of substract from real biogas plant interface (HMI)
        self.query_rho = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-d", location=1, type=1, forecastTime=1)
        self.rho = self.InfluxDB.InfluxDBreader(self.query_rho)
        
        #Get pump-104 flow from real biogas plant
        self.query_SE104 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SE-104", location=1, type=1, forecastTime=1)
        self.SE104v = self.InfluxDB.InfluxDBreader(self.query_SE104)
        
        #Get Temperature from TE101A from real biogas plant
        self.query_TE101A = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TE-101A", location=1, type=1, forecastTime=1)
        self.TE_101Av = self.InfluxDB.InfluxDBreader(self.query_TE101A)
        
        #Get Temperature from TE101B from real biogas plant
        self.query_TE101B = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TE-101B", location=1, type=1, forecastTime=1)
        self.TE_101Bv = self.InfluxDB.InfluxDBreader(self.query_TE101B)
        
        #Get pump-101 flow from real biogas plant
        self.query_SE101 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SE-101", location=1, type=1, forecastTime=1)
        self.SE101v = self.InfluxDB.InfluxDBreader(self.query_SE101)
        
        #get pump-102 flow from real biogas plant
        self.query_SE102 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SE-102", location=1, type=1, forecastTime=1)
        self.SE102v = self.InfluxDB.InfluxDBreader(self.query_SE102)
        
        #get methane concentration from real biogas plant reactor 1
        self.query_AT103A1 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A1", location=1, type=1, forecastTime=1)
        self.AT103A1v = self.InfluxDB.InfluxDBreader(self.query_AT103A1)

        #Get Carbon dioxide Concentration from real biogas plant reactor 1    
        self.query_AT103A2 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A2", location=1, type=1, forecastTime=1)
        self.AT103A2v = self.InfluxDB.InfluxDBreader(self.query_AT103A2)

        #Get hydrogen sulphide Concentration from real biogas plant reactor 1
        self.query_AT103A3 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A3", location=1, type=1, forecastTime=1)
        self.AT103A3v = self.InfluxDB.InfluxDBreader(self.query_AT103A3)

        #Get Oxygen Concentration from real biogas plant reactor 1
        self.query_AT103A4 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A4", location=1, type=1, forecastTime=1)
        self.AT103A4v = self.InfluxDB.InfluxDBreader(self.query_AT103A4)

        #Get Hydrogen H2 concentration from real biogas plant reactor 1
        self.query_AT103A5 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A5", location=1, type=1, forecastTime=1)
        self.AT103A5v = self.InfluxDB.InfluxDBreader(self.query_AT103A5)

        #Get Biogas relative Humidity from rela biogas plant reactor 1
        self.query_AT103B = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103B", location=1, type=1, forecastTime=1)
        self.AT103Bv = self.InfluxDB.InfluxDBreader(self.query_AT103B)
        
        #get pressure from V-101 in real biogas plant
        self.query_PT103 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "PT-103", location=1, type=1, forecastTime=1)
        self.PT103v = self.InfluxDB.InfluxDBreader(self.query_PT103)
        
        #get Temperature from V-101 in real biogas plant
        self.query_TT103 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TT-103", location=1, type=1, forecastTime=1)
        self.TT103v = self.InfluxDB.InfluxDBreader(self.query_TT103)

        #get methane concentration from real biogas plant V-102
        self.query_AT104A1 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A1", location=1, type=1, forecastTime=1)
        self.AT104A1v = self.InfluxDB.InfluxDBreader(self.query_AT104A1)

        #Get Carbon dioxide Concentration from real biogas plant V-102   
        self.query_AT104A2 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A2", location=1, type=1, forecastTime=1)
        self.AT104A2v = self.InfluxDB.InfluxDBreader(self.query_AT104A2)

        #Get hydrogen sulphide Concentration from real biogas plant V-102
        self.query_AT104A3 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A3", location=1, type=1, forecastTime=1)
        self.AT104A3v = self.InfluxDB.InfluxDBreader(self.query_AT104A3)

        #Get Oxygen Concentration from real biogas plant V-102
        self.query_AT104A4 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A4", location=1, type=1, forecastTime=1)
        self.AT104A4v = self.InfluxDB.InfluxDBreader(self.query_AT104A4)

        #Get Hydrogen H2 concentration from real biogas plant V-102
        self.query_AT104A5 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A5", location=1, type=1, forecastTime=1)
        self.AT104A5v = self.InfluxDB.InfluxDBreader(self.query_AT104A5)

        #Get Biogas relative Humidity from rela biogas plant V-102
        self.query_AT104B = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104B", location=1, type=1, forecastTime=1)
        self.AT104Bv = self.InfluxDB.InfluxDBreader(self.query_AT104B)

        #Get Pressure from V-102 in real biogas plant
        self.query_PT104 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "PT-104", location=1, type=1, forecastTime=1)
        self.PT104v = self.InfluxDB.InfluxDBreader(self.query_PT104)

        #Get Temperature from V-102 in real biogas plant
        self.query_TT104 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TT-104", location=1, type=1, forecastTime=1)
        self.TT104v = self.InfluxDB.InfluxDBreader(self.query_TT104)

        #get valve V-101 state
        self.query_SV103 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SV-103", location=1, type=1, forecastTime=1)
        self.SV103v = self.InfluxDB.InfluxDBreader(self.query_SV103)

        #get valve V-102 state
        self.query_SV108 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SV-108", location=1, type=1, forecastTime=1)
        self.SV108v = self.InfluxDB.InfluxDBreader(self.query_SV108)

        #get valve V-107 state
        self.query_SV109 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SV-109", location=1, type=1, forecastTime=1)
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
        #print("pesomolecular del sustrato" + str(self.MW_sustrato))
        
        self.Csus_ini = (self.rho*self.SV)/self.MW_sustrato
        #print("Concentración inicial de solidos volátiles" + str(self.Csus_ini))
        self.Csus_ini_ST = (self.rho*self.ST)/self.MW_sustrato
        #print("Concnetración de sólidos totales" + str(self.Csus_ini_ST))
        self.Csus_fixed = self.Csus_ini_ST - self.Csus_ini
        #print("Concentración de sólidos fijos" + str(self.Csus_fixed))
        self.Ch2o_ini = (self.rho*(1-self.ST))/18

    def Pump104 (self, manual_P104=0, TRH=30, FT_P104=5, TTO_P104=10):    
        self.manual_P104 = manual_P104
        if  self.Online == 0 or self.DigitalTwin == 0 or self.manual_P104 == 1:
            self.TRH = TRH
            self.FT_P104 = FT_P104
            self.TTO_P104 = TTO_P104
            
            self.TurnOnDailyStep_P104 = 24/self.FT_P104
        
            self.Q_daily = self.VR1/self.TRH
            self.Q_time = self.Q_daily/self.FT_P104

            if self.TimeCounterPump_P104<self.TTO_P104*60:
                self.Q_P104 = (self.Q_time/self.TTO_P104)*60
            
            else:
                self.Q_P104= float(0)
            
            self.TimeCounterPump_P104 = self.TimeCounterPump_P104 + self.tp

            if self.TimeCounterPump_P104>=self.TurnOnDailyStep_P104*3600:
                self.TimeCounterPump_P104 = 0

            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][100], variable = self.database_df["Tag"][100], value = self.Q_P104, timestamp = self.timestamp)

            #testing model    
            print("Tiempo de encendido de la bomba P_104: "+str(self.TimeCounterPump_P104))
            print("Caudal de la bomba P_104: "+ str(self.Q_P104))
                    
            #Get data from DT
            self.query_SE104v = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "SE-104v", location=1, type=1, forecastTime=1) 
            self.SE104v = self.InfluxDB.InfluxDBreader(self.query_SE104v)
            self.SE104v = self.SE104v["SE-104v"].tolist()
        
        else:

            self.SE104v = self.SE104v["SE-104"].tolist()
    
    def Pump101 (self, manual_P101=0, FT_P101=5, TTO_P101=10, Q_P101 = 2.4):
        self.manual_P101 = manual_P101
        
        if self.manual_P101 == 1 or self.DigitalTwin == 0 or self.Online == 0:
            self.FT_P101= FT_P101
            self.TTO_P101 = TTO_P101
        
            self.TurnOnDailyStep_P101 = 24/self.FT_P101
            
            if self.TimeCounterPump_P101<self.TTO_P101*60:
               self.Q_P101 = Q_P101
            else:
               self.Q_P101= float(0)
            
            self.TimeCounterPump_P101 = self.TimeCounterPump_P101 + self.tp
            
            if self.TimeCounterPump_P101>=self.TurnOnDailyStep_P101*3600:
                self.TimeCounterPump_P101 = 0

            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][101], variable = self.database_df["Tag"][101], value = self.Q_P101, timestamp = self.timestamp)

            self.query_SE101v = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "SE-101v", location=1, type=1, forecastTime=1) 
            self.SE101v = self.InfluxDB.InfluxDBreader(self.query_SE101v)
            self.SE101v = self.SE101v["SE-101v"].tolist()
        else:

            self.SE101v = self.SE101v["SE-101"].tolist()
        
    def Pump102 (self, manual_P102=0, FT_P102=5, TTO_P102=10, Q_P102 = 2.4):
        self.manual_P102 = manual_P102

        if self.manual_P102 == 1 or self.DigitalTwin == 0 or self.Online == 0:
            self.FT_P102= FT_P102
            self.TTO_P102 = TTO_P102

            self.TurnOnDailyStep_P102 = 24/self.FT_P102

            if self.TimeCounterPump_P102<self.TTO_P102*60:
               self.Q_P102 = Q_P102
            else:
               self.Q_P102= float(0)
            
            self.TimeCounterPump_P102 = self.TimeCounterPump_P102 + self.tp

            if self.TimeCounterPump_P102>=self.TurnOnDailyStep_P102*3600:
                self.TimeCounterPump_P102 = 0
            
            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][102], variable = self.database_df["Tag"][102], value = self.Q_P102, timestamp = self.timestamp)

            self.query_SE102v = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "SE-102v", location=1, type=1, forecastTime=1) 
            self.SE102v = self.InfluxDB.InfluxDBreader(self.query_SE102v)
            self.SE102v = self.SE102v["SE-102v"].tolist()

        else:

            self.SE102v = self.SE102v["SE-102"].tolist()
        
    def Temperature_R101 (self, manual_temp_R101 = 1, Temp_R101=35):
        self.manual_temp_R101 = manual_temp_R101

        if self.manual_temp_R101 == 1 or self.Online == 0:
            self.Temp_R101 = Temp_R101

            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][103], variable = self.database_df["Tag"][103], value = self.Temp_R101, timestamp = self.timestamp)
            
            self.query_TE101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "TE-101v", location=1, type=1, forecastTime=1) 
            self.TE_101v = self.InfluxDB.InfluxDBreader(self.query_TE101)
            self.TE_101v = self.TE_101v["TE-101v"].tolist()

        else:

            self.TE_101Av = self.TE_101Av["TE-101A"].tolist()
            self.TE_101Bv = self.TE_101Bv["TE-101B"].tolist()

            T1 = self.TE_101Av[-1]
            T2 = self.TE_101Bv[-1]
            Tf = (T1 + T2)/2

            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][103], variable = self.database_df["Tag"][103], value = Tf, timestamp = self.timestamp)
        
    def V_101_DT (self):
        self.AT103A1v = self.AT103A1v["AT-103A1"]
        self.AT103A2v = self.AT103A2v["AT-103A2"]
        self.AT103A3v = self.AT103A3v["AT-103A3"]
        self.AT103A4v = self.AT103A4v["AT-103A4"]
        self.AT103A5v = self.AT103A5v["AT-103A5"]

        self.RH_V101 = self.AT103Bv["AT-103B"]

        self.PT103v = self.PT103v["PT-103"]
        self.TT103v = self.TT103v["TT-103"]
        self.SV103v = self.SV103v["SV-103"]

        self.P_std = 100
        self.T_std = 273.15

        self.V_normal_V101 = ((self.PT103v.iloc[-1]*6.89476)*self.VG1*self.T_std)/(self.P_std*(self.TT103v.iloc[-1]+273.15))
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][104], variable = self.database_df["Tag"][104], value = self.V_normal_V101, timestamp = self.timestamp)
        
        self.V_normal_CH4_V101 = self.AT103A1v.iloc[-1]/100*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][105], variable = self.database_df["Tag"][105], value = self.V_normal_CH4_V101, timestamp = self.timestamp)

        self.V_normal_CO2_V101 = self.AT103A2v.iloc[-1]/100*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][106], variable = self.database_df["Tag"][106], value = self.V_normal_CO2_V101, timestamp = self.timestamp)

        self.V_normal_H2S_V101 = self.AT103A3v.iloc[-1]/1000000*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][107], variable = self.database_df["Tag"][107], value = self.V_normal_H2S_V101, timestamp = self.timestamp)

        self.V_normal_O2_V101 = self.AT103A4v.iloc[-1]/100*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][108], variable = self.database_df["Tag"][108], value = self.V_normal_O2_V101, timestamp = self.timestamp)

        self.V_normal_H2_V101 = self.AT103A5v.iloc[-1]/1000000*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][109], variable = self.database_df["Tag"][109], value = self.V_normal_H2_V101, timestamp = self.timestamp)

        self.V_mol_CH4 = self.Thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_CO2 = self.Thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_H2S = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_O2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_H2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]

        self.mol_CH4_V101 = self.V_normal_CH4_V101/self.V_mol_CH4     
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][110], variable = self.database_df["Tag"][110], value = self.mol_CH4_V101, timestamp = self.timestamp)

        self.mol_CO2_V101 = self.V_normal_CO2_V101/self.V_mol_CO2
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][111], variable = self.database_df["Tag"][111], value = self.mol_CO2_V101, timestamp = self.timestamp)

        self.mol_H2S_101 = self.V_normal_H2S_V101/self.V_mol_H2S
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][112], variable = self.database_df["Tag"][112], value = self.mol_H2S_101, timestamp = self.timestamp)

        self.mol_O2_V101 = self.V_normal_O2_V101/self.V_mol_O2
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][113], variable = self.database_df["Tag"][113], value = self.mol_O2_V101, timestamp = self.timestamp)

        self.mol_H2_V101 = self.V_normal_H2_V101/self.V_mol_H2
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][114], variable = self.database_df["Tag"][114], value = self.mol_H2_V101, timestamp = self.timestamp)

        self.RH_V101 = self.AT103Bv.iloc[-1]/100
        self.AH_v101 = self.Thermo.BiogasAbsoluteHumidity(self.RH_V101, self.TT103v.iloc[-1])
        self.mol_H2O_V101 = self.AH_v101*self.V_normal_V101
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][115], variable = self.database_df["Tag"][115], value = self.mol_H2O_V101, timestamp = self.timestamp)

        if (len (self.PT103v) > 1) and (self.PT103v.iloc[-1] < self.PT103v.iloc[-2]-0.01):  #Cambiar cuando se conecte con la planta real
            self.P_ini_V101 = self.Pacum_v101
        
        self.Pacum_v101 = self.PT103v.iloc[-1] + self.P_ini_V101
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][116], variable = self.database_df["Tag"][116], value = self.Pacum_v101, timestamp = self.timestamp)

        self.Vnormal_acum_v101 = ((self.Pacum_v101*6.89476)*self.VG1*self.T_std)/(self.P_std*(self.TT103v.iloc[-1]+273.15))
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][117], variable = self.database_df["Tag"][117], value = self.Vnormal_acum_v101, timestamp = self.timestamp)
    
    def R101_DT (self, Operation_mode=1):
        self.Operation_mode = Operation_mode

        if Operation_mode == 1:
            if self.SE104v[-1]==0:
                self.Msus_exp_R101 = (self.Csus_ini*self.VR1 - (1/self.s_CH4)*self.mol_CH4_V101)
            else:
                self.Msus_exp_R101 = (self.SE104v[-1]*self.Csus_ini*self.tp/60) - (self.SE104v[-1]*(self.Csus_ini*self.VR1 - (1/self.s_CH4)*self.mol_CH4_V101)/self.VR1*self.tp/60) - (self.Csus_ini*self.VR1 - (1/self.s_CH4)*self.mol_CH4_V101)

            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][118], variable = self.database_df["Tag"][118], value = self.Msus_exp_R101, timestamp = self.timestamp)

            self.Csus_exp_R101 = self.Msus_exp_R101/self.VR1
            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][119], variable = self.database_df["Tag"][119], value = self.Csus_exp_R101, timestamp = self.timestamp)

            self.SV_exp_R101 = (self.Csus_exp_R101)*self.MW_sustrato/self.rho
            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][120], variable = self.database_df["Tag"][120], value = self.SV_exp_R101, timestamp = self.timestamp)

            self.ST_exp_R101 = (self.Csus_exp_R101+self.Csus_fixed)*self.MW_sustrato/self.rho
            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][121], variable = self.database_df["Tag"][121], value = self.ST_exp_R101, timestamp = self.timestamp)
