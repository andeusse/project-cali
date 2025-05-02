import os
import sys
import time

# # Get the absolute path of the script
# script_dir = os.path.dirname(os.path.abspath(__file__))  

# # Set the working directory to the correct folder
# project_root = os.path.abspath(os.path.join(script_dir, "../../.."))  # Adjust based on folder structure
# v1_0_path = os.path.join(project_root, "v1.0")

# # Change working directory
# os.chdir(v1_0_path)  
# sys.path.insert(0, v1_0_path)  # Ensure it is the first in sys.path

# print(f"Running script in: {os.getcwd()}")
# print(f"Python path: {sys.path}")

from tools import DBManager
import pandas as pd
import numpy as np
from fractions import Fraction
from functools import reduce
from math import gcd
from scipy.integrate import odeint
from scipy.optimize import minimize
import statistics as st
from simulation_models.Biogas import ThermoProperties
from datetime import datetime
import math

class TrainingBiogasPlant:
    def __init__(self, t_train, ST_ini_R101, SV_ini_R101, Cc_R101, Ch_R101, Co_R101, Cn_R101, Cs_R101, rho_R101, Volume_V101 = 15,  
                 ST_ini_R102 = 2, SV_ini_R102 = 1.5, Cc_R102 = 27.36, Ch_R102 = 6.38, Co_R102 = 12.21, Cn_R102 = 3.04, Cs_R102 = 1.51, rho_R102 = 1000, 
                 Volume_V102 = 35, Volume_V107 = 35):
        #contenedor
        DB_IP = os.getenv('DB_IP')
        DB_Port = os.getenv('DB_Port')
        DB_Bucket = os.getenv('DB_Bucket')
        DB_Organization = os.getenv('DB_Organization')
        DB_Token = os.getenv('DB_Token')
        # #Universidad Santiago De Cali servidor
        # DB_IP = 'localhost'
        # DB_Port = '8086'
        # DB_Bucket = 'Laboratorio_Energias'
        # DB_Organization = 'USC'
        # DB_Token = '4pJB_298afu0WKjKBtPESjnUxvpJV0PODWBNMGzeeU_ahg1P4H3Bg5KOfwI2A9LXm2BQwaQR_un792HXy3bsvg=='
        # #Computador personal UCO
        # DB_IP = 'localhost'
        # DB_Port = '8086'
        # DB_Bucket = 'BiogasPlantSimulator'
        # DB_Organization = 'UCO'
        # DB_Token = 'PdISKZ9gcighknh3X66cqwB1FvOexgDh7KUHKlvWvuLyw3UZZGBd1fGBtZg3IBEkKZmcknzOtYBwmEpJzJl6GQ=='
        
        self.influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
        self.connectionState = self.influxDB.InfluxDBconnection()
        if not self.connectionState:
            return {"message":self.influxDB.ERROR_MESSAGE}, 503
        
        self.t_train = t_train
        
        #------Initial conditions for R101
        self.ST_ini_R101 = ST_ini_R101/100         #Initial condition for reactor
        self.SV_ini_R101 = SV_ini_R101/100         #Initial condition for reactor
        self.Cc_ini_R101 = Cc_R101             #Initial Concentration to charge R101
        self.Ch_ini_R101 = Ch_R101           
        self.Co_ini_R101 = Co_R101
        self.Cn_ini_R101 = Cn_R101
        self.Cs_ini_R101 = Cs_R101
        self.rho_ini_R101 = rho_R101  
        self.Vsus_inj_total_R101 = 0                 #Total substrate feed in R101
        
        self.molC_ini_R101 = self.Cc_ini_R101*(1/12.01)
        self.molH_ini_R101 = self.Ch_ini_R101*(1/1.01)
        self.molO_ini_R101 = self.Co_ini_R101*(1/16)
        self.molN_ini_R101 = self.Cn_ini_R101*(1/14)
        self.molS_ini_R101 = self.Cs_ini_R101*(1/32)

        #initial concentration inside reactor 101
        n_i_R101 = self.molC_ini_R101
        a_i_R101 = self.molH_ini_R101
        b_i_R101 = self.molO_ini_R101
        c_i_R101 = self.molN_ini_R101
        d_i_R101 = self.molS_ini_R101
        
        def lcm(a,b):
                return a * b // gcd(a, b)
        
        numbers = [n_i_R101, a_i_R101, b_i_R101, c_i_R101, d_i_R101]
        denominators = [Fraction(num).limit_denominator(10).denominator for num in numbers]
        common_denominator = reduce(lcm, denominators)
        self.subindex_R101 = [int(num * common_denominator) for num in numbers]

        n_ini_R101 = self.subindex_R101[0]
        a_ini_R101 = self.subindex_R101[1]
        b_ini_R101 = self.subindex_R101[2]
        c_ini_R101 = self.subindex_R101[3]
        d_ini_R101 = self.subindex_R101[4]

        #Initial molecular weight in R101    
        self.MW_inocum_ini_R101 = n_ini_R101*12.01 + a_ini_R101*1.01 + b_ini_R101*16 + c_ini_R101*14 + d_ini_R101*32

        #initial concentration in R101
        if self.ST_ini_R101 == 0:
            self.Csus_ini_ST_R101 = 0
            self.Csus_ini_SV_R101 = 0
            self.Csus_ini_fixed_R101 = 0
            self.MW_inocum_ini_R101 = 18         #molecular weight of the water  
        else:
            self.Csus_ini_ST_R101 = ((self.ST_ini_R101)*self.rho_ini_R101)/self.MW_inocum_ini_R101     #molST/L    
            self.Csus_ini_SV_R101 = ((self.SV_ini_R101)*self.rho_ini_R101)/self.MW_inocum_ini_R101     #molSV/L
            self.Csus_ini_SV_R101_gl = ((self.SV_ini_R101)*self.rho_ini_R101)
            self.Csus_ini_ST_R101_gl = ((self.ST_ini_R101)*self.rho_ini_R101)
            self.Csus_ini_fixed_R101 = self.Csus_ini_ST_R101 - self.Csus_ini_SV_R101  
        
        print("------initial concentrations SV [mol/L]", self.Csus_ini_SV_R101)
        print("------initial concentration ST[mol/L]---", self.Csus_ini_ST_R101)
        print("------initial concentration SV------", self.Csus_ini_SV_R101_gl)
        print("------initial concentration ST------", self.Csus_ini_ST_R101_gl)
        

        #-------Initial and constructive conditions for V101
        self.Pi_V101 = 0          #Is the biggest pressure in V101 before pressure in V101 drop
        self.Ptransfer_V101_to_V102 = 0    #Initially the pressure transfer to V102 is 0
        self.Pacum_V101_i = 0
        self.Pacum_V101 = 0
        self.Volume_V101 = Volume_V101     #Volume of the tank in Liters
        
        #-------Initial conditions for R102
        self.ST_ini_R102 = ST_ini_R102/100         #Initial condition for reactor
        self.SV_ini_R102 = SV_ini_R102/100         #Initial condition for reactor
        self.Cc_ini_R102 = Cc_R102             #Initial Concentration to charge R102
        self.Ch_ini_R102 = Ch_R102           
        self.Co_ini_R102 = Co_R102
        self.Cn_ini_R102 = Cn_R102
        self.Cs_ini_R102 = Cs_R102
        self.rho_ini_R102 = rho_R102 
        self.Vsus_inj_total_R102 = 0   

        self.molC_ini_R102 = self.Cc_ini_R102*(1/12.01)
        self.molH_ini_R102 = self.Ch_ini_R102*(1/1.01)
        self.molO_ini_R102 = self.Co_ini_R102*(1/16)
        self.molN_ini_R102 = self.Cn_ini_R102*(1/14)
        self.molS_ini_R102 = self.Cs_ini_R102*(1/32)

        #initial concentration inside reactor 102
        n_i_R102 = self.molC_ini_R102
        a_i_R102 = self.molH_ini_R102
        b_i_R102 = self.molO_ini_R102
        c_i_R102 = self.molN_ini_R102
        d_i_R102 = self.molS_ini_R102

        numbers = [n_i_R102, a_i_R102, b_i_R102, c_i_R102, d_i_R102]
        denominators = [Fraction(num).limit_denominator(10).denominator for num in numbers]
        common_denominator = reduce(lcm, denominators)
        self.subindex_R102 = [int(num * common_denominator) for num in numbers]

        n_ini_R102 = self.subindex_R102[0]
        a_ini_R102 = self.subindex_R102[1]
        b_ini_R102 = self.subindex_R102[2]
        c_ini_R102 = self.subindex_R102[3]
        d_ini_R102 = self.subindex_R102[4]

        #Initial molecular weight in R101    
        self.MW_inocum_ini_R102 = n_ini_R102*12.01 + a_ini_R102*1.01 + b_ini_R102*16 + c_ini_R102*14 + d_ini_R102*32

        #initial concentration inside reactor 102
        if self.ST_ini_R102 == 0:
            self.Csus_ini_ST_R102 = 0
            self.Csus_ini_SV_R102 = 0
            self.Csus_ini_fixed_R102 = 0
            self.MW_inocum_ini_R102 = 18
        else:
            self.Csus_ini_ST_R102 = ((self.ST_ini_R102/100)*rho_R102)/self.MW_inocum_ini_R102     ##18: molecular weight of water, this is for inoculum Units: mol/L
            self.Csus_ini_SV_R102 = ((self.SV_ini_R102/100)*rho_R102)/self.MW_inocum_ini_R102    #1000: Standar density of water   Units: mol/L - kmol/m3
            self.Csus_ini_fixed_R102 = self.Csus_ini_ST_R102 - self.Csus_ini_SV_R102
        
        #initial and constructive conditions for V102
        self.Pi_V102 = 0                   #Is the biggest pressure in V102 before pressure in V102 drop
        self.Volume_V102 = Volume_V102     #Volume of the tank in Liters
        self.Pacum_V102 = 0
        self.Pacum_V102_i = 0

        #Initial and constructive conditions for V107
        self.Pi_V107 = 0                   #Is the biggest pressure in V107 before pressure in V107 drop  
        self.Volume_V107 = Volume_V107     #Volume of the tank in liters 
        self.Pacum_V107 = 0 
        self.Pacum_V107_i = 0
        
        #Initial values for Arrhenius and ADM1
        self.K_mean_R101 = 1
        self.Ea_mean_R101 = 1
        self.K_mean_R102 = 1
        self.Ea_mean_R102 = 1
        
        #Initial values for Gompertz
        self.ym_R101 = 1
        self.U_R101 = 1
        self.L_R101 = 1
        self.ym_R102 = 1
        self.U_R102 = 1
        self.L_R102 = 1
        
        #Model train time for gompertz
        self.total_time = 0
        self.timeGompertz = []
        self.tp = 8               #min

        #Vessels for biogas storage
        #Thermodynamic model initilization
        self.Thermo = ThermoProperties.ThermoProperties()
        
    def getData (self):

        #Function to normalice time
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
        
        #Get data from User input plant plant
        attempts = 1
        while attempts <= 5:
            try:
                self.query1 = self.influxDB.QueryCreator(measurement="Planta_Biogas", device="interfaz", type=5)
                self.Datainterfaz = pd.concat(self.influxDB.InfluxDBreader(query = self.query1), ignore_index=True)
                # self.Datainterfaz = self.influxDB.InfluxDBreader(query = self.query1)
                self.Datainterfaz.set_index("_field", inplace = True)
                self.Operation_mode = self.Datainterfaz["_value"]["ciclo"]
                break
            except:
                attempts += 1
            
        #Get Asynchronous and synchronous Data
        attempts = 1
        while attempts <= 5:
            try:
                self.query2 = self.influxDB.QueryCreator(measurement="Planta_Biogas", train_time=str(self.t_train), type=4)
                # DataPlant = pd.concat(self.influxDB.InfluxDBreader(query = self.query2), ignore_index=True)
                DataPlant = self.influxDB.InfluxDBreader(query = self.query2)
                DataPlant.set_index("_field", inplace = True)
                self.DataPlanti = DataPlant
                break
            except:
                attempts += 1

        #get Mixers Data
        attempts = 1
        while attempts <= 5:
            try:
                self.query3 = self.influxDB.QueryCreator(measurement="Planta_Biogas", type=7)
                self.Mixers_df = self.influxDB.InfluxDBreader(query = self.query3)
                self.Mixers_df.set_index("_field", inplace = True)
                self.Mix_Velocity_TK100 = self.Mixers_df["_value"]["SE-107"]
                self.Mix_Velocity_R101 = self.Mixers_df["_value"]["SE-108"]
                self.Mix_Velocity_R102 = self.Mixers_df["_value"]["SE_109"]
                break
            except:
                attempts += 1

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
                "_time":time,
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

            #add asynchronous data Pumps
            P104_df = DataPlant.loc["FE-104",["_time", "_value"]]
            P104_df["_time"]=pd.to_datetime(P104_df["_time"])
            P104_df = P104_df.rename(columns={"_value": "FE-104"})
            self.DataPlant = pd.merge(self.DataPlant, P104_df, on="_time", how = "outer")
            self.DataPlant = self.DataPlant.sort_values(by = "_time")
            self.DataPlant.ffill(inplace=True)

            self.DataPlant["V_R101"] = self.DataPlant["V_R101"].fillna(self.DataPlant["V_R101"].mean())
            self.DataPlant["T_V101"] = self.DataPlant["T_V101"].fillna(self.DataPlant["T_V101"].mean())
            
            self.DataPlant.fillna(0, inplace = True)

            #normalice time in Dataplant
            time_norm = normaliceTime(self.DataPlant["_time"])
            self.DataPlant["normTime"] = time_norm

            if (self.DataPlant.iloc[0, 1:] == 0).all():
                self.DataPlant = self.DataPlant[1:].reset_index(drop = True)

            #Single values for frontend
            #P-104
            self.P104 = float(self.DataPlant["FE-104"].iloc[-1])
            # R101
            self.pH_R101 = float(self.DataPlant["PH_R101"].iloc[-1])
            self.T_R101 = float(self.DataPlant["Tprom_R101"].iloc[-1])

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
                "_time":time,
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
        
            # #### ----Asynchronous Data
            #add asynchronous data Pumps
            #P-104
            P104_df = DataPlant.loc["FE-104",["_time", "_value"]]
            P104_df["_time"]=pd.to_datetime(P104_df["_time"])
            P104_df = P104_df.rename(columns={"_value": "FE-104"})
            self.DataPlant = pd.merge(self.DataPlant, P104_df, on="_time", how = "outer")
            self.DataPlant = self.DataPlant.sort_values(by = "_time")
            self.DataPlant.ffill(inplace=True)
        
            #P-101
            P101_df = DataPlant.loc["P-101", ["_time","_value"]]
            P101_df["_time"]=pd.to_datetime(P101_df["_time"])
            P101_df = P101_df.rename(columns={"_value": "P-101"})
            self.DataPlant = pd.merge(self.DataPlant, P101_df, on="_time", how = "outer")
            self.DataPlant = self.DataPlant.sort_values(by = "_time")
            self.DataPlant.ffill(inplace=True)

            self.DataPlant["V_R101"] = self.DataPlant["V_R101"].fillna(self.DataPlant["V_R101"].mean())
            self.DataPlant["T_V101"] = self.DataPlant["T_V101"].fillna(self.DataPlant["T_V101"].mean())
            
            self.DataPlant.fillna(0, inplace = True)

            #normalice time in Dataplant
            time_norm = normaliceTime(self.DataPlant["_time"])
            self.DataPlant["normTime"] = time_norm

            if (self.DataPlant.iloc[0, 1:] == 0).all():
                self.DataPlant = self.DataPlant[1:].reset_index(drop = True)

            #Single values for frontend
            #P-104
            self.P104 = float(self.DataPlant["FE-104"].iloc[-1])
            #P-101
            self.P101 = float(self.DataPlant["P-101"].iloc[-1])
            # R101
            self.pH_R101 = float(self.DataPlant["PH_R101"].iloc[-1])
            self.T_R101 = float(self.DataPlant["Tprom_R101"].iloc[-1])
        
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
                "_time": time_norm,
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
        
            # #### ----Asynchronous Data
            #P-104
            P104_df = DataPlant.loc["FE-104",["_time", "_value"]]
            P104_df["_time"]=pd.to_datetime(P104_df["_time"])
            P104_df = P104_df.rename(columns={"_value": "FE-104"})
            self.DataPlant = pd.merge(self.DataPlant, P104_df, on="_time", how = "outer")
            self.DataPlant = self.DataPlant.sort_values(by = "_time")
            self.DataPlant.ffill(inplace=True)

            #P-101
            P101_df = DataPlant.loc["P-101",["_time", "_value"]]
            P101_df["_time"]=pd.to_datetime(P101_df["_time"])
            P101_df = P101_df.rename(columns={"_value": "P-101"})
            self.DataPlant = pd.merge(self.DataPlant, P101_df, on="_time", how = "outer")
            self.DataPlant = self.DataPlant.sort_values(by = "_time")
            self.DataPlant.ffill(inplace=True)

            self.DataPlant["V_R101"] = self.DataPlant["V_R101"].fillna(self.DataPlant["V_R101"].mean())
            self.DataPlant["T_V101"] = self.DataPlant["T_V101"].fillna(self.DataPlant["T_V101"].mean())

            self.DataPlant.fillna(0, inplace = True)

            #normalice time in Dataplant
            time_norm = normaliceTime(self.DataPlant["_time"])
            self.DataPlant["normTime"] = time_norm

            if (self.DataPlant.iloc[0, 1:] == 0).all():
                self.DataPlant = self.DataPlant[1:].reset_index(drop = True)

            #Single values for frontend
            #P104
            self.P104 = float(self.DataPlant["FE-104"].iloc[-1])
            #P101
            self.P101 = float(self.DataPlant["P-101"].iloc[-1])
            # R101
            self.pH_R101 = float(self.DataPlant["PH_R101"].iloc[-1])
            self.T_R101 = float(self.DataPlant["Tprom_R101"].iloc[-1])

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
                "_time": time_norm,
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
        
            # #### ----Asynchronous Data
            #P-104
            P104_df = DataPlant.loc["FE-104",["_time", "_value"]]
            P104_df["_time"]=pd.to_datetime(P104_df["_time"])
            P104_df = P104_df.rename(columns={"_value": "FE-104"})
            self.DataPlant = pd.merge(self.DataPlant, P104_df, on="_time", how = "outer")
            self.DataPlant = self.DataPlant.sort_values(by = "_time")
            self.DataPlant.ffill(inplace=True)

            #P-101
            P101_df = DataPlant.loc["P-101",["_time", "_value"]]
            P101_df["_time"]=pd.to_datetime(P101_df["_time"])
            P101_df = P101_df.rename(columns={"_value": "P-101"})
            self.DataPlant = pd.merge(self.DataPlant, P101_df, on="_time", how = "outer")
            self.DataPlant = self.DataPlant.sort_values(by = "_time")
            self.DataPlant.ffill(inplace=True)

            #P-102
            P102_df = DataPlant.loc["P-102", ["_time", "_value"]]
            P102_df["_time"]=pd.to_datetime(P102_df["_time"])
            P102_df = P102_df.rename(columns={"_value": "P-102"})
            self.DataPlant = pd.merge(self.DataPlant, P101_df, on="_time", how = "outer")
            self.DataPlant.ffill(inplace=True)

            self.DataPlant["V_R101"] = self.DataPlant["V_R101"].fillna(self.DataPlant["V_R101"].mean())
            self.DataPlant["T_V101"] = self.DataPlant["T_V101"].fillna(self.DataPlant["T_V101"].mean())
            self.DataPlant.fillna(0, inplace = True)

            #normalice time in Dataplant
            time_norm = normaliceTime(self.DataPlant["_time"])
            self.DataPlant["normTime"] = time_norm

            if (self.DataPlant.iloc[0, 1:] == 0).all():
                self.DataPlant = self.DataPlant[1:].reset_index(drop = True)

            #Single values for frontend
            #P104
            self.P104 = float(self.DataPlant["FE-104"].iloc[-1])
            #P101
            self.P101 = float(self.DataPlant["P-101"].iloc[-1])
            # R101
            self.pH_R101 = float(self.DataPlant["PH_R101"].iloc[-1])
            self.T_R101 = float(self.DataPlant["Tprom_R101"].iloc[-1])
            # P102
            self.P102 = float(self.DataPlant["P-102"].iloc[-1])

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
        self.Cst_sus_gl = (self.rho*(self.ST/100))
        self.Csv_sus = (self.rho*(self.SV/100))/self.MW_sustrato
        self.Csv_sus_gl = (self.rho*(self.SV/100))
        self.Cfixed = self.Cst_sus - self.Csv_sus

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
                        #initial values for biogas vessels
                        #V101
                        self.Pacum_V101_i = self.Pacum_V101_i
                        self.Pi_V101 = self.Pi_V101
                        self.Pacum_V101 = self.Pacum_V101
                        #V102
                        self.Pacum_V102_i = self.Pacum_V102_i
                        self.Pi_V102 = self.Pi_V102
                        self.Pacum_V102 = self.Pacum_V102
                        #V107
                        self.Pacum_V107_i = self.Pacum_V107_i
                        self.Pi_V107 = self.Pi_V107
                        self.Pacum_V107 = self.Pacum_V107
                        #Initial values for substrate concentration
                        self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                        self.Csus_ini_ST_R101 = self.Csus_ini_ST_R101
                        self.Vsus_inj_total_R101 = self.Vsus_inj_total_R101
                    
                    else:

                        self.Csus_ini_SV_R101 = self.TrainMode1["Csus_exp"].iloc[0]
                        self.Csus_ini_ST_R101 = self.TrainMode1["Csus_exp_ST"].iloc[0]
                        self.Vsus_inj_total_R101 = self.TrainMode1["Vsus_inj_R101"].iloc[0]
                        #initial values for biogas vessels in the other iteration
                        #V101
                        self.Pacum_V101_i = self.TrainMode1["Pacum_V101_i"].iloc[1]
                        self.Pi_V101 = self.TrainMode1["Pi_V101"].iloc[1]
                        self.Pacum_V101 = self.TrainMode1["Pacum_V101"].iloc[1]
                        #V102
                        self.Pacum_V102_i = self.TrainMode1["Pacum_V102_i"].iloc[1]
                        self.Pi_V102 = self.TrainMode1["Pi_V102"].iloc[1]
                        self.Pacum_V102 = self.TrainMode1["Pacum_V102"].iloc[1]
                        #V107
                        self.Pacum_V107_i = self.TrainMode1["Pacum_V102_i"].iloc[1]
                        self.Pi_V107 = self.TrainMode1["Pi_V107"].iloc[1]
                        self.Pacum_V107 = self.TrainMode1["Pacum_V107"].iloc[1]
                        
                else:

                    if self.TrainMode2.empty:
                        print("The DataFrame exists but is empty.")
                        #initial values for biogas vessels
                        #V101
                        self.Pacum_V101_i = self.Pacum_V101_i
                        self.Pi_V101 = self.Pi_V101
                        self.Pacum_V101 = self.Pacum_V101
                        #V102
                        self.Pacum_V102_i = self.Pacum_V102_i
                        self.Pi_V102 = self.Pi_V102
                        self.Pacum_V102 = self.Pacum_V102
                        #V107
                        self.Pacum_V107_i = self.Pacum_V107_i
                        self.Pi_V107 = self.Pi_V107
                        self.Pacum_V107 = self.Pacum_V107
                        #Initial values for substrate concentration
                        self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                        self.Csus_ini_ST_R101 = self.Csus_ini_ST_R101
                        self.Vsus_inj_total_R101 = self.Vsus_inj_total_R101
                        
                    else:

                        self.Csus_ini_SV_R101 = self.TrainMode2["Csus_exp"].iloc[0]  
                        self.Csus_ini_ST_R101 = self.TrainMode2["Csus_exp_ST"].iloc[0] 
                        self.Vsus_inj_total_R101 = self.TrainMode2["Vsus_inj_R101"].iloc[0]
                        #initial values for biogas vessels in the other iteration
                        #V101
                        self.Pacum_V101_i = self.TrainMode2["Pacum_V101_i"].iloc[1]
                        self.Pi_V101 = self.TrainMode2["Pi_V101"].iloc[1]
                        self.Pacum_V101 = self.TrainMode2["Pacum_V101"].iloc[1]
                        #V102
                        self.Pacum_V102_i = self.TrainMode2["Pacum_V102_i"].iloc[1]
                        self.Pi_V102 = self.TrainMode2["Pi_V102"].iloc[1]
                        self.Pacum_V102 = self.TrainMode2["Pacum_V102"].iloc[1]
                        #V107
                        self.Pacum_V107_i = self.TrainMode2["Pacum_V102_i"].iloc[1]
                        self.Pi_V107 = self.TrainMode2["Pi_V107"].iloc[1]
                        self.Pacum_V107 = self.TrainMode2["Pacum_V107"].iloc[1]

            except AttributeError:
                    print("The DataFrame does not exist.")
            
            # Create lists for TrainModel Dataframe 
            # R101           
            C_in_sus = []
            V = []
            Csus = []
            Csus_ST = []
            Q_P104v = []
            timev = []
            n_biogas_acum_Gompertz = []
            SV_g_Gompertz = []
            V_inj_R101 = []
            #Biogas storge
            #V101
            Pi_V101 = []
            Pacum_V101_i = []
            Pacum_V101 = []
            #V102
            Pi_V102 = []
            Pacum_V102_i = []
            Pacum_V102 = []
            #V107
            Pi_V107 = []
            Pacum_V107_i = []
            Pacum_V107 = []

            for i in range (len(self.DataPlant)):
                self.P_V101 = self.DataPlant["P_V101"].iloc[i]
                self.P_V102 = self.DataPlant["P_V102"].iloc[i]
                self.P_V107 = self.DataPlant["P_V107"].iloc[i]
                #conditions when the pressure inside V101 drop
                if i > 0:
                    if (i + 1) in self.DataPlant.index and i in self.DataPlant.index:
                        tp = self.DataPlant["normTime"].iloc[i+1] - self.DataPlant["normTime"].iloc[i]
                    else:
                        tp = 0
                    
                    Q_P104 = (self.DataPlant["FE-104"][i-1])/60                        #Convert[L/h] to [LPM]
                    #Conditions for estimation of accumulated pressure in V101
                    if self.P_V101 > 2:
                        if (self.P_V101*1.04) < (self.DataPlant["P_V101"].iloc[i-1]): 
                            print("Pressure drop")      
                            self.Pi_V101 = self.P_V101
                            self.Pacum_V101_i = self.Pacum_V101
                        
                    #Conditions for estimation of accumulated pressure in V102
                    if self.P_V102 > 2:
                        if (self.P_V102*1.04) < (self.DataPlant["P_V102"].iloc[i-1]):
                            self.Pi_V102 = self.P_V102
                            self.Pacum_V102_i = self.Pacum_V102
                    
                    #Conditions for estimation of accumulated pressure in V107
                    if self.P_V107 > 2:
                        if (self.P_V107*1.04) < (self.DataPlant["P_V107"].iloc[i-1]):
                            self.Pi_V107 = self.P_V107
                            self.Pacum_V107_i = self.Pacum_V107
                else:
                    tp = 0
                    Q_P104 = 0  #Flow of pump at the beginning
                    
                #Estimate the accumulated pressure
                #V101
                self.Pacum_V101 = self.Pacum_V101_i + (self.P_V101 - self.Pi_V101)
                Pacum_V101.append(self.Pacum_V101)
                Pi_V101.append(self.Pi_V101)
                Pacum_V101_i.append(self.Pacum_V101_i)
                #V102
                self.Pacum_V102 = self.Pacum_V102_i + (self.P_V102 - self.Pi_V102)
                Pacum_V102.append(self.Pacum_V102)
                Pi_V102.append(self.Pi_V102)
                Pacum_V102_i.append(self.Pacum_V102_i)
                #V107
                self.Pacum_V107 = self.Pacum_V107_i + (self.P_V107 - self.Pi_V107)
                Pacum_V107.append(self.Pacum_V107)
                Pi_V107.append(self.Pi_V107)
                Pacum_V107_i.append(self.Pacum_V107_i)

                #Estimate the Storage and accumulated mol of biogas
                # Storage biogas mol in V101
                self.T_V101_actual = self.DataPlant["T_V101"].iloc[i]
                if self.DataPlant["T_V101"].iloc[i] == 0:
                    self.T_V101_actual = self.DataPlant["T_V101"].iloc[i+1]

                self.n_biogas_sto_V101 = (((self.P_V101*6894.76) * (self.Volume_V101/1000))/
                                          (8.314 * (self.T_V101_actual + 273.15)))           #mol
                
                # Accumulated biogas mol in V101
                self.n_biogas_acum_V101 = (((self.Pacum_V101*6894.76) * (self.Volume_V101/1000))/
                                          (8.314 * (self.T_V101_actual + 273.15)))           #mol
                                
                n_biogas_acum_Gompertz.append(self.n_biogas_acum_V101)
                
                #Estimate the storage and accumulated mol for component in biogas
                #Storage compounds
                self.mol_sto_CH4_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_CH4_V101"].iloc[i]/100)      #mol
                self.mol_sto_CO2_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_CO2_V101"].iloc[i]/100)      #mol
                self.mol_sto_O2_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_O2_V101"].iloc[i]/100)        #mol
                self.mol_sto_H2S_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_H2S_V101"].iloc[i]/1000000)      #mol
                self.mol_sto_H2_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_H2_V101"].iloc[i]/1000000)        #mol
            
                #Accumulated compounds
                self.mol_acum_CH4_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_CH4_V101"].iloc[i]/100)     #mol
                self.mol_acum_CO2_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_CO2_V101"].iloc[i]/100)      #mol
                self.mol_acum_O2_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_O2_V101"].iloc[i]/100)        #mol
                self.mol_acum_H2S_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_H2S_V101"].iloc[i]/1000000)      #mol
                self.mol_acum_H2_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_H2_V101"].iloc[i]/1000000)       #mol
                
                #Stochoimetric expenditure
                #fraction inoculum/substrate
                self.Level_R101_actual = self.DataPlant["V_R101"].iloc[i]
                
                if self.Level_R101_actual == 0 or pd.isna(self.Level_R101_actual):
                    self.Level_R101_actual = self.DataPlant["V_R101"].iloc[i+1]
                
                self.Vsus_inj_total_R101 = self.Vsus_inj_total_R101 + (Q_P104 * tp)
                if self.Vsus_inj_total_R101 >= 30:
                    x_substrate = 1
                    x_inoculum = 0
                else:
                    x_substrate = self.Vsus_inj_total_R101/ self.Level_R101_actual
                    x_inoculum = (1 - x_substrate)
                
                #Volatile solids
                mol_ini = self.Csus_ini_SV_R101 * (self.Level_R101_actual)                            #mol
                mol_in_R101 = Q_P104 * tp * self.Csv_sus                                              #mol
                if x_substrate == 0:
                    mol_expended = 0
                else: 
                    mol_expended = (self.mol_acum_CH4_V101) * (1/(x_substrate*self.s_CH4))            #mol
                mol_out_R101 = (Q_P104 * tp * self.Csus_ini_SV_R101)   
                self.Csus_ini_SV_R101 = (mol_ini + mol_in_R101 - mol_out_R101 - mol_expended)/(self.Level_R101_actual)    #mol/L
                self.SV_g = self.Csus_ini_SV_R101 * (self.MW_sustrato*x_substrate + self.MW_inocum_ini_R101*x_inoculum) * self.Level_R101_actual              #Volatile solids g
                SV_g_Gompertz.append(self.SV_g)                                                                 #storage grams of volatile solids  
                # print("molin:", mol_in_R101)
                # print("molini: ", mol_ini)
                # print("mol expended", mol_expended)
                # print("mol out", mol_out_R101)
                #Total solids
                mol_ini_ST = self.Csus_ini_ST_R101 * (self.Level_R101_actual)                         #mol
                mol_in_R101_ST = Q_P104 * tp * self.Cst_sus                                           #mol
                mol_out_R101_ST = (Q_P104 * tp * self.Csus_ini_ST_R101)
                self.Csus_ini_ST_R101 = (mol_ini_ST + mol_in_R101_ST  - mol_out_R101_ST - mol_expended)/(self.Level_R101_actual)                                    #mol/L
                self.ST_g = self.Csus_ini_ST_R101 * (self.MW_sustrato*x_substrate + self.MW_inocum_ini_R101*x_inoculum) * self.Level_R101_actual                    #Total solids g
                
                timev.append(self.DataPlant["normTime"].iloc[i])
                V.append(self.Level_R101_actual)
                Q_P104v.append(Q_P104)   
                C_in_sus.append(self.Csv_sus)
                if math.isnan(self.Csus_ini_SV_R101):
                    Csus.append(Csus[-1])
                else:
                    Csus.append(self.Csus_ini_SV_R101)
                if math.isnan(self.Csus_ini_ST_R101):
                    Csus_ST.append(Csus_ST[-1])
                else:
                    Csus_ST.append(self.Csus_ini_ST_R101)
                V_inj_R101.append(self.Vsus_inj_total_R101)
            
            #DataFrame to realize optimization
            if self.Operation_mode == 1:
                self.TrainMode1 = pd.DataFrame({"time": timev,
                                                "Vol": V,
                                                "Q_P104": Q_P104v,
                                                "Csus_in": C_in_sus,
                                                "Csus_exp":Csus,
                                                "Csus_exp_ST":Csus_ST,
                                                "Vsus_inj_R101":V_inj_R101,
                                                "T_R101": self.DataPlant["Tprom_R101"],
                                                "Pacum_V101_i": Pacum_V101_i,
                                                "Pi_V101": Pi_V101,
                                                "Pacum_V101": Pacum_V101,
                                                "Pacum_V102_i": Pacum_V102_i,
                                                "Pi_V102": Pi_V102,
                                                "Pacum_V102": Pacum_V102,
                                                "Pacum_V107_i": Pacum_V107_i,
                                                "Pi_V107": Pi_V107,
                                                "Pacum_V107": Pacum_V107
                                                })
                tp_global_OC = self.TrainMode1["time"].iloc[-1] - self.TrainMode1["time"].iloc[0]
            else:
                self.TrainMode2 = pd.DataFrame({"time": timev,
                                                "Vol": V,
                                                "Q_P104": Q_P104v,
                                                "Csus_in": C_in_sus,
                                                "Csus_exp":Csus,
                                                "Csus_exp_ST":Csus_ST,
                                                "Vsus_inj_R101":V_inj_R101,
                                                "T_R101": self.DataPlant["Tprom_R101"],
                                                "Q_P101": (self.DataPlant["P-101"]/60).tolist(),
                                                "Pacum_V101_i": Pacum_V101_i,
                                                "Pi_V101": Pi_V101,
                                                "Pacum_V101": Pacum_V101,
                                                "Pacum_V102_i": Pacum_V102_i,
                                                "Pi_V102": Pi_V102,
                                                "Pacum_V102": Pacum_V102,
                                                "Pacum_V107_i": Pacum_V107_i,
                                                "Pi_V107": Pi_V107,
                                                "Pacum_V107": Pacum_V107
                                                })
                tp_global_OC = self.TrainMode2["time"].iloc[-1] - self.TrainMode2["time"].iloc[0]
            
            #Data to train Gompertz model in operation Model 1
            self.Model = Model
            if self.Model == "Gompertz":
                V_biogas_gompertz = []
                for i in range (len(n_biogas_acum_Gompertz)):
                    V_bio = (((V_biogas_gompertz[i]*8.314 * 273.15)/(100)*1000))/SV_g_Gompertz[i]         #Normal volume of biogas according to produce moles in V_101 (L/gSV)
                    V_biogas_gompertz.append(V_bio)
                self.TrainGompertzMode1 = pd.DataFrame({"time": self.timeGompertz[-len(self.DataPlant):],
                                                        "y_t_exp": V_biogas_gompertz})
            
            #Estimated variables to sent to frontEnd
            self.Csus_SV_R01 = self.Csus_ini_SV_R101 * (self.MW_sustrato*x_substrate + self.MW_inocum_ini_R101*x_inoculum)
            self.SV_R101 = ((self.Csus_SV_R01)/(self.rho*x_substrate + self.rho_ini_R101*x_inoculum))*100
            self.Csus_ST_R101 = self.Csus_ini_ST_R101 * (self.MW_sustrato*x_substrate + self.MW_inocum_ini_R101*x_inoculum)
            self.ST_R01 = ((self.Csus_ST_R101)/(self.rho*x_substrate + self.rho_ini_R101*x_inoculum))*100
            self.x_R101 = (abs(self.Cst_sus - self.Csus_ini_SV_R101)/self.Cst_sus) * 100
            self.OC_R101 = self.Csus_SV_R01/(tp_global_OC/1440)
            self.TrainMode2.to_csv("Train2.csv")
            
        #---------------------------------------------
        #--------- Variables to train Operation Mode 3 or 5
        if self.Operation_mode == 3 or self.Operation_mode == 5:
            # Methane produce by R101 using V101 storage
            #Set initial value from previuos layer
            try:
                if self.Operation_mode == 3:
                    if self.TrainMode3.empty:
                        print("The DataFrame exists but is empty.")
                        #initial values for biogas vessels
                        #V101
                        self.Pacum_V101_i = self.Pacum_V101_i
                        self.Pi_V101 = self.Pi_V101
                        self.Pacum_V101 = self.Pacum_V101
                        #V102
                        self.Pacum_V102_i = self.Pacum_V102_i
                        self.Pi_V102 = self.Pi_V102
                        self.Pacum_V102 = self.Pacum_V102
                        #V107
                        self.Pacum_V107_i = self.Pacum_V107_i
                        self.Pi_V107 = self.Pi_V107
                        self.Pacum_V107 = self.Pacum_V107
                        #Initial values for substrate concentration in R101
                        self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                        self.Csus_ini_ST_R101 = self.Csus_ini_ST_R101
                        self.Vsus_inj_total_R101 = self.Vsus_inj_total_R101
                        #Initial values for substrate concentration in R102
                        self.Csus_ini_SV_R102 = self.Csus_ini_SV_R102
                        self.Csus_ini_ST_R102 = self.Csus_ini_ST_R102
                        self.Vsus_inj_total_R102 = self.Vsus_inj_total_R102

                    else:
                        #initial values for substrate concentration in R101
                        self.Csus_ini_SV_R102 = self.TrainMode3["Csus_exp_R101"].iloc[0]
                        self.Csus_ini_ST_R101 = self.TrainMode3["Csus_exp_ST_R101"].iloc[0]
                        self.Vsus_inj_total_R101 = self.TrainMode3["Vsus_inj_R101"].iloc[0]
                        #Initial values for substrate concentration in R102
                        self.Csus_ini_SV_R102 = self.TrainMode1["Csus_exp_R102"].iloc[0]
                        self.Csus_ini_ST_R102 = self.TrainMode1["Csus_exp_ST_R102"].iloc[0]
                        self.Vsus_inj_total_R102 = self.TrainMode1["Vsus_inj_R102"].iloc[0]
                        #initial values for biogas vessels in the other iteration
                        #V101
                        self.Pacum_V101_i = self.TrainMode1["Pacum_V101_i"].iloc[1]
                        self.Pi_V101 = self.TrainMode1["Pi_V101"].iloc[1]
                        self.Pacum_V101 = self.TrainMode1["Pacum_V101"].iloc[1]
                        #V102
                        self.Pacum_V102_i = self.TrainMode1["Pacum_V102_i"].iloc[1]
                        self.Pi_V102 = self.TrainMode1["Pi_V102"].iloc[1]
                        self.Pacum_V102 = self.TrainMode1["Pacum_V102"].iloc[1]
                        #V107
                        self.Pacum_V107_i = self.TrainMode1["Pacum_V102_i"].iloc[1]
                        self.Pi_V107 = self.TrainMode1["Pi_V107"].iloc[1]
                        self.Pacum_V107 = self.TrainMode1["Pacum_V107"].iloc[1]

                else:
                    if self.TrainMode5.empty:
                        print("The DataFrame exists but is empty.")
                        #initial values for biogas vessels
                        #V101
                        self.Pacum_V101_i = self.Pacum_V101_i
                        self.Pi_V101 = self.Pi_V101
                        self.Pacum_V101 = self.Pacum_V101
                        #V102
                        self.Pacum_V102_i = self.Pacum_V102_i
                        self.Pi_V102 = self.Pi_V102
                        self.Pacum_V102 = self.Pacum_V102
                        #V107
                        self.Pacum_V107_i = self.Pacum_V107_i
                        self.Pi_V107 = self.Pi_V107
                        self.Pacum_V107 = self.Pacum_V107
                        #Initial values for substrate concentration in R101
                        self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                        self.Csus_ini_ST_R101 = self.Csus_ini_ST_R101
                        self.Vsus_inj_total_R101 = self.Vsus_inj_total_R101
                        #Initial values for substrate concentration in R102
                        self.Csus_ini_SV_R102 = self.Csus_ini_SV_R102
                        self.Csus_ini_ST_R102 = self.Csus_ini_ST_R102
                        self.Vsus_inj_total_R102 = self.Vsus_inj_total_R102
                    else:
                        #initial values for substrate concentration in R101
                        self.Csus_ini_SV_R102 = self.TrainMode3["Csus_exp_R101"].iloc[0]
                        self.Csus_ini_ST_R101 = self.TrainMode3["Csus_exp_ST_R101"].iloc[0]
                        self.Vsus_inj_total_R101 = self.TrainMode3["Vsus_inj_R101"].iloc[0]
                        #Initial values for substrate concentration in R102
                        self.Csus_ini_SV_R102 = self.TrainMode1["Csus_exp_R102"].iloc[0]
                        self.Csus_ini_ST_R102 = self.TrainMode1["Csus_exp_ST_R102"].iloc[0]
                        self.Vsus_inj_total_R102 = self.TrainMode1["Vsus_inj_R102"].iloc[0]
                        #initial values for biogas vessels in the other iteration
                        #V101
                        self.Pacum_V101_i = self.TrainMode1["Pacum_V101_i"].iloc[1]
                        self.Pi_V101 = self.TrainMode1["Pi_V101"].iloc[1]
                        self.Pacum_V101 = self.TrainMode1["Pacum_V101"].iloc[1]
                        #V102
                        self.Pacum_V102_i = self.TrainMode1["Pacum_V102_i"].iloc[1]
                        self.Pi_V102 = self.TrainMode1["Pi_V102"].iloc[1]
                        self.Pacum_V102 = self.TrainMode1["Pacum_V102"].iloc[1]
                        #V107
                        self.Pacum_V107_i = self.TrainMode1["Pacum_V102_i"].iloc[1]
                        self.Pi_V107 = self.TrainMode1["Pi_V107"].iloc[1]
                        self.Pacum_V107 = self.TrainMode1["Pacum_V107"].iloc[1]
            except AttributeError:
                    print("The DataFrame does not exist.")
            
            # Create lists for TrainModel Dataframe
            
            # General variables
            timev = []

            # #Biogas storge
            #V101
            Pi_V101 = []
            Pacum_V101_i = []
            Pacum_V101 = []
            #V102
            Pi_V102 = []
            Pacum_V102_i = []
            Pacum_V102 = []
            #V107
            Pi_V107 = []
            Pacum_V107_i = []
            Pacum_V107 = []    
            #pump 104 
            Q_P104v = []
            # R101  
            V_R101 = []                             #Liquid volume in R101     
            C_in_sus_R101 = []                      #VS inlet
            Csus_R101 = []                          #VS inside the reactor
            Csus_ST_R101 = []                       #TS inside the reactor
            
            n_biogas_acum_Gompertz_R101 = []        #biogas mol produced by R101    
            V_inj_R101 = []
            
            # R102
            C_in_sus_R102 = []
            
            V_R102 = []
            
            
            Csus_R102 = []
            Csus_ST_R102 = []
            
            Q_P101v = []
            
            n_biogas_acum_Gompertz_R102 = []
            SV_g_Gompertz_R101 = []
            SV_g_Gompertz_R102 = []
            
            V_inj_R102 = []
            self.Pi_V101 = 0
            self.Pi_V102 = 0
            self.Pi_V107 = 0
            PacumV101 = []
            PacumV102 = []
            PacumV107 = []
            self.Pacum_V101 = 0
            self.Pacum_V102 = 0
            self.Pacum_V107 = 0

            for i in range (len(self.DataPlant)):
                self.P_V101 = self.DataPlant["P_V101"].iloc[i]
                self.P_V102 = self.DataPlant["P_V102"].iloc[i]
                self.P_V107 = self.DataPlant["P_V107"].iloc[i]

                #conditions when the pressure inside Vessels drop
                if i > 0:
                    if (i + 1) in self.DataPlant.index and i in self.DataPlant.index:
                        tp = self.DataPlant["normTime"][i+1] - self.DataPlant["normTime"][i]
                    else:
                        tp = 0
                    Q_P104 = self.DataPlant["FE-104"][i-1]/60
                    Q_P101 = self.DataPlant["P-101"][i-1]/60
                    #Conditions for estimation of accumulated pressure in V101
                    if (self.P_V101*1.25) < (self.DataPlant["P_V101"].iloc[i-1]): 
                        print("Pressure drop")      
                        self.Pi_V101 = self.P_V101
                        self.Pacum_V101_i = self.Pacum_V101
                        if "_value" in self.DataPlanti and "BV-129" in self.DataPlanti["_value"]:
                            self.Ptransfer_V101_to_V102 = self.Pacum_V101_i - self.Pi_V101

                    #Conditions for estimation of accumulated pressure in V102
                    if (self.P_V102*1.25) < (self.DataPlant["P_V102"].iloc[i-1]):
                        self.Pi_V102 = self.P_V102
                        self.Pacum_V102_i = self.Pacum_V102
                    
                    #Conditions for estimation of accumulated pressure in V107
                    if (self.P_V107*1.25) < (self.DataPlant["P_V107"].iloc[i-1]):
                        self.Pi_V107 = self.P_V107
                        self.Pacum_V107_i = self.Pacum_V107
                else:
                    tp = 0
                    Q_P104 = 0  #Flow of pump at the beginning
                    Q_P101 = 0
                    Q_P102 = 0
                    
                #Estimate the accumulated pressure
                #V101
                self.Pacum_V101 = self.Pacum_V101_i + (self.P_V101 - self.Pi_V101)
                Pacum_V101.append(self.Pacum_V101)
                Pi_V101.append(self.Pi_V101)
                Pacum_V101_i.append(self.Pacum_V101_i)
                #V102
                self.Pacum_V102 = self.Pacum_V102_i + (self.P_V102 - self.Pi_V102)
                Pacum_V102.append(self.Pacum_V102)
                Pi_V102.append(self.Pi_V102)
                Pacum_V102_i.append(self.Pacum_V102_i)
                #V107
                self.Pacum_V107 = self.Pacum_V107_i + (self.P_V107 - self.Pi_V107)
                Pacum_V107.append(self.Pacum_V107)
                Pi_V107.append(self.Pi_V107)
                Pacum_V107_i.append(self.Pacum_V107_i)
                                
                #Estimate the Storage and accumulated mol of biogas in V101
                # Storage biogas mol in V101
                self.n_biogas_sto_V101 = (((self.P_V101*6894.76) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"].iloc[i] + 273.15)))           #mol
                
                # Accumulated biogas mol in V101
                self.n_biogas_acum_V101 = (((self.Pacum_V101*6894.76) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"].iloc[i] + 273.15)))           #mol
                n_biogas_acum_Gompertz_R101.append(self.n_biogas_acum_V101)                           #Total mol of biogas produced by R101

                #Estimate the Storage and accumulated mol of biogas in V102
                # Storage biogas mol in V102
                self.n_biogas_sto_V102 = (((self.P_V102*6894.76) * (self.Volume_V102/1000))/
                                          (8.314 * (self.DataPlant["T_V102"].iloc[i] + 273.15)))           #mol
                # Accumulated biogas mol in V102
                self.n_biogas_acum_V102 = (((self.Pacum_V102*6894.76) * (self.Volume_V102/1000))/     
                                          (8.314 * (self.DataPlant["T_V102"].iloc[i] + 273.15)) - 
                                          (((self.Ptransfer_V101_to_V102*6894.76) * (self.Volume_V101/1000))/
                                          (8.314 * (self.DataPlant["T_V101"].iloc[i] + 273.15))))           #mol
                
                #Estimate the Storage and accumulated mol of biogas in V107
                # Storage biogas mol in V107
                self.n_biogas_sto_V107 = (((self.P_V107*6894.76) * (self.Volume_V107/1000))/
                                          (8.314 * (self.DataPlant["T_V107"].iloc[i] + 273.15)))           #mol
                # Accumulated biogas mol in V102
                self.n_biogas_acum_V107 = (((self.Pacum_V107*6894.76) * (self.Volume_V102/1000))/
                                          (8.314 * (self.DataPlant["T_V102"].iloc[i] + 273.15)))
                                          
                
                n_biogas_acum_Gompertz_R102.append(self.n_biogas_acum_V102)
                
                #------- Mass balance in R101 according with biogas produced
                #Estimate the storage and accumulated mol for component in biogas in V101
                #Storage compounds in V101
                self.mol_sto_CH4_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_CH4_V101"].iloc[i]      #kmol
                self.mol_sto_CO2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_CO2_V101"].iloc[i]      #kmol
                self.mol_sto_O2_V101 = self.n_biogas_sto_V101 *  self.DataPlant["x_O2_V101"].iloc[i]        #kmol
                self.mol_sto_H2S_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_H2S_V101"].iloc[i]/1000000)      #kmol
                self.mol_sto_H2_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_H2_V101"].iloc[i]/1000000)        #kmol
                #Accumulated compounds in V101
                self.mol_acum_CH4_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CH4_V101"].iloc[i]      #kmol
                self.mol_acum_CO2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CO2_V101"].iloc[i]      #kmol
                self.mol_acum_O2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_O2_V101"].iloc[i]        #kmol
                self.mol_acum_H2S_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_H2S_V101"].iloc[i]/1000000)      #kmol
                self.mol_acum_H2_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_H2_V101"].iloc[i]/1000000)        #kmol
                
                #Stochoimetric expenditure in R101
                #fraction inoculum/substrate
                self.Level_R101_actual = self.DataPlant["V_R101"].iloc[i]
                if self.Level_R101_actual == 0 or pd.isna(self.Level_R101_actual):
                    self.Level_R101_actual = self.DataPlant["V_R101"].iloc[i+1]
                
                self.Vsus_inj_total_R101 = self.Vsus_inj_total_R101 + (Q_P104 * tp)
                if self.Vsus_inj_total_R101 >= 30:
                    x_substrate_R101 = 1
                    x_inoculum_R101 = 0
                else:
                    Vtotal_R101 = self.Vsus_inj_total_R101 + self.Level_R101_actual
                    x_inoculum_R101 = self.Level_R101_actual / Vtotal_R101
                    x_substrate_R101 = self.Vsus_inj_total_R101/ Vtotal_R101
                
                #mol organic compound
                #Volatile solids
                mol_ini_R101 = self.Csus_ini_SV_R101 * self.DataPlant["V_R101"].iloc[i]
                mol_in_R101 = Q_P104 * tp * self.Csv_sus
                mol_expended_R101 = self.mol_acum_CH4_V101 * (1/self.s_CH4)
                mol_out_R101 = (Q_P104 * tp * self.Csus_ini_SV_R101)
                self.Csus_ini_SV_R101 = (mol_ini_R101 + mol_in_R101 - mol_out_R101 - mol_expended_R101)/(self.DataPlant["V_R101"].iloc[i])
                self.SV_g_R101 = self.Csus_ini_SV_R101 * (self.MW_sustrato * x_substrate_R101 + self.MW_inocum_ini_R101 * x_inoculum_R101) * self.DataPlant["V_R101"].iloc[i]         #Volatile solids g
                SV_g_Gompertz.append(self.SV_g_R101)                                                            #storage grams of volatile solids  
                  
                #Total solids
                mol_ini_R101_ST = self.Csus_ini_ST_R101 * self.DataPlant["V_R101"].iloc[i]
                mol_in_R101_ST = Q_P104 * tp * self.Cst_sus
                mol_out_R101_ST =  Q_P104 * tp * self.Csus_ini_ST_R101
                self.Csus_ini_ST_R101 = (mol_ini_R101_ST + mol_in_R101_ST - mol_out_R101_ST - mol_expended_R101)/(self.DataPlant["V_R101"][i])

                timev.append(self.DataPlant["normTime"][i])
                V_R101.append(self.DataPlant["V_R101"][i])
                Q_P104v.append(Q_P104)
                C_in_sus_R101.append(self.Csv_sus)
                if math.isnan(self.Csus_ini_SV_R101):
                    Csus_R101.append(Csus_R101[-1])
                else:
                    Csus_R101.append(self.Csus_ini_SV_R101)
                if math.isnan(self.Csus_ini_ST_R101):
                    Csus_ST_R101.append(Csus_ST_R101[-1])
                else:
                    Csus_ST_R101.append(self.Csus_ini_ST_R101)
            
                #Estimate the storage and accumulated mol for component in biogas in V102
                #Storage compounds in V102
                self.mol_sto_CH4_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_CH4_V102"].iloc[i]      #kmol
                self.mol_sto_CO2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_CO2_V102"].iloc[i]      #kmol
                self.mol_sto_O2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_O2_V102"].iloc[i]        #kmol
                self.mol_sto_H2S_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_H2S_V102"].iloc[i]      #kmol
                self.mol_sto_H2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_H2_V102"].iloc[i]        #kmol
                #Accumulated compounds in V102
                self.mol_acum_CH4_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_CH4_V102"].iloc[i]      #kmol
                self.mol_acum_CO2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_CO2_V102"].iloc[i]      #kmol
                self.mol_acum_O2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_O2_V102"].iloc[i]        #kmol
                self.mol_acum_H2S_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_H2S_V102"].iloc[i]      #kmol
                self.mol_acum_H2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_H2_V102"].iloc[i]        #kmol
                
                #Stochoimetric expenditure in R102
                self.Vsus_inj_total_R102 = self.Vsus_inj_total_R102 + (Q_P101 * tp)
                if self.Vsus_inj_total_R102 >= 30:
                    x_substrate_R102 = 1
                    x_inoculum_R102 = 0
                else:
                    Vtotal_R102 = self.Vsus_inj_total_R102 + self.DataPlant.iloc["V_R102"][i]
                    x_inoculum_R102 = self.DataPlant["V_R102"].iloc[i] / Vtotal_R102
                    x_substrate_R102 = self.Vsus_inj_total_R102/ Vtotal_R102
                #mol organic compound (Volatile solids)
                mol_ini_R102 = self.Csus_ini_SV_R102 * self.DataPlant["V_R102"][i]
                mol_in_R102 = Q_P101 * tp * Csus_R101[-1]
                mol_expended_R102 = self.mol_acum_CH4_V102 * (1/self.s_CH4)
                mol_out_R102 = Q_P101 * tp * self.Csus_ini_SV_R102
                self.Csus_ini_SV_R102 = (mol_ini_R102 + mol_in_R102 - mol_out_R102 - mol_expended_R102)/(self.DataPlant["V_R102"][i])
                self.SV_g_R102 = self.Csus_ini_SV_R102 * (self.MW_sustrato * x_substrate_R102 + self.MW_inocum_ini_R102 * x_inoculum_R102) * self.DataPlant["V_R102"][i]              #Volatile solids g
                SV_g_Gompertz_R102.append(self.SV_g_R102)                                                                 #storage grams of volatile solids  
                                    
                #Total Solids
                mol_ini_R102_ST = self.Csus_ini_SV_R102 * self.DataPlant["V_R102"][i]
                mol_in_R102_ST = Q_P101 *  tp * Csus_ST_R101[-1]
                mol_out_R102_ST = Q_P101 *  tp * self.Csus_ini_SV_R102
                self.Csus_ini_ST_R102 = (mol_ini_R102_ST + mol_in_R102_ST - mol_out_R102_ST - mol_expended_R102)/(self.DataPlant["V_R102"][i])

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
        
            #Estimated variables to sent to frontEnd
            #R101
            self.Csus_SV_R101 = self.Csus_ini_SV_R101 / (self.MW_sustrato * x_substrate + self.MW_inocum_ini_R101 * x_inoculum)   #[g/L]
            self.SV_R101 = (self.Csus_SV_R101 / (self.rho * x_substrate_R101 + self.rho_ini_R101 * x_inoculum_R101))*100          #[%]
            
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
                self.mol_sto_H2S_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_H2S_V101"][i]/1000000)      #kmol
                self.mol_sto_H2_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_H2_V101"][i]/1000000)        #kmol
                #Accumulated compounds in V101
                self.mol_acum_CH4_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CH4_V101"][i]      #kmol
                self.mol_acum_CO2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_CO2_V101"][i]      #kmol
                self.mol_acum_O2_V101 = self.n_biogas_acum_V101 *  self.DataPlant["x_O2_V101"][i]        #kmol
                self.mol_acum_H2S_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_H2S_V101"][i]/1000000)      #kmol
                self.mol_acum_H2_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_H2_V101"][i]/1000000)        #kmol
                
                #Stochoimetric expenditure in R101
                #mol organic compound
                mol_ini_R101 = self.Csus_ini_SV_R101 * self.DataPlant["V_R101"][i]
                mol_in_R101 = (Q_P104 * tp/60 * self.Csv_sus) + (Q_P102 * tp/60 * self.Csus_ini_SV_R102)
                mol_expended_R101 = self.mol_acum_CH4_V101 * (1/self.s_CH4)
                self.Csus_ini_SV_R101 = (mol_ini_R101 + mol_in_R101 - mol_expended_R101)/(self.DataPlant["V_R101"][i])
                self.SV_g_R101 = self.Csus_ini_SV_R101 * self.MW_sustrato * self.DataPlant["V_R101"][i]         #Volatile solids g
                SV_g_Gompertz_R101.append(self.SV_g_R101)                                                       #storage grams of volatile solids  
                              
                timev.append(self.DataPlant["normTime"][i])
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
        
        def model_ADM1(C, t, K, VR_in_func, Q_func_1, Q_func_2, Csus_in_func_1, Csus_in_func_2, Operation):
            Q_1=Q_func_1(t)
            Q_2=Q_func_2(t)
            Csus_in_1 = Csus_in_func_1(t)
            Csus_in_2 = Csus_in_func_2(t)
            VR = VR_in_func(t)
            if Operation == 1:         #Without recirculation
                dCsus_dt = ((Q_1 / VR) * (Csus_in_1 - C)) - (C * K) / VR
            elif Operation == 2:       #two entrances
                dCsus_dt = (Q_1 * Csus_in_1)/VR + (Q_2 * Csus_in_2)/VR - ((Q_1 + Q_2)*C)/VR - (C * K) / VR
            elif Operation == 3:       #Auto-recirculation
                dCsus_dt = (Q_1 * Csus_in_1)/VR + (Q_2 * C)/VR - ((Q_1 + Q_2)*C)/VR - (C * K) / VR
            return dCsus_dt
        
        # Optimization function t: vector of experimental time, C_exp: sustrate experimental concentration, y0: Initial value, 
        def Optimization(t, C_exp, y0, VR, Qi1, Csus_in_i1, Qi2, Csus_in_i2, Operation, K=1): 
            # Define the objective function to minimize
            def objective(params):
                K = params
                t_train = t
                #interpol the vectors according to experimental time
                Q_func1 = lambda t: np.interp(t, t_train, Qi1)
                Q_func2 = lambda t: np.interp(t, t_train, Qi2)
                VR_func = lambda t: np.interp(t, t_train, VR)
                Csus_in1 = lambda t: np.interp(t, t_train, Csus_in_i1)
                Csus_in2 = lambda t: np.interp(t, t_train, Csus_in_i2)
                
                C_model = odeint(model_ADM1, y0, t, args = (K, VR_func, Q_func1, Q_func2, Csus_in1, Csus_in2, Operation)).flatten()

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
                                                  Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt,
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
                                                  Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt,
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
                                                    Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_R101_opt,
                                                    Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_R101_opt, Operation = 1, K = self.K_mean_R101)
                
                K_R101.append(Opt_kinetic_params_R101.x[0])

                #Optimization for R102
                Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_R102_opt, y0 = C_exp_R102_opt[0], VR = VR_exp_R102_opt,
                                                  Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_R101_opt,
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
                                                  Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_R101_opt,
                                                  Qi2 = Q_P102_opt, Csus_in_i2 = Csus_in_R101_opt, Operation = 2, K = self.K_mean_R101)
                
                K_R101.append(Opt_kinetic_params_R101.x[0])
                
                #Optimization for R102
                Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_R102_opt, y0 = C_exp_R102_opt[0], VR = VR_exp_R102_opt,
                                                  Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_R101_opt,
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
                                                  Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_R101_opt,
                                                  Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_R101_opt, Operation = 1, K = self.K_mean_R101)
                
                K_R101.append(Opt_kinetic_params_R101.x[0])
                
                #Optimization for R102
                Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_R102_opt, y0 = C_exp_R102_opt[0], VR = VR_exp_R102_opt,
                                                  Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_R101_opt,
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

    def V101 (self):
        #Estimation of ammonia production
        self.mol_acum_NH3_V101 = self.mol_acum_CH4_V101 * (self.s_NH3/self.s_CH4)
        self.mol_sto_NH3_V101 = self.mol_sto_CH4_V101 * (self.s_NH3/self.s_CH4)
        #Absollute humidity estimation
        self.AH_V101 = self.Thermo.BiogasAbsoluteHumidity(RH = float(self.DataPlant["rh_V101"].iloc[-1]), T = float(self.DataPlant["T_V101"].iloc[-1]))
        #Estimation of normal volume of biogas
        self.Vnorm_bio_V101 = ((self.Pacum_V101*6894.76)*(self.Volume_V101/1000)*273.15)/(100000*(float(self.DataPlant["T_V101"].iloc[-1])+273.15))
        self.Vnorm_bio_sto_V101 = ((self.P_V101*6894.76)*(self.Volume_V101/1000)*273.15)/(100000*(float(self.DataPlant["T_V101"].iloc[-1])+273.15))
        #Estimation moles of water
        MW_H2O = 18
        self.mol_acum_H2O_V101 = (self.AH_V101 * self.Vnorm_bio_V101 )/MW_H2O*1000 #mol H2O
        #Relative humidity to show in front
        self.RH_V101 = self.DataPlant["rh_V101"].iloc[-1]

        self.mol_biogas_total_dry_V101 = (self.mol_acum_CH4_V101 + self.mol_acum_CO2_V101 + self.mol_acum_O2_V101 + self.mol_acum_H2S_V101 + 
                                    self.mol_acum_H2_V101 + self.mol_acum_NH3_V101)
        
        self.mol_biogas_storage_V101 = (self.mol_sto_CH4_V101 + self.mol_sto_CO2_V101 + self.mol_sto_O2_V101 + self.mol_sto_H2S_V101 + 
                                    self.mol_sto_H2_V101 + self.mol_sto_NH3_V101)
        
        if self.mol_biogas_total_dry_V101 > 0:
            self.xCH4_V101 = self.mol_acum_CH4_V101/self.mol_biogas_total_dry_V101
            self.xCO2_V101 = self.mol_acum_CO2_V101/self.mol_biogas_total_dry_V101
            self.xO2_V101 = self.mol_acum_O2_V101/self.mol_biogas_total_dry_V101
            self.xH2S_V101 = self.mol_acum_H2S_V101/self.mol_biogas_total_dry_V101 * 1000000
            self.xH2_V101 = self.mol_acum_H2_V101/self.mol_biogas_total_dry_V101 * 1000000
            self.xNH3_V101 = self.mol_acum_NH3_V101/self.mol_biogas_total_dry_V101 * 1000000

            self.VCH4_acum_V101 = self.Vnorm_bio_V101 * self.xCH4_V101
            self.VCO2_acum_V101 = self.Vnorm_bio_V101 * self.xCO2_V101
            self.VO2_acum_V101 = self.Vnorm_bio_V101 * self.xO2_V101
            self.VH2S_acum_V101 = (self.Vnorm_bio_V101 * self.xH2S_V101) / 1000000
            self.VH2_acum_V101 = (self.Vnorm_bio_V101 * self.xH2_V101) / 1000000
            self.VNH3_acum_V101 = (self.Vnorm_bio_V101 * self.xNH3_V101) / 1000000

            self.LHV_V101 = self.Thermo.LHV(molCH4=self.mol_acum_CH4_V101, molCO2=self.mol_acum_CO2_V101, molH2S = self.mol_acum_H2S_V101,
                                            molO2=self.mol_acum_O2_V101, molH2=self.mol_acum_H2_V101)
            
            self.LHV_V101 = self.LHV_V101[0]
            self.Energy_V101 = self.LHV_V101 * self.mol_biogas_storage_V101

        else:
            self.xCH4_V101 = 0
            self.xCO2_V101 = 0
            self.xO2_V101 = 0
            self.xH2S_V101 = 0
            self.xH2_V101 = 0
            self.xNH3_V101 = 0

            self.VCH4_acum_V101 = 0
            self.VCO2_acum_V101 = 0
            self.VO2_acum_V101 = 0
            self.VH2S_acum_V101 = 0
            self.VH2_acum_V101 = 0
            self.VNH3_acum_V101 = 0

            self.LHV_V101 = 0
            self.Energy_V101 = 0
        
    def V102 (self):
        # Storage biogas mol in V102
        self.n_biogas_sto_V102 = (((self.P_V102*6894.76) * (self.Volume_V102/1000))/
                                    (8.314 * (self.DataPlant["T_V102"].iloc[-1] + 273.15)))           #mol
        # Accumulated biogas mol in V102
        self.n_biogas_acum_V102 = (((self.Pacum_V102*6894.76) * (self.Volume_V102/1000))/
                                    (8.314 * (self.DataPlant["T_V102"].iloc[-1] + 273.15)))           #mol
        
        #Estimate the storage and accumulated mol for component in biogas
        #Storage compounds
        self.mol_sto_CH4_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_CH4_V102"].iloc[-1]      #mol
        self.mol_sto_CO2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_CO2_V102"].iloc[-1]      #mol
        self.mol_sto_O2_V102 = self.n_biogas_sto_V102 *  self.DataPlant["x_O2_V102"].iloc[-1]        #mol
        self.mol_sto_H2S_V102 = self.n_biogas_sto_V102 *  (self.DataPlant["x_H2S_V102"].iloc[-1]/1000000)      #mol
        self.mol_sto_H2_V102 = self.n_biogas_sto_V102 *  (self.DataPlant["x_H2_V102"].iloc[-1]/1000000)        #mol
    
        #Accumulated compounds
        self.mol_acum_CH4_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_CH4_V102"].iloc[-1]      #mol
        self.mol_acum_CO2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_CO2_V102"].iloc[-1]      #mol
        self.mol_acum_O2_V102 = self.n_biogas_acum_V102 *  self.DataPlant["x_O2_V102"].iloc[-1]        #mol
        self.mol_acum_H2S_V102 = self.n_biogas_acum_V102 *  (self.DataPlant["x_H2S_V102"].iloc[-1]/1000000)      #mol
        self.mol_acum_H2_V102 = self.n_biogas_acum_V102 *  (self.DataPlant["x_H2_V102"].iloc[-1]/1000000)       #mol

        #Estimation of ammonia production
        self.mol_acum_NH3_V102 = self.mol_acum_CH4_V102 * (self.s_NH3/self.s_CH4)
        self.mol_sto_NH3_V102 = self.mol_sto_CH4_V102 * (self.s_NH3/self.s_CH4)

        #Absollute humidity estimation
        self.AH_V102 = self.Thermo.BiogasAbsoluteHumidity(RH = float(self.DataPlant["rh_V102"].iloc[-1]), T = float(self.DataPlant["T_V102"].iloc[-1]))
        #Estimation of normal volume of biogas
        self.Vnorm_bio_V102 = ((self.Pacum_V102*6894.76)*(self.Volume_V102/1000)*273.15)/(100000*float(self.DataPlant["T_V102"].iloc[-1]+273.15))
        self.Vnorm_bio_sto_V102 = ((self.P_V102*6894.76)*(self.Volume_V102/1000)*273.15)/(100000*float(self.DataPlant["T_V102"].iloc[-1]+273.15))

        #Estimation moles of water
        MW_H2O = 18
        self.mol_acum_H2O_V102 = (self.AH_V102 * self.Vnorm_bio_V102 )/MW_H2O*1000 #mol H2O

        #Relative humidity to show in front
        self.RH_V102 = self.DataPlant["rh_V102"].iloc[-1]

        self.mol_biogas_total_dry_V102 = (self.mol_acum_CH4_V102 + self.mol_acum_CO2_V102 + self.mol_acum_O2_V102 + self.mol_acum_H2S_V102 + 
                                    self.mol_acum_H2_V102 + self.mol_acum_NH3_V102)
        
        self.mol_biogas_storage_V102 = (self.mol_sto_CH4_V102 + self.mol_sto_CO2_V102 + self.mol_sto_O2_V102 + self.mol_sto_H2S_V102 + 
                                    self.mol_sto_H2_V102 + self.mol_sto_NH3_V102)
        
        if self.mol_biogas_total_dry_V102 > 0:
            self.xCH4_V102 = self.mol_acum_CH4_V102/self.mol_biogas_total_dry_V102
            self.xCO2_V102 = self.mol_acum_CO2_V102/self.mol_biogas_total_dry_V102
            self.xO2_V102 = self.mol_acum_O2_V102/self.mol_biogas_total_dry_V102
            self.xH2S_V102 = self.mol_acum_H2S_V102/self.mol_biogas_total_dry_V102 * 1000000
            self.xH2_V102 = self.mol_acum_H2_V102/self.mol_biogas_total_dry_V102 * 1000000
            self.xNH3_V102 = self.mol_acum_NH3_V102/self.mol_biogas_total_dry_V102 * 1000000

            self.VCH4_acum_V102 = self.Vnorm_bio_V102 * self.xCH4_V102
            self.VCO2_acum_V102 = self.Vnorm_bio_V102 * self.xCO2_V102
            self.VO2_acum_V102 = self.Vnorm_bio_V102 * self.xO2_V102
            self.VH2S_acum_V102 = (self.Vnorm_bio_V102 * self.xH2S_V102) / 1000000
            self.VH2_acum_V102 = (self.Vnorm_bio_V102 * self.xH2_V102) / 1000000
            self.VNH3_acum_V102 = (self.Vnorm_bio_V102 * self.xNH3_V102) / 1000000

            self.LHV_V102 = self.Thermo.LHV(molCH4=self.mol_acum_CH4_V102, molCO2=self.mol_acum_CO2_V102, molH2S = self.mol_acum_H2S_V102,
                                            molO2=self.mol_acum_O2_V102, molH2=self.mol_acum_H2_V102)
            
            self.LHV_V102 = self.LHV_V102[0]
            self.Energy_V102 = self.LHV_V102 * self.mol_biogas_storage_V102
        else:
            self.xCH4_V102 = 0
            self.xCO2_V102 = 0
            self.xO2_V102 = 0
            self.xH2S_V102 = 0
            self.xH2_V102 = 0
            self.xNH3_V102 = 0

            self.VCH4_acum_V102 = 0
            self.VCO2_acum_V102 = 0
            self.VO2_acum_V102 = 0
            self.VH2S_acum_V102 = 0
            self.VH2_acum_V102 = 0
            self.VNH3_acum_V102 = 0

            self.LHV_V102 = 0
            self.Energy_V102 = 0
    
    def V107 (self):
        # Storage biogas mol in V107
        self.n_biogas_sto_V107 = (((self.P_V107*6894.76) * (self.Volume_V107/1000))/
                                    (8.314 * (self.DataPlant["T_V107"].iloc[-1] + 273.15)))           #mol
        # Accumulated biogas mol in V107
        self.n_biogas_acum_V107 = (((self.Pacum_V107*6894.76) * (self.Volume_V107/1000))/
                                    (8.314 * (self.DataPlant["T_V107"].iloc[-1] + 273.15)))           #mol
        
        #Estimate the storage and accumulated mol for component in biogas
        #Storage compounds
        self.mol_sto_CH4_V107 = self.n_biogas_sto_V107 *  self.DataPlant["x_CH4_V107"].iloc[-1]      #mol
        self.mol_sto_CO2_V107 = self.n_biogas_sto_V107 *  self.DataPlant["x_CO2_V107"].iloc[-1]      #mol
        self.mol_sto_O2_V107 = self.n_biogas_sto_V107 *  self.DataPlant["x_O2_V107"].iloc[-1]        #mol
        self.mol_sto_H2S_V107 = self.n_biogas_sto_V107 *  (self.DataPlant["x_H2S_V107"].iloc[-1]/1000000)      #mol
        self.mol_sto_H2_V107 = self.n_biogas_sto_V107 *  (self.DataPlant["x_H2_V107"].iloc[-1]/1000000)        #mol

        #Accumulated compounds
        self.mol_acum_CH4_V107 = self.n_biogas_acum_V107 *  self.DataPlant["x_CH4_V107"].iloc[-1]      #mol
        self.mol_acum_CO2_V107 = self.n_biogas_acum_V107 *  self.DataPlant["x_CO2_V107"].iloc[-1]      #mol
        self.mol_acum_O2_V107 = self.n_biogas_acum_V107 *  self.DataPlant["x_O2_V107"].iloc[-1]        #mol
        self.mol_acum_H2S_V107 = self.n_biogas_acum_V107 *  (self.DataPlant["x_H2S_V107"].iloc[-1]/1000000)      #mol
        self.mol_acum_H2_V107 = self.n_biogas_acum_V107 *  (self.DataPlant["x_H2_V107"].iloc[-1]/1000000)       #mol

        #Estimation of ammonia production
        self.mol_acum_NH3_V107 = self.mol_acum_CH4_V107 * (self.s_NH3/self.s_CH4)
        self.mol_sto_NH3_V107 = self.mol_sto_CH4_V107 * (self.s_NH3/self.s_CH4)

        #Absollute humidity estimation
        self.AH_V107 = self.Thermo.BiogasAbsoluteHumidity(RH = float(self.DataPlant["rh_V107"].iloc[-1]), T = float(self.DataPlant["T_V107"].iloc[-1]))
        #Estimation of normal volume of biogas
        self.Vnorm_bio_V107 = ((self.Pacum_V107*6894.76)*(self.Volume_V107/1000)*273.15)/(100000*float(self.DataPlant["T_V107"].iloc[-1]+273.15))
        self.Vnorm_bio_sto_V107 = ((self.P_V107*6894.76)*(self.Volume_V107/1000)*273.15)/(100000*float(self.DataPlant["T_V107"].iloc[-1]+273.15))
        #Estimation moles of water
        MW_H2O = 18
        self.mol_acum_H2O_V107 = (self.AH_V107 * self.Vnorm_bio_V107 )/MW_H2O*1000 #mol H2O

        #Relative humidity to show in front
        self.RH_V107 = self.DataPlant["rh_V107"].iloc[-1]

        self.mol_biogas_total_dry_V107 = (self.mol_acum_CH4_V107 + self.mol_acum_CO2_V107 + self.mol_acum_O2_V107 + self.mol_acum_H2S_V107 + 
                                    self.mol_acum_H2_V107 + self.mol_acum_NH3_V107)
        
        self.mol_biogas_storage_V107 = (self.mol_sto_CH4_V107 + self.mol_sto_CO2_V107 + self.mol_sto_O2_V107 + self.mol_sto_H2S_V107 + 
                                    self.mol_sto_H2_V107 + self.mol_sto_NH3_V107)
        
        if self.mol_biogas_total_dry_V107 > 0:
            self.xCH4_V107 = self.mol_acum_CH4_V107/self.mol_biogas_total_dry_V107
            self.xCO2_V107 = self.mol_acum_CO2_V107/self.mol_biogas_total_dry_V107
            self.xO2_V107 = self.mol_acum_O2_V107/self.mol_biogas_total_dry_V107
            self.xH2S_V107 = self.mol_acum_H2S_V107/self.mol_biogas_total_dry_V107 * 1000000
            self.xH2_V107 = self.mol_acum_H2_V107/self.mol_biogas_total_dry_V107 * 1000000
            self.xNH3_V107 = self.mol_acum_NH3_V107/self.mol_biogas_total_dry_V107 * 1000000

            self.VCH4_acum_V107 = self.Vnorm_bio_V107 * self.xCH4_V107
            self.VCO2_acum_V107 = self.Vnorm_bio_V107 * self.xCO2_V107
            self.VO2_acum_V107 = self.Vnorm_bio_V107 * self.xO2_V107
            self.VH2S_acum_V107 = (self.Vnorm_bio_V107 * self.xH2S_V107) / 1000000
            self.VH2_acum_V107 = (self.Vnorm_bio_V107 * self.xH2_V107) / 1000000
            self.VNH3_acum_V107 = (self.Vnorm_bio_V107 * self.xNH3_V107) / 1000000

            self.LHV_V107 = self.Thermo.LHV(molCH4=self.mol_acum_CH4_V107, molCO2=self.mol_acum_CO2_V107, molH2S = self.mol_acum_H2S_V107,
                                            molO2=self.mol_acum_O2_V107, molH2=self.mol_acum_H2_V107)
            
            self.LHV_V107 = self.LHV_V107[0]
            
            self.Energy_V107 = self.LHV_V107 * self.mol_biogas_storage_V107
        else:
            self.xCH4_V107 = 0
            self.xCO2_V107 = 0
            self.xO2_V107 = 0
            self.xH2S_V107 = 0
            self.xH2_V107 = 0
            self.xNH3_V107 = 0

            self.VCH4_acum_V107 = 0
            self.VCO2_acum_V107 = 0
            self.VO2_acum_V107 = 0
            self.VH2S_acum_V107 = 0
            self.VH2_acum_V107 = 0
            self.VNH3_acum_V107 = 0

            self.LHV_V107 = 0
            self.Energy_V107 = 0

    def biogas_treatment(self, resolution):
                
        #mol H2S adsorption 
        if (self.mol_acum_H2S_V101 + self.mol_acum_H2S_V102) > self.mol_acum_H2S_V107:
            self.mol_H2S_ads = (self.mol_acum_H2S_V101 + self.mol_acum_H2S_V102)-self.mol_acum_H2S_V107
            self.x_H2S_ads = ((self.mol_acum_H2S_V101 + self.mol_acum_H2S_V102)-self.mol_acum_H2S_V107)/(self.mol_acum_H2S_V101 + self.mol_acum_H2S_V102)
            
        else: 
            self.mol_H2S_ads = 0
            self.x_H2S_ads = 0
            
        
        #mol NH3 adsorption
        if (self.mol_acum_NH3_V101 + self.mol_acum_NH3_V102) > self.mol_acum_NH3_V107:
            self.mol_NH3_ads = (self.mol_acum_NH3_V101 + self.mol_acum_NH3_V102)-self.mol_acum_NH3_V107
            self.x_NH3_ads = ((self.mol_acum_NH3_V101 + self.mol_acum_NH3_V102)-self.mol_acum_NH3_V107)/(self.mol_acum_NH3_V101 + self.mol_acum_NH3_V102)
            
        else: 
            self.mol_NH3_ads = 0
            self.x_NH3_ads = 0
            
        
        #mol H2O adsorption
        if (self.mol_acum_H2O_V101 + self.mol_acum_H2O_V102) > self.mol_acum_H2O_V107:
            self.mol_H2O_ads = (self.mol_acum_H2O_V101 + self.mol_acum_H2O_V102)-self.mol_acum_H2O_V107
            self.x_H2O_ads = ((self.mol_acum_H2O_V101 + self.mol_acum_H2O_V102)-self.mol_acum_H2O_V107)/(self.mol_acum_H2O_V101 + self.mol_acum_H2O_V102)
            
        else: 
            self.mol_H2O_ads = 0
            self.x_H2O_ads = 0
            
        
        self.Xglobal = (self.x_H2S_ads + self.x_NH3_ads + self.x_H2O_ads)/3

    def StorageData (self, name):
        timestamp = self.DataPlant["_time"].iloc[-1]  # Convert to nanoseconds
        
        if self.Model == "Arrhenius" and (self.Operation_mode == 1 or self.Operation_mode == 2):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R101?{name}', value = float(self.K_mean_R101), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?Ea_R101?{name}', value = float(self.Ea_mean_R101), timestamp=timestamp)  
        
        elif self.Model == "ADM1" and (self.Operation_mode == 1 or self.Operation_mode == 2):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", mode=self.Operation_mode,
                                                    model = self.Model, variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R101?{name}', value = float(self.K_mean_R101), timestamp=timestamp)
        
        elif self.Model == "Gompertz" and (self.Operation_mode == 1 or self.Operation_mode == 2):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?ym_R101?{name}', value = float(self.ym_R101), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?U_R101?{name}', value = float(self.U_R101), timestamp=timestamp)
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?L_R101?{name}', value = float(self.L_R101), timestamp=timestamp)

        elif self.Model == "Arrhenius" and (self.Operation_mode == 3 or self.Operation_mode == 4 or self.Operation_mode == 5):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R101?{name}', value = float(self.K_mean_R101), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?Ea_R101?{name}', value = float(self.Ea_mean_R101), timestamp=timestamp)
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?Ea_R102?{name}', value = float(self.K_mean_R102), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?Ea_R102?{name}', value = float(self.Ea_mean_R102), timestamp=timestamp)
        
        elif self.Model == "ADM1"  and (self.Operation_mode == 3 or self.Operation_mode == 4 or self.Operation_mode == 5):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R101?{name}', value = float(self.K_mean_R101), timestamp=timestamp)
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R102?{name}', value = float(self.K_mean_R102), timestamp=timestamp)
        
        elif self.Model == "Gompertz" and (self.Operation_mode == 3 or self.Operation_mode == 4 or self.Operation_mode == 5):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?ym_R101?{name}', value = float(self.ym_R101), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?U_R101?{name}', value = float(self.U_R101), timestamp=timestamp)
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?L_R101?{name}', value = float(self.L_R101), timestamp=timestamp)
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?ym_R102?{name}', value = float(self.ym_R102), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?U_R102?{name}', value = float(self.U_R102), timestamp=timestamp)
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?L_R102?{name}', value = float(self.L_R102), timestamp=timestamp)
        
        self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device="entrenamiento", variable=f'Modo{int(self.Operation_mode)}?{self.Model}?N_H2S_abs?{name}', value=self.mol_H2S_ads, timestamp=timestamp)
        self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device="entrenamiento", variable=f'Modo{int(self.Operation_mode)}?{self.Model}?N_NH3_abs?{name}', value=self.mol_NH3_ads, timestamp=timestamp)
        self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device="entrenamiento", variable=f'Modo{int(self.Operation_mode)}?{self.Model}?N_H2O_abs?{name}', value=self.mol_H2O_ads, timestamp=timestamp)

