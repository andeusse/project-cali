import os
import sys

current_directory = os.getcwd()
current_directory = os.path.join(current_directory, "V1.0")
sys.path.append(current_directory)

from tools import DBManager
import pandas as pd

class TrainingBiogasPlant:
    def __init__(self):
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
       
    def getData (self):
        #Get data from User input plant plant
        self.query1 = self.influxDB.QueryCreator(measurement="Planta_Biogas", device="interfaz", type=5)
        self.Datainterfaz = self.influxDB.InfluxDBreader(query = self.query1)
        self.Datainterfaz1 = pd.concat(self.Datainterfaz, ignore_index=True)
        self.Datainterfaz1.set_index("_field", inplace = True)
        
        #Get data from P104
        # self.query2 = self.influxDB.QueryCreator(measurement="PLanta_biogas", device="P104")
    
    def LimitReagentCalculation(self):
        self.SN = self.Datainterfaz1["_value"]["MNS"]    #SN: substrate number
        
        if self.SN  == 4:
            #Water proportion
            self.MPH = self.Datainterfaz1["_value"]["MPH"]    #MPH: Water proportion in the mix
            self.ST1 = self.Datainterfaz1["_value"]["ST1"]    #ST1: Substrate 1 name
            
            
#This will be the way to call method from API
Training = TrainingBiogasPlant()
Training.getData()
Training.LimitReagentCalculation()
print(Training.SN)


        