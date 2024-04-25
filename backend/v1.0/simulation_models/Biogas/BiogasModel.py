#import sys
import os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
current_directory = os.getcwd()
excel_file_path = os.path.join(os.path.abspath(os.path.join(current_directory, '..', '..')), "tools", "DB_Mapping.xlsx")
print(excel_file_path)

import pandas as pd
import time
from datetime import datetime
import ThermoProperties as TP
from scipy.integrate import odeint
from scipy.optimize import minimize
import numpy as np
import statistics as st
from  tools import DBManager


class BiogasPlant:

    def __init__(self, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, t_prediction = 1, timetrain=1, Kini=1):

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
        
        #Initial values
        self.TotalTime = 0
        self.TimeCounterPump = 0
        self.Pacum = 0
        self.P_ini = 0

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

    def DTOperationModel1 (self, manual_P104=0, manual_temp_R101=0,  TRH=30, FT_P104=5, TTO_P104=10, Temp_R101 = 35):
        
        #%%Obtención de las variables que no tienen sensores
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
            self.query_SE104v = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "SE-104v", location=1, type=1, forecastTime=1) 
            self.SE104v = self.InfluxDB.InfluxDBreader(self.query_SE104v)
            self.SE104v = self.SE104v["SE-104v"].tolist()
        
        else:

            self.SE104v = self.SE104v["SE-104"].tolist()
        
        if (self.Online == 0 or self.manual_temp_R101 == 1):

            self.Temp_R101 = Temp_R101
            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][92], variable = self.database_df["Tag"][92], value = self.Temp_R101, timestamp = self.timestamp)
            
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
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][92], variable = self.database_df["Tag"][92], value = Tf, timestamp = self.timestamp)

            self.query_TE101 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "TE-101v", location=1, type=0, forecastTime=1) 
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
        
        self.V_normal_CO2 = self.AT103A2v.iloc[-1]/100*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][95], variable = self.database_df["Tag"][95], value = self.V_normal_CO2, timestamp = self.timestamp)

        self.V_normal_H2S = self.AT103A3v.iloc[-1]/1000000*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][96], variable = self.database_df["Tag"][96], value = self.V_normal_H2S, timestamp = self.timestamp)

        self.V_normal_O2 = self.AT103A4v.iloc[-1]/100*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][97], variable = self.database_df["Tag"][97], value = self.V_normal_O2, timestamp = self.timestamp)

        self.V_normal_H2 = self.AT103A5v.iloc[-1]/1000000*self.V_normal
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][98], variable = self.database_df["Tag"][98], value = self.V_normal_H2, timestamp = self.timestamp)

        self.RH_V101 = self.AT103Bv.iloc[-1]/100
        self.AH_v101 = self.Thermo.BiogasAbsoluteHumidity(self.RH_V101, self.TT103v.iloc[-1])
        self.mol_H2O = self.AH_v101*self.V_normal
        
        self.V_mol_CH4 = self.Thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_CO2 = self.Thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_H2S = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_O2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_H2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
      
        self.mol_CH4 = self.V_normal_CH4/self.V_mol_CH4     
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][95], variable = self.database_df["Tag"][95], value = self.mol_CH4, timestamp = self.timestamp)

        self.V_mol_CO2 = self.V_normal_CO2/self.V_mol_CO2
                


        P_iniv = []
        if len(self.PT103v)>1:
            if self.SV103v.iloc[-1] == 1 or self.PT103v.iloc[-1] < (self.PT103v.iloc[-2]-0.01):
                P_iniv.append(self.PT103v.iloc[-1])
                self.P_ini =self.Pacum
        #print(self.P_ini)
        #print(self.Pacum)
        
        self.Pacum = self.PT103v.iloc[-1] + self.P_ini
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][96], variable = self.database_df["Tag"][96], value = self.Pacum, timestamp = self.timestamp)
        
        self.Vnormal_acum = ((self.Pacum*6.89476)*self.VG1*self.T_std)/(self.P_std*(self.TT103v.iloc[-1]+273.15))
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][97], variable = self.database_df["Tag"][97], value = self.Vnormal_acum, timestamp = self.timestamp)
        
        if self.SE104v[-1] == 0:
            self.Msus_exp = (self.Csus_ini*self.VR1 - (1/self.s_CH4)*self.mol_CH4)
        else:
            self.Msus_exp = (self.SE104v[-1]*self.Csus_ini*self.tp/60)-(self.SE104v[-1]*((1/self.s_CH4)*self.mol_CH4)*self.tp/60) + (self.Csus_ini*self.VR1 - (1/self.s_CH4)*self.mol_CH4)
        
        # print("moles de sustrato acumulado" + str(self.Msus_exp))
        # self.v1 = (self.SE104v[-1]*self.Csus_ini*self.tp/60)
        # self.v = (self.SE104v[-1]*((1/self.s_CH4)*self.mol_CH4)*self.tp/60)
        # self.v2 = (self.Csus_ini*self.VR1 - (1/self.s_CH4)*self.mol_CH4)
        # print(str(self.v))
        # print(str(self.v1))
        # print(str(self.v2))
              
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][98], variable = self.database_df["Tag"][98], value = self.Msus_exp, timestamp = self.timestamp)
       
        self.Csus_exp = self.Msus_exp/self.VR1
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][99], variable = self.database_df["Tag"][99], value = self.Csus_exp, timestamp = self.timestamp)

        self.SV_exp = (self.Csus_exp)*self.MW_sustrato/self.rho
        print("Concentracion de SV: "+str(self.SV_exp))
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][100], variable = self.database_df["Tag"][100], value = self.SV_exp, timestamp = self.timestamp)

        self.ST_exp = (self.Csus_exp+self.Csus_fixed)*self.MW_sustrato/self.rho
        print("Concentracion de ST: "+str(self.ST_exp))
        self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][101], variable = self.database_df["Tag"][101], value = self.ST_exp, timestamp = self.timestamp)
      
        self.query_Msus_exp = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "Msus_exp", location=1, type=1, forecastTime=1)
        self.Msus_expv = self.InfluxDB.InfluxDBreader(self.query_Msus_exp)
        self.Msus_expv = self.Msus_expv["Msus_exp"].tolist()

        self.Q_P104v = self.SE104v

        self.query_molCH4 = self.InfluxDB.QueryCreator(device = "DTPlantaBiogas", variable = "M-molA_CH4", location=1, type=1, forecastTime=1)
        self.mol_CH4v = self.InfluxDB.InfluxDBreader(self.query_molCH4)
        self.mol_CH4v = self.mol_CH4v["M-molA_CH4"].tolist()
        
        self.query_VN_biogas = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable="M-VGA", location=1, type=1, forecastTime=1)
        self.VN_biogasv = self.InfluxDB.InfluxDBreader(self.query_VN_biogas)
        self.VN_biogasv = self.VN_biogasv["M-VGA"].tolist()
        
        self.points = int(round(2*(self.timetrain/self.tp),0))
        print("Puntos para sustrato experimental "+str(len(self.Msus_expv)))
        print("Puntos que debe tener para entrenarse "+str(self.points))
        
        #%% Optimización
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
            
            self.PredictionPoints = int(round(self.t_prediction/self.tp,0))
            self.t_predictionv = np.linspace(self.TotalTime+self.timetrain+self.validation_time+self.tp, self.TotalTime+self.timetrain+self.validation_time+self.t_prediction, self.PredictionPoints)

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
            
            #Run train model
            self.K_optimizadav = []
            self.Csus_model_train = []

            for i in range (len(self.t_train)):
                self.tv = self.t_train[i : i+2]
                self.C_train = self.Csus_exp_train [i : i+2]
                self.Q_train = self.Q_P104_train [i : i+2]

                self.Ko = self.Kini
                self.Optimizacion = Optimization(K=self.Ko, t=self.tv, Csus_exp = self.C_train, Q = self.Q_train)

                self.K_optimizadav.append(float(self.Optimizacion[0]))
                self.Kini = float(self.Optimizacion[0])
                self.Csus_model_train.append(float(self.Optimizacion[1][0]))

            self.K_mean = st.mean(self.K_optimizadav)
            self.timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            self.InfluxDB.InfluxDBwriter(load = self.database_df["Device"][102], variable = self.database_df["Tag"][102], value = self.K_mean, timestamp = self.timestamp)
            print(self.K_optimizadav)

            #Run validation
            self.Validationv = []
            for i in range (len(self.t_val)):
                self.tvv = self.t_val[i : i+2]
                self.C_val = self.Csus_exp_val[i : i+2]
                self.Q_val = self.Q_P104_val[i : i+2]

                self.validation = ValidationModel1(K = self.K_mean, t = self.tvv, Q = self.Q_val, C = self.C_val)
                self.Validationv.append(float(self.validation[-1]))

            #Run Prediction
            #Prediction pump behavior

            self.Q_P104_predv = []
            self.Co = float(self.Validationv[-1])
            self.Csus_model_prediction = []
            
            for i in range (len(self.t_predictionv)):
                    
                #timers
                self.t_prediction1v = self.t_predictionv[i : i+2]
                self.TimeCounterPump_pred = self.TimeCounterPump + self.tp
                
                #pump control
                if self.TimeCounterPump_pred<self.TTO_P104*60:
                    self.Q_P104_pred = (self.Q_time/self.TTO_P104)*60
                
                else:
                    self.Q_P104_pred= float(0)    
                
                self.Q_P104_predv.append(self.Q_P104_pred)
            
                self.Csus_model_prediction.append(self.Co)
                self.prediction = ValidationModel1(K=self.K_mean, t=self.t_prediction1v, Q=[self.Q_P104_pred], C=[self.Co])
                self.Co = float(self.prediction[-1])
                self.Csus_model_prediction.append(self.Co)
                
            #%%Puede ser otra función
            self.CH2O_trainv=[]
            self.NCH4_model_trainv=[]
            self.NCO2_model_trainv=[]
            self.NH2S_model_trainv=[]
            self.NH3_model_trainv=[]
            self.xCH4_model_trainv=[]
            self.xCO2_model_trainv=[]
            self.xH2S_model_trainv=[]
            self.xNH3_model_trainv=[]
            self.VN_biogas_model_trainv=[]
            self.SV_trainv = []
            self.ST_trainv=[]

            #Train Data Interface Visualization
            for i in range (len(self.t_train)):
                self.SV_train = (self.Csus_model_train[i])*self.MW_sustrato/self.rho
                self.Nsus_train = self.Csus_model_train[i]*self.VR1
                self.Nsus_ini = self.Csus_ini*self.VR1
                self.x_train = (self.Nsus_ini - self.Nsus_train)/self.Nsus_ini

                self.CH2O_train = self.Ch2o_ini - self.s_H2O*self.Csus_ini*self.x_train

                self.ST_train = (self.Csus_model_train[i]+self.Csus_fixed)*self.MW_sustrato/self.rho

                self.NCH4_model_train = self.s_CH4*self.Nsus_ini*self.x_train
                self.NCO2_model_train = self.s_CO2*self.Nsus_ini*self.x_train
                self.NH3_model_train = self.s_NH3*self.Nsus_ini*self.x_train
                self.NH2S_model_train = self.s_H2S*self.Nsus_ini*self.x_train

                self.Nbiogas_train = self.NCH4_model_train + self.NCO2_model_train + self.NH3_model_train + self.NH2S_model_train
                    
                self.x_CH4_model_train = self.NCH4_model_train/self.Nbiogas_train
                self.x_CO2_model_train = self.NCO2_model_train/self.Nbiogas_train
                self.x_NH3_model_train = self.NH3_model_train/self.Nbiogas_train
                self.x_H2S_model_train = self.NH2S_model_train/self.Nbiogas_train

                self.VN_biogas_model_train = (self.Nbiogas_train*8.314*self.T_std)/self.P_std

                self.CH2O_trainv.append(self.CH2O_train)
                
                self.NCH4_model_trainv.append(self.NCH4_model_train)
                self.NCO2_model_trainv.append(self.NCO2_model_train)
                self.NH2S_model_trainv.append(self.NH2S_model_train)
                self.NH3_model_trainv.append(self.NH3_model_train)
                
                self.VN_biogas_model_trainv.append(self.VN_biogas_model_train)
                
                self.xCH4_model_trainv.append(self.x_CH4_model_train)
                self.xCO2_model_trainv.append(self.x_CO2_model_train)
                self.xH2S_model_trainv.append(self.x_H2S_model_train)
                self.xNH3_model_trainv.append(self.x_NH3_model_train)
                
                self.SV_trainv.append(self.SV_train)
                self.ST_trainv.append(self.ST_train)
            
            #Validation data Interface visualization
            self.CH2O_valv=[]
            self.NCH4_model_valv=[]
            self.NCO2_model_valv=[]
            self.NH2S_model_valv=[]
            self.NH3_model_valv=[]
            self.xCH4_model_valv=[]
            self.xCO2_model_valv=[]
            self.xH2S_model_valv=[]
            self.xNH3_model_valv=[]
            self.VN_biogas_model_valv=[]
            self.SV_valv = []
            self.ST_valv=[]

            for i in range (len(self.t_val)):
                self.SV_val = (self.Validationv[i])*self.MW_sustrato/self.rho
                self.Nsus_val = self.Validationv[i]*self.VR1
                self.Nsus_ini = self.Csus_ini*self.VR1
                self.x_val = (self.Nsus_ini - self.Nsus_val)/self.Nsus_ini

                self.CH2O_val = self.Ch2o_ini - self.s_H2O*self.Csus_ini*self.x_val

                self.ST_val = (self.Validationv[i]+self.Csus_fixed)*self.MW_sustrato/self.rho

                self.NCH4_model_val = self.s_CH4*self.Nsus_ini*self.x_val
                self.NCO2_model_val = self.s_CO2*self.Nsus_ini*self.x_val
                self.NH3_model_val = self.s_NH3*self.Nsus_ini*self.x_val
                self.NH2S_model_val = self.s_H2S*self.Nsus_ini*self.x_val

                self.Nbiogas_val = self.NCH4_model_val + self.NCO2_model_val + self.NH3_model_val + self.NH2S_model_val
                    
                self.x_CH4_model_val = self.NCH4_model_val/self.Nbiogas_val
                self.x_CO2_model_val = self.NCO2_model_val/self.Nbiogas_val
                self.x_NH3_model_val = self.NH3_model_train/self.Nbiogas_val
                self.x_H2S_model_val = self.NH2S_model_train/self.Nbiogas_val

                self.VN_biogas_model_val = (self.Nbiogas_val*8.314*self.T_std)/self.P_std

                
                self.NCH4_model_valv.append(self.NCH4_model_val)
                self.NCO2_model_valv.append(self.NCO2_model_val)
                self.NH2S_model_valv.append(self.NH2S_model_val)
                self.NH3_model_valv.append(self.NH3_model_val)
                
                self.VN_biogas_model_valv.append(self.VN_biogas_model_val)
                
                self.xCH4_model_valv.append(self.x_CH4_model_val)
                self.xCO2_model_valv.append(self.x_CO2_model_val)
                self.xH2S_model_valv.append(self.x_H2S_model_val)
                self.xNH3_model_valv.append(self.x_NH3_model_val)
                
                self.SV_valv.append(self.SV_val)
                self.ST_trainv.append(self.ST_train)
            
            #Prediction data Interface visualization
            self.CH2O_predv=[]
            self.NCH4_model_predv=[]
            self.NCO2_model_predv=[]
            self.NH2S_model_predv=[]
            self.NH3_model_predv=[]
            self.xCH4_model_predv=[]
            self.xCO2_model_predv=[]
            self.xH2S_model_predv=[]
            self.xNH3_model_predv=[]
            self.VN_biogas_model_predv=[]
            self.SV_predv = []
            self.ST_predv=[]

            for i in range (len(self.t_prediction)):
                self.SV_pred = (self.Csus_model_prediction[i])*self.MW_sustrato/self.rho
                self.Nsus_pred = self.Csus_model_prediction[i]*self.VR1
                self.Nsus_ini = self.Csus_ini*self.VR1
                self.x_pred = (self.Nsus_ini - self.Nsus_pred)/self.Nsus_ini

                self.CH2O_pred = self.Ch2o_ini - self.s_H2O*self.Csus_ini*self.x_pred

                self.ST_pred = (self.Csus_model_prediction[i]+self.Csus_fixed)*self.MW_sustrato/self.rho

                self.NCH4_model_pred = self.s_CH4*self.Nsus_ini*self.x_pred
                self.NCO2_model_pred = self.s_CO2*self.Nsus_ini*self.x_pred
                self.NH3_model_pred = self.s_NH3*self.Nsus_ini*self.x_pred
                self.NH2S_model_pred = self.s_H2S*self.Nsus_ini*self.x_pred

                self.Nbiogas_pred = self.NCH4_model_pred + self.NCO2_model_pred + self.NH3_model_pred + self.NH2S_model_pred
                    
                self.x_CH4_model_pred = self.NCH4_model_pred/self.Nbiogas_pred
                self.x_CO2_model_pred = self.NCO2_model_pred/self.Nbiogas_pred
                self.x_NH3_model_pred = self.NH3_model_train/self.Nbiogas_pred
                self.x_H2S_model_pred = self.NH2S_model_train/self.Nbiogas_pred

                self.VN_biogas_model_pred = (self.Nbiogas_pred*8.314*self.T_std)/self.P_std

                
                self.NCH4_model_predv.append(self.NCH4_model_pred)
                self.NCO2_model_predv.append(self.NCO2_model_pred)
                self.NH2S_model_predv.append(self.NH2S_model_pred)
                self.NH3_model_predv.append(self.NH3_model_pred)
                
                self.VN_biogas_model_predv.append(self.VN_biogas_model_pred)
                
                self.xCH4_model_predv.append(self.x_CH4_model_pred)
                self.xCO2_model_predv.append(self.x_CO2_model_pred)
                self.xH2S_model_predv.append(self.x_H2S_model_pred)
                self.xNH3_model_predv.append(self.x_NH3_model_pred)
                
                self.SV_predv.append(self.SV_pred)
                self.ST_predv.append(self.ST_pred)




        self.TotalTime = self.TotalTime + self.tp
        time.sleep(self.tp)
