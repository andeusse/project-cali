import DBManager
import pandas as pd
import time
from datetime import datetime
import random




while True:
    
    database_df = pd.read_excel('.\Registros_Modbus.xlsx', sheet_name = 'ConexionDB')
    testValues_dfs = pd.read_excel('.\Devices_test.xlsx', sheet_name = None)
    
    for device in list(testValues_dfs.keys()):
        testValues_df = testValues_dfs[device]
        for index in testValues_df.index:
            for database_index in database_df.index:
                influxDB = DBManager.InfluxDBmodel(server = 'http://' + str(database_df['IP'][database_index]) + ':' +  str(database_df['Port'][database_index]) + '/', org = database_df['Organization'][database_index], bucket = database_df['Bucket'][database_index], token = str(database_df['Token'][database_index]))
                msg = influxDB.InfluxDBconnection()
                timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
                value = testValues_df["Value"][index] * random.uniform(1.0, 1.02)
                print(influxDB.InfluxDBwriter( load = testValues_df["Device"][index], variable =  testValues_df["Tag"][index], value = value, timestamp = timestamp))
    
        time.sleep(2)