# #This will be the way to call method from API
# #singletone
# Model = "Arrhenius"     #Get value from frontEnd
# Training = TrainingBiogasPlant(t_train = 72*60, ST_ini_R101 = 10, SV_ini_R101 = 1.42, Cc_R101 = 27.36, Ch_R101 = 6.38, Co_R101=12.21, Cn_R101=3.04, Cs_R101=1.51, rho_R101=986.45, Volume_V101 = 15,  
#                              Volume_V102 = 30, Volume_V107 = 30) 
# # # Training.getData()
# # # Training.LimitReagentCalculation()
# # # Training.StochoimetricExpenditure(Model = Model)

# while True:
#     Training.getData()
#     Training.LimitReagentCalculation()
#     Training.StochoimetricExpenditure(Model = Model)
#     if Model == "Arrhenius":
#         Training.OptimizationArrhenius(resolution=2)
#     elif Model == "ADM1":
#         Training.OptimizationADM1(resolution=2)
#     elif Model == "Gompertz":
#         Training.OptimizationGompertz(resolution=2)
    
#     Training.V101()
#     Training.V102()
#     Training.V107()
#     Training.biogas_treatment(resolution =2)

#     #Output variables for TK100
#     print("----------------TK-100--------------------------")
#     print("subindex C",Training.n)
#     print("subindex H",Training.a)
#     print("Subindex O",Training.b)
#     print("subindex N",Training.c)
#     print("subindex S",Training.d)
#     print("Mixing velocity TK100 [RPM]", float(Training.Mix_Velocity_TK100))
#     print("Volatile solids concnetration TK100 [gSV/L]", Training.Csv_sus_gl)
#     print("Volatile solids concetration TK-100 [%]", Training.SV)
#     print("Total solids concentration TK-100 [g/L]", Training.Cst_sus_gl)
#     print("Total solids concentration [%]", Training.ST)

