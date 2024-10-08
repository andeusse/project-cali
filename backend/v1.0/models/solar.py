from flask import request
from flask_restful import Resource
from simulation_models import TwinPVWF
import pandas as pd
import numpy as np
from utils import InfluxDbConnection
from dotenv import load_dotenv
import os

class Solar(Resource):
  def post(self):
    data = request.get_json()
    solarWind = {}

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

      query = influxDB.QueryCreator(measurement='Solar_eolico', type=1)
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
    deratingFactorList = [data["monocrystallinePanel"]["deratingFactor"]["value"], data["policrystallinePanel"]["deratingFactor"]["value"], data["flexPanel"]["deratingFactor"]["value"], data["cadmiumTelluridePanel"]["deratingFactor"]["value"]]
    print(deratingFactorList)
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
    batteryState = data['isBatteryConnected']

    if data["solarRadiation1"]["arrayEnabled"]:
      solarRadiation1Array = np.repeat(np.array(data["solarRadiation1Array"]),repeats)
      if iteration <= len(solarRadiation1Array):
        solarRadiation1 = float(solarRadiation1Array[iteration-1])
      else:
        solarRadiation1 = float(solarRadiation1Array[-1])
    else:
      solarRadiation1 = (0.0 if not data["solarRadiation1"]["value"] else data["solarRadiation1"]["value"]) if not data["solarRadiation1"]["disabled"] else round(values_df["Value"]['RS-001'],2)
    if data["solarRadiation2"]["arrayEnabled"]:
      solarRadiation2Array = np.repeat(np.array(data["solarRadiation2Array"]),repeats)
      if iteration <= len(solarRadiation2Array):
        solarRadiation2 = float(solarRadiation2Array[iteration-1])
      else:
        solarRadiation2 = float(solarRadiation2Array[-1])
    else:
      solarRadiation2 = (0.0 if not data["solarRadiation2"]["value"] else data["solarRadiation2"]["value"]) if not data["solarRadiation2"]["disabled"] else round(values_df["Value"]['RS-002'],2)
    if data["temperature"]["arrayEnabled"]:
      temperatureArray = np.repeat(np.array(data["temperatureArray"]),repeats)
      if iteration <= len(temperatureArray):
        temperature = float(temperatureArray[iteration-1])
      else:
        temperature = float(temperatureArray[-1])
    else:
      temperature = 0.0 if not data["temperature"]["value"] else data["temperature"]["value"]
    if data["windSpeed"]["arrayEnabled"]:
      windSpeedArray = np.repeat(np.array(data["windSpeedArray"]),repeats)
      if iteration <= len(windSpeedArray):
        windSpeed = float(windSpeedArray[iteration-1])
      else:
        windSpeed = float(windSpeedArray[-1])
    else:
      windSpeed = (0.0 if not data["windSpeed"]["value"] else data["windSpeed"]["value"]) if not data["windSpeed"]["disabled"] else round(values_df["Value"]['VV-001'],2)
    if data["inputOfflineOperation"]:
      if data["directCurrentLoadPower"]["arrayEnabled"]:
        directCurrentLoadPowerArray = np.repeat(np.array(data["directCurrentLoadPowerArray"]),repeats)
        if iteration <= len(directCurrentLoadPowerArray):
          inputDirectCurrentPower = float(directCurrentLoadPowerArray[iteration-1])
        else:
          inputDirectCurrentPower = float(directCurrentLoadPowerArray[-1])
      else:
        inputDirectCurrentPower = 0.0 if not data["directCurrentLoadPower"]["value"] else data["directCurrentLoadPower"]["value"]
    else:
      inputDirectCurrentPower = 6.0 if data["directCurrentLoadConnected"] else 0.0
    windDensity = 0.0 if not data["windDensity"]["value"] else data["windDensity"]["value"]

    if (data["inputOperationMode"] == 'Mode2' or (data["inputOperationMode"] == 'Mode1' and cdteModuleState)) and inverterState:
      if data["alternCurrentLoadPower"]["arrayEnabled"]:
        alternCurrentLoadPowerArray = np.repeat(np.array(data["alternCurrentLoadPowerArray"]),repeats)
        if iteration <= len(alternCurrentLoadPowerArray):
          inputActivePower = float(alternCurrentLoadPowerArray[iteration-1])
        else:
          inputActivePower = float(alternCurrentLoadPowerArray[-1])
      else:
        inputActivePower = (0.0 if not data["alternCurrentLoadPower"]["value"] else data["alternCurrentLoadPower"]["value"]) if not data["alternCurrentLoadPower"]["disabled"] else round(values_df["Value"]['PKW-002'] * 1000,2)
      if data["alternCurrentLoadPowerFactor"]["arrayEnabled"]:
        alternCurrentLoadPowerFactorArray = np.repeat(np.array(data["alternCurrentLoadPowerFactorArray"]),repeats)
        if iteration <= len(alternCurrentLoadPowerFactorArray):
          inputPowerFactor = float(alternCurrentLoadPowerFactorArray[iteration-1])
        else:
          inputPowerFactor = float(alternCurrentLoadPowerFactorArray[-1])
      else: 
        inputPowerFactor = (1.0 if not data["alternCurrentLoadPowerFactor"]["value"] and data["alternCurrentLoadPowerFactor"]["value"]!=0 else data["alternCurrentLoadPowerFactor"]["value"]) if not data["alternCurrentLoadPowerFactor"]["disabled"] else round(values_df["Value"]['FP-001'] * (1 if values_df["Value"]['PKVAR-001'] >= 0.0 else -1),2)
      simulatedInverterState = data["simulatedInverterState"] if "simulatedInverterState" in data else inverterState
    elif data["inputOperationMode"] == 'Mode2' and hybridState:
      if data["alternCurrentLoadPower"]["arrayEnabled"]:
        alternCurrentLoadPowerArray = np.repeat(np.array(data["alternCurrentLoadPowerArray"]),repeats)
        if iteration <= len(alternCurrentLoadPowerArray):
          inputActivePower = float(alternCurrentLoadPowerArray[iteration-1])
        else:
          inputActivePower = float(alternCurrentLoadPowerArray[-1])
      else:
        inputActivePower = (0.0 if not data["alternCurrentLoadPower"]["value"] else data["alternCurrentLoadPower"]["value"]) if not data["alternCurrentLoadPower"]["disabled"] else round(values_df["Value"]['PKW-003'] * 1000,2)
      if data["alternCurrentLoadPowerFactor"]["arrayEnabled"]:
        alternCurrentLoadPowerFactorArray = np.repeat(np.array(data["alternCurrentLoadPowerFactorArray"]),repeats)
        if iteration <= len(alternCurrentLoadPowerFactorArray):
          inputPowerFactor = float(alternCurrentLoadPowerFactorArray[iteration-1])
        else:
          inputPowerFactor = float(alternCurrentLoadPowerFactorArray[-1])
      else:
        inputPowerFactor = (1.0 if not data["alternCurrentLoadPowerFactor"]["value"] and data["alternCurrentLoadPowerFactor"]["value"]!=0 else data["alternCurrentLoadPowerFactor"]["value"]) if not data["alternCurrentLoadPowerFactor"]["disabled"] else round(values_df["Value"]['FP-002'] * (1 if values_df["Value"]['PKVAR-002'] >= 0.0 else -1),2)
      inputDirectCurrentPower = 0.0
      simulatedInverterState = False
    else:
      inputActivePower = 0.0
      inputPowerFactor = 1.0
      simulatedInverterState = False
    
    solarWind["inputAlternCurrentLoadPower"] = inputActivePower
    solarWind["inputAlternCurrentLoadPowerFactor"] = inputPowerFactor
    solarWind["inputDirectCurrentLoadPower"] = inputDirectCurrentPower

    simulatedChargeCycle = data["simulatedChargeCycle"] if "simulatedChargeCycle" in data else False
    batteryStateOfCharge = data["simulatedBatteryStateOfCharge"] if "simulatedBatteryStateOfCharge" in data else (data["battery1"]["stateOfCharge"]["value"] + int(data["isBattery2"]) * data["battery2"]["stateOfCharge"]["value"]) / (1 + int(data["isBattery2"]))
    chargeCycleInitialSOC = data['simulatedChargeCycleInitialSOC'] if 'simulatedChargeCycleInitialSOC' in data else (data["battery1"]["stateOfCharge"]["value"] + int(data["isBattery2"]) * data["battery2"]["stateOfCharge"]["value"]) / (1 + int(data["isBattery2"]))

    controllerChargeVoltageBulk = data["controller"]["chargeVoltageBulk"]["value"]
    controllerChargeVoltageFloat = data["controller"]["chargeVoltageFloat"]["value"]
    controllerChargingMinimumVoltage = data["controller"]["chargingMinimumVoltage"]["value"]
    hybridChargeVoltageBulk = data["hybridInverter"]["chargeVoltageBulk"]["value"]
    hybridChargeVoltageFloat = data["hybridInverter"]["chargeVoltageFloat"]["value"]
    hybridChargingMinimumVoltage = data["hybridInverter"]["chargingMinimumVoltage"]["value"]

    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = data["queryTime"] / 1000 # Delta de tiempo de la simulación en s -> se definen valores diferentes para offline y online

    twinPVWF = TwinPVWF(name)

    if not data["inputOfflineOperation"]:
      if data["inputOperationMode"] == 'Mode2' and hybridState:
        batteryTemperature = 30.0
        measuredPV_Power = round(values_df["Value"]['PG-003'],2)
        measuredWT_Power = 0.0
        measuredHybridDC_Power = round(values_df["Value"]['PC-003'],2)
        PV_Voltage = round(values_df["Value"]['VG-003'],2)
        gridVoltage = round(values_df["Value"]['VAC-004'],2)
        WT_Voltage = 0.0
        directCurrentVoltage = round(values_df["Value"]['VCH-002'],2)
        hybridInverterVoltage = round(values_df["Value"]['VAC-006'],2)
      else:
        batteryTemperature = 30.0
        simulatedInverterState = bool(int(values_df["Value"]['EI-001']))
        measuredPV_Power = round(values_df["Value"]['PC-001'],2)
        measuredWT_Power = round(values_df["Value"]['PC-002'],2)
        measuredControllerDC_Power = round(values_df["Value"]['PC-001']+values_df["Value"]['PC-002'],2)
        PV_Voltage = round(values_df["Value"]['VG-001'],2)
        WT_Voltage = round(values_df["Value"]['VG-002'],2)
        directCurrentVoltage = round(values_df["Value"]['VCH-001'],2)
        inverterVoltage = round(values_df["Value"]['VAC-002'],2)
        directCurrentLoadVoltage = round(values_df["Value"]['VDC-001'],2)
        solarWind['windTurbineRevolutions'] = round(values_df["Value"]['RPM-001'],2)

      solarWind["batteryTemperature"] = batteryTemperature
      if data["solarRadiation1"]["disabled"]: solarWind["inputSolarRadiation1"] = solarRadiation1
      if data["solarRadiation2"]["disabled"]: solarWind["inputSolarRadiation2"] = solarRadiation2
      if data["windSpeed"]["disabled"]: solarWind["inputWindSpeed"] = windSpeed
    else:
      batteryTemperature = 30.0
      PV_Voltage = 0.0
      gridVoltage = 0.0
      WT_Voltage = 0.0
      inverterVoltage = 0.0
      directCurrentLoadVoltage = 0.0
      hybridInverterVoltage = 0.0
      solarWind['windTurbineRevolutions'] = 0.0

    twinPVWF.twinParameters(controllerEfficiency, inverterEfficiency, hybridEfficiency, batteries, isParallel)
    PV_Results = twinPVWF.arrayPowerOutput(data["inputOfflineOperation"], deratingFactorList, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
    WT_Results = twinPVWF.WT_PowerOutput(data["inputOfflineOperation"], turbineState, windDensity, windSpeed)
    
    if monoModuleState or polyModuleState:
      if not data["inputOfflineOperation"] and data["solarRadiation1"]["disabled"]:
        twinPVWF.optimal_f_PV(measuredPV_Power)
        PV_Results = twinPVWF.arrayPowerOutput(data["inputOfflineOperation"], deratingFactorList, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
        if not (data["inputOperationMode"] == 'Mode2' and hybridState):
          twinPVWF.optimal_n_controller(inputDirectCurrentPower, measuredControllerDC_Power)
    elif flexiModuleState or cdteModuleState:
      if not data["inputOfflineOperation"] and data["solarRadiation2"]["disabled"]:
        twinPVWF.optimal_f_PV(measuredPV_Power)
        PV_Results = twinPVWF.arrayPowerOutput(data["inputOfflineOperation"], deratingFactorList, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
        if not (data["inputOperationMode"] == 'Mode2' and hybridState):
          twinPVWF.optimal_n_controller(inputDirectCurrentPower, measuredControllerDC_Power)

    if turbineState and not data["inputOfflineOperation"] and data["windSpeed"]["disabled"]:
      twinPVWF.optimal_n_WT(measuredWT_Power)
      WT_Results = twinPVWF.WT_PowerOutput(data["inputOfflineOperation"], turbineState, windDensity, windSpeed)
      twinPVWF.optimal_n_controller(inputDirectCurrentPower, measuredControllerDC_Power)

    solarWind["controllerEfficiency"] = twinPVWF.n_controller
    solarWind["inverterEfficiency"] = twinPVWF.n_inverter
    solarWind["hybridEfficiency"] = twinPVWF.n_hybrid

    if data["inputOperationMode"] == 'Mode2' and hybridState:
      solarWind['solarPanelPower'] = PV_Results[0]
      solarWind['monocrystallinePanelTemperature'] = PV_Results[1]
      solarWind['policrystallinePanelTemperature'] = PV_Results[2]
      solarWind['flexPanelTemperature'] = PV_Results[3]
      solarWind['cadmiumTelluridePanelTemperature'] = PV_Results[4]

      directCurrentVoltage  = data["simulatedDirectCurrentVoltage"] if "simulatedDirectCurrentVoltage" in data else 12.6 * (1 + (not isParallel))
      
      twinResults = twinPVWF.ongridTwinOutput(chargeCycleInitialSOC, batteryState, gridState, inputActivePower, inputPowerFactor, batteryTemperature, directCurrentVoltage, 
                                batteryStateOfCharge, hybridChargeVoltageBulk, hybridChargeVoltageFloat, 
                                hybridChargingMinimumVoltage, simulatedChargeCycle, PV_Voltage, gridVoltage, 
                                hybridInverterVoltage, delta_t*timeMultiplier)
      
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
      solarWind['solarPanelPower'] = PV_Results[0]
      solarWind['monocrystallinePanelTemperature'] = PV_Results[1]
      solarWind['policrystallinePanelTemperature'] = PV_Results[2]
      solarWind['flexPanelTemperature'] = PV_Results[3]
      solarWind['cadmiumTelluridePanelTemperature'] = PV_Results[4]
      solarWind['windTurbinePower'] = WT_Results

      if "simulatedDirectCurrentVoltage" in data:
        directCurrentVoltage = data["simulatedDirectCurrentVoltage"]
      else:
        P_CC = ((solarWind['solarPanelPower'] + solarWind['windTurbinePower']) * twinPVWF.n_controller / 100) - (inputDirectCurrentPower / (twinPVWF.n_controller / 100))
        P_inv = (inputActivePower / abs(inputPowerFactor)) / (twinPVWF.n_inverter / 100)
        P_bat = P_CC - P_inv
        if P_bat < 0.0:
          batteryCurrent = abs(P_bat / 25.21)
          if batteryCurrent <= 7.5:
            initialVoltage = 25.92/(1 + isParallel)
          elif batteryCurrent <= 15:
            initialVoltage = 25.68/(1 + isParallel)
          elif batteryCurrent <= 37.5:
            initialVoltage = 25.13/(1 + isParallel)
          elif batteryCurrent <= 82.5:
            initialVoltage = 24.84/(1 + isParallel)
          else:
            initialVoltage = 24.48/(1 + isParallel)
          directCurrentVoltage = initialVoltage
        else:
          if batteryStateOfCharge >= 50:
            directCurrentVoltage = 24.6/(1 + isParallel)
          else:
            directCurrentVoltage = 24.0/(1 + isParallel)
      
      twinResults = twinPVWF.offgridTwinOutput(chargeCycleInitialSOC, batteryState, simulatedInverterState, inputActivePower, inputPowerFactor, inputDirectCurrentPower, 
                                 batteryTemperature, directCurrentVoltage, batteryStateOfCharge, controllerChargeVoltageBulk, 
                                 controllerChargeVoltageFloat, controllerChargingMinimumVoltage, PV_Voltage, WT_Voltage, 
                                 directCurrentLoadVoltage, inverterVoltage, delta_t*timeMultiplier)
            
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
    
    solarWind['batteryState'] = batteryState

    if solarWind["batteryPower"] <= 0.0:
      solarWind["chargeCycleInitialSOC"] = solarWind["batteryStateOfCharge"]
    else:
      solarWind["chargeCycleInitialSOC"] = chargeCycleInitialSOC

    return {"model": solarWind}