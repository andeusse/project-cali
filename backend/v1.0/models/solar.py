from flask import request
from flask_restful import Resource
from simulation_models import TwinPVWF
import pandas as pd
from utils import ExcelReader
from utils import InfluxDbConnection

class Solar(Resource):
  def post(self):
    data = request.get_json()
    solar = {}
    
    if not data["inputOfflineOperation"]:
      excelReader = ExcelReader()
      excelReader.read_excel('./v1.0/tools/DB_Mapping.xlsx', None)
      database_dic = excelReader.data
      database_df = database_dic['ConexionDB']
      variables_df = database_dic['InfluxDBVariables']
      variables_df = variables_df.drop(variables_df[variables_df['Device'] != 'Módulo solar eólico'].index)
      values_df = pd.DataFrame(columns=["Tag", "Value"])
      values_df["Tag"] = variables_df["Tag"]
      values_df.set_index('Tag', inplace=True)

      influxDB_Connection = InfluxDbConnection()
      # Cambiar datos de conexión DB según corresponda en el excel. Eros = [0], Daniel = [1], Eusse = [2]
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

    monoModuleState = data["monocrystallinePanel"]["isConnected"]
    polyModuleState = data["policrystallinePanel"]["isConnected"]
    flexiModuleState = data["flexPanel"]["isConnected"]
    cdteModuleState = data["cadmiumTelluridePanel"]["isConnected"]
    if data["inputOperationMode"] == 'Mode4' or data["inputOperationMode"] == 'Mode5':
      turbineState = True
    else:
      turbineState = False

    batteries = int(data["battery1"]["isConnected"]) + int(data["battery2"]["isConnected"])
    if data["inputOperationMode"] == 'Mode2' or (data["inputOperationMode"] == 'Mode1' and cdteModuleState):
      isParallel = False
    else:
      isParallel = True

    controllerEfficiency = data["controller"]["efficiency"]["value"]
    inverterEfficiency = data["offgridInverter"]["efficiency"]["value"]
    hybridEfficiency = data["hybridInverter"]["efficiency"]["value"]

    inverterState = data["offgridInverter"]["isConnected"]
    hybridState = data["hybridInverter"]["isConnected"]
    gridState = data["externalGridState"]
    chargeCycle = data["chargeCycle"]

    solarRadiation1 = (data["solarRadiation1"]["value"] if not data["solarRadiation1"]["disabled"] else round(values_df["Value"][''],2))
    solarRadiation2 = (data["solarRadiation2"]["value"] if not data["solarRadiation2"]["disabled"] else round(values_df["Value"][''],2))
    temperature = data["temperature"]["value"]
    windSpeed = (data["windSpeed"]["value"] if not data["windSpeed"]["disabled"] else round(values_df["Value"][''],2))
    windDensity = data["windDensity"]["value"]

    if inverterState or hybridState:
      inputActivePower = data["alternCurrentLoadPower"]["value"] if not data["alternCurrentLoadPower"]["disabled"] else round(values_df["Value"][''],2)
      inputPowerFactor = data["alternCurrentLoadPowerFactor"]["value"] if not data["alternCurrentLoadPowerFactor"]["disabled"] else round(values_df["Value"][''],2)
    else:
      inputActivePower = 0.0
      inputPowerFactor = 1.0

    if data["inputOperationMode"] == 'Mode2' and hybridState:
      inputDirectCurrentPower = 0.0
    else:
      inputDirectCurrentPower = data["directCurrentLoadPower"]["value"] if not data["directCurrentLoadPower"]["disabled"] else round(values_df["Value"][''],2)
    
    if inverterState:
      simulatedInverterState = data["simulatedInverterState"] if "simulatedInverterState" in data else inverterState

    simulatedChargeCycle = data["simulatedChargeCycle"] if "simulatedChargeCycle" in data else False
    batteryStateOfCharge = data["simulatedBatteryStateOfCharge"] if "simulatedBatteryStateOfCharge" in data else data["battery"]["stateOfCharge"]["value"]
    directCurrentVoltage  = data["simulatedDirectCurrentVoltage"] if "simulatedDirectCurrentVoltage" in data else 13.0 * (1 + (not isParallel))
    

    controllerChargeVoltageBulk = data["controller"]["chargeVoltageBulk"]["value"]
    controllerChargeVoltageFloat = data["controller"]["chargeVoltageFloat"]["value"]
    controllerChargingMinimunVoltage = data["controller"]["chargingMinimunVoltage"]["value"]


    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = data["queryTime"] / 1000 # Delta de tiempo de la simulación en s -> se definen valores diferentes para offline y online

    twinPVWF = TwinPVWF(name)

    twinPVWF.arrayPowerOutput(isParallel, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
    # system.optimal_f_PV(P_PV_meas)
    
    twinPVWF.WT_PowerOutput(turbineState, windDensity, windSpeed)
    # system.optimal_n_WT(P_WT_meas)
    
    twinPVWF.arrayPowerOutput(isParallel, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
    twinPVWF.WT_PowerOutput(turbineState, windDensity, windSpeed)
    
    twinPVWF.twinParameters(controllerEfficiency, inverterEfficiency, hybridEfficiency, batteries)

    # if data["inputOperationMode"] == 'Mode2' and hybridState:
    #   twinPVWF.ongridTwinOutput(gridState, inputActivePower, inputPowerFactor, T_bat, directCurrentVoltage, batteryStateOfCharge, controllerChargeVoltageBulk, controllerChargeVoltageFloat, controllerChargingMinimunVoltage, simulatedChargeCycle, V_PV, V_grid, V_CA, delta_t*timeMultiplier)
    # else:
    #   twinPVWF.offgridTwinOutput(inverterState, inputActivePower, inputPowerFactor, inputDirectCurrentPower, T_bat, directCurrentVoltage, batteryStateOfCharge, controllerChargeVoltageBulk, controllerChargeVoltageFloat, controllerChargingMinimunVoltage, V_PV, V_WT, V_CDload, V_CA, delta_t*timeMultiplier)
    

    # turbine = {}

    # if not data["inputOfflineOperation"]:
    #   T_bat = round(values_df["Value"]['TE003'],2)
    #   simulatedInverterState = bool(int(values_df["Value"]['EI001']))
    #   P_h_meas = round(values_df["Value"]['PG001'],2)
    #   P_CC_meas = round(values_df["Value"]['VB001'] * values_df["Value"]['IC001'],2)
    #   V_CA = round(values_df["Value"]['VAC001'],2)
    #   V_t = round(values_df["Value"]['VG001'],2)
    #   simulatedDirectCurrentVoltage = round(values_df["Value"]['VB001'],2)
    #   simulatedSinkLoadState = bool(int(values_df["Value"]['ED001']))
    #   simulatedInverterState = bool(int(values_df["Value"]['EI001']))

    #   turbine["batteryTemperature"] = T_bat
    #   if data["inputPressure"]["disabled"]: turbine["inputPressure"] = round(inputPressure / 6.89476, 2) # kPa to psi conversion
    #   if data["inputFlow"]["disabled"]: turbine["inputFlow"] = round(inputFlow * 60, 2) # L/s to L/min conversion
    #   if data["inputActivePower"]["disabled"]: turbine["inputActivePower"] = inputActivePower
    #   if data["inputPowerFactor"]["disabled"]: turbine["inputPowerFactor"] = inputPowerFactor
    # else:
    #   T_bat = 30.0
    #   V_CA = 0
    #   V_t = 0

    # twinHydro.turbineType(turbineType)
    # P_h = twinHydro.PowerOutput(inputPressure, inputFlow)
    # twinHydro.twinParameters(controllerEfficiency, inverterEfficiency)
    
    # if not data["inputOfflineOperation"] and not data["inputPressure"]["disabled"] and data["inputFlow"]["disabled"]:
    #   twinHydro.optimal_n_t(twinHydro.n_t, P_h_meas, inputPressure, inputFlow)
    #   P_h = twinHydro.PowerOutput(inputPressure, inputFlow)
    #   twinHydro.optimal_n_controller(controllerEfficiency, P_h, inputDirectCurrentPower, P_CC_meas)

    # results = twinHydro.twinOutput(inputActivePower, simulatedInverterState, inputPowerFactor, inputDirectCurrentPower, T_bat, simulatedDirectCurrentVoltage, batteryStateOfCharge, 
    #                                  controllerChargeVoltageBulk, controllerChargeVoltageFloat, controllerChargingMinimunVoltage, simulatedSinkLoadState, controllerSinkOnVoltage, controllerSinkOffVoltage, 
    #                                  delta_t*timeMultiplier, V_t, V_CA)

    # turbine["turbinePower"] = P_h

    # turbine["controllerPower"] = results[0]
    # turbine["inverterInputPower"] = results[1]
    # turbine["batteryPower"] = results[2]
    # turbine["turbineVoltage"] = results[3]
    # turbine["inverterOutputVoltage"] = results[4]
    # turbine["batteryStateOfCharge"] = results[5]
    # turbine["batteryVoltage"] = results[6]
    # turbine["directCurrentVoltage"] = results[7]
    # turbine["sinkLoadState"] = results[8]
    # turbine["sinkLoadPower"] = results[9]
    # turbine["inverterApparentPower"] = results[10]
    # turbine["inverterActivePower"] = results[11]
    # turbine["inverterReactivePower"] = results[12]
    # turbine["inverterState"] = results[13]
    # turbine["turbineCurrent"] = results[14]
    # turbine["controllerCurrent"] = results[15]
    # turbine["batteryCurrent"] = results[16]
    # turbine["inverterOutputCurrent"] = results[17]
    # turbine["inverterInputCurrent"] = results[18]

    return {"model": solar}