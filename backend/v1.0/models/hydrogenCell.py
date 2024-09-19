from flask import request
from flask_restful import Resource
from simulation_models import TwinCell
import pandas as pd
import numpy as np
from utils import InfluxDbConnection
from dotenv import load_dotenv
import os

class hydrogenCell(Resource):
  def post(self):
    data = request.get_json()
    cell = {}

    if not data["inputOfflineOperation"]:
      load_dotenv('./v1.0/.env')
      DB_IP = os.getenv('DB_IP')
      DB_Port = os.getenv('DB_Port')
      DB_Bucket = os.getenv('DB_Bucket')
      DB_Organization = os.getenv('DB_Organization')
      DB_Token = os.getenv('DB_Token')

      values_df = pd.DataFrame(columns=["field", "Value"])

      influxDB_Connection = InfluxDbConnection()
      influxDB_Connection.createConnection(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
      influxDB = influxDB_Connection.data

      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503

      query = influxDB.QueryCreator(measurement='Hidrogeno', type=1)
      values_df_temp = influxDB.InfluxDBreader(query)
      values_df_temp = pd.concat(influxDB.InfluxDBreader(query))
      values_df['field'] = values_df_temp['_field']
      values_df['Value'] = values_df_temp['_value']
      values_df.set_index('field', inplace=True)
      influxDB.InfluxDBclose()

    if data["steps"]["value"] > 1:
      iteration = data["iteration"]
      if data["stepUnit"] == "Second":
        repeats = data["stepTime"]["value"]
      elif data["stepUnit"] == "Minute":
        repeats = 60 * data["stepTime"]["value"]
      elif data["stepUnit"] == "Hour":
        repeats = 3600 * data["stepTime"]["value"]
      elif data["stepUnit"] == "Day":
        repeats = 86400 * data["stepTime"]["value"]

    name = data["name"]
    lightsMode = data["lightsMode"]

    if data["inputCellTemperature"]["arrayEnabled"]:
      inputCellTemperatureArray = np.repeat(np.array(data["inputCellTemperatureArray"]),repeats)
      if iteration <= len(inputCellTemperatureArray):
        inputCellTemperature = float(inputCellTemperatureArray[iteration-1])
      else:
        inputCellTemperature = float(inputCellTemperatureArray[-1])
    else:
      inputCellTemperature = ((35.0 if not data["inputCellTemperature"]["value"] else data["inputCellTemperature"]["value"]) if not data["inputCellTemperature"]["disabled"] else round(values_df["Value"]['TE-101'],2))
    if data["inputElectronicLoadCurrent"]["arrayEnabled"]:
      inputElectronicLoadCurrentArray = np.repeat(np.array(data["inputElectronicLoadCurrentArray"]),repeats)
      if iteration <= len(inputElectronicLoadCurrentArray):
        inputElectronicLoadCurrent = float(inputElectronicLoadCurrentArray[iteration-1])
      else:
        inputElectronicLoadCurrent = float(inputElectronicLoadCurrentArray[-1])
    else:
      inputElectronicLoadCurrent = ((2.0 if not data["inputElectronicLoadCurrent"]["value"] else data["inputElectronicLoadCurrent"]["value"]) if not data["inputElectronicLoadCurrent"]["disabled"] else round(values_df["Value"]['IM'],2))
    cellSelfFeeding = data["cellSelfFeeding"]
    lightsConnected = data["lightsConnected"]
    previousGeneratedEnergy = data["simulatedGeneratedEnergy"] if "simulatedGeneratedEnergy" in data else 0.0

    if not data["inputOfflineOperation"]:
      hydrogenPressure = round(values_df["Value"]['PT-101'],2)
      fanPercentage = round(values_df["Value"]['F-101'],2)
    else:
      hydrogenPressure = 5.0
      fanPercentage = 100.0


    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = data["queryTime"] / 1000 # Delta de tiempo de la simulación en s -> se definen valores diferentes para offline y online

    twinCell = twinCell(name)
    twinCell.lightsPower(lightsMode, lightsConnected)
    twinCell.twinParameters()

    results = twinCell.twinOutput(inputCellTemperature, inputElectronicLoadCurrent, cellSelfFeeding, previousGeneratedEnergy, delta_t * timeMultiplier)

    cell["hydrogenFlow"] = results[0]
    cell["cellCurrent"] = results[1]
    cell["cellVoltage"] = results[2]
    cell["cellPower"] = results[3]
    cell["electronicLoadVoltage"] = results[4]
    cell["electronicLoadPower"] = results[5]
    cell["cellSelfFeedingPower"] = results[6]
    cell["lightsPower"] = results[7]
    cell["cellEfficiency"] = results[8]
    cell["cellGeneratedEnergy"] = results[9]


    cell["hydrogenPressure"] = hydrogenPressure
    cell["fanPercentage"] = fanPercentage
    cell["cellTemperature"] = inputCellTemperature
    cell["electronicLoadMode"] = data["electronicLoadMode"]
    cell["electronicLoadCurrent"] = data["inputElectronicLoadCurrent"]["value"]


    return {"model": cell}