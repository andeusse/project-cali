from flask import request
from flask_restful import Resource
from simulation_models.Biogas import BiogasModel
import pandas as pd
from utils import Biogas_Start

class Biogas(Resource):
  def post(self):
    data = request.get_json()
    
    biogas_input = {}
    biogas_output = {}

    biogas_input["name"] = data["name"]
    biogas_input["anaerobicReactorVolume1"]=data["anaerobicReactorVolume1"]["value"]
    biogas_input["anaerobicReactorVolume2"]=data["anaerobicReactorVolume2"]["value"]
    biogas_input["biogasTankVolume1"]=data["biogasTankVolume1"]["value"]
    biogas_input["biogasTankVolume2"]=data["biogasTankVolume2"]["value"]
    biogas_input["biogasTankVolume3"]=data["biogasTankVolume3"]["value"]
    biogas_input["inputOperationMode"]=int(data["inputOperationMode"][4:])
    biogas_input["inputSubstrateConditions"]=data["inputSubstrateConditions"]
    biogas_input["inputElementalAnalysisCarbonContent"]=data["inputElementalAnalysisCarbonContent"]["value"]
    biogas_input["inputElementalAnalysisHydrogenContent"]=data["inputElementalAnalysisHydrogenContent"]["value"]
    biogas_input["inputElementalAnalysisOxygenContent"]=data["inputElementalAnalysisOxygenContent"]["value"]
    biogas_input["inputElementalAnalysisNitrogenContent"]=data["inputElementalAnalysisNitrogenContent"]["value"]
    biogas_input["inputElementalAnalysisSulfurContent"]=data["inputElementalAnalysisSulfurContent"]["value"]
    biogas_input["inputProximateAnalysisTotalSolids"]=data["inputProximateAnalysisTotalSolids"]["value"]
    biogas_input["inputProximateAnalysisVolatileSolids"]=data["inputProximateAnalysisVolatileSolids"]["value"]
    biogas_input["inputProximateAnalysisDensity"]=data["inputProximateAnalysisDensity"]["value"]
    biogas_input["inputDigitalTwin"]=data["inputDigitalTwin"]
    biogas_input["inputDigitalTwinStepTime"]=data["inputDigitalTwinStepTime"]["value"]
    biogas_input["inputDigitalTwinTrainingTime"]=data["inputDigitalTwinTrainingTime"]["value"]
    biogas_input["inputDigitalTwinForecastTime"]=data["inputDigitalTwinForecastTime"]["value"]
    biogas_input["inputKineticParameterInitialValue"]=data["inputKineticParameterInitialValue"]["value"]
    biogas_input["inputSpeedLawOrder"]=int(data["inputSpeedLawOrder"][5:])
    biogas_input["inputSpeedLawExponentialFactor"]=data["inputSpeedLawExponentialFactor"]["value"]
    biogas_input["inputSpeedLawStartEnergy"]=data["inputSpeedLawStartEnergy"]["value"]
    biogas_input["inputPump104"]=data["inputPump104"]
    biogas_input["inputPump104HydraulicRetentionTime"]=data["inputPump104HydraulicRetentionTime"]["value"]
    biogas_input["inputPump104StartTime"]=data["inputPump104StartTime"]["value"]
    biogas_input["inputPump104StartsPerDay"]=data["inputPump104StartsPerDay"]["value"]
    biogas_input["inputPump102"]=data["inputPump102"]
    biogas_input["inputPump102Flow"]=data["inputPump102Flow"]["value"]
    biogas_input["inputPump102StartTime"]=data["inputPump102StartTime"]["value"]
    biogas_input["inputPump102StartsPerDay"]=data["inputPump102StartsPerDay"]["value"]
    biogas_input["inputPump101"]=data["inputPump101"]
    biogas_input["inputPump101Flow"]=data["inputPump101Flow"]["value"]
    biogas_input["inputPump101StartTime"]=data["inputPump101StartTime"]["value"]
    biogas_input["inputPump101StartsPerDay"]=data["inputPump101StartsPerDay"]["value"]
    biogas_input["inputTemperature101"]=data["inputTemperature101"]["value"]
    biogas_input["inputTemperature102"]=data["inputTemperature102"]["value"]

    if biogas_input["inputDigitalTwin"] == 1:
      Biogas_plant_DT_ini = Biogas_Start.BiogasStart()
      Biogas_plant_DT_ini.starting(VR1 = biogas_input["anaerobicReactorVolume1"], VR2 = biogas_input["anaerobicReactorVolume2"], VG1 = biogas_input["biogasTankVolume1"], VG2 = biogas_input["biogasTankVolume2"],
                                VG3 = biogas_input["biogasTankVolume3"], tp = biogas_input["inputDigitalTwinStepTime"])
      
      Biogas_plant_DT = Biogas_plant_DT_ini.data
      Biogas_plant_DT.GetValuesFromBiogasPlant()
      if biogas_input["inputOperationMode"] == 1:
        Biogas_plant_DT.Substrate_conditions(Online = biogas_input["inputSubstrateConditions"], manual_sustrate= biogas_input["inputPump104"], ST=biogas_input["inputProximateAnalysisTotalSolids"], 
                                            SV=biogas_input["inputProximateAnalysisVolatileSolids"], Cc=biogas_input["inputElementalAnalysisCarbonContent"], Ch=biogas_input["inputElementalAnalysisHydrogenContent"],
                                              Co=biogas_input["inputElementalAnalysisOxygenContent"], Cn=biogas_input["inputElementalAnalysisNitrogenContent"], Cs=biogas_input["inputElementalAnalysisSulfurContent"],
                                                rho = biogas_input["inputProximateAnalysisDensity"], 
                                                ST_R101=10, SV_R101=1, Cc_R101=40.48, Ch_R101=5.29, Co_R101=29.66, Cn_R101=1.37, Cs_R101=0.211, rho_R101 = 1000,
                                                  ST_R102=0, SV_R102=0, Cc_R102=0, Ch_R102=0, Co_R102=0, Cn_R102=0, Cs_R102=0, rho_R102 = 0) #Definir las condiciones iniciales con las que se llena cada reactor antes de iniciar el gemelo, para este modo de operación las condiciones del reactor R-102 no importan las dejo en 0
        
        Biogas_plant_DT.Pump104_Operation_1_2(manual_P104=biogas_input["inputPump104"], TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
        Biogas_plant_DT.Temperature_R101(manual_temp_R101 = 1, Temp_R101=biogas_input["inputTemperature101"])    #Falta el input de manual automático para temperatura de R101
        Biogas_plant_DT.V_101_DT()
        Biogas_plant_DT.V_102_DT()
        Biogas_plant_DT.V_103_DT()
        Biogas_plant_DT.R101_DT_operation_1()


        """
        #variables de salida real-time operation
        """
        #A la entrada de R101
        VolatileSolidsInletR101 = Biogas_plant_DT.Csus_ini    #Concentración de sólidos volátiles que ingresa a la planta por R101 [M][mol/L]
        TotalSolidsInletR101 = Biogas_plant_DT.Csus_ini_ST    #Concentración de sólidos totales que ingresa a la planta por R101 [M][mol/L]
        n = Biogas_plant_DT.n                                 #Subindice de carbono en la ecuación empírica del sustrato
        a = Biogas_plant_DT.a                                 #Subindice de hidrógeno en la ecuación empírica del sustrato
        b = Biogas_plant_DT.b                                 #Subindice de oxígeno en la ecuacción empírica del sustrato
        c = Biogas_plant_DT.c                                 #Subindice de nitrogeno en la ecuacción empírica del sustrato
        d = Biogas_plant_DT.d                                 #Subindice de azufre en la ecuacción empírica del sustrato
        Pump101Flow = Biogas_plant_DT.Q_P104                  #Flujo volumétro de la bomba P104 [L/h]

        """
        #En el tanque de biogas V-101

        # En la interfaz ¿Es posible poner selectores para visualizar diferentes parámetros del biogás?
        # Selector 1: Para el tanque: Seleccionar: [acumulado, almacenado]
        # Selector 2: Para las variables de total biogas: [Presión, volumen normal]
        # Selector 3: Para los compuestos del biogas: [Concentración, Volumen_parcial_normal, moles]
        # Selector 4: Para la humedad del biogás: [Humedad relativa, moles]
        """
        #Biogas almacenado por volumen
        StorageBiogasVolumeV101 = Biogas_plant_DT.V_normal_V101     #Volumen de biogás almacenado (actual) en el tanque V-101 [NL]

        #Biogás acumulado por volumen
        AcumBiogasVolumenV101 = Biogas_plant_DT.Vnormal_acum_v101   #Volumen de biogás total producido por la planta (acumulado) en el tanque V-101 [NL] 

        #Biogás almacenado en variable presión
        StorageBiogasPressureV101 = Biogas_plant_DT.PT103v.iloc[-1]  #Presión de biogás almacenado (actual) en el tanque V-101 [kPa]

        #Biogás acumulado por presión
        AcumBiogasPressureV101 = Biogas_plant_DT.Pacum_v101         #Presión de biogás total producida en el tanque V-101 [kPa]

        #compuestos del biogás
        # Visualización de volumen parcial en el gemelo digital
        StorageCH4_V101Volume = Biogas_plant_DT.V_normal_CH4_V101   #Volumen de metano almacenado (actual) en el tanque V-101 [NL]
        StorageCO2_V101Volume = Biogas_plant_DT.V_normal_CO2_V101   #Volumen de dióxido de carbono almacenado (actual) en el tanque V-101 [NL]
        StorageH2S_V101Volume = Biogas_plant_DT.V_normal_H2S_V101   #Volumen de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [NL]
        StorageO2_V101Volume = Biogas_plant_DT.V_normal_O2_V101     #Volumen de oxígeno almacenado (actual) en el tanque V-101 [NL]
        StorageH2_V101Volume = Biogas_plant_DT.V_normal_H2_V101     #Volumen de hidrógeno almacenado (actual) en el tanque V-101 [NL]

        # Visualización por concentraciones en el gemelo digital
        StorageCH4_V101Concentration = Biogas_plant_DT.AT103A1v.iloc[-1]   #Concentración de metano almacenado (actual) en el tanque V-101 [%]
        StorageCO2_V101Concentration = Biogas_plant_DT.AT103A2v.iloc[-1]   #Concentración de dióxido de carbono almacenado (actual) en el tanque V-101 [%]
        StorageH2S_V101Concentration = Biogas_plant_DT.AT103A3v.iloc[-1]   #Concentración de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [%]
        StorageO2_V101Concentration = Biogas_plant_DT.AT103A4v.iloc[-1]    #Concentración de oxígeno almacenado (actual) en el tanque V-101 [%]
        StorageH2_V101Concentration = Biogas_plant_DT.AT103A5v.iloc[-1]    #Concentración de hidrógeno almacenado (actual) en el tanque V-101 [%]

        # Visualización por moles en el gemelo digital
        StorageCH4_V101moles = Biogas_plant_DT.mol_CH4_R101               #moles de metano almacenado (actual) en el tanque V-101 [%]
        StorageCO2_V101moles = Biogas_plant_DT.mol_CO2_V101               #moles de dióxido de carbono almacenado (actual) en el tanque V-101 [%]
        StorageH2S_V101moles = Biogas_plant_DT.mol_H2S_V101               #moles de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [%]
        StorageO2_V101moles = Biogas_plant_DT.mol_O2_V101                 #moles de oxígeno almacenado (actual) en el tanque V-101 [%]
        StorageH2_V101moles = Biogas_plant_DT.mol_H2_V101                 #moles de hidrógeno almacenado (actual) en el tanque V-101 [%]

        #Humedad del biogás en humedad relativa
        Relative_humidity_V101 = Biogas_plant_DT.AT103Bv.iloc[-1]          #[%]

        #Humedad del biogás en moles
        moles_humidity_V101 = Biogas_plant_DT.mol_H2O_V102                 #[mol]


        """
        #En el tanque de biogas V-102

        # En la interfaz ¿Es posible poner selectores para visualizar diferentes parámetros del biogás?
        # Selector 1: Para el tanque: Seleccionar: [acumulado, almacenado]
        # Selector 2: Para las variables de total biogas: [Presión, volumen normal]
        # Selector 3: Para los compuestos del biogas: [Concentración, Volumen_parcial_normal, moles]
        # Selector 4: Para la humedad del biogás: [Humedad relativa, moles]
        """

        #falta ingresar el módulo de aprendizaje de máquinas se corre aquí, de aqui se generan las matrices para las gráficas de resultados

      elif biogas_input["inputOperationMode"] == 2:
        Biogas_plant_DT.Substrate_conditions(Online = biogas_input["inputSubstrateConditions"], manual_sustrate= biogas_input["inputPump104"], ST=biogas_input["inputProximateAnalysisTotalSolids"], 
                                            SV=biogas_input["inputProximateAnalysisVolatileSolids"], Cc=biogas_input["inputElementalAnalysisCarbonContent"], Ch=biogas_input["inputElementalAnalysisHydrogenContent"],
                                              Co=biogas_input["inputElementalAnalysisOxygenContent"], Cn=biogas_input["inputElementalAnalysisNitrogenContent"], Cs=biogas_input["inputElementalAnalysisSulfurContent"],
                                                rho = biogas_input["inputProximateAnalysisDensity"], 
                                                ST_R101=10, SV_R101=1, Cc_R101=40.48, Ch_R101=5.29, Co_R101=29.66, Cn_R101=1.37, Cs_R101=0.211, rho_R101 = 1000,
                                                  ST_R102=0, SV_R102=0, Cc_R102=0, Ch_R102=0, Co_R102=0, Cn_R102=0, Cs_R102=0, rho_R102 = 0) #Definir las condiciones iniciales con las que se llena cada reactor antes de iniciar el gemelo, para este modo de operación las condiciones del reactor R-102 no importan las dejo en 0
        
        
        Biogas_plant_DT.Pump104_Operation_1_2(manual_P104=biogas_input["inputPump104"], TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
        Biogas_plant_DT.Temperature_R101(manual_temp_R101 = 1, Temp_R101=biogas_input["inputTemperature101"])    #Falta el input de manual automático para temperatura de R101
        Biogas_plant_DT.V_101_DT()
        Biogas_plant_DT.V_102_DT()
        Biogas_plant_DT.V_103_DT()
        Biogas_plant_DT.R101_DT_Operation_2()


    elif biogas_input["inputOperationMode"] == 3:
      pass
    elif biogas_input["inputOperationMode"] == 4:
      pass
    else:
      pass
    
    print(biogas_input)
    print(biogas_output)

    return {}, 200