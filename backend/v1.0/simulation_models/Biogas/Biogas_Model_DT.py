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

    def __init__(self, VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=30, rho_R101=1000, rho_R102=1000, OperationMode=1):

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
        self.ST_R101 = 0
        self.SV_R101 = 0
        self.rho_R101 = rho_R101
        self.Csus_ini_R101 = 0
        self.Csus_ini_ST_R101 = 0

        #Reactor 102 initial conditions
        self.ST_R102 = 0
        self.SV_R102 = 0
        self.rho_R102 = rho_R102
        self.Csus_ini_R102 = 0
        self.Csus_ini_ST_R102 = 0
        
        #Create DataFrames to storage Data
        self.OperationMode = OperationMode
        if self.OperationMode ==1:
            columns = ["timestamp"
            , "Q_P104"
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
            , "Pacum_V101"
            , "Vnormal_acum_V101"
            , "mol_CH4_acum_V101"
            , "mol_sus_int_ini_R101"
            , "Csus_ini_R101"
            , "SV_R101"
            , "ST_R101"]
            
            
        
        elif self.OperationMode == 2:
            columns = ["timestamp"
            , "Q_P104"
            , "Q_P101"
            , "Temp_R101"
            , "V_normal_V101"
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
            , "Pacum_V101"
            , "Vnormal_acum_V101"
            , "mol_CH4_acum_V101"
            , "mol_sus_int_ini_R101"
            , "Csus_ini_R101"
            , "SV_R101"
            , "ST_R101"]

        elif self.OperationMode == 3:
            columns = ["timestamp"
            , "Q_P104"
            , "Q_P101"
            , "Temp_R101" 
            , "Temp_R102"
            , "V_normal_V101"
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
            , "Pacum_V101"
            , "Vnormal_acum_V101"
            , "mol_CH4_acum_V101"
            , "V_normal_V102"
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
            , "ST_R102"]
        
        elif self.OperationMode == 4 or self.OperationMode == 5:
            columns = ["timestamp"
            , "Q_P104"
            , "Q_P101"
            , "Q_P102"
            , "Temp_R101" 
            , "Temp_R102"
            , "V_normal_V101"
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
            , "Pacum_V101"
            , "Vnormal_acum_V101"
            , "mol_CH4_acum_V101"
            , "V_normal_V102"
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
            , "ST_R102"]

        self.DT_Data = pd.DataFrame(columns= columns)

                      
    def GetValuesFromBiogasPlant (self):
        
        msg = self.InfluxDB.InfluxDBconnection()
        if not msg:
            return {"message":self.influxDB.ERROR_MESSAGE}, 503
        
        query = self.InfluxDB.QueryCreator(measurement = "Planta", type = 1)
        data_biogas = self.InfluxDB.InfluxDBreader(query)
        data_biogas.set_index("_field", inplace = True)

        #Get substrate conditions from plant interface
        self.substrateNumber = data_biogas["_value"]["MNS"]
        self.WaterPorportion = data_biogas["_value"]["MPH"]

        if self.substrateNumber == 1:
            self.substrateproportion1 = data_biogas["_value"]["MP1"]/100
            self.ST1 = data_biogas["_value"]["MST1"]/100
            self.SV1 = data_biogas["_value"]["MSV1"]/100
            self.Cc1 = data_biogas["_value"]["MCc1"]
            self.Ch1 = data_biogas["_value"]["MCh1"]
            self.Co1 = data_biogas["_value"]["MCo1"]
            self.Cn1 = data_biogas["_value"]["MCn1"]
            self.Cs1 = data_biogas["_value"]["MCs1"]
            self.rho1 = data_biogas["_value"]["Md1"]
        
        elif self.substrateNumber == 2:
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
        
        elif self.substrateNumber == 3:
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
        
        elif self.substrateNumber == 4:
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
        self.SE_107 = data_biogas["_value"]["Md4"]
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

        if self.OperationMode == 2:
            #get values for P101
            self.FT_P101 = data_biogas["_value"]["MFTP101"]
            self.TTO_P101 = data_biogas["_value"]["MTTOP101"]
            self.Qset_P101 = data_biogas["_value"]["MQP101"]
            self.SE101 = data_biogas["_value"]["SE101"]
        
        elif self.OperationMode == 3:
            self.SE101 = data_biogas["_value"]["SE101"]
            #Get Values for R102
            self.TE_102A = data_biogas["_value"]["TE102A"]
            self.TE_102B = data_biogas["_value"]["TE102B"]
            self.AT_102 = data_biogas["_value"]["AT102"]
            self.SE_109 = data_biogas["_value"]["SE109"]
            self.LT_102 = data_biogas["_value"]["LT102"]
        
        elif self.OperationMode == 4 or self.OperationMode == 5:
            self.SE101 = data_biogas["_value"]["SE101"]
            self.FT_P102 = data_biogas["_value"]["MFTP102"]
            self.TTO_P102 = data_biogas["_value"]["MTTOP102"]
            self.Qset_P102 = data_biogas["_value"]["MQP102"]
            self.SE102 = data_biogas["_value"]["SE102"]
            #Get Values for R102
            self.TE_102Av = data_biogas["_value"]["TE102A"]
            self.TE_102Bv = data_biogas["_value"]["TE102B"]
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

    def Substrate_conditions (self): 
        
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
        self.Csus_ini_ST = (self.rho*self.ST)/self.MW_sustrato
        self.Csus_fixed = self.Csus_ini_ST - self.Csus_ini

    def Pump104 (self, manual_P104=False, TRH=30, FT_P104=5, TTO_P104=10):    
        
        self.manual_P104 = manual_P104
        
        if  self.manual_P104 == True:
            self.TRH = TRH
            self.FT_P104 = FT_P104
            self.TTO_P104 = TTO_P104
            
            self.TurnOnDailyStep_P104 = 24/self.FT_P104
            
            if self.OperationMode == 1 or self.OperationMode == 2:
                self.Q_daily = self.VR1/self.TRH
            
            elif self.OperationMode == 3 or self.OperationMode == 4 or self.OperationMode == 5:
                self.Q_daily = (self.VR1 + self.VR2)/self.TRH
            
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
            
            self.Q_P104 = self.SE104
            self.TRH = self.TRH
            self.FT_P104 = self.FT_P104
            self.TTO_P104 = self.TTO_P104
            
    
    def Pump101 (self, manual_P101=False, FT_P101=5, TTO_P101=10, Q_P101 = 2.4):
        
        self.manual_P101 = manual_P101
    
        if self.manual_P101 == True:

            if self.OperationMode == 1:
                pass

            elif self.OperationMode == 2:
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

            elif self.OperationMode == 3 or self.OperationMode == 5:
                self.Q_P101 = self.Q_P104

            elif self.OperationMode == 4:
                try:
                    self.Q_P102 = self.Q_P102
                except NameError:
                    self.Q_P102 = 0

                self.Q_P101 = self.Q_P101 + self.Q_P102
                self.FT_P101 = self.FT_P101
                self.TTO_P101 = self.TTO_P101
                self.Qset_P101 = self.Qset_P101

        
        else:

            if self.OperationMode == 1:
                pass
            else:
                self.Q_P101 = self.SE101
    
    def Pump102 (self, manual_P102=False, FT_P102=5, TTO_P102=10, Q_P102 = 2.4):
        self.manual_P102 = manual_P102

        if self.manual_P102 == True:

            if self.OperationMode == 1 or self.OperationMode == 2 or self.OperationMode == 3:
                pass

            if self.OperationMode == 4 or self.OperationMode == 5:
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

            self.Q_P102 = self.SE102
           
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
        self.organic_charge_R101_in = self.SV*self.rho*self.Q_P104*24

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

            self.organic_charge_R101_out = self.SV_R101*self.rho*self.Q_P104*24
           
        else:
            
            self.organic_charge_R101_out = self.SV_R101*self.rho*self.Q_P104*24
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
        
            self.organic_charge_R101_in = self.SV*self.rho*self.Q_P104*24
            self.organic_charge_R101_out = self.SV_R101*self.rho*self.Q_P104*24
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

            print("----------------",self.SV)
            print("----------------", self.SV_R101)
            # self.organic_charge_R101_in = self.SV[-1]*self.rho*self.Q_P104*24
            # self.organic_charge_R101_out = self.SV_R101*self.rho*self.Q_P104*24

            # print("--------------", self.organic_charge_R101_in)
            # print("--------------", self.organic_charge_R101_out)


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

            self.organic_charge_R101_in = self.SV*self.rho*self.Q_P104*24
            self.organic_charge_R101_out = self.SV_R101*self.rho*self.Q_P104*24
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




        


        


        
