from flask import request
from flask_restful import Resource
from simulation_models import TwinHydro
import pandas as pd
import time
from utils import ExcelReader
from utils import InfluxDbConnection

class Turbine(Resource):
  def post(self):
    data = request.get_json()

    if not data["inputOfflineOperation"]:
      timeStart = time.time()
      excelReader = ExcelReader()
      excelReader.read_excel('./v1.0/tools/DB_Mapping.xlsx', None)
      database_dic = excelReader.data
      database_df = database_dic['ConexionDB']
      testValues_df = database_dic['InfluxDBVariables']
      values_df = pd.DataFrame(columns=["Tag", "Value"])
      values_df["Tag"] = testValues_df["Tag"]
      values_df.set_index('Tag', inplace=True)

      # Cambiar línea de modelo de DB según corresponda en el excel. Eros = [0], Daniel = [1], Eusse (?) = [2]
      # influxDB = DBManager.InfluxDBmodel(server = 'http://' + str(database_df['IP'][0]) + ':' +  str(database_df['Port'][0]) + '/', org = database_df['Organization'][0], bucket = database_df['Bucket'][0], token = str(database_df['Token'][0]))
      # influxDB = DBManager.InfluxDBmodel(server = 'http://' + str(database_df['IP'][1]) + ':' +  str(database_df['Port'][1]) + '/', org = database_df['Organization'][1], bucket = database_df['Bucket'][1], token = str(database_df['Token'][1]))
      # influxDB = DBManager.InfluxDBmodel(server = 'http://' + str(database_df['IP'][2]) + ':' +  str(database_df['Port'][2]) + '/', org = database_df['Organization'][2], bucket = database_df['Bucket'][2], token = str(database_df['Token'][2]))
      
      influxDB_Connection = InfluxDbConnection()
      influxDB_Connection.createConnection(server = 'http://' + str(database_df['IP'][0]) + ':' +  str(database_df['Port'][0]) + '/', org = database_df['Organization'][0], bucket = database_df['Bucket'][0], token = str(database_df['Token'][0]))
      influxDB = influxDB_Connection.data

      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503

      for index in testValues_df.index:
          query = influxDB.QueryCreator(device= testValues_df["Device"][index], variable= testValues_df["Tag"][index], location= '', type= 0, forecastTime= 0)
          values_df.loc[testValues_df["Tag"][index], "Value"] = influxDB.InfluxDBreader(query)[testValues_df["Tag"][index]][0]
      influxDB.InfluxDBclose()

      timeFinish = time.time()
      print((timeFinish-timeStart)*1000)

    name = data["name"]
    turbineType = 1 if data["turbineType"] == "Pelton" else 2
    inputPressure = data["inputPressure"]["value"] if not data["inputPressure"]["disabled"] else round(values_df["Value"]['PT001'],2)
    inputFlow = data["inputFlow"]["value"] if not data["inputFlow"]["disabled"] else round(values_df["Value"]['FIT001'],2)
    inputActivePower = data["inputActivePower"]["value"] if not data["inputActivePower"]["disabled"] else round(values_df["Value"]['PKW001'],2)
    inputPowerFactor = data["inputPowerFactor"]["value"] if not data["inputPowerFactor"]["disabled"] else round(values_df["Value"]['FP001'],2)
    inputDirectCurrentPower = 0.0 if data["inputDirectCurrentPower"] == False else 2.4
    
    batteryStateOfCharge = data["simulatedBatteryStateOfCharge"] if "simulatedBatteryStateOfCharge" in data else data["batteryStateOfCharge"]["value"]
    simulatedDirectCurrentVoltage  = data["simulatedDirectCurrentVoltage"] if "simulatedDirectCurrentVoltage" in data else 25.0
    simulatedInverterState = data["simulatedInverterState"] if "simulatedInverterState" in data else True
    if "simulatedSinkLoadState" in data:
      simulatedSinkLoadState = data["simulatedSinkLoadState"]
    elif data["sinkLoadInitialState"] == "Apagada":
      simulatedSinkLoadState = False
    else:
      simulatedSinkLoadState = True

    controllerChargeVoltageBulk = data["controllerChargeVoltageBulk"]["value"]
    controllerChargeVoltageFloat = data["controllerChargeVoltageFloat"]["value"]
    controllerChargingMinimunVoltage = data["controllerChargingMinimunVoltage"]["value"]
    controllerSinkOnVoltage = data["controllerSinkOnVoltage"]["value"]
    controllerSinkOffVoltage = data["controllerSinkOffVoltage"]["value"]
    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = 1.0 # Delta de tiempo de la simulación en s -> se define un valor por defecto

    controllerEfficiency = data["controllerEfficiency"]["value"]
    inverterEfficiency = data["inverterEfficiency"]["value"]

    twinHydro = TwinHydro(name)

    turbine = {}

    if not data["inputOfflineOperation"]:
      T_bat = round(values_df["Value"]['TE003'],2)
      simulatedInverterState = bool(int(values_df["Value"]['EI001']))
      P_h_meas = round(values_df["Value"]['PG001'],2)
      P_CC_meas = round(values_df["Value"]['VB001'] * values_df["Value"]['IC001'],2)
      V_CA = round(values_df["Value"]['VAC001'],2)
      V_t = round(values_df["Value"]['VG001'],2)
      simulatedDirectCurrentVoltage = round(values_df["Value"]['VB001'],2)
      simulatedSinkLoadState = bool(int(values_df["Value"]['ED001']))
      simulatedInverterState = bool(int(values_df["Value"]['EI001']))

      turbine["batteryTemperature"] = T_bat
      if data["inputPressure"]["disabled"]: turbine["inputPressure"] = inputPressure
      if data["inputFlow"]["disabled"]: turbine["inputFlow"] = inputFlow
      if data["inputActivePower"]["disabled"]: turbine["inputActivePower"] = inputActivePower
      if data["inputPowerFactor"]["disabled"]: turbine["inputPowerFactor"] = inputPowerFactor
    else:
      T_bat = 30.0
      V_CA = 0
      V_t = 0

    twinHydro.turbineType(turbineType)
    P_h = twinHydro.PowerOutput(inputPressure, inputFlow)
    twinHydro.twinParameters(controllerEfficiency, inverterEfficiency)
    
    if not data["inputOfflineOperation"] and not data["inputPressure"]["disabled"] and data["inputFlow"]["disabled"]:
      twinHydro.optimal_n_t(twinHydro.n_t, P_h_meas, inputPressure, inputFlow)
      P_h = twinHydro.PowerOutput(inputPressure, inputFlow)
      twinHydro.optimal_n_controller(controllerEfficiency, P_h, inputDirectCurrentPower, P_CC_meas)

    results = twinHydro.twinOutput(inputActivePower, simulatedInverterState, inputPowerFactor, inputDirectCurrentPower, T_bat, simulatedDirectCurrentVoltage, batteryStateOfCharge, 
                                     controllerChargeVoltageBulk, controllerChargeVoltageFloat, controllerChargingMinimunVoltage, simulatedSinkLoadState, controllerSinkOnVoltage, controllerSinkOffVoltage, delta_t*timeMultiplier, V_t, V_CA)

    turbine["turbinePower"] = P_h

    turbine["controllerPower"] = results[0]
    turbine["inverterInputPower"] = results[1]
    turbine["batteryPower"] = results[2]
    turbine["turbineVoltage"] = results[3]
    turbine["inverterOutputVoltage"] = results[4]
    turbine["batteryStateOfCharge"] = results[5]
    turbine["batteryVoltage"] = results[6]
    turbine["directCurrentVoltage"] = results[7]
    turbine["sinkLoadState"] = results[8]
    turbine["sinkLoadPower"] = results[9]
    turbine["inverterApparentPower"] = results[10]
    turbine["inverterActivePower"] = results[11]
    turbine["inverterReactivePower"] = results[12]
    turbine["inverterState"] = results[13]
    turbine["turbineCurrent"] = results[14]
    turbine["controllerCurrent"] = results[15]
    turbine["batteryCurrent"] = results[16]
    turbine["inverterOutputCurrent"] = results[17]
    turbine["inverterInputCurrent"] = results[18]

    return {"model": turbine}