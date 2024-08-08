import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
current_directory = os.getcwd()
print(current_directory)
excel_file_path = os.path.join(os.path.abspath(os.path.join(current_directory)), "v1.0", "tools", "DB_Mapping.xlsx")
#excel_file_path = r"C:\Users\Sergio\OneDrive - UCO\Documents\GitHub\backend\v1.0\tools\DB_Mapping.xlsx"
print(excel_file_path)

import pandas as pd
from datetime import datetime
from simulation_models.Biogas import ThermoProperties as TP
from  tools import DBManager
from fractions import Fraction
from math import gcd
from functools import reduce


class BiogasPlantDT:

    def __init__(self, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, 
                 ST_R101=10, SV_R101=1, Cc_R101=40.48, Ch_R101=5.29, Co_R101=29.66, Cn_R101=1.37, Cs_R101=0.211, rho_R101=1000,
                 ST_R102=10, SV_R102=1, Cc_R102=40.48, Ch_R102=5.29, Co_R102=29.66, Cn_R102=1.37, Cs_R102=0.211, rho_R102=1000, OperationModo="Modo1"):

        #Interface Inputs
        self.VR1 = VR1
        self.VR2 = VR2
        self.VG1 = VG1
        self.VG2 = VG2
        self.VG3 = VG3
        self.databaseConnection_df = pd.read_excel(excel_file_path, sheet_name='ConexionDB')
        self.database_df = pd.read_excel(excel_file_path, sheet_name='InfluxDBVariables')
        index = 3
        self.InfluxDB = DBManager.InfluxDBmodel(server = 'http://' + str(self.databaseConnection_df['IP'][index])+':'+str(self.databaseConnection_df['Port'][index])+'/', org = self.databaseConnection_df['Organization'][index], bucket = self.databaseConnection_df['Bucket'][index], token = self.databaseConnection_df['Token'][index])
        self.Thermo = TP.ThermoProperties()
        self.tp = tp
        #Initial values
        #Global time
        self.GlobalTime = 0
        #Pumps
        self.TimeCounterPump_P104 = 0
        self.TimeCounterPump_P101 = 0
        self.TimeCounterPump_P102 = 0
        #mixers
        self.TimeCounterMixer_TK100 = 0
        self.TimeCounterMixer_R101 = 0
        self.TimeCounterMixer_R102 = 0
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
        self.ST_R101 = ST_R101
        self.SV_R101 = SV_R101
        self.Cc_R101 = Cc_R101
        self.Ch_R101 = Ch_R101
        self.Co_R101 = Co_R101
        self.Cn_R101 = Cn_R101
        self.Cs_R101 = Cs_R101
        self.rho_R101 = rho_R101
        if self.ST_R101 == 0:
            self.Csus_ini_R101 = 0
            self.Csus_ini_ST_R101 = 0
        else:
            self.molC_R101 = self.Cc_R101*(1/12.01)
            self.molH_R101 = self.Ch_R101*(1/1.01)
            self.molO_R101 = self.Co_R101*(1/16)
            self.molN_R101 = self.Cn_R101*(1/14)
            self.molS_R101 = self.Cs_R101*(1/32)

            n_R101 = self.molC_R101
            a_R101 = self.molH_R101
            b_R101 = self.molO_R101
            c_R101 = self.molN_R101
            d_R101 = self.molS_R101

            def lcm(a,b):
                return a * b // gcd(a, b)

            numbers_R101 = [n_R101, a_R101, b_R101, c_R101, d_R101]
            denominators_R101 = [Fraction(num).limit_denominator(10).denominator for num in numbers_R101]
            common_denominator_R101 = reduce(lcm, denominators_R101)
            subindex_R101 = [int(num * common_denominator_R101) for num in numbers_R101]

            self.n_R101 = subindex_R101[0]
            self.a_R101 = subindex_R101[1]
            self.b_R101 = subindex_R101[2]
            self.c_R101 = subindex_R101[3]
            self.d_R101 = subindex_R101[4]
            
            self.s_H2O_R101 = self.n_R101-(self.a_R101/4)-(self.b_R101/2)+(3/4)*self.c_R101+(self.d_R101/2)
            self.s_CH4_R101 = (self.n_R101/2)+(self.a_R101/8)-(self.b_R101/4)-(3/8)*self.c_R101-(self.d_R101/4)
            self.s_CO2_R101 = (self.n_R101/2)-(self.a_R101/8)+(self.b_R101/4)+(3/8)*self.c_R101-(self.d_R101/4)
            self.s_NH3_R101 = self.c_R101
            self.s_H2S_R101 = self.d_R101
            
            self.MW_sustrato_R101 = self.n_R101*12.01+self.a_R101*1.01+self.b_R101*16+self.c_R101*14+self.d_R101*32
            self.Csus_ini_R101 = (self.rho_R101*self.SV_R101)/self.MW_sustrato_R101
            self.Csus_ini_ST_R101 = (self.rho_R101*self.ST_R101)/self.MW_sustrato_R101
            self.Csus_fixed_R101 = self.Csus_ini_ST_R101 - self.Csus_ini_R101
            

        #Reactor 102 initial conditions
        if OperationModo in ["Modo3", "Modo4", "Modo5"]:
            self.ST_R102 = ST_R102
            self.SV_R102 = SV_R102
            self.Cc_R102 = Cc_R102
            self.Ch_R102 = Ch_R102
            self.Co_R102 = Co_R102
            self.Cn_R102 = Cn_R102
            self.Cs_R102 = Cs_R102
            self.rho_R102 = rho_R102
            if self.ST_R102 == 0:
                self.Csus_ini_R102 = 0
                self.Csus_ini_ST_R102 = 0
            else:
                self.molC_R102 = self.Cc_R102*(1/12.01)
                self.molH_R102 = self.Ch_R102*(1/1.01)
                self.molO_R102 = self.Co_R102*(1/16)
                self.molN_R102 = self.Cn_R102*(1/14)
                self.molS_R102 = self.Cs_R102*(1/32)

                n_R102 = self.molC_R102
                a_R102 = self.molH_R102
                b_R102 = self.molO_R102
                c_R102 = self.molN_R102
                d_R102 = self.molS_R102

                def lcm(a,b):
                    return a * b // gcd(a, b)

                numbers_R102 = [n_R102, a_R102, b_R102, c_R102, d_R102]
                denominators_R102 = [Fraction(num).limit_denominator(10).denominator for num in numbers_R102]
                common_denominator_R102 = reduce(lcm, denominators_R102)
                subindex_R102 = [int(num * common_denominator_R102) for num in numbers_R102]

                self.n_R102 = subindex_R102[0]
                self.a_R102 = subindex_R102[1]
                self.b_R102 = subindex_R102[2]
                self.c_R102 = subindex_R102[3]
                self.d_R102 = subindex_R102[4]
                
                self.s_H2O_R102 = self.n_R102-(self.a_R102/4)-(self.b_R102/2)+(3/4)*self.c_R102+(self.d_R102/2)
                self.s_CH4_R102 = (self.n_R102/2)+(self.a_R102/8)-(self.b_R102/4)-(3/8)*self.c_R102-(self.d_R102/4)
                self.s_CO2_R102 = (self.n_R102/2)-(self.a_R102/8)+(self.b_R102/4)+(3/8)*self.c_R102-(self.d_R102/4)
                self.s_NH3_R102 = self.c_R102
                self.s_H2S_R102 = self.d_R102
                
                self.MW_sustrato_R102 = self.n_R102*12.01+self.a_R102*1.01+self.b_R102*16+self.c_R102*14+self.d_R102*32
                self.Csus_ini_R102 = (self.rho_R102*self.SV_R102)/self.MW_sustrato_R102
                self.Csus_ini_ST_R102 = (self.rho_R102*self.ST_R102)/self.MW_sustrato_R102
                self.Csus_fixed_R102 = self.Csus_ini_ST_R102 - self.Csus_ini_R102
        
        
        #Create DataFrames to storage Data
        self.OperationModo = OperationModo
        if self.OperationModo == "Modo1":
            columns = ["timestamp"
            , "Q_P104"
            , "Csus_ini"
            , "Temp_R101"
            , "V_normal_V101"
            , "V_normal_CH4_V101"
            , "V_normal_CO2_V101"
            , "V_normal_H2S_V101"
            , "V_normal_O2_V101"
            , "V_normal_H2_V101"
            , "mol_CH4_V101"
            , "mol_CO2_V101"
            , "mol_H2S_V101"
            , "mol_O2_V101"
            , "mol_H2_V101"
            , "mol_H2O_V101"
            , "P_V101"
            , "P_V102"
            , "P_V107"
            , "Pacum_V101"
            , "Vnormal_acum_V101"
            , "mol_CH4_acum_V101"
            , "mol_sus_int_ini_R101"
            , "Csus_ini_R101"
            , "SV_R101"
            , "ST_R101"
            , "yt_R101"]
            
        elif self.OperationModo == "Modo2":
            columns = ["timestamp"
            , "Q_P104"
            , "Csus_ini"
            , "Q_P101"
            , "Temp_R101"
            , "V_normal_V101"
            , "V_normal_CH4_V101"
            , "V_normal_CO2_V101"
            , "V_normal_H2S_V101"
            , "V_normal_O2_V101"
            , "V_normal_H2_V101"
            , "mol_CH4_V101"
            , "mol_CO2_V101"
            , "mol_H2S_V101"
            , "mol_O2_V101"
            , "mol_H2_V101"
            , "mol_H2O_V101"
            , "P_V101"
            , "P_V102"
            , "P_V107"
            , "Pacum_V101"
            , "Vnormal_acum_V101"
            , "mol_CH4_acum_V101"
            , "mol_sus_int_ini_R101"
            , "Csus_ini_R101"
            , "SV_R101"
            , "ST_R101"
            , "yt_R101"]

        elif self.OperationModo == "Modo3":
            columns = ["timestamp"
            , "Q_P104"
            , "Csus_ini"
            , "Q_P101"
            , "Temp_R101" 
            , "Temp_R102"
            , "V_normal_V101"
            , "V_normal_CH4_V101"
            , "V_normal_CO2_V101"
            , "V_normal_H2S_V101"
            , "V_normal_O2_V101"
            , "V_normal_H2_V101"
            , "mol_CH4_V101"
            , "mol_CO2_V101"
            , "mol_H2S_V101"
            , "mol_O2_V101"
            , "mol_H2_V101"
            , "mol_H2O_V101"
            , "P_V101"
            , "P_V102"
            , "P_V107"
            , "Pacum_V101"
            , "Vnormal_acum_V101"
            , "mol_CH4_acum_V101"
            , "V_normal_V102"
            , "V_normal_CH4_V102"
            , "V_normal_CO2_V102"
            , "V_normal_H2S_V102"
            , "V_normal_O2_V102"
            , "V_normal_H2_V102"
            , "mol_CH4_V102"
            , "mol_CO2_V102"
            , "mol_H2S_V102"
            , "mol_O2_V102"
            , "mol_H2_V102"
            , "mol_H2O_V102"
            , "Pacum_V102"
            , "Vnormal_acum_V102"
            , "mol_CH4_acum_V102"
            , "mol_sus_int_ini_R101"
            , "Csus_ini_R101"
            , "SV_R101"
            , "ST_R101"
            , "mol_sus_int_ini_R102"
            , "Csus_ini_R102"
            , "SV_R102"
            , "ST_R102"
            , "yt_R101"
            , "yt_R102"]
        
        elif self.OperationModo == "Modo4" or self.OperationModo == "Modo5":
            columns = ["timestamp"
            , "Q_P104"
            , "Csus_ini"
            , "Q_P101"
            , "Q_P102"
            , "Temp_R101" 
            , "Temp_R102"
            , "V_normal_V101"
            , "V_normal_CH4_V101"
            , "V_normal_CO2_V101"
            , "V_normal_H2S_V101"
            , "V_normal_O2_V101"
            , "V_normal_H2_V101"
            , "mol_CH4_V101"
            , "mol_CO2_V101"
            , "mol_H2S_V101"
            , "mol_O2_V101"
            , "mol_H2_V101"
            , "mol_H2O_V101"
            , "P_V101"
            , "P_V102"
            , "P_V107"
            , "Pacum_V101"
            , "Vnormal_acum_V101"
            , "mol_CH4_acum_V101"
            , "V_normal_V102"
            , "V_normal_CH4_V102"
            , "V_normal_CO2_V102"
            , "V_normal_H2S_V102"
            , "V_normal_O2_V102"
            , "V_normal_H2_V102"
            , "mol_CH4_V102"
            , "mol_CO2_V102"
            , "mol_H2S_V102"
            , "mol_O2_V102"
            , "mol_H2_V102"
            , "mol_H2O_V102"
            , "Pacum_V102"
            , "Vnormal_acum_V102"
            , "mol_CH4_acum_V102"
            , "mol_sus_int_ini_R101"
            , "Csus_ini_R101"
            , "SV_R101"
            , "ST_R101"
            , "mol_sus_int_ini_R102"
            , "Csus_ini_R102"
            , "SV_R102"
            , "ST_R102"
            , "yt_R101"
            , "yt_R102"]

        self.DT_Data = pd.DataFrame(columns= columns)

                      
    def GetValuesFromBiogasPlant (self):
        
        msg = self.InfluxDB.InfluxDBconnection()
        if not msg:
            return {"message":self.influxDB.ERROR_MESSAGE}, 503
        
        query = self.InfluxDB.QueryCreator(measurement = "Planta_Biogas", type = 1)
        data_biogas = self.InfluxDB.InfluxDBreader(query)
        data_biogas.set_index("_field", inplace = True)

        #Get substrate conditions from plant interface
        self.substrateNumber = round(data_biogas["_value"]["MNS"],0)
        self.WaterPorportion = data_biogas["_value"]["MPH"]

        if self.substrateNumber == 1.0:
            self.substrateproportion1 = data_biogas["_value"]["MP1"]/100
            self.ST1 = data_biogas["_value"]["MST1"]/100
            self.SV1 = data_biogas["_value"]["MSV1"]/100
            self.Cc1 = data_biogas["_value"]["MCc1"]
            self.Ch1 = data_biogas["_value"]["MCh1"]
            self.Co1 = data_biogas["_value"]["MCo1"]
            self.Cn1 = data_biogas["_value"]["MCn1"]
            self.Cs1 = data_biogas["_value"]["MCs1"]
            self.rho1 = data_biogas["_value"]["Md1"]
        
        elif self.substrateNumber == 2.0:
            self.substrateproportion1 = data_biogas["_value"]["MP1"]/100
            self.ST1 = data_biogas["_value"]["MST1"]/100
            self.SV1 = data_biogas["_value"]["MSV1"]/100
            self.Cc1 = data_biogas["_value"]["MCc1"]
            self.Ch1 = data_biogas["_value"]["MCh1"]
            self.Co1 = data_biogas["_value"]["MCo1"]
            self.Cn1 = data_biogas["_value"]["MCn1"]
            self.Cs1 = data_biogas["_value"]["MCs1"]
            self.rho1 = data_biogas["_value"]["Md1"]

            self.substrateproportion2 = data_biogas["_value"]["MP2"]/100
            self.ST2 = data_biogas["_value"]["MST2"]/100
            self.SV2 = data_biogas["_value"]["MSV2"]/100
            self.Cc2 = data_biogas["_value"]["MCc2"]
            self.Ch2 = data_biogas["_value"]["MCh2"]
            self.Co2 = data_biogas["_value"]["MCo2"]
            self.Cn2 = data_biogas["_value"]["MCn2"]
            self.Cs2 = data_biogas["_value"]["MCs2"]
            self.rho2 = data_biogas["_value"]["Md2"]
        
        elif self.substrateNumber == 3.0:
            self.substrateproportion1 = data_biogas["_value"]["MP1"]/100
            self.ST1 = data_biogas["_value"]["MST1"]/100
            self.SV1 = data_biogas["_value"]["MSV1"]/100
            self.Cc1 = data_biogas["_value"]["MCc1"]
            self.Ch1 = data_biogas["_value"]["MCh1"]
            self.Co1 = data_biogas["_value"]["MCo1"]
            self.Cn1 = data_biogas["_value"]["MCn1"]
            self.Cs1 = data_biogas["_value"]["MCs1"]
            self.rho1 = data_biogas["_value"]["Md1"]

            self.substrateproportion2 = data_biogas["_value"]["MP2"]/100
            self.ST2 = data_biogas["_value"]["MST2"]/100
            self.SV2 = data_biogas["_value"]["MSV2"]/100
            self.Cc2 = data_biogas["_value"]["MCc2"]
            self.Ch2 = data_biogas["_value"]["MCh2"]
            self.Co2 = data_biogas["_value"]["MCo2"]
            self.Cn2 = data_biogas["_value"]["MCn2"]
            self.Cs2 = data_biogas["_value"]["MCs2"]
            self.rho2 = data_biogas["_value"]["Md2"]

            self.substrateproportion3 = data_biogas["_value"]["MP3"]/100
            self.ST3 = data_biogas["_value"]["MST3"]/100
            self.SV3 = data_biogas["_value"]["MSV3"]/100
            self.Cc3 = data_biogas["_value"]["MCc3"]
            self.Ch3 = data_biogas["_value"]["MCh3"]
            self.Co3 = data_biogas["_value"]["MCo3"]
            self.Cn3 = data_biogas["_value"]["MCn3"]
            self.Cs3 = data_biogas["_value"]["MCs3"]
            self.rho3 = data_biogas["_value"]["Md3"]
        
        elif self.substrateNumber == 4.0:
            self.substrateproportion1 = data_biogas["_value"]["MP1"]/100
            self.ST1 = data_biogas["_value"]["MST1"]/100
            self.SV1 = data_biogas["_value"]["MSV1"]/100
            self.Cc1 = data_biogas["_value"]["MCc1"]
            self.Ch1 = data_biogas["_value"]["MCh1"]
            self.Co1 = data_biogas["_value"]["MCo1"]
            self.Cn1 = data_biogas["_value"]["MCn1"]
            self.Cs1 = data_biogas["_value"]["MCs1"]
            self.rho1 = data_biogas["_value"]["Md1"]

            self.substrateproportion2 = data_biogas["_value"]["MP2"]/100
            self.ST2 = data_biogas["_value"]["MST2"]/100
            self.SV2 = data_biogas["_value"]["MSV2"]/100
            self.Cc2 = data_biogas["_value"]["MCc2"]
            self.Ch2 = data_biogas["_value"]["MCh2"]
            self.Co2 = data_biogas["_value"]["MCo2"]
            self.Cn2 = data_biogas["_value"]["MCn2"]
            self.Cs2 = data_biogas["_value"]["MCs2"]
            self.rho2 = data_biogas["_value"]["Md2"]

            self.substrateproportion3 = data_biogas["_value"]["MP3"]/100
            self.ST3 = data_biogas["_value"]["MST3"]/100
            self.SV3 = data_biogas["_value"]["MSV3"]/100
            self.Cc3 = data_biogas["_value"]["MCc3"]
            self.Ch3 = data_biogas["_value"]["MCh3"]
            self.Co3 = data_biogas["_value"]["MCo3"]
            self.Cn3 = data_biogas["_value"]["MCn3"]
            self.Cs3 = data_biogas["_value"]["MCs3"]
            self.rho3 = data_biogas["_value"]["Md3"]

            self.substrateproportion4 = data_biogas["_value"]["MP4"]/100
            self.ST4 = data_biogas["_value"]["MST4"]/100
            self.SV4 = data_biogas["_value"]["MSV4"]/100
            self.Cc4 = data_biogas["_value"]["MCc4"]
            self.Ch4 = data_biogas["_value"]["MCh4"]
            self.Co4 = data_biogas["_value"]["MCo4"]
            self.Cn4 = data_biogas["_value"]["MCn4"]
            self.Cs4 = data_biogas["_value"]["MCs4"]
            self.rho4 = data_biogas["_value"]["Md4"]
        
        #Get RPM from TK-100
        self.SE_107 = data_biogas["_value"]["SE107"]
        #Get values for P104
        self.TRH = data_biogas["_value"]["MTRH"]
        self.FT_P104 = data_biogas["_value"]["MFTP104"]
        self.TTO_P104 = data_biogas["_value"]["MTTOP104"]
        self.timeP104 = data_biogas["_time"]["SE104"]
        self.SE104 = data_biogas["_value"]["SE104"]
        #Get Values for R101
        self.TE_101Av = data_biogas["_value"]["TE101A"]
        self.TE_101Bv = data_biogas["_value"]["TE101A"]
        self.AT_101 = data_biogas["_value"]["AT101"]
        self.SE_108 = data_biogas["_value"]["SE108"]
        self.LT_101 = data_biogas["_value"]["LT101"]

        if self.OperationModo == "Modo2":
            #get values for P101
            self.FT_P101 = data_biogas["_value"]["MFTP101"]
            self.TTO_P101 = data_biogas["_value"]["MTTOP101"]
            self.Qset_P101 = data_biogas["_value"]["MQP101"]
            self.SE101 = data_biogas["_value"]["SE101"]
        
        elif self.OperationModo == "Modo3":
            self.SE101 = data_biogas["_value"]["SE101"]
            #Get Values for R102
            self.TE_102A = data_biogas["_value"]["TE102A"]
            self.TE_102B = data_biogas["_value"]["TE102B"]
            self.AT_102 = data_biogas["_value"]["AT102"]
            self.SE_109 = data_biogas["_value"]["SE109"]
            self.LT_102 = data_biogas["_value"]["LT102"]
        
        elif self.OperationModo == "Modo4" or self.OperationModo == "Modo5":
            self.SE101 = data_biogas["_value"]["SE101"]
            self.FT_P102 = data_biogas["_value"]["MFTP102"]
            self.TTO_P102 = data_biogas["_value"]["MTTOP102"]
            self.Qset_P102 = data_biogas["_value"]["MQP102"]
            self.SE102 = data_biogas["_value"]["SE102"]
            #Get Values for R102
            self.TE_102A = data_biogas["_value"]["TE102A"]
            self.TE_102B = data_biogas["_value"]["TE102B"]
            self.AT_102 = data_biogas["_value"]["AT102"]
            self.SE_109 = data_biogas["_value"]["SE109"]
            self.LT_102 = data_biogas["_value"]["LT102"]
        
        #Get values from V-101
        self.AT103A1 = data_biogas["_value"]["AT103ACH4"]
        self.AT103A2 = data_biogas["_value"]["AT103ACO2"]
        self.AT103A3 = data_biogas["_value"]["AT103AH2S"]
        self.AT103A4 = data_biogas["_value"]["AT103AO2"]
        self.AT103A5 = data_biogas["_value"]["AT103AH2"]
        self.AT103B = data_biogas["_value"]["AT103B"]
        self.PT103 = data_biogas["_value"]["PT103"]
        self.TT103 = data_biogas["_value"]["TT103"]

        #Get values from V-102
        self.AT104A1 = data_biogas["_value"]["AT104ACH4"]
        self.AT104A2 = data_biogas["_value"]["AT104ACO2"]
        self.AT104A3 = data_biogas["_value"]["AT104AH2S"]
        self.AT104A4 = data_biogas["_value"]["AT104AO2"]
        self.AT104A5 = data_biogas["_value"]["AT104AH2"]
        self.AT104B = data_biogas["_value"]["AT104B"]
        self.PT104 = data_biogas["_value"]["PT104"]
        self.TT104 = data_biogas["_value"]["TT104"]

        #Get values from V-107
        self.AT105A1 = data_biogas["_value"]["AT105ACH4"]
        self.AT105A2 = data_biogas["_value"]["AT105ACO2"]
        self.AT105A3 = data_biogas["_value"]["AT105AH2S"]
        self.AT105A4 = data_biogas["_value"]["AT105AO2"]
        self.AT105A5 = data_biogas["_value"]["AT105AH2"]
        self.AT105B = data_biogas["_value"]["AT105B"]
        self.PT105 = data_biogas["_value"]["PT105"]
        self.TT105 = data_biogas["_value"]["TT105"]

    def Substrate_conditions (self, manual_substrate, Cc, Ch, Co, Cn, Cs, rho, ST, SV):

        if manual_substrate == True:
            self.ST = ST
            self.SV = SV
            self.Cc = Cc
            self.Ch = Ch
            self.Co = Co
            self.Cn = Cn
            self.Cs = Cs
            self.rho = rho
        
        else:
            
            if self.substrateNumber == 1:
                self.ST = self.ST1/100
                self.SV = self.SV1/100
                self.Cc = self.Cc1
                self.Ch = self.Ch1
                self.Co = self.Co1
                self.Cn = self.Cn1
                self.Cs = self.Cs1
                self.rho = self.rho1  

            elif self.substrateNumber == 2:
                self.ST = self.ST1*self.substrateproportion1 + self.ST2*self.substrateproportion2
                self.SV = self.SV1*self.substrateproportion1 + self.SV2*self.substrateproportion2
                self.rho = self.rho1*self.substrateproportion1 + self.rho2*self.substrateproportion2 + 1000*self.WaterPorportion
                self.Cc = self.Cc1*self.substrateproportion1 + self.Cc2*self.substrateproportion2
                self.Ch = self.Ch1*self.substrateproportion1 + self.Ch2*self.substrateproportion2
                self.Co = self.Co1*self.substrateproportion1 + self.Co2*self.substrateproportion2
                self.Cn = self.Cn1*self.substrateproportion1 + self.Cn2*self.substrateproportion2
                self.Cs = self.Cs1*self.substrateproportion1 + self.Cs2*self.substrateproportion2
            
            elif self.substrateNumber == 3:
                self.ST = self.ST1*self.substrateproportion1 + self.ST2*self.substrateproportion2 + self.ST3*self.substrateproportion3
                self.SV = self.SV1*self.substrateproportion1 + self.SV2*self.substrateproportion2 + self.ST3*self.substrateproportion3
                self.rho = self.rho1*self.substrateproportion1 + self.rho2*self.substrateproportion2 + self.rho3*self.substrateproportion3 + 1000*self.WaterPorportion
                self.Cc = self.Cc1*self.substrateproportion1 + self.Cc2*self.substrateproportion2 + self.Cc3*self.substrateproportion3
                self.Ch = self.Ch1*self.substrateproportion1 + self.Ch2*self.substrateproportion2 + self.Ch3*self.substrateproportion3
                self.Co = self.Co1*self.substrateproportion1 + self.Co2*self.substrateproportion2 + self.Co3*self.substrateproportion3
                self.Cn = self.Cn1*self.substrateproportion1 + self.Cn2*self.substrateproportion2 + self.Cn3*self.substrateproportion3
                self.Cs = self.Cs1*self.substrateproportion1 + self.Cs2*self.substrateproportion2 + self.Cs3*self.substrateproportion3   
                
            elif self.substrateNumber == 4:
                self.ST = self.ST1*self.substrateproportion1 + self.ST2*self.substrateproportion2 + self.ST3*self.substrateproportion3 + self.ST4*self.substrateproportion4
                self.SV = self.SV1*self.substrateproportion1 + self.SV2*self.substrateproportion2 + self.ST3*self.substrateproportion3 + self.ST4*self.substrateproportion4
                self.rho = self.rho1*self.substrateproportion1 + self.rho2*self.substrateproportion2 + self.rho3*self.substrateproportion3 + 1000*self.WaterPorportion
                self.Cc = self.Cc1*self.substrateproportion1 + self.Cc2*self.substrateproportion2 + self.Cc3*self.substrateproportion3 + self.Cc4*self.substrateproportion4
                self.Ch = self.Ch1*self.substrateproportion1 + self.Ch2*self.substrateproportion2 + self.Ch3*self.substrateproportion3 + self.Ch4*self.substrateproportion4
                self.Co = self.Co1*self.substrateproportion1 + self.Co2*self.substrateproportion2 + self.Co3*self.substrateproportion3 + self.Co4*self.substrateproportion4
                self.Cn = self.Cn1*self.substrateproportion1 + self.Cn2*self.substrateproportion2 + self.Cn3*self.substrateproportion3 + self.Cn4*self.substrateproportion4
                self.Cs = self.Cs1*self.substrateproportion1 + self.Cs2*self.substrateproportion2 + self.Cs3*self.substrateproportion3 + self.Cs4*self.substrateproportion4   
        
        #Mix of substrates
        self.molC = self.Cc*(1/12.01)
        self.molH = self.Ch*(1/1.01)
        self.molO = self.Co*(1/16)
        self.molN = self.Cn*(1/14)
        self.molS = self.Cs*(1/32)

        n = self.molC
        a = self.molH
        b = self.molO
        c = self.molN
        d = self.molS

        def lcm(a,b):
                return a * b // gcd(a, b)
        
        numbers = [n, a, b, c, d]
        denominators = [Fraction(num).limit_denominator(10).denominator for num in numbers]
        common_denominator = reduce(lcm, denominators)
        subindex = [int(num * common_denominator) for num in numbers]

        self.n = subindex[0]
        self.a = subindex[1]
        self.b = subindex[2]
        self.c = subindex[3]
        self.d = subindex[4]
        
        self.s_H2O = self.n-(self.a/4)-(self.b/2)+(3/4)*self.c+(self.d/2)
        self.s_CH4 = (self.n/2)+(self.a/8)-(self.b/4)-(3/8)*self.c-(self.d/4)
        self.s_CO2 = (self.n/2)-(self.a/8)+(self.b/4)+(3/8)*self.c-(self.d/4)
        self.s_NH3 = self.c
        self.s_H2S = self.d
        
        self.MW_sustrato = self.n*12.01+self.a*1.01+self.b*16+self.c*14+self.d*32
        self.Csus_ini = (self.rho*self.SV)/self.MW_sustrato
        self.Csus_ini_ST = (self.rho*self.ST)/self.MW_sustrato
        self.Csus_fixed = self.Csus_ini_ST - self.Csus_ini

        self.Csv = (self.rho*(self.SV/100))
        self.Cst = (self.rho*(self.ST/100))

    def Pump104 (self, manual_P104=False, TRH=30, FT_P104=5, TTO_P104=10):    
        
        self.manual_P104 = manual_P104
        
        if  self.manual_P104 == True:
            self.TRH = TRH
            self.FT_P104 = FT_P104
            self.TTO_P104 = TTO_P104
            try:
                self.TurnOnDailyStep_P104 = 24/self.FT_P104
            except ZeroDivisionError:
                self.TurnOnDailyStep_P104=0
            
            if self.OperationModo == "Modo1" or self.OperationModo == "Modo2":
                self.Q_daily = self.VR1/self.TRH
            
            elif self.OperationModo == "Modo3" or self.OperationModo == "Modo4" or self.OperationModo == "Modo5":
                self.Q_daily = (self.VR1 + self.VR2)/self.TRH
            
            self.Q_time = self.Q_daily/self.FT_P104

            if self.TimeCounterPump_P104<self.TTO_P104*60:
                self.Q_P104 = (self.Q_time/self.TTO_P104)*60
            else:
                self.Q_P104= float(0)
            
            self.TimeCounterPump_P104 = self.TimeCounterPump_P104 + self.tp

            if self.TimeCounterPump_P104>=self.TurnOnDailyStep_P104*3600:
                self.TimeCounterPump_P104 = 0
        
        else:
            
            self.Q_P104 = self.SE104
            self.TRH = self.TRH
            self.FT_P104 = self.FT_P104
            self.TTO_P104 = self.TTO_P104
            
    
    def Pump101 (self, manual_P101=False, FT_P101=5, TTO_P101=10, Q_P101 = 2.4):
        
        self.manual_P101 = manual_P101
    
        if self.manual_P101 == True:

            if self.OperationModo == "Modo1":
                pass

            elif self.OperationModo == "Modo2":
                self.FT_P101= FT_P101
                self.TTO_P101 = TTO_P101

                try:
                    self.TurnOnDailyStep_P101 = 24/self.FT_P101
                except ZeroDivisionError:
                    self.TurnOnDailyStep_P101 = 0


                if self.TimeCounterPump_P101<self.TTO_P101*60:
                    self.Q_P101 = Q_P101
                else:
                    self.Q_P101= float(0)
                
                self.TimeCounterPump_P101 = self.TimeCounterPump_P101 + self.tp
            
                if self.TimeCounterPump_P101>=self.TurnOnDailyStep_P101*3600:
                    self.TimeCounterPump_P101 = 0

            elif self.OperationModo == "Modo3" or self.OperationModo == "Modo5":
                self.Q_P101 = self.Q_P104

            elif self.OperationModo == "Modo4":
                
                try:
                    self.Q_P102 = self.Q_P102
                except:
                    self.Q_P102 = 0

                self.Q_P101 = self.Q_P104 + self.Q_P102
                
        else:

            if self.OperationModo == "Modo1":
                pass
            elif self.OperationModo == "Modo2":
                self.Q_P101 = self.SE101
                self.FT_P101 = self.FT_P101
                self.TTO_P101 = self.TTO_P101
                self.Qset_P101 = self.Qset_P101
            elif self.OperationModo in ["Modo3", "Modo4", "Modo5"]:
                self.Q_P101 = self.SE101


    
    def Pump102 (self, manual_P102=False, FT_P102=5, TTO_P102=10, Q_P102 = 2.4):
        
        self.manual_P102 = manual_P102

        if self.manual_P102 == True:

            if self.OperationModo == "Modo1" or self.OperationModo == "Modo2" or self.OperationModo == "Modo3":
                pass

            elif self.OperationModo == "Modo4" or self.OperationModo == "Modo5":
                self.FT_P102= FT_P102
                self.TTO_P102 = TTO_P102

                try:
                    self.TurnOnDailyStep_P102 = 24/self.FT_P102
                except ZeroDivisionError:
                    self.TurnOnDailyStep_P102 = 0

                if self.TimeCounterPump_P102<self.TTO_P102*60:
                    self.Q_P102 = Q_P102
                else:
                    self.Q_P102= float(0)
                
                self.TimeCounterPump_P102 = self.TimeCounterPump_P102 + self.tp

                if self.TimeCounterPump_P102>=self.TurnOnDailyStep_P102*3600:
                    self.TimeCounterPump_P102 = 0

        else:

            if self.OperationModo == "Modo1" or self.OperationModo == "Modo2" or self.OperationModo == "Modo3":
                pass

            else:
                self.Q_P102 = self.SE102
                self.FT_P102 = self.FT_P102
                self.TTO_P102 = self.TTO_P102
                self.Qset_P102 = self.Qset_P102
    
    def pHR101(self, manual_pH_R101 = False, pH = 7):
        self.manual_pH_R101 = manual_pH_R101
        if self.manual_pH_R101 == True:
            self.pH_R101 = pH
        else:
            self.pH_R101 = self.AT_101
    
    def pHR102(self, manual_pH_R102 = False, pH = 7):
        self.manual_pH_R102 = manual_pH_R102
        if self.manual_pH_R102 == True:
            self.pH_R102 = pH
        else:
            self.pH_R102 = self.AT_102
            
    def Temperature_R101 (self, manual_temp_R101 = False, Temp_R101=35):
        
        self.manual_temp_R101 = manual_temp_R101

        if self.manual_temp_R101 == False:
            self.Temp_R101 = float(Temp_R101)

        else:

            self.TE_101Av = self.TE_101Av
            self.TE_101Bv = self.TE_101Bv

            T1 = float(self.TE_101Av)
            T2 = float(self.TE_101Bv)
            self.Temp_R101 = float((T1 + T2)/2)
    
    def Temperature_R102 (self, manual_temp_R102 = 1, Temp_R102=35):
        self.manual_temp_R102 = manual_temp_R102

        if self.OperationModo == "Modo1" or self.OperationModo == "Modo2":
            pass

        else:

            if self.manual_temp_R102 == False:
                self.Temp_R102 = float(Temp_R102)

            else:
                self.TE_102Av = self.TE_102A
                self.TE_102Bv = self.TE_102B

                T1 = self.TE_102Av
                T2 = self.TE_102Bv
                self.Temp_R102 = (T1 + T2)/2
    
    def Mixing_TK100 (self, manual_mixing = False, FT_mixing_TK100=5, TTO_mixing_TK100 = 10, RPM_TK100 = 50):
        
        if manual_mixing == True:
            self.FT_mixing_TK100 = FT_mixing_TK100
            self.TTO_mixing_TK100 = TTO_mixing_TK100
            try:
                self.TurnOnDailyStep_Mixing_TK100 = 24/self.FT_mixing_TK100
            except ZeroDivisionError:
                self.TurnOnDailyStep_Mixing_TK100 = 0
            
            if self.TimeCounterMixer_TK100<self.TTO_mixing_TK100*60:
                self.RPM_TK100 = RPM_TK100
            else:
                self.RPM_TK100 = RPM_TK100
            
            self.TimeCounterMixer_TK100 = self.TimeCounterMixer_TK100 + self.tp

            if self.TimeCounterMixer_TK100>=self.TurnOnDailyStep_Mixing_TK100*3600:
                self.TimeCounterMixer_TK100 = 0
        
        else:
            self.RPM_TK100 = self.SE_107
    
    def Mixing_R101 (self, manual_mixing = False, FT_mixing_R101=5, TTO_mixing_R101 = 10, RPM_R101 = 50):
        
        if manual_mixing == True:
            self.FT_mixing_R101 = FT_mixing_R101
            self.TTO_mixing_R101 = TTO_mixing_R101
            try:
                self.TurnOnDailyStep_Mixing_R101 = 24/self.FT_mixing_R101
            except ZeroDivisionError:
                self.TurnOnDailyStep_Mixing_R101 = 0
            
            if self.TimeCounterMixer_R101<self.TTO_mixing_R101*60:
                self.RPM_R101 = RPM_R101
            else:
                self.RPM_R101 = RPM_R101
            
            self.TimeCounterMixer_R101 = self.TimeCounterMixer_R101 + self.tp

            if self.TimeCounterMixer_R101>=self.TurnOnDailyStep_Mixing_R101*3600:
                self.TimeCounterMixer_R101 = 0
        
        else:
            self.RPM_R101 = self.SE_108
    
    def Mixing_R102 (self, manual_mixing = False, FT_mixing_R102=5, TTO_mixing_R102 = 10, RPM_R102 = 50):
        
        if manual_mixing == True:
            if self.OperationModo in ["Modo1", "Modo2"]:
                pass
            else:
                self.FT_mixing_R102 = FT_mixing_R102
                self.TTO_mixing_R102 = TTO_mixing_R102
                try:
                    self.TurnOnDailyStep_Mixing_R102 = 24/self.FT_mixing_R102
                except ZeroDivisionError:
                    self.TurnOnDailyStep_Mixing_R102 = 0
                
                if self.TimeCounterMixer_R102<self.TTO_mixing_R102*60:
                    self.RPM_R102 = RPM_R102
                else:
                    self.RPM_R102 = RPM_R102
                
                self.TimeCounterMixer_R102 = self.TimeCounterMixer_R102 + self.tp

                if self.TimeCounterMixer_R102>=self.TurnOnDailyStep_Mixing_R102*3600:
                    self.TimeCounterMixer_R102 = 0
        else:
            pass

    def V_101_DT (self):               
        self.RH_V101 = self.AT103B

        self.P_std = 100        #[kPa]
        self.T_std = 273.15     #[K]    

        self.V_normal_V101 = ((self.PT103*6.89476)*self.VG1*self.T_std)/(self.P_std*(self.TT103+273.15))
        
        self.V_normal_CH4_V101 = self.AT103A1/100*self.V_normal_V101
        
        self.V_normal_CO2_V101 = self.AT103A2/100*self.V_normal_V101
       
        self.V_normal_H2S_V101 = self.AT103A3/1000000*self.V_normal_V101
        
        self.V_normal_O2_V101 = self.AT103A4/100*self.V_normal_V101
        
        self.V_normal_H2_V101 = self.AT103A5/1000000*self.V_normal_V101
        
        self.V_mol_CH4 = self.Thermo.Hgases(xCH4=1, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103, Patm=100, T=self.TT103)[2]
        self.V_mol_CO2 = self.Thermo.Hgases(xCH4=0, xCO2=1, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103, Patm=100, T=self.TT103)[2]
        self.V_mol_H2S = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=1, xH2=0, P=self.PT103, Patm=100, T=self.TT103)[2]
        self.V_mol_O2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=1, xN2=0, xH2S=0, xH2=0, P=self.PT103, Patm=100, T=self.TT103)[2]
        self.V_mol_H2 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=1, P=self.PT103, Patm=100, T=self.TT103)[2]
        self.V_mol_NH3 = self.Thermo.Hgases(xCH4=0, xCO2=0, xH2O=0, xO2=0, xN2=0, xH2S=0, xH2=0, P=self.PT103, Patm=100, T=self.TT103, xNH3=1)[2]

        self.mol_CH4_V101 = self.V_normal_CH4_V101/self.V_mol_CH4     
        
        self.mol_CO2_V101 = self.V_normal_CO2_V101/self.V_mol_CO2
        
        self.mol_H2S_V101 = self.V_normal_H2S_V101/self.V_mol_H2S
        
        self.mol_O2_V101 = self.V_normal_O2_V101/self.V_mol_O2
        
        self.mol_H2_V101 = self.V_normal_H2_V101/self.V_mol_H2

        #Amonio
        self.mol_NH3_V101 = (self.s_NH3/self.s_CH4)*self.mol_CH4_V101
        self.V_normal_NH3_V101 = self.mol_NH3_V101*self.V_mol_NH3
        try:
            if (self.mol_CH4_V101 + self.mol_CO2_V101 + self.mol_H2S_V101 + self.mol_O2_V101 + self.mol_H2_V101 + self.mol_NH3_V101) == 0:
                self.AT103A6 = 0
            else:
                self.AT103A6 =  self.mol_NH3_V101/(self.mol_CH4_V101 + self.mol_CO2_V101 + self.mol_H2S_V101 + self.mol_O2_V101 + self.mol_H2_V101 + self.mol_NH3_V101)*1000000
        except (ZeroDivisionError, ValueError):
            self.AT103A6 = 0

        self.RH_V101 = self.RH_V101/100
        self.AH_v101 = self.Thermo.BiogasAbsoluteHumidity(self.RH_V101, self.TT103)
        self.mol_H2O_V101 = self.AH_v101*self.V_normal_V101

        if (len (self.DT_Data["P_V101"]) > 1) and (self.PT103*1.05 < self.DT_Data["P_V101"].iloc[-1]):  #Cambiar cuando se conecte con la planta real
            self.P_ini_V101 = self.Pacum_V101
        
        self.Pacum_V101 = self.PT103 + self.P_ini_V101
       
        self.Vnormal_acum_V101 = ((self.Pacum_V101*6.89476)*self.VG1*self.T_std)/(self.P_std*(self.TT103+273.15))
        
        self.V_normal_CH4_acum_V101 = self.AT103A1/100*self.Vnormal_acum_V101
        self.mol_CH4_acum_V101 = self.V_normal_CH4_acum_V101/self.V_mol_CH4 

        self.V_normal_CO2_acum_V101 = self.AT103A2/100*self.Vnormal_acum_V101
        self.mol_CO2_acum_V101 = self.V_normal_CO2_acum_V101/self.V_mol_CO2

        self.V_normal_H2S_acum_V101 = self.AT103A3/1000000*self.Vnormal_acum_V101
        self.mol_H2S_acum_V101 = self.V_normal_H2S_acum_V101/self.V_mol_H2S

        self.V_normal_O2_acum_V101 = self.AT103A4/100*self.Vnormal_acum_V101
        self.mol_O2_acum_V101 = self.V_normal_O2_acum_V101/self.V_mol_O2

        self.V_normal_H2_acum_V101 = self.AT103A5/1000000*self.Vnormal_acum_V101
        self.mol_H2_acum_V101 = self.V_normal_H2_acum_V101/self.V_mol_H2

    def V_102_DT (self):

        self.RH_V102 = self.AT104B

        self.V_normal_V102 = ((self.PT104*6.89476)*self.VG2*self.T_std)/(self.P_std*(self.TT104+273.15))
        
        self.V_normal_CH4_V102 = self.AT104A1/100*self.V_normal_V102
        
        self.V_normal_CO2_V102 = self.AT104A2/100*self.V_normal_V102
        
        self.V_normal_H2S_V102 = self.AT104A3/1000000*self.V_normal_V102
        
        self.V_normal_O2_V102 = self.AT104A4/100*self.V_normal_V102
        
        self.V_normal_H2_V102 = self.AT103A5/1000000*self.V_normal_V102
        
        self.mol_CH4_V102 = self.V_normal_CH4_V102/self.V_mol_CH4     
        
        self.mol_CO2_V102 = self.V_normal_CO2_V102/self.V_mol_CO2
        
        self.mol_H2S_V102 = self.V_normal_H2S_V102/self.V_mol_H2S
        
        self.mol_O2_V102 = self.V_normal_O2_V102/self.V_mol_O2
        
        self.mol_H2_V102 = self.V_normal_H2_V102/self.V_mol_H2

        #Amonio
        self.mol_NH3_V102 = (self.s_NH3/self.s_CH4)*self.mol_CH4_V102
        self.V_normal_NH3_V102 = self.mol_NH3_V102*self.V_mol_NH3
        
        try:
            if (self.mol_CH4_V102 + self.mol_CO2_V102 + self.mol_H2S_V102 + self.mol_O2_V102 + self.mol_H2_V102 + self.mol_NH3_V102) == 0:
                self.AT104A6 = 0
            else:
                self.AT104A6 =  self.mol_NH3_V102/(self.mol_CH4_V102 + self.mol_CO2_V102 + self.mol_H2S_V102 + self.mol_O2_V102 + self.mol_H2_V102 + self.mol_NH3_V102)*1000000
        except ZeroDivisionError:
            self.AT104A6 = 0


        self.RH_V102 = self.RH_V102/100
        self.AH_v102 = self.Thermo.BiogasAbsoluteHumidity(self.RH_V102, self.TT104)
        self.mol_H2O_V102 = self.AH_v102*self.V_normal_V102
        
        if (len (self.DT_Data["P_V102"]) > 1) and (self.PT104*1.05 < self.DT_Data["P_V102"].iloc[-1]):  #Cambiar cuando se conecte con la planta real
            self.P_ini_V102 = self.Pacum_V102
        
        self.Pacum_V102 = self.PT104 + self.P_ini_V102
        
        self.Vnormal_acum_V102 = ((self.Pacum_V102*6.89476)*self.VG2*self.T_std)/(self.P_std*(self.TT104+273.15))
        
        self.V_normal_CH4_acum_V102 = self.AT104A1/100*self.Vnormal_acum_V102
        self.mol_CH4_acum_V102 = self.V_normal_CH4_acum_V102/self.V_mol_CH4     

        self.V_normal_CO2_acum_V102 = self.AT104A2/100*self.Vnormal_acum_V102
        self.mol_CO2_acum_V102 = self.V_normal_CO2_acum_V102/self.V_mol_CO2

        self.V_normal_H2S_acum_V102 = self.AT104A3/1000000*self.Vnormal_acum_V102
        self.mol_H2S_acum_V102 = self.V_normal_H2S_acum_V102/self.V_mol_H2S

        self.V_normal_O2_acum_V102 = self.AT104A4/100*self.Vnormal_acum_V102
        self.mol_O2_acum_V102 = self.V_normal_O2_acum_V102/self.V_mol_O2

        self.V_normal_H2_acum_V102 = self.AT104A5/1000000*self.Vnormal_acum_V102
        self.mol_H2_acum_V102 = self.V_normal_H2_acum_V102/self.V_mol_H2
        
        
    def V_107_DT (self):
        self.RH_V107 = self.AT105B

        self.V_normal_V107 = ((self.PT105*6.89476)*self.VG3*self.T_std)/(self.P_std*(self.TT105+273.15))
        
        self.V_normal_CH4_V107 = self.AT105A1/100*self.V_normal_V107
       
        self.V_normal_CO2_V107 = self.AT105A2/100*self.V_normal_V107
        
        self.V_normal_H2S_V107 = self.AT105A3/1000000*self.V_normal_V107
        
        self.V_normal_O2_V107 = self.AT105A4/100*self.V_normal_V107
        
        self.V_normal_H2_V107 = self.AT105A5/1000000*self.V_normal_V107
       
        self.mol_CH4_V107 = self.V_normal_CH4_V107/self.V_mol_CH4     
        
        self.mol_CO2_V107 = self.V_normal_CO2_V107/self.V_mol_CO2
        
        self.mol_H2S_V107 = self.V_normal_H2S_V107/self.V_mol_H2S
        
        self.mol_O2_V107 = self.V_normal_O2_V107/self.V_mol_O2
        
        self.mol_H2_V107 = self.V_normal_H2_V107/self.V_mol_H2

        #Amonio
        self.mol_NH3_V107 = (self.s_NH3/self.s_CH4)*self.mol_CH4_V107
        self.V_normal_NH3_V107 = self.mol_NH3_V107*self.V_mol_NH3
        
        try:
            if (self.mol_CH4_V107 + self.mol_CO2_V107 + self.mol_H2S_V107 + self.mol_O2_V107 + self.mol_H2_V107 + self.mol_NH3_V107) == 0:
                self.AT105A6 =  0
            else:
                self.AT105A6 =  self.mol_NH3_V107/(self.mol_CH4_V107 + self.mol_CO2_V107 + self.mol_H2S_V107 + self.mol_O2_V107 + self.mol_H2_V107 + self.mol_NH3_V107)*1000000

        except ZeroDivisionError:
            self.AT105A6 = 0

        self.RH_V107 = self.RH_V107/100
        self.AH_v107 = self.Thermo.BiogasAbsoluteHumidity(self.RH_V107, self.TT105)
        self.mol_H2O_V107 = self.AH_v107*self.V_normal_V107
        
        if (len (self.DT_Data["P_V107"]) > 1) and (self.PT105*1.05 < self.DT_Data["P_V107"].iloc[-1]):  #Cambiar cuando se conecte con la planta real
            self.P_ini_V107 = self.Pacum_V107
        
        self.Pacum_V107 = self.PT105 + self.P_ini_V107
        
        self.Vnormal_acum_V107 = ((self.Pacum_V107*6.89476)*self.VG3*self.T_std)/(self.P_std*(self.TT105+273.15))
       
        self.V_normal_CH4_acum_V107 = self.AT105A1/100*self.Vnormal_acum_V107
        self.mol_CH4_acum_V107 = self.V_normal_CH4_acum_V107/self.V_mol_CH4 

        self.V_normal_CO2_acum_V107 = self.AT104A2/100*self.Vnormal_acum_V107
        self.mol_CO2_acum_V107 = self.V_normal_CO2_acum_V107/self.V_mol_CO2

        self.V_normal_H2S_acum_V107 = self.AT104A3/1000000*self.Vnormal_acum_V107
        self.mol_H2S_acum_V107 = self.V_normal_H2S_acum_V107/self.V_mol_H2S

        self.V_normal_O2_acum_V107 = self.AT104A4/100*self.Vnormal_acum_V107
        self.mol_O2_acum_V107 = self.V_normal_O2_acum_V107/self.V_mol_O2

        self.V_normal_H2_acum_V107 = self.AT104A5/1000000*self.Vnormal_acum_V107
        self.mol_H2_acum_V107 = self.V_normal_H2_acum_V107/self.V_mol_H2    
        
    def R101_DT (self):      
        
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

            self.volatilemass_int_ini_R101 = self.SV_R101*self.rho_R101*self.VR1
            self.volatilemass_in_R101 = self.Q_P104*self.SV*self.rho*(self.tp/3600)

            self.TotalSolids_int_ini_R101 = self.ST_R101*self.rho_R101*self.VR1
            self.TotalSolids_in_R101 = self.Q_P104*self.ST*self.rho*(self.tp/3600)
            
            if self.OperationModo == "Modo1":
                
                self.Csus_ini_R101 = (self.mol_sus_int_ini_R101 + self.mol_sus_in_R101 - self.mol_sus_stoichometricFR_R101)/(self.VR1+(self.Q_P104*(self.tp/3600)))
                self.SV_R101 = ((self.volatilemass_int_ini_R101 + self.volatilemass_in_R101 - self.volatilemass_stoichometricFR_R101)/(self.VR1 + (self.Q_P104*(self.tp/3600))))/self.rho
                self.ST_R101 = ((self.TotalSolids_int_ini_R101 + self.TotalSolids_in_R101 - self.TotalSolids_stoichometricFR_R101)/(self.VR1+(self.Q_P104*(self.tp/3600))))/self.rho
                            
            elif self.OperationModo == "Modo2":

                self.Csus_ini_R101 = (self.mol_sus_int_ini_R101 + self.mol_sus_in_R101 - self.mol_sus_stoichometricFR_R101)/(self.VR1 - self.Q_P101*(self.tp/3600) + (self.Q_P104+self.Q_P101)*(self.tp/3600))
                self.SV_R101 = ((self.volatilemass_int_ini_R101 + self.volatilemass_in_R101 - self.volatilemass_stoichometricFR_R101)/(self.VR1 - self.Q_P101*(self.tp/3600) + (self.Q_P104+self.Q_P101)*(self.tp/3600)))/self.rho
                self.ST_R101 = ((self.TotalSolids_int_ini_R101 + self.TotalSolids_in_R101 - self.TotalSolids_stoichometricFR_R101)/(self.VR1 - self.Q_P101*(self.tp/3600) + (self.Q_P104+self.Q_P101)*(self.tp/3600)))/self.rho
                
            elif self.OperationModo == "Modo3" or self.OperationModo == "Modo5":

                self.Csus_ini_R101 = (self.mol_sus_int_ini_R101 + self.mol_sus_in_R101 - self.mol_sus_stoichometricFR_R101)/(self.VR1+(self.Q_P101*(self.tp/3600)))
                self.SV_R101 = ((self.volatilemass_int_ini_R101 + self.volatilemass_in_R101 - self.volatilemass_stoichometricFR_R101)/(self.VR1 + (self.Q_P101*(self.tp/3600))))/self.rho
                self.ST_R101 = ((self.TotalSolids_int_ini_R101 + self.TotalSolids_in_R101 - self.TotalSolids_stoichometricFR_R101)/(self.VR1+(self.Q_P101*(self.tp/3600))))/self.rho
                
            elif self.OperationModo == "Modo4":
                self.mol_sus_in_R101_2 = self.Q_P102*self.Csus_ini_R102
                self.Csus_ini_R101 = (self.mol_sus_int_ini_R101 + self.mol_sus_in_R101 + self.mol_sus_in_R101_2 - self.mol_sus_stoichometricFR_R101)/(self.VR1 + (self.Q_P101)*(self.tp/3600))

                self.volatilemass_in_R101_2 = self.Q_P102*self.SV_R102*self.rho*(self.tp/3600)
                self.SV_R101 = ((self.volatilemass_int_ini_R101 + self.volatilemass_in_R101 + self.volatilemass_in_R101_2 - self.volatilemass_stoichometricFR_R101)/(self.VR1 + (self.Q_P101)*(self.tp/3600)))/self.rho

                self.TotalSolids_in_R101_2 = self.Q_P102*self.ST_R102*(self.tp/3600)
                self.ST_R101 = (self.TotalSolids_int_ini_R101 + self.TotalSolids_in_R101 + self.TotalSolids_in_R101_2 - self.TotalSolids_stoichometricFR_R101)/(self.VR1 + (self.Q_P101)*(self.tp/3600))/self.rho
                            
            self.SV_R101_gL = self.SV_R101*self.rho
            self.ST_R101_gl = self.ST_R101*self.rho
            self.X_R101 = (self.mol_sus_in_R101 - self.mol_sus_int_ini_R101)/self.mol_sus_in_R101
            self.y_gompertz_R101 = (self.V_normal_CH4_acum_V101/self.SV_R101_gL)*self.VR1
            try:
                if self.GlobalTime == 0:
                    self.organic_charge_R101 = self.SV_R101_gL
                else:
                    self.organic_charge_R101 = self.SV_R101_gL/self.GlobalTime
            except ZeroDivisionError:
                self.organic_charge_R101 = 0

        else:
            self.mol_sus_int_ini_R101 = self.Csus_ini_R101*self.VR1
            self.SV_R101_gL = self.SV_R101*self.rho
            self.ST_R101_gl = self.ST_R101*self.rho
            self.X_R101 = (self.Csus_ini - self.Csus_ini_R101)/self.Csus_ini
            self.y_gompertz_R101 = (self.V_normal_CH4_acum_V101/self.SV_R101_gL)*self.VR1
            try:
                if self.GlobalTime == 0:
                    self.organic_charge_R101 = self.SV_R101_gL
                else:
                    self.organic_charge_R101 = self.SV_R101_gL/self.GlobalTime
            except ZeroDivisionError:
                self.organic_charge_R101 = 0

            

    def R102_DT (self):
        if self.OperationModo == "Modo1" or self.OperationModo == "Modo2":
            pass

        else:
            self.mol_CH4_R102v = self.DT_Data["mol_CH4_acum_V102"] .tolist()

            if len(self.mol_CH4_R102v)>=2:
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
                self.mol_sus_in_R102 = self.Q_P101*self.Csus_ini_R101*(self.tp/3600)

                self.volatilemass_int_ini_R102 = self.SV_R102*self.rho_R102*self.VR2
                self.volatilemass_in_R102 = self.Q_P101*self.SV_R101*self.rho*(self.tp/3600)

                self.TotalSolids_int_ini_R102 = self.ST_R102*self.rho_R102*self.VR2
                self.TotalSolids_in_R102 = self.Q_P101*self.ST_R101*(self.tp/3600)

                if self.OperationModo == "Modo1" or self.OperationModo == "Modo2":
                    pass

                elif self.OperationModo == "Modo3":
                    self.Csus_ini_R102 = (self.mol_sus_int_ini_R102 + self.mol_sus_in_R102 - self.mol_sus_stoichometricFR_R102)/(self.VR2+(self.Q_P101*(self.tp/3600)))
                    self.SV_R102 = ((self.volatilemass_int_ini_R102 + self.volatilemass_in_R102 - self.volatilemass_stoichometricFR_R102)/(self.VR2+(self.Q_P101*(self.tp/3600))))/self.rho
                    self.ST_R102 = ((self.TotalSolids_int_ini_R102 + self.TotalSolids_in_R102 - self.TotalSolids_stoichometricFR_R102)/(self.VR2+(self.Q_P101*(self.tp/3600))))/self.rho   

                elif self.OperationModo == "Modo4":
                    self.Csus_ini_R102 = (self.mol_sus_int_ini_R102 + self.mol_sus_in_R102 - self.mol_sus_stoichometricFR_R102)/(self.VR2+((self.Q_P102+self.Q_P104)*(self.tp/3600)))
                    self.SV_R102 = ((self.volatilemass_int_ini_R102 + self.volatilemass_in_R102 - self.volatilemass_stoichometricFR_R102)/(self.VR2+((self.Q_P102+self.Q_P104)*(self.tp/3600))))/self.rho
                    self.ST_R102 = ((self.TotalSolids_int_ini_R102 + self.TotalSolids_in_R102 - self.TotalSolids_stoichometricFR_R102)/(self.VR2+((self.Q_P102+self.Q_P104)*(self.tp/3600))))/self.rho 
                    
                elif self.OperationModo == "Modo5":
                    self.Csus_ini_R102 = (self.mol_sus_int_ini_R102 + self.mol_sus_in_R102 - self.mol_sus_stoichometricFR_R102)/(self.VR2+((self.Q_P102+(self.Q_P104-self.Q_P102))*(self.tp/3600)))
                    self.SV_R102 = ((self.volatilemass_int_ini_R102 + self.volatilemass_in_R102 - self.volatilemass_stoichometricFR_R102)/(self.VR2+((self.Q_P102+(self.Q_P104-self.Q_P102))*(self.tp/3600))))/self.rho
                    self.ST_R102 = ((self.TotalSolids_int_ini_R102 + self.TotalSolids_in_R102 - self.TotalSolids_stoichometricFR_R102)/(self.VR2+((self.Q_P102+(self.Q_P104-self.Q_P102))*(self.tp/3600))))/self.rho
                    
                self.mol_sus_int_ini_R102 = self.Csus_ini_R102*self.VR1
                self.SV_R102_gL = self.SV_R102*self.rho
                self.X_R102= (self.mol_sus_in_R102- self.mol_sus_int_ini_R102)/self.mol_sus_in_R102
                self.y_gompertz_R102 = (self.mol_CH4_R102*self.V_mol_CH4/self.SV_R102_gL)*self.VR2
                try:
                    if self.GlobalTime == 0:
                        self.organic_charge_R102 = self.SV_R102_gL
                    else:
                        self.organic_charge_R102 = self.SV_R102_gL/self.GlobalTime
                except ZeroDivisionError:
                    self.organic_charge_R102 = 0
        
            else:
                self.mol_sus_int_ini_R102 = self.Csus_ini_R102*self.VR1
                self.SV_R102_gL = self.SV_R102*self.rho
                self.X_R102= 0
                self.y_gompertz_R102 = (self.V_normal_CH4_acum_V102/self.SV_R102_gL)*self.VR2

                if self.OperationModo == "Modo1" or self.OperationModo == "Modo2":
                    pass
                try:
                    if self.GlobalTime == 0:
                        self.organic_charge_R102 = self.SV_R102_gL
                    else:
                        self.organic_charge_R102 = self.SV_R102_gL/self.GlobalTime
                except ZeroDivisionError:
                    self.organic_charge_R102 = 0
                    
    def Energy_Biogas (self): 
        self.LHV_V101 = self.Thermo.LHV(molCH4 = self.mol_CH4_V101, molCO2 = self.mol_CO2_V101, molH2S = self.mol_H2S_V101, molO2 = self.mol_O2_V101, molH2 = self.mol_H2_V101)
        self.Energy_V101 = self.LHV_V101[1]

        self.LHV_V102 = self.Thermo.LHV(molCH4 = self.mol_CH4_V102, molCO2 = self.mol_CO2_V102, molH2S = self.mol_H2S_V102, molO2 = self.mol_O2_V102, molH2 = self.mol_H2_V102)
        self.Energy_V102 = self.LHV_V102[1]

        self.LHV_V107 = self.Thermo.LHV(molCH4 = self.mol_CH4_V107, molCO2 = self.mol_CO2_V107, molH2S = self.mol_H2S_V107, molO2 = self.mol_O2_V107, molH2 = self.mol_H2_V107)
        self.Energy_V107 = self.LHV_V107[1]
    
    def StorageData (self):
        self.timestamp = datetime.now()
        if self.OperationModo == "Modo1":
            new_row = pd.DataFrame({"timestamp": [self.timestamp],
                                    "Q_P104" : [self.Q_P104],
                                    "Csus_ini" : [self.Csus_ini],
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
                                    "P_V101":[self.PT103],
                                    "P_V102":[self.PT104],
                                    "P_V107":[self.PT105],
                                    "Pacum_V101":[self.Pacum_V101],
                                    "Vnormal_acum_V101":[self.Vnormal_acum_V101],
                                    "mol_CH4_acum_V101":[self.mol_CH4_acum_V101],
                                    "mol_sus_int_ini_R101":[self.mol_sus_int_ini_R101],
                                    "Csus_ini_R101":[self.Csus_ini_R101],
                                    "SV_R101":[self.SV_R101],
                                    "ST_R101":[self.ST_R101],
                                    "yt_R101":[self.y_gompertz_R101]
                                    })
            
        elif self.OperationModo == "Modo2":
            new_row = pd.DataFrame({"timestamp":[self.timestamp],
                                     "Q_P104":[self.Q_P104],
                                     "Csus_ini" : [self.Csus_ini],
                                     "Q_P101":[self.Q_P101],
                                     "Temp_R101":[self.Temp_R101],
                                     "V_normal_V101":[self.V_normal_V101],
                                     "V_normal_CH4_V101":[self.V_normal_CH4_V101],
                                     "V_normal_CO2_V101":[self.V_normal_CO2_V101],
                                     "V_normal_H2S_V101":[self.V_normal_H2S_V101],
                                     "V_normal_O2_V101":[self.V_normal_O2_V101],
                                     "V_normal_H2_V101":[self.V_normal_H2_V101],
                                     "mol_CH4_V101":[self.mol_CH4_V101],
                                     "mol_CO2_V101":[self.mol_CO2_V101],
                                     "mol_H2S_V101":[self.mol_H2S_V101],
                                     "mol_O2_V101":[self.mol_O2_V101],
                                     "mol_H2_V101":[self.mol_H2_V101],
                                     "mol_H2O_V101":[self.mol_H2O_V101],
                                     "P_V101":[self.PT103],
                                     "P_V102":[self.PT104],
                                     "P_V107":[self.PT105],
                                     "Pacum_V101":[self.Pacum_V101],
                                     "Vnormal_acum_V101":[self.Vnormal_acum_V101],
                                     "mol_CH4_acum_V101":[self.mol_CH4_acum_V101],
                                     "mol_sus_int_ini_R101":[self.mol_sus_int_ini_R101],
                                     "Csus_ini_R101":[self.Csus_ini_R101],
                                     "SV_R101":[self.SV_R101],
                                     "ST_R101":[self.ST_R101],
                                     "yt_R101":[self.y_gompertz_R101]
                                    })
            
        elif self.OperationModo == "Modo3":
            new_row = pd.DataFrame({"timestamp":[self.timestamp],
                                     "Q_P104":[self.Q_P104],
                                     "Csus_ini" : [self.Csus_ini],
                                     "Q_P101":[self.Q_P101],
                                     "Temp_R101":[self.Temp_R101], 
                                     "Temp_R102":[self.Temp_R102],
                                     "V_normal_V101":[self.V_normal_V101],
                                     "V_normal_CH4_V101":[self.V_normal_CH4_V101],
                                     "V_normal_CO2_V101":[self.V_normal_CO2_V101],
                                     "V_normal_H2S_V101":[self.V_normal_H2S_V101],
                                     "V_normal_O2_V101":[self.V_normal_O2_V101],
                                     "V_normal_H2_V101":[self.V_normal_H2_V101],
                                     "mol_CH4_V101":[self.mol_CH4_V101],
                                     "mol_CO2_V101":[self.mol_CO2_V101],
                                     "mol_H2S_V101":[self.mol_H2S_V101],
                                     "mol_O2_V101":[self.mol_O2_V101],
                                     "mol_H2_V101":[self.mol_H2_V101],
                                     "mol_H2O_V101":[self.mol_H2O_V101],
                                     "P_V101":[self.PT103],
                                     "P_V102":[self.PT104],
                                     "P_V107":[self.PT105],
                                     "Pacum_V101":[self.Pacum_V101],
                                     "Vnormal_acum_V101":[self.Vnormal_acum_V101],
                                     "mol_CH4_acum_V101":[self.mol_CH4_acum_V101],
                                     "V_normal_V102":[self.V_normal_V102],
                                     "V_normal_CH4_V102":[self.V_normal_CH4_V102],
                                     "V_normal_CO2_V102":[self.V_normal_CO2_V102],
                                     "V_normal_H2S_V102":[self.V_normal_H2S_V102],
                                     "V_normal_O2_V102":[self.V_normal_O2_V102],
                                     "V_normal_H2_V102":[self.V_normal_H2_V102],
                                     "mol_CH4_V102":[self.mol_CH4_V102],
                                     "mol_CO2_V102":[self.mol_CO2_V102],
                                     "mol_H2S_V102":[self.mol_H2S_V102],
                                     "mol_O2_V102":[self.mol_O2_V102],
                                     "mol_H2_V102":[self.mol_H2_V102],
                                     "mol_H2O_V102":[self.mol_H2O_V102],
                                     "Pacum_V102":[self.Pacum_V102],
                                     "Vnormal_acum_V102":[self.Vnormal_acum_V102],
                                     "mol_CH4_acum_V102":[self.mol_CH4_acum_V102],
                                     "mol_sus_int_ini_R101":[self.mol_sus_int_ini_R101],
                                     "Csus_ini_R101":[self.Csus_ini_R101],
                                     "SV_R101":[self.SV_R101],
                                     "ST_R101":[self.ST_R101],
                                     "mol_sus_int_ini_R102":[self.mol_sus_int_ini_R102],
                                     "Csus_ini_R102":[self.Csus_ini_R102],
                                     "SV_R102":[self.SV_R102],
                                     "ST_R102":[self.ST_R102],
                                     "yt_R101":[self.y_gompertz_R101],
                                     "yt_R102":[self.y_gompertz_R102]
                                    })
            
        elif self.OperationModo == "Modo4" or self.OperationModo == "Modo5":
             new_row = pd.DataFrame({"timestamp":[self.timestamp],
                                     "Q_P104":[self.Q_P104],
                                     "Csus_ini" : [self.Csus_ini],
                                     "Q_P101":[self.Q_P101],
                                     "Q_P102":[self.Q_P102],
                                     "Temp_R101":[self.Temp_R101], 
                                     "Temp_R102":[self.Temp_R102],
                                     "V_normal_V101":[self.V_normal_V101],
                                     "V_normal_CH4_V101":[self.V_normal_CH4_V101],
                                     "V_normal_CO2_V101":[self.V_normal_CO2_V101],
                                     "V_normal_H2S_V101":[self.V_normal_H2S_V101],
                                     "V_normal_O2_V101":[self.V_normal_O2_V101],
                                     "V_normal_H2_V101":[self.V_normal_H2_V101],
                                     "mol_CH4_V101":[self.mol_CH4_V101],
                                     "mol_CO2_V101":[self.mol_CO2_V101],
                                     "mol_H2S_V101":[self.mol_H2S_V101],
                                     "mol_O2_V101":[self.mol_O2_V101],
                                     "mol_H2_V101":[self.mol_H2_V101],
                                     "mol_H2O_V101":[self.mol_H2O_V101],
                                     "P_V101":[self.PT103],
                                     "P_V102":[self.PT104],
                                     "P_V107":[self.PT105],
                                     "Pacum_V101":[self.Pacum_V101],
                                     "Vnormal_acum_V101":[self.Vnormal_acum_V101],
                                     "mol_CH4_acum_V101":[self.mol_CH4_acum_V101],
                                     "V_normal_V102":[self.V_normal_V102],
                                     "V_normal_CH4_V102":[self.V_normal_CH4_V102],
                                     "V_normal_CO2_V102":[self.V_normal_CO2_V102],
                                     "V_normal_H2S_V102":[self.V_normal_H2S_V102],
                                     "V_normal_O2_V102":[self.V_normal_O2_V102],
                                     "V_normal_H2_V102":[self.V_normal_H2_V102],
                                     "mol_CH4_V102":[self.mol_CH4_V102],
                                     "mol_CO2_V102":[self.mol_CO2_V102],
                                     "mol_H2S_V102":[self.mol_H2S_V102],
                                     "mol_O2_V102":[self.mol_O2_V102],
                                     "mol_H2_V102":[self.mol_H2_V102],
                                     "mol_H2O_V102":[self.mol_H2O_V102],
                                     "Pacum_V102":[self.Pacum_V102],
                                     "Vnormal_acum_V102":[self.Vnormal_acum_V102],
                                     "mol_CH4_acum_V102":[self.mol_CH4_acum_V102],
                                     "mol_sus_int_ini_R101":[self.mol_sus_int_ini_R101],
                                     "Csus_ini_R101":[self.Csus_ini_R101],
                                     "SV_R101":[self.SV_R101],
                                     "ST_R101":[self.ST_R101],
                                     "mol_sus_int_ini_R102":[self.mol_sus_int_ini_R102],
                                     "Csus_ini_R102":[self.Csus_ini_R102],
                                     "SV_R102":[self.SV_R102],
                                     "ST_R102":[self.ST_R102],
                                     "yt_R101":[self.y_gompertz_R101],
                                     "yt_R102":[self.y_gompertz_R102]
                                    })
        
        new_row_filtered = new_row.dropna(axis=1, how ='all')
        self.DT_Data = self.DT_Data.dropna(axis=1, how='all')
        self.DT_Data = pd.concat([self.DT_Data, new_row_filtered], ignore_index=True)     
        self.GlobalTime = self.GlobalTime + self.tp
       
    


        


        
