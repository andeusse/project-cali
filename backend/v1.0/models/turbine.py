from flask import request
from flask_restful import Resource
from simulation_models import Twin_Hydro
import pandas as pd
from tools import DBManager

class Turbine(Resource):
  def post(self):
    data = request.get_json()

    if not data["inputOfflineOperation"]:
      database_df = pd.read_excel('./v1.0/tools/Registros_Modbus.xlsx', sheet_name = 'ConexionDB')
      testValues_df = pd.read_excel('./v1.0/tools/Hydro_test.xlsx', sheet_name = 'Hoja1')
      values_df = pd.DataFrame(columns=["Tag", "Value"])
      values_df["Tag"] = testValues_df["Tag"]
      values_df.set_index('Tag', inplace=True)
      influxDB = DBManager.InfluxDBmodel(server = 'http://' + str(database_df['IP'][0]) + ':' +  str(database_df['Port'][0]) + '/', org = database_df['Organization'][0], bucket = database_df['Bucket'][0], token = str(database_df['Token'][0]))
      # influxDB = DBManager.InfluxDBmodel(server = 'http://' + str(database_df['IP'][1]) + ':' +  str(database_df['Port'][1]) + '/', org = database_df['Organization'][1], bucket = database_df['Bucket'][1], token = str(database_df['Token'][1]))
      # influxDB = DBManager.InfluxDBmodel(server = 'http://' + str(database_df['IP'][2]) + ':' +  str(database_df['Port'][2]) + '/', org = database_df['Organization'][2], bucket = database_df['Bucket'][2], token = str(database_df['Token'][2]))
      connectionState = influxDB.InfluxDBconnection()
      print(connectionState)
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503

      for index in testValues_df.index:
          query = influxDB.QueryCreator(device= testValues_df["Device"][index], variable= testValues_df["Tag"][index], location= '', type= 0, forecastTime= 0)
          values_df.loc[testValues_df["Tag"][index], "Value"] = influxDB.InfluxDBreader(query)[testValues_df["Tag"][index]][0]

    name = data["name"]
    turbineType = 1 if data["turbineType"] == "Pelton" else 2
    pressure = data["inputPressure"]["value"] if not data["inputPressure"]["disabled"] else round(values_df["Value"]['PT001'],2)
    flux = data["inputFlow"]["value"] if not data["inputFlow"]["disabled"] else round(values_df["Value"]['FIT001'],2)
    P_CA = data["inputActivePower"]["value"] if not data["inputActivePower"]["disabled"] else round(values_df["Value"]['PKW001'],2)
    PF = data["inputPowerFactor"]["value"] if not data["inputPowerFactor"]["disabled"] else round(values_df["Value"]['FP001'],2)
    P_CD = 0.0 if data["inputDirectCurrentPower"] == False else 2.4
    
    SOC = data["simulatedBatteryStateOfCharge"] if "simulatedBatteryStateOfCharge" in data else data["batteryStateOfCharge"]["value"]
    V_CD  = data["simulatedDirectCurrentVoltage"] if "simulatedDirectCurrentVoltage" in data else 25.0
    inverterState = data["simulatedInverterState"] if "simulatedInverterState" in data else True
    if "simulatedSinkLoadState" in data:
      sinkState = data["simulatedSinkLoadState"]
    elif data["sinkLoadInitialState"] == "Apagada":
      sinkState = False
    else:
      sinkState = True

    V_bulk = data["controllerChargeVoltageBulk"]["value"]
    V_float = data["controllerChargeVoltageFloat"]["value"]
    V_charge = data["controllerChargingMinimunVoltage"]["value"]
    V_sink_on = data["controllerSinkOnVoltage"]["value"]
    V_sink_off = data["controllerSinkOffVoltage"]["value"]
    delta_t = 1.0 # Delta de tiempo de la simulación en s -> se define un valor por defecto

    n_controller = data["controllerEfficiency"]["value"]
    n_inverter = data["inverterEfficiency"]["value"]

    hydroSystem = Twin_Hydro.Hydro_twin(name)

    turbine = {}

    if not data["inputOfflineOperation"]:
      T_bat = round(values_df["Value"]['TE003'],2)
      inverterState = bool(int(values_df["Value"]['EI001']))
      P_h_meas = round(values_df["Value"]['PG001'],2)
      P_CC_meas = round(values_df["Value"]['VB001'] * values_df["Value"]['IC001'],2)
      V_CA = round(values_df["Value"]['VAC001'],2)
      V_t = round(values_df["Value"]['VG001'],2)
      V_CD = round(values_df["Value"]['VB001'],2)
      sinkState = bool(int(values_df["Value"]['ED001']))
      inverterState = bool(int(values_df["Value"]['EI001']))
      turbine["batteryTemperature"] = T_bat
      if data["inputPressure"]["disabled"]: turbine["inputFlow"] = pressure
      if data["inputFlow"]["disabled"]: turbine["inputPressure"] = flux
      if data["inputActivePower"]["disabled"]: turbine["inputActivePower"] = P_CA
      if data["inputPowerFactor"]["disabled"]: turbine["inputPowerFactor"] = PF
    else:
      T_bat = 30.0
      V_CA = 0
      V_t = 0

    hydroSystem.turbineType(turbineType)
    P_h = hydroSystem.PowerOutput(pressure, flux)
    hydroSystem.twinParameters(n_controller, n_inverter)
    
    if not data["inputOfflineOperation"] and not data["inputPressure"]["disabled"] and data["inputFlow"]["disabled"]:
      hydroSystem.optimal_n_t(hydroSystem.n_t, P_h_meas, pressure, flux)
      P_h = hydroSystem.PowerOutput(pressure, flux)
      hydroSystem.optimal_n_controller(n_controller, P_h, P_CD, P_CC_meas)
    
    results = hydroSystem.twinOutput(P_CA, inverterState, PF, P_CD, T_bat, V_CD, SOC, 
                                     V_bulk, V_float, V_charge, sinkState, V_sink_on, V_sink_off, delta_t, V_t, V_CA)

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