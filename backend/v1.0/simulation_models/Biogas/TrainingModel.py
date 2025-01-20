import os
import sys

current_directory = os.getcwd()
current_directory = os.path.join(current_directory, 'v1.0')
print(current_directory)
sys.path.append(current_directory)

from tools import DBManager
import pandas as pd
import numpy as np
from fractions import Fraction
from functools import reduce
from math import gcd

class TrainingBiogasPlant:
    def __init__(self, t_train, ST_ini, SV_ini, V_V101):
        # DB_IP = os.getenv('DB_IP')
        # DB_Port = os.getenv('DB_Port')
        # DB_Bucket = os.getenv('DB_Bucket')
        # DB_Organization = os.getenv('DB_Organization')
        # DB_Token = os.getenv('DB_Token')
        DB_IP = "localhost"
        DB_Port = "8086"
        DB_Organization = "UCO"
        DB_Token = "koJGMnzyGyMV1cI70BKs9TDKP1gEL7OjtcDS96rwSssoGqi-eaUeM6IxY4_eOufdoC8jJlS8IinYhIRhnnxrLg=="
        DB_Bucket = "BiogasPlantSimulator"
        
        self.influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
        self.influxDB.InfluxDBconnection()
        self.t_train = t_train
        
        self.ST_ini = ST_ini    #Initial condition for reactor
        self.SV_ini = SV_ini    #Initial condition for reactor
        #initial concentration inside reactor
        self.Csus_ini_ST = (1000*(self.ST_ini/100))/18.0     #18: molecular weight of water, this is for inoculum
        self.Csus_ini_SV = (1000*(self.SV_ini/100))/18.0     #1000: Standar density of water   
        self.Csus_ini_fixed = self.Csus_ini_ST - self.Csus_ini_SV
       
        #constructive condition for storage biogás 
        self.V_V101 = V_V101
       
    def getData (self):
        #Get data from User input plant plant
        self.query1 = self.influxDB.QueryCreator(measurement="Planta_Biogas", device="interfaz", type=5)
        self.Datainterfaz = pd.concat(self.influxDB.InfluxDBreader(query = self.query1), ignore_index=True)
        self.Datainterfaz.set_index("_field", inplace = True)
        
        #Get Asynchronous and synchronous Data
        self.query2 = self.influxDB.QueryCreator(measurement="Planta_Biogas", train_time=str(self.t_train), type=4)
        DataPlant = pd.concat(self.influxDB.InfluxDBreader(query = self.query2), ignore_index=True)
        DataPlant.set_index("_field", inplace = True)
        
        self.Operation_mode = self.Datainterfaz["_value"]["ciclo"]
        
        #function to verify the lenght of synchronous vector
        def SameDimension(V1, V2):   #V1 is always pressure in the tank 
            try:
                if len(V1) != len(V2):
                    print("lengths not equal... normalice the variables")
                    if len(V2)>len(V1):
                        V2 = V2[:len(V1)]
                        return V2
                    else:
                        V2 = V2 + [np.nan] * (len(V1)-len(V2))
                        return V2
                else:
                    return V2
            except TypeError as e:
                return V2
            
        
        #Function for asynchronous data align with the synchronous Data
        def AlignAsynchronous (variable, SyncDBRaw, SyncDB,  current_time):
            if isinstance(current_time, pd.Series):
                current_time = current_time.iloc[-1]
            else:
                current_time = current_time
            if f"{variable}" in SyncDBRaw.index:
                Var = SyncDBRaw["_value"][f"{variable}"]
                time_Var = SyncDBRaw["_time"][f'{variable}']
            else:
                Var = 0
                time_Var = current_time
            #Verify if there is a singular variable in DB
            if np.isscalar(Var):
                AsyncDB = pd.DataFrame({
                    "time_var":[time_Var],
                    f"{variable}": [Var]
                })
            else:
                AsyncDB = pd.DataFrame({
                    "time_var":time_Var,
                    f"{variable}": Var
                })      
            SyncDB["format_time"] = pd.to_datetime(SyncDB["format_time"])
            
            SyncDB = pd.merge_asof(SyncDB.sort_values('format_time'), 
                            AsyncDB.sort_values('time_var'),
                            left_on='format_time', 
                            right_on='time_var', 
                            direction='forward')
            SyncDB[f"{variable}"] = SyncDB[f"{variable}"].ffill()
            SyncDB = SyncDB.drop(columns=["time_var"])
            return SyncDB
        
        def normaliceTime (time):
            #check the lenght of the vector
            try: 
                if len(time) > 1:
                    time_norm = []
                    for i in range (len(time)):
                        time_diff = time.iloc[i] - time.iloc[0]
                        time_diff = time_diff.total_seconds()/60
                        time_norm.append(time_diff)
                else: 
                    time_norm = []
                    time_norm.append(0)
            except TypeError as e:
                time_norm = []
                time_norm.append(0)
            return time_norm
        
        #Organice data with the same lenght according with operation Mode
        if self.Operation_mode == 1:
            # ----- Synchronous Data
            #V101
            time = DataPlant["_time"]["PT-103"]
            time = pd.to_datetime(time)
            P_V101 = DataPlant["_value"]["PT-103"]
            T_V101 = DataPlant["_value"]["TT-103"]
            rh_V101 = DataPlant["_value"]["AT-103B"]        #rh: relative humidity
            x_CH4_V101 = DataPlant["_value"]["AT-103A-CH4"]
            x_CO2_V101 = DataPlant["_value"]["AT-103A-CO2"]
            x_O2_V101 = DataPlant["_value"]["AT-103A-O2"]
            x_H2S_V101 = DataPlant["_value"]["AT-103A-H2S"]
            x_H2_V101 = DataPlant["_value"]["AT-103A-H2"]
            
            #R101
            PH_R101 = DataPlant["_value"]["AT-101"]        
            L_R101 = DataPlant["_value"]["LT-101"]       #L: level
            P_R101 = DataPlant["_value"]["PT-101"]
            T1_R101 =  DataPlant["_value"]["TE-101A"]
            T2_R101 = DataPlant["_value"]["TE-101B"]
            Tprom_R101 = DataPlant["_value"]["TE-R101"]  
            
            
            time_norm = normaliceTime(time = time)
            
            #Variable for V101
            TT_V101 = SameDimension(P_V101, T_V101)
            rh_V101 = SameDimension(P_V101, rh_V101)
            x_CH4_V101 = SameDimension(P_V101, x_CH4_V101)
            x_CO2_V101 = SameDimension(P_V101, x_CO2_V101)
            x_O2_V101 = SameDimension(P_V101, x_O2_V101)
            x_H2S_V101 = SameDimension(P_V101, x_H2S_V101)
            x_H2_V101 = SameDimension(P_V101, x_H2_V101)
            
            #Variables for R101
            T1_R101 = SameDimension(P_V101, T1_R101)
            T2_R101 = SameDimension(P_V101, T2_R101)
            Tprom_R101 = SameDimension(P_V101, Tprom_R101)
            PH_R101 = SameDimension(P_V101, PH_R101)
            L_R101 = SameDimension(P_V101, L_R101)
            P_R101 = SameDimension(P_V101, P_R101)   
                                         
            self.DataPlant = pd.DataFrame({
                "format_time":time,
                "time": time_norm,
                "P_V101":P_V101.tolist(),
                "T_V101":TT_V101.tolist(),
                "rh_V101": rh_V101.tolist(),
                "x_CH4_V101": x_CH4_V101.tolist(),
                "x_CO2_V101": x_CO2_V101.tolist(),
                "x_O2_V101": x_O2_V101.tolist(),
                "x_H2S_V101": x_H2S_V101.tolist(),
                "x_H2_V101": x_H2_V101.tolist(),
                "T1_R101": T1_R101.tolist(),
                "T2_R101": T2_R101.tolist(),
                "Tprom_R101": Tprom_R101.tolist(),
                "PH_R101": PH_R101.tolist(),
                "L_R101": L_R101.tolist(),
                "P_R101": P_R101.tolist()             
            })
        
            #### ----Asynchronous Data
            # Pump 104
            self.DataPlant = AlignAsynchronous(variable = "FE-104", SyncDBRaw =  DataPlant, SyncDB = self.DataPlant, current_time = time)
            # Mixing R101
            self.DataPlant = AlignAsynchronous(variable = "SE-108", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
        
        elif self.Operation_mode == 2:
            # ----- Synchronous Data
            #V101
            time = DataPlant["_time"]["PT-103"]
            time = pd.to_datetime(time)
            P_V101 = DataPlant["_value"]["PT-103"]
            T_V101 = DataPlant["_value"]["TT-103"]
            rh_V101 = DataPlant["_value"]["AT-103B"]        #rh: relative humidity
            x_CH4_V101 = DataPlant["_value"]["AT-103A-CH4"]
            x_CO2_V101 = DataPlant["_value"]["AT-103A-CO2"]
            x_O2_V101 = DataPlant["_value"]["AT-103A-O2"]
            x_H2S_V101 = DataPlant["_value"]["AT-103A-H2S"]
            x_H2_V101 = DataPlant["_value"]["AT-103A-H2"]
            
            #R101
            PH_R101 = DataPlant["_value"]["AT-101"]        
            L_R101 = DataPlant["_value"]["LT-101"]       #L: level
            P_R101 = DataPlant["_value"]["PT-101"]
            T1_R101 =  DataPlant["_value"]["TE-101A"]
            T2_R101 = DataPlant["_value"]["TE-101B"]
            Tprom_R101 = DataPlant["_value"]["TE-R101"] 
            
            time_norm = normaliceTime(time = time)
            
            #Variable for V101
            TT_V101 = SameDimension(P_V101, T_V101)
            rh_V101 = SameDimension(P_V101, rh_V101)
            x_CH4_V101 = SameDimension(P_V101, x_CH4_V101)
            x_CO2_V101 = SameDimension(P_V101, x_CO2_V101)
            x_O2_V101 = SameDimension(P_V101, x_O2_V101)
            x_H2S_V101 = SameDimension(P_V101, x_H2S_V101)
            x_H2_V101 = SameDimension(P_V101, x_H2_V101)
            
            #Variables for R101
            T1_R101 = SameDimension(P_V101, T1_R101)
            T2_R101 = SameDimension(P_V101, T2_R101)
            Tprom_R101 = SameDimension(P_V101, Tprom_R101)
            PH_R101 = SameDimension(P_V101, PH_R101)
            L_R101 = SameDimension(P_V101, L_R101)
            P_R101 = SameDimension(P_V101, P_R101)   
                                         
            self.DataPlant = pd.DataFrame({
                "format_time":time,
                "time": time_norm,
                "P_V101":P_V101.tolist(),
                "T_V101":TT_V101.tolist(),
                "rh_V101": rh_V101.tolist(),
                "x_CH4_V101": x_CH4_V101.tolist(),
                "x_CO2_V101": x_CO2_V101.tolist(),
                "x_O2_V101": x_O2_V101.tolist(),
                "x_H2S_V101": x_H2S_V101.tolist(),
                "x_H2_V101": x_H2_V101.tolist(),
                "T1_R101": T1_R101.tolist(),
                "T2_R101": T2_R101.tolist(),
                "Tprom_R101": Tprom_R101.tolist(),
                "PH_R101": PH_R101.tolist(),
                "L_R101": L_R101.tolist(),
                "P_R101": P_R101.tolist()             
            })
        
            #### ----Asynchronous Data
            # Pump 104
            self.DataPlant = AlignAsynchronous(variable = "FE-104", SyncDBRaw =  DataPlant, SyncDB = self.DataPlant, current_time = time)
            # Mixing R101
            self.DataPlant = AlignAsynchronous(variable = "SE-108", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
            # Pump 101
            self.DataPlant = AlignAsynchronous(variable = "P-101", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
            
            
            
        
    def LimitReagentCalculation(self):
        self.SN = self.Datainterfaz["_value"]["MNS"]    #SN: substrate number
        #Water proportion
        self.MPH = self.Datainterfaz["_value"]["MPH"]    #MPH: Water proportion in the mix
        
        if self.SN  == 4:    
            #Substrate 1 Characterization
            self.MST1 = self.Datainterfaz["_value"]["ST1"]   #ST1: Substrate 1 name
            self.MP1 = self.Datainterfaz["_value"]["MP1"]    #MP1: substrate 1 proportion in mix
            self.ST1 = self.Datainterfaz["_value"]["MST1"]   #MST1: Total solids of substrate 1
            self.SV1 = self.Datainterfaz["_value"]["MSV1"]   #MSV1: Volatile solids of substrate 1
            self.Cc1 = self.Datainterfaz["_value"]["MCc1"]   #MCc1: Carbon concentration substrate 1
            self.Ch1 = self.Datainterfaz["_value"]["MCh1"]   #MCh1: hydrogen concentration substrate 1 
            self.Co1 = self.Datainterfaz["_value"]["MCo1"]   #MCo1: oxygen concentration substrate 1
            self.Cn1 = self.Datainterfaz["_value"]["MCn1"]   #MCh1: nytrogen concentration substrate 1
            self.Cs1 = self.Datainterfaz["_value"]["MCs1"]   #MCh1: sulfur concentration substrate 1
            self.rho1 = self.Datainterfaz["_value"]["Md1"]   #Md1: substrate density
            
            #Substrate 2 Characterization
            self.MST2 = self.Datainterfaz["_value"]["ST2"]   #ST2: Substrate 2 name
            self.MP2 = self.Datainterfaz["_value"]["MP2"]    #MP2: substrate 2 proportion in mix
            self.ST2 = self.Datainterfaz["_value"]["MST2"]   #MST2: Total solids of substrate 2
            self.SV2 = self.Datainterfaz["_value"]["MSV2"]   #MSV2: Volatile solids of substrate 2
            self.Cc2 = self.Datainterfaz["_value"]["MCc2"]   #MCc2: Carbon concentration substrate 2
            self.Ch2 = self.Datainterfaz["_value"]["MCh2"]   #MCh2: hydrogen concentration substrate 2 
            self.Co2 = self.Datainterfaz["_value"]["MCo2"]   #MCo2: oxygen concentration substrate 2
            self.Cn2 = self.Datainterfaz["_value"]["MCn2"]   #MCh2: nytrogen concentration substrate 2
            self.Cs2 = self.Datainterfaz["_value"]["MCs2"]   #MCh2: sulfur concentration substrate 2
            self.rho2 = self.Datainterfaz["_value"]["Md2"]   #Md2: substrate density
            
            #Substrate 3 Characterization
            self.MST3 = self.Datainterfaz["_value"]["ST3"]   #ST3: Substrate 3 name
            self.MP3 = self.Datainterfaz["_value"]["MP3"]    #MP3: substrate 3 proportion in mix
            self.ST3 = self.Datainterfaz["_value"]["MST3"]   #MST3: Total solids of substrate 3
            self.SV3 = self.Datainterfaz["_value"]["MSV3"]   #MSV3: Volatile solids of substrate 3
            self.Cc3 = self.Datainterfaz["_value"]["MCc3"]   #MCc3: Carbon concentration substrate 3
            self.Ch3 = self.Datainterfaz["_value"]["MCh3"]   #MCh3: hydrogen concentration substrate 3 
            self.Co3 = self.Datainterfaz["_value"]["MCo3"]   #MCo3: oxygen concentration substrate 3
            self.Cn3 = self.Datainterfaz["_value"]["MCn3"]   #MCh3: nytrogen concentration substrate 3
            self.Cs3 = self.Datainterfaz["_value"]["MCs3"]   #MCh3: sulfur concentration substrate 3
            self.rho3 = self.Datainterfaz["_value"]["Md3"]   #Md3: substrate density
            
            #Substrate 4 Characterization
            self.MST4 = self.Datainterfaz["_value"]["ST4"]   #ST4: Substrate 4 name
            self.MP4 = self.Datainterfaz["_value"]["MP4"]    #MP4: substrate 4 proportion in mix
            self.ST4 = self.Datainterfaz["_value"]["MST4"]   #MST4: Total solids of substrate 4
            self.SV4 = self.Datainterfaz["_value"]["MSV4"]   #MSV4: Volatile solids of substrate 4
            self.Cc4 = self.Datainterfaz["_value"]["MCc4"]   #MCc4: Carbon concentration substrate 4
            self.Ch4 = self.Datainterfaz["_value"]["MCh4"]   #MCh4: hydrogen concentration substrate 4 
            self.Co4 = self.Datainterfaz["_value"]["MCo4"]   #MCo4: oxygen concentration substrate 4
            self.Cn4 = self.Datainterfaz["_value"]["MCn4"]   #MCh4: nytrogen concentration substrate 4
            self.Cs4 = self.Datainterfaz["_value"]["MCs4"]   #MCh4: sulfur concentration substrate 4
            self.rho4 = self.Datainterfaz["_value"]["Md4"]   #Md4: substrate density
            
            #Proximate analysis for mixture
            self.ST = (self.ST1*self.MP1 + self.ST2*self.MP2 + self.ST3*self.MP3 + self.ST4*self.MP4)/100
            self.SV = (self.SV1*self.MP1 + self.SV2*self.MP2 + self.SV3*self.MP3 + self.SV4*self.MP4)/100
            self.rho = (self.rho1*self.MP1 + self.rho2*self.MP2 + self.rho3*self.MP3 + self.rho4*self.MP4 + 1000*self.MPH)/100
            
            gCc1 = self.Cc1 * self.MP1 * self.ST1; gCc2 = self.Cc2 * self.MP2 * self.ST2; gCc3 = self.Cc3 * self.MP3 * self.ST3; gCc4 = self.Cc4 * self.MP4 * self.ST4    #Carbon content
            gCh1 = self.Ch1 * self.MP1 * self.ST1; gCh2 = self.Ch2 * self.MP2 * self.ST2; gCh3 = self.Ch3 * self.MP3 * self.ST3; gCh4 = self.Ch4 * self.MP4 * self.ST4    #hydrogen content
            gCo1 = self.Co1 * self.MP1 * self.ST1; gCo2 = self.Co2 * self.MP2 * self.ST2; gCo3 = self.Co3 * self.MP3 * self.ST3; gCo4 = self.Co4 * self.MP4 * self.ST4    #oxygen content
            gCn1 = self.Cn1 * self.MP1 * self.ST1; gCn2 = self.Cn2 * self.MP2 * self.ST2; gCn3 = self.Cn3 * self.MP3 * self.ST3; gCn4 = self.Cn4 * self.MP4 * self.ST4    #nitrogen content
            gCs1 = self.Cs1 * self.MP1 * self.ST1; gCs2 = self.Cs2 * self.MP2 * self.ST2; gCs3 = self.Cs3 * self.MP3 * self.ST3; gCs4 = self.Cs4 * self.MP4 * self.ST4    #sulfur content
            
            #Elemental analysis for mixture
            self.Cc = ((gCc1 + gCc2 + gCc3 + gCc4) / self.ST)/100
            self.Ch = ((gCh1 + gCh2 + gCh3 + gCh4) / self.ST)/100
            self.Co = ((gCo1 + gCo2 + gCo3 + gCo4) / self.ST)/100
            self.Cn = ((gCn1 + gCn2 + gCn3 + gCn4) / self.ST)/100
            self.Cs = ((gCs1 + gCs2 + gCs3 + gCs4) / self.ST)/100
                       
        elif self.SN  == 3:
            #Substrate 1 Characterization
            self.MST1 = self.Datainterfaz["_value"]["ST1"]   #ST1: Substrate 1 name
            self.MP1 = self.Datainterfaz["_value"]["MP1"]    #MP1: substrate 1 proportion in mix
            self.ST1 = self.Datainterfaz["_value"]["MST1"]   #MST1: Total solids of substrate 1
            self.SV1 = self.Datainterfaz["_value"]["MSV1"]   #MSV1: Volatile solids of substrate 1
            self.Cc1 = self.Datainterfaz["_value"]["MCc1"]   #MCc1: Carbon concentration substrate 1
            self.Ch1 = self.Datainterfaz["_value"]["MCh1"]   #MCh1: hydrogen concentration substrate 1 
            self.Co1 = self.Datainterfaz["_value"]["MCo1"]   #MCo1: oxygen concentration substrate 1
            self.Cn1 = self.Datainterfaz["_value"]["MCn1"]   #MCh1: nytrogen concentration substrate 1
            self.Cs1 = self.Datainterfaz["_value"]["MCs1"]   #MCh1: sulfur concentration substrate 1
            self.rho1 = self.Datainterfaz["_value"]["Md1"]   #Md1: substrate density
            
            #Substrate 2 Characterization
            self.MST2 = self.Datainterfaz["_value"]["ST2"]   #ST2: Substrate 2 name
            self.MP2 = self.Datainterfaz["_value"]["MP2"]    #MP2: substrate 2 proportion in mix
            self.ST2 = self.Datainterfaz["_value"]["MST2"]   #MST2: Total solids of substrate 2
            self.SV2 = self.Datainterfaz["_value"]["MSV2"]   #MSV2: Volatile solids of substrate 2
            self.Cc2 = self.Datainterfaz["_value"]["MCc2"]   #MCc2: Carbon concentration substrate 2
            self.Ch2 = self.Datainterfaz["_value"]["MCh2"]   #MCh2: hydrogen concentration substrate 2 
            self.Co2 = self.Datainterfaz["_value"]["MCo2"]   #MCo2: oxygen concentration substrate 2
            self.Cn2 = self.Datainterfaz["_value"]["MCn2"]   #MCh2: nytrogen concentration substrate 2
            self.Cs2 = self.Datainterfaz["_value"]["MCs2"]   #MCh2: sulfur concentration substrate 2
            self.rho2 = self.Datainterfaz["_value"]["Md2"]   #Md2: substrate density
            
            #Substrate 3 Characterization
            self.MST3 = self.Datainterfaz["_value"]["ST3"]   #ST3: Substrate 3 name
            self.MP3 = self.Datainterfaz["_value"]["MP3"]    #MP3: substrate 3 proportion in mix
            self.ST3 = self.Datainterfaz["_value"]["MST3"]   #MST3: Total solids of substrate 3
            self.SV3 = self.Datainterfaz["_value"]["MSV3"]   #MSV3: Volatile solids of substrate 3
            self.Cc3 = self.Datainterfaz["_value"]["MCc3"]   #MCc3: Carbon concentration substrate 3
            self.Ch3 = self.Datainterfaz["_value"]["MCh3"]   #MCh3: hydrogen concentration substrate 3 
            self.Co3 = self.Datainterfaz["_value"]["MCo3"]   #MCo3: oxygen concentration substrate 3
            self.Cn3 = self.Datainterfaz["_value"]["MCn3"]   #MCh3: nytrogen concentration substrate 3
            self.Cs3 = self.Datainterfaz["_value"]["MCs3"]   #MCh3: sulfur concentration substrate 3
            self.rho3 = self.Datainterfaz["_value"]["Md3"]   #Md3: substrate density
                        
            #Proximate analysis for mixture
            self.ST = (self.ST1*self.MP1 + self.ST2*self.MP2 + self.ST3*self.MP3)/100
            self.SV = (self.SV1*self.MP1 + self.SV2*self.MP2 + self.SV3*self.MP3)/100
            self.rho = (self.rho1*self.MP1 + self.rho2*self.MP2 + self.rho3*self.MP3 + 1000*self.MPH)/100
            
            gCc1 = self.Cc1 * self.MP1 * self.ST1; gCc2 = self.Cc2 * self.MP2 * self.ST2; gCc3 = self.Cc3 * self.MP3 * self.ST3    #Carbon content
            gCh1 = self.Ch1 * self.MP1 * self.ST1; gCh2 = self.Ch2 * self.MP2 * self.ST2; gCh3 = self.Ch3 * self.MP3 * self.ST3    #hydrogen content
            gCo1 = self.Co1 * self.MP1 * self.ST1; gCo2 = self.Co2 * self.MP2 * self.ST2; gCo3 = self.Co3 * self.MP3 * self.ST3    #oxygen content
            gCn1 = self.Cn1 * self.MP1 * self.ST1; gCn2 = self.Cn2 * self.MP2 * self.ST2; gCn3 = self.Cn3 * self.MP3 * self.ST3    #nitrogen content
            gCs1 = self.Cs1 * self.MP1 * self.ST1; gCs2 = self.Cs2 * self.MP2 * self.ST2; gCs3 = self.Cs3 * self.MP3 * self.ST3    #sulfur content
            
            #Elemental analysis for mixture
            self.Cc = ((gCc1 + gCc2 + gCc3) / self.ST)/100
            self.Ch = ((gCh1 + gCh2 + gCh3) / self.ST)/100
            self.Co = ((gCo1 + gCo2 + gCo3) / self.ST)/100
            self.Cn = ((gCn1 + gCn2 + gCn3) / self.ST)/100
            self.Cs = ((gCs1 + gCs2 + gCs3) / self.ST)/100
        
        elif self.SN  == 2:
            #Substrate 1 Characterization
            self.MST1 = self.Datainterfaz["_value"]["ST1"]   #ST1: Substrate 1 name
            self.MP1 = self.Datainterfaz["_value"]["MP1"]    #MP1: substrate 1 proportion in mix
            self.ST1 = self.Datainterfaz["_value"]["MST1"]   #MST1: Total solids of substrate 1
            self.SV1 = self.Datainterfaz["_value"]["MSV1"]   #MSV1: Volatile solids of substrate 1
            self.Cc1 = self.Datainterfaz["_value"]["MCc1"]   #MCc1: Carbon concentration substrate 1
            self.Ch1 = self.Datainterfaz["_value"]["MCh1"]   #MCh1: hydrogen concentration substrate 1 
            self.Co1 = self.Datainterfaz["_value"]["MCo1"]   #MCo1: oxygen concentration substrate 1
            self.Cn1 = self.Datainterfaz["_value"]["MCn1"]   #MCh1: nytrogen concentration substrate 1
            self.Cs1 = self.Datainterfaz["_value"]["MCs1"]   #MCh1: sulfur concentration substrate 1
            self.rho1 = self.Datainterfaz["_value"]["Md1"]   #Md1: substrate density
            
            #Substrate 2 Characterization
            self.MST2 = self.Datainterfaz["_value"]["ST2"]   #ST2: Substrate 2 name
            self.MP2 = self.Datainterfaz["_value"]["MP2"]    #MP2: substrate 2 proportion in mix
            self.ST2 = self.Datainterfaz["_value"]["MST2"]   #MST2: Total solids of substrate 2
            self.SV2 = self.Datainterfaz["_value"]["MSV2"]   #MSV2: Volatile solids of substrate 2
            self.Cc2 = self.Datainterfaz["_value"]["MCc2"]   #MCc2: Carbon concentration substrate 2
            self.Ch2 = self.Datainterfaz["_value"]["MCh2"]   #MCh2: hydrogen concentration substrate 2 
            self.Co2 = self.Datainterfaz["_value"]["MCo2"]   #MCo2: oxygen concentration substrate 2
            self.Cn2 = self.Datainterfaz["_value"]["MCn2"]   #MCh2: nytrogen concentration substrate 2
            self.Cs2 = self.Datainterfaz["_value"]["MCs2"]   #MCh2: sulfur concentration substrate 2
            self.rho2 = self.Datainterfaz["_value"]["Md2"]   #Md2: substrate density
                                    
            #Proximate analysis for mixture
            self.ST = (self.ST1*self.MP1 + self.ST2*self.MP2 )/100
            self.SV = (self.SV1*self.MP1 + self.SV2*self.MP2 )/100
            self.rho = (self.rho1*self.MP1 + self.rho2*self.MP2 + 1000*self.MPH)/100
            
            gCh1 = self.Ch1 * self.MP1 * self.ST1; gCh2 = self.Ch2 * self.MP2 * self.ST2    #hydrogen content
            gCc1 = self.Cc1 * self.MP1 * self.ST1; gCc2 = self.Cc2 * self.MP2 * self.ST2    #Carbon content
            gCo1 = self.Co1 * self.MP1 * self.ST1; gCo2 = self.Co2 * self.MP2 * self.ST2    #oxygen content
            gCn1 = self.Cn1 * self.MP1 * self.ST1; gCn2 = self.Cn2 * self.MP2 * self.ST2    #nitrogen content
            gCs1 = self.Cs1 * self.MP1 * self.ST1; gCs2 = self.Cs2 * self.MP2 * self.ST2    #sulfur content
            
            #Elemental analysis for mixture
            self.Cc = ((gCc1 + gCc2) / self.ST)/100
            self.Ch = ((gCh1 + gCh2) / self.ST)/100
            self.Co = ((gCo1 + gCo2) / self.ST)/100
            self.Cn = ((gCn1 + gCn2) / self.ST)/100
            self.Cs = ((gCs1 + gCs2) / self.ST)/100
        
        elif self.SN  == 1:
            #Substrate 1 Characterization
            self.MST1 = self.Datainterfaz["_value"]["ST1"]   #ST1: Substrate 1 name
            self.MP1 = self.Datainterfaz["_value"]["MP1"]    #MP1: substrate 1 proportion in mix
            self.ST1 = self.Datainterfaz["_value"]["MST1"]   #MST1: Total solids of substrate 1
            self.SV1 = self.Datainterfaz["_value"]["MSV1"]   #MSV1: Volatile solids of substrate 1
            self.Cc1 = self.Datainterfaz["_value"]["MCc1"]   #MCc1: Carbon concentration substrate 1
            self.Ch1 = self.Datainterfaz["_value"]["MCh1"]   #MCh1: hydrogen concentration substrate 1 
            self.Co1 = self.Datainterfaz["_value"]["MCo1"]   #MCo1: oxygen concentration substrate 1
            self.Cn1 = self.Datainterfaz["_value"]["MCn1"]   #MCh1: nytrogen concentration substrate 1
            self.Cs1 = self.Datainterfaz["_value"]["MCs1"]   #MCh1: sulfur concentration substrate 1
            self.rho1 = self.Datainterfaz["_value"]["Md1"]   #Md1: substrate density
                                                           
            #Proximate analysis for mixture
            self.ST = (self.ST1*self.MP1 )/100
            self.SV = (self.SV1*self.MP1 )/100
            self.rho = (self.rho1*self.MP1 + 1000*self.MPH)/100
            
            gCh1 = self.Ch1 * self.MP1 * self.ST1   #hydrogen content
            gCc1 = self.Cc1 * self.MP1 * self.ST1   #Carbon content
            gCo1 = self.Co1 * self.MP1 * self.ST1   #oxygen content
            gCn1 = self.Cn1 * self.MP1 * self.ST1   #nitrogen content
            gCs1 = self.Cs1 * self.MP1 * self.ST1   #sulfur content
            
            #Elemental analysis for mixture
            self.Cc = ((gCc1) / self.ST)/100
            self.Ch = ((gCh1) / self.ST)/100
            self.Co = ((gCo1) / self.ST)/100
            self.Cn = ((gCn1) / self.ST)/100
            self.Cs = ((gCs1) / self.ST)/100
        
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
        self.subindex = [int(num * common_denominator) for num in numbers]

        self.n = self.subindex[0]
        self.a = self.subindex[1]
        self.b = self.subindex[2]
        self.c = self.subindex[3]
        self.d = self.subindex[4]
        
        self.s_H2O = self.n-(self.a/4)-(self.b/2)+(3/4)*c+(self.d/2)
        self.s_CH4 = (self.n/2)+(self.a/8)-(self.b/4)-(3/8)*self.c-(self.d/4)
        self.s_CO2 = (self.n/2)-(self.a/8)+(self.b/4)+(3/8)*self.c-(self.d/4)
        self.s_NH3 = self.c
        self.s_H2S = self.d 
        
        #sustrate
        self.MW_sustrato = self.n*12.01 + self.a*1.01 + self.b*16 + self.c*14 + self.d*32
        self.Cst_sus = (self.rho*(self.ST/100))/self.MW_sustrato
        self.Csv_sus = (self.rho*(self.SV/100))/self.MW_sustrato
    
    # def StochoimetricExpenditure(self):
    #     
    #     print(time)
              
#This will be the way to call method from API
Training = TrainingBiogasPlant(ST_ini = 2, SV_ini = 1.5, t_train=60, V_V101=15)
Training.getData()
Training.LimitReagentCalculation()
print(Training.DataPlant)








        