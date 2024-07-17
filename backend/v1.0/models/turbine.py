from flask import request
from flask_restful import Resource
from simulation_models import TwinHydro
import pandas as pd
from utils import ExcelReader
from utils import InfluxDbConnection

class Turbine(Resource):
  def post(self):
    data = request.get_json()
    turbine = {}

    if not data["inputOfflineOperation"]:
      excelReader = ExcelReader()
      excelReader.read_excel('./v1.0/tools/DB_Mapping.xlsx', None)
      database_dic = excelReader.data
      database_df = database_dic['ConexionDB']
      values_df = pd.DataFrame(columns=["field", "Value"])

      influxDB_Connection = InfluxDbConnection()
      # Cambiar datos de conexión DB según corresponda en el excel. Eros = [0], Daniel = [1], Eusse = [2], checho = [3]
      db = 0
      influxDB_Connection.createConnection(server = 'http://' + str(database_df['IP'][db]) + ':' +  str(database_df['Port'][db]) + '/', org = database_df['Organization'][db], bucket = database_df['Bucket'][db], token = str(database_df['Token'][db]))
      influxDB = influxDB_Connection.data

      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503

      query = influxDB.QueryCreator(measurement='Turbinas', type=1)
      values_df_temp = influxDB.InfluxDBreader(query)
      values_df['field'] = values_df_temp['_field']
      values_df['Value'] = values_df_temp['_value']
      values_df.set_index('field', inplace=True)
      influxDB.InfluxDBclose()

    name = data["name"]
    turbineType = 1 if data["turbineType"] == "Pelton" else 2
    inputPressure = ((0.0 if not data["inputPressure"]["value"] else data["inputPressure"]["value"]) if not data["inputPressure"]["disabled"] else round(values_df["Value"]['PT-001'],2)) * 9.8064 # mH2O to kPa conversion
    inputFlow = (0.0 if not data["inputFlow"]["value"] else data["inputFlow"]["value"]) if not data["inputFlow"]["disabled"] else round(values_df["Value"]['FT-001'],2)
    inputActivePower = (0.0 if not data["inputActivePower"]["value"] else data["inputActivePower"]["value"]) if not data["inputActivePower"]["disabled"] else round(values_df["Value"]['PKW-002'],2)
    inputPowerFactor = (1.0 if not data["inputPowerFactor"]["value"] else data["inputPowerFactor"]["value"]) if not data["inputPowerFactor"]["disabled"] else round(values_df["Value"]['FP-001'],2)
    inputDirectCurrentPower = 0.0 if data["inputDirectCurrentPower"] == False else 2.4
    
    turbine["inputActivePower"] = inputActivePower
    turbine["inputPowerFactor"] = inputPowerFactor

    batteryState = data['isBatteryConnected']
    batteryStateOfCharge = data["simulatedBatteryStateOfCharge"] if "simulatedBatteryStateOfCharge" in data else data["battery"]["stateOfCharge"]["value"]
    chargeCycleInitialSOC = data['simulatedChargeCycleInitialSOC'] if 'simulatedChargeCycleInitialSOC' in data else data["battery"]["stateOfCharge"]["value"]
    simulatedInverterState = data["simulatedInverterState"] if "simulatedInverterState" in data else True
    sinkLoadMode = data['sinkLoadMode']
    if "simulatedSinkLoadState" in data:
      simulatedSinkLoadState = data["simulatedSinkLoadState"]
    elif data["controller"]["sinkLoadInitialState"] == "Apagada":
      simulatedSinkLoadState = False
    else:
      simulatedSinkLoadState = True

    controllerChargeVoltageBulk = data["controller"]["chargeVoltageBulk"]["value"]
    controllerChargeVoltageFloat = data["controller"]["chargeVoltageFloat"]["value"]
    controllerChargingMinimunVoltage = data["controller"]["chargingMinimunVoltage"]["value"]
    controllerSinkOnVoltage = data["controller"]["sinkOnVoltage"]["value"]
    controllerSinkOffVoltage = data["controller"]["sinkOffVoltage"]["value"]
    controllerEfficiency = data["controller"]["efficiency"]["value"]

    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = data["queryTime"] / 1000 # Delta de tiempo de la simulación en s -> se definen valores diferentes para offline y online

    inverterEfficiency = data["inverterEfficiency"]["value"]

    twinHydro = TwinHydro(name)

    if not data["inputOfflineOperation"]:
      if data["turbineType"] == "Pelton":
        T_bat = round(values_df["Value"]['TE-003'],2)
        P_h_meas = round(values_df["Value"]['PG-001'],2)
        P_CC_meas = round(values_df["Value"]['PC-001'],2)
        V_t = round(values_df["Value"]['VG-001'],2)
        simulatedDirectCurrentVoltage = round(values_df["Value"]['VB-001'],2)
        simulatedSinkLoadState = bool(int(values_df["Value"]['AUX-1001']))
      else:
        T_bat = round(values_df["Value"]['TE-004'],2)
        P_h_meas = round(values_df["Value"]['PG-002'],2)
        P_CC_meas = round(values_df["Value"]['PC-002'],2)
        V_t = round(values_df["Value"]['VG-002'],2)
        simulatedDirectCurrentVoltage = round(values_df["Value"]['VB-002'],2)
        simulatedSinkLoadState = bool(int(values_df["Value"]['AUX-1002']))

      V_CA = round(values_df["Value"]['VAC-002'],2)
      simulatedInverterState = bool(int(values_df["Value"]['EI-001']))

      if data["inputPressure"]["disabled"]: turbine["inputPressure"] = round(inputPressure / 9.8064, 2) # kPa to mH2O conversion
      if data["inputFlow"]["disabled"]: turbine["inputFlow"] = round(inputFlow, 2)
    else:
      T_bat = 30.0
      V_CA = 0
      V_t = 0
    
    turbine["batteryTemperature"] = T_bat

    twinHydro.turbineType(turbineType)
    P_h = twinHydro.PowerOutput(inputPressure, inputFlow)
    twinHydro.twinParameters(controllerEfficiency, inverterEfficiency)
    
    if not data["inputOfflineOperation"] and data["inputPressure"]["disabled"] and data["inputFlow"]["disabled"]:
      twinHydro.optimal_n_t(twinHydro.n_t, P_h_meas, inputPressure, inputFlow)
      P_h = twinHydro.PowerOutput(inputPressure, inputFlow)
      twinHydro.optimal_n_controller(controllerEfficiency, P_h, inputDirectCurrentPower, P_CC_meas)
    
    turbine["controllerEfficiency"] = twinHydro.n_controller
    turbine["inverterEfficiency"] = twinHydro.n_inverter

    if "simulatedDirectCurrentVoltage" in data:
      simulatedDirectCurrentVoltage = data["simulatedDirectCurrentVoltage"]
    else:
      P_CC = (P_h * twinHydro.n_controller / 100) - inputDirectCurrentPower
      P_inv = (inputActivePower / abs(inputPowerFactor)) / (twinHydro.n_inverter / 100)
      P_bat = P_CC - P_inv
      if P_bat < 0.0:
        batteryCurrent = abs(P_bat / 25.21)
        if batteryCurrent <= 7.5:
          initialVoltage = 25.92
        elif batteryCurrent <= 15:
          initialVoltage = 25.68
        elif batteryCurrent <= 37.5:
          initialVoltage = 25.13
        elif batteryCurrent <= 82.5:
          initialVoltage = 24.84
        else:
          initialVoltage = 24.48
        simulatedDirectCurrentVoltage = initialVoltage
      else:
        if batteryStateOfCharge >= 50:
          simulatedDirectCurrentVoltage = 24.6
        else:
          simulatedDirectCurrentVoltage = 24.0

    results = twinHydro.twinOutput(chargeCycleInitialSOC, batteryState, inputActivePower, simulatedInverterState, inputPowerFactor, inputDirectCurrentPower, T_bat, simulatedDirectCurrentVoltage, batteryStateOfCharge, 
                                     controllerChargeVoltageBulk, controllerChargeVoltageFloat, controllerChargingMinimunVoltage, sinkLoadMode, simulatedSinkLoadState, controllerSinkOnVoltage, controllerSinkOffVoltage, 
                                     delta_t*timeMultiplier, V_t, V_CA)

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
    turbine["directCurrentLoadPower"] = results[19]
    turbine["directCurrentLoadVoltage"] = results[20]
    turbine["directCurrentLoadCurrent"] = results[21]*1000
    turbine['batteryState'] = batteryState

    if turbine["batteryPower"] <= 0.0:
      turbine["chargeCycleInitialSOC"] = turbine["batteryStateOfCharge"]
    else:
      turbine["chargeCycleInitialSOC"] = chargeCycleInitialSOC

    return {"model": turbine}