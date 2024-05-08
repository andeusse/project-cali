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
      variables_df = database_dic['InfluxDBVariables']
      variables_df = variables_df.drop(variables_df[variables_df['Device'] != 'Módulo de turbinas'].index)
      values_df = pd.DataFrame(columns=["Tag", "Value"])
      values_df["Tag"] = variables_df["Tag"]
      values_df.set_index('Tag', inplace=True)

      influxDB_Connection = InfluxDbConnection()
      # Cambiar datos de conexión DB según corresponda en el excel. Eros = [0], Daniel = [1], Eusse = [2], checho = [3]
      db = 0
      influxDB_Connection.createConnection(server = 'http://' + str(database_df['IP'][db]) + ':' +  str(database_df['Port'][db]) + '/', org = database_df['Organization'][db], bucket = database_df['Bucket'][db], token = str(database_df['Token'][db]))
      influxDB = influxDB_Connection.data

      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503

      for index in variables_df.index:
          query = influxDB.QueryCreator(device= variables_df["Device"][index], variable= variables_df["Tag"][index], location= '', type= 0, forecastTime= 0)
          values_df.loc[variables_df["Tag"][index], "Value"] = influxDB.InfluxDBreader(query)[variables_df["Tag"][index]][0]
      influxDB.InfluxDBclose()

    name = data["name"]
    turbineType = 1 if data["turbineType"] == "Pelton" else 2
    inputPressure = (data["inputPressure"]["value"] if not data["inputPressure"]["disabled"] else round(values_df["Value"]['PT001'],2)) * 6.89476 # psi to kPa conversion
    inputFlow = (data["inputFlow"]["value"] if not data["inputFlow"]["disabled"] else round(values_df["Value"]['FIT001'],2)) / 60 # L/min to L/s conversion
    inputActivePower = data["inputActivePower"]["value"] if not data["inputActivePower"]["disabled"] else round(values_df["Value"]['PKW001'],2)
    inputPowerFactor = data["inputPowerFactor"]["value"] if not data["inputPowerFactor"]["disabled"] else round(values_df["Value"]['FP001'],2)
    inputDirectCurrentPower = 0.0 if data["inputDirectCurrentPower"] == False else 2.4
    
    turbine["inputActivePower"] = inputActivePower
    turbine["inputPowerFactor"] = inputPowerFactor

    batteryStateOfCharge = data["simulatedBatteryStateOfCharge"] if "simulatedBatteryStateOfCharge" in data else data["battery"]["stateOfCharge"]["value"]
    simulatedDirectCurrentVoltage  = data["simulatedDirectCurrentVoltage"] if "simulatedDirectCurrentVoltage" in data else 25.0
    simulatedInverterState = data["simulatedInverterState"] if "simulatedInverterState" in data else True
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
        T_bat = round(values_df["Value"]['TE003'],2)
        P_h_meas = round(values_df["Value"]['PG001'],2)
        P_CC_meas = round(values_df["Value"]['PB001'],2)
        V_t = round(values_df["Value"]['VG001'],2)
        simulatedDirectCurrentVoltage = round(values_df["Value"]['VB001'],2)
      else:
        T_bat = round(values_df["Value"]['TE004'],2)
        P_h_meas = round(values_df["Value"]['PG002'],2)
        P_CC_meas = round(values_df["Value"]['PB002'],2)
        V_t = round(values_df["Value"]['VG002'],2)
        simulatedDirectCurrentVoltage = round(values_df["Value"]['VB002'],2)

      V_CA = round(values_df["Value"]['VAC001'],2)
      simulatedSinkLoadState = bool(int(values_df["Value"]['ED001']))
      simulatedInverterState = bool(int(values_df["Value"]['EI001']))

      if data["inputPressure"]["disabled"]: turbine["inputPressure"] = round(inputPressure / 6.89476, 2) # kPa to psi conversion
      if data["inputFlow"]["disabled"]: turbine["inputFlow"] = round(inputFlow * 60, 2) # L/s to L/min conversion
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

    results = twinHydro.twinOutput(inputActivePower, simulatedInverterState, inputPowerFactor, inputDirectCurrentPower, T_bat, simulatedDirectCurrentVoltage, batteryStateOfCharge, 
                                     controllerChargeVoltageBulk, controllerChargeVoltageFloat, controllerChargingMinimunVoltage, simulatedSinkLoadState, controllerSinkOnVoltage, controllerSinkOffVoltage, 
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

    return {"model": turbine}