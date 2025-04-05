from flask import request
from flask_restful import Resource
from simulation_models import TwinPVWF
import pandas as pd
import numpy as np
from tools import DBManager
import os
import time
from datetime import datetime

class Solar(Resource):
  def post(self):
    data = request.get_json()
    solarWind = {}

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

      query = influxDB.QueryCreator(measurement='Solar_eolico', type=1)
      
      attempts = 1
      while attempts <= 5:
        try:
          # values_df_temp = influxDB.InfluxDBreader(query)
          values_df_temp = pd.concat(influxDB.InfluxDBreader(query))
          values_df['field'] = values_df_temp['_field']
          values_df['Value'] = values_df_temp['_value']
          timestamp = values_df_temp['_time'].mean()
          solarWind['timestamp'] = str(timestamp)

          values_df.set_index('field', inplace=True)
          influxDB.InfluxDBclose()
          break
        except:
          attempts += 1
        finally:
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
    monoModuleState = data["monocrystallinePanel"]["isConnected"]
    polyModuleState = data["policrystallinePanel"]["isConnected"]
    flexiModuleState = data["flexPanel"]["isConnected"]
    cdteModuleState = data["cadmiumTelluridePanel"]["isConnected"]
    if data["inputOperationMode"] == 'Mode4' or data["inputOperationMode"] == 'Mode5':
      turbineState = True
    else:
      turbineState = False
    hybridState = data["hybridInverter"]["isConnected"]
    inverterState = data["offgridInverter"]["isConnected"]
    batteryState = data['isBatteryConnected']
    
    lampsHeight= data["lampsHeight"]
    panelsAngle = data["panelsAngle"]["value"]
    
    training_fPV_Name = "eficienciaPanel" + data["inputOperationMode"] + (monoModuleState * "_mono") + (polyModuleState * "_poli") + (flexiModuleState * "_flex") + (cdteModuleState * "_cdte") + (turbineState * "_aero") + (hybridState * "_hibrid") + ("_alt" + str(lampsHeight)) + ("_ang" + str(panelsAngle))
    training_nWT_Name = "eficienciaAero" + data["inputOperationMode"] + (monoModuleState * "_mono") + (polyModuleState * "_poli") + (flexiModuleState * "_flex") + (cdteModuleState * "_cdte") + (turbineState * "_aero") + (hybridState * "_hibrid")
    training_nController_Name = "eficienciaControl" + data["inputOperationMode"] + (monoModuleState * "_mono") + (polyModuleState * "_poli") + (flexiModuleState * "_flex") + (cdteModuleState * "_cdte") + (turbineState * "_aero") + (hybridState * "_hibrid") + ("_alt" + str(lampsHeight)) + ("_ang" + str(panelsAngle))

    deratingFactorList = [data["monocrystallinePanel"]["deratingFactor"]["value"], data["policrystallinePanel"]["deratingFactor"]["value"], data["flexPanel"]["deratingFactor"]["value"], data["cadmiumTelluridePanel"]["deratingFactor"]["value"]]
    turbineEfficiency = 0.49
    controllerEfficiency = data["controller"]["efficiency"]["value"]

    batteries = 1 + int(data["isBattery2"])
    if (data["inputOperationMode"] == 'Mode1' and cdteModuleState) or data["inputOperationMode"] == 'Mode2' or data["inputOperationMode"] == 'Mode4' or data["inputOperationMode"] == 'Mode5':
      isParallel = False
    else:
      isParallel = True

    # inverterEfficiency = data["offgridInverter"]["efficiency"]["value"]
    inverterEfficiency = 94.0
    hybridEfficiency = data["hybridInverter"]["efficiency"]["value"]

    if data["solarRadiation1"]["arrayEnabled"]:
      solarRadiation1Array = np.repeat(np.array(data["solarRadiation1Array"]),repeats)
      if iteration <= len(solarRadiation1Array):
        solarRadiation1 = float(solarRadiation1Array[iteration-1])
      else:
        solarRadiation1 = float(solarRadiation1Array[-1])
    elif (data["inputOperationMode"] == 'Mode1' and (monoModuleState or polyModuleState)) or (data["inputOperationMode"] == 'Mode2' and (monoModuleState or polyModuleState)) or (data["inputOperationMode"] == 'Mode3' and (monoModuleState or polyModuleState)) or (data["inputOperationMode"] == 'Mode5' and (monoModuleState or polyModuleState)):
      solarRadiation1 = (0.0 if not data["solarRadiation1"]["value"] else data["solarRadiation1"]["value"]) if not data["solarRadiation1"]["disabled"] else round(values_df["Value"]['RS-002'],3)
    else:
      solarRadiation1 = 0.0
    
    if data["solarRadiation2"]["arrayEnabled"]:
      solarRadiation2Array = np.repeat(np.array(data["solarRadiation2Array"]),repeats)
      if iteration <= len(solarRadiation2Array):
        solarRadiation2 = float(solarRadiation2Array[iteration-1])
      else:
        solarRadiation2 = float(solarRadiation2Array[-1])
    elif (data["inputOperationMode"] == 'Mode1' and (flexiModuleState or cdteModuleState)) or (data["inputOperationMode"] == 'Mode2' and (flexiModuleState or cdteModuleState)) or (data["inputOperationMode"] == 'Mode3' and (flexiModuleState or cdteModuleState)) or (data["inputOperationMode"] == 'Mode5' and (flexiModuleState or cdteModuleState)):
      solarRadiation2 = (0.0 if not data["solarRadiation2"]["value"] else data["solarRadiation2"]["value"]) if not data["solarRadiation2"]["disabled"] else round(values_df["Value"]['RS-001'],3)
    else:
      solarRadiation2 = 0.0
    
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
    elif turbineState:
      windSpeed = (0.0 if not data["windSpeed"]["value"] else data["windSpeed"]["value"]) if not data["windSpeed"]["disabled"] else round(values_df["Value"]['VV-001'],3)
    else:
      windSpeed = 0.0
    
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
      inputDirectCurrentPower = 2.4 if data["directCurrentLoadConnected"] else 0.0
    windDensity = 0.0 if not data["windDensity"]["value"] else data["windDensity"]["value"]

    if (data["inputOperationMode"] == 'Mode2' or (data["inputOperationMode"] == 'Mode1' and cdteModuleState) or data["inputOperationMode"] == 'Mode4' or data["inputOperationMode"] == 'Mode5') and inverterState:
    # if (data["inputOperationMode"] == 'Mode2' or (data["inputOperationMode"] == 'Mode1' and cdteModuleState)) and inverterState:
      if data["alternCurrentLoadPower"]["arrayEnabled"]:
        alternCurrentLoadPowerArray = np.repeat(np.array(data["alternCurrentLoadPowerArray"]),repeats)
        if iteration <= len(alternCurrentLoadPowerArray):
          inputActivePower = float(alternCurrentLoadPowerArray[iteration-1])
        else:
          inputActivePower = float(alternCurrentLoadPowerArray[-1])
      else:
        inputActivePower = (0.0 if not data["alternCurrentLoadPower"]["value"] else data["alternCurrentLoadPower"]["value"]) if not data["alternCurrentLoadPower"]["disabled"] else round(values_df["Value"]['PKW-002'],3)
      if data["alternCurrentLoadPowerFactor"]["arrayEnabled"]:
        alternCurrentLoadPowerFactorArray = np.repeat(np.array(data["alternCurrentLoadPowerFactorArray"]),repeats)
        if iteration <= len(alternCurrentLoadPowerFactorArray):
          inputPowerFactor = float(alternCurrentLoadPowerFactorArray[iteration-1])
        else:
          inputPowerFactor = float(alternCurrentLoadPowerFactorArray[-1])
      else: 
        inputPowerFactor = (1.0 if not data["alternCurrentLoadPowerFactor"]["value"] and data["alternCurrentLoadPowerFactor"]["value"]!=0 else data["alternCurrentLoadPowerFactor"]["value"]) if not data["alternCurrentLoadPowerFactor"]["disabled"] else round(values_df["Value"]['FP-001'] * (1 if values_df["Value"]['PKVAR-001'] >= 0.0 else -1),3)
      simulatedInverterState = data["simulatedInverterState"] if "simulatedInverterState" in data else inverterState
    elif data["inputOperationMode"] == 'Mode2' and hybridState:
      if data["alternCurrentLoadPower"]["arrayEnabled"]:
        alternCurrentLoadPowerArray = np.repeat(np.array(data["alternCurrentLoadPowerArray"]),repeats)
        if iteration <= len(alternCurrentLoadPowerArray):
          inputActivePower = float(alternCurrentLoadPowerArray[iteration-1])
        else:
          inputActivePower = float(alternCurrentLoadPowerArray[-1])
      else:
        inputActivePower = (0.0 if not data["alternCurrentLoadPower"]["value"] else data["alternCurrentLoadPower"]["value"]) if not data["alternCurrentLoadPower"]["disabled"] else round(values_df["Value"]['PKW-003'],3)
      if data["alternCurrentLoadPowerFactor"]["arrayEnabled"]:
        alternCurrentLoadPowerFactorArray = np.repeat(np.array(data["alternCurrentLoadPowerFactorArray"]),repeats)
        if iteration <= len(alternCurrentLoadPowerFactorArray):
          inputPowerFactor = float(alternCurrentLoadPowerFactorArray[iteration-1])
        else:
          inputPowerFactor = float(alternCurrentLoadPowerFactorArray[-1])
      else:
        inputPowerFactor = (1.0 if not data["alternCurrentLoadPowerFactor"]["value"] and data["alternCurrentLoadPowerFactor"]["value"]!=0 else data["alternCurrentLoadPowerFactor"]["value"]) if not data["alternCurrentLoadPowerFactor"]["disabled"] else round(values_df["Value"]['FP-002'] * (1 if values_df["Value"]['PKVAR-002'] >= 0.0 else -1),3)
      inputDirectCurrentPower = 0.0
      simulatedInverterState = False
    else:
      inputActivePower = 0.0
      inputPowerFactor = 1.0
      simulatedInverterState = False
    
    if inputPowerFactor == 0.0: inputPowerFactor = 1.0
    
    solarWind["inputSolarRadiation1"] = solarRadiation1
    solarWind["inputSolarRadiation2"] = solarRadiation2
    solarWind["inputTemperature"] = temperature
    solarWind["inputWindSpeed"] = windSpeed
    solarWind["inputDirectCurrentLoadPower"] = inputDirectCurrentPower
    solarWind["inputAlternCurrentLoadPower"] = inputActivePower
    solarWind["inputAlternCurrentLoadPowerFactor"] = inputPowerFactor
    
    simulatedChargeCycle = data["simulatedChargeCycle"] if "simulatedChargeCycle" in data else False
    batteryStateOfCharge = data["simulatedBatteryStateOfCharge"] if "simulatedBatteryStateOfCharge" in data else (data["battery1"]["stateOfCharge"]["value"] + int(data["isBattery2"]) * data["battery2"]["stateOfCharge"]["value"]) / (1 + int(data["isBattery2"]))
    chargeCycleInitialSOC = data['simulatedChargeCycleInitialSOC'] if 'simulatedChargeCycleInitialSOC' in data else (data["battery1"]["stateOfCharge"]["value"] + int(data["isBattery2"]) * data["battery2"]["stateOfCharge"]["value"]) / (1 + int(data["isBattery2"]))

    controllerChargeVoltageBulk = data["controller"]["chargeVoltageBulk"]["value"]
    controllerChargeVoltageFloat = data["controller"]["chargeVoltageFloat"]["value"]
    controllerChargingMinimumVoltage = data["controller"]["chargingMinimumVoltage"]["value"]
    hybridChargeVoltageBulk = data["hybridInverter"]["chargeVoltageBulk"]["value"]
    hybridChargeVoltageFloat = data["hybridInverter"]["chargeVoltageFloat"]["value"]
    hybridChargingMinimumVoltage = data["hybridInverter"]["chargingMinimumVoltage"]["value"]

    if data["inputOperationMode"] in ['Mode1', 'Mode2', 'Mode3', 'Mode5']:
      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503
      if max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 100:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_fPV_Name + '_R1', type=6)
      elif max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 300:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_fPV_Name + '_R2', type=6)
      if max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 500:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_fPV_Name + '_R3', type=6)
      elif max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 700:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_fPV_Name + '_R4', type=6)
      elif max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 900:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_fPV_Name + '_R5', type=6)
      else:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_fPV_Name + '_R6', type=6)

      attempts = 1
      while attempts <= 5:
        try:
          deratingFactorList = [influxDB.InfluxDBreader(query)['_value'][0]] * 4
          influxDB.InfluxDBclose()
          break
        except:
          attempts += 1
          deratingFactorList = [0.5] * 4
          if lampsHeight == 36 and panelsAngle == 0:
            solarCoefficient = 1.0
          else:
            solarCoefficient = ((1.0-panelsAngle/80.0)+(1.0-(lampsHeight-36)/110.0))/2.0-(-0.021*(panelsAngle**2)-0.9857*panelsAngle+48.0)/1000
          deratingFactorList = list(np.array(deratingFactorList) * solarCoefficient)
        finally:
          influxDB.InfluxDBclose()
      
    if data["inputOperationMode"] in ['Mode4', 'Mode5']:
      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503
      if windSpeed <= 4.8:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nWT_Name + "_R1", type=6)
      elif windSpeed <= 7.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nWT_Name + "_R2", type=6)
      elif windSpeed <= 10.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nWT_Name + "_R3", type=6)
      else:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nWT_Name + "_R4", type=6)
      
      attempts = 1
      while attempts <= 5:
        try:
          turbineEfficiency = influxDB.InfluxDBreader(query)['_value'][0]
          influxDB.InfluxDBclose()
          break
        except:
          attempts += 1
          turbineEfficiency = 0.49
        finally:
          influxDB.InfluxDBclose()

    timeMultiplier = data["timeMultiplier"]["value"]
    delta_t = data["queryTime"] / 1000 # Delta de tiempo de la simulación en s -> se definen valores diferentes para offline y online

    twinPVWF = TwinPVWF(name)

    if not data["inputOfflineOperation"]:
      if data["inputOperationMode"] == 'Mode2' and hybridState:
        batteryTemperature = 30.0
        measuredPV_Power = round(values_df["Value"]['PG-003'],3)
        measuredWT_Power = 0.0
        gridState = round(values_df["Value"]['ER-001'])
        measuredHybridDC_Power = round(values_df["Value"]['PC-002'],3)
        measuredGridPower = round(values_df["Value"]['PKVA-003'],3)
        measuredHybridAC_Power = round(values_df["Value"]['PKVA-002'],3)
        PV_Voltage = round(values_df["Value"]['VG-003'],3)
        gridVoltage = round(values_df["Value"]['VAC-004'],3)
        WT_Voltage = 0.0
        directCurrentVoltage = round(values_df["Value"]['VCH-002'],3)
        hybridInverterVoltage = round(values_df["Value"]['VAC-006'],3)
      else:
        batteryTemperature = 30.0
        simulatedInverterState = bool(int(values_df["Value"]['EI-001']))
        measuredPV_Power = round(values_df["Value"]['PG-001'],3)
        measuredWT_Power = round(values_df["Value"]['PG-002'],3)
        measuredControllerDC_Power = round(values_df["Value"]['PC-001'],3)
        PV_Voltage = round(values_df["Value"]['VG-001'],3)
        WT_Voltage = round(values_df["Value"]['VG-002'],3)
        directCurrentVoltage = round(values_df["Value"]['VCH-001'],3)
        inverterVoltage = round(values_df["Value"]['VAC-002'],3)
        directCurrentLoadVoltage = round(values_df["Value"]['VDC-001'],3)
        solarWind['windTurbineRevolutions'] = round(values_df["Value"]['RPM-001'],3)

      solarWind["batteryTemperature"] = batteryTemperature
      
    else:
      if data["inputOperationMode"] == 'Mode2' and hybridState:
        gridState = data["externalGridState"]
      batteryTemperature = 30.0
      PV_Voltage = 0.0
      gridVoltage = 0.0
      WT_Voltage = 0.0
      inverterVoltage = 0.0
      directCurrentLoadVoltage = 0.0
      hybridInverterVoltage = 0.0
      solarWind['windTurbineRevolutions'] = 0.0
    
    PV_Results = twinPVWF.arrayPowerOutput(True, deratingFactorList, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
    WT_Results = twinPVWF.WT_PowerOutput(True, turbineState, turbineEfficiency, windDensity, windSpeed)
    
    if not (data["inputOperationMode"] == 'Mode2' and hybridState):
      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503
      if PV_Results[0] + WT_Results <= 10.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R1", type=6)
      elif PV_Results[0] + WT_Results <= 20.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R2", type=6)
      elif PV_Results[0] + WT_Results <= 30.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R3", type=6)
      elif PV_Results[0] + WT_Results <= 40.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R4", type=6)
      elif PV_Results[0] + WT_Results <= 50.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R5", type=6)
      elif PV_Results[0] + WT_Results <= 60.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R6", type=6)
      elif PV_Results[0] + WT_Results <= 70.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R7", type=6)
      elif PV_Results[0] + WT_Results <= 80.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R8", type=6)
      elif PV_Results[0] + WT_Results <= 90.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R9", type=6)
      elif PV_Results[0] + WT_Results <= 100.0:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R10", type=6)
      else:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = training_nController_Name + "_R11", type=6)
      
      attempts = 1
      while attempts <= 5:
        try:
          controllerEfficiency = influxDB.InfluxDBreader(query)['_value'][0]
          influxDB.InfluxDBclose()
          break
        except:
          attempts += 1
          controllerEfficiency = data["controller"]["efficiency"]["value"]
        finally:
          influxDB.InfluxDBclose()
    else:
      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503
      if not gridState:
        if PV_Results[0]  <= 20.0:
          query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R1", type=6)
        elif PV_Results[0] <= 40.0:
          query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R2", type=6)
        elif PV_Results[0] <= 60.0:
          query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R3", type=6)
        elif PV_Results[0] <= 80.0:
          query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R4", type=6)
        elif PV_Results[0] <= 100.0:
          query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R5", type=6)
        else:
          query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R6", type=6)
      else:
        query = influxDB.QueryCreator(measurement='Solar_eolico', device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid_grid', type=6)
      attempts = 1
      while attempts <= 5:
        try:
          hybridEfficiency = influxDB.InfluxDBreader(query)['_value'][0]
          influxDB.InfluxDBclose()
          break
        except:
          attempts += 1
          hybridEfficiency = data["hybridInverter"]["efficiency"]["value"]
        finally:
          influxDB.InfluxDBclose()

    twinPVWF.twinParameters(controllerEfficiency, inverterEfficiency, hybridEfficiency, batteries, isParallel)

    if monoModuleState or polyModuleState:
      if not data["inputOfflineOperation"] and data["solarRadiation1"]["disabled"]:
        twinPVWF.optimal_f_PV(measuredPV_Power)
        PV_Results = twinPVWF.arrayPowerOutput(data["inputOfflineOperation"], deratingFactorList, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
        if not (data["inputOperationMode"] == 'Mode2' and hybridState):
          twinPVWF.optimal_n_controller(inputDirectCurrentPower, measuredControllerDC_Power)
        elif gridState:
          twinPVWF.optimal_n_hybridController(measuredGridPower, measuredHybridDC_Power, measuredHybridAC_Power)
    elif flexiModuleState or cdteModuleState:
      if not data["inputOfflineOperation"] and data["solarRadiation2"]["disabled"]:
        twinPVWF.optimal_f_PV(measuredPV_Power)
        PV_Results = twinPVWF.arrayPowerOutput(data["inputOfflineOperation"], deratingFactorList, monoModuleState, polyModuleState, flexiModuleState, cdteModuleState, temperature, solarRadiation1, solarRadiation2)
        if not (data["inputOperationMode"] == 'Mode2' and hybridState):
          twinPVWF.optimal_n_controller(inputDirectCurrentPower, measuredControllerDC_Power)
        elif gridState:
          twinPVWF.optimal_n_hybridController(measuredGridPower, measuredHybridDC_Power, measuredHybridAC_Power)

    if turbineState and not data["inputOfflineOperation"] and data["windSpeed"]["disabled"]:
      twinPVWF.optimal_n_WT(measuredWT_Power)
      WT_Results = twinPVWF.WT_PowerOutput(data["inputOfflineOperation"], turbineState, turbineEfficiency, windDensity, windSpeed)
      twinPVWF.optimal_n_controller(inputDirectCurrentPower, measuredControllerDC_Power)

    # solarWind["controllerEfficiency"] = (twinPVWF.n_controller if twinPVWF.n_controller < 100.0 else controllerEfficiency)
    # solarWind["inverterEfficiency"] = (twinPVWF.n_inverter if twinPVWF.n_inverter < 100.0 else inverterEfficiency)
    # solarWind["hybridEfficiency"] = (twinPVWF.n_hybrid if twinPVWF.n_hybrid < 100.0 else hybridEfficiency)
    solarWind["controllerEfficiency"] = controllerEfficiency
    solarWind["inverterEfficiency"] = inverterEfficiency
    solarWind["hybridEfficiency"] = hybridEfficiency

    if data["inputOperationMode"] == 'Mode2' and hybridState:
      solarWind['solarPanelPower'] = PV_Results[0]
      solarWind['monocrystallinePanelTemperature'] = PV_Results[1]
      solarWind['policrystallinePanelTemperature'] = PV_Results[2]
      solarWind['flexPanelTemperature'] = PV_Results[3]
      solarWind['cadmiumTelluridePanelTemperature'] = PV_Results[4]

      directCurrentVoltage  = data["simulatedDirectCurrentVoltage"] if "simulatedDirectCurrentVoltage" in data else 12.6 * (1 + (not isParallel))
      
      twinResults = twinPVWF.ongridTwinOutput(data["inputOfflineOperation"], chargeCycleInitialSOC, batteryState, gridState, inputActivePower, inputPowerFactor, batteryTemperature, directCurrentVoltage, 
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
      if (not data["inputOfflineOperation"] and PV_Voltage == 0.0):
        solarWind['solarPanelVoltage'] = 0.0
      else: 
        solarWind['solarPanelVoltage'] = twinResults[3]
      if (not data["inputOfflineOperation"] and WT_Voltage == 0.0):
        solarWind['windTurbineVoltage'] = 0.0
      else:
        solarWind['windTurbineVoltage'] = twinResults[4]
      solarWind['directCurrentLoadVoltage'] = twinResults[5]
      solarWind['batteryStateOfCharge'] = twinResults[6]
      solarWind['batteryVoltage'] = twinResults[7]
      solarWind['directCurrentVoltage'] = twinResults[8]
      if (not data["inputOfflineOperation"] and inverterVoltage == 0.0) or not simulatedInverterState:
        solarWind['inverterVoltage'] = 0.0
      else:
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

    if trainingState:

      influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
      connectionState = influxDB.InfluxDBconnection()
      timestamp = int(time.mktime(time.strptime(str(datetime.now().year) + "-" + str(datetime.now().month).zfill(2) + "-" + str(datetime.now().day).zfill(2) + " " + str(datetime.now().hour).zfill(2) + ":" + str(datetime.now().minute).zfill(2) + ":" + str(datetime.now().second).zfill(2), '%Y-%m-%d %H:%M:%S')))

      if data["inputOperationMode"] in ['Mode1', 'Mode2', 'Mode3', 'Mode5']:
        if max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 100:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_fPV_Name + '_R1', value = twinPVWF.f_PV, timestamp = timestamp)
        elif max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 300:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_fPV_Name + '_R2', value = twinPVWF.f_PV, timestamp = timestamp)
        elif max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 500:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_fPV_Name + '_R3', value = twinPVWF.f_PV, timestamp = timestamp)
        elif max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 700:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_fPV_Name + '_R4', value = twinPVWF.f_PV, timestamp = timestamp)
        elif max((monoModuleState or polyModuleState)*solarRadiation1, (flexiModuleState or cdteModuleState)*solarRadiation2) <= 900:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_fPV_Name + '_R5', value = twinPVWF.f_PV, timestamp = timestamp)
        else:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_fPV_Name + '_R6', value = twinPVWF.f_PV, timestamp = timestamp)
    
      if data["inputOperationMode"] in ['Mode4', 'Mode5']:
        if windSpeed <= 4.8:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nWT_Name + "_R1", value = twinPVWF.n_WT, timestamp = timestamp)
        elif windSpeed <= 7.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nWT_Name + "_R2", value = twinPVWF.n_WT, timestamp = timestamp)
        elif windSpeed <= 10.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nWT_Name + "_R3", value = twinPVWF.n_WT, timestamp = timestamp)
        else:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nWT_Name + "_R4", value = twinPVWF.n_WT, timestamp = timestamp)

      if not (data["inputOperationMode"] == 'Mode2' and hybridState):
        if twinPVWF.n_controller >= 100: twinPVWF.n_controller = 99.0
        if PV_Results[0] + WT_Results <= 10.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R1", value = twinPVWF.n_controller, timestamp = timestamp)
        elif PV_Results[0] + WT_Results <= 20.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R2", value = twinPVWF.n_controller, timestamp = timestamp)
        elif PV_Results[0] + WT_Results <= 30.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R3", value = twinPVWF.n_controller, timestamp = timestamp)
        elif PV_Results[0] + WT_Results <= 40.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R4", value = twinPVWF.n_controller, timestamp = timestamp)
        elif PV_Results[0] + WT_Results <= 50.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R5", value = twinPVWF.n_controller, timestamp = timestamp)
        elif PV_Results[0] + WT_Results <= 60.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R6", value = twinPVWF.n_controller, timestamp = timestamp)
        elif PV_Results[0] + WT_Results <= 70.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R7", value = twinPVWF.n_controller, timestamp = timestamp)
        elif PV_Results[0] + WT_Results <= 80.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R8", value = twinPVWF.n_controller, timestamp = timestamp)
        elif PV_Results[0] + WT_Results <= 90.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R9", value = twinPVWF.n_controller, timestamp = timestamp)
        elif PV_Results[0] + WT_Results <= 100.0:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R10", value = twinPVWF.n_controller, timestamp = timestamp)
        else:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = training_nController_Name + "_R11", value = twinPVWF.n_controller, timestamp = timestamp)
      else:
        if twinPVWF.n_hybrid >= 100: twinPVWF.n_hybrid = 99.0
        if not gridState:
          if PV_Results[0]  <= 20.0:
            influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R1", value = twinPVWF.n_hybrid, timestamp = timestamp)
          elif PV_Results[0] <= 40.0:
            influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R2", value = twinPVWF.n_hybrid, timestamp = timestamp)
          elif PV_Results[0] <= 60.0:
            influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R3", value = twinPVWF.n_hybrid, timestamp = timestamp)
          elif PV_Results[0] <= 80.0:
            influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R4", value = twinPVWF.n_hybrid, timestamp = timestamp)
          elif PV_Results[0] <= 100.0:
            influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R5", value = twinPVWF.n_hybrid, timestamp = timestamp)
          else:
            influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid' + "_R6", value = twinPVWF.n_hybrid, timestamp = timestamp)
        else:
          influxDB.InfluxDBwriter( measurement = "Solar_eolico", device = "entrenamiento", variable = 'eficienciaControlMode2_hybrid_grid', value = twinPVWF.n_hybrid, timestamp = timestamp)

      influxDB.InfluxDBclose()

    return {"model": solarWind}
