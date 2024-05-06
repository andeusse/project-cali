import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
current_directory = os.getcwd()
excel_file_path = os.path.join(os.path.abspath(os.path.join(current_directory, '..', '..')), "tools", "DB_Mapping.xlsx")
print(excel_file_path)

from  tools import DBManager
import pandas as pd

class BiogasModelTrain:
    def __init__ (self, time_train):
        self.databaseConnection_df = pd.read_excel(excel_file_path, sheet_name='ConexionDB')
        self.database_df = pd.read_excel(excel_file_path, sheet_name='InfluxDBVariables')
        self.InfluxDB = DBManager.InfluxDBmodel(server = 'http://' + str(self.databaseConnection_df['IP'][3])+':'+str(self.databaseConnection_df['Port'][3])+'/', org = self.databaseConnection_df['Organization'][3], bucket = self.databaseConnection_df['Bucket'][3], token = self.databaseConnection_df['Token'][3])
        self.time_train = time_train

    def GetDataModel_Operation_1 (self, Online=1, manual_P104=0):
        self.Online = Online
                
        self.query_Msus_exp_R101 = self.InfluxDB.QueryCreator(device = "DTPlantaBiogas", variable="Msus_exp_R101", location=1, type=1, forecastTime=1)
        self.M_sus_exp_R101 = self.InfluxDB.InfluxDBreader(self.query_Msus_exp_R101)
        self.M_sus_exp_R101v = self.M_sus_exp_R101["Msus_exp_R101"]
        
        self.query_Csus_exp_R101 = self.InfluxDB.QueryCreator(device = "DTPlantaBiogas", variable="Csus_exp_R101", location=1, type=1, forecastTime=1)
        self.C_sus_exp_R101 = self.InfluxDB.InfluxDBreader(self.query_Csus_exp_R101)
        self.C_sus_exp_R101v = self.C_sus_exp_R101["Csus_exp_R101"]
    
    #def Train_function_R101_Operation1 (self)

        