#     #output variables for P104
#     print("")
#     print("----------------P-104--------------------------")
#     print("Flow rate P104 [L/h]", Training.P104)


#     #output Variables for R101
#     print("")
#     print("----------------R101--------------------------")
#     print("pH in reactor R101", Training.pH_R101)
#     print("Temperature in R101", Training.T_R101)
#     print("Mixing velocity R101 [RPM]", Training.Mix_Velocity_R101)
#     print("Volatile solid concentration R101 [gSV/L]", Training.Csus_SV_R01)
#     print("Volatile solis concentration [%]", Training.SV_R101)
#     print("Total solids concentration [gST/L]", Training.Csus_ST_R101)
#     print("Total solids concentration [%]", Training.ST_R01)
#     print("Organic charge [gSV/Lmin]", Training.OC_R101)
#     print("Reagent limist convertion [%]", Training.x_R101)
#     if Model == "Arrhenius":
#         print("Pre-exponential factor [L/min]: ", Training.K_mean_R101)
#         print("Energy activation [J/mol]: ", Training.Ea_mean_R101)
#     elif Model == "ADM1":
#         print("Genral kinetic [L/min]: ", Training.K_mean_R101)
#     elif Model == "Gompertz":
#         pass
        
#     #output variables for P101
#     print("")
#     print("----------------P-101--------------------------")
#     print("Flow rate P104 [L/h]", Training.P101)

