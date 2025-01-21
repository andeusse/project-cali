from flask import request
from flask_restful import Resource
from tools import DBManager
from simulation_models import TwinHydro
import pandas as pd
import numpy as np
import os

class Turbine(Resource):
  def post(self):
    data = request.get_json()
    turbine = {}

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

      query = influxDB.QueryCreator(measurement='Turbinas', type=1)
      
      attempts = 1
      while attempts <= 5:
        try:
          # values_df_temp = influxDB.InfluxDBreader(query)
          values_df_temp = pd.concat(influxDB.InfluxDBreader(query))
          values_df['field'] = values_df_temp['_field']
          values_df['Value'] = values_df_temp['_value']
          timestamp = values_df_temp['_time'].mean()
          turbine['timestamp'] = str(timestamp)
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
    turbineType = 1 if data["turbineType"] == "Pelton" else 2
    if data["inputPressure"]["arrayEnabled"]:
      inputPressureArray = np.repeat(np.array(data["inputPressureArray"]),repeats)
      if iteration <= len(inputPressureArray):
        inputPressure = float(inputPressureArray[iteration-1] * 9.8064) # mH2O to kPa conversion
      else:
        inputPressure = float(inputPressureArray[-1] * 9.8064) # mH2O to kPa conversion
    else:
      inputPressure = ((0.0 if not data["inputPressure"]["value"] else data["inputPressure"]["value"]) if not data["inputPressure"]["disabled"] else round(values_df["Value"]['PT-001'],2)) * 9.8064 # mH2O to kPa conversion
    if data["inputFlow"]["arrayEnabled"]:
      inputFlowArray = np.repeat(np.array(data["inputFlowArray"]),repeats)
      if iteration <= len(inputFlowArray):
        inputFlow = float(inputFlowArray[iteration-1])
      else:
        inputFlow = float(inputFlowArray[-1])
    else:
      inputFlow = (0.0 if not data["inputFlow"]["value"] else data["inputFlow"]["value"]) if not data["inputFlow"]["disabled"] else round(values_df["Value"]['FT-001'],2)
    if data["inputActivePower"]["arrayEnabled"]:
      inputActivePowerArray = np.repeat(np.array(data["inputActivePowerArray"]),repeats)
      if iteration <= len(inputActivePowerArray):
        inputActivePower = float(inputActivePowerArray[iteration-1])
      else:
        inputActivePower = float(inputActivePowerArray[-1])
    else:
      inputActivePower = (0.0 if not data["inputActivePower"]["value"] else data["inputActivePower"]["value"]) if not data["inputActivePower"]["disabled"] else round(values_df["Value"]['PKW-002'],2)
    if data["inputPowerFactor"]["arrayEnabled"]:
      inputPowerFactorArray = np.repeat(np.array(data["inputPowerFactorArray"]),repeats)
      if iteration <= len(inputPowerFactorArray):
        inputPowerFactor = float(inputPowerFactorArray[iteration-1])
      else:
        inputPowerFactor = float(inputPowerFactorArray[-1])
    else:
      inputPowerFactor = (1.0 if not data["inputPowerFactor"]["value"] and data["inputPowerFactor"]["value"]!=0 else data["inputPowerFactor"]["value"]) if not data["inputPowerFactor"]["disabled"] else round((values_df["Value"]['FP-001'] if values_df["Value"]['FP-001'] != 0.0 else 1.0)* (1 if values_df["Value"]['PKVAR-001'] >= 0.0 else -1),2)
    inputDirectCurrentPower = 0.0 if data["inputDirectCurrentPower"] == False or turbineType == 1 else 3.6
    if inputPowerFactor == 0.0: inputPowerFactor = 1.0
    
    turbine["inputPressure"] = round(inputPressure / 9.8064, 2) # kPa to mH2O conversion
    turbine["inputFlow"] = round(inputFlow, 2)
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
    controllerChargingMinimumVoltage = data["controller"]["chargingMinimumVoltage"]["value"]
    controllerSinkOnVoltage = data["controller"]["sinkOnVoltage"]["value"]
    controllerSinkOffVoltage = data["controller"]["sinkOffVoltage"]["value"]
    
    if turbineType == 1:
      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503
      if inputFlow <= 2.1:
        queryTurbine = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_turbina_Pelton_R1", type=0)
        queryController = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_controlador_Pelton_R1", type=0)
      elif inputFlow <= 3.1:
        queryTurbine = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_turbina_Pelton_R2", type=0)
        queryController = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_controlador_Pelton_R2", type=0)
      elif inputFlow <= 4.1:
        queryTurbine = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_turbina_Pelton_R3", type=0)
        queryController = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_controlador_Pelton_R3", type=0)
      else:
        queryTurbine = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_turbina_Pelton_R4", type=0)
        queryController = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_controlador_Pelton_R4", type=0)
      
      attempts = 1
      while attempts <= 5:
        try:
          turbineEfficiency = influxDB.InfluxDBreader(queryTurbine)['_value'][0]
          controllerEfficiency = influxDB.InfluxDBreader(queryController)['_value'][0]
          influxDB.InfluxDBclose()
          break
        except:
          turbineEfficiency = 60.0
          controllerEfficiency = 90.0
          attempts += 1
        finally:
          influxDB.InfluxDBclose()
    else:
      connectionState = influxDB.InfluxDBconnection()
      if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503
      
      if inputFlow <= 4.1:
        queryTurbine = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R0", type=0)
        queryController = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R0", type=0)
      elif inputFlow <= 6.1:
        queryTurbine = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R1", type=0)
        queryController = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R1", type=0)
      elif inputFlow <= 9.1:
        queryTurbine = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R2", type=0)
        queryController = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R2", type=0)
      elif inputFlow <= 11.1:
        queryTurbine = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R3", type=0)
        queryController = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R3", type=0) 
      else:
        queryTurbine = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R4", type=0)
        queryController = influxDB.QueryCreator(measurement='Turbinas', device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R4", type=0)     
      
      attempts = 1
      while attempts <= 5:
        try:
          turbineEfficiency = influxDB.InfluxDBreader(queryTurbine)['_value'][0]
          controllerEfficiency = influxDB.InfluxDBreader(queryController)['_value'][0]
          influxDB.InfluxDBclose()
          break
        except:
          turbineEfficiency = 54.0
          controllerEfficiency = 72.0
          attempts += 1
        finally:
          influxDB.InfluxDBclose()

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
        simulatedDirectCurrentVoltage = round(values_df["Value"]['VCH-001'],2)
        if values_df["Value"]['AUX-1001'] == "OFF":
          simulatedSinkLoadState = False
          sinkLoadMode = "Off"
        elif values_df["Value"]['AUX-1001'] == "ON":
          simulatedSinkLoadState = True
          sinkLoadMode = "On"
      else:
        T_bat = round(values_df["Value"]['TE-004'],2)
        P_h_meas = round(values_df["Value"]['PG-002'],2)
        P_CC_meas = round(values_df["Value"]['PC-002'],2)
        V_t = round(values_df["Value"]['VG-002'],2)
        simulatedDirectCurrentVoltage = round(values_df["Value"]['VCH-002'],2)
        if values_df["Value"]['AUX-1002'] == "OFF":
          simulatedSinkLoadState = False
          sinkLoadMode = "Off"
        elif values_df["Value"]['AUX-1002'] == "ON":
          simulatedSinkLoadState = True
          sinkLoadMode = "On"
        elif values_df["Value"]['AUX-1002'] == "AUTO":
          sinkLoadMode = "Auto"

      V_CA = round(values_df["Value"]['VAC-002'],2)
      simulatedInverterState = bool(int(values_df["Value"]['EI-001']))

    else:
      T_bat = 30.0
      V_CA = 0
      V_t = 0
    
    turbine["batteryTemperature"] = T_bat

    twinHydro.turbineType(turbineType)
    twinHydro.twinParameters(turbineEfficiency, controllerEfficiency, inverterEfficiency)
    P_h = twinHydro.PowerOutput(inputPressure, inputFlow)
    
    if not data["inputOfflineOperation"] and data["inputPressure"]["disabled"] and data["inputFlow"]["disabled"]:
      twinHydro.optimal_n_t(twinHydro.n_t, P_h_meas, inputPressure, inputFlow)
      P_h = twinHydro.PowerOutput(inputPressure, inputFlow)
      twinHydro.optimal_n_controller(controllerEfficiency, P_h, inputDirectCurrentPower, P_CC_meas)
    
    turbine["controllerEfficiency"] = twinHydro.n_controller
    turbine["inverterEfficiency"] = twinHydro.n_inverter

    if "simulatedDirectCurrentVoltage" in data:
      simulatedDirectCurrentVoltage = data["simulatedDirectCurrentVoltage"]
    else:
      P_CC = (P_h * controllerEfficiency / 100) - inputDirectCurrentPower
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
                                     controllerChargeVoltageBulk, controllerChargeVoltageFloat, controllerChargingMinimumVoltage, sinkLoadMode, simulatedSinkLoadState, controllerSinkOnVoltage, controllerSinkOffVoltage, 
                                     delta_t*timeMultiplier, V_t, V_CA)

    turbine["turbinePower"] = P_h

    turbine["controllerPower"] = results[0]
    turbine["inverterInputPower"] = results[1]
    turbine["batteryPower"] = results[2]
    if (not data["inputOfflineOperation"] and V_t == 0.0) or turbine["turbinePower"] == 0.0:
      turbine["turbineVoltage"] = 0.0
    else: 
      turbine["turbineVoltage"] = results[3]
    if not data["inputOfflineOperation"] and V_CA == 0.0:
      turbine["inverterOutputVoltage"] = 0.0
    else: 
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

    if trainingState:

      influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)
      connectionState = influxDB.InfluxDBconnection()
  
      if turbineType == 1:
        if inputFlow <= 2.1:
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_turbina_Pelton_R1", value = twinHydro.n_t, timestamp = timestamp)
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_controlador_Pelton_R1", value = twinHydro.n_controller, timestamp = timestamp)
        elif inputFlow <= 3.1:
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_turbina_Pelton_R2", value = twinHydro.n_t, timestamp = timestamp)
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_controlador_Pelton_R2", value = twinHydro.n_controller, timestamp = timestamp)
        elif inputFlow <= 4.1:
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_turbina_Pelton_R3", value = twinHydro.n_t, timestamp = timestamp)
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_controlador_Pelton_R3", value = twinHydro.n_controller, timestamp = timestamp)
        else:
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_turbina_Pelton_R4", value = twinHydro.n_t, timestamp = timestamp)
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_controlador_Pelton_R4", value = twinHydro.n_controller, timestamp = timestamp)
      else:
        if inputFlow <= 4.1:
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R0", value = twinHydro.n_t, timestamp = timestamp)
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R0", value = twinHydro.n_controller, timestamp = timestamp)
        elif inputFlow <= 6.1:
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R1", value = twinHydro.n_t, timestamp = timestamp)
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R1", value = twinHydro.n_controller, timestamp = timestamp)
        elif inputFlow <= 9.1:
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R2", value = twinHydro.n_t, timestamp = timestamp)
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R2", value = twinHydro.n_controller, timestamp = timestamp)
        elif inputFlow <= 11.1:
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R3", value = twinHydro.n_t, timestamp = timestamp)
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R3", value = twinHydro.n_controller, timestamp = timestamp)
        else:
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_turbina_Turgo_R4", value = twinHydro.n_t, timestamp = timestamp)
          influxDB.InfluxDBwriter( measurement = "Turbinas", device = "entrenamiento", variable = "eficiencia_controlador_Turgo_R4", value = twinHydro.n_controller, timestamp = timestamp)


      influxDB.InfluxDBclose()

    return {"model": turbine}
