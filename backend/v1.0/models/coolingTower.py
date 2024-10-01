from flask import request
from flask_restful import Resource
from simulation_models import TwinTower
import pandas as pd
import numpy as np
from utils import InfluxDbConnection
from dotenv import load_dotenv
import os

class coolingTower(Resource):
  def post(self):
    data = request.get_json()
    tower = {}

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

      query = influxDB.QueryCreator(measurement='Planta_Torre_Enfriamiento', type=1)
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
    fillType = data["fillType"]
    towerArea = data["towerArea"]
    towerHeight = data["towerHeight"]
    nominalAirFlow = data["nominalAirFlow"]
    maximumAirPressure = data["maximumAirPressure"]
    nominalWaterFlow = data["nominalWaterFlow"]
    maximumWaterPressure = data["maximumWaterPressure"]

    if data["topWaterFlow"]["arrayEnabled"]:
      topWaterFlowArray = np.repeat(np.array(data["topWaterFlowArray"]),repeats)
      if iteration <= len(topWaterFlowArray):
        topWaterFlow = float(topWaterFlowArray[iteration-1] / 60000) # L/min to m3/s conversion
      else:
        topWaterFlow = float(topWaterFlowArray[-1] / 60000) # L/min to m3/s conversion
    else:
      topWaterFlow = ((1.0 if not data["topWaterFlow"]["value"] and data["topWaterFlow"]["value"]!=0 else data["topWaterFlow"]["value"]) if not data["topWaterFlow"]["disabled"] else round(values_df["Value"]['FT-102'],2)) / 60000 # L/min to m3/s conversion
    if data["topWaterTemperature"]["arrayEnabled"]:
      topWaterTemperatureArray = np.repeat(np.array(data["topWaterTemperatureArray"]),repeats)
      if iteration <= len(topWaterTemperatureArray):
        topWaterTemperature = float(topWaterTemperatureArray[iteration-1] + 273.15) # °C to kelvin conversion
      else:
        topWaterTemperature = float(topWaterTemperatureArray[-1] + 273.15) # °C to kelvin conversion
    else:
      topWaterTemperature = ((35.0 if not data["topWaterTemperature"]["value"] and data["topWaterTemperature"]["value"]!=0 else data["topWaterTemperature"]["value"]) if not data["topWaterTemperature"]["disabled"] else round(values_df["Value"]['TE-104'],2)) + 273.15 # °C to kelvin conversion
    if data["bottomAirFlow"]["arrayEnabled"]:
      bottomAirFlowArray = np.repeat(np.array(data["bottomAirFlowArray"]),repeats)
      if iteration <= len(bottomAirFlowArray):
        bottomAirFlow = float(bottomAirFlowArray[iteration-1] / 60) # m3/min to m3/s conversion
      else:
        bottomAirFlow = float(bottomAirFlowArray[-1] / 60) # m3/min to m3/s conversion
    else:
      bottomAirFlow = ((2.0 if not data["bottomAirFlow"]["value"] and data["bottomAirFlow"]["value"]!=0 else data["bottomAirFlow"]["value"]) if not data["bottomAirFlow"]["disabled"] else round(values_df["Value"]['FT-101'],2)) / 60 # m3/min to m3/s conversion
    if data["bottomAirTemperature"]["arrayEnabled"]:
      bottomAirTemperatureArray = np.repeat(np.array(data["bottomAirTemperatureArray"]),repeats)
      if iteration <= len(bottomAirTemperatureArray):
        bottomAirTemperature = float(bottomAirTemperatureArray[iteration-1] + 273.15) # °C to kelvin conversion
      else:
        bottomAirTemperature = float(bottomAirTemperatureArray[-1] + 273.15) # °C to kelvin conversion
    else:
      bottomAirTemperature = ((25.0 if not data["bottomAirTemperature"]["value"] and data["bottomAirTemperature"]["value"]!=0 else data["bottomAirTemperature"]["value"]) if not data["bottomAirTemperature"]["disabled"] else round(values_df["Value"]['TE-101'],2)) + 273.15 # °C to kelvin conversion
    if data["bottomAirHumidity"]["arrayEnabled"]:
      bottomAirHumidityArray = np.repeat(np.array(data["bottomAirHumidityArray"]),repeats)
      if iteration <= len(bottomAirHumidityArray):
        bottomAirHumidity = float(bottomAirHumidityArray[iteration-1])
      else:
        bottomAirHumidity = float(bottomAirHumidityArray[-1])
    else:
      bottomAirHumidity = ((80.0 if not data["bottomAirHumidity"]["value"] and data["bottomAirHumidity"]["value"]!=0 else data["bottomAirHumidity"]["value"]) if not data["bottomAirHumidity"]["disabled"] else round(values_df["Value"]['AT-101'],2))
    atmosphericPressure = ((90.0 if not data["atmosphericPressure"]["value"] else data["atmosphericPressure"]["value"]) if not data["atmosphericPressure"]["disabled"] else round(values_df["Value"]['PT-102'],2)) * 1000 # kPa to Pa conversion
    previousEnergyApplied = data["simulatedEnergyAppliedToWater"] if "simulatedEnergyAppliedToWater" in data else 0.0

    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = data["queryTime"] / 1000 # Delta de tiempo de la simulación en s -> se definen valores diferentes para offline y online
    
    twinTower = TwinTower(name)
    twinTower.twinParameters()
    results = twinTower.twinOutput(fillType, topWaterFlow, topWaterTemperature, bottomAirFlow, bottomAirTemperature, bottomAirHumidity, atmosphericPressure, previousEnergyApplied, delta_t * timeMultiplier)

    tower["bottomWaterTemperature"] = results[0] - 273.15
    tower["waterTemperatureReduction"] = results[1]
    tower["topAirTemperature"] = results[2] - 273.15
    tower["topAirHumidity"] = results[3]
    tower["airTemperatureRise"] = results[4]
    tower["powerAppliedToWater"] = results[5]
    tower["energyAppliedToWater"] = results[6]
    tower["deltaPressure"] = results[7]

    tower["topWaterFlow"] = topWaterFlow * 60000
    tower["topWaterTemperature"] = topWaterTemperature - 273.15
    tower["bottomAirFlow"] = bottomAirFlow * 60
    tower["bottomAirTemperature"] = bottomAirTemperature - 273.15
    tower["bottomAirHumidity"] = bottomAirHumidity
    tower["atmosphericPressure"] = atmosphericPressure / 1000

    return {"model": tower}