#     #Output variables for V101
#     print("")
#     print("----------------V101--------------------------")
#     print("Accumulated pressure in V101 [psig]",Training.Pacum_V101)
#     print("Storage pressure in V101 [psig]", Training.P_V101)
#     print("biogas normal volume accumulated [NL]", Training.Vnorm_bio_V101*1000)
#     print("biogas normal volume storage [NL]", Training.Vnorm_bio_sto_V101*1000)
#     print("biogas methane concentration", Training.xCH4_V101*100)
#     print("biogas methane concentration", Training.xCO2_V101*100)
#     print("biogas carbon dioxide concentration", Training.xO2_V101*100)
#     print("biogas hydrogen sulphur concentration", Training.xH2S_V101)
#     print("biogas amonnia concentration", Training.xNH3_V101)
#     print("biogas hydrogen concentration", Training.xH2_V101)
#     print("biogas methane mol", Training.mol_acum_CH4_V101)
#     print("biogas methane mol", Training.mol_acum_CO2_V101)
#     print("biogas carbon dioxide mol", Training.mol_acum_O2_V101)
#     print("biogas hydrogen sulphur mol", Training.mol_acum_H2S_V101)
#     print("biogas amonnia mol", Training.mol_acum_NH3_V101)
#     print("biogas hydrogen mol", Training.mol_acum_H2_V101)
#     print("biogas methane volumen", Training.VCH4_acum_V101)
#     print("biogas methane volumen", Training.VCO2_acum_V101)
#     print("biogas carbon dioxide volumen", Training.VO2_acum_V101)
#     print("biogas hydrogen sulphur volumen", Training.VH2S_acum_V101)
#     print("biogas amonnia volumen", Training.VNH3_acum_V101)
#     print("biogas hydrogen volumen", Training.VH2_acum_V101)
#     print("biogas relativity humidity", Training.RH_V101)
#     print("biogas water moles", Training.mol_acum_H2O_V101)

