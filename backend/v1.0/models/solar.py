from flask import request
from flask_restful import Resource
from simulation_models import TwinPVWF
import pandas as pd
from utils import ExcelReader
from utils import InfluxDbConnection

class Solar(Resource):
  def post(self):
    data = request.get_json()
    solarWind = {}
    
    if not data["inputOfflineOperation"]:
      excelReader = ExcelReader()
      excelReader.read_excel('./v1.0/tools/DB_Mapping.xlsx', None)
      database_dic = excelReader.data
      database_df = database_dic['ConexionDB']
      variables_df = database_dic['InfluxDBVariables']
      variables_df = variables_df.drop(variables_df[variables_df['Device'] != 'Módulo solar-eólico'].index)
      values_df = pd.DataFrame(columns=["Tag", "Value"])
      values_df["Tag"] = variables_df["Tag"]
      values_df.set_index('Tag', inplace=True)

      influxDB_Connection = InfluxDbConnection()
      # Cambiar datos de conexión DB según corresponda en el excel. Eros = [0], Daniel = [1], Eusse = [2]
      db = 2
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

    batteries = 1 + int(data["isBattery2"])
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

    solarRadiation1 = (data["solarRadiation1"]["value"] if not data["solarRadiation1"]["disabled"] else round(values_df["Value"]['RS001'],2))
    solarRadiation2 = (data["solarRadiation2"]["value"] if not data["solarRadiation2"]["disabled"] else round(values_df["Value"]['RS002'],2))
    temperature = data["temperature"]["value"]
    windSpeed = (data["windSpeed"]["value"] if not data["windSpeed"]["disabled"] else round(values_df["Value"]['VV001'],2))
    windDensity = data["windDensity"]["value"]

    if (data["inputOperationMode"] == 'Mode2' or (data["inputOperationMode"] == 'Mode1' and cdteModuleState)) and inverterState:
      inputActivePower = data["alternCurrentLoadPower"]["value"] if not data["alternCurrentLoadPower"]["disabled"] else round(values_df["Value"]['PKW001'],2)
      inputPowerFactor = data["alternCurrentLoadPowerFactor"]["value"] if not data["alternCurrentLoadPowerFactor"]["disabled"] else round(values_df["Value"]['FP001'],2)
      simulatedInverterState = data["simulatedInverterState"] if "simulatedInverterState" in data else inverterState
    else:
      inputActivePower = 0.0
      inputPowerFactor = 1.0
      simulatedInverterState = False

    if data["inputOperationMode"] == 'Mode2' and hybridState:
      inputActivePower = data["alternCurrentLoadPower"]["value"] if not data["alternCurrentLoadPower"]["disabled"] else round(values_df["Value"]['PKW002'],2)
      inputPowerFactor = data["alternCurrentLoadPowerFactor"]["value"] if not data["alternCurrentLoadPowerFactor"]["disabled"] else round(values_df["Value"]['FP002'],2)
      inputDirectCurrentPower = 0.0
    else:
      inputActivePower = 0.0
      inputPowerFactor = 1.0
      #############################################################
      inputDirectCurrentPower = data["directCurrentLoadPower"]["value"] if not data["directCurrentLoadPower"]["disabled"] else round(values_df["Value"]['PDC001'],2)

    simulatedChargeCycle = data["simulatedChargeCycle"] if "simulatedChargeCycle" in data else False
    batteryStateOfCharge = data["simulatedBatteryStateOfCharge"] if "simulatedBatteryStateOfCharge" in data else data["battery1"]["stateOfCharge"]["value"]
    directCurrentVoltage  = data["simulatedDirectCurrentVoltage"] if "simulatedDirectCurrentVoltage" in data else 13.0 * (1 + (not isParallel))

    controllerChargeVoltageBulk = data["controller"]["chargeVoltageBulk"]["value"]
    controllerChargeVoltageFloat = data["controller"]["chargeVoltageFloat"]["value"]
    controllerChargingMinimunVoltage = data["controller"]["chargingMinimunVoltage"]["value"]

    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = data["queryTime"] / 1000 # Delta de tiempo de la simulación en s -> se definen valores diferentes para offline y online

    twinPVWF = TwinPVWF(name)

    if not data["inputOfflineOperation"]:
      ############################################################
      batteryTemperature = round(values_df["Value"]['TB001'],2)
      simulatedInverterState = bool(int(values_df["Value"]['EI001']))
      measuredPV_Power = round(values_df["Value"]['PG001'],2)
      measuredWT_Power = round(values_df["Value"]['PG005'],2)
      ############################################################
      measuredControllerDC_Power = round(values_df["Value"]['PB001'],2)
      PV_Voltage = round(values_df["Value"]['VG001'],2)
      ############################################################
      gridVoltage = round(values_df["Value"]['VGR001'],2)
      WT_Voltage = round(values_df["Value"]['VG002'],2)
      directCurrentVoltage = round(values_df["Value"]['VB001'],2)
      inverterVoltage = round(values_df["Value"]['VAC001'],2)
      ############################################################
      directCurrentLoadVoltage = round(values_df["Value"]['VDC001'],2)
      hybridInverterVoltage = round(values_df["Value"]['VAC002'],2)
      solarWind['windTurbineRevolutions'] = round(values_df["Value"]['RPM001'],2)

      solarWind["batteryTemperature"] = batteryTemperature
      if data["solarRadiation1"]["disabled"]: solarWind["solarRadiation1"] = solarRadiation1
      if data["solarRadiation2"]["disabled"]: solarWind["solarRadiation2"] = solarRadiation2
      if data["windSpeed"]["disabled"]: solarWind["windSpeed"] = windSpeed
      if data["alternCurrentLoadPower"]["disabled"]: solarWind["alternCurrentLoadPower"] = inputActivePower
      if data["alternCurrentLoadPowerFactor"]["disabled"]: solarWind["alternCurrentLoadPowerFactor"] = inputPowerFactor
      if data["directCurrentLoadPower"]["disabled"]: solarWind["directCurrentLoadPower"] = inputDirectCurrentPower
    else:
      batteryTemperature = 30.0
      PV_Voltage = 0.0
      gridVoltage = 0.0
      WT_Voltage = 0.0
      inverterVoltage = 0.0
      directCurrentLoadVoltage = 0.0
      hybridInverterVoltage = 0.0
      solarWind['windTurbineRevolutions'] = 0.0

    PV_Results = twinPVWF.arrayPowerOutput(isParallel, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
    WT_Results = twinPVWF.WT_PowerOutput(turbineState, windDensity, windSpeed)
    twinPVWF.twinParameters(controllerEfficiency, inverterEfficiency, hybridEfficiency, batteries)
    
    if monoModuleState or polyModuleState:
      if not data["inputOfflineOperation"] and data["solarRadiation1"]["disabled"]:
        twinPVWF.optimal_f_PV(measuredPV_Power)
        PV_Results = twinPVWF.arrayPowerOutput(isParallel, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
        if not (data["inputOperationMode"] == 'Mode2' and hybridState):
          twinPVWF.optimal_n_controller(inputDirectCurrentPower, measuredControllerDC_Power)
    elif flexiModuleState or cdteModuleState:
      if not data["inputOfflineOperation"] and data["solarRadiation2"]["disabled"]:
        twinPVWF.optimal_f_PV(measuredPV_Power)
        PV_Results = twinPVWF.arrayPowerOutput(isParallel, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
        if not (data["inputOperationMode"] == 'Mode2' and hybridState):
          twinPVWF.optimal_n_controller(inputDirectCurrentPower, measuredControllerDC_Power)

    if turbineState and not data["inputOfflineOperation"] and data["windSpeed"]["disabled"]:
      twinPVWF.optimal_n_WT(measuredWT_Power)
      WT_Results = twinPVWF.WT_PowerOutput(turbineState, windDensity, windSpeed)
      twinPVWF.optimal_n_controller(inputDirectCurrentPower, measuredControllerDC_Power)

    if data["inputOperationMode"] == 'Mode2' and hybridState:
      twinResults = twinPVWF.ongridTwinOutput(gridState, inputActivePower, inputPowerFactor, batteryTemperature, directCurrentVoltage, 
                                batteryStateOfCharge, controllerChargeVoltageBulk, controllerChargeVoltageFloat, 
                                controllerChargingMinimunVoltage, simulatedChargeCycle, PV_Voltage, gridVoltage, 
                                hybridInverterVoltage, delta_t*timeMultiplier)
      solarWind['solarPanelPower'] = PV_Results[0]
      solarWind['monocrystallinePanelTemperature'] = PV_Results[1]
      solarWind['policrystallinePanelTemperature'] = PV_Results[2]
      solarWind['flexPanelTemperature'] = PV_Results[3]
      solarWind['cadmiumTelluridePanelTemperature'] = PV_Results[4]
      
      solarWind["externalGridPower"] = twinResults[0]
      solarWind["inverterInputPower"] = twinResults[1]
      solarWind["batteryPower"] = twinResults[2]
      solarWind['externalGridVoltage'] = twinResults[3]
      solarWind['solarPanelVoltage'] = twinResults[4]
      solarWind['batteryStateOfCharge'] = twinResults[5]
      solarWind['batteryVoltage'] = twinResults[6]
      solarWind['directCurrentVoltage'] = twinResults[7]
      solarWind['hybridInverterVoltage'] = twinResults[8]
      solarWind['hybridInverterApparentPower'] = twinResults[9]
      solarWind['hybridInverterActivePower'] = twinResults[10]
      solarWind['hybridInverterReactivePower'] = twinResults[11]
      solarWind['externalGridState'] = twinResults[12]
      solarWind['chargeCycle'] = twinResults[13]
      solarWind['solarPanelCurrent'] = twinResults[14]
      solarWind['batteryCurrent'] = twinResults[15]
      solarWind['externalGridCurrent'] = twinResults[16]
      solarWind['hybridInverterOutputCurrent'] = twinResults[17]
      
    else:
      twinResults = twinPVWF.offgridTwinOutput(simulatedInverterState, inputActivePower, inputPowerFactor, inputDirectCurrentPower, 
                                 batteryTemperature, directCurrentVoltage, batteryStateOfCharge, controllerChargeVoltageBulk, 
                                 controllerChargeVoltageFloat, controllerChargingMinimunVoltage, PV_Voltage, WT_Voltage, 
                                 directCurrentLoadVoltage, inverterVoltage, delta_t*timeMultiplier)
      solarWind['solarPanelPower'] = PV_Results[0]
      solarWind['monoModuleTemperature'] = PV_Results[1]
      solarWind['polyModuleTemperature'] = PV_Results[2]
      solarWind['flexiModuleTemperature'] = PV_Results[3]
      solarWind['cdteModuleTemperature'] = PV_Results[4]
      solarWind['windTurbinePower'] = WT_Results
      
      solarWind["controllerPower"] = twinResults[0]
      solarWind["inverterInputPower"] = twinResults[1]
      solarWind["batteryPower"] = twinResults[2]
      solarWind['solarPanelVoltage'] = twinResults[3]
      solarWind['windTurbineVoltage'] = twinResults[4]
      solarWind['directCurrentLoadVoltage'] = twinResults[5]
      solarWind['batteryStateOfCharge'] = twinResults[6]
      solarWind['batteryVoltage'] = twinResults[7]
      solarWind['directCurrentVoltage'] = twinResults[8]
      solarWind['inverterVoltage'] = twinResults[9]
      solarWind['inverterApparentPower'] = twinResults[10]
      solarWind['inverterActivePower'] = twinResults[11]
      solarWind['inverterReactivePower'] = twinResults[12]
      solarWind['directCurrentLoadPower'] = twinResults[13]
      solarWind['inverterState'] = twinResults[14]
      solarWind['solarPanelCurrent'] = twinResults[15]
      solarWind['windTurbineCurrent'] = twinResults[16]
      solarWind['directCurrentLoadCurrent'] = twinResults[17]
      solarWind['controllerCurrent'] = twinResults[18]
      solarWind['batteryCurrent'] = twinResults[19]
      solarWind['inverterOutputCurrent'] = twinResults[20]
      solarWind['inverterInputCurrent'] = twinResults[21]

    return {"model": solarWind}