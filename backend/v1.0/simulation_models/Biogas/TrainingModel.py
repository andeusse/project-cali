import os
import sys
import time

# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))  

# Set the working directory to the correct folder
project_root = os.path.abspath(os.path.join(script_dir, "../../.."))  # Adjust based on folder structure
v1_0_path = os.path.join(project_root, "v1.0")

# Change working directory
os.chdir(v1_0_path)  
sys.path.insert(0, v1_0_path)  # Ensure it is the first in sys.path

print(f"Running script in: {os.getcwd()}")
print(f"Python path: {sys.path}")

# current_directory = os.getcwd()
# current_directory = os.path.join(current_directory, "v1.0")
# print(current_directory)
# sys.path.append(current_directory)

# print(f"Current Working Directory: {os.getcwd()}")

from tools import DBManager
import pandas as pd
import numpy as np
from fractions import Fraction
from functools import reduce
from math import gcd
from scipy.integrate import odeint
from scipy.optimize import minimize
import statistics as st

class TrainingBiogasPlant:
    def __init__(self, t_train, ST_ini_R101, SV_ini_R101, Volume_V101 = 15, ST_ini_R102 = 2, SV_ini_R102 = 1.5, Volume_V102 = 35, Volume_V107 = 35):
        # DB_IP = os.getenv('DB_IP')
        # DB_Port = os.getenv('DB_Port')
        # DB_Bucket = os.getenv('DB_Bucket')
        # DB_Organization = os.getenv('DB_Organization')
        # DB_Token = os.getenv('DB_Token')
        ## Universidad Santiago De Cali servidor
        # DB_IP = 'localhost'
        # DB_Port = '8086'
        # DB_Bucket = 'Laboratorio_Energias'
        # DB_Organization = 'USC'
        # DB_Token = '4pJB_298afu0WKjKBtPESjnUxvpJV0PODWBNMGzeeU_ahg1P4H3Bg5KOfwI2A9LXm2BQwaQR_un792HXy3bsvg=='
        ## Computador personal UCO
        DB_IP = 'localhost'
        DB_Port = '8086'
        DB_Bucket = 'BiogasPlantSimulator'
        DB_Organization = 'UCO'
        DB_Token = 'PdISKZ9gcighknh3X66cqwB1FvOexgDh7KUHKlvWvuLyw3UZZGBd1fGBtZg3IBEkKZmcknzOtYBwmEpJzJl6GQ=='
        
        self.influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
        self.influxDB.InfluxDBconnection()
        self.t_train = t_train
        
        #------Initial conditions for R101
        self.ST_ini_R101 = ST_ini_R101    #Initial condition for reactor
        self.SV_ini_R101 = SV_ini_R101         #Initial condition for reactor
        #initial concentration inside reactor 101
        self.Csus_ini_ST_R101 = (1000*(self.ST_ini_R101/100))/18.0     #18: molecular weight of water, this is for inoculum Units: mol/L
        self.Csus_ini_SV_R101 = (1000*(self.SV_ini_R101/100))/18.0     #1000: Standar density of water   Units: mol/L - kmol/m3
        self.Csus_ini_fixed_R101 = self.Csus_ini_ST_R101 - self.Csus_ini_SV_R101
                   
        #initial and constructive conditions for V101
        self.Pi_V101 = 0          #Is the biggest pressure in V101 before pressure in V101 drop
        self.Ptransfer_V101_to_V102 = 0    #Initially the pressure transfer to V102 is 0
        self.Volume_V101 = Volume_V101     #Volume of the tank in Liters
        
        #-------Initial conditions for R102
        self.ST_ini_R102 = ST_ini_R102    #Initial condition for reactor
        self.SV_ini_R102 = SV_ini_R102
        #initial concentration inside reactor 102
        self.Csus_ini_ST_R102 = (1000*(self.ST_ini_R102/100))/18.0     ##18: molecular weight of water, this is for inoculum Units: mol/L
        self.Csus_ini_SV_R102 = (1000*(self.SV_ini_R102/100))/18.0     #1000: Standar density of water   Units: mol/L - kmol/m3
        self.Csus_ini_fixed_R102 = self.Csus_ini_ST_R102 - self.Csus_ini_SV_R102
        
        #initial and constructive conditions for V102
        self.Pi_V102 = 0                   #Is the biggest pressure in V102 before pressure in V102 drop
        self.Volume_V102 = Volume_V102     #Volume of the tank in Liters

        #Initial and constructive conditions for V107
        self.Pi_V107 = 0                   #Is the biggest pressure in V107 before pressure in V107 drop  
        self.Volume_V107 = Volume_V107     #Volume of the tank in liters  
        
        #Initial values for Arrhenius and ADM1
        self.K_mean_R101 = 1, self.Ea_mean_R101 = 1
        self.K_mean_R102 = 1, self.Ea_mean_R102 = 1
        
        #Initial values for Gompertz
        self.ym_R101 = 1, self.U_R101 = 1, self.L_R101 = 1
        self.ym_R102 = 1, self.U_R102 = 1, self.L_R102 = 1
        
        #Model train time for gompertz
        self.total_time = 0
        self.timeGompertz = []
        self.tp = 8               #min
        
    def getData (self):
        #Get data from User input plant plant
        self.query1 = self.influxDB.QueryCreator(measurement="Planta_Biogas", device="interfaz", type=5)
        self.Datainterfaz = pd.concat(self.influxDB.InfluxDBreader(query = self.query1), ignore_index=True)
        # self.Datainterfaz = self.influxDB.InfluxDBreader(query = self.query1)
        self.Datainterfaz.set_index("_field", inplace = True)
        
        #Get Asynchronous and synchronous Data
        self.query2 = self.influxDB.QueryCreator(measurement="Planta_Biogas", train_time=str(self.t_train), type=4)
        DataPlant = pd.concat(self.influxDB.InfluxDBreader(query = self.query2), ignore_index=True)
        # DataPlant = self.influxDB.InfluxDBreader(query = self.query2)
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
            
            #V102
            P_V102 = DataPlant["_value"]["PT-104"]
            T_V102 = DataPlant["_value"]["TT-104"]
            rh_V102 = DataPlant["_value"]["AT-103B"]        #rh: relative humidity
            x_CH4_V102 = DataPlant["_value"]["AT-104A-CH4"]
            x_CO2_V102 = DataPlant["_value"]["AT-104A-CO2"]
            x_O2_V102 = DataPlant["_value"]["AT-104A-O2"]
            x_H2S_V102 = DataPlant["_value"]["AT-104A-H2S"]
            x_H2_V102 = DataPlant["_value"]["AT-104A-H2"]
            
            #V107
            P_V107 = DataPlant["_value"]["PT-105"]
            T_V107 = DataPlant["_value"]["TT-105"]
            rh_V107 = DataPlant["_value"]["AT-105B"]        #rh: relative humidity
            x_CH4_V107 = DataPlant["_value"]["AT-105A-CH4"]
            x_CO2_V107 = DataPlant["_value"]["AT-105A-CO2"]
            x_O2_V107 = DataPlant["_value"]["AT-105A-O2"]
            x_H2S_V107 = DataPlant["_value"]["AT-105A-H2S"]
            x_H2_V107 = DataPlant["_value"]["AT-105A-H2"]  
            
            #Normalize the time for differential equation
            time_norm = normaliceTime(time = time)
            
            #Sizing synchronous vectors (same lenght for Model)
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
            V_R101 = SameDimension(P_V101, L_R101)
            P_R101 = SameDimension(P_V101, P_R101)
            
            #Variable for V102
            TT_V102 = SameDimension(P_V101, T_V102)
            rh_V102 = SameDimension(P_V101, rh_V102)
            x_CH4_V102 = SameDimension(P_V101, x_CH4_V102)
            x_CO2_V102 = SameDimension(P_V101, x_CO2_V102)
            x_O2_V102 = SameDimension(P_V101, x_O2_V102)
            x_H2S_V102 = SameDimension(P_V101, x_H2S_V102)
            x_H2_V102 = SameDimension(P_V101, x_H2_V102)
            
            #Variable for V107
            TT_V107 = SameDimension(P_V101, T_V107)
            rh_V107 = SameDimension(P_V101, rh_V107)
            x_CH4_V107 = SameDimension(P_V101, x_CH4_V107)
            x_CO2_V107 = SameDimension(P_V101, x_CO2_V107)
            x_O2_V107 = SameDimension(P_V101, x_O2_V107)
            x_H2S_V107 = SameDimension(P_V101, x_H2S_V107)
            x_H2_V107 = SameDimension(P_V101, x_H2_V107)
            
            #Create DataFrame with Synchronous Data                                   
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
                "V_R101": V_R101.tolist(),
                "P_R101": P_R101.tolist(),
                "P_V102":P_V102.tolist(),
                "T_V102":TT_V102.tolist(),
                "rh_V102": rh_V102.tolist(),
                "x_CH4_V102": x_CH4_V102.tolist(),
                "x_CO2_V102": x_CO2_V102.tolist(),
                "x_O2_V102": x_O2_V102.tolist(),
                "x_H2S_V102": x_H2S_V102.tolist(),
                "x_H2_V102": x_H2_V102.tolist(),
                "P_V107":P_V107.tolist(),
                "T_V107":TT_V107.tolist(),
                "rh_V107": rh_V107.tolist(),
                "x_CH4_V107": x_CH4_V107.tolist(),
                "x_CO2_V107": x_CO2_V107.tolist(),
                "x_O2_V107": x_O2_V107.tolist(),
                "x_H2S_V107": x_H2S_V107.tolist(),
                "x_H2_V107": x_H2_V107.tolist()               
            })
        
            #### ----add Asynchronous Data
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
            
            #V102
            P_V102 = DataPlant["_value"]["PT-104"]
            T_V102 = DataPlant["_value"]["TT-104"]
            rh_V102 = DataPlant["_value"]["AT-103B"]        #rh: relative humidity
            x_CH4_V102 = DataPlant["_value"]["AT-104A-CH4"]
            x_CO2_V102 = DataPlant["_value"]["AT-104A-CO2"]
            x_O2_V102 = DataPlant["_value"]["AT-104A-O2"]
            x_H2S_V102 = DataPlant["_value"]["AT-104A-H2S"]
            x_H2_V102 = DataPlant["_value"]["AT-104A-H2"]
            
            #V107
            P_V107 = DataPlant["_value"]["PT-105"]
            T_V107 = DataPlant["_value"]["TT-105"]
            rh_V107 = DataPlant["_value"]["AT-105B"]        #rh: relative humidity
            x_CH4_V107 = DataPlant["_value"]["AT-105A-CH4"]
            x_CO2_V107 = DataPlant["_value"]["AT-105A-CO2"]
            x_O2_V107 = DataPlant["_value"]["AT-105A-O2"]
            x_H2S_V107 = DataPlant["_value"]["AT-105A-H2S"]
            x_H2_V107 = DataPlant["_value"]["AT-105A-H2"]  
             
            #Normalize the time for differential equation
            time_norm = normaliceTime(time = time)
            
            #Sizing synchronous vectors (same lenght for Model)
            #Variable for V102
            TT_V102 = SameDimension(P_V101, T_V102)
            rh_V102 = SameDimension(P_V101, rh_V102)
            x_CH4_V102 = SameDimension(P_V101, x_CH4_V102)
            x_CO2_V102 = SameDimension(P_V101, x_CO2_V102)
            x_O2_V102 = SameDimension(P_V101, x_O2_V102)
            x_H2S_V102 = SameDimension(P_V101, x_H2S_V102)
            x_H2_V102 = SameDimension(P_V101, x_H2_V102)
            
            #Variable for V107
            TT_V107 = SameDimension(P_V101, T_V107)
            rh_V107 = SameDimension(P_V101, rh_V107)
            x_CH4_V107 = SameDimension(P_V101, x_CH4_V107)
            x_CO2_V107 = SameDimension(P_V101, x_CO2_V107)
            x_O2_V107 = SameDimension(P_V101, x_O2_V107)
            x_H2S_V107 = SameDimension(P_V101, x_H2S_V107)
            x_H2_V107 = SameDimension(P_V101, x_H2_V107)
                        
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
            V_R101 = SameDimension(P_V101, L_R101)
            P_R101 = SameDimension(P_V101, P_R101)   
            
            #Create DataFrame with Synchronous Data                             
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
                "V_R101": V_R101.tolist(),
                "P_R101": P_R101.tolist(),
                "P_V102":P_V102.tolist(),
                "T_V102":TT_V102.tolist(),
                "rh_V102": rh_V102.tolist(),
                "x_CH4_V102": x_CH4_V102.tolist(),
                "x_CO2_V102": x_CO2_V102.tolist(),
                "x_O2_V102": x_O2_V102.tolist(),
                "x_H2S_V102": x_H2S_V102.tolist(),
                "x_H2_V102": x_H2_V102.tolist(),
                "P_V107":P_V107.tolist(),
                "T_V107":TT_V107.tolist(),
                "rh_V107": rh_V107.tolist(),
                "x_CH4_V107": x_CH4_V107.tolist(),
                "x_CO2_V107": x_CO2_V107.tolist(),
                "x_O2_V107": x_O2_V107.tolist(),
                "x_H2S_V107": x_H2S_V107.tolist(),
                "x_H2_V107": x_H2_V107.tolist(),              
            })
        
            #### ----Asynchronous Data
            # Pump 104
            self.DataPlant = AlignAsynchronous(variable = "FE-104", SyncDBRaw =  DataPlant, SyncDB = self.DataPlant, current_time = time)
            # Mixing R101
            self.DataPlant = AlignAsynchronous(variable = "SE-108", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
            # Pump 101
            self.DataPlant = AlignAsynchronous(variable = "P-101", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
        
        elif self.Operation_mode == 3:
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
             
            #V102
            P_V102 = DataPlant["_value"]["PT-104"]
            T_V102 = DataPlant["_value"]["TT-104"]
            rh_V102 = DataPlant["_value"]["AT-103B"]        #rh: relative humidity
            x_CH4_V102 = DataPlant["_value"]["AT-104A-CH4"]
            x_CO2_V102 = DataPlant["_value"]["AT-104A-CO2"]
            x_O2_V102 = DataPlant["_value"]["AT-104A-O2"]
            x_H2S_V102 = DataPlant["_value"]["AT-104A-H2S"]
            x_H2_V102 = DataPlant["_value"]["AT-104A-H2"]
            
            #R102
            PH_R102 = DataPlant["_value"]["AT-102"]        
            L_R102 = DataPlant["_value"]["LT-102"]       #L: level
            P_R102 = DataPlant["_value"]["PT-102"]
            T1_R102 =  DataPlant["_value"]["TE-102A"]
            T2_R102 = DataPlant["_value"]["TE-102B"]
            Tprom_R102 = DataPlant["_value"]["TE-R102"]
            
            #V107
            P_V107 = DataPlant["_value"]["PT-105"]
            T_V107 = DataPlant["_value"]["TT-105"]
            rh_V107 = DataPlant["_value"]["AT-105B"]        #rh: relative humidity
            x_CH4_V107 = DataPlant["_value"]["AT-105A-CH4"]
            x_CO2_V107 = DataPlant["_value"]["AT-105A-CO2"]
            x_O2_V107 = DataPlant["_value"]["AT-105A-O2"]
            x_H2S_V107 = DataPlant["_value"]["AT-105A-H2S"]
            x_H2_V107 = DataPlant["_value"]["AT-105A-H2"]  
            
            #Normalize the time for differential equation 
            time_norm = normaliceTime(time = time)
            
            #Sizing synchronous vectors (same lenght for Model)
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
            V_R101 = SameDimension(P_V101, L_R101)
            P_R101 = SameDimension(P_V101, P_R101)  
            
            #Variables for V102
            TT_V102 = SameDimension(P_V101, T_V102)
            rh_V102 = SameDimension(P_V101, rh_V102)
            x_CH4_V102 = SameDimension(P_V101, x_CH4_V102)
            x_CO2_V102 = SameDimension(P_V101, x_CO2_V102)
            x_O2_V102 = SameDimension(P_V101, x_O2_V102)
            x_H2S_V102 = SameDimension(P_V101, x_H2S_V102)
            x_H2_V102 = SameDimension(P_V101, x_H2_V102)
            
            #Variables for R102
            T1_R102 = SameDimension(P_V101, T1_R102)
            T2_R102 = SameDimension(P_V101, T2_R102)
            Tprom_R102 = SameDimension(P_V101, Tprom_R102)
            PH_R102 = SameDimension(P_V101, PH_R102)
            V_R102 = SameDimension(P_V101, L_R102)
            P_R102 = SameDimension(P_V101, P_R102)
            
            #Variable for V107
            TT_V107 = SameDimension(P_V101, T_V107)
            rh_V107 = SameDimension(P_V101, rh_V107)
            x_CH4_V107 = SameDimension(P_V101, x_CH4_V107)
            x_CO2_V107 = SameDimension(P_V101, x_CO2_V107)
            x_O2_V107 = SameDimension(P_V101, x_O2_V107)
            x_H2S_V107 = SameDimension(P_V101, x_H2S_V107)
            x_H2_V107 = SameDimension(P_V101, x_H2_V107)
                                      
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
                "V_R101": V_R101.tolist(),
                "P_R101": P_R101.tolist(),
                "P_V102":P_V102.tolist(),
                "T_V102":TT_V102.tolist(),
                "rh_V102": rh_V102.tolist(),
                "x_CH4_V102": x_CH4_V102.tolist(),
                "x_CO2_V102": x_CO2_V102.tolist(),
                "x_O2_V102": x_O2_V102.tolist(),
                "x_H2S_V102": x_H2S_V102.tolist(),
                "x_H2_V102": x_H2_V102.tolist(),
                "T1_R102": T1_R102.tolist(),
                "T2_R102": T2_R102.tolist(),
                "Tprom_R102": Tprom_R102.tolist(),
                "PH_R102": PH_R102.tolist(),
                "V_R102": V_R102.tolist(),
                "P_R102": P_R102.tolist(),
                "P_V107":P_V107.tolist(),
                "T_V107":TT_V107.tolist(),
                "rh_V107": rh_V107.tolist(),
                "x_CH4_V107": x_CH4_V107.tolist(),
                "x_CO2_V107": x_CO2_V107.tolist(),
                "x_O2_V107": x_O2_V107.tolist(),
                "x_H2S_V107": x_H2S_V107.tolist(),
                "x_H2_V107": x_H2_V107.tolist(),               
            })
        
            #### ----Asynchronous Data
            # Pump 104
            self.DataPlant = AlignAsynchronous(variable = "FE-104", SyncDBRaw =  DataPlant, SyncDB = self.DataPlant, current_time = time)
            # Mixing R101
            self.DataPlant = AlignAsynchronous(variable = "SE-108", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
            # Pump 101
            self.DataPlant = AlignAsynchronous(variable = "P-101", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
            #Mixing R102 
            self.DataPlant = AlignAsynchronous(variable = "SE-109", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
        
        elif self.Operation_mode == 4 or self.Operation_mode == 5:
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
             
            #V102
            P_V102 = DataPlant["_value"]["PT-104"]
            T_V102 = DataPlant["_value"]["TT-104"]
            rh_V102 = DataPlant["_value"]["AT-103B"]        #rh: relative humidity
            x_CH4_V102 = DataPlant["_value"]["AT-104A-CH4"]
            x_CO2_V102 = DataPlant["_value"]["AT-104A-CO2"]
            x_O2_V102 = DataPlant["_value"]["AT-104A-O2"]
            x_H2S_V102 = DataPlant["_value"]["AT-104A-H2S"]
            x_H2_V102 = DataPlant["_value"]["AT-104A-H2"]
            
            #R102
            PH_R102 = DataPlant["_value"]["AT-102"]        
            L_R102 = DataPlant["_value"]["LT-102"]       #L: level
            P_R102 = DataPlant["_value"]["PT-102"]
            T1_R102 =  DataPlant["_value"]["TE-102A"]
            T2_R102 = DataPlant["_value"]["TE-102B"]
            Tprom_R102 = DataPlant["_value"]["TE-R102"]
            
            #V107
            P_V107 = DataPlant["_value"]["PT-105"]
            T_V107 = DataPlant["_value"]["TT-105"]
            rh_V107 = DataPlant["_value"]["AT-105B"]        #rh: relative humidity
            x_CH4_V107 = DataPlant["_value"]["AT-105A-CH4"]
            x_CO2_V107 = DataPlant["_value"]["AT-105A-CO2"]
            x_O2_V107 = DataPlant["_value"]["AT-105A-O2"]
            x_H2S_V107 = DataPlant["_value"]["AT-105A-H2S"]
            x_H2_V107 = DataPlant["_value"]["AT-105A-H2"]
             
            #Normalize the time for differential equation 
            time_norm = normaliceTime(time = time)
            
            #Sizing synchronous vectors (same lenght for Model)
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
            V_R101 = SameDimension(P_V101, L_R101)
            P_R101 = SameDimension(P_V101, P_R101)  
            
            #Variables for V102
            TT_V102 = SameDimension(P_V101, T_V102)
            rh_V102 = SameDimension(P_V101, rh_V102)
            x_CH4_V102 = SameDimension(P_V101, x_CH4_V102)
            x_CO2_V102 = SameDimension(P_V101, x_CO2_V102)
            x_O2_V102 = SameDimension(P_V101, x_O2_V102)
            x_H2S_V102 = SameDimension(P_V101, x_H2S_V102)
            x_H2_V102 = SameDimension(P_V101, x_H2_V102)
            
            #Variables for R102
            T1_R102 = SameDimension(P_V101, T1_R102)
            T2_R102 = SameDimension(P_V101, T2_R102)
            Tprom_R102 = SameDimension(P_V101, Tprom_R102)
            PH_R102 = SameDimension(P_V101, PH_R102)
            V_R102 = SameDimension(P_V101, L_R102)
            P_R102 = SameDimension(P_V101, P_R102)
            
            #Variable for V107
            TT_V107 = SameDimension(P_V101, T_V107)
            rh_V107 = SameDimension(P_V101, rh_V107)
            x_CH4_V107 = SameDimension(P_V101, x_CH4_V107)
            x_CO2_V107 = SameDimension(P_V101, x_CO2_V107)
            x_O2_V107 = SameDimension(P_V101, x_O2_V107)
            x_H2S_V107 = SameDimension(P_V101, x_H2S_V107)
            x_H2_V107 = SameDimension(P_V101, x_H2_V107)
                                      
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
                "V_R101": V_R101.tolist(),
                "P_R101": P_R101.tolist(),
                "P_V102":P_V102.tolist(),
                "T_V102":TT_V102.tolist(),
                "rh_V102": rh_V102.tolist(),
                "x_CH4_V102": x_CH4_V102.tolist(),
                "x_CO2_V102": x_CO2_V102.tolist(),
                "x_O2_V102": x_O2_V102.tolist(),
                "x_H2S_V102": x_H2S_V102.tolist(),
                "x_H2_V102": x_H2_V102.tolist(),
                "T1_R102": T1_R102.tolist(),
                "T2_R102": T2_R102.tolist(),
                "Tprom_R102": Tprom_R102.tolist(),
                "PH_R102": PH_R102.tolist(),
                "V_R102": V_R102.tolist(),
                "P_R102": P_R102.tolist(),
                "P_V107":P_V107.tolist(),
                "T_V107":TT_V107.tolist(),
                "rh_V107": rh_V107.tolist(),
                "x_CH4_V107": x_CH4_V107.tolist(),
                "x_CO2_V107": x_CO2_V107.tolist(),
                "x_O2_V107": x_O2_V107.tolist(),
                "x_H2S_V107": x_H2S_V107.tolist(),
                "x_H2_V107": x_H2_V107.tolist(),                 
            })
        
            #### ----Asynchronous Data
            # Pump 104
            self.DataPlant = AlignAsynchronous(variable = "FE-104", SyncDBRaw =  DataPlant, SyncDB = self.DataPlant, current_time = time)
            # Mixing R101
            self.DataPlant = AlignAsynchronous(variable = "SE-108", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
            # Pump 101
            self.DataPlant = AlignAsynchronous(variable = "P-101", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
            #Mixing R102 
            self.DataPlant = AlignAsynchronous(variable = "SE-109", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)
            #Pump 102
            self.DataPlant = AlignAsynchronous(variable = "P-102", SyncDBRaw = DataPlant, SyncDB = self.DataPlant, current_time = time)

        self.DataPlant.fillna(0, inplace = True)

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
    
    def StochoimetricExpenditure(self, Model = "Arrhenius"):
        '''
            quantify the methane produced : Note: If the training execution starts significantly later than the plant's operation
            (exceeding the training time), it will not be possible to quantify the methane produced by the plant before the training begins.
            Example: If the training time is 60 minutes but the plant starts operating 70 minutes earlier, there will be 10 minutes of methane 
            production that cannot be quantified by the digital twin.   
            ''' 
        #Time for gompertz model only
        self.timeGompertz.append(self.total_time)
        self.total_time = self.total_time + self.tp     #minutes
        
        #---------------------------------------------
        #--------- Variables to train Operation Mode 1 and 2
        if self.Operation_mode == 1 or self.Operation_mode == 2:
            # Methane produce by R101 using V101 storage
            #Set initial value from previuos layer
            try:
                if self.Operation_mode == 1:
                    if self.TrainMode1.empty:
                        print("The DataFrame exists but is empty.")
                        self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                    else:
                        self.Csus_ini_SV_R101 = self.TrainMode1["Csus_exp"].iloc[0]
                else:
                    if self.TrainMode2.empty:
                        print("The DataFrame exists but is empty.")
                        self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                    else:
                        self.Csus_ini_SV_R101 = self.TrainMode2["Csus_exp"].iloc[0]             
            except AttributeError:
                    print("The DataFrame does not exist.")
            # Create list for TrainModel Dataframe            
            C_in_sus = []
            V = []
            Csus = []
            Q_P104v = []
            timev = []
            n_biogas_acum_Gompertz = []
            SV_g_Gompertz = []
            for i in range (len(self.DataPlant)):
                self.P_V101 = self.DataPlant["P_V101"][i]
                self.P_V102 = self.DataPlant["P_V102"][i]
                self.P_V107 = self.DataPlant["P_V107"][i]
                #conditions when the pressure inside V101 drop
                if i > 0:
                    if (i + 1) in self.DataPlant.index and i in self.DataPlant.index:
                        tp = self.DataPlant["time"][i+1] - self.DataPlant["time"][i]
                    else:
                        tp = 0
                    Q_P104 = self.DataPlant["FE-104"][i-1]
                    if self.P_V101 < (self.DataPlant["P_V101"][i-1] * 1.05):         
                        self.Pi_V101 = self.P_V101          #P_ini is the actual pressure in V101
                    if self.P_V102 < (self.DataPlant["P_V102"][i-1] * 1.05):
                        self.Pi_V102 = self.P_V102
                    if self.P_V107 < (self.DataPlant["P_V107"][i-1] * 1.05):
                        self.Pi_V107 = self.P_V107
                else:
                    tp = 0
                    Q_P104 = 0  #Flow of pump at the beginning
                    
                #Estimate the accumulated pressure in each vessel
                self.Pacum_V101 = self.Pi_V101 + self.P_V101
                self.Pacum_V102 = self.Pi_V102 + self.P_V102
                self.Pacum_V107 = self.Pi_V107 + self.Pi_V107
                
                #Estimate the Storage and accumulated mol of biogas
                # Storage biogas mol
                self.n_biogas_sto_V101 = (((self.P_V101*6.899476) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"][i] + 273.15)))           #kmol
                # Accumulated biogas mol
                self.n_biogas_acum_V101 = (((self.Pacum_V101*6.899476) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"][i] + 273.15)))           #kmol
                
                n_biogas_acum_Gompertz.append(self.n_biogas_acum_V101)
                #Estimate the storage and accumulated mol for component in biogas
                #Storage compounds
                self.mol_sto_CH4_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_CH4_V101"][i]      #kmol
                self.mol_sto_CO2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_CO2_V101"][i]      #kmol
                self.mol_sto_O2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_O2_V101"][i]        #kmol
                self.mol_sto_H2S_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_H2S_V101"][i]      #kmol
                self.mol_sto_H2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_H2_V101"][i]        #kmol
            
                #Accumulated compounds
                self.mol_acum_CH4_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CH4_V101"][i]      #kmol
                self.mol_acum_CO2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CO2_V101"][i]      #kmol
                self.mol_acum_O2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_O2_V101"][i]        #kmol
                self.mol_acum_H2S_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_H2S_V101"][i]      #kmol
                self.mol_acum_H2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_H2_V101"][i]        #kmol
                
                #Stochoimetric expenditure
                #mol organic compound
                mol_ini = self.Csus_ini_SV_R101 * (self.DataPlant["V_R101"][i])                       #Kmol
                mol_in_R101 = Q_P104 * tp/60 * self.Csv_sus                                           #Kmol 
                mol_expended = (self.mol_acum_CH4_V101) * (1/self.s_CH4)                              #Kmol    
                self.Csus_ini_SV_R101 = (mol_ini + mol_in_R101 - mol_expended)/(self.DataPlant["V_R101"][i])    #kmol/m3 = mol/L
                self.SV_g = self.Csus_ini_SV_R101 * self.MW_sustrato * self.DataPlant["V_R101"][i]              #Volatile solids g
                SV_g_Gompertz.append(self.SV_g)                                                                 #storage grams of volatile solids  

                timev.append(self.DataPlant["time"][i])
                V.append(self.DataPlant["V_R101"][i])
                Q_P104v.append(Q_P104)
                C_in_sus.append(self.Csv_sus)
                Csus.append(self.Csus_ini_SV_R101)
                
            if self.Operation_mode == 1:
                self.TrainMode1 = pd.DataFrame({"time": timev,
                                                "Vol": V,
                                                "Q_P104": self.DataPlant["FE-104"].tolist(),
                                                "Csus_in": C_in_sus,
                                                "Csus_exp":Csus,
                                                "T_R101": self.DataPlant["Tprom_R101"] 
                                                })
            else:
                self.TrainMode2 = pd.DataFrame({"time": timev,
                                                "Vol": V,
                                                "Q_P104": self.DataPlant["FE-104"].tolist(),
                                                "Csus_in": C_in_sus,
                                                "Csus_exp":Csus,
                                                "T_R101": self.DataPlant["Tprom_R101"],
                                                "Q_P101": self.DataPlant["P-101"].tolist()  
                                                })
            
            #Data to train Gompertz model in operation Model 1
            self.Model = Model
            if self.Model == "Gompertz":
                V_biogas_gompertz = []
                for i in range (len(n_biogas_acum_Gompertz)):
                    V_bio = (((V_biogas_gompertz[i]*8.314 * 273.15)/(100)*1000))/SV_g_Gompertz[i]         #Normal volume of biogas according to produce moles in V_101 (L/gSV)
                    V_biogas_gompertz.append(V_bio)
                self.TrainGompertzMode1 = pd.DataFrame({"time": self.timeGompertz[-len(self.DataPlant):],
                                                        "y_t_exp": V_biogas_gompertz})
            
        #---------------------------------------------
        #--------- Variables to train Operation Mode 3 or 5
        if self.Operation_mode == 3 or self.Operation_mode == 5:
            # Methane produce by R101 using V101 storage
            #Set initial value from previuos layer
            try:
                if self.Operation_mode == 3:
                    if self.TrainMode3.empty:
                        print("The DataFrame exists but is empty.")
                        self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                        self.Csus_ini_SV_R102 = self.Csus_ini_SV_R102
                    else:
                        self.Csus_ini_SV_R101 = self.TrainMode3["Csus_exp_R101"].iloc[0]
                        self.Csus_ini_SV_R102 = self.TrainMode3["Csus_exp_R102"].iloc[0]
                else:
                    if self.TrainMode5.empty:
                        print("The DataFrame exists but is empty.")
                        self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                        self.Csus_ini_SV_R102 = self.Csus_ini_SV_R102
                    else:
                        self.Csus_ini_SV_R101 = self.TrainMode5["Csus_exp_R101"].iloc[0]
                        self.Csus_ini_SV_R102 = self.TrainMode5["Csus_exp_R102"].iloc[0]
            except AttributeError:
                    print("The DataFrame does not exist.")
            # Create list for TrainModel Dataframe            
            C_in_sus_R101 = []
            C_in_sus_R102 = []
            V_R101 = []
            V_R102 = []
            Csus_R101 = []
            Csus_R102 = []
            Q_P104v = []
            Q_P101v = []
            timev = []
            n_biogas_acum_Gompertz_R101 = []
            n_biogas_acum_Gompertz_R102 = []
            SV_g_Gompertz_R101 = []
            SV_g_Gompertz_R102 = []
            for i in range (len(self.DataPlant)):
                self.P_V101 = self.DataPlant["P_V101"][i]
                self.P_V102 = self.DataPlant["P_V102"][i]

                #conditions when the pressure inside V101 drop
                if i > 0:
                    if (i + 1) in self.DataPlant.index and i in self.DataPlant.index:
                        tp = self.DataPlant["time"][i+1] - self.DataPlant["time"][i]
                    else:
                        tp = 0
                    Q_P104 = self.DataPlant["FE-104"][i-1]
                    Q_P101 = self.DataPlant["P-101"][i-1]
                    if self.P_V101 < (self.DataPlant["P_V101"][i-1] * 1.05):         
                        self.Pi_V101 = self.P_V101          #P_ini is the actual pressure in V101
                        self.Ptransfer_V101_to_V102 = self.Pi_V101    #Presión transfer to V102 before drop

                    if self.P_V102 < (self.DataPlant["P_V102"][i-1] * 1.05):         
                        self.Pi_V102 = self.P_V102          #P_ini is the actual pressure in V102
                else:
                    tp = 0
                    Q_P104 = 0  #Flow of pump at the beginning
                    Q_P101 = 0
                    Q_P102 = 0
                    
                #Estimate the accumulated pressure in V101
                self.Pacum_V101 = self.Pi_V101 + self.P_V101
                
                #Estimate the accumulated pressure in V102
                self.Pacum_V102 = self.Pi_V102 + self.P_V102
                
                #Estimate the Storage and accumulated mol of biogas in V101
                # Storage biogas mol in V101
                self.n_biogas_sto_V101 = (((self.P_V101*6.899476) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"][i] + 273.15)))           #kmol
                # Accumulated biogas mol in V101
                self.n_biogas_acum_V101 = (((self.Pacum_V101*6.899476) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"][i] + 273.15)))           #kmol
                n_biogas_acum_Gompertz_R101.append(self.n_biogas_acum_V101)                           #Total mol of biogas produced by R101

                #Estimate the Storage and accumulated mol of biogas in V102
                # Storage biogas mol in V102
                self.n_biogas_sto_V102 = (((self.P_V102*6.899476) * (self.Volume_V102/1000))/
                                          (8.314 * (self.DataPlant["T_V102"][i] + 273.15)))           #kmol
                # Accumulated biogas mol in V102
                self.n_biogas_acum_V102 = (((self.Pacum_V102*6.899476) * (self.Volume_V102/1000))/
                                          (8.314 * (self.DataPlant["T_V102"][i] + 273.15)) - 
                                          (((self.Ptransfer_V101_to_V102*6.899476) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"][i] + 273.15))))           #kmol
                n_biogas_acum_Gompertz_R102.append(self.n_biogas_acum_V102)
                
                #------- Mass balance in R101 according with biogas produced
                #Estimate the storage and accumulated mol for component in biogas in V101
                #Storage compounds in V101
                self.mol_sto_CH4_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_CH4_V101"][i]      #kmol
                self.mol_sto_CO2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_CO2_V101"][i]      #kmol
                self.mol_sto_O2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_O2_V101"][i]        #kmol
                self.mol_sto_H2S_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_H2S_V101"][i]      #kmol
                self.mol_sto_H2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_H2_V101"][i]        #kmol
                #Accumulated compounds in V101
                self.mol_acum_CH4_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CH4_V101"][i]      #kmol
                self.mol_acum_CO2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CO2_V101"][i]      #kmol
                self.mol_acum_O2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_O2_V101"][i]        #kmol
                self.mol_acum_H2S_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_H2S_V101"][i]      #kmol
                self.mol_acum_H2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_H2_V101"][i]        #kmol
                
                #Stochoimetric expenditure in R101
                #mol organic compound
                mol_ini_R101 = self.Csus_ini_SV_R101 * self.DataPlant["V_R101"][i]
                mol_in_R101 = Q_P104 * tp/60 * self.Csv_sus
                mol_expended_R101 = self.mol_acum_CH4_V101 * (1/self.s_CH4)
                self.Csus_ini_SV_R101 = (mol_ini_R101 + mol_in_R101 - mol_expended_R101)/(self.DataPlant["V_R101"][i])
                self.SV_g_R101 = self.Csus_ini_SV_R101 * self.MW_sustrato * self.DataPlant["V_R101"][i]         #Volatile solids g
                SV_g_Gompertz.append(self.SV_g_R101)                                                            #storage grams of volatile solids  
                  
                timev.append(self.DataPlant["time"][i])
                V_R101.append(self.DataPlant["V_R101"][i])
                Q_P104v.append(Q_P104)
                C_in_sus_R101.append(self.Csv_sus)
                Csus_R101.append(self.Csus_ini_SV_R101)
                
                #Estimate the storage and accumulated mol for component in biogas in V102
                #Storage compounds in V102
                self.mol_sto_CH4_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_CH4_V102"][i]      #kmol
                self.mol_sto_CO2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_CO2_V102"][i]      #kmol
                self.mol_sto_O2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_O2_V102"][i]        #kmol
                self.mol_sto_H2S_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_H2S_V102"][i]      #kmol
                self.mol_sto_H2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_H2_V102"][i]        #kmol
                #Accumulated compounds in V102
                self.mol_acum_CH4_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_CH4_V102"][i]      #kmol
                self.mol_acum_CO2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_CO2_V102"][i]      #kmol
                self.mol_acum_O2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_O2_V102"][i]        #kmol
                self.mol_acum_H2S_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_H2S_V102"][i]      #kmol
                self.mol_acum_H2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_H2_V102"][i]        #kmol
                
                #Stochoimetric expenditure in R102
                #mol organic compound
                mol_ini_R102 = self.Csus_ini_SV_R102 * self.DataPlant["V_R102"][i]
                mol_in_R102 = Q_P101 * tp/60 * Csus_R101[-1]
                mol_expended_R102 = self.mol_acum_CH4_V102 * (1/self.s_CH4)
                self.Csus_ini_SV_R102 = (mol_ini_R102 + mol_in_R102 - mol_expended_R102)/(self.DataPlant["V_R102"][i])
                self.SV_g_R102 = self.Csus_ini_SV_R102 * self.MW_sustrato * self.DataPlant["V_R102"][i]              #Volatile solids g
                SV_g_Gompertz_R102.append(self.SV_g_R102)                                                                 #storage grams of volatile solids  
                                    
                V_R102.append(self.DataPlant["V_R102"][i])
                Q_P101v.append(Q_P101)
                C_in_sus_R102.append(self.Csv_sus)
                Csus_R102.append(self.Csus_ini_SV_R102)
                
            if self.Operation_mode == 3:
                self.TrainMode3 = pd.DataFrame({"time": timev,
                                                "Vol_R101": V_R101,
                                                "Q_P104": self.DataPlant["FE-104"].tolist(),
                                                "Csus_exp_R101":Csus_R101,
                                                "Csus_in_R101": C_in_sus_R101,
                                                "T_R101": self.DataPlant["Tprom_R101"],
                                                "Vol_R102": V_R102,
                                                "Q_P101": self.DataPlant["P-101"].tolist(), 
                                                "Csus_exp_R102":Csus_R102,
                                                "T_R102": self.DataPlant["Tprom_R102"]                                                
                                                })
            else:
                self.TrainMode5 = pd.DataFrame({"time": timev,
                                                "Vol_R101": V_R101,
                                                "Q_P104": self.DataPlant["FE-104"].tolist(),
                                                "Csus_exp_R101":Csus_R101,
                                                "Csus_in_R101": C_in_sus_R101,
                                                "T_R101": self.DataPlant["Tprom_R101"],
                                                "Vol_R102": V_R102,
                                                "Q_P101": self.DataPlant["P-101"].tolist(), 
                                                "Csus_exp_R102":Csus_R102,
                                                "T_R102": self.DataPlant["Tprom_R102"],
                                                "Q_P102": self.DataPlant["P-102"].tolist(),                                                
                                                })
            
            #Data to train Gompertz model in Operation model 3 or 5
            self.Model = Model
            if self.Model == "Gompertz":
                V_biogas_gompertz_R101 = []
                V_biogas_gompertz_R102 = []
                for i in range (len(n_biogas_acum_Gompertz_R101)):
                    V_bio_R101 = (((n_biogas_acum_Gompertz_R101[i]*8.314 * 273.15)/(100))*1000)/(SV_g_Gompertz_R101[i])         #Normal volume of biogas per unit of volatile solids weight [L/gSV]
                    V_bio_R102 = (((n_biogas_acum_Gompertz_R102[i]*8.314 * 273.15)/(100))*1000)/(SV_g_Gompertz_R102[i])         #Normal volume of biogas per unit of volatile solids weight [L/gSV] 
                    V_biogas_gompertz_R101.append(V_bio_R101)
                    V_biogas_gompertz_R102.append(V_bio_R102)
                self.TrainGompertzMode3_5 = pd.DataFrame({"time": self.timeGompertz[-len(self.DataPlant):],
                                                        "y_t_exp_R101": V_biogas_gompertz_R101,
                                                        "y_t_exp_R102": V_biogas_gompertz_R102})
        
        #---------------------------------------------
        #--------- Variables to train Operation Mode 4
        if self.Operation_mode == 4:
            # Methane produce by R101 using V101 storage
            #Set initial value from previuos layer
            try:
                if self.TrainMode4.empty:
                    print("The DataFrame exists but is empty.")
                    self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                    self.Csus_ini_SV_R102 = self.Csus_ini_SV_R102
                else:
                    self.Csus_ini_SV_R101 = self.TrainMode4["Csus_exp_R101"].iloc[0]
                    self.Csus_ini_SV_R102 = self.TrainMode4["Csus_exp_R102"].iloc[0]       
            except AttributeError:
                    print("The DataFrame does not exist.")
            # Create list for TrainModel Dataframe            
            C_in_sus_R101 = []
            C_in_sus_R102 = []
            V_R101 = []
            V_R102 = []
            Csus_R101 = []
            Csus_R102 = []
            Q_P104v = []
            Q_P101v = []
            Q_P102v = []
            timev = []
            n_biogas_acum_Gompertz_R101 = []
            n_biogas_acum_Gompertz_R102 = []
            SV_g_Gompertz_R101 = []
            SV_g_Gompertz_R102 = []
            for i in range (len(self.DataPlant)):
                self.P_V101 = self.DataPlant["P_V101"][i]
                self.P_V102 = self.DataPlant["P_V102"][i]

                #conditions when the pressure inside V101 drop
                if i > 0:
                    if (i + 1) in self.DataPlant.index and i in self.DataPlant.index:
                        tp = self.DataPlant["time"][i+1] - self.DataPlant["time"][i]
                    else:
                        tp = 0
                    Q_P104 = self.DataPlant["FE-104"][i-1]
                    Q_P101 = self.DataPlant["P-101"][i-1]
                    Q_P102 = self.DataPlant["P-102"][i-1]
                    if self.P_V101 < (self.DataPlant["P_V101"][i-1] * 1.05):         
                        self.Pi_V101 = self.P_V101          #P_ini is the actual pressure in V101
                        self.Ptransfer_V101_to_V102 = self.Pi_V101    #Presión transfer to V102 before drop
                    if self.P_V102 < (self.DataPlant["P_V102"][i-1] * 1.05):         
                        self.Pi_V102 = self.P_V102          #P_ini is the actual pressure in V102
                    
                else:
                    tp = 0
                    Q_P104 = 0  #Flow of pump at the beginning
                    Q_P101 = 0
                    Q_P102 = 0
                    
                #Estimate the accumulated pressure in V101
                self.Pacum_V101 = self.Pi_V101 + self.P_V101
                
                #Estimate the accumulated pressure in V102
                self.Pacum_V102 = self.Pi_V102 + self.P_V102
                
                #Estimate the Storage and accumulated mol of biogas in V101
                # Storage biogas mol in V101
                self.n_biogas_sto_V101 = (((self.P_V101*6.899476) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"][i] + 273.15)))           #kmol
                # Accumulated biogas mol in V101
                self.n_biogas_acum_V101 = (((self.Pacum_V101*6.899476) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"][i] + 273.15)))           #kmol
                n_biogas_acum_Gompertz_R101.append(self.n_biogas_acum_V101)
                
                #Estimate the Storage and accumulated mol of biogas in V102
                # Storage biogas mol in V102
                self.n_biogas_sto_V102 = (((self.P_V102*6.899476) * (self.Volume_V102/1000))/
                                          (8.314 * (self.DataPlant["T_V102"][i] + 273.15)))             #kmol
                
                # Accumulated biogas mol in V102
                self.n_biogas_acum_V102 = (((self.Pacum_V102*6.899476) * (self.Volume_V102/1000))/
                                          (8.314 * (self.DataPlant["T_V102"][i] + 273.15)) - 
                                          (((self.Ptransfer_V101_to_V102*6.899476) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"][i] + 273.15))))           #kmol
                n_biogas_acum_Gompertz_R102.append(self.n_biogas_acum_V102)

                #------- Mass balance in R101 according with biogas produced
                #Estimate the storage and accumulated mol for component in biogas in V101
                #Storage compounds in V101
                self.mol_sto_CH4_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_CH4_V101"][i]      #kmol
                self.mol_sto_CO2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_CO2_V101"][i]      #kmol
                self.mol_sto_O2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_O2_V101"][i]        #kmol
                self.mol_sto_H2S_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_H2S_V101"][i]      #kmol
                self.mol_sto_H2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_H2_V101"][i]        #kmol
                #Accumulated compounds in V101
                self.mol_acum_CH4_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CH4_V101"][i]      #kmol
                self.mol_acum_CO2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CO2_V101"][i]      #kmol
                self.mol_acum_O2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_O2_V101"][i]        #kmol
                self.mol_acum_H2S_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_H2S_V101"][i]      #kmol
                self.mol_acum_H2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_H2_V101"][i]        #kmol
                
                #Stochoimetric expenditure in R101
                #mol organic compound
                mol_ini_R101 = self.Csus_ini_SV_R101 * self.DataPlant["V_R101"][i]
                mol_in_R101 = (Q_P104 * tp/60 * self.Csv_sus) + (Q_P102 * tp/60 * self.Csus_ini_SV_R102)
                mol_expended_R101 = self.mol_acum_CH4_V101 * (1/self.s_CH4)
                self.Csus_ini_SV_R101 = (mol_ini_R101 + mol_in_R101 - mol_expended_R101)/(self.DataPlant["V_R101"][i])
                self.SV_g_R101 = self.Csus_ini_SV_R101 * self.MW_sustrato * self.DataPlant["V_R101"][i]         #Volatile solids g
                SV_g_Gompertz_R101.append(self.SV_g_R101)                                                       #storage grams of volatile solids  
                              
                timev.append(self.DataPlant["time"][i])
                V_R101.append(self.DataPlant["V_R101"][i])
                Q_P104v.append(Q_P104)
                C_in_sus_R101.append(self.Csv_sus)
                Csus_R101.append(self.Csus_ini_SV_R101)
                
                #Estimate the storage and accumulated mol for component in biogas in V102
                #Storage compounds in V102
                self.mol_sto_CH4_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_CH4_V102"][i]      #kmol
                self.mol_sto_CO2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_CO2_V102"][i]      #kmol
                self.mol_sto_O2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_O2_V102"][i]        #kmol
                self.mol_sto_H2S_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_H2S_V102"][i]      #kmol
                self.mol_sto_H2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_H2_V102"][i]        #kmol
                #Accumulated compounds in V102
                self.mol_acum_CH4_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_CH4_V102"][i]      #kmol
                self.mol_acum_CO2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_CO2_V102"][i]      #kmol
                self.mol_acum_O2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_O2_V102"][i]        #kmol
                self.mol_acum_H2S_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_H2S_V102"][i]      #kmol
                self.mol_acum_H2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_H2_V102"][i]        #kmol
                
                #Stochoimetric expenditure in R102
                #mol organic compound
                mol_ini_R102 = self.Csus_ini_SV_R102 * self.DataPlant["V_R102"][i]
                mol_in_R102 = Q_P101 * tp/60 * Csus_R101[-1]
                mol_expended_R102 = self.mol_acum_CH4_V102 * (1/self.s_CH4)
                self.Csus_ini_SV_R102 = (mol_ini_R102 + mol_in_R102 - mol_expended_R102)/(self.DataPlant["V_R102"][i])
                self.SV_g_R102 = self.Csus_ini_SV_R102 * self.MW_sustrato * self.DataPlant["V_R102"][i]         #Volatile solids g
                SV_g_Gompertz_R101.append(self.SV_g_R101)                                                       #storage grams of volatile solids
                             
                V_R102.append(self.DataPlant["V_R102"][i])
                Q_P101v.append(Q_P101)
                C_in_sus_R102.append(self.Csv_sus)
                Csus_R102.append(self.Csus_ini_SV_R102)
                
            
            self.TrainMode4 = pd.DataFrame({"time": timev,
                                            "Vol_R101": V_R101,
                                            "Q_P104": self.DataPlant["FE-104"].tolist(),
                                            "Csus_exp_R101":Csus_R101,
                                            "Csus_in_R101": C_in_sus_R101,
                                            "T_R101": self.DataPlant["Tprom_R101"],
                                            "Vol_R102": V_R102,
                                            "Q_P101": self.DataPlant["P-101"].tolist(), 
                                            "Csus_exp_R102":Csus_R102,
                                            "T_R102": self.DataPlant["Tprom_R102"],
                                            "Q_P102": self.DataPlant["P-102"].tolist()                                               
                                            })
            
            #Data to train Gompertz model in Operation model 3 or 5
            self.Model = Model
            if self.Model == "Gompertz":
                V_biogas_gompertz_R101 = []
                V_biogas_gompertz_R102 = []
                for i in range (len(n_biogas_acum_Gompertz_R101)):
                    V_bio_R101 = (((n_biogas_acum_Gompertz_R101[i]*8.314 * 273.15)/(100))*1000)/(SV_g_Gompertz_R101[i])         #Normal volume of biogas according to moles produced by R_101
                    V_bio_R102 = (((n_biogas_acum_Gompertz_R102[i]*8.314 * 273.15)/(100))*1000)/(SV_g_Gompertz_R102[i])         #Normal volume of biogas according to moles produced by R_102  
                    V_biogas_gompertz_R101.append(V_bio_R101)
                    V_biogas_gompertz_R102.append(V_bio_R102)
                self.TrainGompertzMode4 = pd.DataFrame({"time": self.timeGompertz[-len(self.DataPlant):],
                                                        "y_t_exp_R101": V_biogas_gompertz_R101,
                                                        "y_t_exp_R102": V_biogas_gompertz_R102})
        
    
    def OptimizationArrhenius (self, resolution):
        
        def model_Arrhenius(C, t, K, Ea, VR_in_func, T_func, Q_func_1, Q_func_2, Csus_in_func_1, Csus_in_func_2, Operation):
            R = 8.314
            T=T_func(t)
            Q_1=Q_func_1(t)
            Q_2=Q_func_2(t)
            Csus_in_1 = Csus_in_func_1(t)
            Csus_in_2 = Csus_in_func_2(t)
            VR = VR_in_func(t)               #Volume change in the time by the control
            if Operation == 1:         #One entrance without recirculation
                dCsus_dt = ((Q_1 / VR) * (Csus_in_1 - C)) - (C * K * np.exp(-(Ea)/(R*T))) / VR
            elif Operation == 2:       #Two entrances with differents concentrations
                dCsus_dt = (Q_1 * Csus_in_1)/VR + (Q_2 * Csus_in_2)/VR - ((Q_1+Q_2)*C)/VR - (C * K * np.exp(-Ea/(R*T))) / VR
            elif Operation == 3:       #One entrance with recirculation
                dCsus_dt = (Q_1 * Csus_in_1)/VR + (Q_2 * C)/VR - ((Q_1)*C)/VR - (C * K * np.exp(-Ea/(R*T))) / VR
            return dCsus_dt
        
        # Optimization function t: vector of experimental time, C_exp: sustrate experimental concentration, y0: Initial value, 
        def Optimization(t, C_exp, y0, VR, temperatures, Qi1, Csus_in_i1, Qi2, Csus_in_i2, Operation, K=1, Ea=1): 
            # Define the objective function to minimize
            def objective(params):
                K, Ea = params
                t_train = t

                #interpol the vectors according to experimental time
                T_func = lambda t: np.interp(t, t_train, temperatures)
                Q_func1 = lambda t: np.interp(t, t_train, Qi1)
                Q_func2 = lambda t: np.interp(t, t_train, Qi2)
                VR_func = lambda t: np.interp(t, t_train, VR)
                Csus_in1 = lambda t: np.interp(t, t_train, Csus_in_i1)
                Csus_in2 = lambda t: np.interp(t, t_train, Csus_in_i2)
                
                C_model = odeint(model_Arrhenius, y0, t, args = (K, Ea, VR_func, T_func, Q_func1, Q_func2, Csus_in1, Csus_in2, Operation)).flatten()

                squared_diff = np.sum((C_exp - C_model) ** 2)
                return squared_diff
            
            result = minimize(objective, [K, Ea], method = 'Nelder-Mead')
            return result
        
        if self.Operation_mode == 1:
            t_exp = (self.TrainMode1["time"]*60).tolist()   #seconds
            C_exp = self.TrainMode1["Csus_exp"].tolist()    #Kmol/m3 = mol/L
            VR_exp = self.TrainMode1["Vol"].tolist()        #L 
            Csus_in = self.TrainMode1["Csus_in"].to_list()  #mol/L
            T_R101 = (self.TrainMode1["T_R101"]+273.15).tolist()  #K     
            Q_P104 = (self.TrainMode1["Q_P104"]/3600).tolist()    #L/s 
            K = []
            Ea = []
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt = C_exp[i : i+resolution]
                VR_exp_opt = VR_exp[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                Csus_in_opt = Csus_in[i : i + resolution]
                Opt_kinetic_params = Optimization(t = t_exp_opt, C_exp = C_exp_opt, y0 = C_exp_opt[0], VR = VR_exp_opt,
                                                  temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt,
                                                  Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_opt, Operation = 1, K = self.K_mean_R101, Ea = self.Ea_mean_R101)
                K.append(Opt_kinetic_params.x[0])
                Ea.append(Opt_kinetic_params.x[1])
            
            self.K_mean_R101 = st.mean(K)
            self.Ea_mean_R101 = st.mean(Ea)
        
        elif self.Operation_mode == 2:
            t_exp = (self.TrainMode2["time"]*60).tolist()   #seconds
            C_exp = self.TrainMode2["Csus_exp"].tolist()    #Kmol/m3 = mol/L
            VR_exp = self.TrainMode2["Vol"].tolist()        #L 
            Csus_in = self.TrainMode2["Csus_in"].to_list()  #mol/L
            T_R101 = (self.TrainMode2["T_R101"]+273.15).tolist()  #K     
            Q_P104 = (self.TrainMode2["Q_P104"]/3600).tolist()    #L/s 
            K = []
            Ea = []
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt = C_exp[i : i+resolution]
                VR_exp_opt = VR_exp[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                Csus_in_opt = Csus_in[i : i + resolution]
                Opt_kinetic_params = Optimization(t = t_exp_opt, C_exp = C_exp_opt, y0 = C_exp_opt[0], VR = VR_exp_opt,
                                                  temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt,
                                                  Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_opt, Operation = 1, K = self.K_mean_R101, Ea=self.Ea_mean_R101)
                K.append(Opt_kinetic_params.x[0])
                Ea.append(Opt_kinetic_params.x[1])
            
            self.K_mean_R101 = st.mean(K)
            self.Ea_mean_R101 = st.mean(Ea)
        
        elif self.Operation_mode == 3:
            #Optimization variables for R101
            t_exp = (self.TrainMode3["time"]*60).tolist()               #seconds
            C_exp_R101 = self.TrainMode3["Csus_exp_R101"].tolist()      #Kmol/m3 = mol/L
            Q_P104 = (self.TrainMode3["Q_P104"]/3600).tolist()          #L/s
            VR_exp_R101 = self.TrainMode3["Vol_R101"].tolist()            #L
            T_R101 = (self.TrainMode3["T_R101"] + 273.15).tolist()      #K
            Csus_in_R101 = (self.TrainMode3["Csus_in_R101"]).tolist()   #kmol/m3 = mol/L
            K_R101 = []
            Ea_R101 = []

            #Optimization variables R102
            C_exp_R102 = self.TrainMode3["Csus_exp_R102"].tolist()    #Kmol/m3 = mol/L
            Q_P101 = (self.TrainMode3["Q_P101"]/3600).tolist()        #L/s
            VR_exp_R102 = self.TrainMode3["Vol_R102"].tolist()          #L
            T_R102 = (self.TrainMode3["T_R102"]).tolist()             #K
            Csus_in_R102 = self.TrainMode3["Csus_exp_R101"].tolist()  #Kmol/m3 = mol/L
            K_R102 = []
            Ea_R102 = []

            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                #Variables for R101
                C_exp_R101_opt = C_exp_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                VR_exp_R101_opt = VR_exp_R101[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Csus_in_R101_opt = Csus_in_R101[i : i+resolution]

                #Variables for R102
                C_exp_R102_opt = C_exp_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]
                VR_exp_R102_opt = VR_exp_R102[i : i+resolution]
                T_R102_opt = T_R102[i : i+resolution]

                #Optimization for R101
                Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_R101_opt, y0 = C_exp_R101_opt[0], VR = VR_exp_R101_opt,
                                                  temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_R101_opt,
                                                  Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_R101_opt, Operation = 1, K = self.K_mean_R101, Ea = self.Ea_mean_R101)
                
                K_R101.append(Opt_kinetic_params_R101.x[0])
                Ea_R101.append(Opt_kinetic_params_R101.x[1])

                #Optimization for R102
                Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_R102_opt, y0 = C_exp_R102_opt[0], VR = VR_exp_R102_opt,
                                                  temperatures = T_R102_opt, Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_R101_opt,
                                                  Qi2 = Q_P101_opt, Csus_in_i2 = C_exp_R101_opt, Operation = 1, K = self.K_mean_R102, Ea = self.Ea_mean_R102)
                
                K_R102.append(Opt_kinetic_params_R102.x[0])
                Ea_R102.append(Opt_kinetic_params_R102.x[1])

            #Kinetics for R101
            self.K_mean_R101 = st.mean(K_R101)
            self.Ea_mean_R101 = st.mean(Ea_R101)

            #Kinetics for R102
            self.K_mean_R102 = st.mean(K_R102)
            self.Ea_mean_R102 = st.mean(Ea_R102)
        
        elif self.Operation_mode == 4:
            #Optimization variables for R101
            t_exp = (self.TrainMode4["time"]*60).tolist()               #seconds
            C_exp_R101 = self.TrainMode4["Csus_exp_R101"].tolist()      #Kmol/m3 = mol/L
            Q_P104 = (self.TrainMode4["Q_P104"]/3600).tolist()          #L/s
            VR_exp_R101 = self.TrainMode4["Vol_R101"].tolist()          #L
            T_R101 = (self.TrainMode4["T_R101"] + 273.15).tolist()      #K
            Csus_in_R101 = (self.TrainMode4["Csus_in_R101"]).tolist()   #kmol/m3 = mol/L
            Q_P102 = (self.TrainMode4["Q_P102"]/3600).tolist()
            K_R101 = []
            Ea_R101 = []
            
            #Optimization variables for R102
            C_exp_R102 = self.TrainMode4["Csus_exp_R102"].tolist()    #Kmol/m3 = mol/L
            Q_P101 = (self.TrainMode4["Q_P101"]/3600).tolist()        #L/s
            VR_exp_R102 = self.TrainMode4["Vol_R102"].tolist()          #L
            T_R102 = (self.TrainMode4["T_R102"]).tolist()             #K
            K_R102 = []
            Ea_R102 = []
        
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                #Variables for R101
                C_exp_R101_opt = C_exp_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                VR_exp_R101_opt = VR_exp_R101[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Csus_in_R101_opt = Csus_in_R101[i : i+resolution]
                Q_P102_opt = Q_P102[i : i+resolution]
                
                #Variables for R102
                C_exp_R102_opt = C_exp_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]
                VR_exp_R102_opt = VR_exp_R102[i : i+resolution]
                T_R102_opt = T_R102[i : i+resolution]
                
                #optimization R101
                Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_R101_opt, y0 = C_exp_R101_opt[0], VR = VR_exp_R101_opt,
                                                  temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_R101_opt,
                                                  Qi2 = Q_P102_opt, Csus_in_i2 = Csus_in_R101_opt, Operation = 2, K = self.K_mean_R101, Ea = self.Ea_mean_R101)
                
                K_R101.append(Opt_kinetic_params_R101.x[0])
                Ea_R101.append(Opt_kinetic_params_R101.x[1])
                
                #Optimization for R102
                Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_R102_opt, y0 = C_exp_R102_opt[0], VR = VR_exp_R102_opt,
                                                  temperatures = T_R102_opt, Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_R101_opt,
                                                  Qi2 = Q_P101_opt, Csus_in_i2 = C_exp_R101_opt, Operation = 1, K = self.K_mean_R102, Ea = self.Ea_mean_R102)
                
                K_R102.append(Opt_kinetic_params_R102.x[0])
                Ea_R102.append(Opt_kinetic_params_R102.x[1])
            
            #Kinetics for R101
            self.K_mean_R101 = st.mean(K_R101)
            self.Ea_mean_R101 = st.mean(Ea_R101)

            #Kinetics for R102
            self.K_mean_R102 = st.mean(K_R102)
            self.Ea_mean_R102 = st.mean(Ea_R102)
        
        elif self.Operation_mode == 5:
            #Optimization variables for R101
            t_exp = (self.TrainMode5["time"]*60).tolist()               #seconds
            C_exp_R101 = self.TrainMode5["Csus_exp_R101"].tolist()      #Kmol/m3 = mol/L
            Q_P104 = (self.TrainMode5["Q_P104"]/3600).tolist()          #L/s
            VR_exp_R101 = self.TrainMode5["Vol_R101"].tolist()          #L
            T_R101 = (self.TrainMode5["T_R101"] + 273.15).tolist()      #K
            Csus_in_R101 = (self.TrainMode5["Csus_in_R101"]).tolist()   #kmol/m3 = mol/L
            Q_P102 = (self.TrainMode5["Q_P102"]/3600).tolist()          #L/s
            K_R101 = []
            Ea_R101 = []
            
            #Optimization variables for R102
            C_exp_R102 = self.TrainMode5["Csus_exp_R102"].tolist()    #Kmol/m3 = mol/L
            Q_P101 = (self.TrainMode5["Q_P101"]/3600).tolist()        #L/s
            VR_exp_R102 = self.TrainMode5["Vol_R102"].tolist()          #L
            T_R102 = (self.TrainMode5["T_R102"]).tolist()             #K
            Csus_in_R102 = self.TrainMode5["Csus_exp_R101"].tolist()  #Kmol/m3 = mol/L
            K_R102 = []
            Ea_R102 = []
            
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                #Variables for R101
                C_exp_R101_opt = C_exp_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                VR_exp_R101_opt = VR_exp_R101[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Csus_in_R101_opt = Csus_in_R101[i : i+resolution]

                #Variables for R102
                C_exp_R102_opt = C_exp_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]
                VR_exp_R102_opt = VR_exp_R102[i : i+resolution]
                T_R102_opt = T_R102[i : i+resolution]

                #Optimization for R101
                Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_R101_opt, y0 = C_exp_R101_opt[0], VR = VR_exp_R101_opt,
                                                  temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_R101_opt,
                                                  Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_R101_opt, Operation = 1, K = self.K_mean_R101, Ea = self.Ea_mean_R101)
                
                K_R101.append(Opt_kinetic_params_R101.x[0])
                Ea_R101.append(Opt_kinetic_params_R101.x[1])
                
                #Optimization for R102
                Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_R102_opt, y0 = C_exp_R102_opt[0], VR = VR_exp_R102_opt,
                                                  temperatures = T_R102_opt, Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_R101_opt,
                                                  Qi2 = Q_P101_opt, Csus_in_i2 = C_exp_R101_opt, Operation = 1, K = self.K_mean_R102, Ea = self.Ea_mean_R102)
                
                K_R102.append(Opt_kinetic_params_R102.x[0])
                Ea_R102.append(Opt_kinetic_params_R102.x[1])

            #Kinetics for R101
            self.K_mean_R101 = st.mean(K_R101)
            self.Ea_mean_R101 = st.mean(Ea_R101)
    
    def OptimizationADM1 (self, resolution):
        
        def model_ADM1(C, t, K, VR, Q_func_1, Q_func_2, Csus_in_func_1, Csus_in_func_2, Operation):
            Q_1=Q_func_1(t)
            Q_2=Q_func_2(t)
            Csus_in_1 = Csus_in_func_1(t)
            Csus_in_2 = Csus_in_func_2(t)
            if Operation == 1:         #Without recirculation
                dCsus_dt = ((Q_1 / VR) * (Csus_in_1 - C)) - (C * K) / VR
            elif Operation == 2:       #two entrances
                dCsus_dt = (Q_1 * Csus_in_1)/VR + (Q_2 * Csus_in_2)/VR - ((Q_1 + Q_2)*C)/VR - (C * K) / VR
            elif Operation == 3:       #Auto-recirculation
                dCsus_dt = (Q_1 * Csus_in_1)/VR + (Q_2 * C)/VR - ((Q_1 + Q_2)*C)/VR - (C * K) / VR
            return dCsus_dt
        
        # Optimization function t: vector of experimental time, C_exp: sustrate experimental concentration, y0: Initial value, 
        def Optimization(t, C_exp, y0, VR, temperatures, Qi1, Csus_in_i1, Qi2, Csus_in_i2, Operation, K=1): 
            # Define the objective function to minimize
            def objective(params):
                K = params
                t_train = t

                #interpol the vectors according to experimental time
                T_func = lambda t: np.interp(t, t_train, temperatures)
                Q_func1 = lambda t: np.interp(t, t_train, Qi1)
                Q_func2 = lambda t: np.interp(t, t_train, Qi2)
                VR_func = lambda t: np.interp(t, t_train, VR)
                Csus_in1 = lambda t: np.interp(t, t_train, Csus_in_i1)
                Csus_in2 = lambda t: np.interp(t, t_train, Csus_in_i2)
                
                C_model = odeint(model_ADM1, y0, t, args = (K, VR_func, T_func, Q_func1, Q_func2, Csus_in1, Csus_in2, Operation)).flatten()

                squared_diff = np.sum((C_exp - C_model) ** 2)
                return squared_diff
            
            result = minimize(objective, [K], method = 'Nelder-Mead')
            return result
        
        if self.Operation_mode == 1:
            t_exp = (self.TrainMode1["time"]*60).tolist()   #seconds
            C_exp = self.TrainMode1["Csus_exp"].tolist()    #Kmol/m3 = mol/L
            VR_exp = self.TrainMode1["Vol"].tolist()        #L 
            Csus_in = self.TrainMode1["Csus_in"].to_list()  #mol/L
            T_R101 = (self.TrainMode1["T_R101"]+273.15).tolist()  #K     
            Q_P104 = (self.TrainMode1["Q_P104"]/3600).tolist()    #L/s 
            K = []
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt = C_exp[i : i+resolution]
                VR_exp_opt = VR_exp[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                Csus_in_opt = Csus_in[i : i + resolution]
                Opt_kinetic_params = Optimization(t = t_exp_opt, C_exp = C_exp_opt, y0 = C_exp_opt[0], VR = VR_exp_opt,
                                                  temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt,
                                                  Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_opt, Operation = 1, K = self.K_mean_R101)
                K.append(Opt_kinetic_params.x[0])
            
            self.K_mean_R101 = st.mean(K)
        
        elif self.Operation_mode == 2:
            t_exp = (self.TrainMode2["time"]*60).tolist()   #seconds
            C_exp = self.TrainMode2["Csus_exp"].tolist()    #Kmol/m3 = mol/L
            VR_exp = self.TrainMode2["Vol"].tolist()        #L 
            Csus_in = self.TrainMode2["Csus_in"].to_list()  #mol/L
            T_R101 = (self.TrainMode2["T_R101"]+273.15).tolist()  #K     
            Q_P104 = (self.TrainMode2["Q_P104"]/3600).tolist()    #L/s 
            K = []
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt = C_exp[i : i+resolution]
                VR_exp_opt = VR_exp[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                Csus_in_opt = Csus_in[i : i + resolution]
                Opt_kinetic_params = Optimization(t = t_exp_opt, C_exp = C_exp_opt, y0 = C_exp_opt[0], VR = VR_exp_opt,
                                                  temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt,
                                                  Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_opt, Operation = 1, K = self.K_mean_R101)
                K.append(Opt_kinetic_params.x[0])
            
            self.K_mean_R101 = st.mean(K)

        elif self.Operation_mode == 3:
            #Optimization variables for R101
            t_exp = (self.TrainMode3["time"]*60).tolist()               #seconds
            C_exp_R101 = self.TrainMode3["Csus_exp_R101"].tolist()      #Kmol/m3 = mol/L
            Q_P104 = (self.TrainMode3["Q_P104"]/3600).tolist()          #L/s
            VR_exp_R101 = self.TrainMode3["Vol_R101"].tolist()            #L
            T_R101 = (self.TrainMode3["T_R101"] + 273.15).tolist()      #K
            Csus_in_R101 = (self.TrainMode3["Csus_in_R101"]).tolist()   #kmol/m3 = mol/L
            K_R101 = []

            #Optimization variables R102
            C_exp_R102 = self.TrainMode3["Csus_exp_R102"].tolist()    #Kmol/m3 = mol/L
            Q_P101 = (self.TrainMode3["Q_P101"]/3600).tolist()        #L/s
            VR_exp_R102 = self.TrainMode3["Vol_R102"].tolist()          #L
            T_R102 = (self.TrainMode3["T_R102"]).tolist()             #K
            Csus_in_R102 = self.TrainMode3["Csus_exp_R101"].tolist()  #Kmol/m3 = mol/L
            K_R102 = []

            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                #Variables for R101
                C_exp_R101_opt = C_exp_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                VR_exp_R101_opt = VR_exp_R101[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Csus_in_R101_opt = Csus_in_R101[i : i+resolution]

                #Variables for R102
                C_exp_R102_opt = C_exp_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]
                VR_exp_R102_opt = VR_exp_R102[i : i+resolution]
                T_R102_opt = T_R102[i : i+resolution]

                #Optimization for R101
                Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_R101_opt, y0 = C_exp_R101_opt[0], VR = VR_exp_R101_opt,
                                                    temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_R101_opt,
                                                    Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_R101_opt, Operation = 1, K = self.K_mean_R101)
                
                K_R101.append(Opt_kinetic_params_R101.x[0])

                #Optimization for R102
                Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_R102_opt, y0 = C_exp_R102_opt[0], VR = VR_exp_R102_opt,
                                                  temperatures = T_R102_opt, Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_R101_opt,
                                                  Qi2 = Q_P101_opt, Csus_in_i2 = C_exp_R101_opt, Operation = 1, K = self.K_mean_R102)
                
                K_R102.append(Opt_kinetic_params_R102.x[0])

        elif self.Operation_mode == 4:
            #Optimization variables for R101
            t_exp = (self.TrainMode4["time"]*60).tolist()               #seconds
            C_exp_R101 = self.TrainMode4["Csus_exp_R101"].tolist()      #Kmol/m3 = mol/L
            Q_P104 = (self.TrainMode4["Q_P104"]/3600).tolist()          #L/s
            VR_exp_R101 = self.TrainMode4["Vol_R101"].tolist()          #L
            T_R101 = (self.TrainMode4["T_R101"] + 273.15).tolist()      #K
            Csus_in_R101 = (self.TrainMode4["Csus_in_R101"]).tolist()   #kmol/m3 = mol/L
            Q_P102 = (self.TrainMode4["Q_P102"]/3600).tolist()
            K_R101 = []
            
            #Optimization variables for R102
            C_exp_R102 = self.TrainMode4["Csus_exp_R102"].tolist()    #Kmol/m3 = mol/L
            Q_P101 = (self.TrainMode4["Q_P101"]/3600).tolist()        #L/s
            VR_exp_R102 = self.TrainMode4["Vol_R102"].tolist()          #L
            T_R102 = (self.TrainMode4["T_R102"]).tolist()             #K
            K_R102 = []
        
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                #Variables for R101
                C_exp_R101_opt = C_exp_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                VR_exp_R101_opt = VR_exp_R101[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Csus_in_R101_opt = Csus_in_R101[i : i+resolution]
                Q_P102_opt = Q_P102[i : i+resolution]
                
                #Variables for R102
                C_exp_R102_opt = C_exp_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]
                VR_exp_R102_opt = VR_exp_R102[i : i+resolution]
                T_R102_opt = T_R102[i : i+resolution]
                
                #optimization R101
                Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_R101_opt, y0 = C_exp_R101_opt[0], VR = VR_exp_R101_opt,
                                                  temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_R101_opt,
                                                  Qi2 = Q_P102_opt, Csus_in_i2 = Csus_in_R101_opt, Operation = 2, K = self.K_mean_R101)
                
                K_R101.append(Opt_kinetic_params_R101.x[0])
                
                #Optimization for R102
                Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_R102_opt, y0 = C_exp_R102_opt[0], VR = VR_exp_R102_opt,
                                                  temperatures = T_R102_opt, Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_R101_opt,
                                                  Qi2 = Q_P101_opt, Csus_in_i2 = C_exp_R101_opt, Operation = 1, K = self.K_mean_R102)
                
                K_R102.append(Opt_kinetic_params_R102.x[0])
            
            #Kinetics for R101
            self.K_mean_R101 = st.mean(K_R101)

            #Kinetics for R102
            self.K_mean_R102 = st.mean(K_R102)

        elif self.Operation_mode == 5:
            #Optimization variables for R101
            t_exp = (self.TrainMode5["time"]*60).tolist()               #seconds
            C_exp_R101 = self.TrainMode5["Csus_exp_R101"].tolist()      #Kmol/m3 = mol/L
            Q_P104 = (self.TrainMode5["Q_P104"]/3600).tolist()          #L/s
            VR_exp_R101 = self.TrainMode5["Vol_R101"].tolist()          #L
            T_R101 = (self.TrainMode5["T_R101"] + 273.15).tolist()      #K
            Csus_in_R101 = (self.TrainMode5["Csus_in_R101"]).tolist()   #kmol/m3 = mol/L
            Q_P102 = (self.TrainMode5["Q_P102"]/3600).tolist()          #L/s
            K_R101 = []
            
            #Optimization variables for R102
            C_exp_R102 = self.TrainMode5["Csus_exp_R102"].tolist()    #Kmol/m3 = mol/L
            Q_P101 = (self.TrainMode5["Q_P101"]/3600).tolist()        #L/s
            VR_exp_R102 = self.TrainMode5["Vol_R102"].tolist()          #L
            T_R102 = (self.TrainMode5["T_R102"]).tolist()             #K
            Csus_in_R102 = self.TrainMode5["Csus_exp_R101"].tolist()  #Kmol/m3 = mol/L
            K_R102 = []
            
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                #Variables for R101
                C_exp_R101_opt = C_exp_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                VR_exp_R101_opt = VR_exp_R101[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Csus_in_R101_opt = Csus_in_R101[i : i+resolution]

                #Variables for R102
                C_exp_R102_opt = C_exp_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]
                VR_exp_R102_opt = VR_exp_R102[i : i+resolution]
                T_R102_opt = T_R102[i : i+resolution]

                #Optimization for R101
                Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_R101_opt, y0 = C_exp_R101_opt[0], VR = VR_exp_R101_opt,
                                                  temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_R101_opt,
                                                  Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_R101_opt, Operation = 1, K = self.K_mean_R101)
                
                K_R101.append(Opt_kinetic_params_R101.x[0])
                
                #Optimization for R102
                Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_R102_opt, y0 = C_exp_R102_opt[0], VR = VR_exp_R102_opt,
                                                  temperatures = T_R102_opt, Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_R101_opt,
                                                  Qi2 = Q_P101_opt, Csus_in_i2 = C_exp_R101_opt, Operation = 1, K = self.K_mean_R102)
                
                K_R102.append(Opt_kinetic_params_R102.x[0])

            #Kinetics for R101
            self.K_mean_R101 = st.mean(K_R101)
            
            #Kinetics for R102
            self.K_mean_R102 = st.mean(K_R102)
    
    def OptimizationGompertz(self, resolution):
        
        def model_Gompertz(t, ym, U, L):
            y_t = ym * np.exp(-np.exp((U * np.e) / ym * (L - t) + 1))
            return y_t
        
        def Optimization_Gompertz(params, t, y_exp):
            ym, U, L = params
            y_pred = model_Gompertz(t, ym, U, L)
            residuals = y_exp - y_pred
            return np.sum(residuals**2)
        
        if self.Operation_mode == 1 or self.Operation_mode == 2:
            t_exp = self.TrainGompertzMode1["time"].tolist()
            y_exp = self.TrainGompertzMode1["y_t_exp"].tolist()
            ym = []
            U = []
            L = []
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i + resolution]
                y_exp_opt = y_exp[i : i + resolution]
                
                #Optimization Gompertz
                Results = Optimization_Gompertz(params = (self.ym_R101, self.U_R101, self.L_R101), t = t_exp_opt, y_exp = y_exp_opt)
                ym.append(Results.x[0])
                U.append(Results.x[1])
                L.append(Results.x[2])
            
            self.ym_R101 = st.mean(ym)
            self.U_R101 = st.mean(U)
            self.L_R101 = st.mean(L)
        
        elif self.Operation_mode == 3 or self.Operation_mode == 5:
            t_exp = self.TrainGompertzMode3_5["time"].tolist()
            y_exp_R101 = self.TrainGompertzMode3_5["y_t_exp_R101"].tolist()
            y_exp_R102 = self.TrainGompertzMode3_5["y_t_exp_R102"].tolist()
            ym_R101 = []
            U_R101 = []
            L_R101 = []
            ym_R102 = []
            U_R102 = []
            L_R102 = []
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i + resolution]
                y_exp_R101_opt = y_exp_R101[i : i + resolution]
                y_exp_R102_opt = y_exp_R102[i: i + resolution]
                #Optimization for R101
                results_R101 = Optimization_Gompertz(params = (self.ym_R101, self.U_R101, self.L_R101), t = t_exp_opt, y_exp = y_exp_R101_opt)
                #Optimization for R102
                results_R102 = Optimization_Gompertz(params = (self.ym_R102, self.U_R102, self.L_R102), t = t_exp_opt, y_exp = y_exp_R102_opt)
                #Storage Values for R101
                ym_R101.append(results_R101.x[0])
                U_R101.append(results_R101.x[1])
                L_R101.append(results_R101.x[2])
                #Storage values for R102
                ym_R102.append(results_R102.x[0])
                U_R102.append(results_R102.x[1])
                L_R102.append(results_R102.x[2])
            
            #Average params for Gompertz in R101
            self.ym_R101 = st.mean(ym_R101)
            self.U_R101 = st.mean(U_R101)
            self.L_R101 = st.mean(L_R101)
            
            #Average params for gompertz in R102
            self.ym_R102 = st.mean(ym_R102)
            self.U_R102 = st.mean(U_R102)
            self.L_R102 = st.mean(L_R102)
        
        elif self.Operation_mode == 4:
            t_exp = self.TrainGompertzMode4["time"].tolist()
            y_exp_R101 = self.TrainGompertzMode4["y_t_exp_R101"].tolist()
            y_exp_R102 = self.TrainGompertzMode4["y_t_exp_R102"].tolist()
            ym_R101 = []
            U_R101 = []
            L_R101 = []
            ym_R102 = []
            U_R102 = []
            L_R102 = []
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i + resolution]
                y_exp_R101_opt = y_exp_R101[i : i + resolution]
                y_exp_R102_opt = y_exp_R102[i: i + resolution]
                #Optimization for R101
                results_R101 = Optimization_Gompertz(params = (self.ym_R101, self.U_R101, self.L_R101), t = t_exp_opt, y_exp = y_exp_R101_opt)
                #Optimization for R102
                results_R102 = Optimization_Gompertz(params = (self.ym_R102, self.U_R102, self.L_R102), t = t_exp_opt, y_exp = y_exp_R102_opt)
                #Storage Values for R101
                ym_R101.append(results_R101.x[0])
                U_R101.append(results_R101.x[1])
                L_R101.append(results_R101.x[2])
                #Storage values for R102
                ym_R102.append(results_R102.x[0])
                U_R102.append(results_R102.x[1])
                L_R102.append(results_R102.x[2])
            
            #Average params for Gompertz in R101
            self.ym_R101 = st.mean(ym_R101)
            self.U_R101 = st.mean(U_R101)
            self.L_R101 = st.mean(L_R101)
            
            #Average params for gompertz in R102
            self.ym_R102 = st.mean(ym_R102)
            self.U_R102 = st.mean(U_R102)
            self.L_R102 = st.mean(L_R102)


#This will be the way to call method from API
#singletone
Training = TrainingBiogasPlant(ST_ini_R101 = 4.9, SV_ini_R101 = 1.5, t_train=60, Volume_V101 = 15) 
#Loop calling
while True:
    Training.getData()
    print("-------- Datos de interfaz")
    print(Training.Datainterfaz)
    print("------------Datos de planta")
    print(Training.DataPlant)
    Training.LimitReagentCalculation()
    Training.StochoimetricExpenditure()
    print(Training.TrainMode4)
    Training.OptimizationArrhenius(resolution=2)
    print(Training.K_mean_R101)
    print(Training.Ea_mean_R101)
    print(Training.K_mean_R102)
    print(Training.Ea_mean_R102)
    time.sleep(600)
      