#     #Output variables for V102
#     print("")
#     print("----------------V102--------------------------")
#     print("Accumulated pressure in V102 [psig]",Training.Pacum_V102)
#     print("Storage pressure in V102 [psig]", Training.P_V102)
#     print("biogas normal volume accumulated [NL]", Training.Vnorm_bio_V102*1000)
#     print("biogas normal volume storage [NL]", Training.Vnorm_bio_sto_V102*1000)
#     print("biogas methane concentration", Training.xCH4_V102*100)
#     print("biogas methane concentration", Training.xCO2_V102*100)
#     print("biogas carbon dioxide concentration", Training.xO2_V102*100)
#     print("biogas hydrogen sulphur concentration", Training.xH2S_V102)
#     print("biogas amonnia concentration", Training.xNH3_V102)
#     print("biogas hydrogen concentration", Training.xH2_V102)
#     print("biogas methane mol", Training.mol_acum_CH4_V102)
#     print("biogas methane mol", Training.mol_acum_CO2_V102)
#     print("biogas carbon dioxide mol", Training.mol_acum_O2_V102)
#     print("biogas hydrogen sulphur mol", Training.mol_acum_H2S_V102)
#     print("biogas amonnia mol", Training.mol_acum_NH3_V102)
#     print("biogas hydrogen mol", Training.mol_acum_H2_V102)
#     print("biogas methane volumen", Training.VCH4_acum_V102)
#     print("biogas methane volumen", Training.VCO2_acum_V102)
#     print("biogas carbon dioxide volumen", Training.VO2_acum_V102)
#     print("biogas hydrogen sulphur volumen", Training.VH2S_acum_V102)
#     print("biogas amonnia volumen", Training.VNH3_acum_V102)
#     print("biogas hydrogen volumen", Training.VH2_acum_V102)
#     print("biogas relativity humidity", Training.RH_V102)
#     print("biogas water moles", Training.mol_acum_H2O_V102)

