import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
current_directory = os.getcwd()
print(current_directory)
excel_file_path = os.path.join(os.path.abspath(os.path.join(current_directory)), "v1.0", "tools", "DB_Mapping.xlsx")
print(excel_file_path)

import pandas as pd
from datetime import datetime
from simulation_models.Biogas import ThermoProperties as TP
from  tools import DBManager


class BiogasPlantDT:

    def __init__(self, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30,
                 ST_R101=10, SV_R101=1, Cc_R101=40.48, Ch_R101=5.29, Co_R101=29.66, Cn_R101=1.37, Cs_R101=0.211, rho_R101 = 1000,
                 ST_R102=10, SV_R102=1, Cc_R102=40.48, Ch_R102=5.29, Co_R102=29.66, Cn_R102=1.37, Cs_R102=0.211, rho_R102 = 1000, OperationMode=1):

        #Interface Inputs
        self.VR1 = VR1
        self.VR2 = VR2
        self.VG1 = VG1
        self.VG2 = VG2
        self.VG3 = VG3
        self.databaseConnection_df = pd.read_excel(excel_file_path, sheet_name='ConexionDB')
        self.database_df = pd.read_excel(excel_file_path, sheet_name='InfluxDBVariables')
        index = 1
        self.InfluxDB = DBManager.InfluxDBmodel(server = 'http://' + str(self.databaseConnection_df['IP'][index])+':'+str(self.databaseConnection_df['Port'][index])+'/', org = self.databaseConnection_df['Organization'][index], bucket = self.databaseConnection_df['Bucket'][index], token = self.databaseConnection_df['Token'][index])
        self.Thermo = TP.ThermoProperties()
        self.tp = tp
        #Initial values
        #Global time
        self.TotalTime = 0
        #Pumps
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
        
        self.ST_R101 = ST_R101/100
        self.SV_R101 = SV_R101/100

        if ST_R101 == 0:
            self.Csus_ini_R101 = 0
            self.SV_R101 = 0
            self.rho_R101 = rho_R101
        else:
            self.ST_R101 = ST_R101/100
            self.SV_R101 = SV_R101/100
            self.Cc_R101 = Cc_R101
            self.Ch_R101 = Ch_R101
            self.Co_R101 = Co_R101
            self.Cn_R101 = Cn_R101
            self.Cs_R101 = Cs_R101
            self.rho_R101 = rho_R101
        
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
            self.Ch2o_ini_R101 = (self.rho_R101*(1-self.ST_R101))/18
        
        #Reactor 102 initial conditions
        self.ST_R102 = ST_R102/100
        self.SV_R102 = SV_R102/100
        
        if ST_R102 == 0:
            self.Csus_ini_R102 = 0
            self.SV_R102 = 0
            self.rho_R102 = rho_R102
        else:
            self.ST_R102 = ST_R102/100
            self.SV_R102 = SV_R102/100
            self.Cc_R102 = Cc_R102
            self.Ch_R102 = Ch_R102
            self.Co_R102 = Co_R102
            self.Cn_R102 = Cn_R102
            self.Cs_R102 = Cs_R102
            self.rho_R102 = rho_R102

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
            self.Ch2o_ini_R102 = (self.rho_R102*(1-self.ST_R102))/18
        
        #Create DataFrames to storage Data
        self.OperationMode = OperationMode
        self.DT_Data = pd.DataFrame()
        if self.OperationMode ==1:
            self.DT_Data["timestamp"] = None
            self.DT_Data["Q_P104"] = None
            self.DT_Data["Temp_R101"] = None
            self.DT_Data["V_normal_V101"] = None
            self.DT_Data["V_normal_CH4_V101"] = None
            self.DT_Data["V_normal_CO2_V101"] = None
            self.DT_Data["V_normal_H2S_V101"] = None
            self.DT_Data["V_normal_O2_V101"] = None
            self.DT_Data["V_normal_H2_V101"] = None
            self.DT_Data["mol_CH4_V101"] = None
            self.DT_Data["mol_CO2_V101"] = None
            self.DT_Data["mol_H2S_V101"] = None
            self.DT_Data["mol_O2_V101"] = None
            self.DT_Data["mol_H2_V101"] = None
            self.DT_Data["mol_H2O_V101"] = None
            self.DT_Data["Pacum_V101"] = None
            self.DT_Data["Vnormal_acum_V101"] = None
            self.DT_Data["mol_CH4_acum_V101"] = None
            self.DT_Data["mol_sus_int_ini_R101"] = None
            self.DT_Data["Csus_ini_R101"] = None
            self.DT_Data["SV_R101"] = None
            self.DT_Data["ST_R101"] = None
        
        if self.OperationMode == 2:
            self.DT_Data["timestamp"] = None
            self.DT_Data["Q_P104"] = None
            self.DT_Data["Q_P101"] = None
            self.DT_Data["Temp_R101"] = None
            self.DT_Data["V_normal_V101"] = None
            self.DT_Data["V_normal_V101"] = None
            self.DT_Data["V_normal_CH4_V101"] = None
            self.DT_Data["V_normal_CO2_V101"] = None
            self.DT_Data["V_normal_H2S_V101"] = None
            self.DT_Data["V_normal_O2_V101"] = None
            self.DT_Data["V_normal_H2_V101"] = None
            self.DT_Data["mol_CH4_V101"] = None
            self.DT_Data["mol_CO2_V101"] = None
            self.DT_Data["mol_H2S_V101"] = None
            self.DT_Data["mol_O2_V101"] = None
            self.DT_Data["mol_H2_V101"] = None
            self.DT_Data["mol_H2O_V101"] = None
            self.DT_Data["Pacum_V101"] = None
            self.DT_Data["Vnormal_acum_V101"] = None
            self.DT_Data["mol_CH4_acum_V101"] = None
            self.DT_Data["mol_sus_int_ini_R101"] = None
            self.DT_Data["Csus_ini_R101"] = None
            self.DT_Data["SV_R101"] = None
            self.DT_Data["ST_R101"] = None

        if self.OperationMode == 3:
            self.DT_Data["timestamp"] = None
            self.DT_Data["Q_P104"] = None
            self.DT_Data["Q_P101"] = None
            self.DT_Data["Temp_R101"] = None 
            self.DT_Data["Temp_R102"] = None
            
            self.DT_Data["V_normal_V101"] = None
            self.DT_Data["V_normal_V101"] = None
            self.DT_Data["V_normal_CH4_V101"] = None
            self.DT_Data["V_normal_CO2_V101"] = None
            self.DT_Data["V_normal_H2S_V101"] = None
            self.DT_Data["V_normal_O2_V101"] = None
            self.DT_Data["V_normal_H2_V101"] = None
            self.DT_Data["mol_CH4_V101"] = None
            self.DT_Data["mol_CO2_V101"] = None
            self.DT_Data["mol_H2S_V101"] = None
            self.DT_Data["mol_O2_V101"] = None
            self.DT_Data["mol_H2_V101"] = None
            self.DT_Data["mol_H2O_V101"] = None
            self.DT_Data["Pacum_V101"] = None
            self.DT_Data["Vnormal_acum_V101"] = None
            self.DT_Data["mol_CH4_acum_V101"] = None

            self.DT_Data["V_normal_V102"] = None
            self.DT_Data["V_normal_V102"] = None
            self.DT_Data["V_normal_CH4_V102"] = None
            self.DT_Data["V_normal_CO2_V102"] = None
            self.DT_Data["V_normal_H2S_V102"] = None
            self.DT_Data["V_normal_O2_V102"] = None
            self.DT_Data["V_normal_H2_V102"] = None
            self.DT_Data["mol_CH4_V102"] = None
            self.DT_Data["mol_CO2_V102"] = None
            self.DT_Data["mol_H2S_V102"] = None
            self.DT_Data["mol_O2_V102"] = None
            self.DT_Data["mol_H2_V102"] = None
            self.DT_Data["mol_H2O_V102"] = None
            self.DT_Data["Pacum_V102"] = None
            self.DT_Data["Vnormal_acum_V102"] = None
            self.DT_Data["mol_CH4_acum_V102"] = None

            self.DT_Data["mol_sus_int_ini_R101"] = None
            self.DT_Data["Csus_ini_R101"] = None
            self.DT_Data["SV_R101"] = None
            self.DT_Data["ST_R101"] = None

            self.DT_Data["mol_sus_int_ini_R102"] = None
            self.DT_Data["Csus_ini_R102"] = None
            self.DT_Data["SV_R102"] = None
            self.DT_Data["ST_R102"] = None

                      
    def GetValuesFromBiogasPlant (self):
        
        msg = self.InfluxDB.InfluxDBconnection()
        if not msg:
            return {"message":self.influxDB.ERROR_MESSAGE}, 503
        
        query = self.InfluxDB.QueryCreator(measurement = "Planta Biogás", type = 2)
        data_biogas = self.InfluxDB.InfluxDBreader(query)
        data_biogas.set_index("_field", inplace = True)
        
        #Get total solids from real biogas plant interface (HMI)
        #self.queryST = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-ST", location=1, type=1, forecastTime=1) 
        #self.ST = self.InfluxDB.InfluxDBreader(self.queryST)
        self.ST = data_biogas["_value"]["MST"]

        #Get volatile solids from real biogas plant interface (HMI)
        # self.querySV = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-SV", location=1, type=1, forecastTime=1) 
        # self.SV = self.InfluxDB.InfluxDBreader(self.querySV)
        self.SV = data_biogas["_value"]["MSV"]

        #Get Carbon concentration from real biogas plant interface (HMI)
        # self.queryCc = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Cc", location=1, type=1, forecastTime=1) 
        # self.Cc = self.InfluxDB.InfluxDBreader(self.queryCc)
        self.Cc = data_biogas["_value"]["MCc"]

        #Get Hydrogen concentration from real biogas plant interface (HMI)
        # self.queryCh = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Ch", location=1, type=1, forecastTime=1)
        # self.Ch = self.InfluxDB.InfluxDBreader(self.queryCh)
        self.Ch = data_biogas["_value"]["MCh"]

        #Get Oxygen concentration from real biogas plant interface (HMI)
        # self.queryCo = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Co", location=1, type=1, forecastTime=1)
        # self.Co = self.InfluxDB.InfluxDBreader(self.queryCo)
        self.Co = data_biogas["_value"]["MCo"]

        #Get nitrogen concentration from real biogas plant interface (HMI)
        # self.queryCn = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Cn", location=1, type=1, forecastTime=1)
        # self.Cn = self.InfluxDB.InfluxDBreader(self.queryCn)
        self.Cn = data_biogas["_value"]["MCn"]

        #Get sulfide concentration from real biogas plant interface (HMI)
        # self.queryCs = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-Cs", location=1, type=1, forecastTime=1)
        # self.Cs = self.InfluxDB.InfluxDBreader(self.queryCs)
        self.Cs = data_biogas["_value"]["MCs"]

        #Get density of substract from real biogas plant interface (HMI)
        # self.query_rho = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "M-d", location=1, type=1, forecastTime=1)
        # self.rho = self.InfluxDB.InfluxDBreader(self.query_rho)        
        self.rho = data_biogas["_value"]["Md"]

        #Get pump-104 flow from real biogas plant
        # self.query_SE104 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SE-104", location=1, type=1, forecastTime=1)
        # self.SE104v = self.InfluxDB.InfluxDBreader(self.query_SE104)        
        self.SE104v = data_biogas["_value"]["SE104"]

        #Get Temperature from TE101A from real biogas plant
        # self.query_TE101A = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TE-101A", location=1, type=1, forecastTime=1)
        # self.TE_101Av = self.InfluxDB.InfluxDBreader(self.query_TE101A)        
        self.TE_101Av = data_biogas["_value"]["TE101A"]
        
        #Get Temperature from TE101B from real biogas plant
        # self.query_TE101B = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TE-101B", location=1, type=1, forecastTime=1)
        # self.TE_101Bv = self.InfluxDB.InfluxDBreader(self.query_TE101B)
        self.TE_101Bv = data_biogas["_value"]["TE101B"]

        #Get temperature from TE102A from real biogas plant
        # self.query_TE102A = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TE-102A", location=1, type=1, forecastTime=1)
        # self.TE_102Av = self.InfluxDB.InfluxDBreader(self.query_TE102A)
        self.TE_102Av = data_biogas["_value"]["TE102A"]

        #Get temperature from TE102B from real biogas plant
        # self.query_TE102B = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TE-102B", location=1, type=1, forecastTime=1)
        # self.TE_102Bv = self.InfluxDB.InfluxDBreader(self.query_TE102B)        
        self.TE_102Bv = data_biogas["_value"]["TE102B"]

        #Get pump-101 flow from real biogas plant
        # self.query_SE101 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SE-101", location=1, type=1, forecastTime=1)
        # self.SE101v = self.InfluxDB.InfluxDBreader(self.query_SE101)        
        self.SE101v = data_biogas["_value"]["SE101"]

        #get pump-102 flow from real biogas plant
        # self.query_SE102 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SE-102", location=1, type=1, forecastTime=1)
        # self.SE102v = self.InfluxDB.InfluxDBreader(self.query_SE102)        
        self.SE102v = data_biogas["_value"]["SE102"]

        #get methane concentration from real biogas plant reactor 1
        # self.query_AT103A1 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A1", location=1, type=1, forecastTime=1)
        # self.AT103A1v = self.InfluxDB.InfluxDBreader(self.query_AT103A1)
        self.AT103A1v = data_biogas["_value"]["AT103A1"]

        #Get Carbon dioxide Concentration from real biogas plant reactor 1    
        # self.query_AT103A2 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A2", location=1, type=1, forecastTime=1)
        # self.AT103A2v = self.InfluxDB.InfluxDBreader(self.query_AT103A2)
        self.AT103A2v = data_biogas["_value"]["AT103A2"]

        #Get hydrogen sulphide Concentration from real biogas plant reactor 1
        # self.query_AT103A3 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A3", location=1, type=1, forecastTime=1)
        # self.AT103A3v = self.InfluxDB.InfluxDBreader(self.query_AT103A3)
        self.AT103A3v = data_biogas["_value"]["AT103A3"]

        #Get Oxygen Concentration from real biogas plant reactor 1
        # self.query_AT103A4 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A4", location=1, type=1, forecastTime=1)
        # self.AT103A4v = self.InfluxDB.InfluxDBreader(self.query_AT103A4)
        self.AT103A4v = data_biogas["_value"]["AT103A4"]

        #Get Hydrogen H2 concentration from real biogas plant reactor 1
        # self.query_AT103A5 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103A5", location=1, type=1, forecastTime=1)
        # self.AT103A5v = self.InfluxDB.InfluxDBreader(self.query_AT103A5)
        self.AT103A5v = data_biogas["_value"]["AT103A5"]

        #Get Biogas relative Humidity from rela biogas plant reactor 1
        # self.query_AT103B = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-103B", location=1, type=1, forecastTime=1)
        # self.AT103Bv = self.InfluxDB.InfluxDBreader(self.query_AT103B)        
        self.AT103Bv = data_biogas["_value"]["AT103B"]

        #get pressure from V-101 in real biogas plant
        # self.query_PT103 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "PT-103", location=1, type=1, forecastTime=1)
        # self.PT103v = self.InfluxDB.InfluxDBreader(self.query_PT103)        
        self.PT103v = data_biogas["_value"]["PT103"]

        #get Temperature from V-101 in real biogas plant
        # self.query_TT103 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TT-103", location=1, type=1, forecastTime=1)
        # self.TT103v = self.InfluxDB.InfluxDBreader(self.query_TT103)
        self.TT103v = data_biogas["_value"]["TT103"]

        #get methane concentration from real biogas plant V-102
        # self.query_AT104A1 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A1", location=1, type=1, forecastTime=1)
        # self.AT104A1v = self.InfluxDB.InfluxDBreader(self.query_AT104A1)
        self.AT104A1v = data_biogas["_value"]["AT104A1"]

        #Get Carbon dioxide Concentration from real biogas plant V-102   
        # self.query_AT104A2 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A2", location=1, type=1, forecastTime=1)
        # self.AT104A2v = self.InfluxDB.InfluxDBreader(self.query_AT104A2)
        self.AT104A2v = data_biogas["_value"]["AT104A2"]

        #Get hydrogen sulphide Concentration from real biogas plant V-102
        # self.query_AT104A3 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A3", location=1, type=1, forecastTime=1)
        # self.AT104A3v = self.InfluxDB.InfluxDBreader(self.query_AT104A3)
        self.AT104A3v = data_biogas["_value"]["AT104A3"]

        #Get Oxygen Concentration from real biogas plant V-102
        # self.query_AT104A4 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A4", location=1, type=1, forecastTime=1)
        # self.AT104A4v = self.InfluxDB.InfluxDBreader(self.query_AT104A4)
        self.AT104A4v = data_biogas["_value"]["AT104A4"]

        #Get Hydrogen H2 concentration from real biogas plant V-102
        # self.query_AT104A5 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104A5", location=1, type=1, forecastTime=1)
        # self.AT104A5v = self.InfluxDB.InfluxDBreader(self.query_AT104A5)
        self.AT104A5v = data_biogas["_value"]["AT104A5"]

        #Get Biogas relative Humidity from real biogas plant V-102
        # self.query_AT104B = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-104B", location=1, type=1, forecastTime=1)
        # self.AT104Bv = self.InfluxDB.InfluxDBreader(self.query_AT104B)
        self.AT104Bv = data_biogas["_value"]["AT104B"]

        #Get Pressure from V-102 in real biogas plant
        # self.query_PT104 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "PT-104", location=1, type=1, forecastTime=1)
        # self.PT104v = self.InfluxDB.InfluxDBreader(self.query_PT104)
        self.PT104v = data_biogas["_value"]["PT104"]

        #Get Temperature from V-102 in real biogas plant
        # self.query_TT104 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TT-104", location=1, type=1, forecastTime=1)
        # self.TT104v = self.InfluxDB.InfluxDBreader(self.query_TT104)
        self.TT104v = data_biogas["_value"]["TT104"]

        #get methane concentration from real biogas plant V-107
        # self.query_AT105A1 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-105A1", location=1, type=1, forecastTime=1)
        # self.AT105A1v = self.InfluxDB.InfluxDBreader(self.query_AT105A1)
        self.AT105A1v = data_biogas["_value"]["AT105A1"]

        #Get Carbon dioxide Concentration from real biogas plant V-107   
        # self.query_AT105A2 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-105A2", location=1, type=1, forecastTime=1)
        # self.AT105A2v = self.InfluxDB.InfluxDBreader(self.query_AT105A2)
        self.AT105A2v = data_biogas["_value"]["AT105A2"]

        #Get hydrogen sulphide Concentration from real biogas plant V-107
        # self.query_AT105A3 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-105A3", location=1, type=1, forecastTime=1)
        # self.AT105A3v = self.InfluxDB.InfluxDBreader(self.query_AT105A3)
        self.AT105A3v = data_biogas["_value"]["AT105A3"]

        #Get Oxygen Concentration from real biogas plant V-107
        # self.query_AT105A4 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-105A4", location=1, type=1, forecastTime=1)
        # self.AT105A4v = self.InfluxDB.InfluxDBreader(self.query_AT105A4)
        self.AT105A4v = data_biogas["_value"]["AT105A4"]

        #Get Hydrogen H2 concentration from real biogas plant V-107
        # self.query_AT105A5 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-105A5", location=1, type=1, forecastTime=1)
        # self.AT105A5v = self.InfluxDB.InfluxDBreader(self.query_AT105A5)
        self.AT105A5v = data_biogas["_value"]["AT105A5"]

        #Get Biogas relative Humidity from real biogas plant V-102
        # self.query_AT105B = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "AT-105B", location=1, type=1, forecastTime=1)
        # self.AT105Bv = self.InfluxDB.InfluxDBreader(self.query_AT105B)
        self.AT105Bv = data_biogas["_value"]["AT105B"]

        #Get Pressure from V-107 in real biogas plant
        # self.query_PT105 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "PT-105", location=1, type=1, forecastTime=1)
        # self.PT105v = self.InfluxDB.InfluxDBreader(self.query_PT105)
        self.PT105v = data_biogas["_value"]["PT105"]

        #Get Temperature from V-107 in real biogas plant
        # self.query_TT105 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "TT-105", location=1, type=1, forecastTime=1)
        # self.TT105v = self.InfluxDB.InfluxDBreader(self.query_TT105)
        self.TT105v = data_biogas["_value"]["TT105"]

        #get valve V-101 state
        # self.query_SV103 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SV-103", location=1, type=1, forecastTime=1)
        # self.SV103v = self.InfluxDB.InfluxDBreader(self.query_SV103)
        self.SV103v = data_biogas["_value"]["SV103"]

        #get valve V-102 state
        # self.query_SV108 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SV-108", location=1, type=1, forecastTime=1)
        # self.SV108v = self.InfluxDB.InfluxDBreader(self.query_SV108)
        self.SV108v = data_biogas["_value"]["SV108"]

        #get valve V-107 state
        # self.query_SV109 = self.InfluxDB.QueryCreator(device="Planta Biogas", variable = "SV-109", location=1, type=1, forecastTime=1)
        # self.SV109v = self.InfluxDB.InfluxDBreader(self.query_SV109)
        self.SV109v = data_biogas["_value"]["SV109"]

    def Substrate_conditions (self,  Offline = True, manual_sustrate=True, ST=10.0, SV=1.0, Cc=40.48, Ch=5.29, Co=29.66, Cn=1.37, Cs=0.211, rho = 1000.0): 
        
        #Get from interface if entrances are manual or auto
        self.Offline = Offline
        self.manual_sustrate = manual_sustrate

        if self.Offline == True or self.manual_sustrate == True:
            
            self.ST = ST/100
            self.SV = SV/100
            self.Cc = Cc
            self.Ch = Ch
            self.Co = Co
            self.Cn = Cn
            self.Cs = Cs
            self.rho = rho 
        
        elif self.manual_sustrate == False:

            self.ST = self.ST["MST"].iloc[-1]/100
            self.SV = self.SV["MSV"].iloc[-1]/100
            self.Cc = self.Cc["MCc"].iloc[-1]
            self.Ch = self.Ch["MCh"].iloc[-1]
            self.Co = self.Co["MCo"].iloc[-1]
            self.Cn = self.Cn["MCn"].iloc[-1]
            self.Cs = self.Cs["MCs"].iloc[-1]
            self.rho = self.rho["Md"].iloc[-1]
        
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

    def Pump104_Operation_1_2 (self, manual_P104=True, TRH=30.0, FT_P104=5, TTO_P104=10):    
        self.manual_P104 = manual_P104
        
        if  self.Offline == True or self.manual_P104 == True:
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

            #testing model    
            print("Tiempo de encendido de la bomba P_104: "+str(self.TimeCounterPump_P104))
            print("Caudal de la bomba P_104: "+ str(self.Q_P104))
                   
        else:

            self.SE104v = self.SE104v["SE104"].tolist()
            self.Q_P104 = float(self.SE104v[-1])

    def Pump104_Operation_3_4_5 (self, manual_P104=0, TRH=30, FT_P104=5, TTO_P104=10):    
        self.manual_P104 = manual_P104
        
        if  self.Offline == False or self.manual_P104 == True:
            self.TRH = TRH
            self.FT_P104 = FT_P104
            self.TTO_P104 = TTO_P104
            
            self.TurnOnDailyStep_P104 = 24/self.FT_P104
        
            self.Q_daily = (self.VR1+self.VR2)/self.TRH
            self.Q_time = self.Q_daily/self.FT_P104

            if self.TimeCounterPump_P104<self.TTO_P104*60:
                self.Q_P104 = (self.Q_time/self.TTO_P104)*60
            
            else:
                self.Q_P104= float(0)
            
            self.TimeCounterPump_P104 = self.TimeCounterPump_P104 + self.tp

            if self.TimeCounterPump_P104>=self.TurnOnDailyStep_P104*3600:
                self.TimeCounterPump_P104 = 0

            #testing model    
            print("Tiempo de encendido de la bomba P_104: "+str(self.TimeCounterPump_P104))
            print("Caudal de la bomba P_104: "+ str(self.Q_P104))
        
        else:

            self.SE104v = self.SE104v["SE104"].tolist()
            self.Q_P104 = float(self.SE104v[-1])
    
    def Pump101_Operation_2 (self, manual_P101=0, FT_P101=5, TTO_P101=10, Q_P101 = 2.4):
        self.manual_P101 = manual_P101
        
        if self.manual_P101 == True or self.Offline == False:
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

        else:

            self.SE101v = self.SE101v["SE101"].tolist()
            self.Q_P101 = float(self.SE101v[-1])
    
    def Pump101_Operation_3_5 (self, manual_P101=0):
        self.manual_P101 = manual_P101
        
        if self.manual_P101 == True or self.Offline == False:
            self.Q_P101 = self.Q_P104

        else:

            self.SE101v = self.SE101v["SE101"].tolist()
            self.Q_P101 = float(self.SE101v[-1])
    
    def Pump101_Operation_4 (self, manual_P101=0):         #en este modo de operación primero se ejecuta la función de la bomba 102
        self.manual_P101 = manual_P101
        
        if self.manual_P101 == True or self.Offline == False:
            self.Q_P101 = self.Q_P104 + self.Q_P102

        else:

            self.SE101v = self.SE101v["SE101"].tolist()
            self.Q_P101 = float(self.SE101v[-1])
        
    def Pump102_Operation_4_5 (self, manual_P102=0, FT_P102=5, TTO_P102=10, Q_P102 = 2.4):
        self.manual_P102 = manual_P102

        if self.manual_P102 == True or self.Offline == False:
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

        else:

            self.SE102v = self.SE102v["SE102"].tolist()
            self.Q_P102 = float(self.SE102v)
    
           
    def Temperature_R101 (self, manual_temp_R101 = False, Temp_R101=35):
        self.manual_temp_R101 = manual_temp_R101

        if self.manual_temp_R101 == False or self.Offline == True:
            self.Temp_R101 = float(Temp_R101)

        elif self.manual_temp_R101 == True:

            self.TE_101Av = self.TE_101Av["TE101A"].tolist()
            self.TE_101Bv = self.TE_101Bv["TE101B"].tolist()

            T1 = float(self.TE_101Av[-1])
            T2 = float(self.TE_101Bv[-1])
            self.Temp_R101 = float((T1 + T2)/2)
    
    def Temperature_R102 (self, manual_temp_R102 = 1, Temp_R102=35):
        self.manual_temp_R102 = manual_temp_R102

        if self.manual_temp_R102 == False or self.Offline == False:
            self.Temp_R102 = float(Temp_R102)

        elif self.manual_temp_R102 == True:

            self.TE_102Av = self.TE_102Av["TE102A"].tolist()
            self.TE_102Bv = self.TE_102Bv["TE102B"].tolist()

            T1 = self.TE_102Av[-1]
            T2 = self.TE_102Bv[-1]
            self.Temp_R102 = (T1 + T2)/2
        
    def V_101_DT (self):
        self.AT103A1v = self.AT103A1v["AT103A1"]
        self.AT103A2v = self.AT103A2v["AT103A2"]
        self.AT103A3v = self.AT103A3v["AT103A3"]
        self.AT103A4v = self.AT103A4v["AT103A4"]
        self.AT103A5v = self.AT103A5v["AT103A5"]
                
        self.RH_V101v = self.AT103Bv["AT103B"]
        
        self.PT103v = self.PT103v["PT103"]
        self.TT103v = self.TT103v["TT103"]
        self.SV103v = self.SV103v["SV103"]

        self.P_std = 100        #[kPa]
        self.T_std = 273.15     #[K]    

        self.V_normal_V101 = ((self.PT103v.iloc[-1]*6.89476)*self.VG1*self.T_std)/(self.P_std*(self.TT103v.iloc[-1]+273.15))
        
        self.V_normal_CH4_V101 = self.AT103A1v.iloc[-1]/100*self.V_normal_V101
        
        self.V_normal_CO2_V101 = self.AT103A2v.iloc[-1]/100*self.V_normal_V101
       
        self.V_normal_H2S_V101 = self.AT103A3v.iloc[-1]/1000000*self.V_normal_V101
        
        self.V_normal_O2_V101 = self.AT103A4v.iloc[-1]/100*self.V_normal_V101
        
        self.V_normal_H2_V101 = self.AT103A5v.iloc[-1]/1000000*self.V_normal_V101
        
        self.V_mol_CH4 = self.Thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_CO2 = self.Thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_H2S = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_O2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]
        self.V_mol_H2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.PT103v.iloc[-1], Patm=100, T=self.TT103v.iloc[-1])[2]

        self.mol_CH4_V101 = self.V_normal_CH4_V101/self.V_mol_CH4     
        
        self.mol_CO2_V101 = self.V_normal_CO2_V101/self.V_mol_CO2
        
        self.mol_H2S_V101 = self.V_normal_H2S_V101/self.V_mol_H2S
        
        self.mol_O2_V101 = self.V_normal_O2_V101/self.V_mol_O2
        
        self.mol_H2_V101 = self.V_normal_H2_V101/self.V_mol_H2
        
        self.RH_V101 = self.RH_V101v.iloc[-1]/100
        self.AH_v101 = self.Thermo.BiogasAbsoluteHumidity(self.RH_V101, self.TT103v.iloc[-1])
        self.mol_H2O_V101 = self.AH_v101*self.V_normal_V101

        if (len (self.PT103v) > 1) and (self.PT103v.iloc[-1]*1.05 < self.PT103v.iloc[-2]):  #Cambiar cuando se conecte con la planta real
            self.P_ini_V101 = self.Pacum_V101
        
        self.Pacum_V101 = self.PT103v.iloc[-1] + self.P_ini_V101
       
        self.Vnormal_acum_V101 = ((self.Pacum_V101*6.89476)*self.VG1*self.T_std)/(self.P_std*(self.TT103v.iloc[-1]+273.15))
        
        self.V_normal_CH4_acum_V101 = self.AT103A1v.iloc[-1]/100*self.Vnormal_acum_V101
        self.mol_CH4_acum_V101 = self.V_normal_CH4_acum_V101/self.V_mol_CH4 

        self.V_normal_CO2_acum_V101 = self.AT103A2v.iloc[-1]/100*self.Vnormal_acum_V101
        self.mol_CO2_acum_V101 = self.V_normal_CO2_acum_V101/self.V_mol_CO2

        self.V_normal_H2S_acum_V101 = self.AT103A3v.iloc[-1]/1000000*self.Vnormal_acum_V101
        self.mol_H2S_acum_V101 = self.V_normal_H2S_acum_V101/self.V_mol_H2S

        self.V_normal_O2_acum_V101 = self.AT103A4v.iloc[-1]/100*self.Vnormal_acum_V101
        self.mol_O2_acum_V101 = self.V_normal_O2_acum_V101/self.V_mol_O2

        self.V_normal_H2_acum_V101 = self.AT103A5v.iloc[-1]/1000000*self.Vnormal_acum_V101
        self.mol_H2_acum_V101 = self.V_normal_H2_acum_V101/self.V_mol_H2

    def V_102_DT (self):
        self.AT104A1v = self.AT104A1v["AT104A1"]
        self.AT104A2v = self.AT104A2v["AT104A2"]
        self.AT104A3v = self.AT104A3v["AT104A3"]
        self.AT104A4v = self.AT104A4v["AT104A4"]
        self.AT104A5v = self.AT104A5v["AT104A5"]

        self.RH_V102v = self.AT104Bv["AT104B"]

        self.PT104v = self.PT104v["PT104"]
        self.TT104v = self.TT104v["TT104"]
        #self.SV104v = self.SV104v["SV-104"]

        self.V_normal_V102 = ((self.PT104v.iloc[-1]*6.89476)*self.VG2*self.T_std)/(self.P_std*(self.TT104v.iloc[-1]+273.15))
        
        self.V_normal_CH4_V102 = self.AT104A1v.iloc[-1]/100*self.V_normal_V102
        
        self.V_normal_CO2_V102 = self.AT104A2v.iloc[-1]/100*self.V_normal_V102
        
        self.V_normal_H2S_V102 = self.AT104A3v.iloc[-1]/1000000*self.V_normal_V102
        
        self.V_normal_O2_V102 = self.AT104A4v.iloc[-1]/100*self.V_normal_V102
        
        self.V_normal_H2_V102 = self.AT103A5v.iloc[-1]/1000000*self.V_normal_V102
        
        self.mol_CH4_V102 = self.V_normal_CH4_V102/self.V_mol_CH4     
        
        self.mol_CO2_V102 = self.V_normal_CO2_V102/self.V_mol_CO2
        
        self.mol_H2S_V102 = self.V_normal_H2S_V102/self.V_mol_H2S
        
        self.mol_O2_V102 = self.V_normal_O2_V102/self.V_mol_O2
        
        self.mol_H2_V102 = self.V_normal_H2_V102/self.V_mol_H2
        
        self.RH_V102 = self.RH_V102v.iloc[-1]/100
        self.AH_v102 = self.Thermo.BiogasAbsoluteHumidity(self.RH_V102, self.TT104v.iloc[-1])
        self.mol_H2O_V102 = self.AH_v102*self.V_normal_V102
        
        if (len (self.PT104v) > 1) and (self.PT104v.iloc[-1]*1.05 < self.PT104v.iloc[-2]):  #Cambiar cuando se conecte con la planta real
            self.P_ini_V102 = self.Pacum_V102
        
        self.Pacum_V102 = self.PT104v.iloc[-1] + self.P_ini_V102
        
        self.Vnormal_acum_V102 = ((self.Pacum_V102*6.89476)*self.VG2*self.T_std)/(self.P_std*(self.TT104v.iloc[-1]+273.15))
        
        self.V_normal_CH4_acum_V102 = self.AT104A1v.iloc[-1]/100*self.Vnormal_acum_V102
        self.mol_CH4_acum_V102 = self.V_normal_CH4_acum_V102/self.V_mol_CH4     

        self.V_normal_CO2_acum_V102 = self.AT104A2v.iloc[-1]/100*self.Vnormal_acum_V102
        self.mol_CO2_acum_V102 = self.V_normal_CO2_acum_V102/self.V_mol_CO2

        self.V_normal_H2S_acum_V102 = self.AT104A3v.iloc[-1]/1000000*self.Vnormal_acum_V102
        self.mol_H2S_acum_V102 = self.V_normal_H2S_acum_V102/self.V_mol_H2S

        self.V_normal_O2_acum_V102 = self.AT104A4v.iloc[-1]/100*self.Vnormal_acum_V102
        self.mol_O2_acum_V102 = self.V_normal_O2_acum_V102/self.V_mol_O2

        self.V_normal_H2_acum_V102 = self.AT104A5v.iloc[-1]/1000000*self.Vnormal_acum_V102
        self.mol_H2_acum_V102 = self.V_normal_H2_acum_V102/self.V_mol_H2
        
        
    def V_107_DT (self):
        self.AT105A1v = self.AT105A1v["AT105A1"]
        self.AT105A2v = self.AT105A2v["AT105A2"]
        self.AT105A3v = self.AT105A3v["AT105A3"]
        self.AT105A4v = self.AT105A4v["AT105A4"]
        self.AT105A5v = self.AT105A5v["AT105A5"]

        self.RH_V107v = self.AT105Bv["AT105B"]

        self.PT105v = self.PT105v["PT105"]
        self.TT105v = self.TT105v["TT105"]

        self.V_normal_V107 = ((self.PT105v.iloc[-1]*6.89476)*self.VG3*self.T_std)/(self.P_std*(self.TT105v.iloc[-1]+273.15))
        
        self.V_normal_CH4_V107 = self.AT105A1v.iloc[-1]/100*self.V_normal_V107
       
        self.V_normal_CO2_V107 = self.AT105A2v.iloc[-1]/100*self.V_normal_V107
        
        self.V_normal_H2S_V107 = self.AT105A3v.iloc[-1]/1000000*self.V_normal_V107
        
        self.V_normal_O2_V107 = self.AT105A4v.iloc[-1]/100*self.V_normal_V107
        
        self.V_normal_H2_V107 = self.AT105A5v.iloc[-1]/1000000*self.V_normal_V107
       
        self.mol_CH4_V107 = self.V_normal_CH4_V107/self.V_mol_CH4     
        
        self.mol_CO2_V107 = self.V_normal_CO2_V107/self.V_mol_CO2
        
        self.mol_H2S_V107 = self.V_normal_H2S_V107/self.V_mol_H2S
        
        self.mol_O2_V107 = self.V_normal_O2_V107/self.V_mol_O2
        
        self.mol_H2_V107 = self.V_normal_H2_V107/self.V_mol_H2
        
        self.RH_V107 = self.RH_V107v.iloc[-1]/100
        self.AH_v107 = self.Thermo.BiogasAbsoluteHumidity(self.RH_V107, self.TT105v.iloc[-1])
        self.mol_H2O_V107 = self.AH_v107*self.V_normal_V107
        
        if (len (self.PT105v) > 1) and (self.PT105v.iloc[-1]*1.05 < self.PT105v.iloc[-2]):  #Cambiar cuando se conecte con la planta real
            self.P_ini_V107 = self.Pacum_V107
        
        self.Pacum_V107 = self.PT105v.iloc[-1] + self.P_ini_V107
        
        self.Vnormal_acum_V107 = ((self.Pacum_V107*6.89476)*self.VG3*self.T_std)/(self.P_std*(self.TT105v.iloc[-1]+273.15))
       
        self.V_normal_CH4_acum_V107 = self.AT105A1v.iloc[-1]/100*self.Vnormal_acum_V107
        self.mol_CH4_acum_V107 = self.V_normal_CH4_acum_V107/self.V_mol_CH4 

        self.V_normal_CO2_acum_V107 = self.AT104A2v.iloc[-1]/100*self.Vnormal_acum_V107
        self.mol_CO2_acum_V107 = self.V_normal_CO2_acum_V107/self.V_mol_CO2

        self.V_normal_H2S_acum_V107 = self.AT104A3v.iloc[-1]/1000000*self.Vnormal_acum_V107
        self.mol_H2S_acum_V107 = self.V_normal_H2S_acum_V107/self.V_mol_H2S

        self.V_normal_O2_acum_V107 = self.AT104A4v.iloc[-1]/100*self.Vnormal_acum_V107
        self.mol_O2_acum_V107 = self.V_normal_O2_acum_V107/self.V_mol_O2

        self.V_normal_H2_acum_V107 = self.AT104A5v.iloc[-1]/1000000*self.Vnormal_acum_V107
        self.mol_H2_acum_V107 = self.V_normal_H2_acum_V107/self.V_mol_H2    
        
    def R101_DT_operation_1 (self):      
        self.mol_CH4_R101v = self.DT_Data["mol_CH4_acum_V101"].tolist()

        if len(self.mol_CH4_R101v)>=2:
            self.mol_CH4_R101 = self.mol_CH4_R101v[-1]
            self.mol_CH4_R101_i = self.mol_CH4_R101v[-2]

            if self.mol_CH4_R101 < self.mol_CH4_R101_i:
                self.mol_sus_stoichometricFR_R101 = 0
                self.volatilemass_stoichometricFR_R101 = 0
                self.TotalSolids_stoichometricFR_R101 = 0
            else:
                self.mol_sus_stoichometricFR_R101 =  (1/self.s_CH4)*(self.mol_CH4_R101 - self.mol_CH4_R101_i)
                self.volatilemass_stoichometricFR_R101 = self.mol_sus_stoichometricFR_R101*self.MW_sustrato
                self.TotalSolids_stoichometricFR_R101 = self.mol_sus_stoichometricFR_R101*self.MW_sustrato

            self.mol_sus_int_ini_R101 = self.Csus_ini_R101*self.VR1
            self.mol_sus_in_R101 = self.Q_P104*self.Csus_ini*(self.tp/3600)
            
            self.Csus_ini_R101 = (self.mol_sus_int_ini_R101 + self.mol_sus_in_R101 - self.mol_sus_stoichometricFR_R101)/(self.VR1+(self.Q_P104*(self.tp/3600)))

            self.volatilemass_int_ini_R101 = self.SV_R101*self.rho_R101*self.VR1
            self.volatilemass_in_R101 = self.Q_P104*self.SV*self.rho*(self.tp/3600)

            self.SV_R101 = ((self.volatilemass_int_ini_R101 + self.volatilemass_in_R101 - self.volatilemass_stoichometricFR_R101)/(self.VR1 + (self.Q_P104*(self.tp/3600))))/self.rho

            self.TotalSolids_int_ini_R101 = self.ST_R101*self.rho_R101*self.VR1
            self.TotalSolids_in_R101 = self.Q_P104*self.ST*self.rho*(self.tp/3600)

            self.ST_R101 = ((self.TotalSolids_int_ini_R101 + self.TotalSolids_in_R101 - self.TotalSolids_stoichometricFR_R101)/(self.VR1+(self.Q_P104*(self.tp/3600))))/self.rho
        
        else:

            self.mol_sus_int_ini_R101 = self.Csus_ini_R101*self.VR1
            return ("Data is required to continue, please wait...")
    
    def R101_DT_Operation_2 (self):
        self.mol_CH4_R101v = self.DT_Data["mol_CH4_acum_V101"].tolist()

        if len(self.mol_CH4_R101v)>=2:
            self.mol_CH4_R101 = self.mol_CH4_R101v[-1]
            self.mol_CH4_R101_i = self.mol_CH4_R101v[-2]

            if self.mol_CH4_R101 < self.mol_CH4_R101_i:
                self.mol_sus_stoichometricFR_R101 = 0
                self.volatilemass_stoichometricFR_R101 = 0
                self.TotalSolids_stoichometricFR_R101 = 0
            else:
                self.mol_sus_stoichometricFR_R101 =  (1/self.s_CH4)*(self.mol_CH4_R101 - self.mol_CH4_R101_i)
                self.volatilemass_stoichometricFR_R101 = self.mol_sus_stoichometricFR_R101*self.MW_sustrato
                self.TotalSolids_stoichometricFR_R101 = self.mol_sus_stoichometricFR_R101*self.MW_sustrato
            
            self.mol_sus_int_ini_R101 = self.Csus_ini_R101*self.VR1
            self.mol_sus_in_R101 = self.Q_P104*self.Csus_ini*(self.tp/3600)

            self.Csus_ini_R101 = (self.mol_sus_int_ini_R101 + self.mol_sus_in_R101 - self.mol_sus_stoichometricFR_R101)/(self.VR1 - self.SE101v[-1]*(self.tp/3600) + (self.Q_P104+self.SE101v[-1])*(self.tp/3600))

            self.volatilemass_int_ini_R101 = self.SV_R101*self.rho_R101*self.VR1
            self.volatilemass_in_R101 = self.Q_P104*self.SV*self.rho*(self.tp/3600)

            self.SV_R101 = ((self.volatilemass_int_ini_R101 + self.volatilemass_in_R101 - self.volatilemass_stoichometricFR_R101)/(self.VR1 - self.SE101v[-1]*(self.tp/3600) + (self.Q_P104+self.SE101v[-1])*(self.tp/3600)))/self.rho

            self.TotalSolids_int_ini_R101 = self.ST_R101*self.rho_R101*self.VR1
            self.TotalSolids_in_R101 = self.Q_P104*self.ST*(self.tp/3600)

            self.ST_R101 = ((self.TotalSolids_int_ini_R101 + self.TotalSolids_in_R101 - self.TotalSolids_stoichometricFR_R101)/(self.VR1 - self.SE101v[-1]*(self.tp/3600) + (self.Q_P104+self.SE101v[-1])*(self.tp/3600)))/self.rho
        else:

            self.mol_sus_int_ini_R101 = self.Csus_ini_R101*self.VR1
            return ("Data is required to continue, please wait...")

    def R101_DT_operation_3_5 (self):      
        self.mol_CH4_R101v = self.DT_Data["mol_CH4_acum_V101"].tolist()

        if len(self.mol_CH4_R101v)>=2:
            self.mol_CH4_R101 = self.mol_CH4_R101v[-1]
            self.mol_CH4_R101_i = self.mol_CH4_R101v[-2]

            if self.mol_CH4_R101 < self.mol_CH4_R101_i:
                self.mol_sus_stoichometricFR_R101 = 0
                self.volatilemass_stoichometricFR_R101 = 0
                self.TotalSolids_stoichometricFR_R101 = 0
            else:
                self.mol_sus_stoichometricFR_R101 =  (1/self.s_CH4)*(self.mol_CH4_R101 - self.mol_CH4_R101_i)
                self.volatilemass_stoichometricFR_R101 = self.mol_sus_stoichometricFR_R101*self.MW_sustrato
                self.TotalSolids_stoichometricFR_R101 = self.mol_sus_stoichometricFR_R101*self.MW_sustrato

            self.mol_sus_int_ini_R101 = self.Csus_ini_R101*self.VR1
            self.mol_sus_in_R101 = self.Q_P104*self.Csus_ini*(self.tp/3600)
           
            self.Csus_ini_R101 = (self.mol_sus_int_ini_R101 + self.mol_sus_in_R101 - self.mol_sus_stoichometricFR_R101)/(self.VR1+(self.SE101v[-1]*(self.tp/3600)))

            self.volatilemass_int_ini_R101 = self.SV_R101*self.rho_R101*self.VR1
            self.volatilemass_in_R101 = self.Q_P104*self.SV*self.rho*(self.tp/3600)

            self.SV_R101 = ((self.volatilemass_int_ini_R101 + self.volatilemass_in_R101 - self.volatilemass_stoichometricFR_R101)/(self.VR1 + (self.SE101v[-1]*(self.tp/3600))))/self.rho

            self.TotalSolids_int_ini_R101 = self.ST_R101*self.rho_R101*self.VR1
            self.TotalSolids_in_R101 = self.Q_P104*self.ST*(self.tp/3600)

            self.ST_R101 = ((self.TotalSolids_int_ini_R101 + self.TotalSolids_in_R101 - self.TotalSolids_stoichometricFR_R101)/(self.VR1+(self.SE101v[-1]*(self.tp/3600))))/self.rho
        
        else:
            self.mol_sus_int_ini_R101 = self.Csus_ini_R101*self.VR1
            return ("Data is required to continue, please wait...")
    
    def R101_DT_Operation_4 (self):
        self.mol_CH4_R101v = self.DT_Data["mol_CH4_acum_V101"].tolist()

        if len(self.mol_CH4_R101v)>=2:
            self.mol_CH4_R101 = self.mol_CH4_R101v[-1]
            self.mol_CH4_R101_i = self.mol_CH4_R101v[-2]

            if self.mol_CH4_R101 < self.mol_CH4_R101_i:
                self.mol_sus_stoichometricFR_R101 = 0
                self.volatilemass_stoichometricFR_R101 = 0
                self.TotalSolids_stoichometricFR_R101 = 0
            else:
                self.mol_sus_stoichometricFR_R101 =  (1/self.s_CH4)*(self.mol_CH4_R101 - self.mol_CH4_R101_i)
                self.volatilemass_stoichometricFR_R101 = self.mol_sus_stoichometricFR_R101*self.MW_sustrato
                self.TotalSolids_stoichometricFR_R101 = self.mol_sus_stoichometricFR_R101*self.MW_sustrato
            
            self.mol_sus_int_ini_R101 = self.Csus_ini_R101*self.VR1
            self.mol_sus_in_R101_1 = self.Q_P104*self.Csus_ini*(self.tp/3600)
            self.mol_sus_in_R101_2 = self.SE102v[-1]*self.Csus_ini_R102*(self.tp/3600)

            self.Csus_ini_R101 = (self.mol_sus_int_ini_R101 + self.mol_sus_in_R101_1 + self.mol_sus_in_R101_2 - self.mol_sus_stoichometricFR_R101)/(self.VR1 + (self.SE101v[-1])*self.tp) 

            self.volatilemass_int_ini_R101 = self.SV_R101*self.rho_R101*self.VR1
            self.volatilemass_in_R101_1 = self.Q_P104*self.SV*self.rho*(self.tp/3600)
            self.volatilemass_in_R101_2 = self.SE102v[-1]*self.SV_R102*self.rho*(self.tp/3600)

            self.SV_R101 = ((self.volatilemass_int_ini_R101 + self.volatilemass_in_R101_1 + self.volatilemass_in_R101_2 - self.volatilemass_stoichometricFR_R101)/(self.VR1 + (self.SE101v[-1])*(self.tp/3600)))/self.rho

            self.TotalSolids_int_ini_R101 = self.ST_R101*self.rho_R101*self.VR1
            self.TotalSolids_in_R101_1 = self.Q_P104*self.ST*(self.tp/3600)
            self.TotalSolids_in_R101_2 = self.SE102v[-1]*self.ST_R102*(self.tp/3600)

            self.ST_R101 = (self.TotalSolids_int_ini_R101 + self.TotalSolids_in_R101_1 + self.TotalSolids_in_R101_2 - self.TotalSolids_stoichometricFR_R101)/(self.VR1 + (self.SE101v[-1])*(self.tp/3600))/self.rho


        else:

            self.mol_sus_int_ini_R101 = self.Csus_ini_R101*self.VR1

            return ("Data is required to continue, please wait...")
            

        
    def R102_DT_Operation_3 (self):
        
        self.mol_CH4_R102v = self.DT_Data["mol_CH4_acum_V102"] .tolist()

        if len(self.mol_CH4_R101v)>=2:
            self.mol_CH4_R102 = self.mol_CH4_R102v[-1]
            self.mol_CH4_R102_i = self.mol_CH4_R102v[-2]

            #El biogas de ambos tanques pasa por V-102
            if self.Pacum_V101 < 50:                                           #Este valor es el valor de presión máximo que puede almacenar V-101
                self.mol_CH4_R102 = self.mol_CH4_R102
                self.mol_CH4_R102_i = self.mol_CH4_R102_i
            else:
                self.mol_CH4_R102 = self.mol_CH4_R102 - self.mol_CH4_R101
                self.mol_CH4_R102_i = self.mol_CH4_R102_i - self.mol_CH4_R101_i
            
            if self.mol_CH4_R102 < self.mol_CH4_R102_i:
                self.mol_sus_stoichometricFR_R102 = 0
                self.volatilemass_stoichometricFR_R102 = 0
                self.TotalSolids_stoichometricFR_R102 = 0
            
            else:
                self.mol_sus_stoichometricFR_R102 =  (1/self.s_CH4)*(self.mol_CH4_R102 - self.mol_CH4_R102_i)
                self.volatilemass_stoichometricFR_R102 = self.mol_sus_stoichometricFR_R102*self.MW_sustrato
                self.TotalSolids_stoichometricFR_R102 = self.mol_sus_stoichometricFR_R102*self.MW_sustrato
            
            self.mol_sus_int_ini_R102 = self.Csus_ini_R102*self.VR2
            self.mol_sus_in_R102 = self.SE101v[-1]*self.Csus_ini_R101*(self.tp/3600)

            self.Csus_ini_R102 = (self.mol_sus_int_ini_R102 + self.mol_sus_in_R102 - self.mol_sus_stoichometricFR_R102)/(self.VR2+(self.SE101v[-1]*(self.tp/3600)))

            self.volatilemass_int_ini_R102 = self.SV_R102*self.rho_R102*self.VR2
            self.volatilemass_in_R102 = self.SE101v[-1]*self.SV_R101*self.rho*(self.tp/3600)

            self.SV_R102 = ((self.volatilemass_int_ini_R102 + self.volatilemass_in_R102 - self.volatilemass_stoichometricFR_R102)/(self.VR2+(self.SE101v[-1]*(self.tp/3600))))/self.rho

            self.TotalSolids_int_ini_R102 = self.ST_R102*self.rho_R102*self.VR2
            self.TotalSolids_in_R102 = self.SE101v[-1]*self.ST_R101*(self.tp/3600)

            self.ST_R102 = ((self.TotalSolids_int_ini_R102 + self.TotalSolids_in_R102 - self.TotalSolids_stoichometricFR_R102)/(self.VR2+(self.SE101v[-1]*(self.tp/3600))))/self.rho           

        else:
            return ("Data is required to continue, please wait...")
    
    def R102_DT_Operation_4 (self):
        self.query_mol_CH4_R102 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "M-molT_CH4_V102", location=1, type=1, forecastTime=1)
        self.mol_CH4_R102v = self.InfluxDB.InfluxDBreader(self.query_mol_CH4_R102)
        self.mol_CH4_R102v = self.mol_CH4_R102v["M-molT_CH4_V102"].tolist()

        if len(self.mol_CH4_R101v)>=2:
            self.mol_CH4_R102 = self.mol_CH4_R102v[-1]
            self.mol_CH4_R102_i = self.mol_CH4_R102v[-2]

            #El biogas de ambos tanques pasa por V-102
            if self.Pacum_V101 < 50:                                           #Este valor es el valor de presión máximo que puede almacenar V-101
                self.mol_CH4_R102 = self.mol_CH4_R102
                self.mol_CH4_R102_i = self.mol_CH4_R102_i
            else:
                self.mol_CH4_R102 = self.mol_CH4_R102 - self.mol_CH4_R101
                self.mol_CH4_R102_i = self.mol_CH4_R102_i - self.mol_CH4_R101_i
            
            if self.mol_CH4_R102 < self.mol_CH4_R102_i:
                self.mol_sus_stoichometricFR_R102 = 0
                self.volatilemass_stoichometricFR_R102 = 0
                self.TotalSolids_stoichometricFR_R102 = 0
            
            else:
                self.mol_sus_stoichometricFR_R102 =  (1/self.s_CH4)*(self.mol_CH4_R102 - self.mol_CH4_R102_i)
                self.volatilemass_stoichometricFR_R102 = self.mol_sus_stoichometricFR_R102*self.MW_sustrato
                self.TotalSolids_stoichometricFR_R102 = self.mol_sus_stoichometricFR_R102*self.MW_sustrato
            
            self.mol_sus_int_ini_R102 = self.Csus_ini_R102*self.VR2
            self.mol_sus_in_R102 = self.SE101v[-1]*self.Csus_ini_R101*(self.tp/3600)

            self.Csus_ini_R102 = (self.mol_sus_int_ini_R102 + self.mol_sus_in_R102 - self.mol_sus_stoichometricFR_R102)/(self.VR2+((self.SE102v[-1]+self.Q_P104)*(self.tp/3600)))

            self.volatilemass_int_ini_R102 = self.SV_R102*self.rho_R102*self.VR2
            self.volatilemass_in_R102 = self.SE101v[-1]*self.SV_R101*self.rho*(self.tp/3600)

            self.SV_R102 = ((self.volatilemass_int_ini_R102 + self.volatilemass_in_R102 - self.volatilemass_stoichometricFR_R102)/(self.VR2+((self.SE102v[-1]+self.Q_P104)*(self.tp/3600))))/self.rho

            self.TotalSolids_int_ini_R102 = self.ST_R102*self.rho_R102*self.VR2
            self.TotalSolids_in_R102 = self.SE101v[-1]*self.ST_R101*(self.tp/3600)

            self.ST_R102 = ((self.TotalSolids_int_ini_R102 + self.TotalSolids_in_R102 - self.TotalSolids_stoichometricFR_R102)/(self.VR2+((self.SE102v[-1]+self.Q_P104)*(self.tp/3600))))/self.rho 

    def R102_DT_Operation_5(self):
        self.query_mol_CH4_R102 = self.InfluxDB.QueryCreator(device="DTPlantaBiogas", variable = "M-molT_CH4_V102", location=1, type=1, forecastTime=1)
        self.mol_CH4_R102v = self.InfluxDB.InfluxDBreader(self.query_mol_CH4_R102)
        self.mol_CH4_R102v = self.mol_CH4_R102v["M-molT_CH4_V102"].tolist()

        if len(self.mol_CH4_R101v)>=2:
            self.mol_CH4_R102 = self.mol_CH4_R102v[-1]
            self.mol_CH4_R102_i = self.mol_CH4_R102v[-2]

            #El biogas de ambos tanques pasa por V-102
            if self.Pacum_V101 < 50:                                           #Este valor es el valor de presión máximo que puede almacenar V-101
                self.mol_CH4_R102 = self.mol_CH4_R102
                self.mol_CH4_R102_i = self.mol_CH4_R102_i
            else:
                self.mol_CH4_R102 = self.mol_CH4_R102 - self.mol_CH4_R101
                self.mol_CH4_R102_i = self.mol_CH4_R102_i - self.mol_CH4_R101_i
            
            if self.mol_CH4_R102 < self.mol_CH4_R102_i:
                self.mol_sus_stoichometricFR_R102 = 0
                self.volatilemass_stoichometricFR_R102 = 0
                self.TotalSolids_stoichometricFR_R102 = 0
            
            else:
                self.mol_sus_stoichometricFR_R102 =  (1/self.s_CH4)*(self.mol_CH4_R102 - self.mol_CH4_R102_i)
                self.volatilemass_stoichometricFR_R102 = self.mol_sus_stoichometricFR_R102*self.MW_sustrato
                self.TotalSolids_stoichometricFR_R102 = self.mol_sus_stoichometricFR_R102*self.MW_sustrato
            
            self.mol_sus_int_ini_R102 = self.Csus_ini_R102*self.VR2
            self.mol_sus_in_R102 = self.SE101v[-1]*self.Csus_ini_R101*(self.tp/3600)

            self.Csus_ini_R102 = (self.mol_sus_int_ini_R102 + self.mol_sus_in_R102 - self.mol_sus_stoichometricFR_R102)/(self.VR2+((self.SE102v[-1]+(self.Q_P104-self.SE102v[-1]))*(self.tp/3600)))

            self.volatilemass_int_ini_R102 = self.SV_R102*self.rho_R102*self.VR2
            self.volatilemass_in_R102 = self.SE101v[-1]*self.SV_R101*self.rho*(self.tp/3600)

            self.SV_R102 = ((self.volatilemass_int_ini_R102 + self.volatilemass_in_R102 - self.volatilemass_stoichometricFR_R102)/(self.VR2+((self.SE102v[-1]+(self.Q_P104-self.SE102v[-1]))*(self.tp/3600))))/self.rho

            self.TotalSolids_int_ini_R102 = self.ST_R102*self.rho_R102*self.VR2
            self.TotalSolids_in_R102 = self.SE101v[-1]*self.ST_R101*(self.tp/3600)

            self.ST_R102 = ((self.TotalSolids_int_ini_R102 + self.TotalSolids_in_R102 - self.TotalSolids_stoichometricFR_R102)/(self.VR2+((self.SE102v[-1]+(self.Q_P104-self.SE102v[-1]))*(self.tp/3600))))/self.rho

    def Energy_Biogas (self): 
        self.LHV_V101 = self.Thermo.LHV(molCH4 = self.mol_CH4_V101, molCO2 = self.mol_CO2_V101, molH2S = self.mol_H2S_V101, molO2 = self.mol_O2_V101, molH2 = self.mol_H2_V101)
        self.Energy_V101 = self.LHV_V101[1]

        self.LHV_V102 = self.Thermo.LHV(molCH4 = self.mol_CH4_V102, molCO2 = self.mol_CO2_V102, molH2S = self.mol_H2S_V102, molO2 = self.mol_O2_V102, molH2 = self.mol_H2_V102)
        self.Energy_V102 = self.LHV_V102[1]

        self.LHV_V107 = self.Thermo.LHV(molCH4 = self.mol_CH4_V107, molCO2 = self.mol_CO2_V107, molH2S = self.mol_H2S_V107, molO2 = self.mol_O2_V107, molH2 = self.mol_H2_V107)
        self.Energy_V107 = self.LHV_V107[1]
    
    def StorageData (self):
        self.timestamp = datetime.now()
        if self.OperationMode == 1:
            new_row = pd.DataFrame({"timestamp": [self.timestamp],
                                    "Q_P104" : [self.Q_P104],
                                    "Temp_R101": [self.Temp_R101],
                                    "V_normal_V101": [self.V_normal_V101],
                                    "V_normal_CH4_V101": [self.V_normal_CH4_V101],
                                    "V_normal_CO2_V101":[self.V_normal_CO2_V101],
                                    "V_normal_H2S_V101":[self.V_normal_H2S_V101],
                                    "V_normal_O2_V101":[self.V_normal_H2S_V101],
                                    "V_normal_H2_V101":[self.V_normal_H2_V101],
                                    "mol_CH4_V101": [self.mol_CH4_V101],
                                    "mol_CO2_V101":[self.mol_CO2_V101],
                                    "mol_H2S_V101":[self.mol_H2S_V101],
                                    "mol_O2_V101":[self.mol_O2_V101],
                                    "mol_H2_V101":[self.mol_H2_V101],
                                    "mol_H2O_V101":[self.mol_H2O_V101],
                                    "Pacum_V101":[self.Pacum_V101],
                                    "Vnormal_acum_V101":[self.Vnormal_acum_V101],
                                    "mol_CH4_acum_V101":[self.mol_CH4_acum_V101],
                                    "mol_sus_int_ini_R101":[self.mol_sus_int_ini_R101],
                                    "Csus_ini_R101":[self.Csus_ini_R101],
                                    "SV_R101":[self.SV_R101],
                                    "ST_R101":[self.ST_R101]
                                    })
            self.DT_Data = pd.concat([self.DT_Data, new_row], ignore_index=True)




        


        


        
