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
from scipy.integrate import odeint
from scipy.optimize import minimize
import statistics as st
import time

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
        self.ST_ini_R101_res = ST_ini_R101/100
        self.SV_ini_R101 = SV_ini_R101/100         #Initial condition for reactor
        self.SV_ini_R101_res = SV_ini_R101/100     #Iniital conditions if something wrong in the mass balance
        self.Cc_ini_R101 = Cc_R101                 #Initial Concentration to charge R101
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
            self.Csus_ini_SV_R101_res = 0
            self.Csus_ini_fixed_R101 = 0
            self.MW_inocum_ini_R101 = 18         #molecular weight of the water 
        
        else:
            self.Csus_ini_ST_R101 = ((self.ST_ini_R101)*self.rho_ini_R101)/self.MW_inocum_ini_R101     #molST/L 
            self.Csus_ini_SV_R101 = ((self.SV_ini_R101)*self.rho_ini_R101)/self.MW_inocum_ini_R101     #molSV/L
            self.Csus_ini_fixed_R101 = self.Csus_ini_ST_R101 - self.Csus_ini_SV_R101                   #molSF/L 
            self.Csus_ini_SV_R101_gl = ((self.SV_ini_R101)*self.rho_ini_R101)                          #gSV/L 
            self.Csus_ini_SV_R101_res =  self.Csus_ini_SV_R101
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
        self.ST_ini_R102_res = ST_ini_R102/100
        self.SV_ini_R102 = SV_ini_R102/100         #Initial condition for reactor
        self.SV_ini_R102_res = SV_ini_R102/100
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
        self.K_ini_Arr_R101 = 10
        self.K_ini_ADM1_R101 = 0.0000001
        self.Ea_ini_R101 = 100000
        self.K_ini_Arr_R102 = 10
        self.K_ini_ADM1_R102 = 0.0000001
        self.Ea_ini_R102 = 100000
        
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

        #global time initial
        self.global_time = 0
    
    def getData(self):
        attempts = 1
        while attempts <= 5:
            try:
                self.query1 = self.influxDB.QueryCreator(measurement="Planta_Biogas", device="interfaz", type=5)
                self.Datainterfaz = pd.concat(self.influxDB.InfluxDBreader(query = self.query1), ignore_index=True)
                # self.Datainterfaz = self.influxDB.InfluxDBreader(query = self.query1)
                self.Datainterfaz.set_index("_field", inplace = True)
                self.Operation_mode = self.Datainterfaz["_value"]["ciclo"]
                self.Operation_mode = self.Operation_mode.iloc[-1]
                break
            except:
                attempts += 1

        attempts = 1
        while attempts <= 5:
            try:
                self.query2 = self.influxDB.QueryCreator(measurement="Planta_Biogas", train_time=str(self.t_train), type=4)
                print("acquiring Data from sensors...")
                # DataPlant = pd.concat(self.influxDB.InfluxDBreader(query = self.query2), ignore_index=True)
                DataPlant = self.influxDB.InfluxDBreader(query = self.query2)
                print("Instrumentation Data acquired...")
                DataPlant.set_index("_field", inplace = True)
                self.DataPlanti = DataPlant
                break
            except:
                attempts += 1
        
        #Get estimation Data
        attempts = 1
        while attempts <= 5:
            try:
                self.query3 = self.influxDB.QueryCreator(measurement="Planta_Biogas", train_time=str(self.t_train), type=8)
                print("acquiring Data from estimations...")
                Interfaz = self.influxDB.InfluxDBreader(query = self.query3)
                print("Estimation Data acquired...")
                Interfaz.set_index("_field", inplace = True)
                self.interfaz = Interfaz
                break
            except:
                attempts += 1
        
        #Genral time to train
        time_date = DataPlant["_time"]["PT-103"]
        time_date = pd.to_datetime(time_date, format = "mixed")
        
        #------Extract Series from Main DataFrame (influx) (all operation modes has these variables)
        
        #V101
        Pacum_V101 = Interfaz.loc["PAcumV101", ["_time", "_value"]]
        Vacum_V101 = Interfaz.loc["Volumen_bioV101", ["_time", "_value"]]
        self.Energia_jouleV101 = Interfaz.loc["Energia_jouleV101", ["_time", "_value"]]
        P_V101 = DataPlant.loc["PT-103", ["_time", "_value"]]
        T_V101 = DataPlant.loc["TT-103", ["_time", "_value"]]
        rh_V101 = DataPlant.loc["AT-103B", ["_time", "_value"]]
        xCH4_V101 = DataPlant.loc["AT-103A-CH4", ["_time", "_value"]]
        xCO2_V101 = DataPlant.loc["AT-103A-CO2", ["_time", "_value"]]
        xO2_V101 = DataPlant.loc["AT-103A-O2", ["_time", "_value"]]
        xH2S_V101 = DataPlant.loc["AT-103A-H2S", ["_time", "_value"]]
        xH2_V101 = DataPlant.loc["AT-103A-H2", ["_time", "_value"]]
        
        #P104
        P104 = DataPlant.loc["FE-104", ["_time", "_value"]]

        #Historic for feeding
        #substrate number
        # MNS = Interfaz.loc["MNS", ["_time", "_value"]]
        # MNS["_value"] = MNS["_value"].replace(0,np.nan)
        # MNS['_value'] = MNS['_value'].bfill()
        # ## Proportions
        # # substrate 1
        # MP1 = Interfaz.loc["MP1", ["_time", "_value"]]
        # MP1["_value"] = MP1["_value"].replace(0,np.nan)
        # MP1["_value"] = MP1["_value"].bfill()
        # # substrate 2
        # MP2 = Interfaz.loc["MP2", ["_time", "_value"]]
        # MP2["_value"] = MP2["_value"].replace(0,np.nan)
        # MP2["_value"] = MP2["_value"].bfill()
        # # substrate 3
        # MP3 = Interfaz.loc["MP3", ["_time", "_value"]]
        # MP3["_value"] = MP3["_value"].replace(0,np.nan)
        # MP3["_value"] = MP3["_value"].bfill()
        # # substrate 4
        # MP4 = Interfaz.loc["MP4", ["_time", "_value"]]
        # MP4["_value"] = MP4["_value"].replace(0,np.nan)
        # MP4["_value"] = MP4["_value"].bfill()
        # ## densitys
        # # substrate 1
        # Md1 = Interfaz.loc["Md1", ["_time", "_value"]]
        # Md1["_value"] = Md1["_value"].replace(0,np.nan)
        # Md1["_value"] = Md1["_value"].bfill()
        # # substrate 2
        # Md2 = Interfaz.loc["Md2", ["_time", "_value"]]
        # Md2["_value"] = Md2["_value"].replace(0,np.nan)
        # Md2["_value"] = Md2["_value"].bfill()
        # # substrate 3
        # Md3 = Interfaz.loc["Md3", ["_time", "_value"]]
        # Md3["_value"] = Md3["_value"].replace(0,np.nan)
        # Md3["_value"] = Md3["_value"].bfill()
        # # substrate 4
        # Md4 = Interfaz.loc["Md4", ["_time", "_value"]]
        # Md4["_value"] = Md4["_value"].replace(0,np.nan)
        # Md4["_value"] = Md4["_value"].bfill()
        # #Total solids (If there are changes in substrate feeding during the test it is possible consult the historic with the query)

        #TK100
        self.Mix_Velocity_TK100 = DataPlant.loc["SE-107",["_time", "_value"]]

        #R101
        self.Mix_Velocity_R101 = DataPlant.loc["SE-108", ["_time", "_value"]]
        pH_R101 = DataPlant.loc["AT-101", ["_time", "_value"]]
        L_R101 = DataPlant.loc["LT-101", ["_time", "_value"]]       #L: level
        P_R101 = DataPlant.loc["PT-101", ["_time", "_value"]]
        T1_R101 =  DataPlant.loc["TE-101A", ["_time", "_value"]]
        T2_R101 = DataPlant.loc["TE-101B", ["_time", "_value"]]
        Tprom_R101 = DataPlant.loc["TE-R101", ["_time", "_value"]]


        #V102
        try:
            Pacum_V102 = Interfaz.loc["PAcumV102", ["_time", "_value"]]
        except KeyError:
            Pacum_V102 = Pacum_V101.copy()
            Pacum_V102["_value"] = 0
        try:
            Vacum_V102 = Interfaz.loc["Volumen_bioV102", ["_time", "_value"]]
        except KeyError:
             Vacum_V102 = Vacum_V101.copy()
             Vacum_V102["_value"] = 0
        try:
            self.Energia_jouleV102 = Interfaz.loc["Energia_jouleV102", ["_time", "_value"]]
        except KeyError:
            self.Energia_jouleV102 = 0
        P_V102 = DataPlant.loc["PT-104", ["_time", "_value"]]
        T_V102 = DataPlant.loc["TT-104", ["_time", "_value"]]
        rh_V102 = DataPlant.loc["AT-103B", ["_time", "_value"]]        #rh: relative humidity
        xCH4_V102 = DataPlant.loc["AT-104A-CH4", ["_time", "_value"]]
        xCO2_V102 = DataPlant.loc["AT-104A-CO2", ["_time", "_value"]]
        xO2_V102 = DataPlant.loc["AT-104A-O2", ["_time", "_value"]]
        xH2S_V102 = DataPlant.loc["AT-104A-H2S", ["_time", "_value"]]
        xH2_V102 = DataPlant.loc["AT-104A-H2", ["_time", "_value"]]
        
        #V107
        Pacum_V107 = Interfaz.loc["PAcumV107", ["_time", "_value"]]
        Vacum_V107 = Interfaz.loc["Volumen_bioV107", ["_time", "_value"]]
        self.Energia_jouleV107 = Interfaz.loc["Energia_jouleV107", ["_time", "_value"]]
        P_V107 = DataPlant.loc["PT-105", ["_time", "_value"]]
        T_V107 = DataPlant.loc["TT-105", ["_time", "_value"]]
        rh_V107 = DataPlant.loc["AT-105B", ["_time", "_value"]]        #rh: relative humidity
        xCH4_V107 = DataPlant.loc["AT-105A-CH4", ["_time", "_value"]]
        xCO2_V107 = DataPlant.loc["AT-105A-CO2", ["_time", "_value"]]
        xO2_V107 = DataPlant.loc["AT-105A-O2", ["_time", "_value"]]
        xH2S_V107 = DataPlant.loc["AT-105A-H2S", ["_time", "_value"]]
        xH2_V107 = DataPlant.loc["AT-105A-H2", ["_time", "_value"]]

        #Normalice asynchronous data
        def asynchronousdata(timeSeries, AsyncSeries):
            df1 = AsyncSeries["_time"]
            df1 = pd.to_datetime(df1, format="mixed")
            merge_df = pd.concat([timeSeries, df1], ignore_index=True)
            merge_df = merge_df.sort_values().reset_index(drop=True)
            merge_df = pd.merge(merge_df, AsyncSeries, on="_time", how="left")
            merge_df = merge_df.fillna(0)
            return merge_df
        
        #Two pumps
        def concatAsync(series1, series2, name1, name2):
            all_times = pd.concat([series1["_time"], series2["_time"]], ignore_index=True)
            all_times = all_times.drop_duplicates().sort_values().reset_index(drop=True)
            time_df = pd.DataFrame({"_time": all_times})
            merged = pd.merge(time_df, series1, on="_time", how="left")
            merged = pd.merge(merged, series2, on="_time", how="left")
            merged = merged.rename(columns={"_value_x": name1, "_value_y":name2})
            merged = merged.ffill()
            return merged
        
        #Three pumps
        def concatAsync2(series1, series2, series3, name1, name2, name3):
            all_times = pd.concat([series1["_time"], series2["_time"], series3["_time"]], ignore_index=True)
            all_times = all_times.drop_duplicates().sort_values().reset_index(drop=True)
            time_df = pd.DataFrame({"_time": all_times})

            # Rename _value columns before merging
            series1_renamed = series1.rename(columns={"_value": name1})
            series2_renamed = series2.rename(columns={"_value": name2})
            series3_renamed = series3.rename(columns={"_value": name3})

            # Merge all series on _time
            merged = pd.merge(time_df, series1_renamed[["_time", name1]], on="_time", how="left")
            merged = pd.merge(merged, series2_renamed[["_time", name2]], on="_time", how="left")
            merged = pd.merge(merged, series3_renamed[["_time", name3]], on="_time", how="left")

            # Fill missing values
            merged = merged.ffill()

            return merged
        
        #funtion to align Data series
        def alignDimension (timeSeries, AsynSeries):
            timeSeries = timeSeries.sort_values()
            AsynSeries["_time"] = pd.to_datetime(AsynSeries["_time"], format = "mixed")
            AsynSeries = AsynSeries.sort_values("_time")
            merge_df = pd.merge_asof(timeSeries, AsynSeries, on = "_time", direction = 'backward')
            #merge_df["_value"] = replace_outliers_with_interpolation(merge_df["_value"])
            merge_df = merge_df["_value"]
            merge_df = merge_df.ffill()
            return merge_df

        #function to make treatment of outliers
        def replace_outliers_with_interpolation(series):
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            # Replace outliers with NaN
            series_out = series.copy()
            series_out[(series < lower_bound) | (series > upper_bound)] = pd.NA
            # Interpolate linearly
            series_out = series_out.interpolate(method='linear')
            return series_out
        
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
            
        #DataFrame Generation for operation Mode 1
        if self.Operation_mode == 1:
            #Synchronyze Data
            P104 = asynchronousdata(time_date, P104)
            #Defining time
            time_definitive = Pumps["_time"]
            normal_time = normaliceTime(time_definitive)
            #V101
            Pacum_V101 = alignDimension(time_definitive, Pacum_V101)
            Vacum_V101 = alignDimension(time_definitive, Vacum_V101)
            P_V101 = alignDimension(time_definitive, P_V101)
            T_V101 = alignDimension(time_definitive, T_V101)
            rh_V101 = alignDimension(time_definitive, rh_V101)
            xCH4_V101 = alignDimension(time_definitive, xCH4_V101)
            xCO2_V101 = alignDimension(time_definitive, xCO2_V101)
            xO2_V101 = alignDimension(time_definitive, xO2_V101)
            xH2S_V101 = alignDimension(time_definitive, xH2S_V101)
            xH2_V101 = alignDimension(time_definitive, xH2_V101)
            #R101
            pH_R101 = alignDimension(time_definitive, pH_R101)
            L_R101 = alignDimension(time_definitive, L_R101)       #L: level
            P_R101 = alignDimension(time_definitive, P_R101)
            T1_R101 =  alignDimension(time_definitive, T1_R101)
            T2_R101 = alignDimension(time_definitive, T2_R101)
            Tprom_R101 = alignDimension(time_definitive, Tprom_R101)
            #V102
            try:
                Pacum_V102 = alignDimension(time_definitive, Pacum_V102)
            except:
                Pacum_V102 = Pacum_V102["_value"]
            try: 
                Vacum_V102 = alignDimension(time_definitive, Vacum_V102)
            except:
                Vacum_V102 = Vacum_V102["_value"]
            P_V102 = alignDimension(time_definitive, P_V102)
            T_V102 = alignDimension(time_definitive, T_V102)
            rh_V102 = alignDimension(time_definitive, rh_V102)
            xCH4_V102 = alignDimension(time_definitive, xCH4_V102)
            xCO2_V102 = alignDimension(time_definitive, xCO2_V102)
            xO2_V102 = alignDimension(time_definitive, xO2_V102)
            xH2S_V102 = alignDimension(time_definitive, xH2S_V102)
            xH2_V102 = alignDimension(time_definitive, xH2_V102)
            #V107
            Pacum_V107 = alignDimension(time_definitive, Pacum_V107)
            Vacum_V107 = alignDimension(time_definitive, Vacum_V107)
            P_V107 = alignDimension(time_definitive, P_V107)
            T_V107 = alignDimension(time_definitive, T_V107)
            rh_V107 = alignDimension(time_definitive, rh_V107)
            xCH4_V107 = alignDimension(time_definitive, xCH4_V107)
            xCO2_V107 = alignDimension(time_definitive, xCO2_V107)
            xO2_V107 = alignDimension(time_definitive, xO2_V107)
            xH2S_V107 = alignDimension(time_definitive, xH2S_V107)
            xH2_V107 = alignDimension(time_definitive, xH2_V107)
            #feeding data
            # MNS = alignDimension(time_definitive, MNS)

                        
            self.DataPlant = pd.DataFrame({"time": time_definitive,
                                           "normal_time": normal_time,
                                           "P104": Pumps["P104"],
                                           "Pacum_V101": Pacum_V101,
                                           "Vacum_V101": Vacum_V101,
                                           "P_V101": P_V101,
                                           "T_V101": T_V101,
                                           "rh_V101": rh_V101,
                                           "xCH4_V101": xCH4_V101,
                                           "xCO2_V101": xCO2_V101,
                                           "xO2_V101": xO2_V101,
                                           "xH2S_V101": xH2S_V101,
                                           "xH2_V101": xH2_V101,
                                           "pH_R101": pH_R101,
                                           "L_R101": L_R101,
                                           "P_R101": P_R101,
                                           "T1_R101": T1_R101,
                                           "T2_R101": T2_R101,
                                           "Tprom_R101": Tprom_R101,
                                           "Pacum_V102": Pacum_V102,
                                           "Vacum_V102": Vacum_V102,
                                           "P_V102": P_V102,
                                           "T_V102": T_V102,
                                           "rh_V102": rh_V102,
                                           "xCH4_V102": xCH4_V102,
                                           "xCO2_V102": xCO2_V102,
                                           "xO2_V102": xO2_V102,
                                           "xH2S_V102": xH2S_V102,
                                           "xH2_V102": xH2_V102,
                                           "Pacum_V107": Pacum_V107,
                                           "Vacum_V107": Vacum_V107,
                                           "P_V107": P_V107,
                                           "T_V107": T_V107,
                                           "rh_V107": rh_V107,
                                           "xCH4_V107": xCH4_V107,
                                           "xCO2_V107": xCO2_V107,
                                           "xO2_V107": xO2_V107,
                                           "xH2S_V107": xH2S_V107,
                                           "xH2_V107": xH2_V107
                                           })
            
        
        #DataFrame Generation for operation Mode 2
        elif self.Operation_mode == 2:
            #Adding varaibles for this operation mode
            P101 = DataPlant.loc["P-101", ["_time", "_value"]]
            #Synchronyze Data
            P104 = asynchronousdata(time_date, P104)
            P101 = asynchronousdata(time_date, P101)
            Pumps = concatAsync(P104, P101, "P104", "P101")
            #Defining time
            time_definitive = Pumps["_time"]
            normal_time = normaliceTime(time_definitive)
            #V101
            Pacum_V101 = alignDimension(time_definitive, Pacum_V101)
            Vacum_V101 = alignDimension(time_definitive, Vacum_V101)
            P_V101 = alignDimension(time_definitive, P_V101)
            T_V101 = alignDimension(time_definitive, T_V101)
            rh_V101 = alignDimension(time_definitive, rh_V101)
            xCH4_V101 = alignDimension(time_definitive, xCH4_V101)
            xCO2_V101 = alignDimension(time_definitive, xCO2_V101)
            xO2_V101 = alignDimension(time_definitive, xO2_V101)
            xH2S_V101 = alignDimension(time_definitive, xH2S_V101)
            xH2_V101 = alignDimension(time_definitive, xH2_V101)
            #R101
            pH_R101 = alignDimension(time_definitive, pH_R101)
            L_R101 = alignDimension(time_definitive, L_R101)       #L: level
            P_R101 = alignDimension(time_definitive, P_R101)
            T1_R101 =  alignDimension(time_definitive, T1_R101)
            T2_R101 = alignDimension(time_definitive, T2_R101)
            Tprom_R101 = alignDimension(time_definitive, Tprom_R101)
            #V102
            try:
                Pacum_V102 = alignDimension(time_definitive, Pacum_V102)
            except:
                Pacum_V102 = Pacum_V102["_value"]
            try: 
                Vacum_V102 = alignDimension(time_definitive, Vacum_V102)
            except:
                Vacum_V102 = Vacum_V102["_value"]
            P_V102 = alignDimension(time_definitive, P_V102)
            T_V102 = alignDimension(time_definitive, T_V102)
            rh_V102 = alignDimension(time_definitive, rh_V102)
            xCH4_V102 = alignDimension(time_definitive, xCH4_V102)
            xCO2_V102 = alignDimension(time_definitive, xCO2_V102)
            xO2_V102 = alignDimension(time_definitive, xO2_V102)
            xH2S_V102 = alignDimension(time_definitive, xH2S_V102)
            xH2_V102 = alignDimension(time_definitive, xH2_V102)
            #V107
            Pacum_V107 = alignDimension(time_definitive, Pacum_V107)
            Vacum_V107 = alignDimension(time_definitive, Vacum_V107)
            P_V107 = alignDimension(time_definitive, P_V107)
            T_V107 = alignDimension(time_definitive, T_V107)
            rh_V107 = alignDimension(time_definitive, rh_V107)
            xCH4_V107 = alignDimension(time_definitive, xCH4_V107)
            xCO2_V107 = alignDimension(time_definitive, xCO2_V107)
            xO2_V107 = alignDimension(time_definitive, xO2_V107)
            xH2S_V107 = alignDimension(time_definitive, xH2S_V107)
            xH2_V107 = alignDimension(time_definitive, xH2_V107)
            #feeding data
            # MNS = alignDimension(time_definitive, MNS)

                        
            self.DataPlant = pd.DataFrame({"time": time_definitive,
                                           "normal_time": normal_time,
                                           "P104": Pumps["P104"],
                                           "P101": Pumps["P101"],
                                           "Pacum_V101": Pacum_V101,
                                           "Vacum_V101": Vacum_V101,
                                           "P_V101": P_V101,
                                           "T_V101": T_V101,
                                           "rh_V101": rh_V101,
                                           "xCH4_V101": xCH4_V101,
                                           "xCO2_V101": xCO2_V101,
                                           "xO2_V101": xO2_V101,
                                           "xH2S_V101": xH2S_V101,
                                           "xH2_V101": xH2_V101,
                                           "pH_R101": pH_R101,
                                           "L_R101": L_R101,
                                           "P_R101": P_R101,
                                           "T1_R101": T1_R101,
                                           "T2_R101": T2_R101,
                                           "Tprom_R101": Tprom_R101,
                                           "Pacum_V102": Pacum_V102,
                                           "Vacum_V102": Vacum_V102,
                                           "P_V102": P_V102,
                                           "T_V102": T_V102,
                                           "rh_V102": rh_V102,
                                           "xCH4_V102": xCH4_V102,
                                           "xCO2_V102": xCO2_V102,
                                           "xO2_V102": xO2_V102,
                                           "xH2S_V102": xH2S_V102,
                                           "xH2_V102": xH2_V102,
                                           "Pacum_V107": Pacum_V107,
                                           "Vacum_V107": Vacum_V107,
                                           "P_V107": P_V107,
                                           "T_V107": T_V107,
                                           "rh_V107": rh_V107,
                                           "xCH4_V107": xCH4_V107,
                                           "xCO2_V107": xCO2_V107,
                                           "xO2_V107": xO2_V107,
                                           "xH2S_V107": xH2S_V107,
                                           "xH2_V107": xH2_V107
                                           })
            
        elif self.Operation_mode == 3:
            #Adding varaibles for this operation mode
            # Pump 101
            P101 = DataPlant.loc["P-101", ["_time", "_value"]]
            #R102
            pH_R102 = DataPlant.loc["AT-102", ["_time", "_value"]]
            L_R102 = DataPlant.loc["LT-102", ["_time", "_value"]]       #L: level
            P_R102 = DataPlant.loc["PT-102", ["_time", "_value"]]
            T1_R102 =  DataPlant.loc["TE-102A", ["_time", "_value"]]
            T2_R102 = DataPlant.loc["TE-102B", ["_time", "_value"]]
            Tprom_R102 = DataPlant.loc["TE-R102", ["_time", "_value"]]
            
            #Synchronyze Data
            P104 = asynchronousdata(time_date, P104)
            P101 = asynchronousdata(time_date, P101)
            Pumps = concatAsync(P104, P101, "P104", "P101")
            #Defining time
            time_definitive = Pumps["_time"]
            normal_time = normaliceTime(time_definitive)
            #V101
            Pacum_V101 = alignDimension(time_definitive, Pacum_V101)
            Vacum_V101 = alignDimension(time_definitive, Vacum_V101)
            P_V101 = alignDimension(time_definitive, P_V101)
            T_V101 = alignDimension(time_definitive, T_V101)
            rh_V101 = alignDimension(time_definitive, rh_V101)
            xCH4_V101 = alignDimension(time_definitive, xCH4_V101)
            xCO2_V101 = alignDimension(time_definitive, xCO2_V101)
            xO2_V101 = alignDimension(time_definitive, xO2_V101)
            xH2S_V101 = alignDimension(time_definitive, xH2S_V101)
            xH2_V101 = alignDimension(time_definitive, xH2_V101)
            #V102
            try:
                Pacum_V102 = alignDimension(time_definitive, Pacum_V102)
            except:
                Pacum_V102 = Pacum_V102["_value"]
            try: 
                Vacum_V102 = alignDimension(time_definitive, Vacum_V102)
            except:
                Vacum_V102 = Vacum_V102["_value"]
            P_V102 = alignDimension(time_definitive, P_V102)
            T_V102 = alignDimension(time_definitive, T_V102)
            rh_V102 = alignDimension(time_definitive, rh_V102)
            xCH4_V102 = alignDimension(time_definitive, xCH4_V102)
            xCO2_V102 = alignDimension(time_definitive, xCO2_V102)
            xO2_V102 = alignDimension(time_definitive, xO2_V102)
            xH2S_V102 = alignDimension(time_definitive, xH2S_V102)
            xH2_V102 = alignDimension(time_definitive, xH2_V102)
            #R101
            pH_R101 = alignDimension(time_definitive, pH_R101)
            L_R101 = alignDimension(time_definitive, L_R101)       #L: level
            P_R101 = alignDimension(time_definitive, P_R101)
            T1_R101 =  alignDimension(time_definitive, T1_R101)
            T2_R101 = alignDimension(time_definitive, T2_R101)
            Tprom_R101 = alignDimension(time_definitive, Tprom_R101)
            #R102
            pH_R102 = alignDimension(time_definitive, pH_R102)
            L_R102 = alignDimension(time_definitive, L_R102)       #L: level
            P_R102 = alignDimension(time_definitive, P_R102)
            T1_R102 =  alignDimension(time_definitive, T1_R102)
            T2_R102 = alignDimension(time_definitive, T2_R102)
            Tprom_R102 = alignDimension(time_definitive, Tprom_R102)
            #V107
            Pacum_V107 = alignDimension(time_definitive, Pacum_V107)
            Vacum_V107 = alignDimension(time_definitive, Vacum_V107)
            P_V107 = alignDimension(time_definitive, P_V107)
            T_V107 = alignDimension(time_definitive, T_V107)
            rh_V107 = alignDimension(time_definitive, rh_V107)
            xCH4_V107 = alignDimension(time_definitive, xCH4_V107)
            xCO2_V107 = alignDimension(time_definitive, xCO2_V107)
            xO2_V107 = alignDimension(time_definitive, xO2_V107)
            xH2S_V107 = alignDimension(time_definitive, xH2S_V107)
            xH2_V107 = alignDimension(time_definitive, xH2_V107)
            #feeding data
            # MNS = alignDimension(time_definitive, MNS)
           

            self.DataPlant = pd.DataFrame({"time": time_definitive,
                                           "normal_time": normal_time,
                                           "P104": Pumps["P104"],
                                           "P101": Pumps["P101"],
                                           "Pacum_V101": Pacum_V101,
                                           "Vacum_V101": Vacum_V101,
                                           "P_V101": P_V101,
                                           "T_V101": T_V101,
                                           "rh_V101": rh_V101,
                                           "xCH4_V101": xCH4_V101,
                                           "xCO2_V101": xCO2_V101,
                                           "xO2_V101": xO2_V101,
                                           "xH2S_V101": xH2S_V101,
                                           "xH2_V101": xH2_V101,
                                           "pH_R101": pH_R101,
                                           "L_R101": L_R101,
                                           "P_R101": P_R101,
                                           "T1_R101": T1_R101,
                                           "T2_R101": T2_R101,
                                           "Tprom_R101": Tprom_R101,
                                           "pH_R102": pH_R102,
                                           "L_R102": L_R102,
                                           "P_R102": P_R102,
                                           "T1_R102": T1_R102,
                                           "T2_R102": T2_R102,
                                           "Tprom_R102": Tprom_R102,
                                           "Pacum_V102": Pacum_V102,
                                           "Vacum_V102": Vacum_V102,
                                           "P_V102": P_V102,
                                           "T_V102": T_V102,
                                           "rh_V102": rh_V102,
                                           "xCH4_V102": xCH4_V102,
                                           "xCO2_V102": xCO2_V102,
                                           "xO2_V102": xO2_V102,
                                           "xH2S_V102": xH2S_V102,
                                           "xH2_V102": xH2_V102,
                                           "Pacum_V107": Pacum_V107,
                                           "Vacum_V107": Vacum_V107,
                                           "P_V107": P_V107,
                                           "T_V107": T_V107,
                                           "rh_V107": rh_V107,
                                           "xCH4_V107": xCH4_V107,
                                           "xCO2_V107": xCO2_V107,
                                           "xO2_V107": xO2_V107,
                                           "xH2S_V107": xH2S_V107,
                                           "xH2_V107": xH2_V107
                                           })
        
        elif self.Operation_mode in [4, 5]:
            #Adding varaibles for this operation mode
            # Pump 101
            P101 = DataPlant.loc["P-101", ["_time", "_value"]]
            # Pump 102
            P102 = DataPlant.loc["P-102", ["_time", "_value"]]
            #R102
            pH_R102 = DataPlant.loc["AT-102", ["_time", "_value"]]
            L_R102 = DataPlant.loc["LT-102", ["_time", "_value"]]       #L: level
            P_R102 = DataPlant.loc["PT-102", ["_time", "_value"]]
            T1_R102 =  DataPlant.loc["TE-102A", ["_time", "_value"]]
            T2_R102 = DataPlant.loc["TE-102B", ["_time", "_value"]]
            Tprom_R102 = DataPlant.loc["TE-R102", ["_time", "_value"]]

            #Synchronyze Data
            P104 = asynchronousdata(time_date, P104)
            P101 = asynchronousdata(time_date, P101)
            P102 = asynchronousdata(time_date, P102)
            Pumps = concatAsync2(P104, P101, P102, "P104", "P101", "P102")
            #Defining time
            time_definitive = Pumps["_time"]
            normal_time = normaliceTime(time_definitive)
            #V101
            Pacum_V101 = alignDimension(time_definitive, Pacum_V101)
            Vacum_V101 = alignDimension(time_definitive, Vacum_V101)
            P_V101 = alignDimension(time_definitive, P_V101)
            T_V101 = alignDimension(time_definitive, T_V101)
            rh_V101 = alignDimension(time_definitive, rh_V101)
            xCH4_V101 = alignDimension(time_definitive, xCH4_V101)
            xCO2_V101 = alignDimension(time_definitive, xCO2_V101)
            xO2_V101 = alignDimension(time_definitive, xO2_V101)
            xH2S_V101 = alignDimension(time_definitive, xH2S_V101)
            xH2_V101 = alignDimension(time_definitive, xH2_V101)
            #V102
            Pacum_V102 = alignDimension(time_definitive, Pacum_V102)
            Vacum_V102 = alignDimension(time_definitive, Vacum_V102)
            P_V102 = alignDimension(time_definitive, P_V102)
            T_V102 = alignDimension(time_definitive, T_V102)
            rh_V102 = alignDimension(time_definitive, rh_V102)
            xCH4_V102 = alignDimension(time_definitive, xCH4_V102)
            xCO2_V102 = alignDimension(time_definitive, xCO2_V102)
            xO2_V102 = alignDimension(time_definitive, xO2_V102)
            xH2S_V102 = alignDimension(time_definitive, xH2S_V102)
            xH2_V102 = alignDimension(time_definitive, xH2_V102)
            #R101
            pH_R101 = alignDimension(time_definitive, pH_R101)
            L_R101 = alignDimension(time_definitive, L_R101)       #L: level
            P_R101 = alignDimension(time_definitive, P_R101)
            T1_R101 =  alignDimension(time_definitive, T1_R101)
            T2_R101 = alignDimension(time_definitive, T2_R101)
            Tprom_R101 = alignDimension(time_definitive, Tprom_R101)
            #R102
            pH_R102 = alignDimension(time_definitive, pH_R102)
            L_R102 = alignDimension(time_definitive, L_R102)       #L: level
            P_R102 = alignDimension(time_definitive, P_R102)
            T1_R102 =  alignDimension(time_definitive, T1_R102)
            T2_R102 = alignDimension(time_definitive, T2_R102)
            Tprom_R102 = alignDimension(time_definitive, Tprom_R102)
            #V107
            Pacum_V107 = alignDimension(time_definitive, Pacum_V107)
            Vacum_V107 = alignDimension(time_definitive, Vacum_V107)
            P_V107 = alignDimension(time_definitive, P_V107)
            T_V107 = alignDimension(time_definitive, T_V107)
            rh_V107 = alignDimension(time_definitive, rh_V107)
            xCH4_V107 = alignDimension(time_definitive, xCH4_V107)
            xCO2_V107 = alignDimension(time_definitive, xCO2_V107)
            xO2_V107 = alignDimension(time_definitive, xO2_V107)
            xH2S_V107 = alignDimension(time_definitive, xH2S_V107)
            xH2_V107 = alignDimension(time_definitive, xH2_V107)
            #feeding data
            # MNS = alignDimension(time_definitive, MNS)
            # print(MNS)

            self.DataPlant = pd.DataFrame({"time": time_definitive,
                                        "normal_time": normal_time,
                                        "P104": Pumps["P104"],
                                        "P101": Pumps["P101"],
                                        "P102": Pumps["P102"],
                                        "Pacum_V101": Pacum_V101,
                                        "Vacum_V101": Vacum_V101,
                                        "P_V101": P_V101,
                                        "T_V101": T_V101,
                                        "rh_V101": rh_V101,
                                        "xCH4_V101": xCH4_V101,
                                        "xCO2_V101": xCO2_V101,
                                        "xO2_V101": xO2_V101,
                                        "xH2S_V101": xH2S_V101,
                                        "xH2_V101": xH2_V101,
                                        "pH_R101": pH_R101,
                                        "L_R101": L_R101,
                                        "P_R101": P_R101,
                                        "T1_R101": T1_R101,
                                        "T2_R101": T2_R101,
                                        "Tprom_R101": Tprom_R101,
                                        "pH_R102": pH_R102,
                                        "L_R102": L_R102,
                                        "P_R102": P_R102,
                                        "T1_R102": T1_R102,
                                        "T2_R102": T2_R102,
                                        "Tprom_R102": Tprom_R102,
                                        "Pacum_V102": Pacum_V102,
                                        "Vacum_V102": Vacum_V102,
                                        "P_V102": P_V102,
                                        "T_V102": T_V102,
                                        "rh_V102": rh_V102,
                                        "xCH4_V102": xCH4_V102,
                                        "xCO2_V102": xCO2_V102,
                                        "xO2_V102": xO2_V102,
                                        "xH2S_V102": xH2S_V102,
                                        "xH2_V102": xH2_V102,
                                        "Pacum_V107": Pacum_V107,
                                        "Vacum_V107": Vacum_V107,
                                        "P_V107": P_V107,
                                        "T_V107": T_V107,
                                        "rh_V107": rh_V107,
                                        "xCH4_V107": xCH4_V107,
                                        "xCO2_V107": xCO2_V107,
                                        "xO2_V107": xO2_V107,
                                        "xH2S_V107": xH2S_V107,
                                        "xH2_V107": xH2_V107
                                        })

        #Normalice Data from biogas analyzer
        #Correction of concentration
        #Methane V101
        if (self.DataPlant["xCH4_V101"] != 0).any():
            self.DataPlant["xCH4_V101_filled"] = self.DataPlant["xCH4_V101"].replace(0, np.nan)
            self.DataPlant["xCH4_V101_filled"] = self.DataPlant["xCH4_V101_filled"].ffill()
            self.DataPlant['xCH4_V101_filled'] = self.DataPlant.apply(lambda row: row['xCH4_V101_filled'] if row['xCH4_V101'] == 0 else row['xCH4_V101'], axis=1)
            self.DataPlant['xCH4_V101_filled'] = self.DataPlant['xCH4_V101_filled'].fillna(0).astype(float)
            self.DataPlant['xCH4_V101_filled'] = self.DataPlant['xCH4_V101_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xCH4_V101_filled"] = self.DataPlant["xCH4_V101_filled"].mask(self.DataPlant["xCH4_V101_filled"] > 100, np.nan)
            self.DataPlant["xCH4_V101_filled"] = self.DataPlant["xCH4_V101_filled"].ffill()
            mean_value_xCH4_V101 = self.DataPlant["xCH4_V101_filled"]#.mean()
            self.DataPlant["xCH4_V101_filled"] = mean_value_xCH4_V101
        else:
            self.DataPlant["xCH4_V101_filled"] = self.DataPlant["xCH4_V101"]
        
        #Methane V102
        if (self.DataPlant["xCH4_V102"] != 0).any():
            self.DataPlant["xCH4_V102_filled"] = self.DataPlant["xCH4_V102"].replace(0, np.nan)
            self.DataPlant["xCH4_V102_filled"] = self.DataPlant["xCH4_V102_filled"].ffill()
            self.DataPlant['xCH4_V102_filled'] = self.DataPlant.apply(lambda row: row['xCH4_V102_filled'] if row['xCH4_V102'] == 0 else row['xCH4_V102'], axis=1)
            self.DataPlant['xCH4_V102_filled'] = self.DataPlant['xCH4_V102_filled'].fillna(0).astype(float)
            self.DataPlant['xCH4_V102_filled'] = self.DataPlant['xCH4_V102_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xCH4_V102_filled"] = self.DataPlant["xCH4_V102_filled"].mask(self.DataPlant["xCH4_V102_filled"] > 100, np.nan)
            self.DataPlant["xCH4_V102_filled"] = self.DataPlant["xCH4_V102_filled"].ffill()
            mean_value_xCH4_V102 = self.DataPlant["xCH4_V102_filled"]#.mean()
            self.DataPlant["xCH4_V102_filled"] = mean_value_xCH4_V102
        else:
            self.DataPlant["xCH4_V102_filled"] = self.DataPlant["xCH4_V102"]
        
        #Methane V107
        if (self.DataPlant["xCH4_V107"] != 0).any():
            self.DataPlant["xCH4_V107_filled"] = self.DataPlant["xCH4_V107"].replace(0, np.nan)
            self.DataPlant["xCH4_V107_filled"] = self.DataPlant["xCH4_V107_filled"].ffill()
            self.DataPlant['xCH4_V107_filled'] = self.DataPlant.apply(lambda row: row['xCH4_V107_filled'] if row['xCH4_V107'] == 0 else row['xCH4_V107'], axis=1)
            self.DataPlant['xCH4_V107_filled'] = self.DataPlant['xCH4_V107_filled'].fillna(0).astype(float)
            self.DataPlant['xCH4_V107_filled'] = self.DataPlant['xCH4_V107_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xCH4_V107_filled"] = self.DataPlant["xCH4_V107_filled"].mask(self.DataPlant["xCH4_V107_filled"] > 100, np.nan)
            self.DataPlant["xCH4_V107_filled"] = self.DataPlant["xCH4_V107_filled"].ffill()
            mean_value_xCH4_V107 = self.DataPlant["xCH4_V107_filled"]#.mean()
            self.DataPlant["xCH4_V107_filled"] = mean_value_xCH4_V107
        else:
            self.DataPlant["xCH4_V107_filled"] = self.DataPlant["xCH4_V107"]
        
            # Carbon dioxide V101
        if (self.DataPlant["xCO2_V101"] != 0).any():
            self.DataPlant["xCO2_V101_filled"] = self.DataPlant["xCO2_V101"].replace(0, np.nan)
            self.DataPlant["xCO2_V101_filled"] = self.DataPlant["xCO2_V101_filled"].ffill()
            self.DataPlant['xCO2_V101_filled'] = self.DataPlant.apply(lambda row: row['xCO2_V101_filled'] if row['xCO2_V101'] == 0 else row['xCO2_V101'], axis=1)
            self.DataPlant['xCO2_V101_filled'] = self.DataPlant['xCO2_V101_filled'].fillna(0).astype(float)
            self.DataPlant['xCO2_V101_filled'] = self.DataPlant['xCO2_V101_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xCO2_V101_filled"] = self.DataPlant["xCO2_V101_filled"].mask(self.DataPlant["xCO2_V101_filled"] > 100, np.nan)
            self.DataPlant["xCO2_V101_filled"] = self.DataPlant["xCO2_V101_filled"].ffill()
            mean_value_xCO2_V101 = self.DataPlant["xCO2_V101_filled"]#.mean()
            self.DataPlant["xCO2_V101_filled"] = mean_value_xCO2_V101
        else:
            self.DataPlant["xCO2_V101_filled"] = self.DataPlant["xCO2_V101"]
        
        # Carbon dioxide V102
        if (self.DataPlant["xCO2_V102"] != 0).any():
            self.DataPlant["xCO2_V102_filled"] = self.DataPlant["xCO2_V102"].replace(0, np.nan)
            self.DataPlant["xCO2_V102_filled"] = self.DataPlant["xCO2_V102_filled"].ffill()
            self.DataPlant['xCO2_V102_filled'] = self.DataPlant.apply(lambda row: row['xCO2_V102_filled'] if row['xCO2_V102'] == 0 else row['xCO2_V102'], axis=1)
            self.DataPlant['xCO2_V102_filled'] = self.DataPlant['xCO2_V102_filled'].fillna(0).astype(float)
            self.DataPlant['xCO2_V102_filled'] = self.DataPlant['xCO2_V102_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xCO2_V102_filled"] = self.DataPlant["xCO2_V102_filled"].mask(self.DataPlant["xCO2_V102_filled"] > 100, np.nan)
            self.DataPlant["xCO2_V102_filled"] = self.DataPlant["xCO2_V102_filled"].ffill()
            mean_value_xCO2_V102 = self.DataPlant["xCO2_V102_filled"]#.mean()
            self.DataPlant["xCO2_V102_filled"] = mean_value_xCO2_V102
        else:
            self.DataPlant["xCO2_V102_filled"] = self.DataPlant["xCO2_V102"]
        
        # Carbon dioxide V107
        if (self.DataPlant["xCO2_V107"] != 0).any():
            self.DataPlant["xCO2_V107_filled"] = self.DataPlant["xCO2_V107"].replace(0, np.nan)
            self.DataPlant["xCO2_V107_filled"] = self.DataPlant["xCO2_V107_filled"].ffill()
            self.DataPlant['xCO2_V107_filled'] = self.DataPlant.apply(lambda row: row['xCO2_V107_filled'] if row['xCO2_V107'] == 0 else row['xCO2_V107'], axis=1)
            self.DataPlant['xCO2_V107_filled'] = self.DataPlant['xCO2_V107_filled'].fillna(0).astype(float)
            self.DataPlant['xCO2_V107_filled'] = self.DataPlant['xCO2_V107_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xCO2_V107_filled"] = self.DataPlant["xCO2_V107_filled"].mask(self.DataPlant["xCO2_V107_filled"] > 100, np.nan)
            self.DataPlant["xCO2_V107_filled"] = self.DataPlant["xCO2_V107_filled"].ffill()
            mean_value_xCO2_V107 = self.DataPlant["xCO2_V107_filled"]#.mean()
            self.DataPlant["xCO2_V107_filled"] = mean_value_xCO2_V107
        else:
            self.DataPlant["xCO2_V107_filled"] = self.DataPlant["xCO2_V107"]
        
        # Oxygen V101
        if (self.DataPlant["xO2_V101"] != 0).any():
            self.DataPlant["xO2_V101_filled"] = self.DataPlant["xO2_V101"].replace(0, np.nan)
            self.DataPlant["xO2_V101_filled"] = self.DataPlant["xO2_V101_filled"].ffill()
            self.DataPlant['xO2_V101_filled'] = self.DataPlant.apply(lambda row: row['xO2_V101_filled'] if row['xO2_V101'] == 0 else row['xO2_V101'], axis=1)
            self.DataPlant['xO2_V101_filled'] = self.DataPlant['xO2_V101_filled'].fillna(0).astype(float)
            self.DataPlant['xO2_V101_filled'] = self.DataPlant['xO2_V101_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xO2_V101_filled"] = self.DataPlant["xO2_V101_filled"].mask(self.DataPlant["xO2_V101_filled"] > 100, np.nan)
            self.DataPlant["xO2_V101_filled"] = self.DataPlant["xO2_V101_filled"].ffill()
            mean_value_xO2_V101 = self.DataPlant["xO2_V101_filled"]#.mean()
            self.DataPlant["xO2_V101_filled"] = mean_value_xO2_V101
        else:
            self.DataPlant["xO2_V101_filled"] = self.DataPlant["xO2_V101"]
        
        # Oxygen V102
        if (self.DataPlant["xO2_V102"] != 0).any():
            self.DataPlant["xO2_V102_filled"] = self.DataPlant["xO2_V102"].replace(0, np.nan)
            self.DataPlant["xO2_V102_filled"] = self.DataPlant["xO2_V102_filled"].ffill()
            self.DataPlant['xO2_V102_filled'] = self.DataPlant.apply(lambda row: row['xO2_V102_filled'] if row['xO2_V102'] == 0 else row['xO2_V102'], axis=1)
            self.DataPlant['xO2_V102_filled'] = self.DataPlant['xO2_V102_filled'].fillna(0).astype(float)
            self.DataPlant['xO2_V102_filled'] = self.DataPlant['xO2_V102_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xO2_V102_filled"] = self.DataPlant["xO2_V102_filled"].mask(self.DataPlant["xO2_V102_filled"] > 100, np.nan)
            self.DataPlant["xO2_V102_filled"] = self.DataPlant["xO2_V102_filled"].ffill()
            mean_value_xO2_V102 = self.DataPlant["xO2_V102_filled"]#.mean()
            self.DataPlant["xO2_V102_filled"] = mean_value_xO2_V102
        else:
            self.DataPlant["xO2_V102_filled"] = self.DataPlant["xO2_V102"]
        
        # Oxygen V107
        if (self.DataPlant["xO2_V107"] != 0).any():
            self.DataPlant["xO2_V107_filled"] = self.DataPlant["xO2_V107"].replace(0, np.nan)
            self.DataPlant["xO2_V107_filled"] = self.DataPlant["xO2_V107_filled"].ffill()
            self.DataPlant['xO2_V107_filled'] = self.DataPlant.apply(lambda row: row['xO2_V107_filled'] if row['xO2_V107'] == 0 else row['xO2_V107'], axis=1)
            self.DataPlant['xO2_V107_filled'] = self.DataPlant['xO2_V107_filled'].fillna(0).astype(float)
            self.DataPlant['xO2_V107_filled'] = self.DataPlant['xO2_V107_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xO2_V107_filled"] = self.DataPlant["xO2_V107_filled"].mask(self.DataPlant["xO2_V107_filled"] > 100, np.nan)
            self.DataPlant["xO2_V107_filled"] = self.DataPlant["xO2_V107_filled"].ffill()
            mean_value_xO2_V107 = self.DataPlant["xO2_V107_filled"]#.mean()
            self.DataPlant["xO2_V107_filled"] = mean_value_xO2_V107
        else:
            self.DataPlant["xO2_V107_filled"] = self.DataPlant["xO2_V107"]
            
        # Hydrogen V101
        if (self.DataPlant["xH2_V101"] != 0).any():
            self.DataPlant["xH2_V101_filled"] = self.DataPlant["xH2_V101"].replace(0, np.nan)
            self.DataPlant["xH2_V101_filled"] = self.DataPlant["xH2_V101_filled"].ffill()
            self.DataPlant['xH2_V101_filled'] = self.DataPlant.apply(lambda row: row['xH2_V101_filled'] if row['xH2_V101'] == 0 else row['xH2_V101'], axis=1)
            self.DataPlant['xH2_V101_filled'] = self.DataPlant['xH2_V101_filled'].fillna(0).astype(float)
            self.DataPlant['xH2_V101_filled'] = self.DataPlant['xH2_V101_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xH2_V101_filled"] = self.DataPlant["xH2_V101_filled"].mask(self.DataPlant["xH2_V101_filled"] > 1000000, np.nan)
            self.DataPlant["xH2_V101_filled"] = self.DataPlant["xH2_V101_filled"].ffill()
            mean_value_xH2_V101 = self.DataPlant["xH2_V101_filled"]#.mean()
            self.DataPlant["xH2_V101_filled"] = mean_value_xH2_V101
        else:
            self.DataPlant["xH2_V101_filled"] = self.DataPlant["xH2_V101"]
        
        # Hydrogen V102
        if (self.DataPlant["xH2_V102"] != 0).any():
            self.DataPlant["xH2_V102_filled"] = self.DataPlant["xH2_V102"].replace(0, np.nan)
            self.DataPlant["xH2_V102_filled"] = self.DataPlant["xH2_V102_filled"].ffill()
            self.DataPlant['xH2_V102_filled'] = self.DataPlant.apply(lambda row: row['xH2_V102_filled'] if row['xH2_V102'] == 0 else row['xH2_V102'], axis=1)
            self.DataPlant['xH2_V102_filled'] = self.DataPlant['xH2_V102_filled'].fillna(0).astype(float)
            self.DataPlant['xH2_V102_filled'] = self.DataPlant['xH2_V102_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xH2_V102_filled"] = self.DataPlant["xH2_V102_filled"].mask(self.DataPlant["xH2_V102_filled"] > 1000000, np.nan)
            self.DataPlant["xH2_V102_filled"] = self.DataPlant["xH2_V102_filled"].ffill()
            mean_value_xH2_V102 = self.DataPlant["xH2_V102_filled"]#.mean()
            self.DataPlant["xH2_V102_filled"] = mean_value_xH2_V102
        else:
            self.DataPlant["xH2_V102_filled"] = self.DataPlant["xH2_V102"]
        
        # Hydrogen V107
        if (self.DataPlant["xH2_V107"] != 0).any():
            self.DataPlant["xH2_V107_filled"] = self.DataPlant["xH2_V107"].replace(0, np.nan)
            self.DataPlant["xH2_V107_filled"] = self.DataPlant["xH2_V107_filled"].ffill()
            self.DataPlant['xH2_V107_filled'] = self.DataPlant.apply(lambda row: row['xH2_V107_filled'] if row['xH2_V107'] == 0 else row['xH2_V107'], axis=1)
            self.DataPlant['xH2_V107_filled'] = self.DataPlant['xH2_V107_filled'].fillna(0).astype(float)
            self.DataPlant['xH2_V107_filled'] = self.DataPlant['xH2_V107_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xH2_V107_filled"] = self.DataPlant["xH2_V107_filled"].mask(self.DataPlant["xH2_V107_filled"] > 1000000, np.nan)
            self.DataPlant["xH2_V107_filled"] = self.DataPlant["xH2_V107_filled"].ffill()
            mean_value_xH2_V107 = self.DataPlant["xH2_V107_filled"]#.mean()
            self.DataPlant["xH2_V107_filled"] = mean_value_xH2_V107
        else:
            self.DataPlant["xH2_V107_filled"] = self.DataPlant["xH2_V107"]
        
        # Hydrogen sulphide V101
        if (self.DataPlant["xH2S_V101"] != 0).any():
            self.DataPlant["xH2S_V101_filled"] = self.DataPlant["xH2S_V101"].replace(0, np.nan)
            self.DataPlant["xH2S_V101_filled"] = self.DataPlant["xH2S_V101_filled"].ffill()
            self.DataPlant['xH2S_V101_filled'] = self.DataPlant.apply(lambda row: row['xH2S_V101_filled'] if row['xH2S_V101'] == 0 else row['xH2S_V101'], axis=1)
            self.DataPlant['xH2S_V101_filled'] = self.DataPlant['xH2S_V101_filled'].fillna(0).astype(float)
            self.DataPlant['xH2S_V101_filled'] = self.DataPlant['xH2S_V101_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xH2S_V101_filled"] = self.DataPlant["xH2S_V101_filled"].mask(self.DataPlant["xH2S_V101_filled"] > 1000000, np.nan)
            self.DataPlant["xH2S_V101_filled"] = self.DataPlant["xH2S_V101_filled"].ffill()
            mean_value_xH2S_V101 = self.DataPlant["xH2S_V101_filled"]#.mean()
            self.DataPlant["xH2S_V101_filled"] = mean_value_xH2S_V101
        else:
            self.DataPlant["xH2S_V101_filled"] = self.DataPlant["xH2S_V101"]
        
        # Hydrogen sulphide V102
        if (self.DataPlant["xH2S_V102"] != 0).any():
            self.DataPlant["xH2S_V102_filled"] = self.DataPlant["xH2S_V102"].replace(0, np.nan)
            self.DataPlant["xH2S_V102_filled"] = self.DataPlant["xH2S_V102_filled"].ffill()
            self.DataPlant['xH2S_V102_filled'] = self.DataPlant.apply(lambda row: row['xH2S_V102_filled'] if row['xH2S_V102'] == 0 else row['xH2S_V102'], axis=1)
            self.DataPlant['xH2S_V102_filled'] = self.DataPlant['xH2S_V102_filled'].fillna(0).astype(float)
            self.DataPlant['xH2S_V102_filled'] = self.DataPlant['xH2S_V102_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xH2S_V102_filled"] = self.DataPlant["xH2S_V102_filled"].mask(self.DataPlant["xH2S_V102_filled"] > 1000000, np.nan)
            self.DataPlant["xH2S_V102_filled"] = self.DataPlant["xH2S_V102_filled"].ffill()
            mean_value_xH2S_V102 = self.DataPlant["xH2S_V102_filled"]#.mean()
            self.DataPlant["xH2S_V102_filled"] = mean_value_xH2S_V102
        else:
            self.DataPlant["xH2S_V102_filled"] = self.DataPlant["xH2S_V102"]
        
        # Hydrogen sulphide V107
        if (self.DataPlant["xH2S_V107"] != 0).any():
            self.DataPlant["xH2S_V107_filled"] = self.DataPlant["xH2S_V107"].replace(0, np.nan)
            self.DataPlant["xH2S_V107_filled"] = self.DataPlant["xH2S_V107_filled"].ffill()
            self.DataPlant['xH2S_V107_filled'] = self.DataPlant.apply(lambda row: row['xH2S_V107_filled'] if row['xH2S_V107'] == 0 else row['xH2S_V107'], axis=1)
            self.DataPlant['xH2S_V107_filled'] = self.DataPlant['xH2S_V107_filled'].fillna(0).astype(float)
            self.DataPlant['xH2S_V107_filled'] = self.DataPlant['xH2S_V107_filled'].replace(0, np.nan).bfill().ffill()
            self.DataPlant["xH2S_V107_filled"] = self.DataPlant["xH2S_V107_filled"].mask(self.DataPlant["xH2S_V107_filled"] > 1000000, np.nan)
            self.DataPlant["xH2S_V107_filled"] = self.DataPlant["xH2S_V107_filled"].ffill()
            mean_value_xH2S_V107 = self.DataPlant["xH2S_V107_filled"]#.mean()
            self.DataPlant["xH2S_V107_filled"] = mean_value_xH2S_V107
        else:
            self.DataPlant["xH2S_V107_filled"] = self.DataPlant["xH2S_V107"]
        
        self.DataPlant = self.DataPlant.drop_duplicates(subset = "time", keep = "first")
        self.DataPlant.ffill(inplace=True)
        self.DataPlant.bfill(inplace=True)
    
    def LimitReagentCalculation(self):
        self.SN = self.Datainterfaz["_value"]["MNS"]
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
            self.rho = (self.rho1*self.MP1 + self.rho2*self.MP2 + self.rho3*self.MP3 + self.rho4*self.MP4 + 1000*self.MPH)
            
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
            self.rho = (self.rho1*self.MP1 + self.rho2*self.MP2 + self.rho3*self.MP3 + 1000*self.MPH)
            
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
            self.rho = (self.rho1*self.MP1 + self.rho2*self.MP2 + 1000*self.MPH)
            
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
            self.rho = (self.rho1*self.MP1 + 1000*self.MPH)
            
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
        self.Cst_sus = (self.rho*(self.ST))/self.MW_sustrato
        self.Cst_sus_gl = (self.rho*(self.ST))
        self.Csv_sus = (self.rho*(self.SV))/self.MW_sustrato
        self.Csv_sus_gl = (self.rho*(self.SV))
        self.Cfixed = self.Cst_sus - self.Csv_sus
    
    def StochoimetricExpenditure(self, Model):
        '''
            quantify the methane produced : Note: If the training execution starts significantly later than the plant's operation
            (exceeding the training time), it will not be possible to quantify the methane produced by the plant before the training begins.
            Example: If the training time is 60 minutes but the plant starts operating 70 minutes earlier, there will be 10 minutes of methane 
            production that cannot be quantified by the digital twin.   
            '''
        self.Model = Model
        #---------------------------------------------
        #--------- Variables to train Operation Mode 1 and 2
        if self.Operation_mode == 1 or self.Operation_mode == 2:
            #Compounds by mol V101 
            # Accumulated
            self.biogas_mol_V101_acum = ((self.DataPlant["Pacum_V101"]*6894.76)*self.Volume_V101/1000)/(8.314*(self.DataPlant["T_V101"]+273.15))
            self.biogas_mol_V101_acum.ffill(inplace=True)
            self.biogas_mol_V101_acum.bfill(inplace=True)
            self.biogas_mol_V101_acum_NN = self.biogas_mol_V101_acum
            if self.biogas_mol_V101_acum.iloc[0]>0:
                nbiogas_max_value = max(self.biogas_mol_V101_acum)
                self.biogas_mol_V101_acum = self.biogas_mol_V101_acum - nbiogas_max_value
            self.nCH4_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xCH4_V101_filled"]/100
            self.nCO2_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xCO2_V101_filled"]/100
            self.nO2_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xO2_V101_filled"]/100
            self.nH2S_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xH2S_V101_filled"]/1000000
            self.nH2_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xH2_V101_filled"]/1000000
            self.nNH3_V101_acum = self.nCH4_V101_acum * (self.s_NH3/self.s_CH4)
            #Accumulated (g)
            self.wCH4_V101_acum = self.nCH4_V101_acum * 16.04
            self.wCO2_V101_acum = self.nCO2_V101_acum * 44.009
            self.wO2_V101_acum = self.nO2_V101_acum * 32
            self.wH2S_V101_acum = self.nH2S_V101_acum * 34.082
            self.wH2_V101_acum = self.nH2_V101_acum * 2
            self.wNH3_V101_acum = self.nNH3_V101_acum * 17.031
            # Storaged
            self.biogas_mol_V101 = ((self.DataPlant["P_V101"]*6894.76) * self.Volume_V101/1000)/(8.314*(self.DataPlant["T_V101"]+273.15))
            self.nCH4_V101 = self.biogas_mol_V101 * self.DataPlant["xCH4_V101_filled"]/100
            self.nCO2_V101 = self.biogas_mol_V101 * self.DataPlant["xCO2_V101_filled"]/100
            self.nO2_V101 = self.biogas_mol_V101 * self.DataPlant["xO2_V101_filled"]/100
            self.nH2S_V101 = self.biogas_mol_V101 * self.DataPlant["xH2S_V101_filled"]/1000000
            self.nH2_V101 = self.biogas_mol_V101 * self.DataPlant["xH2_V101_filled"]/1000000
            self.nNH3_V101 = self.nCH4_V101 * (self.s_NH3/self.s_CH4)
            
            #Compound by mol V102
            #Accumulated (mol)
            self.biogas_mol_V102_acum = ((self.DataPlant["Pacum_V102"]*6894.76)*self.Volume_V102/1000)/(8.314*(self.DataPlant["T_V102"]+273.15))
            self.biogas_mol_V102_acum.ffill(inplace=True)
            self.biogas_mol_V102_acum.bfill(inplace = True)
            self.biogas_mol_V102_acum_NN = self.biogas_mol_V102_acum
            self.nCH4_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xCH4_V102_filled"]/100
            self.nCO2_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xCO2_V102_filled"]/100
            self.nO2_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xO2_V102_filled"]/100
            self.nH2S_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xH2S_V102_filled"]/1000000
            self.nH2_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xH2_V102_filled"]/1000000
            self.nNH3_V102_acum = self.nCH4_V102_acum * (self.s_NH3/self.s_CH4)
            #Accumulated (g)
            self.wCH4_V102_acum = self.nCH4_V102_acum * 16.04
            self.wCO2_V102_acum = self.nCO2_V102_acum * 44.009
            self.wO2_V102_acum = self.nO2_V102_acum * 32
            self.wH2S_V102_acum = self.nH2S_V102_acum * 34.082
            self.wH2_V102_acum = self.nH2_V102_acum * 2
            self.wNH3_V102_acum = self.nNH3_V102_acum * 17.031
            #Storage
            self.biogas_mol_V102 = ((self.DataPlant["P_V102"]*6894.76)*self.Volume_V102/1000)/(8.314*(self.DataPlant["T_V102"]+273.15))
            self.nCH4_V102 = self.biogas_mol_V102 * self.DataPlant["xCH4_V102_filled"]/100
            self.nCO2_V102 = self.biogas_mol_V102 * self.DataPlant["xCO2_V102_filled"]/100
            self.nO2_V102 = self.biogas_mol_V102 * self.DataPlant["xO2_V102_filled"]/100
            self.nH2S_V102 = self.biogas_mol_V102 * self.DataPlant["xH2S_V102_filled"]/1000000
            self.nH2_V102 = self.biogas_mol_V102 * self.DataPlant["xH2_V102_filled"]/1000000
            self.nNH3_V102 = self.nCH4_V102 * (self.s_NH3/self.s_CH4)

            #compound by mol V107
            #Accumulated
            self.biogas_mol_V107_acum = ((self.DataPlant["Pacum_V107"]*6894.76)*self.Volume_V107/1000)/(8.314*(self.DataPlant["T_V107"]+273.15))
            self.biogas_mol_V107_acum.ffill(inplace=True)
            self.biogas_mol_V107_acum.bfill(inplace=True)
            self.nCH4_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xCH4_V107_filled"]/100
            self.nCO2_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xCO2_V107_filled"]/100
            self.nO2_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xO2_V107_filled"]/100
            self.nH2S_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xH2S_V107_filled"]/1000000
            self.nH2_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xH2_V107_filled"]/1000000
            self.nNH3_V107_acum = self.nCH4_V107_acum * (self.s_NH3/self.s_CH4)
            #Accumulated (g)
            self.wCH4_V107_acum = self.nCH4_V107_acum * 16.04
            self.wCO2_V107_acum = self.nCO2_V107_acum * 44.009
            self.wO2_V107_acum = self.nO2_V107_acum * 32
            self.wH2S_V107_acum = self.nH2S_V107_acum * 34.082
            self.wH2_V107_acum = self.nH2_V107_acum * 2
            self.wNH3_V107_acum = self.nNH3_V107_acum * 17.031
            #Storage
            self.biogas_mol_V107 = ((self.DataPlant["P_V107"]*6894.76)*self.Volume_V107/1000)/(8.314*(self.DataPlant["T_V107"]+273.15))
            self.nCH4_V107 = self.biogas_mol_V107 * self.DataPlant["xCH4_V107_filled"]/100
            self.nCO2_V107 = self.biogas_mol_V107 * self.DataPlant["xCO2_V107_filled"]/100
            self.nO2_V107 = self.biogas_mol_V107 * self.DataPlant["xO2_V107_filled"]/100
            self.nH2S_V107 = self.biogas_mol_V107 * self.DataPlant["xH2S_V107_filled"]/1000000
            self.nH2_V107 = self.biogas_mol_V107 * self.DataPlant["xH2_V107_filled"]/1000000
            self.nNH3_V107 = self.nCH4_V107 * (self.s_NH3/self.s_CH4)

            #R101 mol trnaformed
            self.dnCH4_dt = self.nCH4_V101_acum.diff().fillna(0)
            self.dnCO2_dt = self.nCO2_V101_acum.diff().fillna(0)
            self.dnO2_dt = self.nO2_V101_acum.diff().fillna(0)
            self.dnH2S_dt = self.nH2S_V101_acum.diff().fillna(0)
            self.dnH2_dt = self.nH2_V101_acum.diff().fillna(0)
            self.dnNH3_dt = self.nNH3_V101_acum.diff().fillna(0)
            self.dnbio_dt = (self.dnCH4_dt + self.dnCO2_dt + self.dnO2_dt + self.dnH2S_dt + self.dnH2_dt + self.dnNH3_dt)
            #R101 mass trnasformed (gram)
            self.dwCH4_dt = self.wCH4_V101_acum.diff().fillna(0)
            self.dwCO2_dt = self.wCO2_V101_acum.diff().fillna(0)
            self.dwO2_dt = self.wO2_V101_acum.diff().fillna(0)
            self.dwH2S_dt = self.wH2S_V101_acum.diff().fillna(0)
            self.dwH2_dt = self.wH2_V101_acum.diff().fillna(0)
            self.dwNH3_dt = self.wNH3_V101_acum.diff().fillna(0)
            self.dwbio_dt = (self.dwCH4_dt + self.dwCO2_dt + self.dwO2_dt + self.dwH2S_dt + self.dwH2_dt + self.dwNH3_dt)

            #Mass balance
            #Initial value (mass inside reactor)
            try:
                if self.TrainMode.empty:
                    print("The DataFrame exists but is empty.")
                    self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                    self.SV_ini_R101 = self.SV_ini_R101
                    self.ST_ini_R101 = self.ST_ini_R101
                else:
                    self.Csus_ini_SV_R101 = self.TrainMode["Csus_exp"].iloc[0]
                    self.SV_ini_R101 = self.TrainMode["SV_exp_R101"].iloc[0]
                    self.ST_ini_R101 = self.TrainMode["ST_exp_R101"].iloc[0]

            except AttributeError:
                    print("The DataFrame does not exist.")
            
            # dt
            self.tp = self.DataPlant["normal_time"].diff().fillna(0)                       #min
            # Vol inyected in L
            self.Vol_inj_R101 = self.DataPlant["P104"] * (self.tp/60)                      #Liters
            self.Vol_inj_R101 = self.Vol_inj_R101.cumsum()
            # substrate_inoculum ratio
            self.substrate_ratio = (self.Vol_inj_R101/30).clip(upper=1)
            self.inoculum_ratio = 1 - self.substrate_ratio
            # mass inyected in volatile solids
            self.mass_inlet = self.DataPlant["P104"] * self.rho * (self.tp/60) * self.SV/100   #gSV (grams of volatile solids)
            
            #Mass Balance
            normal_time = []
            OM_int_SV = []
            OM_in_SV = []
            OM_int_ST = []
            OM_in_ST = []
            mol_int = []
            mol_in = []
            Q_P104 = []
            T_R101 = []
            mass_out = []
            
            for i in range (len(self.mass_inlet)-1):
                #Mass balance in grams for volatile solids
                self.mass_ini = (self.SV_ini_R101 * 30 * (self.substrate_ratio.iloc[i]*self.rho + self.inoculum_ratio.iloc[i]*self.rho_ini_R101))
                self.mass_in = ((self.SV) * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outl = (self.SV_ini_R101 * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outg = self.dwbio_dt.iloc[i]
                self.SV_ini_R101 = (self.mass_ini + self.mass_in - self.mass_outl - self.mass_outg)/30/(self.substrate_ratio.iloc[i]*self.rho + self.inoculum_ratio.iloc[i]*self.rho_ini_R101)
                self.Csus_ini_SV_R101_gl = self.SV_ini_R101 * (self.substrate_ratio.iloc[i]*self.rho + self.inoculum_ratio.iloc[i]*self.rho_ini_R101)
                if not pd.isna(self.SV_ini_R101):
                    OM_int_SV.append(self.SV_ini_R101)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (SVR101).")
                            OM_int_SV.append(self.SV_ini_R101_res)
                        else:
                            OM_int_SV.append(self.TrainMode["SV_exp_R101"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (SVR101).")
                        OM_int_SV.append(self.SV_ini_R101_res)
                OM_in_SV.append(self.mass_in)
                # Mass balance in grams for total solids
                self.mass_ini_ST = (self.ST_ini_R101 * 30 * (self.substrate_ratio.iloc[i]*self.rho + self.inoculum_ratio.iloc[i]*self.rho_ini_R101))
                self.mass_in_ST = ((self.ST) * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outl_ST = (self.ST_ini_R101 * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outg_ST = self.dwbio_dt.iloc[i]
                self.ST_ini_R101 = (self.mass_ini_ST + self.mass_in_ST - self.mass_outl_ST - self.mass_outg_ST)/30/(self.substrate_ratio.iloc[i]*self.rho + self.inoculum_ratio.iloc[i]*self.rho_ini_R101)
                self.Csus_ini_ST_R101_gl = self.ST_ini_R101 * (self.substrate_ratio.iloc[i]*self.rho + self.inoculum_ratio.iloc[i]*self.rho_ini_R101)
                if not pd.isna(self.ST_ini_R101):
                    OM_int_ST.append(self.ST_ini_R101)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (ST_R101).")
                            OM_int_ST.append(self.ST_ini_R101_res)
                        else:
                            OM_int_ST.append(self.TrainMode["ST_exp_R101"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (ST_R101).")
                        OM_int_ST.append(self.ST_ini_R101_res)
                OM_in_ST.append(self.mass_in_ST)
                # Mass balance in mol volatile solids
                self.mol_ini = (self.Csus_ini_SV_R101 * 30)
                self.mol_in = (self.Csv_sus * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60))
                self.mol_outl = (self.Csus_ini_SV_R101 * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60))
                self.mol_outg = self.dnCH4_dt.iloc[i]*(1/(self.substrate_ratio.iloc[i]*self.s_CH4 + self.inoculum_ratio.iloc[i]*self.s_CH4_ini_R101))
                self.Csus_ini_SV_R101 = (self.mol_ini + self.mol_in - self.mol_outl - self.mol_outg)/30
                if not pd.isna(self.Csus_ini_SV_R101):
                    mol_int.append(self.Csus_ini_SV_R101)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (ST_R101).")
                            mol_int.append(self.Csus_ini_SV_R101_res)
                        else:
                            mol_int.append(self.TrainMode["ST_exp_R101"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (ST_R101).")
                        mol_int.append(self.Csus_ini_SV_R101_res)
                mol_in.append(self.mol_in)
                # Storage time to avoid dimenssion issues
                normal_time.append(self.DataPlant["normal_time"].iloc[i])
                mass_out.append(self.dwbio_dt.iloc[i])
                Q_P104.append(self.DataPlant["P104"].iloc[i])
                T_R101.append(self.DataPlant["Tprom_R101"].iloc[i])
                
            print("mass_ini_SV: ",self.mass_ini) 
            print("mass_in_SV: ", self.mass_in) 
            print("mass_outl_SV: ", self.mass_outl)
            print("mass_outg_SV: ", self.mass_outg)
            print("rho_R101_SV: ", (self.substrate_ratio.iloc[-1]*self.rho + self.inoculum_ratio.iloc[-1]*self.rho_ini_R101))
            print("SV_ini_R101: ", self.SV_ini_R101)

            print("mass_ini_ST: ",self.mass_ini_ST) 
            print("mass_in_ST: ", self.mass_in_ST) 
            print("mass_outl_ST: ", self.mass_outl_ST)
            print("mass_outg_ST: ", self.mass_outg_ST)
            print("ST_ini_R101: ", self.ST_ini_R101)
            
            self.TrainMode = pd.DataFrame({"time": normal_time,
                                        "SV_exp_R101": OM_int_SV,
                                        "VS_in": OM_in_SV,
                                        "ST_exp_R101": OM_int_ST,
                                        "TS_in": OM_in_ST,
                                        "Csus_exp": mol_int,
                                        "mol_org_in": mol_in,
                                        "mass_out": mass_out,
                                        "Q_P104": Q_P104,
                                        "T_R101": T_R101})
            
            self.TrainMode["Vol"] = 30
            self.TrainMode["Csus_in_R101"] = self.Csv_sus
            self.x_R101 = (self.TrainMode["Csus_in_R101"] - self.TrainMode["Csus_exp"])/self.TrainMode["Csus_in_R101"]

            if self.Model == "Gompertz":
                V_acum_Gompertz = self.DataPlant["Vacum_V101"]
                if V_acum_Gompertz.iloc[0] > 0:
                    max_value_Vacum_gompertz = max(V_acum_Gompertz)
                else:
                    V_acum_Gompertz = V_acum_Gompertz - max_value_Vacum_gompertz
                self.V_bio_Gompertz = V_acum_Gompertz/self.mass_ini      #gompertz exit Lbio/gSV
                self.TrainMode_gompertz = pd.DataFrame({"time": self.DataPlant["normal_time"],
                                                        "y_t_exp": self.V_bio_Gompertz,
                                                        "Vacum_V101": V_acum_Gompertz})
            
            self.global_time = self.global_time + (10/1440)
            self.OC_R101 = self.SV_ini_R101/self.global_time

        elif self.Operation_mode in [3, 5]:
            #Compounds by mol V101 
            # Accumulated
            self.biogas_mol_V101_acum = ((self.DataPlant["Pacum_V101"]*6894.76)*self.Volume_V101/1000)/(8.314*(self.DataPlant["T_V101"]+273.15))
            self.biogas_mol_V101_acum.ffill(inplace=True)
            self.biogas_mol_V101_acum.bfill(inplace=True)
            self.biogas_mol_V101_acum_NN = self.biogas_mol_V101_acum
            if self.biogas_mol_V101_acum.iloc[0]>0:
                nbiogas_max_value_V101 = max(self.biogas_mol_V101_acum)
                self.biogas_mol_V101_acum = self.biogas_mol_V101_acum - nbiogas_max_value_V101
            self.nCH4_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xCH4_V101_filled"]/100
            self.nCO2_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xCO2_V101_filled"]/100
            self.nO2_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xO2_V101_filled"]/100
            self.nH2S_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xH2S_V101_filled"]/1000000
            self.nH2_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xH2_V101_filled"]/1000000
            self.nNH3_V101_acum = self.nCH4_V101_acum * (self.s_NH3/self.s_CH4)
            #Accumulated (g)
            self.wCH4_V101_acum = self.nCH4_V101_acum * 16.04
            self.wCO2_V101_acum = self.nCO2_V101_acum * 44.009
            self.wO2_V101_acum = self.nO2_V101_acum * 32
            self.wH2S_V101_acum = self.nH2S_V101_acum * 34.082
            self.wH2_V101_acum = self.nH2_V101_acum * 2
            self.wNH3_V101_acum = self.nNH3_V101_acum * 17.031
             # Storaged
            self.biogas_mol_V101 = ((self.DataPlant["P_V101"]*6894.76) * self.Volume_V101/1000)/(8.314*(self.DataPlant["T_V101"]+273.15))
            self.nCH4_V101 = self.biogas_mol_V101 * self.DataPlant["xCH4_V101_filled"]/100
            self.nCO2_V101 = self.biogas_mol_V101 * self.DataPlant["xCO2_V101_filled"]/100
            self.nO2_V101 = self.biogas_mol_V101 * self.DataPlant["xO2_V101_filled"]/100
            self.nH2S_V101 = self.biogas_mol_V101 * self.DataPlant["xH2S_V101_filled"]/1000000
            self.nH2_V101 = self.biogas_mol_V101 * self.DataPlant["xH2_V101_filled"]/1000000
            self.nNH3_V101 = self.nCH4_V101 * (self.s_NH3/self.s_CH4)
            
            #Compound by mol V102
            #Accumulated (mol)
            self.biogas_mol_V102_acum = ((self.DataPlant["Pacum_V102"]*6894.76)*self.Volume_V102/1000)/(8.314*(self.DataPlant["T_V102"]+273.15))
            self.biogas_mol_V102_acum.ffill(inplace=True)
            self.biogas_mol_V102_acum.bfill(inplace=True)
            if self.biogas_mol_V102_acum.iloc[0]>0:
                nbiogas_max_value_V102 = max(self.biogas_mol_V102_acum)
                self.biogas_mol_V102_acum = self.biogas_mol_V102_acum - nbiogas_max_value_V102
            self.nCH4_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xCH4_V102_filled"]/100
            self.nCO2_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xCO2_V102_filled"]/100
            self.nO2_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xO2_V102_filled"]/100
            self.nH2S_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xH2S_V102_filled"]/1000000
            self.nH2_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xH2_V102_filled"]/1000000
            self.nNH3_V102_acum = self.nCH4_V102_acum * (self.s_NH3/self.s_CH4)
            #Accumulated (g)
            self.wCH4_V102_acum = self.nCH4_V102_acum * 16.04
            self.wCO2_V102_acum = self.nCO2_V102_acum * 44.009
            self.wO2_V102_acum = self.nO2_V102_acum * 32
            self.wH2S_V102_acum = self.nH2S_V102_acum * 34.082
            self.wH2_V102_acum = self.nH2_V102_acum * 2
            self.wNH3_V102_acum = self.nNH3_V102_acum * 17.031
            #Storage
            self.biogas_mol_V102 = ((self.DataPlant["P_V102"]*6894.76)*self.Volume_V102/1000)/(8.314*(self.DataPlant["T_V102"]+273.15))
            self.nCH4_V102 = self.biogas_mol_V102 * self.DataPlant["xCH4_V102_filled"]/100
            self.nCO2_V102 = self.biogas_mol_V102 * self.DataPlant["xCO2_V102_filled"]/100
            self.nO2_V102 = self.biogas_mol_V102 * self.DataPlant["xO2_V102_filled"]/100
            self.nH2S_V102 = self.biogas_mol_V102 * self.DataPlant["xH2S_V102_filled"]/1000000
            self.nH2_V102 = self.biogas_mol_V102 * self.DataPlant["xH2_V102_filled"]/1000000
            self.nNH3_V102 = self.nCH4_V102 * (self.s_NH3/self.s_CH4)

            #compound by mol V107
            #Accumulated
            self.biogas_mol_V107_acum = ((self.DataPlant["Pacum_V107"]*6894.76)*self.Volume_V107/1000)/(8.314*(self.DataPlant["T_V107"]+273.15))
            self.nCH4_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xCH4_V107_filled"]/100
            self.nCO2_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xCO2_V107_filled"]/100
            self.nO2_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xO2_V107_filled"]/100
            self.nH2S_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xH2S_V107_filled"]/1000000
            self.nH2_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xH2_V107_filled"]/1000000
            self.nNH3_V107_acum = self.nCH4_V107_acum * (self.s_NH3/self.s_CH4)
            #Accumulated (g)
            self.wCH4_V107_acum = self.nCH4_V107_acum * 16.04
            self.wCO2_V107_acum = self.nCO2_V107_acum * 44.009
            self.wO2_V107_acum = self.nO2_V107_acum * 32
            self.wH2S_V107_acum = self.nH2S_V107_acum * 34.082
            self.wH2_V107_acum = self.nH2_V107_acum * 2
            self.wNH3_V107_acum = self.nNH3_V107_acum * 17.031
            #Storage
            self.biogas_mol_V107 = ((self.DataPlant["P_V107"]*6894.76)*self.Volume_V107/1000)/(8.314*(self.DataPlant["T_V107"]+273.15))
            self.nCH4_V107 = self.biogas_mol_V107 * self.DataPlant["xCH4_V107_filled"]/100
            self.nCO2_V107 = self.biogas_mol_V107 * self.DataPlant["xCO2_V107_filled"]/100
            self.nO2_V107 = self.biogas_mol_V107 * self.DataPlant["xO2_V107_filled"]/100
            self.nH2S_V107 = self.biogas_mol_V107 * self.DataPlant["xH2S_V107_filled"]/1000000
            self.nH2_V107 = self.biogas_mol_V107 * self.DataPlant["xH2_V107_filled"]/1000000
            self.nNH3_V107 = self.nCH4_V107 * (self.s_NH3/self.s_CH4)

            #R101 mol transformed
            self.dnCH4_dt_R101 = self.nCH4_V101_acum.diff().fillna(0)
            self.dnCO2_dt_R101 = self.nCO2_V101_acum.diff().fillna(0)
            self.dnO2_dt_R101 = self.nO2_V101_acum.diff().fillna(0)
            self.dnH2S_dt_R101 = self.nH2S_V101_acum.diff().fillna(0)
            self.dnH2_dt_R101 = self.nH2_V101_acum.diff().fillna(0)
            self.dnNH3_dt_R101 = self.nNH3_V101_acum.diff().fillna(0)
            self.dnbio_dt_R101 = (self.dnCH4_dt + self.dnCO2_dt + self.dnO2_dt + self.dnH2S_dt + self.dnH2_dt + self.dnNH3_dt)
            #R101 mass trnasformed (gram)
            self.dwCH4_dt_R101 = self.wCH4_V101_acum.diff().fillna(0)
            self.dwCO2_dt_R101 = self.wCO2_V101_acum.diff().fillna(0)
            self.dwO2_dt_R101 = self.wO2_V101_acum.diff().fillna(0)
            self.dwH2S_dt_R101 = self.wH2S_V101_acum.diff().fillna(0)
            self.dwH2_dt_R101 = self.wH2_V101_acum.diff().fillna(0)
            self.dwNH3_dt_R101 = self.wNH3_V101_acum.diff().fillna(0)
            self.dwbio_dt_R101 = (self.dwCH4_dt_R101 + self.dwCO2_dt_R101 + self.dwO2_dt_R101 + self.dwH2S_dt_R101 + self.dwH2_dt_R101 + self.dwNH3_dt_R101)

            #R102 mol transformed
            self.dnCH4_dt_R102 = self.nCH4_V102_acum.diff().fillna(0)
            self.dnCO2_dt_R102 = self.nCO2_V102_acum.diff().fillna(0)
            self.dnO2_dt_R102 = self.nO2_V102_acum.diff().fillna(0)
            self.dnH2S_dt_R102 = self.nH2S_V102_acum.diff().fillna(0)
            self.dnH2_dt_R102 = self.nH2_V102_acum.diff().fillna(0)
            self.dnNH3_dt_R102 = self.nNH3_V102_acum.diff().fillna(0)
            self.dnbio_dt_R102 = (self.dnCH4_dt_R102 + self.dnCO2_dt_R102 + self.dnO2_dt_R102 + self.dnH2S_dt_R102 + self.dnH2_dt_R102 + self.dnNH3_dt_R102)
            #R102 mass trnasformed (gram)
            self.dwCH4_dt_R102 = self.wCH4_V102_acum.diff().fillna(0)
            self.dwCO2_dt_R102 = self.wCO2_V102_acum.diff().fillna(0)
            self.dwO2_dt_R102 = self.wO2_V102_acum.diff().fillna(0)
            self.dwH2S_dt_R102 = self.wH2S_V102_acum.diff().fillna(0)
            self.dwH2_dt_R102 = self.wH2_V102_acum.diff().fillna(0)
            self.dwNH3_dt_R102 = self.wNH3_V102_acum.diff().fillna(0)
            self.dwbio_dt_R102 = (self.dwCH4_dt_R102 + self.dwCO2_dt_R102 + self.dwO2_dt_R102 + self.dwH2S_dt_R102 + self.dwH2_dt_R102 + self.dwNH3_dt_R102)

            #Mass balance
            #Initial values (mass inside reactors)
            try:
                if self.TrainMode.empty:
                    print("The DataFrame exists but is empty.")
                    self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                    self.SV_ini_R101 = self.SV_ini_R101
                    self.ST_ini_R101 = self.ST_ini_R101
                    
                    self.Csus_ini_SV_R102 = self.Csus_ini_SV_R102
                    self.SV_ini_R102 = self.SV_ini_R102
                    self.ST_ini_R102 = self.ST_ini_R102 
                else:
                    self.Csus_ini_SV_R101 = self.TrainMode["Csus_exp_R101"].iloc[0]
                    self.SV_ini_R101 = self.TrainMode["SV_exp_R101"].iloc[0]
                    self.ST_ini_R101 = self.TrainMode["ST_exp_R101"].iloc[0]

                    self.Csus_ini_SV_R102 = self.TrainMode["Csus_exp_R102"].iloc[0]
                    self.SV_ini_R102 = self.TrainMode["SV_exp_R102"].iloc[0]
                    self.ST_ini_R102 = self.TrainMode["ST_exp_R102"].iloc[0]
            
            except AttributeError:
                    print("The DataFrame does not exist.")
            
            # dt
            self.tp = self.DataPlant["normal_time"].diff().fillna(0)                       #min
            # Vol inyected in L
            self.Vol_inj_R101 = self.DataPlant["P104"] * (self.tp/60)                      #Liters
            self.Vol_inj_R101 = self.Vol_inj_R101.cumsum()

            self.Vol_inj_R102 = self.DataPlant["P101"] * (self.tp/60)                      #Liters
            self.Vol_inj_R102 = self.Vol_inj_R102.cumsum()

            # substrate_inoculum ratio
            self.substrate_ratio_R101 = (self.Vol_inj_R101/30).clip(upper=1)
            self.inoculum_ratio_R101 = 1 - self.substrate_ratio_R101

            self.substrate_ratio_R102 = (self.Vol_inj_R102/70).clip(upper=1)
            self.inoculum_ratio_R102 = 1 - self.substrate_ratio_R102 

            # mass inyected to R101
            self.mass_inlet = self.DataPlant["P104"] * self.rho * (self.tp/60) * self.SV/100   #gSV (grams of volatile solids)

            #time, pumps and temperature
            normal_time = []
            Q_P104 = []
            Q_P101 = []

            #Mass Balance R101
            OM_int_SV_R101 = []
            OM_in_SV_R101 = []
            OM_int_ST_R101 = []
            OM_in_ST_R101 = []
            mol_int_R101 = []
            mol_in_R101 = []
            T_R101 = []
            mass_out_R101 = []

            #Mass Balance R102
            OM_int_SV_R102 = []
            OM_in_SV_R102 = []
            OM_int_ST_R102 = []
            OM_in_ST_R102 = []
            mol_int_R102 = []
            mol_in_R102 = []
            T_R102 = []
            mass_out_R102 = []

            for i in range (len(self.mass_inlet - 1)):
                # Mass balance in R101
                #Mass balance in grams for volatile solids
                self.mass_ini_R101 = (self.SV_ini_R101 * 30 * (self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101))
                self.mass_in_R101 = ((self.SV) * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outl_R101 = (self.SV_ini_R101 * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)          #This mass in to R102
                self.mass_outg_R101 = self.dwbio_dt_R101.iloc[i]
                self.SV_ini_R101 = (self.mass_ini_R101 + self.mass_in_R101 - self.mass_outl_R101 - self.mass_outg_R101)/30/(self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101)
                self.Csus_ini_SV_R101_gl = self.SV_ini_R101 * (self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101)
                if not pd.isna(self.SV_ini_R101):
                    OM_int_SV_R101.append(self.SV_ini_R101)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (SVR101).")
                            OM_int_SV_R101.append(self.SV_ini_R101_res)
                        else:
                            OM_int_SV_R101.append(self.TrainMode["SV_exp_R101"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (SVR101).")
                        OM_int_SV_R101.append(self.SV_ini_R101_res)
                OM_in_SV_R101.append(self.mass_in_R101)
                # Mass balance in grams for total solids
                self.mass_ini_ST_R101 = (self.ST_ini_R101 * 30 * (self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101))
                self.mass_in_ST_R101 = ((self.ST) * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outl_ST_R101 = (self.ST_ini_R101 * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outg_ST_R101 = self.dwbio_dt_R101.iloc[i]
                self.ST_ini_R101 = (self.mass_ini_ST_R101 + self.mass_in_ST_R101 - self.mass_outl_ST_R101 - self.mass_outg_ST_R101)/30/(self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101)
                self.Csus_ini_ST_R101_gl = self.ST_ini_R101 * (self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101)
                if not pd.isna(self.ST_ini_R101):
                    OM_int_ST_R101.append(self.ST_ini_R101)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (STR101).")
                            OM_int_ST_R101.append(self.ST_ini_R101_res)
                        else:
                            OM_int_ST_R101.append(self.TrainMode["ST_exp_R101"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (STR101).")
                        OM_int_ST_R101.append(self.ST_ini_R101_res)
                OM_in_ST_R101.append(self.mass_in_ST_R101)
                # Mass balance in mol volatile solids
                self.mol_ini_R101 = (self.Csus_ini_SV_R101 * 30)
                self.mol_in_R101 = (self.Csv_sus * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60))
                self.mol_outl_R101 = (self.Csus_ini_SV_R101 * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60))
                self.mol_outg_R101 = self.dnCH4_dt_R101.iloc[i]*(1/(self.substrate_ratio_R101.iloc[i]*self.s_CH4 + self.inoculum_ratio_R101.iloc[i]*self.s_CH4_ini_R101))
                self.Csus_ini_SV_R101 = (self.mol_ini_R101 + self.mol_in_R101 - self.mol_outl_R101 - self.mol_outg_R101)/30
                if not pd.isna(self.Csus_ini_SV_R101):
                    mol_int_R101.append(self.Csus_ini_SV_R101)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (STR101).")
                            mol_int_R101.append(self.Csus_ini_SV_R101_res)
                        else:
                            mol_int_R101.append(self.TrainMode["Csus_exp"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (STR101).")
                        mol_int_R101.append(self.ST_ini_R101_res)
                mol_in_R101.append(self.mol_in_R101)
        
                #Mass balance in R102
                #Mass balance in grams for volatile solids
                self.mass_ini_R102 = (self.SV_ini_R102 * 30 * (self.substrate_ratio_R102.iloc[i]*self.rho + self.inoculum_ratio_R102.iloc[i]*self.rho_ini_R102))
                self.mass_in_R102 = ((self.SV_ini_R101) * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outl_R102 = (self.SV_ini_R102 * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)          #This mass in to R102
                self.mass_outg_R102 = self.dwbio_dt_R102.iloc[i]
                self.SV_ini_R102 = (self.mass_ini_R102 + self.mass_in_R102 - self.mass_outl_R102 - self.mass_outg_R102)/30/(self.substrate_ratio_R102.iloc[i]*self.rho + self.inoculum_ratio_R102.iloc[i]*self.rho_ini_R102)
                if not pd.isna(self.SV_ini_R102):
                    OM_int_SV_R102.append(self.SV_ini_R102)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (SVR102).")
                            OM_int_SV_R102.append(self.SV_ini_R102_res)
                        else:
                            OM_int_SV_R102.append(self.TrainMode["SV_exp_R102"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (SVR102).")
                        OM_int_SV_R102.append(self.SV_ini_R102_res)
                OM_in_SV_R102.append(self.mass_in_R102)
                # Mass balance in grams for total solids
                self.mass_ini_ST_R102 = (self.ST_ini_R102 * 30 * (self.substrate_ratio_R102.iloc[i]*self.rho + self.inoculum_ratio_R102.iloc[i]*self.rho_ini_R102))
                self.mass_in_ST_R102 = ((self.ST_ini_R101) * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outl_ST_R102 = (self.ST_ini_R102 * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outg_ST_R102 = self.dwbio_dt_R102.iloc[i]
                self.ST_ini_R102 = (self.mass_ini_ST_R102 + self.mass_in_ST_R102 - self.mass_outl_ST_R102 - self.mass_outg_ST_R102)/30/(self.substrate_ratio_R102.iloc[i]*self.rho + self.inoculum_ratio_R102.iloc[i]*self.rho_ini_R102)
                if not pd.isna(self.ST_ini_R102):
                    OM_int_ST_R102.append(self.ST_ini_R102)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (STR102).")
                            OM_int_ST_R102.append(self.ST_ini_R102_res)
                        else:
                            OM_int_ST_R102.append(self.TrainMode["ST_exp_R102"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (STR102).")
                        OM_int_ST_R102.append(self.ST_ini_R102_res)
                OM_in_ST_R102.append(self.mass_in_ST_R102)
                # Mass balance in mol volatile solids
                self.mol_ini_R102 = (self.Csus_ini_SV_R102 * 30)
                self.mol_in_R102 = (self.Csus_ini_SV_R101 * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60))
                self.mol_outl_R102 = (self.Csus_ini_SV_R102 * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60))
                self.mol_outg_R102 = self.dnCH4_dt_R102.iloc[i]*(1/(self.substrate_ratio_R102.iloc[i]*self.s_CH4 + self.inoculum_ratio_R102.iloc[i]*self.s_CH4_ini_R102))
                self.Csus_ini_SV_R102 = (self.mol_ini_R102 + self.mol_in_R102 - self.mol_outl_R102 - self.mol_outg_R102)/30
                if not pd.isna(self.Csus_ini_SV_R102):
                    mol_int_R102.append(self.Csus_ini_SV_R102)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (STR102).")
                            mol_int_R102.append(self.Csus_ini_SV_R102_res)
                        else:
                            mol_int_R102.append(self.TrainMode["Csus_exp"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (STR102).")
                        mol_int_R102.append(self.ST_ini_R102_res)
                mol_in_R102.append(self.mol_in_R102)

                #Rest of variable for match lenght
                normal_time.append(self.DataPlant["normal_time"].iloc[i])
                T_R101.append(self.DataPlant["Tprom_R101"].iloc[i])
                T_R102.append(self.DataPlant["Tprom_R102"].iloc[i])
                Q_P104.append(self.DataPlant["P104"].iloc[i])
                Q_P101.append(self.DataPlant["P101"].iloc[i])
                mass_out_R101.append(self.dwbio_dt_R101.iloc[i])
                mass_out_R102.append(self.dwbio_dt_R102.iloc[i])


            self.TrainMode = pd.DataFrame({"time": normal_time,
                                        "SV_exp_R101": OM_int_SV_R101,
                                        "VS_in_R101": OM_in_SV_R101,
                                        "ST_exp_R101": OM_int_ST_R101,
                                        "TS_in_R101": OM_in_ST_R101,
                                        "Csus_exp_R101": mol_int_R101,
                                        "mol_org_in_exp": mol_in_R101,
                                        "mass_out_R101": mass_out_R101,
                                        "T_R101": T_R101,
                                        "SV_exp_R102": OM_int_SV_R102,
                                        "VS_in_R102": OM_in_SV_R102,
                                        "ST_exp_R102": OM_int_ST_R102,
                                        "TS_in_R102": OM_in_ST_R102,
                                        "Csus_exp_R102": mol_int_R102,
                                        "mol_org_in_exp": mol_in_R102,
                                        "mass_out_R102": mass_out_R102,
                                        "T_R102":T_R102,
                                        "Q_P104":Q_P104,
                                        "Q_P101":Q_P101
                                        })

            self.TrainMode["Vol_R101"] = 30
            self.TrainMode["Vol_R102"] = 70
            self.TrainMode["Csus_in_R101"] = self.Csv_sus

            self.x_R101 = (self.TrainMode["Csus_in_R101"] - self.TrainMode["Csus_exp_R101"])/self.TrainMode["Csus_in_R101"]
            self.x_R102 = (self.TrainMode["Csus_exp_R101"] - self.TrainMode["Csus_exp_R102"])/self.TrainMode["Csus_exp_R101"]

            if self.Model == "Gompertz":
                V_acum_Gompertz_V101 = self.DataPlant["Vacum_V101"]
                if V_acum_Gompertz_V101.iloc[0]>0:
                    max_value_Vacum_gompertz_V101 = max(V_acum_Gompertz_V101)
                    V_acum_Gompertz_V101 = V_acum_Gompertz_V101 - max_value_Vacum_gompertz_V101
                V_acum_Gompertz_V102 = self.DataPlant["Vacum_V102"]
                if V_acum_Gompertz_V102.iloc[0]>0:
                    max_value_Vacum_gompertz_V102 = max(V_acum_Gompertz_V102)
                    V_acum_Gompertz_V102 = V_acum_Gompertz_V102 - max_value_Vacum_gompertz_V102

                self.V_bio_Gompertz_R101 = V_acum_Gompertz_V101/self.mass_ini_R101      #gompertz exit Lbio/gSV
                self.V_bio_Gompertz_R102 = V_acum_Gompertz_V102/self.mass_ini_R102      #gompertz exit Lbio/gSV
                self.TrainMode_gompertz = pd.DataFrame({"time": self.DataPlant["normal_time"],
                                                        "y_t_exp_R101": self.V_bio_Gompertz_R101,
                                                        "y_t_exp_R102": self.V_bio_Gompertz_R102,
                                                        "Vacum_V101": V_acum_Gompertz_V101,
                                                        "Vacum_V102": V_acum_Gompertz_V102})
            
            self.global_time = self.global_time + (10/1440)
            self.OC_R101 = self.SV_ini_R101/self.global_time
                
        else:   #Operation in mode 4
            #Compounds by mol V101 
            # Accumulated
            self.biogas_mol_V101_acum = ((self.DataPlant["Pacum_V101"]*6894.76)*self.Volume_V101/1000)/(8.314*(self.DataPlant["T_V101"]+273.15))
            self.biogas_mol_V101_acum.ffill(inplace=True)
            self.biogas_mol_V101_acum.bfill(inplace=True)
            self.biogas_mol_V101_acum_NN = self.biogas_mol_V101_acum
            if self.biogas_mol_V101_acum.iloc[0]>0:
                nbiogas_max_value_V101 = max(self.biogas_mol_V101_acum)
                self.biogas_mol_V101_acum = self.biogas_mol_V101_acum - nbiogas_max_value_V101
            self.nCH4_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xCH4_V101_filled"]/100
            self.nCO2_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xCO2_V101_filled"]/100
            self.nO2_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xO2_V101_filled"]/100
            self.nH2S_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xH2S_V101_filled"]/1000000
            self.nH2_V101_acum = self.biogas_mol_V101_acum * self.DataPlant["xH2_V101_filled"]/1000000
            self.nNH3_V101_acum = self.nCH4_V101_acum * (self.s_NH3/self.s_CH4)
            #Accumulated (g)
            self.wCH4_V101_acum = self.nCH4_V101_acum * 16.04
            self.wCO2_V101_acum = self.nCO2_V101_acum * 44.009
            self.wO2_V101_acum = self.nO2_V101_acum * 32
            self.wH2S_V101_acum = self.nH2S_V101_acum * 34.082
            self.wH2_V101_acum = self.nH2_V101_acum * 2
            self.wNH3_V101_acum = self.nNH3_V101_acum * 17.031
             # Storaged
            self.biogas_mol_V101 = ((self.DataPlant["P_V101"]*6894.76) * self.Volume_V101/1000)/(8.314*(self.DataPlant["T_V101"]+273.15))
            self.nCH4_V101 = self.biogas_mol_V101 * self.DataPlant["xCH4_V101_filled"]/100
            self.nCO2_V101 = self.biogas_mol_V101 * self.DataPlant["xCO2_V101_filled"]/100
            self.nO2_V101 = self.biogas_mol_V101 * self.DataPlant["xO2_V101_filled"]/100
            self.nH2S_V101 = self.biogas_mol_V101 * self.DataPlant["xH2S_V101_filled"]/1000000
            self.nH2_V101 = self.biogas_mol_V101 * self.DataPlant["xH2_V101_filled"]/1000000
            self.nNH3_V101 = self.nCH4_V101 * (self.s_NH3/self.s_CH4)
            
            #Compound by mol V102
            #Accumulated (mol)
            self.biogas_mol_V102_acum = ((self.DataPlant["Pacum_V102"]*6894.76)*self.Volume_V102/1000)/(8.314*(self.DataPlant["T_V102"]+273.15))
            self.biogas_mol_V102_acum.ffill(inplace=True)
            self.biogas_mol_V102_acum.bfill(inplace=True)
            self.biogas_mol_V102_acum_NN = self.biogas_mol_V102_acum
            if self.biogas_mol_V102_acum.iloc[0]>0:
                nbiogas_max_value_V102 = max(self.biogas_mol_V102_acum)
                self.biogas_mol_V102_acum = self.biogas_mol_V102_acum - nbiogas_max_value_V102
            self.nCH4_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xCH4_V102_filled"]/100
            self.nCO2_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xCO2_V102_filled"]/100
            self.nO2_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xO2_V102_filled"]/100
            self.nH2S_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xH2S_V102_filled"]/1000000
            self.nH2_V102_acum = self.biogas_mol_V102_acum * self.DataPlant["xH2_V102_filled"]/1000000
            self.nNH3_V102_acum = self.nCH4_V102_acum * (self.s_NH3/self.s_CH4)
            #Accumulated (g)
            self.wCH4_V102_acum = self.nCH4_V102_acum * 16.04
            self.wCO2_V102_acum = self.nCO2_V102_acum * 44.009
            self.wO2_V102_acum = self.nO2_V102_acum * 32
            self.wH2S_V102_acum = self.nH2S_V102_acum * 34.082
            self.wH2_V102_acum = self.nH2_V102_acum * 2
            self.wNH3_V102_acum = self.nNH3_V102_acum * 17.031
            #Storage
            self.biogas_mol_V102 = ((self.DataPlant["P_V102"]*6894.76)*self.Volume_V102/1000)/(8.314*(self.DataPlant["T_V102"]+273.15))
            self.nCH4_V102 = self.biogas_mol_V102 * self.DataPlant["xCH4_V102_filled"]/100
            self.nCO2_V102 = self.biogas_mol_V102 * self.DataPlant["xCO2_V102_filled"]/100
            self.nO2_V102 = self.biogas_mol_V102 * self.DataPlant["xO2_V102_filled"]/100
            self.nH2S_V102 = self.biogas_mol_V102 * self.DataPlant["xH2S_V102_filled"]/1000000
            self.nH2_V102 = self.biogas_mol_V102 * self.DataPlant["xH2_V102_filled"]/1000000
            self.nNH3_V102 = self.nCH4_V102 * (self.s_NH3/self.s_CH4)

            #compound by mol V107
            #Accumulated
            self.biogas_mol_V107_acum = ((self.DataPlant["Pacum_V107"]*6894.76)*self.Volume_V107/1000)/(8.314*(self.DataPlant["T_V107"]+273.15))
            self.nCH4_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xCH4_V107_filled"]/100
            self.nCO2_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xCO2_V107_filled"]/100
            self.nO2_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xO2_V107_filled"]/100
            self.nH2S_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xH2S_V107_filled"]/1000000
            self.nH2_V107_acum = self.biogas_mol_V107_acum * self.DataPlant["xH2_V107_filled"]/1000000
            self.nNH3_V107_acum = self.nCH4_V107_acum * (self.s_NH3/self.s_CH4)
            #Accumulated (g)
            self.wCH4_V107_acum = self.nCH4_V107_acum * 16.04
            self.wCO2_V107_acum = self.nCO2_V107_acum * 44.009
            self.wO2_V107_acum = self.nO2_V107_acum * 32
            self.wH2S_V107_acum = self.nH2S_V107_acum * 34.082
            self.wH2_V107_acum = self.nH2_V107_acum * 2
            self.wNH3_V107_acum = self.nNH3_V107_acum * 17.031
            #Storage
            self.biogas_mol_V107 = ((self.DataPlant["P_V107"]*6894.76)*self.Volume_V107/1000)/(8.314*(self.DataPlant["T_V107"]+273.15))
            self.nCH4_V107 = self.biogas_mol_V107 * self.DataPlant["xCH4_V107_filled"]/100
            self.nCO2_V107 = self.biogas_mol_V107 * self.DataPlant["xCO2_V107_filled"]/100
            self.nO2_V107 = self.biogas_mol_V107 * self.DataPlant["xO2_V107_filled"]/100
            self.nH2S_V107 = self.biogas_mol_V107 * self.DataPlant["xH2S_V107_filled"]/1000000
            self.nH2_V107 = self.biogas_mol_V107 * self.DataPlant["xH2_V107_filled"]/1000000
            self.nNH3_V107 = self.nCH4_V107 * (self.s_NH3/self.s_CH4)

            #R101 mol transformed
            self.dnCH4_dt_R101 = self.nCH4_V101_acum.diff().fillna(0)
            self.dnCO2_dt_R101 = self.nCO2_V101_acum.diff().fillna(0)
            self.dnO2_dt_R101 = self.nO2_V101_acum.diff().fillna(0)
            self.dnH2S_dt_R101 = self.nH2S_V101_acum.diff().fillna(0)
            self.dnH2_dt_R101 = self.nH2_V101_acum.diff().fillna(0)
            self.dnNH3_dt_R101 = self.nNH3_V101_acum.diff().fillna(0)
            self.dnbio_dt_R101 = (self.dnCH4_dt + self.dnCO2_dt + self.dnO2_dt + self.dnH2S_dt + self.dnH2_dt + self.dnNH3_dt)
            #R101 mass trnasformed (gram)
            self.dwCH4_dt_R101 = self.wCH4_V101_acum.diff().fillna(0)
            self.dwCO2_dt_R101 = self.wCO2_V101_acum.diff().fillna(0)
            self.dwO2_dt_R101 = self.wO2_V101_acum.diff().fillna(0)
            self.dwH2S_dt_R101 = self.wH2S_V101_acum.diff().fillna(0)
            self.dwH2_dt_R101 = self.wH2_V101_acum.diff().fillna(0)
            self.dwNH3_dt_R101 = self.wNH3_V101_acum.diff().fillna(0)
            self.dwbio_dt_R101 = (self.dwCH4_dt_R101 + self.dwCO2_dt_R101 + self.dwO2_dt_R101 + self.dwH2S_dt_R101 + self.dwH2_dt_R101 + self.dwNH3_dt_R101)

            #R102 mol transformed
            self.dnCH4_dt_R102 = self.nCH4_V102_acum.diff().fillna(0)
            self.dnCO2_dt_R102 = self.nCO2_V102_acum.diff().fillna(0)
            self.dnO2_dt_R102 = self.nO2_V102_acum.diff().fillna(0)
            self.dnH2S_dt_R102 = self.nH2S_V102_acum.diff().fillna(0)
            self.dnH2_dt_R102 = self.nH2_V102_acum.diff().fillna(0)
            self.dnNH3_dt_R102 = self.nNH3_V102_acum.diff().fillna(0)
            self.dnbio_dt_R102 = (self.dnCH4_dt_R102 + self.dnCO2_dt_R102 + self.dnO2_dt_R102 + self.dnH2S_dt_R102 + self.dnH2_dt_R102 + self.dnNH3_dt_R102)
            #R102 mass trnasformed (gram)
            self.dwCH4_dt_R102 = self.wCH4_V102_acum.diff().fillna(0)
            self.dwCO2_dt_R102 = self.wCO2_V102_acum.diff().fillna(0)
            self.dwO2_dt_R102 = self.wO2_V102_acum.diff().fillna(0)
            self.dwH2S_dt_R102 = self.wH2S_V102_acum.diff().fillna(0)
            self.dwH2_dt_R102 = self.wH2_V102_acum.diff().fillna(0)
            self.dwNH3_dt_R102 = self.wNH3_V102_acum.diff().fillna(0)
            self.dwbio_dt_R102 = (self.dwCH4_dt_R102 + self.dwCO2_dt_R102 + self.dwO2_dt_R102 + self.dwH2S_dt_R102 + self.dwH2_dt_R102 + self.dwNH3_dt_R102)

            #Mass balance
            #Initial values (mass inside reactors)
            try:
                if self.TrainMode.empty:
                    print("The DataFrame exists but is empty.")
                    self.Csus_ini_SV_R101 = self.Csus_ini_SV_R101
                    self.SV_ini_R101 = self.SV_ini_R101
                    self.ST_ini_R101 = self.ST_ini_R101
                    
                    self.Csus_ini_SV_R102 = self.Csus_ini_SV_R102
                    self.SV_ini_R102 = self.SV_ini_R102
                    self.ST_ini_R102 = self.ST_ini_R102 
                else:
                    self.Csus_ini_SV_R101 = self.TrainMode["Csus_exp_R101"].iloc[0]
                    self.SV_ini_R101 = self.TrainMode["SV_exp_R101"].iloc[0]
                    self.ST_ini_R101 = self.TrainMode["ST_exp_R101"].iloc[0]

                    self.Csus_ini_SV_R102 = self.TrainMode["Csus_exp_R102"].iloc[0]
                    self.SV_ini_R102 = self.TrainMode["SV_exp_R102"].iloc[0]
                    self.ST_ini_R102 = self.TrainMode["ST_exp_R102"].iloc[0]
            
            except AttributeError:
                    print("The DataFrame does not exist.")
            
            # dt
            self.tp = self.DataPlant["normal_time"].diff().fillna(0)                       #min
            # Vol inyected in L
            self.Vol_injsus_R101 = self.DataPlant["P104"] * (self.tp/60)                      #Liters
            self.Vol_injsus_R101 = self.Vol_injsus_R101.cumsum()
            self.Vol_injrec_R101 = self.DataPlant["P102"] * (self.tp/60)
            self.Vol_injrec_R101 = self.Vol_injrec_R101.cumsum()

            self.Vol_inj_R102 = self.DataPlant["P101"] * (self.tp/60)
            self.Vol_inj_R102 = self.Vol_inj_R102.cumsum()

            # substrate_inoculum_recycling ratio
            self.substrate_ratio_R101 = (self.Vol_injsus_R101/30).clip(upper=1)
            self.inoculum_ratio_R101 = 1 - self.substrate_ratio_R101
            
            self.substrate_ratio_R102 = (self.Vol_inj_R102/70).clip(upper=1)
            self.inoculum_ratio_R102 = 1 - self.substrate_ratio_R102

            #Time
            normal_time = []
            Q_P104 = []
            Q_P101 = []
            Q_P102 = []

            #Mass Balance R101
            OM_int_SV_R101 = []
            OM_in_SV_R101 = []
            OM_int_ST_R101 = []
            OM_in_ST_R101 = []
            mol_int_R101 = []
            mol_in_R101 = []
            T_R101 = []
            mass_out_R101 = []

            #Mass Balance R102
            OM_int_SV_R102 = []
            OM_in_SV_R102 = []
            OM_int_ST_R102 = []
            OM_in_ST_R102 = []
            mol_int_R102 = []
            mol_in_R102 = []
            T_R102 = []
            mass_out_R102 = []

            for i in range (len(self.DataPlant["time"] - 1)):
                # Mass balance in R101
                #Mass balance in grams for volatile solids
                self.mass_ini_R101 = (self.SV_ini_R101 * 30 * (self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101))
                self.mass_in_R101 = ((self.SV/100) * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho) + ((self.SV_ini_R102) * self.DataPlant["P102"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho_ini_R102)
                self.mass_outl_R101 = (self.SV_ini_R101 * (self.DataPlant["P104"].iloc[i] + self.DataPlant["P102"].iloc[i]) * (self.tp.iloc[i+1]/60) * self.rho)          
                self.mass_outg_R101 = self.dwbio_dt_R101.iloc[i]
                self.SV_ini_R101 = (self.mass_ini_R101 + self.mass_in_R101 - self.mass_outl_R101 - self.mass_outg_R101)/30/(self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101)
                self.Csus_ini_SV_R101_gl = self.SV_ini_R101 * (self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101)
                if not pd.isna(self.SV_ini_R101):
                    OM_int_SV_R101.append(self.SV_ini_R101)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (SVR101).")
                            OM_int_SV_R101.append(self.SV_ini_R101_res)
                        else:
                            OM_int_SV_R101.append(self.TrainMode["SV_exp_R101"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (SVR101).")
                        OM_int_SV_R101.append(self.SV_ini_R101_res)
                OM_in_SV_R101.append(self.mass_in_R101)
                # Mass balance in grams for total solids
                self.mass_ini_ST_R101 = (self.ST_ini_R101 * 30 * (self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101))
                self.mass_in_ST_R101 = ((self.ST/100) * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho) + ((self.ST_ini_R102) * self.DataPlant["P102"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho_ini_R102)
                self.mass_outl_ST_R101 = (self.ST_ini_R101 * (self.DataPlant["P104"].iloc[i]+self.DataPlant["P102"]) * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outg_ST_R101 = self.dwbio_dt_R101.iloc[i]
                self.ST_ini_R101 = (self.mass_ini_ST_R101 + self.mass_in_ST_R101 - self.mass_outl_ST_R101 - self.mass_outg_ST_R101)/30/(self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101)
                self.Csus_ini_ST_R101_gl = self.ST_ini_R101 * (self.substrate_ratio_R101.iloc[i]*self.rho + self.inoculum_ratio_R101.iloc[i]*self.rho_ini_R101)
                if not pd.isna(self.ST_ini_R101):
                    OM_int_ST_R101.append(self.ST_ini_R101)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (STR101).")
                            OM_int_ST_R101.append(self.ST_ini_R101_res)
                        else:
                            OM_int_ST_R101.append(self.TrainMode["ST_exp_R101"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (STR101).")
                        OM_int_ST_R101.append(self.ST_ini_R101_res)
                OM_in_ST_R101.append(self.mass_in_ST_R101)
                # Mass balance in mol volatile solids
                self.mol_ini_R101 = (self.Csus_ini_SV_R101 * 30)
                self.mol_in_R101 = (self.Csv_sus * self.DataPlant["P104"].iloc[i] * (self.tp.iloc[i+1]/60)) + (self.Csus_ini_SV_R102 * self.DataPlant["P102"].iloc[i] * (self.tp.iloc[i+1]/60))
                self.mol_outl_R101 = (self.Csus_ini_SV_R101 * (self.DataPlant["P104"].iloc[i] + self.DataPlant["P101"].iloc[i]) * (self.tp.iloc[i+1]/60))
                self.mol_outg_R101 = self.dnCH4_dt_R101.iloc[i]*(1/(self.substrate_ratio_R101.iloc[i]*self.s_CH4 + self.inoculum_ratio_R101.iloc[i]*self.s_CH4_ini_R101))
                self.Csus_ini_SV_R101 = (self.mol_ini_R101 + self.mol_in_R101 - self.mol_outl_R101 - self.mol_outg_R101)/30
                if not pd.isna(self.Csus_ini_SV_R101):
                    mol_int_R101.append(self.Csus_ini_SV_R101)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (STR101).")
                            mol_int_R101.append(self.Csus_ini_SV_R101_res)
                        else:
                            mol_int_R101.append(self.TrainMode["Csus_exp"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (STR101).")
                        mol_int_R101.append(self.ST_ini_R101_res)
                mol_int_R101.append(self.Csus_ini_SV_R101)

                #Mass balance in R102
                #Mass balance in grams for volatile solids
                self.mass_ini_R102 = (self.SV_ini_R102 * 30 * (self.substrate_ratio_R102.iloc[i]*self.rho + self.inoculum_ratio_R102.iloc[i]*self.rho_ini_R102))
                self.mass_in_R102 = ((self.SV_ini_R101) * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outl_R102 = (self.SV_ini_R102 * (self.DataPlant["P101"].iloc[i]) * (self.tp.iloc[i+1]/60) * self.rho)          #This mass in to R102
                self.mass_outg_R102 = self.dwbio_dt_R102.iloc[i]
                self.SV_ini_R102 = (self.mass_ini_R102 + self.mass_in_R102 - self.mass_outl_R102 - self.mass_outg_R102)/30/(self.substrate_ratio_R102.iloc[i]*self.rho + self.inoculum_ratio_R102.iloc[i]*self.rho_ini_R102)
                if not pd.isna(self.SV_ini_R102):
                    OM_int_SV_R102.append(self.SV_ini_R102)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (SVR102).")
                            OM_int_SV_R102.append(self.SV_ini_R102_res)
                        else:
                            OM_int_SV_R102.append(self.TrainMode["SV_exp_R102"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (SVR102).")
                        OM_int_SV_R102.append(self.SV_ini_R102_res)
                OM_in_SV_R102.append(self.mass_in_R102)
                # Mass balance in grams for total solids
                self.mass_ini_ST_R102 = (self.ST_ini_R102 * 30 * (self.substrate_ratio_R102.iloc[i]*self.rho + self.inoculum_ratio_R102.iloc[i]*self.rho_ini_R102))
                self.mass_in_ST_R102 = ((self.ST_ini_R101) * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outl_ST_R102 = (self.ST_ini_R102 * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60) * self.rho)
                self.mass_outg_ST_R102 = self.dwbio_dt_R102.iloc[i]
                self.ST_ini_R102 = (self.mass_ini_ST_R102 + self.mass_in_ST_R102 - self.mass_outl_ST_R102 - self.mass_outg_ST_R102)/30/(self.substrate_ratio_R102.iloc[i]*self.rho + self.inoculum_ratio_R102.iloc[i]*self.rho_ini_R102)
                if not pd.isna(self.ST_ini_R102):
                    OM_int_ST_R102.append(self.ST_ini_R102)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (STR102).")
                            OM_int_ST_R102.append(self.ST_ini_R102_res)
                        else:
                            OM_int_ST_R102.append(self.TrainMode["ST_exp_R102"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (STR102).")
                        OM_int_ST_R102.append(self.ST_ini_R102_res)
                OM_in_ST_R102.append(self.mass_in_ST_R102)
                # Mass balance in mol volatile solids
                self.mol_ini_R102 = (self.Csus_ini_SV_R102 * 30)
                self.mol_in_R102 = (self.Csus_ini_SV_R101 * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60))
                self.mol_outl_R102 = (self.Csus_ini_SV_R102 * self.DataPlant["P101"].iloc[i] * (self.tp.iloc[i+1]/60))
                self.mol_outg_R102 = self.dnCH4_dt_R102.iloc[i]*(1/(self.substrate_ratio_R102.iloc[i]*self.s_CH4 + self.inoculum_ratio_R102.iloc[i]*self.s_CH4_ini_R102))
                self.Csus_ini_SV_R102 = (self.mol_ini_R102 + self.mol_in_R102 - self.mol_outl_R102 - self.mol_outg_R102)/30
                if not pd.isna(self.Csus_ini_SV_R102):
                    mol_int_R102.append(self.Csus_ini_SV_R102)
                else:
                    try:
                        if self.TrainMode.empty:
                            print("Error with the calculos of interal concentration (STR102).")
                            mol_int_R102.append(self.Csus_ini_SV_R102_res)
                        else:
                            mol_int_R102.append(self.TrainMode["Csus_exp"].iloc[0])
                    except AttributeError:
                        print("Error with the calculos of interal concentration (STR102).")
                        mol_int_R102.append(self.ST_ini_R102_res)
                mol_in_R102.append(self.mol_in_R102)

                #Rest of variable for match lenght
                normal_time.append(self.DataPlant["normal_time"].iloc[i])
                T_R101.append(self.DataPlant["Tprom_R101"].iloc[i])
                T_R102.append(self.DataPlant["Tprom_R102"].iloc[i])
                Q_P104.append(self.DataPlant["P104"].iloc[i])
                Q_P101.append(self.DataPlant["P101"].iloc[i])
                Q_P102.append(self.DataPlant["P102"].iloc[i])
                mass_out_R101.append(self.dwbio_dt_R101.iloc[i])
                mass_out_R102.append(self.dwbio_dt_R102.iloc[i])
            
            self.TrainMode = pd.DataFrame({"time": normal_time,
                                        "SV_exp_R101": OM_int_SV_R101,
                                        "VS_in_R101": OM_in_SV_R101,
                                        "ST_exp_R101": OM_int_ST_R101,
                                        "TS_in_R101": OM_in_ST_R101,
                                        "Csus_exp_R101": mol_int_R101,
                                        "mol_org_in_exp": mol_in_R101,
                                        "mass_out_R101": mass_out_R101,
                                        "T_R101":T_R101,
                                        "SV_exp_R102": OM_int_SV_R102,
                                        "VS_in_R102": OM_in_SV_R102,
                                        "ST_exp_R102": OM_int_ST_R102,
                                        "TS_in_R102": OM_in_ST_R102,
                                        "Csus_exp_R102": mol_int_R102,
                                        "mol_org_in_exp": mol_in_R102,
                                        "mass_out_R102": mass_out_R102,
                                        "T_R102":T_R102,
                                        "Q_P104":Q_P104,
                                        "Q_P101":Q_P101,
                                        "Q_P102":Q_P102,
                                        })

            self.TrainMode["Vol_R101"] = 30
            self.TrainMode["Vol_R102"] = 70
            self.TrainMode["Csus_in_R101"] = self.Csv_sus

            self.x_R101 = (self.TrainMode["Csus_in_R101"] - self.TrainMode["Csus_exp_R101"])/self.TrainMode["Csus_in_R101"]
            self.x_R102 = (self.TrainMode["Csus_exp_R101"] - self.TrainMode["Csus_exp_R102"])/self.TrainMode["Csus_exp_R101"]

            if self.Model == "Gompertz":
                V_acum_Gompertz_V101 = self.DataPlant["Vacum_V101"]
                if V_acum_Gompertz_V101.iloc[0]>0:
                    max_value_Vacum_gompertz_V101 = max(V_acum_Gompertz_V101)
                    V_acum_Gompertz_V101 = V_acum_Gompertz_V101 - max_value_Vacum_gompertz_V101
                V_acum_Gompertz_V102 = self.DataPlant["Vacum_V102"]
                if V_acum_Gompertz_V102.iloc[0]>0:
                    max_value_Vacum_gompertz_V102 = max(V_acum_Gompertz_V102)
                    V_acum_Gompertz_V102 = V_acum_Gompertz_V102 - max_value_Vacum_gompertz_V102
                
                self.V_bio_Gompertz_R101 = V_acum_Gompertz_V101/self.mass_ini_R101      #gompertz exit Lbio/gSV
                self.V_bio_Gompertz_R102 = V_acum_Gompertz_V102/self.mass_ini_R102      #gompertz exit Lbio/gSV
                self.TrainMode_gompertz = pd.DataFrame({"time": self.DataPlant["normal_time"],
                                                        "y_t_exp_R101": self.V_bio_Gompertz_R101,
                                                        "y_t_exp_R102": self.V_bio_Gompertz_R102,
                                                        "Vacum_V101": V_acum_Gompertz_V101,
                                                        "Vacum_V102": V_acum_Gompertz_V102})
            
            self.global_time = self.global_time + (10/1440)
            self.OC_R101 = self.SV_ini_R101/self.global_time
    
    # def OptimizationArrhenius(self, resolution):
    
    #     def model_Arrhenius(C, t, K, Ea, t_array, VR_vec, T_vec, Q1_vec, Q2_vec, Csus1_vec, Csus2_vec, Operation):
    #         idx = np.searchsorted(t_array, t, side='right') - 1
    #         idx = max(min(idx, len(t_array) - 1), 0)
    #         R = 8.314
    #         T_val = T_vec[idx]
    #         Q1_val = Q1_vec[idx]
    #         Q2_val = Q2_vec[idx]
    #         Csus1_val = Csus1_vec[idx]
    #         Csus2_val = Csus2_vec[idx]
    #         VR_val = VR_vec[idx]

    #         if Operation == 1:
    #             return ((Q1_val / VR_val) * (Csus1_val - C)) - (C * K * np.exp(-Ea / (R * T_val))) / VR_val
    #         elif Operation == 2:
    #             return (Q1_val * Csus1_val + Q2_val * Csus2_val - (Q1_val + Q2_val) * C - C * K * np.exp(-Ea / (R * T_val))) / VR_val
    #         elif Operation == 3:
    #             return (Q1_val * Csus1_val + Q2_val * C - Q1_val * C - C * K * np.exp(-Ea / (R * T_val))) / VR_val
    #         return 0

    #     def Optimization(t, C_exp, y0, VR, temperatures, Qi1, Csus_in_i1, Qi2, Csus_in_i2, Operation, K_init, Ea_init):
    #         t = np.array(t)
    #         C_exp = np.array(C_exp)
    #         y0 = float(y0)

    #         T_vec = np.interp(t, t, temperatures)
    #         Q1_vec = np.interp(t, t, Qi1)
    #         Q2_vec = np.interp(t, t, Qi2)
    #         VR_vec = np.interp(t, t, VR)
    #         Csus1_vec = np.interp(t, t, Csus_in_i1)
    #         Csus2_vec = np.interp(t, t, Csus_in_i2)

    #         def objective(params):
    #             K, Ea = params
    #             try:
    #                 C_model = odeint(model_Arrhenius, y0, t, args=(K, Ea, t, VR_vec, T_vec, Q1_vec, Q2_vec, Csus1_vec, Csus2_vec, Operation)).flatten()
    #                 return np.sum((C_exp - C_model) ** 2)
    #             except Exception:
    #                 return 1e10

    #         bounds = [(1e-5, 1e5), (1000, 200000)]
    #         result = minimize(objective, [K_init, Ea_init], method='L-BFGS-B', bounds=bounds)
    #         return result

    #     # Preparar datos comunes
    #     t_exp = (self.TrainMode["time"] * 60).tolist()
    #     T_R101 = (self.TrainMode["T_R101"] + 273.15).tolist()
    #     Q_P104 = (self.TrainMode["Q_P104"] / 60).tolist()
    #     K_R101, Ea_R101, Error_R101 = [], [], []

    #     if self.Operation_mode in [1, 2]:
    #         C_exp = self.TrainMode["Csus_exp"].tolist()
    #         VR_exp = self.TrainMode["Vol"].tolist()
    #         Csus_in = self.TrainMode["Csus_in_R101"].tolist()
    #         for i in range(len(t_exp) - resolution + 1):
    #             try:
    #                 res = Optimization(
    #                     t_exp[i:i+resolution], C_exp[i:i+resolution], C_exp[i],
    #                     VR_exp[i:i+resolution], T_R101[i:i+resolution],
    #                     Q_P104[i:i+resolution], Csus_in[i:i+resolution],
    #                     Q_P104[i:i+resolution], Csus_in[i:i+resolution],
    #                     1, self.K_ini_Arr_R101, self.Ea_ini_R101
    #                 )
    #                 K_R101.append(res.x[0])
    #                 Ea_R101.append(res.x[1])
    #                 Error_R101.append(res.fun)
    #             except Exception:
    #                 continue
    #         self.K_mean_R101 = st.mean(K_R101)
    #         self.Ea_mean_R101 = st.mean(Ea_R101)

    #     elif self.Operation_mode in [3, 5, 4]:
    #         C_exp_R101 = self.TrainMode["Csus_exp_R101"].tolist()
    #         VR_exp_R101 = self.TrainMode["Vol_R101"].tolist()
    #         Csus_in_R101 = self.TrainMode["Csus_in_R101"].tolist()
    #         C_exp_R102 = self.TrainMode["Csus_exp_R102"].tolist()
    #         VR_exp_R102 = self.TrainMode["Vol_R102"].tolist()
    #         T_R102 = (self.TrainMode["T_R102"] + 273.15).tolist()
    #         Q_P101 = (self.TrainMode["Q_P101"] / 60).tolist()
    #         Q_P102 = (self.TrainMode["Q_P102"] / 60).tolist() if "Q_P102" in self.TrainMode.columns else Q_P101
    #         K_R102, Ea_R102, Error_R102 = [], [], []

    #         for i in range(len(t_exp) - resolution + 1):
    #             # R101
    #             try:
    #                 res1 = Optimization(
    #                     t_exp[i:i+resolution], C_exp_R101[i:i+resolution], C_exp_R101[i],
    #                     VR_exp_R101[i:i+resolution], T_R101[i:i+resolution],
    #                     Q_P104[i:i+resolution], Csus_in_R101[i:i+resolution],
    #                     Q_P102[i:i+resolution] if self.Operation_mode == 4 else Q_P104[i:i+resolution],
    #                     C_exp_R102[i:i+resolution] if self.Operation_mode == 4 else Csus_in_R101[i:i+resolution],
    #                     2 if self.Operation_mode == 4 else 1,
    #                     self.K_ini_Arr_R101, self.Ea_ini_R101
    #                 )
    #                 K_R101.append(res1.x[0])
    #                 Ea_R101.append(res1.x[1])
    #                 Error_R101.append(res1.fun)
    #             except Exception:
    #                 continue

    #             # R102
    #             try:
    #                 res2 = Optimization(
    #                     t_exp[i:i+resolution], C_exp_R102[i:i+resolution], C_exp_R102[i],
    #                     VR_exp_R102[i:i+resolution], T_R102[i:i+resolution],
    #                     Q_P101[i:i+resolution], C_exp_R101[i:i+resolution],
    #                     Q_P101[i:i+resolution], Csus_in_R101[i:i+resolution],
    #                     1, self.K_ini_Arr_R102, self.Ea_ini_R102
    #                 )
    #                 K_R102.append(res2.x[0])
    #                 Ea_R102.append(res2.x[1])
    #                 Error_R102.append(res2.fun)
    #             except Exception:
    #                 continue

    #         self.K_mean_R101 = st.mean(K_R101)
    #         self.Ea_mean_R101 = st.mean(Ea_R101)
    #         self.K_mean_R102 = st.mean(K_R102)
    #         self.Ea_mean_R102 = st.mean(Ea_R102)

    #         # self.Optimized_parameters = pd.DataFrame({
    #         #     "time": self.TrainMode["time"],
    #         #     "K_R101": K_R101 + [None] * (len(self.TrainMode["time"]) - len(K_R101)),
    #         #     "Ea_R101": Ea_R101 + [None] * (len(self.TrainMode["time"]) - len(Ea_R101)),
    #         #     "K_R102": K_R102 + [None] * (len(self.TrainMode["time"]) - len(K_R102)),
    #         #     "Ea_R102": Ea_R102 + [None] * (len(self.TrainMode["time"]) - len(Ea_R102))
    #         # })

    
    def OptimizationArrhenius (self, resolution):
        """
        Perform parameter optimization for Arrhenius model (K, Ea) based on selected operation mode.
        
        Parameters:
            Operation_mode (int): Mode of operation (1, 2, or 3).
            resolution (int): Number of data points used in each optimization window.
        """
        
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
                
                C_model = odeint(model_Arrhenius, y0, t, args = (K, Ea, VR_func, T_func, Q_func1, Q_func2, Csus_in1, Csus_in2, Operation), rtol=1e-4, atol=1e-6).flatten()

                squared_diff = np.sum((C_exp - C_model) ** 2)
                return squared_diff
            
            result = minimize(objective, [K, Ea], method = 'Nelder-Mead')
            return result
        
        if self.Operation_mode == 1 or self.Operation_mode == 2:
            t_exp = (self.TrainMode["time"]).tolist()      #minutes
            C_exp = self.TrainMode["Csus_exp"].tolist()    #Kmol/m3 = mol/L
            VR_exp = self.TrainMode["Vol"].tolist()        #L 
            Csus_in = self.TrainMode["Csus_in_R101"].to_list()  #mol/L
            T_R101 = (self.TrainMode["T_R101"]+273.15).tolist()  #K     
            Q_P104 = (self.TrainMode["Q_P104"]/60).tolist()    #L/min 
            
            K = []
            Ea = []
            Error = []
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt = C_exp[i : i+resolution]
                VR_exp_opt = VR_exp[i : i+resolution]
                T_R101_opt = T_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                Csus_in_opt = Csus_in[i : i + resolution]

                try:
                    Opt_kinetic_params = Optimization(t = t_exp_opt, C_exp = C_exp_opt, y0 = C_exp_opt[0], VR = VR_exp_opt,
                                                    temperatures = T_R101_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt,
                                                    Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_opt, Operation = 1, K = self.K_ini_Arr_R101, Ea = self.Ea_ini_R101)
                    K.append(Opt_kinetic_params.x[0])
                    Ea.append(Opt_kinetic_params.x[1])
                    Error.append(Opt_kinetic_params.fun)
                except Exception as e:
                    print(e)
                    continue
                # self.K_ini_Arr_R101 = st.mean(K)
                # self.Ea_ini_Arr_R101 = st.mean(Ea)
                # print("Pre_exponentialfactor", Opt_kinetic_params.x[0], "Activation Energy", Opt_kinetic_params.x[1], "Error", Opt_kinetic_params.fun)
            
            self.K_mean_R101 = st.mean(K)
            self.Ea_mean_R101 = st.mean(Ea)

            # self.Optimized_parameters = pd.DataFrame({"time": self.TrainMode["time"],
            #                                         "K_R101": K,
            #                                         "Ea_R101": Ea,
            #                                         "Error": Error})
        
        elif self.Operation_mode in [3,5]:
            t_exp = (self.TrainMode["time"]).tolist()                #minutes
            C_exp_R101 = self.TrainMode["Csus_exp_R101"].tolist()    #Kmol/m3 = mol/L
            VR_exp_R101 = self.TrainMode["Vol_R101"].tolist()        #L 
            Csus_in_R101 = self.TrainMode["Csus_in_R101"].to_list()  #mol/L
            C_exp_R102 = self.TrainMode["Csus_exp_R102"].tolist()    #mol/L
            VR_exp_R102 = self.TrainMode["Vol_R102"].tolist()        #L
            T_R101 = (self.TrainMode["T_R101"]+273.15).tolist()  #K   
            T_R102 = (self.TrainMode["T_R102"]+273.154).tolist() #K   
            Q_P104 = (self.TrainMode["Q_P104"]/60).tolist()    #L/min 
            Q_P101 = (self.TrainMode["Q_P101"]/60).tolist()    #L/min

            K_R101 = []
            Ea_R101 = []
            Error_R101 = []
            
            K_R102 = []
            Ea_R102 = []
            Error_R102 = []
            

            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt_R101 = C_exp_R101[i : i+resolution]
                VR_exp_opt_R101 = VR_exp_R101[i : i+resolution]
                Csus_in_opt_R101 = Csus_in_R101[i : i+resolution]
                T_opt_R101 = T_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                
                C_exp_opt_R102 = C_exp_R102[i : i+resolution]
                VR_exp_opt_R102 = VR_exp_R102[i : i+resolution]
                T_opt_R102 = T_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]

                try:
                    Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_opt_R101, y0 = float(C_exp_opt_R101[0]), VR = VR_exp_opt_R101,
                                                    temperatures = T_opt_R101, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt_R101,
                                                    Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_opt_R101, Operation = 1, K = self.K_ini_Arr_R101, Ea = self.Ea_ini_R101)
                    
                    K_R101.append(Opt_kinetic_params_R101.x[0])
                    Ea_R101.append(Opt_kinetic_params_R101.x[1])
                    Error_R101.append(Opt_kinetic_params_R101.fun)
                except Exception as e:
                    continue
                try:
                    Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_opt_R102, y0 = C_exp_opt_R102[0], VR = VR_exp_opt_R102,
                                                    temperatures = T_opt_R102, Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_opt_R101,
                                                    Qi2 = Q_P101_opt, Csus_in_i2 = Csus_in_opt_R101, Operation = 1, K = self.K_ini_Arr_R102, Ea = self.Ea_ini_R102)
                    
                    K_R102.append(Opt_kinetic_params_R102.x[0])
                    Ea_R102.append(Opt_kinetic_params_R102.x[1])
                    Error_R102.append(Opt_kinetic_params_R102.fun)
                except Exception as e:
                    continue
            
            self.K_mean_R101 = st.mean(K_R101)
            self.Ea_mean_R101 = st.mean(Ea_R101)

            self.K_mean_R102 = st.mean(K_R102)
            self.Ea_mean_R102 = st.mean(Ea_R102)


            # self.Optimized_parameters = pd.DataFrame({"time": self.TrainMode["time"],
            #                                     "K_R101": K_R101,
            #                                     "Ea_R101": Ea_R101,
            #                                     "Error_R101": Error_R101,
            #                                     "K_R102": K_R102,
            #                                     "Ea_R102": Ea_R102,
            #                                     "Error_R102": Error_R102})
            
        else:  #Operation Mode 4
            t_exp = (self.TrainMode["time"]).tolist()   #seconds
            C_exp_R101 = self.TrainMode["Csus_exp_R101"].tolist()    #Kmol/m3 = mol/L
            VR_exp_R101 = self.TrainMode["Vol_R101"].tolist()        #L 
            Csus_in_R101 = self.TrainMode["Csus_in_R101"].to_list()  #mol/L
            C_exp_R102 = self.TrainMode["Csus_exp_R102"].tolist()    #mol/L
            VR_exp_R102 = self.TrainMode["Vol_R102"].tolist()        #L
            T_R101 = (self.TrainMode["T_R101"]+273.15).tolist()  #K   
            T_R102 = (self.TrainMode["T_R102"]+273.154).tolist() #K   
            Q_P104 = (self.TrainMode["Q_P104"]/60).tolist()    #L/min 
            Q_P101 = (self.TrainMode["Q_P101"]/60).tolist()    #L/min
            Q_P102 = (self.TrainMode["Q_P102"]/60).tolist()    #L/min

            K_R101 = []
            Ea_R101 = []
            Error_R101 = []

            K_R102 = []
            Ea_R102 = []
            Error_R102 = []

            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt_R101 = C_exp_R101[i : i+resolution]
                VR_exp_opt_R101 = VR_exp_R101[i : i+resolution]
                Csus_in_opt_R101 = Csus_in_R101[i : i+resolution]
                T_opt_R101 = T_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                Q_P102_opt = Q_P102[i : i+resolution]
                
                C_exp_opt_R102 = C_exp_R102[i : i+resolution]
                VR_exp_opt_R102 = VR_exp_R102[i : i+resolution]
                T_opt_R102 = T_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]

                try:
                    Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_opt_R101, y0 = C_exp_opt_R101[0], VR = VR_exp_opt_R101,
                                                    temperatures = T_opt_R101, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt_R101,
                                                    Qi2 = Q_P102_opt, Csus_in_i2 = C_exp_opt_R102, Operation = 2, K = self.K_ini_Arr_R101, Ea = self.Ea_ini_R101)
                    

                    K_R101.append(Opt_kinetic_params_R101.x[0])
                    Ea_R101.append(Opt_kinetic_params_R101.x[1])
                    Error_R101.append(Opt_kinetic_params_R101.fun)
                except Exception as e:
                    continue
                
                try:
                    Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_opt_R102, y0 = C_exp_opt_R102[0], VR = VR_exp_opt_R102,
                                                    temperatures = T_opt_R102, Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_opt_R101,
                                                    Qi2 = Q_P101_opt, Csus_in_i2 = Csus_in_opt_R101, Operation = 1, K = self.K_ini_Arr_R102, Ea = self.Ea_ini_R102)
                    
                    K_R102.append(Opt_kinetic_params_R102.x[0])
                    Ea_R102.append(Opt_kinetic_params_R102.x[1])
                    Error_R102.append(Opt_kinetic_params_R102.fun)
                except Exception as e:
                    continue

            self.K_ini_Arr_R101 = st.mean(K_R101)
            self.Ea_ini_R102 = st.mean(Ea_R101)

            self.K_ini_Arr_R102 = st.mean(K_R102)
            self.Ea_ini_R102 = st.mean(Ea_R102)


            # self.Optimized_parameters = pd.DataFrame({"time": self.TrainMode["time"],
            #                                     "K_R101": K_R101,
            #                                     "Ea_R101": Ea_R101,
            #                                     "K_R102": K_R102,
            #                                     "Ea_R102": Ea_R102})
    def OptimizationADM1(self, resolution):
        
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
                K = params[0]
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
        
        if self.Operation_mode in [1,2]:
            t_exp = (self.TrainMode["time"]).tolist()      #minutes
            C_exp = self.TrainMode["Csus_exp"].tolist()    #Kmol/m3 = mol/L
            VR_exp = self.TrainMode["Vol"].tolist()        #L 
            Csus_in = self.TrainMode["Csus_in_R101"].to_list()  #mol/L     
            Q_P104 = (self.TrainMode["Q_P104"]/60).tolist()    #L/min 
            
            K = []
            Error = []
            
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt = C_exp[i : i+resolution]
                VR_exp_opt = VR_exp[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                Csus_in_opt = Csus_in[i : i + resolution]
                # print("y0:", C_exp_opt[0])
                # print("t:", t_exp[i : i+resolution])
                # print("K:", self.K_ini_ADM1_R101)
                # print("VR_func:", VR_exp_opt)
                # print("Q_func1:", Q_P104_opt)
                # print("Q_func2:", Q_P104_opt)
                # print("Csus_in1:", Csus_in_opt)
                # print("Csus_in2:", Csus_in_opt)
                # print("Operation:", 1)
                time.sleep(0.001)

                try:
                    Opt_kinetc_params = Optimization(t = t_exp_opt, C_exp = C_exp_opt, y0 = C_exp_opt[0], VR = VR_exp_opt, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt, 
                                                    Qi2 = Q_P104_opt, Csus_in_i2 = Csus_in_opt, Operation = 1, K = self.K_ini_ADM1_R101)
                
                    K.append(Opt_kinetc_params.x[0])
                    Error.append(Opt_kinetc_params.fun)
                except Exception as e:
                    continue
            
            self.K_ini_ADM1_R101 = float(st.mean(K))
            # self.Optimized_parameters = pd.DataFrame({"time": self.TrainMode["time"],
            #                                         "K_R101": K,
            #                                         "Error": Error})
        
        elif self.Operation_mode in [3, 5]:
            t_exp = (self.TrainMode["time"]).tolist()                #minutes
            C_exp_R101 = self.TrainMode["Csus_exp_R101"].tolist()    #Kmol/m3 = mol/L
            VR_exp_R101 = self.TrainMode["Vol_R101"].tolist()        #L 
            Csus_in_R101 = self.TrainMode["Csus_in_R101"].to_list()  #mol/L
            C_exp_R102 = self.TrainMode["Csus_exp_R102"].tolist()    #mol/L
            VR_exp_R102 = self.TrainMode["Vol_R102"].tolist()        #L   
            Q_P104 = (self.TrainMode["Q_P104"]/60).tolist()    #L/min 
            Q_P101 = (self.TrainMode["Q_P101"]/60).tolist()    #L/min

            K_R101 = []
            Error_R101 = []
            
            K_R102 = []
            Error_R102 = []
            
            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt_R101 = C_exp_R101[i : i+resolution]
                VR_exp_opt_R101 = VR_exp_R101[i : i+resolution]
                Csus_in_opt_R101 = Csus_in_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                
                C_exp_opt_R102 = C_exp_R102[i : i+resolution]
                VR_exp_opt_R102 = VR_exp_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]

                try:
                    Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_opt_R101, y0 = C_exp_opt_R101[0], VR = VR_exp_opt_R101, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt_R101,
                                                        Qi2 = Q_P104_opt, Csus_in_i2 = C_exp_opt_R101, Operation = 1, K = self.K_ini_ADM1_R101)
                    
                    K_R101.append(Opt_kinetic_params_R101.x[0])
                    Error_R101.append(Opt_kinetic_params_R101.fun)
                except Exception as e:
                    continue
                
                try:
                    Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_opt_R102, y0 = C_exp_opt_R102[0], VR = VR_exp_opt_R102, Qi1 = Q_P101_opt, Csus_in_i1 = C_exp_opt_R101,
                                                        Qi2 = Q_P101_opt, Csus_in_i2 = C_exp_opt_R101, Operation = 1, K = self.K_ini_ADM1_R102)
                    
                    K_R102.append(Opt_kinetic_params_R102.x[0])
                    Error_R102.append(Opt_kinetic_params_R102.fun)
                except Exception as e:
                    continue
            
            self.K_ini_ADM1_R101 = st.mean(K_R101)
            self.K_ini_ADM1_R102 = st.mean(K_R102)

            # self.Optimized_parameters = pd.DataFrame({"time": self.TrainMode["time"],
            #                                         "K_R101": K_R101,
            #                                         "Error_R101": Error_R101,
            #                                         "K_R102": K_R102,
            #                                         "Error_R102": Error_R102})
            
        else:  #Operation Mode 4
            t_exp = (self.TrainMode["time"]).tolist()                #minutes
            C_exp_R101 = self.TrainMode["Csus_exp_R101"].tolist()    #Kmol/m3 = mol/L
            VR_exp_R101 = self.TrainMode["Vol_R101"].tolist()        #L 
            Csus_in_R101 = self.TrainMode["Csus_in_R101"].to_list()  #mol/L
            C_exp_R102 = self.TrainMode["Csus_exp_R102"].tolist()    #mol/L
            VR_exp_R102 = self.TrainMode["Vol_R102"].tolist()        #L
            Q_P104 = (self.TrainMode["Q_P104"]/60).tolist()          #L/min 
            Q_P101 = (self.TrainMode["Q_P101"]/60).tolist()          #L/min
            Q_P102 = (self.TrainMode["Q_P102"]/60).tolist()          #L/min

            K_R101 = []
            Error_R101 = []

            K_R102 = []
            Error_R102 = []

            for i in range (len(t_exp)):
                t_exp_opt = t_exp[i : i+resolution]
                C_exp_opt_R101 = C_exp_R101[i : i+resolution]
                VR_exp_opt_R101 = VR_exp_R101[i : i+resolution]
                Csus_in_opt_R101 = Csus_in_R101[i : i+resolution]
                Q_P104_opt = Q_P104[i : i+resolution]
                Q_P102_opt = Q_P102[i : i+resolution]
                
                C_exp_opt_R102 = C_exp_R102[i : i+resolution]
                VR_exp_opt_R102 = VR_exp_R102[i : i+resolution]
                Q_P101_opt = Q_P101[i : i+resolution]

                try:
                    Opt_kinetic_params_R101 = Optimization(t = t_exp_opt, C_exp = C_exp_opt_R101, y0 = C_exp_opt_R101[0], VR = VR_exp_opt_R101, Qi1 = Q_P104_opt, Csus_in_i1 = Csus_in_opt_R101,
                                                        Qi2 = Q_P102_opt, Csus_in_i2 = C_exp_opt_R102, Operation = 2, K = self.K_ini_ADM1_R101)
                    
                    K_R101.append(Opt_kinetic_params_R101.x[0])
                    Error_R101.append(Opt_kinetic_params_R101.fun)
                except Exception as e:
                    continue
                
                try:
                    Opt_kinetic_params_R102 = Optimization(t = t_exp_opt, C_exp = C_exp_opt_R102, y0 = C_exp_opt_R102[0], VR = VR_exp_opt_R101[0], Qi1 = Q_P101_opt, Csis_in_i1 = C_exp_opt_R101,
                                                        Qi2 = Q_P101_opt, Csus_in_i2 = C_exp_opt_R101, Operation = 1, K = self.K_ini_ADM1_R102)
                    
                    K_R102.append(Opt_kinetic_params_R102.x[0])
                    Error_R102.append(Opt_kinetic_params_R102.fun)
                except Exception as e:
                    continue
            
            self.K_ini_ADM1_R101 = st.mean(K_R101)
            self.K_ini_ADM1_R102 = st.mean(K_R102)

            # self.Optimized_parameters = pd.DataFrame({"time": self.TrainMode["time"],
            #                                         "K_R101": K_R101,
            #                                         "Error_R101": Error_R101,
            #                                         "K_R102": K_R102,
            #                                         "Error_R102": Error_R102})
            
    def Optimization_Gompertz(self):
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
            t_exp = self.TrainMode_gompertz["time"].tolist()
            y_exp = self.TrainMode_gompertz["y_t_exp"].tolist()
            Results = Optimization_Gompertz(params = (self.ym_R101, self.U_R101, self.L_R101), t = t_exp, y_exp = y_exp)
            self.Optimized_parameters = pd.DataFrame({"ym": Results.x[0],
                                                      "U": Results.x[1],
                                                      "L": Results.x[2],
                                                      "Error": Results.fun}, index=[0])
            self.ym_R101 = self.Optimized_parameters["ym"].iloc[0]
            self.U_R101 = self.Optimized_parameters["U"].iloc[0]
            self.L_R101 = self.Optimized_parameters["L"].iloc[0]        
        else:
            t_exp = self.TrainMode_gompertz["time"].tolist()
            y_exp_R101 = self.TrainMode_gompertz["y_t_exp_R101"].tolist()
            y_exp_R102 = self.TrainMode_gompertz["y_t_exp_R102"].tolist()

            Results_R101 = Optimization_Gompertz(params = (self.ym_R101, self.U_R101, self.L_R101), t = t_exp, y_exp = y_exp_R101)
            Results_R102 = Optimization_Gompertz(params = (self.ym_R102, self.U_R102, self.L_R102), t = t_exp, y_exp = y_exp_R102)
        
            self.Optimized_parameters = pd.DataFrame({"ym_R101": Results_R101.x[0],
                                                      "U_R101": Results_R101.x[1],
                                                      "L_R101": Results_R101.x[2],
                                                      "Error_R101": Results_R101.fun,
                                                      "ym_R102": Results_R102.x[0],
                                                      "U_R102": Results_R102.x[1],
                                                      "L_R102": Results_R102.x[2],
                                                      "Error_R102": Results_R102.fun}, index=[0])
            
            self.ym_R101 = self.Optimized_parameters["ym_R101"].iloc[0]
            self.U_R101 = self.Optimized_parameters["U_R101"].iloc[0]
            self.L_R101 = self.Optimized_parameters["L_R101"].iloc[0]

            self.ym_R102 = self.Optimized_parameters["ym_R102"].iloc[0]
            self.U_R102 = self.Optimized_parameters["U_R102"].iloc[0]
            self.L_R102 = self.Optimized_parameters["L_R102"].iloc[0]
    
    def biogas_treatment_optimization (self, W_feSO4, W_silica, qmax_NH3, W_carbon, K_NH3, K2_NH3):
        #V101
        self.biogas_AbsoluteHumidity_V101 = self.Thermo.BiogasAbsoluteHumidity(RH = self.DataPlant["rh_V101"], T = self.DataPlant["T_V101"])
        self.mol_H2O_V101 = (self.biogas_AbsoluteHumidity_V101 * self.DataPlant["Vacum_V101"])/18

        #V102
        self.biogas_AbsoluteHumidity_V102 = self.Thermo.BiogasAbsoluteHumidity(RH = self.DataPlant["rh_V102"], T = self.DataPlant["T_V102"])
        self.mol_H2O_V102 = (self.biogas_AbsoluteHumidity_V102 * self.DataPlant["Vacum_V102"])/18

        #V107
        self.biogas_AbsoluteHumidity_V107 = self.Thermo.BiogasAbsoluteHumidity(RH = self.DataPlant["rh_V107"], T = self.DataPlant["T_V107"])
        self.mol_H2O_V107 = (self.biogas_AbsoluteHumidity_V107 * self.DataPlant["Vacum_V107"])/18

        #Adsorptia estimation
        self.nCH4_V101_acum_f = self.biogas_mol_V101_acum_NN * self.DataPlant["xCH4_V101_filled"]/100
        self.nCO2_V101_acum_f = self.biogas_mol_V101_acum_NN * self.DataPlant["xCO2_V101_filled"]/100
        self.nO2_V101_acum_f = self.biogas_mol_V101_acum_NN * self.DataPlant["xO2_V101_filled"]/100
        self.nH2S_V101_acum_f = self.biogas_mol_V101_acum_NN * self.DataPlant["xH2S_V101_filled"]/1000000
        self.nH2_V101_acum_f = self.biogas_mol_V101_acum_NN * self.DataPlant["xH2_V101_filled"]/1000000
        self.nNH3_V101_acum_f = self.nCH4_V101_acum_f * (self.s_NH3/self.s_CH4)

        self.nCH4_V102_acum_f = self.biogas_mol_V102_acum_NN * self.DataPlant["xCH4_V102_filled"]/100
        self.nCO2_V102_acum_f = self.biogas_mol_V102_acum_NN * self.DataPlant["xCO2_V102_filled"]/100
        self.nO2_V102_acum_f = self.biogas_mol_V102_acum_NN * self.DataPlant["xO2_V102_filled"]/100
        self.nH2S_V102_acum_f = self.biogas_mol_V102_acum_NN * self.DataPlant["xH2S_V102_filled"]/1000000
        self.nH2_V102_acum_f = self.biogas_mol_V102_acum_NN * self.DataPlant["xH2_V102_filled"]/1000000
        self.nNH3_V102_acum_f = self.nCH4_V102_acum_f * (self.s_NH3/self.s_CH4)

        mol_in_H2O = (self.mol_H2O_V101 + self.mol_H2O_V102)
        mol_in_H2S = (self.nH2S_V101_acum + self.nH2S_V102_acum)
        delta_H2O = (self.mol_H2O_V101 + self.mol_H2O_V102) - self.mol_H2O_V107
        self.nH2O_ads = delta_H2O.where(delta_H2O > 0, 0)  
        delta_H2S = (self.nH2S_V101_acum + self.nH2S_V102_acum) - self.nH2S_V107_acum
        self.nH2S_ads = delta_H2S.where(delta_H2S > 0, 0)
        
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
        
        self.Train_filters_data = pd.DataFrame({"time": self.DataPlant["normal_time"],
                                                "mol_in_H2O": mol_in_H2O,
                                                "mol_out_H2O": self.mol_H2O_V107,
                                                "mol_ads_H2O": self.nH2O_ads,
                                                "mol_in_H2S": mol_in_H2S,
                                                "mol_out_H2S": self.nH2S_V107_acum,
                                                "mol_ads_H2S":self.nH2S_ads})
        #print(self.Train_filters_data)
        self.Train_filters_data.ffill(inplace=True)
        self.Train_filters_data.bfill(inplace=True)
        Results_H2O = Langmuir_optimization (params = (self.qmax_H2O, self.K_H2O, self.K2_H2O), t = self.DataPlant["normal_time"], mol_ads_exp = self.nH2O_ads, W = W_silica, mol_transfer = mol_in_H2O)
        Results_H2S = Langmuir_optimization(params = (self.qmax_H2S, self.K_H2S, self.K2_H2S), t = self.DataPlant["normal_time"], mol_ads_exp = self.nH2S_ads, W = W_feSO4, mol_transfer = mol_in_H2S)
        
        self.Optimized_parameters_filter_H2O = pd.DataFrame({"qmax_H2O": float(Results_H2O.x[0]),
                                                             "K_H2O": float(Results_H2O.x[1]),
                                                             "K2_H2O": float(Results_H2O.x[2]),
                                                             "qmax_H2S": float(Results_H2S.x[0]),
                                                             "K_H2S": float(Results_H2S.x[1]),
                                                             "K2_H2S": float(Results_H2S.x[2])}, index=[0],)
        
        self.mol_NH3_ads_teo = Langmuir_model(t = self.DataPlant["normal_time"], qmax = qmax_NH3, K1 = K_NH3, K2 = K2_NH3, W = W_carbon, mol_transfer=np.array(self.nNH3_V101_acum_f + self.nNH3_V102_acum_f))
        self.Train_filters_data["nNH3_ads"] = self.mol_NH3_ads_teo
        total = self.nNH3_V101_acum_f + self.nNH3_V102_acum_f
        self.nNH3_V107_acum = total.where(total <= self.mol_NH3_ads_teo, total - self.mol_NH3_ads_teo)

        #Filter_effciency
        try:
            self.x_ads_H2O = (self.nH2O_ads)/self.Train_filters_data["mol_in_H2O"]
        except ZeroDivisionError:
            self.x_ads_H2O = 0
        try:
            self.x_ads_H2S = (self.nH2S_ads)/self.Train_filters_data["mol_in_H2S"]
        except ZeroDivisionError:
            self.x_ads_H2S = 0
        try:
            self.x_ads_NH3 = (self.mol_NH3_ads_teo)/(self.nNH3_V101_acum + self.nNH3_V102_acum)
        except ZeroDivisionError:
            self.x_ads_NH3 = 0

    def exitVariablestoFrontEnd(self):
        #TK100
        """
        substrate variables are declares in Limit Reagent Estimation function
        """
        self.Mix_Velocity_TK100 = float(self.Mix_Velocity_TK100["_value"].iloc[-1])

       # Pump 104 flow
        last_10_P104 = self.DataPlant["P104"].tail(10)
        non_zero_P104 = last_10_P104[last_10_P104 != 0]

        if not non_zero_P104.empty:
            self.P104 = float(non_zero_P104.max())
        else:
            self.P104 = 0.0  # Or another default value if all are zero
        
        #R101
        self.Mix_Velocity_R101 = float(self.Mix_Velocity_R101["_value"].iloc[-1])
        self.pH_R101 = float(self.DataPlant["pH_R101"].iloc[-1])
        self.T_R101 = float(self.DataPlant["Tprom_R101"].iloc[-1])
        self.x_R101_e = float(self.x_R101.iloc[-1])

        # Pump 101 flow
        if self.Operation_mode in [2,3,4,5]:
            last_10_P101 = self.DataPlant["P101"].tail(5)
            non_zero_P101 = last_10_P101[last_10_P101 != 0]

            if not non_zero_P101.empty:
                self.P101 = float(non_zero_P101.max())
            else:
                self.P101 = 0.0  # Or another default value if all are zero
        else:
            self.P101 = 0.0
        
        # Pump 102 flow
        if self.Operation_mode in [4,5]:
            last_10_P102 = self.DataPlant["P102"].tail(5)
            non_zero_P102 = last_10_P102[last_10_P102 != 0]

            if not non_zero_P102.empty:
                self.P102 = float(non_zero_P102.max())
            else:
                self.P102 = 0.0  # Or another default value if all are zero
        else:
            self.P102 = 0.0

        #V101
        self.Pacum_V101_e = float(self.DataPlant["Pacum_V101"].iloc[-1])
        self.P_V101_e = float(self.DataPlant["P_V101"].iloc[-1])
        self.Vnorm_bio_V101 = float(self.DataPlant["Vacum_V101"].iloc[-1])
        self.T_V101_e = float(self.DataPlant["T_V101"].iloc[-1])
        self.Vnorm_bio_sto_V101 = float((self.P_V101_e*6.8947 * 15 * 273.15)/(100 * (self.T_V101_e + 273.15)))
        self.xCH4_V101_e = float(self.DataPlant["xCH4_V101"].iloc[-1])
        self.VCH4_acum_V101 = self.Vnorm_bio_sto_V101 * (self.xCH4_V101_e/100)
        self.mol_acum_CH4_V101 = float(self.nCH4_V101_acum_f.iloc[-1])
        self.xCO2_V101_e = float(self.DataPlant["xCO2_V101"].iloc[-1])
        self.VCO2_acum_V101 = self.Vnorm_bio_sto_V101 * (self.xCO2_V101_e/100)
        self.mol_acum_CO2_V101 = float(self.nCO2_V101_acum_f.iloc[-1])
        self.xH2S_V101_e = float(self.DataPlant["xH2S_V101"].iloc[-1])
        self.VH2S_acum_V101 = self.Vnorm_bio_sto_V101 * (self.xH2S_V101_e/1000000)
        self.mol_acum_H2S_V101 = float(self.nH2S_V101_acum_f.iloc[-1])
        self.xO2_V101_e = float(self.DataPlant["xO2_V101"].iloc[-1])
        self.VO2_acum_V101 = self.Vnorm_bio_sto_V101 * (self.xO2_V101_e/100)
        self.mol_acum_O2_V101 = float(self.nO2_V101_acum_f.iloc[-1])
        self.xH2_V101_e = float(self.DataPlant["xH2_V101"].iloc[-1])
        self.VH2_acum_V101 = self.Vnorm_bio_sto_V101 * (self.xH2_V101_e/1000000)
        self.mol_acum_H2_V101 = float(self.nH2_V101_acum_f.iloc[-1])
        try:
            self.xNH3_V101_e = (float(self.nNH3_V101_acum_f.iloc[-1])/(float(self.nNH3_V101_acum_f.iloc[-1]) + self.mol_acum_CH4_V101 + self.mol_acum_CO2_V101 + self.mol_acum_H2S_V101 + self.mol_acum_O2_V101 + self.mol_acum_H2_V101))*1000000
        except ZeroDivisionError:
            self.xNH3_V101_e = 0
        self.VNH3_acum_V101 = self.Vnorm_bio_sto_V101 * (self.xNH3_V101_e/1000000)
        self.mol_acum_NH3_V101 = float(self.nNH3_V101_acum_f.iloc[-1])
        self.RH_V101_e = float(self.DataPlant["rh_V101"].iloc[-1])
        self.Energy_V101 = float(self.Energia_jouleV101["_value"].iloc[-1])
        self.mol_acum_H2O_V101 = self.Thermo.BiogasAbsoluteHumidity(RH = self.RH_V101_e/100, T = self.T_V101_e) * self.Vnorm_bio_V101

        #V102
        self.Pacum_V102_e = float(self.DataPlant["Pacum_V102"].iloc[-1])
        self.P_V102_e = float(self.DataPlant["P_V102"].iloc[-1])
        self.Vnorm_bio_V102 = float(self.DataPlant["Vacum_V102"].iloc[-1])
        self.T_V102_e = float(self.DataPlant["T_V102"].iloc[-1])
        self.Vnorm_bio_sto_V102 = float((self.P_V102_e*6.8947 * 15 * 273.15)/(100 * (self.T_V102_e + 273.15)))
        self.xCH4_V102_e = float(self.DataPlant["xCH4_V102"].iloc[-1])
        self.VCH4_acum_V102 = self.Vnorm_bio_sto_V102 * (self.xCH4_V102_e/100)
        self.mol_acum_CH4_V102 = float(self.nCH4_V102_acum_f.iloc[-1])
        self.xCO2_V102_e = float(self.DataPlant["xCO2_V102"].iloc[-1])
        self.VCO2_acum_V102 = self.Vnorm_bio_sto_V102 * (self.xCO2_V102_e/100)
        self.mol_acum_CO2_V102 = float(self.nCO2_V102_acum_f.iloc[-1])
        self.xH2S_V102_e = float(self.DataPlant["xH2S_V102"].iloc[-1])
        self.VH2S_acum_V102 = self.Vnorm_bio_sto_V102 * (self.xH2S_V102_e/1000000)
        self.mol_acum_H2S_V102 = float(self.nH2S_V102_acum_f.iloc[-1])
        self.xO2_V102_e = float(self.DataPlant["xO2_V102"].iloc[-1])
        self.VO2_acum_V102 = self.Vnorm_bio_sto_V102 * (self.xO2_V102_e/100)
        self.mol_acum_O2_V102 = float(self.nO2_V102_acum_f.iloc[-1])
        self.xH2_V102_e = float(self.DataPlant["xH2_V102"].iloc[-1])
        self.VH2_acum_V102 = self.Vnorm_bio_sto_V102 * (self.xH2_V102_e/1000000)
        self.mol_acum_H2_V102 = float(self.nH2_V102_acum_f.iloc[-1])
        try:
            self.xNH3_V102_e = (float(self.nNH3_V102_acum_f.iloc[-1])/(float(self.nNH3_V102_acum_f.iloc[-1]) + self.mol_acum_CH4_V102 + self.mol_acum_CO2_V102 + self.mol_acum_H2S_V102 + self.mol_acum_O2_V102 + self.mol_acum_H2_V102))*1000000
        except ZeroDivisionError:
            self.xNH3_V102_e = 0
        self.VNH3_acum_V102 = self.Vnorm_bio_sto_V102 * (self.xNH3_V102_e/1000000)
        self.mol_acum_NH3_V102 = float(self.nNH3_V102_acum.iloc[-1])
        self.RH_V102_e = float(self.DataPlant["rh_V102"].iloc[-1])
        try:
            self.Energy_V102 = float(self.Energia_jouleV102["_value"].iloc[-1])
        except (TypeError, AttributeError, IndexError, KeyError) as e:
            print(f"Error accessing energy value: {e}")
            self.Energy_V102 = 0.0  # or None, or raise, depending on your use case
        self.mol_acum_H2O_V102 = self.Thermo.BiogasAbsoluteHumidity(RH = self.RH_V102_e/100, T = self.T_V102_e) * self.Vnorm_bio_V102

        #V107
        self.Pacum_V107_e = float(self.DataPlant["Pacum_V107"].iloc[-1])
        self.P_V107_e = float(self.DataPlant["P_V107"].iloc[-1])
        self.Vnorm_bio_V107 = float(self.DataPlant["Vacum_V107"].iloc[-1])
        self.T_V107_e = float(self.DataPlant["T_V107"].iloc[-1])
        self.Vnorm_bio_sto_V107 = float((self.P_V107_e*6.8947 * 15 * 273.15)/(100 * (self.T_V107_e + 273.15)))
        self.xCH4_V107_e = float(self.DataPlant["xCH4_V107"].iloc[-1])
        self.VCH4_acum_V107 = self.Vnorm_bio_sto_V107 * (self.xCH4_V107_e/100)
        self.mol_acum_CH4_V107 = float(self.nCH4_V107_acum.iloc[-1])
        self.xCO2_V107_e = float(self.DataPlant["xCO2_V107"].iloc[-1])
        self.VCO2_acum_V107 = self.Vnorm_bio_sto_V107 * (self.xCO2_V107_e/100)
        self.mol_acum_CO2_V107 = float(self.nCO2_V107_acum.iloc[-1])
        self.xH2S_V107_e = float(self.DataPlant["xH2S_V107"].iloc[-1])
        self.VH2S_acum_V107 = self.Vnorm_bio_sto_V107 * (self.xH2S_V107_e/1000000)
        self.mol_acum_H2S_V107 = float(self.nH2S_V107_acum.iloc[-1])
        self.xO2_V107_e = float(self.DataPlant["xO2_V107"].iloc[-1])
        self.VO2_acum_V107 = self.Vnorm_bio_sto_V107 * (self.xO2_V107_e/100)
        self.mol_acum_O2_V107 = float(self.nO2_V107_acum.iloc[-1])
        self.xH2_V107_e = float(self.DataPlant["xH2_V107"].iloc[-1])
        self.VH2_acum_V107 = self.Vnorm_bio_sto_V107 * (self.xH2_V107_e/1000000)
        self.mol_acum_H2_V107 = float(self.nH2_V107_acum.iloc[-1])
        try:
            self.xNH3_V107_e = (float(self.nNH3_V107_acum.iloc[-1])/(float(self.nNH3_V107_acum.iloc[-1]) + self.mol_acum_CH4_V107 + self.mol_acum_CO2_V107 + self.mol_acum_H2S_V107 + self.mol_acum_O2_V107 + self.mol_acum_H2_V107))*1000000
        except ZeroDivisionError:
            self.xNH3_V107_e = 0
        self.VNH3_acum_V107 = self.Vnorm_bio_sto_V107 * (self.xNH3_V107_e/1000000)
        self.mol_acum_NH3_V107 = float(self.nNH3_V107_acum.iloc[-1])
        self.RH_V107_e = float(self.DataPlant["rh_V107"].iloc[-1])
        try:
            self.Energy_V107 = float(self.Energia_jouleV107["_value"].iloc[-1])
        except (TypeError, AttributeError, IndexError, KeyError) as e:
            print(f"Error accessing energy value: {e}")
            self.Energy_V107 = 0.0  # or None, or raise, depending on your use case
        self.Energy_V107 = float(self.Energia_jouleV107["_value"].iloc[-1])
        self.mol_acum_H2O_V107 = self.Thermo.BiogasAbsoluteHumidity(RH = self.RH_V107_e/100, T = self.T_V107_e) * self.Vnorm_bio_V107

        #Biogas Treatment
        self.mol_NH3_ads = self.mol_NH3_ads_teo.iloc[-1]
        self.mol_H2S_ads = self.nH2S_ads.iloc[-1]
        self.mol_H2O_ads = self.nH2O_ads.iloc[-1]
        try:
            mol_in_H2O = self.Train_filters_data["mol_in_H2O"].iloc[-1]
            if mol_in_H2O != 0 and not pd.isna(mol_in_H2O):
                x_ads_H2O = self.mol_H2O_ads / mol_in_H2O
            else:
                x_ads_H2O = 0
            # print("mol_in_H2O:", mol_in_H2O)
            # print("mol_H2O_ads:", self.mol_H2O_ads)
            # print("x_ads_H2O:", x_ads_H2O)
        except Exception as e:
            print("Error calculating x_ads_H2O:", e)
            x_ads_H2O = 0
        try:
            mol_in_H2S = self.Train_filters_data["mol_in_H2S"].iloc[-1]
            if mol_in_H2S != 0 and not pd.isna(mol_in_H2S):
                x_ads_H2S = self.mol_H2S_ads / mol_in_H2S
            else:
                x_ads_H2S = 0
        except Exception as e:
            print("Error calculating x_ads_H2S:", e)
            x_ads_H2S = 0
        try:
            total_n_NH3 = self.nNH3_V101_acum_f.iloc[-1] + self.nNH3_V102_acum_f.iloc[-1]
            if total_n_NH3 != 0 and not pd.isna(total_n_NH3):
                x_ads_NH3 = self.mol_NH3_ads / total_n_NH3
            else:
                x_ads_NH3 = 0

            # print("total_n_NH3:", total_n_NH3)
            # print("mol_NH3_ads:", self.mol_NH3_ads)
            # print("x_ads_NH3:", x_ads_NH3)
        except Exception as e:
            print("Error calculating x_ads_NH3:", e)
            x_ads_NH3 = 0

        self.Xglobal = ((x_ads_H2O + x_ads_H2S + x_ads_NH3)/3)
        
    def StorageData (self, name):
        timestamp = self.DataPlant["time"].iloc[-1]  # Convert to nanoseconds
        
        if self.Model == "Arrhenius" and (self.Operation_mode == 1 or self.Operation_mode == 2):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R101?{name}', value = abs(float(self.K_mean_R101/60)), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?Ea_R101?{name}', value = abs(float(self.Ea_mean_R101)), timestamp=timestamp)  
        
        elif self.Model == "ADM1" and (self.Operation_mode == 1 or self.Operation_mode == 2):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R101?{name}', value = abs(float(self.K_ini_ADM1_R101/60)), timestamp=timestamp)
        
        elif self.Model == "Gompertz" and (self.Operation_mode == 1 or self.Operation_mode == 2):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?ym_R101?{name}', value = float(self.ym_R101), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?U_R101?{name}', value = float(self.U_R101), timestamp=timestamp)
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?L_R101?{name}', value = float(self.L_R101), timestamp=timestamp)

        elif self.Model == "Arrhenius" and (self.Operation_mode == 3 or self.Operation_mode == 4 or self.Operation_mode == 5):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R101?{name}', value = abs(float(self.K_mean_R101/60)), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?Ea_R101?{name}', value = abs(float(self.Ea_mean_R101)), timestamp=timestamp)
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?Ea_R102?{name}', value = abs(float(self.K_mean_R102/60)), timestamp=timestamp) 
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?Ea_R102?{name}', value = abs(float(self.Ea_mean_R102)), timestamp=timestamp)
        
        elif self.Model == "ADM1"  and (self.Operation_mode == 3 or self.Operation_mode == 4 or self.Operation_mode == 5):
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R101?{name}', value = abs(float(self.K_ini_ADM1_R101/60)), timestamp=timestamp)
            self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device = "entrenamiento", variable = f'Modo{int(self.Operation_mode)}?{self.Model}?K_R102?{name}', value = abs(float(self.K_ini_ADM1_R102/60)), timestamp=timestamp)
        
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
        self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device="entrenamiento", variable=f'Modo{int(self.Operation_mode)}?{self.Model}?qmax_H2O?{name}', value=float(self.Optimized_parameters_filter_H2O["qmax_H2O"].iloc[-1]) , timestamp=timestamp)
        self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device="entrenamiento", variable=f'Modo{int(self.Operation_mode)}?{self.Model}?K_H2O?{name}', value=float(self.Optimized_parameters_filter_H2O["K_H2O"].iloc[-1]) , timestamp=timestamp)
        self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device="entrenamiento", variable=f'Modo{int(self.Operation_mode)}?{self.Model}?K2_H2O?{name}', value=float(self.Optimized_parameters_filter_H2O["K2_H2O"].iloc[-1]) , timestamp=timestamp)
        self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device="entrenamiento", variable=f'Modo{int(self.Operation_mode)}?{self.Model}?qmax_H2S?{name}', value=float(self.Optimized_parameters_filter_H2O["qmax_H2S"].iloc[-1]) , timestamp=timestamp)
        self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device="entrenamiento", variable=f'Modo{int(self.Operation_mode)}?{self.Model}?K_H2S?{name}', value=float(self.Optimized_parameters_filter_H2O["K_H2S"].iloc[-1]) , timestamp=timestamp)
        self.influxDB.InfluxDBwriter(measurement="Planta_Biogas", device="entrenamiento", variable=f'Modo{int(self.Operation_mode)}?{self.Model}?K2_H2S?{name}', value=float(self.Optimized_parameters_filter_H2O["K2_H2S"].iloc[-1]) , timestamp=timestamp)

