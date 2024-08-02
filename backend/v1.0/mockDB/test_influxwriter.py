import os
import sys
import inspect
from dotenv import load_dotenv

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
load_dotenv('v1.0\.env')
DB_IP = os.getenv('DB_IP')
DB_Port = os.getenv('DB_Port')
DB_Bucket = os.getenv('DB_Bucket')
DB_Organization = os.getenv('DB_Organization')
DB_Token = os.getenv('DB_Token')

from tools import DBManager
import pandas as pd
import time
from datetime import datetime
import random
import numpy as np

testValues_dfs = pd.read_excel('v1.0\mockDB\Devices_test.xlsx', sheet_name = None)

influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
msg = influxDB.InfluxDBconnection()


count = 0
while True:
    #database_df = pd.read_excel(r'.\Registros_Modbus.xlsx', sheet_name = 'ConexionDB')
    #testValues_dfs = pd.read_excel(r'.\Devices_test.xlsx', sheet_name = None)
    # database_df = pd.read_excel('v1.0\mockDB\Registros_Modbus.xlsx', sheet_name = 'ConexionDB')
    testValues_dfs = pd.read_excel('v1.0\mockDB\Devices_test.xlsx', sheet_name = None)
    
    for measurement in list(testValues_dfs.keys()):
        testValues_df = testValues_dfs[measurement]
        
        for index in testValues_df.index:
            
            timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))
            value = testValues_df["Value"][index] * random.uniform(1.0, 1.02)
            timesleep = 2
            if measurement == "BiogasPlant":
                timesleep = 30
                if index==18 or index==19 or index==32 or index==33 or index==37:
                    if count==0:
                        value = 0.1*np.log(count+0.1)+0.1
                    else:
                        value = 0.1*np.log(count)+0.1
                    if value>50:
                        count=0
                count=count+timesleep
            print(influxDB.InfluxDBwriter( measurement = testValues_df["measurement"][index], device = testValues_df["device"][index], variable =  testValues_df["field"][index], value = value, timestamp = timestamp))
    
        time.sleep(timesleep)