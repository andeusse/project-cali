import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from tools import DBManager
import pandas as pd
import time
from datetime import datetime
import random
import numpy as np

database_df = pd.read_excel('v1.0\mockDB\Registros_Modbus.xlsx', sheet_name = 'ConexionDB')
testValues_dfs = pd.read_excel('v1.0\mockDB\Devices_test.xlsx', sheet_name = None)

database_index = 3
influxDB = DBManager.InfluxDBmodel(server = 'http://' + str(database_df['IP'][database_index]) + ':' +  str(database_df['Port'][database_index]) + '/', org = database_df['Organization'][database_index], bucket = database_df['Bucket'][database_index], token = str(database_df['Token'][database_index]))
msg = influxDB.InfluxDBconnection()

count = 0

while True:
    database_df = pd.read_excel('v1.0\mockDB\Registros_Modbus.xlsx', sheet_name = 'ConexionDB')
    testValues_df = pd.read_excel('v1.0\mockDB\Devices_test.xlsx', sheet_name = "Hoja2")
    
    #for measurement in list(testValues_dfs.keys()):
    #    testValues_df = testValues_dfs[measurement]

    for index in testValues_df.index:
        timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
        value = testValues_df["Value"][index] * random.uniform(1.0, 1.02)
        timesleep = 0
        # if measurement == "Hoja2":
        #     print(testValues_df["measurement"][index])
        timesleep = 30
        if index==51 or index==52 or index==68 or index==69 or index==76:
            if count==0:
                value = 0.1*np.log(count+0.1)+0.1
            else:
                value = 0.1*np.log(count)+0.1
            if value>50:
                count=0
        elif index == 13:
            value = float(int(value))
        count=count+timesleep
        print(influxDB.InfluxDBwriter( measurement = testValues_df["measurement"][index], device = testValues_df["device"][index], variable =  testValues_df["field"][index], value = value, timestamp = timestamp))
    print("success")
    time.sleep(timesleep)