#     #Output variables for V107
#     print("")
#     print("----------------V107--------------------------")
#     print("Accumulated pressure in V107 [psig]",Training.Pacum_V107)
#     print("Storage pressure in V107 [psig]", Training.P_V107)
#     print("biogas normal volume accumulated [NL]", Training.Vnorm_bio_V107*1000)
#     print("biogas normal volume storage [NL]", Training.Vnorm_bio_sto_V107*1000)
#     print("biogas methane concentration", Training.xCH4_V107*100)
#     print("biogas methane concentration", Training.xCO2_V107*100)
#     print("biogas carbon dioxide concentration", Training.xO2_V107*100)
#     print("biogas hydrogen sulphur concentration", Training.xH2S_V107)
#     print("biogas amonnia concentration", Training.xNH3_V107)
#     print("biogas hydrogen concentration", Training.xH2_V107)
#     print("biogas methane mol", Training.mol_acum_CH4_V107)
#     print("biogas methane mol", Training.mol_acum_CO2_V107)
#     print("biogas carbon dioxide mol", Training.mol_acum_O2_V107)
#     print("biogas hydrogen sulphur mol", Training.mol_acum_H2S_V107)
#     print("biogas amonnia mol", Training.mol_acum_NH3_V107)
#     print("biogas hydrogen mol", Training.mol_acum_H2_V107)
#     print("biogas methane volumen", Training.VCH4_acum_V107)
#     print("biogas methane volumen", Training.VCO2_acum_V107)
#     print("biogas carbon dioxide volumen", Training.VO2_acum_V107)
#     print("biogas hydrogen sulphur volumen", Training.VH2S_acum_V107)
#     print("biogas amonnia volumen", Training.VNH3_acum_V107)
#     print("biogas hydrogen volumen", Training.VH2_acum_V107)
#     print("biogas relativity humidity", Training.RH_V107)
#     print("biogas water moles", Training.mol_acum_H2O_V107)

#     #Output variables for Treatment
#     print("")
#     print("----------------Treatment--------------------------")
#     print("Hydrogen sulphide moles adsorpted: ", Training.mol_H2S_ads)
#     print("Ammonia adsorptia ", Training.mol_NH3_ads)
#     print("Water adsorptia ", Training.mol_H2O_ads)
#     print("Convertion ", Training.Xglobal)

#     # Training.DataPlant.to_csv("Output1.csv")
#     # Training.TrainMode2.to_csv("Output.csv")
#     time.sleep(480)

