from flask import request
from flask_restful import Resource
from simulation_models import TwinTower
import pandas as pd
from utils import InfluxDbConnection
from dotenv import load_dotenv
import os

class coolingTower(Resource):
  def post(self):
    data = request.get_json()
    load_dotenv('v1.0\.env')
    DB_IP = os.getenv('DB_IP')
    DB_Port = os.getenv('DB_Port')
    DB_Bucket = os.getenv('DB_Bucket')
    DB_Organization = os.getenv('DB_Organization')
    DB_Token = os.getenv('DB_Token')
    tower = {}

    if not data["inputOfflineOperation"]:
      values_df = pd.DataFrame(columns=["field", "Value"])

      influxDB_Connection = InfluxDbConnection()
      influxDB_Connection.createConnection(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
      influxDB = influxDB_Connection.data

      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503

      query = influxDB.QueryCreator(measurement='Torre_enfriamiento', type=1)
      values_df_temp = influxDB.InfluxDBreader(query)
      values_df['field'] = values_df_temp['_field']
      values_df['Value'] = values_df_temp['_value']
      values_df.set_index('field', inplace=True)
      influxDB.InfluxDBclose()

    name = data["name"]
    fillType = data["fillType"]
    towerArea = data["towerArea"]
    towerHeight = data["towerHeight"]
    nominalAirFlow = data["nominalAirFlow"]
    maximumAirPressure = data["maximumAirPressure"]
    nominalWaterFlow = data["nominalWaterFlow"]
    maximumWaterPressure = data["maximumWaterPressure"]

    topWaterFlow = ((1.0 if not data["topWaterFlow"]["value"] else data["topWaterFlow"]["value"]) if not data["topWaterFlow"]["disabled"] else round(values_df["Value"]['FT-102'],2)) / 60000 # L/min to m3/s conversion
    topWaterTemperature = ((50.0 if not data["topWaterTemperature"]["value"] else data["topWaterTemperature"]["value"]) if not data["topWaterTemperature"]["disabled"] else round(values_df["Value"]['TE-104'],2)) + 273.15 # °C to kelvin conversion
    bottomAirFlow = ((13 if not data["bottomAirFlow"]["value"] else data["bottomAirFlow"]["value"]) if not data["bottomAirFlow"]["disabled"] else round(values_df["Value"]['FT-101'],2)) / 60 # m3/min to m3/s conversion
    bottomAirTemperature = ((25.0 if not data["bottomAirTemperature"]["value"] else data["bottomAirTemperature"]["value"]) if not data["bottomAirTemperature"]["disabled"] else round(values_df["Value"]['TE-101'],2)) + 273.15 # °C to kelvin conversion
    bottomAirHumidity = ((80.0 if not data["bottomAirHumidity"]["value"] else data["bottomAirHumidity"]["value"]) if not data["bottomAirHumidity"]["disabled"] else round(values_df["Value"]['AT-101'],2))
    atmosphericPressure = ((101.3 if not data["atmosphericPressure"]["value"] else data["atmosphericPressure"]["value"]) if not data["atmosphericPressure"]["disabled"] else round(values_df["Value"]['PT-102'],2)) * 1000 # kPa to Pa conversion
    previousEnergyApplied = data["simulatedEnergyAppliedToWater"] if "simulatedEnergyAppliedToWater" in data else 0.0

    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = data["queryTime"] / 1000 # Delta de tiempo de la simulación en s -> se definen valores diferentes para offline y online

    twinTower = TwinTower(name)
    twinTower.fillType(fillType)
    twinTower.twinParameters()

    results = twinTower.twinOutput(topWaterFlow, topWaterTemperature, bottomAirFlow, bottomAirTemperature, bottomAirHumidity, atmosphericPressure, previousEnergyApplied, delta_t * timeMultiplier)

    tower["bottomWaterTemperature"] = results[0] - 273.15
    tower["waterTemperatureReduction"] = results[1]
    tower["topAirTemperature"] = results[2] - 273.15
    tower["topAirHumidity"] = results[3]
    tower["airTemperatureRise"] = results[4]
    tower["powerAppliedToWater"] = results[5]
    tower["energyAppliedToWater"] = results[6]

    tower["topWaterFlow"] = topWaterFlow * 60000
    tower["topWaterTemperature"] = topWaterTemperature - 273.15
    tower["bottomAirFlow"] = bottomAirFlow * 60
    tower["bottomAirTemperature"] = bottomAirTemperature - 273.15
    tower["bottomAirHumidity"] = bottomAirHumidity
    tower["deltaPressure"] = 0.0

    return {"model": tower}