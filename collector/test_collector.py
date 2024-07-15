import pandas as pd
import DBManager
import ModbusManager
import time
from datetime import datetime
import random

# %%

database_df = pd.read_excel('./Registros_Modbus.xlsx', sheet_name = 'ConexionDB')
analyzers_df = pd.read_excel('./Registros_Modbus.xlsx', sheet_name = 'ConexionAnalizadores')
loads_df = pd.read_excel('./Registros_Modbus.xlsx', sheet_name = 'Cargas')
variables_df = pd.read_excel('./Registros_Modbus.xlsx', sheet_name = 'Variables')


#%%
while True:
    for analyzer_index in analyzers_df.index:
        ModbusModel = ModbusManager.ModbusModel(str(analyzers_df['IP'][analyzer_index]), int(analyzers_df['Port'][analyzer_index]))
        
        # Open Connection 
        ModbusModel.ModbusConnection()
        
        for load_index in range(len(loads_df)):
            
            if loads_df["Analyzer"][load_index] == analyzers_df['Name'][analyzer_index]:
            
                for variable_index in variables_df.index:
            
                    value = ModbusModel.ModbusReader(loads_df["Unit ID"][load_index], variables_df["Address Dec"][variable_index], variables_df["Word"][variable_index], variables_df["Scale"][variable_index], variables_df["Format"][variable_index])
                    print(value)
                    print(type(value))
                    print(variables_df["Address Dec"][variable_index])
                    timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        
                    for database_index in database_df.index:
                        
                        influxDB = DBManager.InfluxDBmodel(server = 'http://' + str(database_df['IP'][database_index]) + ':' +  str(database_df['Port'][database_index]) + '/', org = database_df['Organization'][database_index], bucket = database_df['Bucket'][database_index], token = str(database_df['Token'][database_index]))
                        msg = influxDB.InfluxDBconnection()
                        influxDB.InfluxDBwriter( load = loads_df["Name"][load_index], variable =  variables_df["Name"][variable_index], value = value, timestamp = timestamp)
                        
        # Close Connection
        ModbusModel.ModbusClose()
        time.sleep(5)