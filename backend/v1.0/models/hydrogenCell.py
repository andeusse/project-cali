from flask import request
from flask_restful import Resource
from simulation_models import TwinCell
import pandas as pd
import numpy as np
from tools import DBManager
import os
import json

class hydrogenCell(Resource):
  def post(self):
    data = request.get_json()
    cell = {}

    trainingState = False
    DB_IP = os.getenv('DB_IP')
    DB_Port = os.getenv('DB_Port')
    DB_Bucket = os.getenv('DB_Bucket')
    DB_Organization = os.getenv('DB_Organization')
    DB_Token = os.getenv('DB_Token')

    influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)

    if not data["inputOfflineOperation"]:
      trainingState = data["trainingMode"]
      values_df = pd.DataFrame(columns=["field", "Value"])
      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503

      query = influxDB.QueryCreator(measurement='Hidrogeno', type=1)
      
      attempts = 1
      while attempts <= 5:
        try:
          # values_df_temp = influxDB.InfluxDBreader(query)
          values_df_temp = pd.concat(influxDB.InfluxDBreader(query))
          values_df['field'] = values_df_temp['_field']
          values_df['Value'] = values_df_temp['_value']
          timestamp = values_df_temp['_time'].mean()
          cell['timestamp'] = str(timestamp)
          values_df.set_index('field', inplace=True)
          influxDB.InfluxDBclose()
          break
        except:
          print(f"Intento: {attempts}", flush=True)
          attempts += 1
        finally:
          influxDB.InfluxDBclose()

    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = data["queryTime"] / 1000 # Delta de tiempo de la simulación en s -> se definen valores diferentes para offline y online
    
    if data["steps"]["value"] > 1:
      iteration = data["iteration"] * timeMultiplier
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
    electronicLoadMode = data["electronicLoadMode"]

    # if data["inputCellTemperature"]["arrayEnabled"]:
    #   inputCellTemperatureArray = np.repeat(np.array(data["inputCellTemperatureArray"]),repeats)
    #   if iteration <= len(inputCellTemperatureArray):
    #     inputCellTemperature = float(inputCellTemperatureArray[iteration-1])
    #   else:
    #     inputCellTemperature = float(inputCellTemperatureArray[-1])
    # else:
    #   inputCellTemperature = ((35.0 if not data["inputCellTemperature"]["value"] else data["inputCellTemperature"]["value"]) if not data["inputCellTemperature"]["disabled"] else round(values_df["Value"]['TE-101'],2))
    
    if data["inputFanPercentage"]["arrayEnabled"]:
      inputFanPercentageArray = np.repeat(np.array(data["inputFanPercentageArray"]),repeats)
      inputFanPercentage = float(inputFanPercentageArray[(iteration-1)-len(inputFanPercentageArray)*((iteration - 1)//len(inputFanPercentageArray))])
    else:
      inputFanPercentage = ((50.0 if not data["inputFanPercentage"]["value"] else data["inputFanPercentage"]["value"]) if not data["inputFanPercentage"]["disabled"] else round(values_df["Value"]['F-101'],2))

    if electronicLoadMode == "Current":
      if data["inputElectronicLoadCurrent"]["arrayEnabled"]:
        inputElectronicLoadCurrentArray = np.repeat(np.array(data["inputElectronicLoadCurrentArray"]),repeats)
        inputElectronicLoad = float(inputElectronicLoadCurrentArray[(iteration-1)-len(inputElectronicLoadCurrentArray)*((iteration - 1)//len(inputElectronicLoadCurrentArray))])
      else:
        inputElectronicLoad = ((0.0 if not data["inputElectronicLoadCurrent"]["value"] else data["inputElectronicLoadCurrent"]["value"]) if not data["inputElectronicLoadCurrent"]["disabled"] else round(values_df["Value"]['IM'],2))
      cell["inputElectronicLoadCurrent"] = inputElectronicLoad
    elif electronicLoadMode == "Power":
      if data["inputElectronicLoadPower"]["arrayEnabled"]:
        inputElectronicLoadPowerArray = np.repeat(np.array(data["inputElectronicLoadPowerArray"]),repeats)
        inputElectronicLoad = float(inputElectronicLoadPowerArray[(iteration-1)-len(inputElectronicLoadPowerArray)*((iteration - 1)//len(inputElectronicLoadPowerArray))])
      else:
        inputElectronicLoad = ((0.0 if not data["inputElectronicLoadPower"]["value"] else data["inputElectronicLoadPower"]["value"]) if not data["inputElectronicLoadPower"]["disabled"] else round(values_df["Value"]['CW'],2))
      cell["inputElectronicLoadPower"] = inputElectronicLoad
    elif electronicLoadMode == "Resistance":
      if data["inputElectronicLoadResistance"]["arrayEnabled"]:
          inputElectronicLoadResistanceArray = np.repeat(np.array(data["inputElectronicLoadResistanceArray"]),repeats)
          inputElectronicLoad = float(inputElectronicLoadResistanceArray[(iteration-1)-len(inputElectronicLoadResistanceArray)*((iteration - 1)//len(inputElectronicLoadResistanceArray))])
      else:
        inputElectronicLoad = ((2.0 if not data["inputElectronicLoadResistance"]["value"] else data["inputElectronicLoadResistance"]["value"]) if not data["inputElectronicLoadResistance"]["disabled"] else round(values_df["Value"]['CR'],2))
      cell["inputElectronicLoadResistance"] = inputElectronicLoad

    cellSelfFeeding = data["cellSelfFeeding"]
    lightsConnected = data["lightsConnected"]
    previousCellVoltage = data["simulatedCellVoltage"] if "simulatedCellVoltage" in data else 16.7
    previousGeneratedEnergy = data["simulatedGeneratedEnergy"] if "simulatedGeneratedEnergy" in data else 0.0

    connectionState = influxDB.InfluxDBconnection()
    if not connectionState:
      return {"message":influxDB.ERROR_MESSAGE}, 503
    queryConverter = influxDB.QueryCreator(measurement='Hidrogeno', device = "entrenamiento", variable = "eficiencia_convertidor_DC", type=0)
    queryCoefficients = influxDB.QueryCreator(measurement='Hidrogeno', device = "entrenamiento", variable = "coeficientes_voltaje_celda", type=0)
    attempts = 1
    while attempts <= 5:
      try:
        converterEfficiency = influxDB.InfluxDBreader(queryConverter)['_value'][0]
        voltageCoefficients = json.loads(influxDB.InfluxDBreader(queryCoefficients)['_value'][0])
        influxDB.InfluxDBclose()
        break
      except:
        converterEfficiency = 0.9
        voltageCoefficients = [1] * 9
        attempts += 1
      finally:
        influxDB.InfluxDBclose()

    if not data["inputOfflineOperation"]:
      hydrogenPressure = round(values_df["Value"]['PT-101'],2)
      cellTemperature = round(values_df["Value"]['TE-101'],2)
      if values_df["Value"]['LONOFF']:
        electronicLoadState = True
      else:
        electronicLoadState = False
      cellVoltage_meas = round(values_df["Value"]['VG-101'],3)
      cellCurrent_meas = round(values_df["Value"]['IG-101'],3)
      lightsPower = round(values_df["Value"]['PC-102'],2)
      cellSelfFeedingPower = round(values_df["Value"]['PC-101'],2)
      cellPower_meas = round(values_df["Value"]['PG-101'],2)
      electronicLoadPower_meas = round(values_df["Value"]['VM'],2) * round(values_df["Value"]['IM'])
    else:
      hydrogenPressure = 5.0
      cellTemperature = 40.0
      electronicLoadState = True
      if lightsMode == 'Parallel':
          lightsPower = 10.0
      elif lightsMode == 'Series':
          lightsPower = 4.0
      cellSelfFeedingPower = 11.0

    inputElectronicLoad = inputElectronicLoad * electronicLoadState
    lightsPower = lightsPower * lightsConnected
    cellSelfFeedingPower = cellSelfFeedingPower * cellSelfFeeding

    twinCell = TwinCell(name)
    twinCell.twinParameters(converterEfficiency, voltageCoefficients)
    
    if not data["inputOfflineOperation"] and data["inputFanPercentage"]["disabled"] and data["inputElectronicLoadCurrent"]["disabled"]:
      twinCell.optimal_voltageCoefficients(cellVoltage_meas, cellCurrent_meas, inputFanPercentage)
      twinCell.optimal_n_converter(cellSelfFeedingPower, lightsPower, cellPower_meas, electronicLoadPower_meas)

    results = twinCell.twinOutput(previousCellVoltage, inputFanPercentage, electronicLoadMode, inputElectronicLoad, lightsPower, cellSelfFeedingPower, previousGeneratedEnergy, delta_t * timeMultiplier)

    cell["hydrogenFlow"] = results[0]
    cell["cellCurrent"] = results[1]
    cell["cellVoltage"] = results[2]
    cell["cellPower"] = results[3]
    cell["electronicLoadVoltage"] = results[4]
    cell["electronicLoadCurrent"] = results[5]
    cell["electronicLoadPower"] = results[6]
    cell["cellEfficiency"] = results[7]
    cell["cellGeneratedEnergy"] = results[8]
    cell["converterEfficiency"] = results[9]
    cell["cellSelfFeedingPower"] = results[10]
    cell["lightsPower"] = results[11]
    cell["hydrogenPressure"] = hydrogenPressure
    cell["fanPercentage"] = inputFanPercentage
    cell["cellTemperature"] = cellTemperature
    cell["electronicLoadMode"] = electronicLoadMode

    if trainingState:

      influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
      connectionState = influxDB.InfluxDBconnection()
      
      influxDB.InfluxDBwriter( measurement = "Hidrogeno", device = "entrenamiento", variable = "eficiencia_convertidor_DC", value = twinCell.n_converter, timestamp = timestamp)
      influxDB.InfluxDBwriter( measurement = "Hidrogeno", device = "entrenamiento", variable = "coeficientes_voltaje_celda", value = str(twinCell.voltageCoefficients), timestamp = timestamp)

      influxDB.InfluxDBclose()

    return {"model": cell}
