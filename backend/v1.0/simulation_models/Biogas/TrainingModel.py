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
from fractions import Fraction
from functools import reduce
from math import gcd
from simulation_models.Biogas import ThermoProperties
import pandas as pd
import numpy as np
import math
from scipy.integrate import odeint
from scipy.optimize import minimize
import statistics as st

class Training_offline:
    def __init__ (self, DB_IP, DB_Port, DB_Organization, DB_Bucket, DB_Token,
                  t_train, ST_ini_R101, SV_ini_R101, Cc_R101, Ch_R101, Co_R101, Cn_R101, Cs_R101, rho_R101, Volume_V101 = 15,  
                  ST_ini_R102 = 2, SV_ini_R102 = 1.5, Cc_R102 = 27.36, Ch_R102 = 6.38, Co_R102 = 12.21, Cn_R102 = 3.04, Cs_R102 = 1.51, rho_R102 = 1000, 
                  Volume_V102 = 35, Volume_V107 = 35):
        self.influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
        self.connectionState = self.influxDB.InfluxDBconnection()
        if not self.connectionState:
            raise ConnectionError(f"Database connection failed: {self.influxDB.ERROR_MESSAGE}")
        
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
        
        self.s_H2O_ini_R101 = n_ini_R101-(a_ini_R101/4)-(b_ini_R101/2)+(3/4)*c_ini_R101+(d_ini_R101/2)
        self.s_CH4_ini_R101 = (n_ini_R101/2)+(a_ini_R101/8)-(b_ini_R101/4)-(3/8)*c_ini_R101-(d_ini_R101/4)
        self.s_CO2_ini_R101 = (n_ini_R101/2)-(a_ini_R101/8)+(b_ini_R101/4)+(3/8)*c_ini_R101-(d_ini_R101/4)
        self.s_NH3_ini_R101 = c_ini_R101
        self.s_H2S_ini_R101 = d_ini_R101 

        #initial concentration in R101
        if self.ST_ini_R101 == 0:
            self.Csus_ini_ST_R101 = 0
            self.Csus_ini_SV_R101 = 0
            self.Csus_ini_SV_R101_i = 0
            self.Csus_ini_fixed_R101 = 0
            self.MW_inocum_ini_R101 = 18         #molecular weight of the water 
        
        else:
            self.Csus_ini_ST_R101 = ((self.ST_ini_R101)*self.rho_ini_R101)/self.MW_inocum_ini_R101     #molST/L    
            self.Csus_ini_SV_R101 = ((self.SV_ini_R101)*self.rho_ini_R101)/self.MW_inocum_ini_R101     #molSV/L
            self.Csus_ini_fixed_R101 = self.Csus_ini_ST_R101 - self.Csus_ini_SV_R101                   #molSF/L 
            self.Csus_ini_SV_R101_gl = ((self.SV_ini_R101)*self.rho_ini_R101)                          #gSV/L 
            self.Csus_ini_SV_R101_gl_i = ((self.SV_ini_R101)*self.rho_ini_R101) 
            self.Csus_ini_ST_R101_gl = ((self.ST_ini_R101)*self.rho_ini_R101)                          #gST/L 
        
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
        self.ym_R101 = 0.02
        self.U_R101 = 5e-6
        self.L_R101 = 0.2
        self.ym_R102 = 1
        self.U_R102 = 1
        self.L_R102 = 1
        
        #Model train time for gompertz
        self.total_time = 0
        self.timeGompertz = []
        self.tp = 8               #min
        self.SV_feed = 0

        #Vessels for biogas storage
        #Thermodynamic model initilization
        self.Thermo = ThermoProperties.ThermoProperties()

        #Biogas filters
        #hydrogen sulphide
        self.K_H2S = 0.34
        self.qmax_H2S = 0.008
        self.K2_H2S = 0.01
        #Water
        self.K_H2O = 0.068
        self.qmax_H2O = 0.0167
        self.K2_H2O = 0.01
    
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

            #Correction of concentration
            #Methane V101
            if (self.DataPlant["x_CH4_V101"] != 0).any():
                self.DataPlant["x_CH4_V101_filled"] = self.DataPlant["x_CH4_V101"].replace(0, np.nan)
                self.DataPlant["x_CH4_V101_filled"] = self.DataPlant["x_CH4_V101_filled"].ffill()
                self.DataPlant['x_CH4_V101_filled'] = self.DataPlant.apply(lambda row: row['x_CH4_V101_filled'] if row['x_CH4_V101'] == 0 else row['x_CH4_V101'], axis=1)
                self.DataPlant['x_CH4_V101_filled'] = self.DataPlant['x_CH4_V101_filled'].fillna(0).astype(float)
                self.DataPlant['x_CH4_V101_filled'] = self.DataPlant['x_CH4_V101_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_CH4_V101_filled"] = self.DataPlant["x_CH4_V101_filled"].mask(self.DataPlant["x_CH4_V101_filled"] > 100, np.nan)
                self.DataPlant["x_CH4_V101_filled"] = self.DataPlant["x_CH4_V101_filled"].ffill()
                mean_value_xCH4_V101 = self.DataPlant["x_CH4_V101_filled"].mean()
                self.DataPlant["x_CH4_V101_filled"] = mean_value_xCH4_V101
            else:
                self.DataPlant["x_CH4_V101_filled"] = self.DataPlant["x_CH4_V101"]
                                
            #Methane V102
            if (self.DataPlant["x_CH4_V102"] != 0).any():
                self.DataPlant["x_CH4_V102_filled"] = self.DataPlant["x_CH4_V102"].replace(0, np.nan)
                self.DataPlant["x_CH4_V102_filled"] = self.DataPlant["x_CH4_V102_filled"].ffill()
                self.DataPlant['x_CH4_V102_filled'] = self.DataPlant.apply(lambda row: row['x_CH4_V102_filled'] if row['x_CH4_V102'] == 0 else row['x_CH4_V102'], axis=1)
                self.DataPlant['x_CH4_V102_filled'] = self.DataPlant['x_CH4_V102_filled'].fillna(0).astype(float)
                self.DataPlant['x_CH4_V102_filled'] = self.DataPlant['x_CH4_V102_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_CH4_V102_filled"] = self.DataPlant["x_CH4_V102_filled"].mask(self.DataPlant["x_CH4_V102_filled"] > 100, np.nan)
                self.DataPlant["x_CH4_V102_filled"] = self.DataPlant["x_CH4_V102_filled"].ffill()
                mean_value_xCH4_V102 = self.DataPlant["x_CH4_V102_filled"].mean()
                self.DataPlant["x_CH4_V102_filled"] = mean_value_xCH4_V102
            else:
                self.DataPlant["x_CH4_V102_filled"] = self.DataPlant["x_CH4_V102"]
                
            #Methane V107
            if (self.DataPlant["x_CH4_V107"] != 0).any():
                self.DataPlant["x_CH4_V107_filled"] = self.DataPlant["x_CH4_V107"].replace(0, np.nan)
                self.DataPlant["x_CH4_V107_filled"] = self.DataPlant["x_CH4_V107_filled"].ffill()
                self.DataPlant['x_CH4_V107_filled'] = self.DataPlant.apply(lambda row: row['x_CH4_V107_filled'] if row['x_CH4_V107'] == 0 else row['x_CH4_V107'], axis=1)
                self.DataPlant['x_CH4_V107_filled'] = self.DataPlant['x_CH4_V107_filled'].fillna(0).astype(float)
                self.DataPlant['x_CH4_V107_filled'] = self.DataPlant['x_CH4_V107_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_CH4_V107_filled"] = self.DataPlant["x_CH4_V107_filled"].mask(self.DataPlant["x_CH4_V107_filled"] > 100, np.nan)
                self.DataPlant["x_CH4_V107_filled"] = self.DataPlant["x_CH4_V107_filled"].ffill()
                mean_value_xCH4_V107 = self.DataPlant["x_CH4_V107_filled"].mean()
                self.DataPlant["x_CH4_V107_filled"] = mean_value_xCH4_V107
            else:
                self.DataPlant["x_CH4_V107_filled"] = self.DataPlant["x_CH4_V107"]
            
            # Carbon dioxide V101
            if (self.DataPlant["x_CO2_V101"] != 0).any():
                self.DataPlant["x_CO2_V101_filled"] = self.DataPlant["x_CO2_V101"].replace(0, np.nan)
                self.DataPlant["x_CO2_V101_filled"] = self.DataPlant["x_CO2_V101_filled"].ffill()
                self.DataPlant['x_CO2_V101_filled'] = self.DataPlant.apply(lambda row: row['x_CO2_V101_filled'] if row['x_CO2_V101'] == 0 else row['x_CO2_V101'], axis=1)
                self.DataPlant['x_CO2_V101_filled'] = self.DataPlant['x_CO2_V101_filled'].fillna(0).astype(float)
                self.DataPlant['x_CO2_V101_filled'] = self.DataPlant['x_CO2_V101_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_CO2_V101_filled"] = self.DataPlant["x_CO2_V101_filled"].mask(self.DataPlant["x_CO2_V101_filled"] > 100, np.nan)
                self.DataPlant["x_CO2_V101_filled"] = self.DataPlant["x_CO2_V101_filled"].ffill()
                mean_value_xCO2_V101 = self.DataPlant["x_CO2_V101_filled"].mean()
                self.DataPlant["x_CO2_V101_filled"] = mean_value_xCO2_V101
            else:
                self.DataPlant["x_CO2_V101_filled"] = self.DataPlant["x_CO2_V101"]
            
            # Carbon dioxide V102
            if (self.DataPlant["x_CO2_V102"] != 0).any():
                self.DataPlant["x_CO2_V102_filled"] = self.DataPlant["x_CO2_V102"].replace(0, np.nan)
                self.DataPlant["x_CO2_V102_filled"] = self.DataPlant["x_CO2_V102_filled"].ffill()
                self.DataPlant['x_CO2_V102_filled'] = self.DataPlant.apply(lambda row: row['x_CO2_V102_filled'] if row['x_CO2_V102'] == 0 else row['x_CO2_V102'], axis=1)
                self.DataPlant['x_CO2_V102_filled'] = self.DataPlant['x_CO2_V102_filled'].fillna(0).astype(float)
                self.DataPlant['x_CO2_V102_filled'] = self.DataPlant['x_CO2_V102_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_CO2_V102_filled"] = self.DataPlant["x_CO2_V102_filled"].mask(self.DataPlant["x_CO2_V102_filled"] > 100, np.nan)
                self.DataPlant["x_CO2_V102_filled"] = self.DataPlant["x_CO2_V102_filled"].ffill()
                mean_value_xCO2_V102 = self.DataPlant["x_CO2_V102_filled"].mean()
                self.DataPlant["x_CO2_V102_filled"] = mean_value_xCO2_V102
            else:
                self.DataPlant["x_CO2_V102_filled"] = self.DataPlant["x_CO2_V102"]
            
            # Carbon dioxide V107
            if (self.DataPlant["x_CO2_V107"] != 0).any():
                self.DataPlant["x_CO2_V107_filled"] = self.DataPlant["x_CO2_V107"].replace(0, np.nan)
                self.DataPlant["x_CO2_V107_filled"] = self.DataPlant["x_CO2_V107_filled"].ffill()
                self.DataPlant['x_CO2_V107_filled'] = self.DataPlant.apply(lambda row: row['x_CO2_V107_filled'] if row['x_CO2_V107'] == 0 else row['x_CO2_V107'], axis=1)
                self.DataPlant['x_CO2_V107_filled'] = self.DataPlant['x_CO2_V107_filled'].fillna(0).astype(float)
                self.DataPlant['x_CO2_V107_filled'] = self.DataPlant['x_CO2_V107_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_CO2_V107_filled"] = self.DataPlant["x_CO2_V107_filled"].mask(self.DataPlant["x_CO2_V107_filled"] > 100, np.nan)
                self.DataPlant["x_CO2_V107_filled"] = self.DataPlant["x_CO2_V107_filled"].ffill()
                mean_value_xCO2_V107 = self.DataPlant["x_CO2_V107_filled"].mean()
                self.DataPlant["x_CO2_V107_filled"] = mean_value_xCO2_V107
            else:
                self.DataPlant["x_CO2_V107_filled"] = self.DataPlant["x_CO2_V107"]
                
            # OXYGEN V101
            if (self.DataPlant["x_O2_V101"] != 0).any():
                self.DataPlant["x_O2_V101_filled"] = self.DataPlant["x_O2_V101"].replace(0, np.nan)
                self.DataPlant["x_O2_V101_filled"] = self.DataPlant["x_O2_V101_filled"].ffill()
                self.DataPlant['x_O2_V101_filled'] = self.DataPlant.apply(lambda row: row['x_O2_V101_filled'] if row['x_O2_V101'] == 0 else row['x_O2_V101'], axis=1)
                self.DataPlant['x_O2_V101_filled'] = self.DataPlant['x_O2_V101_filled'].fillna(0).astype(float)
                self.DataPlant['x_O2_V101_filled'] = self.DataPlant['x_O2_V101_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_O2_V101_filled"] = self.DataPlant["x_O2_V101_filled"].mask(self.DataPlant["x_O2_V101_filled"] > 100, np.nan)
                self.DataPlant["x_O2_V101_filled"] = self.DataPlant["x_O2_V101_filled"].ffill()
                mean_value_xO2_V101 = self.DataPlant["x_O2_V101_filled"].mean()
                self.DataPlant["x_O2_V101_filled"] = mean_value_xO2_V101
            else:
                self.DataPlant["x_O2_V101_filled"] = self.DataPlant["x_O2_V101"]
            
            # OXYGEN V102
            if (self.DataPlant["x_O2_V102"] != 0).any():
                self.DataPlant["x_O2_V102_filled"] = self.DataPlant["x_O2_V102"].replace(0, np.nan)
                self.DataPlant["x_O2_V102_filled"] = self.DataPlant["x_O2_V102_filled"].ffill()
                self.DataPlant['x_O2_V102_filled'] = self.DataPlant.apply(lambda row: row['x_O2_V102_filled'] if row['x_O2_V102'] == 0 else row['x_O2_V102'], axis=1)
                self.DataPlant['x_O2_V102_filled'] = self.DataPlant['x_O2_V102_filled'].fillna(0).astype(float)
                self.DataPlant['x_O2_V102_filled'] = self.DataPlant['x_O2_V102_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_O2_V102_filled"] = self.DataPlant["x_O2_V102_filled"].mask(self.DataPlant["x_O2_V102_filled"] > 100, np.nan)
                self.DataPlant["x_O2_V102_filled"] = self.DataPlant["x_O2_V102_filled"].ffill()
                mean_value_xO2_V102 = self.DataPlant["x_O2_V102_filled"].mean()
                self.DataPlant["x_O2_V102_filled"] = mean_value_xO2_V102
            else:
                self.DataPlant["x_O2_V102_filled"] = self.DataPlant["x_O2_V102"]
            
            # OXYGEN V107
            if (self.DataPlant["x_O2_V107"] != 0).any():
                self.DataPlant["x_O2_V107_filled"] = self.DataPlant["x_O2_V107"].replace(0, np.nan)
                self.DataPlant["x_O2_V107_filled"] = self.DataPlant["x_O2_V107_filled"].ffill()
                self.DataPlant['x_O2_V107_filled'] = self.DataPlant.apply(lambda row: row['x_O2_V107_filled'] if row['x_O2_V107'] == 0 else row['x_O2_V107'], axis=1)
                self.DataPlant['x_O2_V107_filled'] = self.DataPlant['x_O2_V107_filled'].fillna(0).astype(float)
                self.DataPlant['x_O2_V107_filled'] = self.DataPlant['x_O2_V107_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_O2_V107_filled"] = self.DataPlant["x_O2_V107_filled"].mask(self.DataPlant["x_O2_V107_filled"] > 100, np.nan)
                self.DataPlant["x_O2_V107_filled"] = self.DataPlant["x_O2_V107_filled"].ffill()
                mean_value_xO2_V107 = self.DataPlant["x_O2_V107_filled"].mean()
                self.DataPlant["x_O2_V107_filled"] = mean_value_xO2_V107
            else:
                self.DataPlant["x_O2_V107_filled"] = self.DataPlant["x_O2_V107"]
                
            # Hydrogen V101
            if (self.DataPlant["x_H2_V101"] != 0).any():
                self.DataPlant["x_H2_V101_filled"] = self.DataPlant["x_H2_V101"].replace(0, np.nan)
                self.DataPlant["x_H2_V101_filled"] = self.DataPlant["x_H2_V101_filled"].ffill()
                self.DataPlant['x_H2_V101_filled'] = self.DataPlant.apply(lambda row: row['x_H2_V101_filled'] if row['x_H2_V101'] == 0 else row['x_H2_V101'], axis=1)
                self.DataPlant['x_H2_V101_filled'] = self.DataPlant['x_H2_V101_filled'].fillna(0).astype(float)
                self.DataPlant['x_H2_V101_filled'] = self.DataPlant['x_H2_V101_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_H2_V101_filled"] = self.DataPlant["x_H2_V101_filled"].mask(self.DataPlant["x_H2_V101_filled"] > 100, np.nan)
                self.DataPlant["x_H2_V101_filled"] = self.DataPlant["x_H2_V101_filled"].ffill()
                mean_value_xH2_V101 = self.DataPlant["x_H2_V101_filled"].mean()
                self.DataPlant["x_H2_V101_filled"] = mean_value_xH2_V101
            else:
                self.DataPlant["x_H2_V101_filled"] = self.DataPlant["x_H2_V101"]
            
            # Hydrogen V102
            if (self.DataPlant["x_H2_V102"] != 0).any():
                self.DataPlant["x_H2_V102_filled"] = self.DataPlant["x_H2_V102"].replace(0, np.nan)
                self.DataPlant["x_H2_V102_filled"] = self.DataPlant["x_H2_V102_filled"].ffill()
                self.DataPlant['x_H2_V102_filled'] = self.DataPlant.apply(lambda row: row['x_H2_V102_filled'] if row['x_H2_V102'] == 0 else row['x_H2_V102'], axis=1)
                self.DataPlant['x_H2_V102_filled'] = self.DataPlant['x_H2_V102_filled'].fillna(0).astype(float)
                self.DataPlant['x_H2_V102_filled'] = self.DataPlant['x_H2_V102_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_H2_V102_filled"] = self.DataPlant["x_H2_V102_filled"].mask(self.DataPlant["x_H2_V102_filled"] > 100, np.nan)
                self.DataPlant["x_H2_V102_filled"] = self.DataPlant["x_H2_V102_filled"].ffill()
                mean_value_xH2_V102 = self.DataPlant["x_H2_V102_filled"].mean()
                self.DataPlant["x_H2_V102_filled"] = mean_value_xH2_V102
            else:
                self.DataPlant["x_H2_V102_filled"] = self.DataPlant["x_H2_V102"]
            
            # Hydrogen V107
            if (self.DataPlant["x_H2_V107"] != 0).any():
                self.DataPlant["x_H2_V107_filled"] = self.DataPlant["x_H2_V107"].replace(0, np.nan)
                self.DataPlant["x_H2_V107_filled"] = self.DataPlant["x_H2_V107_filled"].ffill()
                self.DataPlant['x_H2_V107_filled'] = self.DataPlant.apply(lambda row: row['x_H2_V107_filled'] if row['x_H2_V107'] == 0 else row['x_H2_V107'], axis=1)
                self.DataPlant['x_H2_V107_filled'] = self.DataPlant['x_H2_V107_filled'].fillna(0).astype(float)
                self.DataPlant['x_H2_V107_filled'] = self.DataPlant['x_H2_V107_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_H2_V107_filled"] = self.DataPlant["x_H2_V107_filled"].mask(self.DataPlant["x_H2_V107_filled"] > 100, np.nan)
                self.DataPlant["x_H2_V107_filled"] = self.DataPlant["x_H2_V107_filled"].ffill()
                mean_value_xH2_V107 = self.DataPlant["x_H2_V107_filled"].mean()
                self.DataPlant["x_H2_V107_filled"] = mean_value_xH2_V107
            else:
                self.DataPlant["x_H2_V107_filled"] = self.DataPlant["x_H2_V107"]
                
            # Hydrogen sulphide V101
            if (self.DataPlant["x_H2S_V101"] != 0).any():
                self.DataPlant["x_H2S_V101_filled"] = self.DataPlant["x_H2S_V101"].replace(0, np.nan)
                self.DataPlant["x_H2S_V101_filled"] = self.DataPlant["x_H2S_V101_filled"].ffill()
                self.DataPlant['x_H2S_V101_filled'] = self.DataPlant.apply(lambda row: row['x_H2S_V101_filled'] if row['x_H2S_V101'] == 0 else row['x_H2S_V101'], axis=1)
                self.DataPlant['x_H2S_V101_filled'] = self.DataPlant['x_H2S_V101_filled'].fillna(0).astype(float)
                self.DataPlant['x_H2S_V101_filled'] = self.DataPlant['x_H2S_V101_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_H2S_V101_filled"] = self.DataPlant["x_H2S_V101_filled"].mask(self.DataPlant["x_H2S_V101_filled"] > 100, np.nan)
                self.DataPlant["x_H2S_V101_filled"] = self.DataPlant["x_H2S_V101_filled"].ffill()
                mean_value_xH2S_V101 = self.DataPlant["x_H2S_V101_filled"].mean()
                self.DataPlant["x_H2S_V101_filled"] = mean_value_xH2S_V101
            else:
                self.DataPlant["x_H2S_V101_filled"] = self.DataPlant["x_H2S_V101"]
            
            # Hydrogen sulphide V102
            if (self.DataPlant["x_H2S_V102"] != 0).any():
                self.DataPlant["x_H2S_V102_filled"] = self.DataPlant["x_H2S_V102"].replace(0, np.nan)
                self.DataPlant["x_H2S_V102_filled"] = self.DataPlant["x_H2S_V102_filled"].ffill()
                self.DataPlant['x_H2S_V102_filled'] = self.DataPlant.apply(lambda row: row['x_H2S_V102_filled'] if row['x_H2S_V102'] == 0 else row['x_H2S_V102'], axis=1)
                self.DataPlant['x_H2S_V102_filled'] = self.DataPlant['x_H2S_V102_filled'].fillna(0).astype(float)
                self.DataPlant['x_H2S_V102_filled'] = self.DataPlant['x_H2S_V102_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_H2S_V102_filled"] = self.DataPlant["x_H2S_V102_filled"].mask(self.DataPlant["x_H2S_V102_filled"] > 100, np.nan)
                self.DataPlant["x_H2S_V102_filled"] = self.DataPlant["x_H2S_V102_filled"].ffill()
                mean_value_xH2S_V102 = self.DataPlant["x_H2S_V102_filled"].mean()
                self.DataPlant["x_H2S_V102_filled"] = mean_value_xH2S_V102
            else:
                self.DataPlant["x_H2S_V102_filled"] = self.DataPlant["x_H2S_V102"]
            
            # Hydrogen sulphide V107
            if (self.DataPlant["x_H2S_V107"] != 0).any():
                self.DataPlant["x_H2S_V107_filled"] = self.DataPlant["x_H2S_V107"].replace(0, np.nan)
                self.DataPlant["x_H2S_V107_filled"] = self.DataPlant["x_H2S_V107_filled"].ffill()
                self.DataPlant['x_H2S_V107_filled'] = self.DataPlant.apply(lambda row: row['x_H2S_V107_filled'] if row['x_H2S_V107'] == 0 else row['x_H2S_V107'], axis=1)
                self.DataPlant['x_H2S_V107_filled'] = self.DataPlant['x_H2S_V107_filled'].fillna(0).astype(float)
                self.DataPlant['x_H2S_V107_filled'] = self.DataPlant['x_H2S_V107_filled'].replace(0, np.nan).bfill().ffill()
                self.DataPlant["x_H2S_V107_filled"] = self.DataPlant["x_H2S_V107_filled"].mask(self.DataPlant["x_H2S_V107_filled"] > 100, np.nan)
                self.DataPlant["x_H2S_V107_filled"] = self.DataPlant["x_H2S_V107_filled"].ffill()
                mean_value_xH2S_V107 = self.DataPlant["x_H2S_V107_filled"].mean()
                self.DataPlant["x_H2S_V107_filled"] = mean_value_xH2S_V107
            else:
                self.DataPlant["x_H2S_V107_filled"] = self.DataPlant["x_H2S_V107"]
                
            self.DataPlant.reset_index(drop=True, inplace=True)
            
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
            Csus_SV = []
            SV_R101 = []
            Csus_ST = []
            ST_R101 = []
            Q_P104v = []
            timev = []
            SV_g_Gompertz = []
            V_inj_R101 = []
            x_R101 = []
            OC_R101 = []
            
            #Biogas storge
            #V101
            #Pressure
            Pi_V101 = []
            Pacum_V101_i = []
            Pacum_V101 = []
            V_norm_sto_V101 = []
            V_norm_acum_V101 = []
            #Biogas compounds
            mol_acum_biogas_V101 = []
            mol_acum_CH4_V101 = []
            m_acum_CH4_V101 = []
            mol_acum_CO2_V101 = []
            m_acum_CO2_V101 = []
            mol_acum_O2_V101 = []
            m_acum_O2_V101 = []
            mol_acum_H2S_V101 = []
            m_acum_H2S_V101 = []
            mol_acum_H2_V101 = []
            m_acum_H2_V101 = []
            mol_acum_NH3_V101 = []
            m_acum_NH3_V101 = []
            
            #V102
            #Pressure
            Pi_V102 = []
            Pacum_V102_i = []
            Pacum_V102 = []
            V_norm_sto_V102 = []
            V_norm_acum_V102 = []
            #Biogas compounds
            mol_acum_biogas_V102 = []
            mol_acum_CH4_V102 = []
            m_acum_CH4_V102 = []
            mol_acum_CO2_V102 = []
            m_acum_CO2_V102 = []
            mol_acum_O2_V102 = []
            m_acum_O2_V102 = []
            mol_acum_H2S_V102 = []
            m_acum_H2S_V102 = []
            mol_acum_H2_V102 = []
            m_acum_H2_V102 = []
            mol_acum_NH3_V102 = []
            m_acum_NH3_V102 = []
            
            #V107
            #Pressure
            Pi_V107 = []
            Pacum_V107_i = []
            Pacum_V107 = []
            V_norm_sto_V107 = []
            V_norm_acum_V107 = []
            #Biogas compounds
            mol_acum_biogas_V107 = []
            mol_acum_CH4_V107 = []
            m_acum_CH4_V107 = []
            mol_acum_CO2_V107 = []
            m_acum_CO2_V107 = []
            mol_acum_O2_V107 = []
            m_acum_O2_V107 = []
            mol_acum_H2S_V107 = []
            m_acum_H2S_V107 = []
            mol_acum_H2_V107 = []
            m_acum_H2_V107 = []
            mol_acum_NH3_V107 = []
            m_acum_NH3_V107 = []
            
            for i in range (len(self.DataPlant)):
                self.P_V101 = self.DataPlant["P_V101"].iloc[i]
                self.P_V102 = self.DataPlant["P_V102"].iloc[i]
                self.P_V107 = self.DataPlant["P_V107"].iloc[i]
                #conditions when the pressure inside V101 drop
                if i > 0:
                    if (i + 1) in self.DataPlant.index and i in self.DataPlant.index:
                        tp = self.DataPlant["normTime"].iloc[i] - self.DataPlant["normTime"].iloc[i-1]
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
                # ----------------------V101
                # Storage biogas mol in V101
                self.T_V101_actual = self.DataPlant["T_V101"].iloc[i]
                if self.DataPlant["T_V101"].iloc[i] == 0:
                    self.T_V101_actual = self.DataPlant["T_V101"].iloc[i+1]

                self.n_biogas_sto_V101 = (((self.P_V101*6894.76) * (self.Volume_V101/1000))/
                                          (8.314 * (self.T_V101_actual + 273.15)))           #mol
                #Storage normal volume
                self.V_norm_sto_V101 = (self.P_V101 * self.Volume_V101 * 273.15)/(14.503774 * (self.T_V101_actual + 273.15))      #L
                
                # Accumulated biogas mol in V101
                self.n_biogas_acum_V101 = (((self.Pacum_V101*6894.76) * (self.Volume_V101/1000))/
                                          (8.314 * (self.T_V101_actual + 273.15)))           #mol
                # Accumulated normal volume
                self.V_norm_acum_V101 = (self.Pacum_V101 * self.Volume_V101 * 273.15)/(14.503774 * (self.T_V101_actual + 273.15))  #NL
                                
                mol_acum_biogas_V101.append(self.n_biogas_acum_V101)
                V_norm_sto_V101.append(self.V_norm_sto_V101)
                V_norm_acum_V101.append(self.V_norm_acum_V101)
                
                #Estimate the storage and accumulated mol for component in biogas
                #Storage compounds [mol]
                self.mol_sto_CH4_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_CH4_V101_filled"].iloc[i]/100)      #mol
                self.mol_sto_CO2_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_CO2_V101_filled"].iloc[i]/100)      #mol
                self.mol_sto_O2_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_O2_V101_filled"].iloc[i]/100)        #mol
                self.mol_sto_H2S_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_H2S_V101_filled"].iloc[i]/1000000)      #mol
                self.mol_sto_H2_V101 = self.n_biogas_sto_V101 *  (self.DataPlant["x_H2_V101_filled"].iloc[i]/1000000)        #mol
                self.mol_sto_NH3_V101 = self.mol_sto_CH4_V101 * (self.s_NH3/self.s_CH4)                                      #mol
                #Storage compounds [g]
                self.m_sto_CH4_V101 = self.mol_sto_CH4_V101 * 16.04256                                                         #g
                self.m_sto_CO2_V101 = self.mol_sto_CO2_V101 * 44.0095                                                          #g
                self.m_sto_O2_V101 = self.mol_sto_O2_V101 * 31.9988                                                            #g
                self.m_sto_H2S_V101 = self.mol_sto_H2S_V101 * 34.08088                                                         #g
                self.m_sto_H2_V101 =  self.mol_sto_H2_V101 *2.016                                                              #g
                self.m_sto_NH3_V101 = self.mol_sto_NH3_V101 *  17.031                                                          #g 
                
                #Accumulated compounds [mol]
                self.mol_acum_CH4_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_CH4_V101_filled"].iloc[i]/100)     #mol
                self.mol_acum_CO2_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_CO2_V101_filled"].iloc[i]/100)      #mol
                self.mol_acum_O2_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_O2_V101_filled"].iloc[i]/100)        #mol
                self.mol_acum_H2S_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_H2S_V101_filled"].iloc[i]/1000000)      #mol
                self.mol_acum_H2_V101 = self.n_biogas_acum_V101 *  (self.DataPlant["x_H2_V101_filled"].iloc[i]/1000000)       #mol
                self.mol_acum_NH3_V101 = self.mol_acum_CH4_V101 * (self.s_NH3/self.s_CH4)                                      #mol
                #storage values in list [mol]
                mol_acum_CH4_V101.append(self.mol_acum_CH4_V101)
                mol_acum_CO2_V101.append(self.mol_acum_CO2_V101)
                mol_acum_O2_V101.append(self.mol_acum_O2_V101)
                mol_acum_H2S_V101.append(self.mol_acum_H2S_V101)
                mol_acum_H2_V101.append(self.mol_acum_H2_V101)
                mol_acum_NH3_V101.append(self.mol_acum_NH3_V101)
                #accumulated compounds [g]
                self.m_acum_CH4_V101 = self.mol_acum_CH4_V101 * 16.04256                                                         #g
                self.m_acum_CO2_V101 = self.mol_acum_CO2_V101 * 44.0095                                                          #g
                self.m_acum_O2_V101 = self.mol_acum_O2_V101 * 31.9988                                                            #g
                self.m_acum_H2S_V101 = self.mol_acum_H2S_V101 * 34.08088                                                         #g
                self.m_acum_H2_V101 =  self.mol_acum_H2_V101 *2.016                                                              #g
                self.m_acum_NH3_V101 = self.mol_acum_NH3_V101 *  17.031                                                          #g 
                #storage values in list [g]
                m_acum_CH4_V101.append(self.m_acum_CH4_V101)
                m_acum_CO2_V101.append(self.m_acum_CO2_V101)
                m_acum_O2_V101.append(self.m_acum_O2_V101)
                m_acum_H2S_V101.append(self.m_acum_H2S_V101)
                m_acum_H2_V101.append(self.m_acum_H2_V101)
                m_acum_NH3_V101.append(self.m_acum_NH3_V101)
                
                # -------------------- V102
                # Storage biogas mol in V102
                self.T_V102_actual = self.DataPlant["T_V102"].iloc[i]
                if self.DataPlant["T_V102"].iloc[i] == 0:
                    self.T_V102_actual = self.DataPlant["T_V102"].iloc[i+1]

                self.n_biogas_sto_V102 = (((self.P_V102*6894.76) * (self.Volume_V102/1000))/
                                          (8.314 * (self.T_V102_actual + 273.15)))           #mol
                #Storage normal volume
                self.V_norm_sto_V102 = (self.P_V102 * self.Volume_V102 * 273.15)/(14.503774 * (self.T_V102_actual + 273.15))      #L
                
                # Accumulated biogas mol in V102
                self.n_biogas_acum_V102 = (((self.Pacum_V102*6894.76) * (self.Volume_V102/1000))/
                                          (8.314 * (self.T_V102_actual + 273.15)))           #mol
                # Accumulated normal volume
                self.V_norm_acum_V102 = (self.Pacum_V102 * self.Volume_V102 * 273.15)/(14.503774 * (self.T_V102_actual + 273.15))  #L
                                
                mol_acum_biogas_V102.append(self.n_biogas_acum_V102)
                V_norm_sto_V102.append(self.V_norm_sto_V102)
                V_norm_acum_V102.append(self.V_norm_acum_V102)
                
                #Estimate the storage and accumulated mol for component in biogas
                #Storage compounds [mol]
                self.mol_sto_CH4_V102 = self.n_biogas_sto_V102 *  (self.DataPlant["x_CH4_V102_filled"].iloc[i]/100)      #mol
                self.mol_sto_CO2_V102 = self.n_biogas_sto_V102 *  (self.DataPlant["x_CO2_V102_filled"].iloc[i]/100)      #mol
                self.mol_sto_O2_V102 = self.n_biogas_sto_V102 *  (self.DataPlant["x_O2_V102_filled"].iloc[i]/100)        #mol
                self.mol_sto_H2S_V102 = self.n_biogas_sto_V102 *  (self.DataPlant["x_H2S_V102_filled"].iloc[i]/1000000)      #mol
                self.mol_sto_H2_V102 = self.n_biogas_sto_V102 *  (self.DataPlant["x_H2_V102_filled"].iloc[i]/1000000)        #mol
                self.mol_sto_NH3_V102 = self.mol_sto_CH4_V102 * (self.s_NH3/self.s_CH4)                                      #mol
                #Storage compounds [g]
                self.m_sto_CH4_V102 = self.mol_sto_CH4_V102 * 16.04256                                                         #g
                self.m_sto_CO2_V102 = self.mol_sto_CO2_V102 * 44.0095                                                          #g
                self.m_sto_O2_V102 = self.mol_sto_O2_V102 * 31.9988                                                            #g
                self.m_sto_H2S_V102 = self.mol_sto_H2S_V102 * 34.08088                                                         #g
                self.m_sto_H2_V102 =  self.mol_sto_H2_V102 *2.016                                                              #g
                self.m_sto_NH3_V102 = self.mol_sto_NH3_V102 *  17.031                                                          #g 
                
                #Accumulated compounds [mol]
                self.mol_acum_CH4_V102 = self.n_biogas_acum_V102 *  (self.DataPlant["x_CH4_V102_filled"].iloc[i]/100)     #mol
                self.mol_acum_CO2_V102 = self.n_biogas_acum_V102 *  (self.DataPlant["x_CO2_V102_filled"].iloc[i]/100)      #mol
                self.mol_acum_O2_V102 = self.n_biogas_acum_V102 *  (self.DataPlant["x_O2_V102_filled"].iloc[i]/100)        #mol
                self.mol_acum_H2S_V102 = self.n_biogas_acum_V102 *  (self.DataPlant["x_H2S_V102_filled"].iloc[i]/1000000)      #mol
                self.mol_acum_H2_V102 = self.n_biogas_acum_V102 *  (self.DataPlant["x_H2_V102_filled"].iloc[i]/1000000)       #mol
                self.mol_acum_NH3_V102 = self.mol_acum_CH4_V102 * (self.s_NH3/self.s_CH4)                                      #mol
                #storage values in list [mol]
                mol_acum_CH4_V102.append(self.mol_acum_CH4_V102)
                mol_acum_CO2_V102.append(self.mol_acum_CO2_V102)
                mol_acum_O2_V102.append(self.mol_acum_O2_V102)
                mol_acum_H2S_V102.append(self.mol_acum_H2S_V102)
                mol_acum_H2_V102.append(self.mol_acum_H2_V102)
                mol_acum_NH3_V102.append(self.mol_acum_NH3_V102)
                #accumulated compounds [g]
                self.m_acum_CH4_V102 = self.mol_acum_CH4_V102 * 16.04256                                                         #g
                self.m_acum_CO2_V102 = self.mol_acum_CO2_V102 * 44.0095                                                          #g
                self.m_acum_O2_V102 = self.mol_acum_O2_V102 * 31.9988                                                            #g
                self.m_acum_H2S_V102 = self.mol_acum_H2S_V102 * 34.08088                                                         #g
                self.m_acum_H2_V102 =  self.mol_acum_H2_V102 *2.016                                                              #g
                self.m_acum_NH3_V102 = self.mol_acum_NH3_V102 *  17.031                                                          #g 
                #storage values in list [g]
                m_acum_CH4_V102.append(self.m_acum_CH4_V102)
                m_acum_CO2_V102.append(self.m_acum_CO2_V102)
                m_acum_O2_V102.append(self.m_acum_O2_V102)
                m_acum_H2S_V102.append(self.m_acum_H2S_V102)
                m_acum_H2_V102.append(self.m_acum_H2_V102)
                m_acum_NH3_V102.append(self.m_acum_NH3_V102)
                
                # -------------------- V107
                # Storage biogas mol in V107
                self.T_V107_actual = self.DataPlant["T_V107"].iloc[i]
                if self.DataPlant["T_V107"].iloc[i] == 0:
                    self.T_V107_actual = self.DataPlant["T_V107"].iloc[i+1]

                self.n_biogas_sto_V107 = (((self.P_V107*6894.76) * (self.Volume_V107/1000))/
                                          (8.314 * (self.T_V107_actual + 273.15)))           #mol
                #Storage normal volume
                self.V_norm_sto_V107 = (self.P_V107 * self.Volume_V107 * 273.15)/(14.503774 * (self.T_V107_actual + 273.15))      #L
                
                # Accumulated biogas mol in V107
                self.n_biogas_acum_V107 = (((self.Pacum_V107*6894.76) * (self.Volume_V107/1000))/
                                          (8.314 * (self.T_V107_actual + 273.15)))           #mol
                # Accumulated normal volume
                self.V_norm_acum_V107 = (self.Pacum_V107 * self.Volume_V107 * 273.15)/(14.503774 * (self.T_V107_actual + 273.15))  #L
                                
                mol_acum_biogas_V107.append(self.n_biogas_acum_V107)
                V_norm_sto_V107.append(self.V_norm_sto_V107)
                V_norm_acum_V107.append(self.V_norm_acum_V107)
                
                #Estimate the storage and accumulated mol for component in biogas
                #Storage compounds [mol]
                self.mol_sto_CH4_V107 = self.n_biogas_sto_V107 *  (self.DataPlant["x_CH4_V107_filled"].iloc[i]/100)      #mol
                self.mol_sto_CO2_V107 = self.n_biogas_sto_V107 *  (self.DataPlant["x_CO2_V107_filled"].iloc[i]/100)      #mol
                self.mol_sto_O2_V107 = self.n_biogas_sto_V107 *  (self.DataPlant["x_O2_V107_filled"].iloc[i]/100)        #mol
                self.mol_sto_H2S_V107 = self.n_biogas_sto_V107 *  (self.DataPlant["x_H2S_V107_filled"].iloc[i]/1000000)      #mol
                self.mol_sto_H2_V107 = self.n_biogas_sto_V107 *  (self.DataPlant["x_H2_V107_filled"].iloc[i]/1000000)        #mol
                self.mol_sto_NH3_V107 = self.mol_sto_CH4_V107 * (self.s_NH3/self.s_CH4)                                      #mol
                #Storage compounds [g]
                self.m_sto_CH4_V107 = self.mol_sto_CH4_V107 * 16.04256                                                         #g
                self.m_sto_CO2_V107 = self.mol_sto_CO2_V107 * 44.0095                                                          #g
                self.m_sto_O2_V107 = self.mol_sto_O2_V107 * 31.9988                                                            #g
                self.m_sto_H2S_V107 = self.mol_sto_H2S_V107 * 34.08088                                                         #g
                self.m_sto_H2_V107 =  self.mol_sto_H2_V107 *2.016                                                              #g
                self.m_sto_NH3_V107 = self.mol_sto_NH3_V107 *  17.031                                                          #g 
                
                #Accumulated compounds [mol]
                self.mol_acum_CH4_V107 = self.n_biogas_acum_V107 *  (self.DataPlant["x_CH4_V107_filled"].iloc[i]/100)     #mol
                self.mol_acum_CO2_V107 = self.n_biogas_acum_V107 *  (self.DataPlant["x_CO2_V107_filled"].iloc[i]/100)      #mol
                self.mol_acum_O2_V107 = self.n_biogas_acum_V107 *  (self.DataPlant["x_O2_V107_filled"].iloc[i]/100)        #mol
                self.mol_acum_H2S_V107 = self.n_biogas_acum_V107 *  (self.DataPlant["x_H2S_V107_filled"].iloc[i]/1000000)      #mol
                self.mol_acum_H2_V107 = self.n_biogas_acum_V107 *  (self.DataPlant["x_H2_V107_filled"].iloc[i]/1000000)       #mol
                self.mol_acum_NH3_V107 = self.mol_acum_CH4_V107 * (self.s_NH3/self.s_CH4)                                      #mol
                #storage values in list [mol]
                mol_acum_CH4_V107.append(self.mol_acum_CH4_V107)
                mol_acum_CO2_V107.append(self.mol_acum_CO2_V107)
                mol_acum_O2_V107.append(self.mol_acum_O2_V107)
                mol_acum_H2S_V107.append(self.mol_acum_H2S_V107)
                mol_acum_H2_V107.append(self.mol_acum_H2_V107)
                mol_acum_NH3_V107.append(self.mol_acum_NH3_V107)
                #accumulated compounds [g]
                self.m_acum_CH4_V107 = self.mol_acum_CH4_V107 * 16.04256                                                         #g
                self.m_acum_CO2_V107 = self.mol_acum_CO2_V107 * 44.0095                                                          #g
                self.m_acum_O2_V107 = self.mol_acum_O2_V107 * 31.9988                                                            #g
                self.m_acum_H2S_V107 = self.mol_acum_H2S_V107 * 34.08088                                                         #g
                self.m_acum_H2_V107 =  self.mol_acum_H2_V107 *2.016                                                              #g
                self.m_acum_NH3_V107 = self.mol_acum_NH3_V107 *  17.031                                                          #g 
                #storage values in list [g]
                m_acum_CH4_V107.append(self.m_acum_CH4_V107)
                m_acum_CO2_V107.append(self.m_acum_CO2_V107)
                m_acum_O2_V107.append(self.m_acum_O2_V107)
                m_acum_H2S_V107.append(self.m_acum_H2S_V107)
                m_acum_H2_V107.append(self.m_acum_H2_V107)
                m_acum_NH3_V107.append(self.m_acum_NH3_V107)
                 
                
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
                    x_substrate = self.Vsus_inj_total_R101 / 30
                    x_inoculum = (1 - x_substrate)
                    # print(x_inoculum)
                    
                #Volatile solids [mol]
                mol_ini = self.Csus_ini_SV_R101 * (self.Level_R101_actual)                            #mol
                mol_in_R101 = Q_P104 * tp * self.Csv_sus                                              #mol
                if len(mol_acum_CH4_V101)<1:
                    mol_expended = 0
                else:
                    mol_expended_CH4 = ((mol_acum_CH4_V101[i] - mol_acum_CH4_V101[i-1])) * (1/(x_substrate*self.s_CH4 + x_inoculum*self.s_CH4_ini_R101))            #mol
                    mol_expended_CO2 = ((mol_acum_CO2_V101[i] - mol_acum_CO2_V101[i-1])) * (1/(x_substrate*self.s_CO2 + x_inoculum*self.s_CO2_ini_R101))            #mol
                    mol_expended_NH3 = ((mol_acum_NH3_V101[i] - mol_acum_NH3_V101[i-1])) * (1/(x_substrate*self.s_NH3 + x_inoculum*self.s_NH3_ini_R101))            #mol
                    try:
                        mol_expended_H2S = ((mol_acum_H2S_V101[i] - mol_acum_H2S_V101[i-1])) * (1/(x_substrate*self.s_H2S + x_inoculum*self.s_H2S_ini_R101))            #mol
                    except ZeroDivisionError:
                        mol_expended_H2S = 0
                    mol_expended = (mol_expended_CH4 + mol_expended_CO2 + mol_expended_NH3 + mol_expended_H2S)
                mol_out_R101 = (Q_P104 * tp * self.Csus_ini_SV_R101)   
                self.Csus_ini_SV_R101 = (mol_ini + mol_in_R101 - mol_out_R101 - mol_expended)/(self.Level_R101_actual)                                           #molSV/L
                #Volatile solids [g]
                self.Csus_ini_SV_R101_gl = self.Csus_ini_SV_R101 * (x_inoculum * self.MW_inocum_ini_R101 + x_substrate * self.MW_sustrato)                       #gSV/L
                self.SV_R101 = self.Csus_ini_SV_R101_gl / (x_inoculum * self.rho_ini_R101 + x_substrate * self.rho)                                              #gTS/gT
                self.SV_g = self.Csus_ini_SV_R101_gl * self.Level_R101_actual                                            #gSV
                SV_g_Gompertz.append(self.SV_g)       
                
                #Total solids [g]
                mol_ini_ST = self.Csus_ini_ST_R101 * (self.Level_R101_actual)                         #mol
                mol_in_R101_ST = Q_P104 * tp * self.Cst_sus                                           #mol
                mol_out_R101_ST = (Q_P104 * tp * self.Csus_ini_ST_R101)                               #mol
                self.Csus_ini_ST_R101 = (mol_ini_ST + mol_in_R101_ST  - mol_out_R101_ST - mol_expended)/(self.Level_R101_actual)                               #molST/L
                #Total Solids [g]
                self.Csus_ini_ST_R101_gl = self.Csus_ini_ST_R101 * (x_inoculum * self.MW_inocum_ini_R101 + x_substrate * self.MW_sustrato)                     #gST/L
                self.ST_R101 = (self.Csus_ini_ST_R101_gl / (x_inoculum * self.rho_ini_R101 + x_substrate * self.rho))                                            #gTS/gT 
                self.ST_g = self.Csus_ini_ST_R101_gl * self.Level_R101_actual                                          #gST
                
                #convertion R101
                try:
                    self.x_R101 = (self.Csv_sus - self.Csus_ini_SV_R101)/self.Csv_sus
                    self.OC_R101 = self.Csus_ini_SV_R101_gl/(self.DataPlant["normTime"].iloc[i]/1440)
                except ZeroDivisionError:
                    self.x_R101 = 0
                    self.OC_R101 = 0
                
                timev.append(self.DataPlant["normTime"].iloc[i])
                V.append(self.Level_R101_actual)
                Q_P104v.append(Q_P104)   
                C_in_sus.append(self.Csv_sus)
                
                if math.isnan(self.Csus_ini_SV_R101):
                    Csus.append(Csus[-1])
                else:
                    Csus.append(self.Csus_ini_SV_R101)
                
                if math.isnan(self.Csus_ini_SV_R101_gl):
                    Csus_SV.append(Csus_SV[-1])
                else:
                    Csus_SV.append(self.Csus_ini_SV_R101_gl)
                
                if math.isnan(self.SV_R101):
                    SV_R101.append(SV_R101[-1])
                else:
                    SV_R101.append(self.SV_R101)
                    
                if math.isnan(self.Csus_ini_ST_R101_gl):
                    Csus_ST.append(Csus_ST[-1])
                else:
                    Csus_ST.append(self.Csus_ini_ST_R101_gl)
                
                if math.isnan(self.ST_R101):
                    ST_R101.append(ST_R101[-1])
                else:
                    ST_R101.append(self.ST_R101)
                
                if math.isnan(self.x_R101):
                    x_R101.append(x_R101[-1])
                else:
                    x_R101.append(self.x_R101)
                    
                if math.isnan(self.OC_R101):
                    OC_R101.append(OC_R101[-1])
                else:
                    OC_R101.append(self.OC_R101)
                
                V_inj_R101.append(self.Vsus_inj_total_R101)
            
            #DataFrame to realize optimization
            if self.Operation_mode == 1:
                self.TrainMode1 = pd.DataFrame({"time": timev,
                                                "Vol": V,
                                                "Q_P104": Q_P104v,
                                                "Csus_in": C_in_sus,
                                                "Csus_exp":Csus,
                                                "Csus_exp_SV":Csus_SV,
                                                "SV": SV_R101,
                                                "Csus_exp_ST":Csus_ST,
                                                "ST": ST_R101,
                                                "x": x_R101,
                                                "OC": OC_R101,
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
            else:
                self.TrainMode2 = pd.DataFrame({"time": timev,
                                                "Vol": V,
                                                "Q_P104": Q_P104v,
                                                "Csus_in": C_in_sus,
                                                "Csus_exp":Csus,
                                                "Csus_exp_SV":Csus_SV,
                                                "SV": SV_R101,
                                                "Csus_exp_ST":Csus_ST,
                                                "ST": ST_R101,
                                                "x": x_R101,
                                                "OC":OC_R101,
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
            
            self.biogas_V101 = pd.DataFrame({"time":timev,
                                             "Pstorage": self.DataPlant["P_V101"],
                                             "Vacum": V_norm_acum_V101,
                                             "Vsto": V_norm_sto_V101,
                                             "mol_biogas": mol_acum_biogas_V101,
                                             "mol_CH4": mol_acum_CH4_V101,
                                             "mol_CO2": mol_acum_CO2_V101,
                                             "mol_O2": mol_acum_O2_V101,
                                             "mol_H2S": mol_acum_H2S_V101,
                                             "mol_H2": mol_acum_H2_V101,
                                             "mol_NH3": mol_acum_NH3_V101})
            
            self.biogas_V102 = pd.DataFrame({"time":timev,
                                             "Pstorage": self.DataPlant["P_V102"],
                                             "Vacum": V_norm_acum_V102,
                                             "Vsto": V_norm_sto_V102,
                                             "mol_biogas": mol_acum_biogas_V102,
                                             "mol_CH4": mol_acum_CH4_V102,
                                             "mol_CO2": mol_acum_CO2_V102,
                                             "mol_O2": mol_acum_O2_V102,
                                             "mol_H2S": mol_acum_H2S_V102,
                                             "mol_H2": mol_acum_H2_V102,
                                             "mol_NH3": mol_acum_NH3_V102})
            
            self.biogas_V107 = pd.DataFrame({"time":timev,
                                             "Pstorage": self.DataPlant["P_V107"],
                                             "Vacum": V_norm_acum_V107,
                                             "Vsto": V_norm_sto_V107,
                                             "mol_biogas": mol_acum_biogas_V107,
                                             "mol_CH4": mol_acum_CH4_V107,
                                             "mol_CO2": mol_acum_CO2_V107,
                                             "mol_O2": mol_acum_O2_V107,
                                             "mol_H2S": mol_acum_H2S_V107,
                                             "mol_H2": mol_acum_H2_V107,
                                             "mol_NH3": mol_acum_NH3_V107})
              
            #Data to train Gompertz model in operation Model 1
            self.Model = Model
            if self.Model == "Gompertz":
                V_biogas_gompertz = []
                V_normal = []
                for i in range (len(mol_acum_biogas_V101)):
                    V_bio = V_norm_acum_V101[i]/SV_g_Gompertz[i]        #Normal volume of biogas according to produce moles in V_101 (L/gSV)
                    V_normal.append(V_norm_acum_V101[i])
                    V_biogas_gompertz.append(V_bio)
                self.TrainGompertzMode1 = pd.DataFrame({"time": timev,
                                                        "V_norm_bio": V_normal,
                                                        "y_t_exp": V_biogas_gompertz})
    
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
            Q_P104 = (self.TrainMode1["Q_P104"]/60).tolist()    #L/s 
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
            
            self.Optimized_parameters = pd.DataFrame({"time": self.TrainMode2["time"],
                                                      "K_R101": K,
                                                      "Ea_R101": Ea})
        
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
                self.K_mean_R101 = Opt_kinetic_params.x[0]
                self.Ea_mean_R101 = Opt_kinetic_params.x[1]
            
            self.K_mean_R101 = st.mean(K)
            self.Ea_mean_R101 = st.mean(Ea)
            
            self.Optimized_parameters = pd.DataFrame({"time": self.TrainMode2["time"],
                                                      "K_R101": K,
                                                      "Ea_R101": Ea})
    
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
                self.K_mean_R101 = Opt_kinetic_params.x[0]
            
            self.K_mean_R101 = st.mean(K)
            self.Optimized_parameters = pd.DataFrame({"time": self.TrainMode2["time"],
                                                      "K_R101": K })
    
    def OptimizationGompertz(self, resolution):
        
        def model_Gompertz(t, ym, U, L):
            t = np.array(t, dtype = float)
            y_t = ym * np.exp(-np.exp(((U*np.e)/ym)*(L-t)+1))
            return y_t
        
        def Optimization_Gompertz (params, t, y_exp):
            def objective(x):
                ym, U, L = x
                y_pred = model_Gompertz(t, ym, U, L)
                residuals = np.array(y_exp) - y_pred
                return np.sum(residuals**2)

            result = minimize(objective, [float(p) for p in params], method='Nelder-Mead')
            return result
        
        if self.Operation_mode == 1 or self.Operation_mode == 2:
            t_exp = self.TrainGompertzMode1["time"].tolist()
            y_exp = self.TrainGompertzMode1["y_t_exp"].tolist()
            Results = Optimization_Gompertz(params = (self.ym_R101, self.U_R101, self.L_R101), t = t_exp, y_exp = y_exp)
            self.Optimized_parameters = pd.DataFrame({"ym": Results.x[0],
                                                      "U": Results.x[1],
                                                      "L": Results.x[2]}, index=[0])
            self.ym_R101 = float(Results.x[0])
            self.U_R101 = float(Results.x[1])
            self.L_R101 = float(Results.x[2])   
    
    def V101model1_2 (self):
        self.Vnorm_bio_V101 = ((self.Pacum_V101 * 6894.76) * self.Volume_V101 * 273.15)/(100000 * (self.T_V101_actual+273.15))
        self.Vnorm_bio_sto_V101 = ((self.P_V101 * 6894.76) * self.Volume_V101 * 273.15)/(100000 * (self.T_V101_actual+273.15))
        self.VCH4_acum_V101 = self.Vnorm_bio_V101 * (self.DataPlant["x_CH4_V101"].iloc[-1]/100)
        self.xCH4_V101 = self.DataPlant["x_CH4_V101"].iloc[-1]
        self.VCO2_acum_V101 = self.Vnorm_bio_V101 * (self.DataPlant["x_CO2_V101"].iloc[-1]/100)
        self.xCO2_V101 = self.DataPlant["x_CO2_V101"].iloc[-1]
        self.VH2S_acum_V101 = self.Vnorm_bio_V101 * (self.DataPlant["x_H2S_V101"].iloc[-1]/100)
        self.xH2S_V101 = self.DataPlant["x_H2S_V101"].iloc[-1]
        self.VO2_acum_V101 = self.Vnorm_bio_V101 * (self.DataPlant["x_O2_V101"].iloc[-1]/100)
        self.xO2_V101 = self.DataPlant["x_O2_V101"].iloc[-1]
        self.VH2_acum_V101 = self.Vnorm_bio_V101 * (self.DataPlant["x_H2_V101"].iloc[-1]/100)
        self.xH2_V101 = self.DataPlant["x_H2_V101"].iloc[-1]
        mol_biogas_Acum_dry_V101 = self.mol_acum_CH4_V101 + self.mol_acum_CO2_V101 + self.mol_acum_H2S_V101 + self.mol_acum_O2_V101 + self.mol_acum_H2_V101 + self.mol_acum_NH3_V101
        try:
            if mol_biogas_Acum_dry_V101 > 0:
                self.xNH3_V101 = (self.mol_acum_NH3_V101/mol_biogas_Acum_dry_V101)*1000000
            else:
                self.xNH3_V101 = 0
        except ZeroDivisionError:
            self.xNH3_V101 = 0
        self.VNH3_acum_V101 = self.Vnorm_bio_V101 * self.xNH3_V101
        mol_biogas_Acum_dry_V101 = self.mol_acum_CH4_V101 + self.mol_acum_CO2_V101 + self.mol_acum_H2S_V101 + self.mol_acum_O2_V101 + self.mol_acum_H2_V101 + self.mol_acum_NH3_V101
        self.xNH3_V101 = (self.mol_acum_NH3_V101/mol_biogas_Acum_dry_V101)*1000000
        self.RH_V101 = self.DataPlant["rh_V101"].iloc[-1]
        Absolute_humidity_V101 = self.Thermo.BiogasAbsoluteHumidity(RH = self.DataPlant["rh_V101"].iloc[-1]/100, T = self.T_V101_actual)
        self.mol_acum_H2O_V101 = (Absolute_humidity_V101 * self.Vnorm_bio_sto_V101) / 18
        Energy_V101 = self.Thermo.LHV(molCH4=self.mol_acum_CH4_V101, molCO2=self.mol_acum_CO2_V101, molH2S=self.mol_acum_H2S_V101, molO2=self.mol_acum_O2_V101, molH2 = self.mol_acum_H2_V101)
        self.Energy_V101 = Energy_V101[1]/3600
        self.LHV_V101 = Energy_V101[0]

    def V102model1_2 (self):
        self.Vnorm_bio_V102 = ((self.Pacum_V102 * 6894.76) * self.Volume_V102 * 273.15)/(100000 * (self.T_V102_actual+273.15))
        self.Vnorm_bio_sto_V102 = ((self.P_V102 * 6894.76) * self.Volume_V102 * 273.15)/(100000 * (self.T_V102_actual+273.15))
        self.VCH4_acum_V102 = self.Vnorm_bio_V102 * (self.DataPlant["x_CH4_V102"].iloc[-1]/100)
        self.xCH4_V102 = self.DataPlant["x_CH4_V102"].iloc[-1]
        self.VCO2_acum_V102 = self.Vnorm_bio_V102 * (self.DataPlant["x_CO2_V102"].iloc[-1]/100)
        self.xCO2_V102 = self.DataPlant["x_CO2_V102"].iloc[-1]
        self.VH2S_acum_V102 = self.Vnorm_bio_V102 * (self.DataPlant["x_H2S_V102"].iloc[-1]/100)
        self.xH2S_V102 = self.DataPlant["x_H2S_V102"].iloc[-1]
        self.VO2_acum_V102 = self.Vnorm_bio_V102 * (self.DataPlant["x_O2_V102"].iloc[-1]/100)
        self.xO2_V102 = self.DataPlant["x_O2_V102"].iloc[-1]
        self.VH2_acum_V102 = self.Vnorm_bio_V102 * (self.DataPlant["x_H2_V102"].iloc[-1]/100)
        self.xH2_V102 = self.DataPlant["x_H2_V102"].iloc[-1]
        mol_biogas_Acum_dry_V102 = self.mol_acum_CH4_V102 + self.mol_acum_CO2_V102 + self.mol_acum_H2S_V102 + self.mol_acum_O2_V102 + self.mol_acum_H2_V102 + self.mol_acum_NH3_V102
        try:
            if mol_biogas_Acum_dry_V102 > 0:
                self.xNH3_V102 = (self.mol_acum_NH3_V102/mol_biogas_Acum_dry_V102)*1000000
            else:
                self.xNH3_V102 = 0
        except ZeroDivisionError:
            self.xNH3_V102 = 0
        self.VNH3_acum_V102 = self.Vnorm_bio_V102 * self.xNH3_V102
        self.RH_V102 = self.DataPlant["rh_V102"].iloc[-1]
        Absolute_humidity_V102 = self.Thermo.BiogasAbsoluteHumidity(RH = self.DataPlant["rh_V102"].iloc[-1]/100, T = self.T_V102_actual)
        self.mol_acum_H2O_V102 = (Absolute_humidity_V102 * self.Vnorm_bio_sto_V102) / 18
        Energy_V102 = self.Thermo.LHV(molCH4=self.mol_acum_CH4_V102, molCO2=self.mol_acum_CO2_V102, molH2S=self.mol_acum_H2S_V102, molO2=self.mol_acum_O2_V102, molH2 = self.mol_acum_H2_V102)
        self.Energy_V102 = Energy_V102[1]/3600
        self.LHV_V102 = Energy_V102[0]
    
    def V107model1_2 (self):
        self.Vnorm_bio_V107 = ((self.Pacum_V107 * 6894.76) * self.Volume_V107 * 273.15)/(100000 * (self.T_V107_actual+273.15))
        self.Vnorm_bio_sto_V107 = ((self.P_V107 * 6894.76) * self.Volume_V107 * 273.15)/(100000 * (self.T_V107_actual+273.15))
        self.VCH4_acum_V107 = self.Vnorm_bio_V107 * (self.DataPlant["x_CH4_V107"].iloc[-1]/100)
        self.xCH4_V107 = self.DataPlant["x_CH4_V107"].iloc[-1]
        self.VCO2_acum_V107 = self.Vnorm_bio_V107 * (self.DataPlant["x_CO2_V107"].iloc[-1]/100)
        self.xCO2_V107 = self.DataPlant["x_CO2_V107"].iloc[-1]
        self.VH2S_acum_V107 = self.Vnorm_bio_V107 * (self.DataPlant["x_H2S_V107"].iloc[-1]/100)
        self.xH2S_V107 = self.DataPlant["x_H2S_V107"].iloc[-1]
        self.VO2_acum_V107 = self.Vnorm_bio_V107 * (self.DataPlant["x_O2_V107"].iloc[-1]/100)
        self.xO2_V107 = self.DataPlant["x_O2_V107"].iloc[-1]
        self.VH2_acum_V107 = self.Vnorm_bio_V107 * (self.DataPlant["x_H2_V107"].iloc[-1]/100)
        self.xH2_V107 = self.DataPlant["x_H2_V107"].iloc[-1]
        mol_biogas_Acum_dry_V107 = self.mol_acum_CH4_V107 + self.mol_acum_CO2_V107 + self.mol_acum_H2S_V107 + self.mol_acum_O2_V107 + self.mol_acum_H2_V107 + self.mol_acum_NH3_V107
        try:
            if mol_biogas_Acum_dry_V107 > 0:
                self.xNH3_V107 = (self.mol_acum_NH3_V107/mol_biogas_Acum_dry_V107)*1000000
            else:
                self.xNH3_V107 = 0
        except ZeroDivisionError:
            self.xNH3_V107 = 0
        self.VNH3_acum_V107 = self.Vnorm_bio_V107 * self.xNH3_V107
        self.RH_V107 = self.DataPlant["rh_V107"].iloc[-1]
        Absolute_humidity_V107 = self.Thermo.BiogasAbsoluteHumidity(RH = self.DataPlant["rh_V107"].iloc[-1]/100, T = self.T_V107_actual)
        self.mol_acum_H2O_V107 = (Absolute_humidity_V107 * self.Vnorm_bio_sto_V107) / 18
        Energy_V107 = self.Thermo.LHV(molCH4=self.mol_acum_CH4_V107, molCO2=self.mol_acum_CO2_V107, molH2S=self.mol_acum_H2S_V107, molO2=self.mol_acum_O2_V107, molH2 = self.mol_acum_H2_V107)
        self.Energy_V107 = Energy_V107[1]/3600
        self.LHV_V107 = Energy_V107[0]
        
    def biogas_treatment_optimization (self, W_feSO4, W_silica):
        
        self.biogas_V101["mol_T"] = self.biogas_V101["mol_CH4"] + self.biogas_V101["mol_CO2"] + self.biogas_V101["mol_O2"] + self.biogas_V101["mol_H2S"] + self.biogas_V101["mol_H2"] + self.biogas_V101["mol_NH3"]
        self.biogas_V101["xCH4"] = np.where(self.biogas_V101["mol_T"] == 0, 0, self.biogas_V101["mol_CH4"] / self.biogas_V101["mol_T"])
        self.biogas_V101["xCO2"] = np.where(self.biogas_V101["mol_T"] == 0, 0, self.biogas_V101["mol_CO2"] / self.biogas_V101["mol_T"])
        self.biogas_V101["xO2"] = np.where(self.biogas_V101["mol_T"] == 0, 0, self.biogas_V101["mol_O2"] / self.biogas_V101["mol_T"])
        self.biogas_V101["xH2S"] = np.where(self.biogas_V101["mol_T"] == 0, 0, self.biogas_V101["mol_H2S"] / self.biogas_V101["mol_T"])
        self.biogas_V101["xH2"] = np.where(self.biogas_V101["mol_T"] == 0, 0, self.biogas_V101["mol_H2"] / self.biogas_V101["mol_T"])
        self.biogas_V101["xNH3"] = np.where(self.biogas_V101["mol_T"] == 0, 0, self.biogas_V101["mol_NH3"] / self.biogas_V101["mol_T"])
        self.biogas_V101["AbsoluteHumidity"] = self.Thermo.BiogasAbsoluteHumidity(RH = self.DataPlant["rh_V101"], T = self.DataPlant["T_V101"])
        self.biogas_V101["mol_H2O"] = (self.biogas_V101["AbsoluteHumidity"] * self.biogas_V101["Vacum"])/18 
        self.biogas_V101.fillna(0, inplace=True)
        
        self.biogas_V102["mol_T"] = self.biogas_V102["mol_CH4"] + self.biogas_V102["mol_CO2"] + self.biogas_V102["mol_O2"] + self.biogas_V102["mol_H2S"] + self.biogas_V102["mol_H2"] + self.biogas_V102["mol_NH3"]
        self.biogas_V102["xCH4"] = np.where(self.biogas_V102["mol_T"] == 0, 0, self.biogas_V102["mol_CH4"] / self.biogas_V102["mol_T"])
        self.biogas_V102["xCO2"] = np.where(self.biogas_V102["mol_T"] == 0, 0, self.biogas_V102["mol_CO2"] / self.biogas_V102["mol_T"])
        self.biogas_V102["xO2"] = np.where(self.biogas_V102["mol_T"] == 0, 0, self.biogas_V102["mol_O2"] / self.biogas_V102["mol_T"])
        self.biogas_V102["xH2S"] = np.where(self.biogas_V102["mol_T"] == 0, 0, self.biogas_V102["mol_H2S"] / self.biogas_V102["mol_T"])
        self.biogas_V102["xH2"] = np.where(self.biogas_V102["mol_T"] == 0, 0, self.biogas_V102["mol_H2"] / self.biogas_V102["mol_T"])
        self.biogas_V102["xNH3"] = np.where(self.biogas_V102["mol_T"] == 0, 0, self.biogas_V102["mol_NH3"] / self.biogas_V102["mol_T"])
        self.biogas_V102["AbsoluteHumidity"] = self.Thermo.BiogasAbsoluteHumidity(RH = self.DataPlant["rh_V102"], T = self.DataPlant["T_V102"])
        self.biogas_V102["mol_H2O"] = (self.biogas_V102["AbsoluteHumidity"] * self.biogas_V102["Vacum"])/18
        self.biogas_V102.fillna(0, inplace=True)
        
        self.biogas_V107["mol_T"] = self.biogas_V107["mol_CH4"] + self.biogas_V107["mol_CO2"] + self.biogas_V107["mol_O2"] + self.biogas_V107["mol_H2S"] + self.biogas_V107["mol_H2"] + self.biogas_V107["mol_NH3"]
        self.biogas_V107["xCH4"] = np.where(self.biogas_V107["mol_T"] == 0, 0, self.biogas_V107["mol_CH4"] / self.biogas_V107["mol_T"])
        self.biogas_V107["xCO2"] = np.where(self.biogas_V107["mol_T"] == 0, 0, self.biogas_V107["mol_CO2"] / self.biogas_V107["mol_T"])
        self.biogas_V107["xO2"] = np.where(self.biogas_V107["mol_T"] == 0, 0, self.biogas_V107["mol_O2"] / self.biogas_V107["mol_T"])
        self.biogas_V107["xH2S"] = np.where(self.biogas_V107["mol_T"] == 0, 0, self.biogas_V107["mol_H2S"] / self.biogas_V107["mol_T"])
        self.biogas_V107["xH2"] = np.where(self.biogas_V107["mol_T"] == 0, 0, self.biogas_V107["mol_H2"] / self.biogas_V107["mol_T"])
        self.biogas_V107["xNH3"] = np.where(self.biogas_V107["mol_T"] == 0, 0, self.biogas_V107["mol_NH3"] / self.biogas_V107["mol_T"])
        self.biogas_V107["AbsoluteHumidity"] = self.Thermo.BiogasAbsoluteHumidity(RH = self.DataPlant["rh_V107"], T = self.DataPlant["T_V107"])
        self.biogas_V107["mol_H2O"] = (self.biogas_V107["AbsoluteHumidity"] * self.biogas_V107["Vacum"])/18
        self.biogas_V107.fillna(0, inplace=True)
        
        self.Treatment_system = pd.DataFrame() 
        self.Treatment_system["time"] = self.biogas_V101["time"]
        self.Treatment_system["nH2O_ads"] = (self.biogas_V101["mol_H2O"] + self.biogas_V102["mol_H2O"]) - self.biogas_V107["mol_H2O"]
        self.Treatment_system["nH2S_ads"] = (self.biogas_V101["mol_H2S"] + self.biogas_V102["mol_H2S"]) - self.biogas_V107["mol_H2S"]
        self.Treatment_system["nNH3_ads"] = (self.biogas_V101["mol_NH3"] + self.biogas_V102["mol_NH3"]) - self.biogas_V107["mol_NH3"]
        self.Treatment_system["xH2O"] = ((self.biogas_V101["mol_H2O"] + self.biogas_V102["mol_H2O"]) - self.biogas_V107["mol_H2O"])/(self.biogas_V101["mol_H2O"] + self.biogas_V102["mol_H2O"])
        self.Treatment_system["xH2S"] = ((self.biogas_V101["mol_H2S"] + self.biogas_V102["mol_H2S"]) - self.biogas_V107["mol_H2S"])/(self.biogas_V101["mol_H2S"] + self.biogas_V102["mol_H2S"])
        self.Treatment_system["xNH3"] = ((self.biogas_V101["mol_NH3"] + self.biogas_V102["mol_NH3"]) - self.biogas_V107["mol_NH3"])/(self.biogas_V101["mol_NH3"] + self.biogas_V102["mol_NH3"])
        self.Treatment_system["xGlobal"] = (self.Treatment_system["xH2O"] + self.Treatment_system["xH2S"] +self.Treatment_system["xNH3"])/3
        
        self.mol_NH3_ads = self.Treatment_system["nNH3_ads"].iloc[-1]
        self.mol_H2S_ads = self.Treatment_system["nH2S_ads"].iloc[-1]
        self.mol_H2O_ads = self.Treatment_system["nH2O_ads"].iloc[-1]
        self.Xglobal = self.Treatment_system["xGlobal"].iloc[-1]
        
        def Langmuir_model(t, qmax, K1, K2, W, mol_transfer):
            q = (qmax * K1 * (mol_transfer))/(1+(K1*mol_transfer))
            mol_ads_teo = W * (q**2 + K2 * t)/(1+ q * K2 * t)
            return mol_ads_teo

        def Langmuir_optimization (params, t, mol_ads_exp, W, mol_transfer):
            def objective(x):
                qmax, K1, K2 = x
                mol_ads_pred = Langmuir_model(t, qmax, K1, K2, W, mol_transfer)
                residuals = np.array(mol_ads_exp) - mol_ads_pred
                return np.sum(residuals**2)

            result = minimize(objective, [float(p) for p in params], method='Nelder-Mead')
            return result
        
        t_exp = np.array(self.Treatment_system["time"].tolist())
        Nabs_exp_H2O = np.array(self.Treatment_system["nH2O_ads"].tolist())
        mol_transfer_H2O = np.array((self.biogas_V101["mol_H2O"] + self.biogas_V102["mol_H2O"]))
        Results_H2O = Langmuir_optimization (params = (self.qmax_H2O, self.K_H2O, self.K2_H2O), t = t_exp, mol_ads_exp = Nabs_exp_H2O, W = W_silica, mol_transfer = mol_transfer_H2O)
        self.Optimized_parameters_filter_H2O = pd.DataFrame({"qmax_H2O": float(Results_H2O.x[0]),
                                                             "K_H2O": float(Results_H2O.x[1]),
                                                             "K2_H2O": float(Results_H2O.x[2])}, index=[0])
        
        
        Nabs_exp_H2S = np.array(self.Treatment_system["nH2S_ads"].tolist())
        mol_transfer_H2S = np.array((self.biogas_V101["mol_H2S"] + self.biogas_V102["mol_H2S"]).tolist())
        Results_H2S = Langmuir_optimization(params = (self.qmax_H2S, self.K_H2S, self.K2_H2S), t = t_exp, mol_ads_exp = Nabs_exp_H2S, W = W_feSO4, mol_transfer = mol_transfer_H2S)
        self.Optimized_parameters_filter_H2S = pd.DataFrame({"qmax_H2s": float(Results_H2S.x[0]),
                                                             "K_H2S": float(Results_H2S.x[1]),
                                                             "K2_H2S": float(Results_H2S.x[2])}, index=[0])