import os
import sys

current_directory = os.getcwd()
current_directory = os.path.join(current_directory, "V1.0")
sys.path.append(current_directory)

from simulation_models.Biogas import Biogas_Model_Simulation
from tools import DBManager
from datetime import datetime
import time

tp = 120
Biogas_plant = Biogas_Model_Simulation.BiogasPlantSimulation(VR1=30, VR2=70, VG1=15, VG2=35, VG3=35, tp=tp, 
                 ST_R101=10, SV_R101=1, Cc_R101=40.48, Ch_R101=5.29, Co_R101=29.66, Cn_R101=1.37, Cs_R101=0.211, rho_R101=1000,
                 ST_R102=10, SV_R102=1, Cc_R102=40.48, Ch_R102=5.29, Co_R102=29.66, Cn_R102=1.37, Cs_R102=0.211, rho_R102=1000, 
                 OperationMode="Modo1")

Biogas_plant.Substrate_conditions(Cc = 40.48, Ch = 5.29, Co = 29.66, Cn = 1.37, Cs = 0.211, rho=1000, ST = 10, SV = 5)   
DB = DBManager.InfluxDBmodel(server="http://localhost:8086", org = "UCO", bucket="BiogasPlantSimulator",token="ZdklaIEjLhq4q9BlkkyS2HkJbN8DGKLV2HUjnRtOPGqvoelgQxEqk9r-x9sXUyiYgF1a29a510FzMqwLT2KBWQ==")
DB.InfluxDBconnection()
timestamp1 = int(time.time())

