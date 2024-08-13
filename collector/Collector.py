import pandas as pd
import DBManager
import ModbusManager
import time
from datetime import datetime
import logging
from dotenv import load_dotenv
import os

# %%

load_dotenv('.env')
DB_IP = os.getenv('DB_IP')
DB_Port = os.getenv('DB_Port')
DB_Bucket = os.getenv('DB_Bucket')
DB_Organization = os.getenv('DB_Organization')
DB_Token = os.getenv('DB_Token')

#%%

database_df = pd.read_excel('Registros_Modbus.xlsx', sheet_name = 'ConexionDB')
analyzers_df = pd.read_excel('Registros_Modbus.xlsx', sheet_name = 'ConexionAnalizadores')
loads_df = pd.read_excel('Registros_Modbus.xlsx', sheet_name = 'Cargas')
variables_df = pd.read_excel('Registros_Modbus.xlsx', sheet_name = 'Variables')
logger = logging.getLogger('Collector')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

#%%
while True:
    for analyzer_index in analyzers_df.index:
        ModbusModel = ModbusManager.ModbusModel(str(analyzers_df['IP'][analyzer_index]), int(analyzers_df['Port'][analyzer_index]))
        
        try:
        # Open Connection 
          logger.info("Intentando conexión con equipos modbus")
          ModbusModel.ModbusConnection()
          
          for load_index in range(len(loads_df)):
              
              if loads_df["Analyzer"][load_index] == analyzers_df['Name'][analyzer_index]:
              
                  for variable_index in variables_df.index:
                    if load_index != 0 and variable_index == 141:
                        break
                    value = ModbusModel.ModbusReader(loads_df["Unit ID"][load_index], variables_df["Address Dec"][variable_index], variables_df["Word"][variable_index], variables_df["Scale"][variable_index], variables_df["Format"][variable_index])
                    
                    # print(type(value))
                    # print(variables_df["Address Dec"][variable_index])
                    timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
   
                    influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
                    msg = influxDB.InfluxDBconnection()
                    influxDB.InfluxDBwriter( measurement = analyzers_df["Name"][analyzer_index], device = loads_df["Name"][load_index], variable =  variables_df["field"][variable_index], value = value, timestamp = timestamp)
        except:
          logger.error("No se pudo conectar al equipo modbus")
                      
        # Close Connection
        ModbusModel.ModbusClose()
        time.sleep(5)