pump104_state=0
mixR101_state = 0
mixR102_state = 0
iteration = 0
pump101_state = 0
pump102_state = 0
while True:
    Biogas_plant.Pump104(TRH = 30, FT_P104 = 5, TTO_P104 = 10)
    Biogas_plant.Pump101(FT_P101 = 5, TTO_P101 = 10, Q_P101 = 2.4)
    Biogas_plant.Pump102(FT_P102 = 5, TTO_P102 = 10, Q_P102 =2.4)
    Biogas_plant.Mixing_R101(FT_mixin_R101 = 5, TTO_mixing_R101 = 10, RPM_R101= 50)
    Biogas_plant.Mixing_R102(FT_mixin_R102 = 5, TTO_mixing_R102 = 10, RPM_R102 = 50)
    Biogas_plant.Data_simulation(Temperature_R101 = 35, Temperature_R102 = 35, pH_R101 = 7, pH_R102 = 7)
    Biogas_plant.ReactorSimulation(Model = "ADM1", A_R101 = 1e-7, B_R101 = 0, C_R101 = 0,
                                   A_R102 = 1e-5, B_R102 = 0, C_R102 = 0)
    Biogas_plant.V101()
    Biogas_plant.V102()
    Biogas_plant.Biogas_treatment(D1 = 1e-10, W1 = 5000, L1 = 0.2,
                                  D2 = 1e-10, W2 = 5000, L2 = 0.2,
                                  D3 = 1e-10, W3 = 5000, L3 = 0.2)
    
    Biogas_plant.V107()
    iteration = iteration + 1
    # write biogas data influx test
    if iteration == 1:
        #timestamp1 = int(begin_date.timestamp())
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MTRH", value = Biogas_plant.TRH, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MFTP104", value = Biogas_plant.FT_P104, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MTTOP104", value = Biogas_plant.TTO_P104, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MNS", value = 3, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MPH", value = 80, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "ST1", value = "porquinaza", timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MP1", value = 8, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MST1", value = 30, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MSV1", value = 25, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCc1", value = 40.48, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCh1", value = 5.29, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCo1", value = 29.66, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCn1", value = 1.37, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCs1", value = 0.211, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "Md1", value = 500, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "ST2", value = "RSU", timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MP2", value = 8, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MST2", value = 20, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MSV2", value = 15, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCc2", value = 40.48, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCh2", value = 5.29, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCo2", value = 29.66, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCn2", value = 1.37, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCs2", value = 0.211, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "Md2", value = 600, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "ST3", value = "Almidon", timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MP3", value = 4, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MST3", value = 35, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MSV3", value = 29, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCc3", value = 40.48, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCh3", value = 5.29, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCo3", value = 29.66, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCn3", value = 1.37, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCs3", value = 0.211, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "Md3", value = 700, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "ST4", value = "Gallinaza", timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MP4", value = 4, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MST4", value = 31, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MSV4", value = 26.1, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCc4", value = 40.48, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCh4", value = 5.29, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCo4", value = 29.66, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCn4", value = 1.37, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MCs4", value = 0.211, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "Md4", value = 800, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MQP101", value = 2.4, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MFTP101", value = 5, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MTTOP101", value = 10, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MQP102", value = 2.4, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MFTP102", value = 5, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "MTTOP102", value = 10, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "interfaz", variable = "ciclo", value = 1, timestamp = timestamp1)
        
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "TE-101A", value = 35, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "TE-101B", value = 36, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "AT-101", value = 7, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "TE-R101", value = (35+36)/2, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "PT-101", value = Biogas_plant.Pstorage_bio_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "LT-101", value = 37, timestamp = timestamp1)
        
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-CH4", value = Biogas_plant.x_CH4_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-CO2", value = Biogas_plant.x_CO2_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-H2S", value = Biogas_plant.x_H2S_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-O2", value = Biogas_plant.x_O2_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-H2", value = Biogas_plant.x_H2_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103B", value = Biogas_plant.RH_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "PT-103", value = Biogas_plant.Pstorage_bio_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "TT-103", value = Biogas_plant.Temperature, timestamp = timestamp1)
        
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "TE-102A", value = 35, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "TE-102B", value = 36, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "AT-102", value = 7, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "TE-R102", value = (35+36)/2, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "PT-102", value = Biogas_plant.Pstorage_bio_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "LT-102", value = 50, timestamp = timestamp1)
        
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-CH4", value = Biogas_plant.x_CH4_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-CO2", value = Biogas_plant.x_CO2_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-H2S", value = Biogas_plant.x_H2S_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-O2", value = Biogas_plant.x_O2_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-H2", value = Biogas_plant.x_H2_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104B", value = Biogas_plant.RH_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "PT-104", value = Biogas_plant.Pstorage_bio_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "TT-104", value = Biogas_plant.Temperature, timestamp = timestamp1)
        
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-CH4", value = Biogas_plant.x_CH4_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-CO2", value = Biogas_plant.x_CO2_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-H2S", value = Biogas_plant.x_H2S_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-O2", value = Biogas_plant.x_O2_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-H2", value = Biogas_plant.x_H2_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105B", value = Biogas_plant.RH_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "PT-105", value = Biogas_plant.Pstorage_bio_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "TT-105", value = Biogas_plant.Temperature, timestamp = timestamp1)
        
        if pump104_state != Biogas_plant.Q_P104:
            pump104_state = Biogas_plant.Q_P104
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P104", variable = "FE-104", value = Biogas_plant.Q_P104, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P104", variable = "MP104TIME", value = Biogas_plant.TimeCounterPump_P104, timestamp = timestamp1)
        if pump101_state != Biogas_plant.Q_P101:
            pump101_state = Biogas_plant.Q_P101
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P101", variable = "P-101", value = Biogas_plant.Q_P101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P101", variable = "MP101TIME", value = Biogas_plant.TimeCounterPump_P101, timestamp = timestamp1)    
        if pump102_state != Biogas_plant.Q_P102:
            pump102_state = Biogas_plant.Q_P102
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P102", variable = "P-102", value = Biogas_plant.Q_P102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P102", variable = "MP102TIME", value = Biogas_plant.TimeCounterPump_P102, timestamp = timestamp1)    
        if mixR101_state != Biogas_plant.RPM_R101:
            mixR101_state = Biogas_plant.RPM_R101
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "SE-108", value = Biogas_plant.RPM_R101, timestamp = timestamp1)
        if mixR102_state != Biogas_plant.RPM_R102:
            mixR102_state = Biogas_plant.RPM_R102
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "SE-108", value = Biogas_plant.RPM_R101, timestamp = timestamp1)                        
    else:   
        timestamp1 = timestamp1 + tp
    
    if (Biogas_plant.GlobalTime/5) % 5 == 0:

        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "TE-101A", value = 35, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "TE-101B", value = 36, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "AT-101", value = 7, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "TE-R101", value = (35+36)/2, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "PT-101", value = Biogas_plant.Pstorage_bio_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "LT-101", value = 37, timestamp = timestamp1)
        
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-CH4", value = Biogas_plant.x_CH4_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-CO2", value = Biogas_plant.x_CO2_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-H2S", value = Biogas_plant.x_H2S_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-O2", value = Biogas_plant.x_O2_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103A-H2", value = Biogas_plant.x_H2_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "AT-103B", value = Biogas_plant.RH_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "PT-103", value = Biogas_plant.Pstorage_bio_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V101", variable = "TT-103", value = Biogas_plant.Temperature, timestamp = timestamp1)
        
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "TE-102A", value = 35, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "TE-102B", value = 36, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "AT-102", value = 7, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "TE-R102", value = (35+36)/2, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "PT-102", value = Biogas_plant.Pstorage_bio_V101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "LT-102", value = 50, timestamp = timestamp1)
        
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-CH4", value = Biogas_plant.x_CH4_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-CO2", value = Biogas_plant.x_CO2_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-H2S", value = Biogas_plant.x_H2S_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-O2", value = Biogas_plant.x_O2_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104A-H2", value = Biogas_plant.x_H2_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "AT-104B", value = Biogas_plant.RH_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "PT-104", value = Biogas_plant.Pstorage_bio_V102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V102", variable = "TT-104", value = Biogas_plant.Temperature, timestamp = timestamp1)
        
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-CH4", value = Biogas_plant.x_CH4_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-CO2", value = Biogas_plant.x_CO2_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-H2S", value = Biogas_plant.x_H2S_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-O2", value = Biogas_plant.x_O2_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105A-H2", value = Biogas_plant.x_H2_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "AT-105B", value = Biogas_plant.RH_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "PT-105", value = Biogas_plant.Pstorage_bio_V107, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "V107", variable = "TT-105", value = Biogas_plant.Temperature, timestamp = timestamp1)
        
    elif Biogas_plant.GlobalTime % 2 == 0: 
        if pump104_state != Biogas_plant.Q_P104:
            pump104_state = Biogas_plant.Q_P104
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P104", variable = "FE-104", value = Biogas_plant.Q_P104, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P104", variable = "MP104TIME", value = Biogas_plant.TimeCounterPump_P104, timestamp = timestamp1)
        if pump101_state != Biogas_plant.Q_P101:
            pump101_state = Biogas_plant.Q_P101
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P101", variable = "P-101", value = Biogas_plant.Q_P101, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P101", variable = "MP101TIME", value = Biogas_plant.TimeCounterPump_P101, timestamp = timestamp1)    
        if pump102_state != Biogas_plant.Q_P102:
            pump102_state = Biogas_plant.Q_P102
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P102", variable = "P-102", value = Biogas_plant.Q_P102, timestamp = timestamp1)
        DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "P102", variable = "MP102TIME", value = Biogas_plant.TimeCounterPump_P102, timestamp = timestamp1)    
        if mixR101_state != Biogas_plant.RPM_R101:
            mixR101_state = Biogas_plant.RPM_R101
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R101", variable = "SE-108", value = Biogas_plant.RPM_R101, timestamp = timestamp1)
        if mixR102_state != Biogas_plant.RPM_R102:
            mixR102_state = Biogas_plant.RPM_R102
            DB.InfluxDBwriter(measurement = "Planta_Biogas", device = "R102", variable = "SE-108", value = Biogas_plant.RPM_R101, timestamp = timestamp1)
               
    
    time.sleep(tp)
    
        
            
    
    
       
