from flask import request
from flask_restful import Resource
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
                                VG3 = biogas_input["biogasTankVolume3"], tp = biogas_input["inputDigitalTwinStepTime"], ST_R101=10, SV_R101=1, Cc_R101=40.48, Ch_R101=5.29, Co_R101=29.66, Cn_R101=1.37, Cs_R101=0.211, rho_R101 = 1000,
                                ST_R102=10, SV_R102=1, Cc_R102=40.48, Ch_R102=5.29, Co_R102=29.66, Cn_R102=1.37, Cs_R102=0.211, rho_R102 = 1000) #Definir las condiciones iniciales del sustrato en R101 y R102, si es modo de operación 1 o 2 las condiciones de R102 son 0.
      
      Biogas_plant_DT = Biogas_plant_DT_ini.data
      Biogas_plant_DT.GetValuesFromBiogasPlant()
      Biogas_plant_DT.Substrate_conditions(Online = biogas_input["inputDigitalTwin"], manual_sustrate=biogas_input["inputSubstrateConditions"], ST=biogas_input["inputProximateAnalysisTotalSolids"], 
                                             SV=biogas_input["inputProximateAnalysisVolatileSolids"], Cc=biogas_input["inputElementalAnalysisCarbonContent"], Ch=biogas_input["inputElementalAnalysisHydrogenContent"],
                                             Co=biogas_input["inputElementalAnalysisOxygenContent"], Cn=biogas_input["inputElementalAnalysisNitrogenContent"], Cs=biogas_input["inputElementalAnalysisSulfurContent"], rho = biogas_input["inputProximateAnalysisDensity"])
        
      if biogas_input["inputOperationMode"] == 1:
        
        Biogas_plant_DT.Pump104_Operation_1_2(manual_P104=biogas_input["inputPump104"], TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
        Biogas_plant_DT.Temperature_R101(manual_temp_R101 = 1, Temp_R101=biogas_input["inputTemperature101"])    #Falta el input de manual automático para temperatura de R101
        Biogas_plant_DT.V_101_DT()
        Biogas_plant_DT.V_102_DT()
        Biogas_plant_DT.V_107_DT()
        Biogas_plant_DT.R101_DT_operation_1()

        '''
        #falta ingresar el módulo de aprendizaje de máquinas se corre aquí, de aqui se generan las matrices para las gráficas de resultados
        '''
        """
        Salidas solo para el modo de operación 1
        """
        '''
        A la salida de R-101
        '''

        FlowExit_R101 = Biogas_plant_DT.Q_P104                              #eL Flujo volumétro de la salida de R-101 es igual al flujo de la bomba P-104 [L/h]
        TotalSolidsOutR101 = Biogas_plant_DT.ST_R101                        #Concentración de sólidos totales a la salida de R101 [%]
        VolatileSolidsOutR101 = Biogas_plant_DT.SV_R101                     #Concentración de sólidos volátiles a la salida de R101 [%]
        SubstrateConcentrationOutR101 = Biogas_plant_DT.Csus_ini_R101       #Concentración de sustrato a la salida de R101 [M]

      elif biogas_input["inputOperationMode"] == 2:
               
        Biogas_plant_DT.Pump104_Operation_1_2 (manual_P104=biogas_input["inputPump104"], TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
        Biogas_plant_DT.Pump101_Operation_2 (manual_P101=biogas_input["inputPump101"], FT_P101=biogas_input["inputPump101StartsPerDay"], TTO_P101=biogas_input["inputPump101StartTime"], Q_P101 = biogas_input["inputPump101Flow"])
        Biogas_plant_DT.Temperature_R101(manual_temp_R101 = 1, Temp_R101=biogas_input["inputTemperature101"])    #Falta el input de manual automático para temperatura de R101
        Biogas_plant_DT.V_101_DT()
        Biogas_plant_DT.V_102_DT()
        Biogas_plant_DT.V_107_DT()
        Biogas_plant_DT.R101_DT_Operation_2()

        '''
        #falta ingresar el módulo de aprendizaje de máquinas se corre aquí, de aqui se generan las matrices para las gráficas de resultados
        '''
        """
        Salidas solo para el modo de operación 2
        """
        '''
        A la salida de R-101
        '''

        FlowExit_R101_1 = Biogas_plant_DT.Q_P104                            #eL Flujo volumétro de la salida de R-101 es igual al flujo de la bomba P-104 [L/h]
        FlowExit_R101_2 = Biogas_plant_DT.Q_P101                            #Sale flujo por el rebose del reactor y por la bomba 
        TotalSolidsOutR101 = Biogas_plant_DT.ST_R101                        #Concentración de sólidos totales a la salida de R101 [%]
        VolatileSolidsOutR101 = Biogas_plant_DT.SV_R101                     #Concentración de sólidos volátiles a la salida de R101 [%]
        SubstrateConcentrationOutR101 = Biogas_plant_DT.Csus_ini_R101       #Concentración de sustrato a la salida de R101 [M]

      elif biogas_input["inputOperationMode"] == 3:
       
        Biogas_plant_DT.Pump104_Operation_3_4_5(manual_P104=biogas_input["inputPump104"], TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
        Biogas_plant_DT.Pump101_Operation_3_5(manual_P101=biogas_input["inputPump101"])
        Biogas_plant_DT.Temperature_R101(manual_temp_R101 = 1, Temp_R101=biogas_input["inputTemperature101"])    #Falta el input de manual automático para temperatura de R101
        Biogas_plant_DT.Temperature_R102(manual_temp_R102=1, Temp_R102=biogas_input["inputTemperature102"])      #Falta el input de manual automático para temperatura de R102
        Biogas_plant_DT.V_101_DT()
        Biogas_plant_DT.V_102_DT()
        Biogas_plant_DT.V_107_DT()
        Biogas_plant_DT.R101_DT_operation_3_5()
        Biogas_plant_DT.R102_DT_Operation_3()

        '''
        #falta ingresar el módulo de aprendizaje de máquinas se corre aquí, de aqui se generan las matrices para las gráficas de resultados
        '''
        """
        Salidas solo para el modo de operación 3
        """
        '''
        A la salida de R-101 y la entrada de R-102
        '''
        FlowExit_R101 = Biogas_plant_DT.Q_P101                            #eL Flujo volumétro de la salida de R-101 es igual al flujo de la bomba P-104 [L/h]
        TotalSolidsOutR101 = Biogas_plant_DT.ST_R101                        #Concentración de sólidos totales a la salida de R101 [%]
        VolatileSolidsOutR101 = Biogas_plant_DT.SV_R101                     #Concentración de sólidos volátiles a la salida de R101 [%]
        SubstrateConcentrationOutR101 = Biogas_plant_DT.Csus_ini_R101       #Concentración de sustrato a la salida de R101 [M]

        """
        A la salida de R-102 solo una salida
        """
        FlowExit_R102 = Biogas_plant_DT.Q_P101                            #eL Flujo volumétro de la salida de R-101 es igual al flujo de la bomba P-104 [L/h]
        TotalSolidsOutR102 = Biogas_plant_DT.ST_R102                        #Concentración de sólidos totales a la salida de R101 [%]
        VolatileSolidsOutR102 = Biogas_plant_DT.SV_R102                     #Concentración de sólidos volátiles a la salida de R101 [%]
        SubstrateConcentrationOutR102 = Biogas_plant_DT.Csus_ini_R102       #Concentración de sustrato a la salida de R101 [M]


      elif biogas_input["inputOperationMode"] == 4:
        
        Biogas_plant_DT.Pump104_Operation_3_4_5(manual_P104=biogas_input["inputPump104"], TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
        Biogas_plant_DT.Pump101_Operation_4(manual_P101=biogas_input["inputPump101"])
        Biogas_plant_DT.Pump102_Operation_4_5(manual_P102=biogas_input["inputPump102"], FT_P102=biogas_input["inputPump102StartsPerDay"], TTO_P102=biogas_input["inputPump102StartTime"], Q_P102 = biogas_input["inputPump102Flow"])
        Biogas_plant_DT.Temperature_R101(manual_temp_R101 = 1, Temp_R101=biogas_input["inputTemperature101"])    #Falta el input de manual automático para temperatura de R101
        Biogas_plant_DT.Temperature_R102(manual_temp_R102=1, Temp_R102=biogas_input["inputTemperature102"])      #Falta el input de manual automático para temperatura de R102
        Biogas_plant_DT.V_101_DT()
        Biogas_plant_DT.V_102_DT()
        Biogas_plant_DT.V_107_DT()
        Biogas_plant_DT.R101_DT_Operation_4()
        Biogas_plant_DT.R102_DT_Operation_4()

        '''
        #falta ingresar el módulo de aprendizaje de máquinas se corre aquí, de aqui se generan las matrices para las gráficas de resultados
        '''
        """
        Salidas solo para el modo de operación 4
        """
        '''
        A la salida de R-101 y la entrada de R-102
        '''
        FlowExit_R101 = Biogas_plant_DT.Q_P101                            #eL Flujo volumétro de la salida de R-101 es igual al flujo de la bomba P-104 [L/h]
        TotalSolidsOutR101 = Biogas_plant_DT.ST_R101                        #Concentración de sólidos totales a la salida de R101 [%]
        VolatileSolidsOutR101 = Biogas_plant_DT.SV_R101                     #Concentración de sólidos volátiles a la salida de R101 [%]
        SubstrateConcentrationOutR101 = Biogas_plant_DT.Csus_ini_R101       #Concentración de sustrato a la salida de R101 [M]

        """
        A la salida de R-102 solo una salida
        """
        FlowExit_R102_1 = Biogas_plant_DT.Q_P104                            #Salida en el rebose de R102 [L/h]
        FlowExit_R102_2 = Biogas_plant_DT.Q_P102                            #Salida por la bomba P-102 [L/h]
        TotalSolidsOutR102 = Biogas_plant_DT.ST_R102                        #Concentración de sólidos totales a la salida de R101 [%]
        VolatileSolidsOutR102 = Biogas_plant_DT.SV_R102                     #Concentración de sólidos volátiles a la salida de R101 [%]
        SubstrateConcentrationOutR102 = Biogas_plant_DT.Csus_ini_R102       #Concentración de sustrato a la salida de R101 [M]

      elif biogas_input["inputOperationMode"] == 5:         #Agregar este modo de operación
        
        Biogas_plant_DT.Pump104_Operation_3_4_5(manual_P104=biogas_input["inputPump104"], TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
        Biogas_plant_DT.Pump101_Operation_3_5(manual_P101=biogas_input["inputPump101"])
        Biogas_plant_DT.Pump102_Operation_4_5(manual_P102=biogas_input["inputPump102"], FT_P102=biogas_input["inputPump102StartsPerDay"], TTO_P102=biogas_input["inputPump102StartTime"], Q_P102 = biogas_input["inputPump102Flow"])
        Biogas_plant_DT.Temperature_R101(manual_temp_R101 = 1, Temp_R101=biogas_input["inputTemperature101"])    #Falta el input de manual automático para temperatura de R101
        Biogas_plant_DT.Temperature_R102(manual_temp_R102=1, Temp_R102=biogas_input["inputTemperature102"])      #Falta el input de manual automático para temperatura de R102
        Biogas_plant_DT.V_101_DT()
        Biogas_plant_DT.V_102_DT()
        Biogas_plant_DT.V_107_DT()

        '''
        #falta ingresar el módulo de aprendizaje de máquinas se corre aquí, de aqui se generan las matrices para las gráficas de resultados
        '''
        """
        Salidas solo para el modo de operación 5
        """
        '''
        A la salida de R-101 y la entrada de R-102
        '''
        FlowExit_R101 = Biogas_plant_DT.Q_P101                              #eL Flujo volumétro de la salida de R-101 es igual al flujo de la bomba P-104 [L/h]
        TotalSolidsOutR101 = Biogas_plant_DT.ST_R101                        #Concentración de sólidos totales a la salida de R101 [%]
        VolatileSolidsOutR101 = Biogas_plant_DT.SV_R101                     #Concentración de sólidos volátiles a la salida de R101 [%]
        SubstrateConcentrationOutR101 = Biogas_plant_DT.Csus_ini_R101       #Concentración de sustrato a la salida de R101 [M]

        """
        A la salida de R-102 solo una salida
        """
        FlowExit_R102_1 = Biogas_plant_DT.Q_P104                            #Salida en el rebose de R102 [L/h]
        FlowExit_R102_2 = Biogas_plant_DT.Q_P102                            #Salida por la bomba P-102 [L/h]
        TotalSolidsOutR102 = Biogas_plant_DT.ST_R102                        #Concentración de sólidos totales a la salida de R101 [%]
        VolatileSolidsOutR102 = Biogas_plant_DT.SV_R102                     #Concentración de sólidos volátiles a la salida de R101 [%]
        SubstrateConcentrationOutR102 = Biogas_plant_DT.Csus_ini_R102       #Concentración de sustrato a la salida de R101 [M]

    
      """
      #variables de salida real-time operation para todos los modos de operación en el gemelo digital
      """
      """
      #A la entrada de R101
      """
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
      StorageCH4_V101moles = Biogas_plant_DT.mol_CH4_V101               #moles de metano almacenado (actual) en el tanque V-101 [%]
      StorageCO2_V101moles = Biogas_plant_DT.mol_CO2_V101               #moles de dióxido de carbono almacenado (actual) en el tanque V-101 [%]
      StorageH2S_V101moles = Biogas_plant_DT.mol_H2S_V101               #moles de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [%]
      StorageO2_V101moles = Biogas_plant_DT.mol_O2_V101                 #moles de oxígeno almacenado (actual) en el tanque V-101 [%]
      StorageH2_V101moles = Biogas_plant_DT.mol_H2_V101                 #moles de hidrógeno almacenado (actual) en el tanque V-101 [%]

      #Humedad del biogás en humedad relativa
      Relative_humidity_V101 = Biogas_plant_DT.AT103Bv.iloc[-1]          #[%]

      #Humedad del biogás en moles
      moles_humidity_V101 = Biogas_plant_DT.mol_H2O_V101                 #[mol]


      """
      #En el tanque de biogas V-102

      # En la interfaz ¿Es posible poner selectores para visualizar diferentes parámetros del biogás?
      # Selector 1: Para el tanque: Seleccionar: [acumulado, almacenado]
      # Selector 2: Para las variables de total biogas: [Presión, volumen normal]
      # Selector 3: Para los compuestos del biogas: [Concentración, Volumen_parcial_normal, moles]
      # Selector 4: Para la humedad del biogás: [Humedad relativa, moles]
      """

      #Biogas almacenado por volumen
      StorageBiogasVolumeV102 = Biogas_plant_DT.V_normal_V102     #Volumen de biogás almacenado (actual) en el tanque V-101 [NL]

      #Biogás acumulado por volumen
      AcumBiogasVolumenv102 = Biogas_plant_DT.Vnormal_acum_v102   #Volumen de biogás total producido por la planta (acumulado) en el tanque V-101 [NL] 

      #Biogás almacenado en variable presión
      StorageBiogasPressureV102 = Biogas_plant_DT.PT104v.iloc[-1]  #Presión de biogás almacenado (actual) en el tanque V-101 [kPa]

      #Biogás acumulado por presión
      AcumBiogasPressureV102 = Biogas_plant_DT.Pacum_v102         #Presión de biogás total producida en el tanque V-101 [kPa]

      #compuestos del biogás
      # Visualización de volumen parcial en el gemelo digital
      StorageCH4_V102Volume = Biogas_plant_DT.V_normal_CH4_V102   #Volumen de metano almacenado (actual) en el tanque V-101 [NL]
      StorageCO2_V102Volume = Biogas_plant_DT.V_normal_CO2_V102   #Volumen de dióxido de carbono almacenado (actual) en el tanque V-101 [NL]
      StorageH2S_V102Volume = Biogas_plant_DT.V_normal_H2S_V102   #Volumen de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [NL]
      StorageO2_V102Volume = Biogas_plant_DT.V_normal_O2_V102     #Volumen de oxígeno almacenado (actual) en el tanque V-101 [NL]
      StorageH2_V102Volume = Biogas_plant_DT.V_normal_H2_V102     #Volumen de hidrógeno almacenado (actual) en el tanque V-101 [NL]

      # Visualización por concentraciones en el gemelo digital
      StorageCH4_V102Concentration = Biogas_plant_DT.AT104A1v.iloc[-1]   #Concentración de metano almacenado (actual) en el tanque V-101 [%]
      StorageCO2_V102Concentration = Biogas_plant_DT.AT104A2v.iloc[-1]   #Concentración de dióxido de carbono almacenado (actual) en el tanque V-101 [%]
      StorageH2S_V102Concentration = Biogas_plant_DT.AT104A3v.iloc[-1]   #Concentración de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [%]
      StorageO2_V102Concentration = Biogas_plant_DT.AT104A4v.iloc[-1]    #Concentración de oxígeno almacenado (actual) en el tanque V-101 [%]
      StorageH2_V102Concentration = Biogas_plant_DT.AT104A5v.iloc[-1]    #Concentración de hidrógeno almacenado (actual) en el tanque V-101 [%]

      # Visualización por moles en el gemelo digital
      StorageCH4_V102moles = Biogas_plant_DT.mol_CH4_V102               #moles de metano almacenado (actual) en el tanque V-101 [%]
      StorageCO2_V102moles = Biogas_plant_DT.mol_CO2_V102               #moles de dióxido de carbono almacenado (actual) en el tanque V-101 [%]
      StorageH2S_V102moles = Biogas_plant_DT.mol_H2S_V102               #moles de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [%]
      StorageO2_V102moles = Biogas_plant_DT.mol_O2_V102                 #moles de oxígeno almacenado (actual) en el tanque V-101 [%]
      StorageH2_V102moles = Biogas_plant_DT.mol_H2_V102                 #moles de hidrógeno almacenado (actual) en el tanque V-101 [%]

      #Humedad del biogás en humedad relativa
      Relative_humidity_V102 = Biogas_plant_DT.AT104Bv.iloc[-1]          #[%]

      #Humedad del biogás en moles
      moles_humidity_V102 = Biogas_plant_DT.mol_H2O_V102                 #[mol]

      """
      #En el tanque de biogas V-107

      # En la interfaz ¿Es posible poner selectores para visualizar diferentes parámetros del biogás?
      # Selector 1: Para el tanque: Seleccionar: [acumulado, almacenado]
      # Selector 2: Para las variables de total biogas: [Presión, volumen normal]
      # Selector 3: Para los compuestos del biogas: [Concentración, Volumen_parcial_normal, moles]
      # Selector 4: Para la humedad del biogás: [Humedad relativa, moles]
      """
      #Biogas almacenado por volumen
      StorageBiogasVolumeV107 = Biogas_plant_DT.V_normal_V107     #Volumen de biogás almacenado (actual) en el tanque V-101 [NL]

      #Biogás acumulado por volumen
      AcumBiogasVolumenV107 = Biogas_plant_DT.Vnormal_acum_v107   #Volumen de biogás total producido por la planta (acumulado) en el tanque V-101 [NL] 

      #Biogás almacenado en variable presión
      StorageBiogasPressureV107 = Biogas_plant_DT.PT105v.iloc[-1]  #Presión de biogás almacenado (actual) en el tanque V-101 [kPa]

      #Biogás acumulado por presión
      AcumBiogasPressureV107 = Biogas_plant_DT.Pacum_v107         #Presión de biogás total producida en el tanque V-101 [kPa]

      #compuestos del biogás
      # Visualización de volumen parcial en el gemelo digital
      StorageCH4_V107Volume = Biogas_plant_DT.V_normal_CH4_V107   #Volumen de metano almacenado (actual) en el tanque V-101 [NL]
      StorageCO2_V107Volume = Biogas_plant_DT.V_normal_CO2_V107   #Volumen de dióxido de carbono almacenado (actual) en el tanque V-101 [NL]
      StorageH2S_V107Volume = Biogas_plant_DT.V_normal_H2S_V107   #Volumen de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [NL]
      StorageO2_V107Volume = Biogas_plant_DT.V_normal_O2_V107     #Volumen de oxígeno almacenado (actual) en el tanque V-101 [NL]
      StorageH2_V107Volume = Biogas_plant_DT.V_normal_H2_V107     #Volumen de hidrógeno almacenado (actual) en el tanque V-101 [NL]

      # Visualización por concentraciones en el gemelo digital
      StorageCH4_V107Concentration = Biogas_plant_DT.AT105A1v.iloc[-1]   #Concentración de metano almacenado (actual) en el tanque V-101 [%]
      StorageCO2_V107Concentration = Biogas_plant_DT.AT105A2v.iloc[-1]   #Concentración de dióxido de carbono almacenado (actual) en el tanque V-101 [%]
      StorageH2S_V107Concentration = Biogas_plant_DT.AT105A3v.iloc[-1]   #Concentración de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [%]
      StorageO2_V107Concentration = Biogas_plant_DT.AT105A4v.iloc[-1]    #Concentración de oxígeno almacenado (actual) en el tanque V-101 [%]
      StorageH2_V107Concentration = Biogas_plant_DT.AT105A5v.iloc[-1]    #Concentración de hidrógeno almacenado (actual) en el tanque V-101 [%]

      # Visualización por moles en el gemelo digital
      StorageCH4_V107moles = Biogas_plant_DT.mol_CH4_V107               #moles de metano almacenado (actual) en el tanque V-101 [%]
      StorageCO2_V107moles = Biogas_plant_DT.mol_CO2_V107               #moles de dióxido de carbono almacenado (actual) en el tanque V-101 [%]
      StorageH2S_V107moles = Biogas_plant_DT.mol_H2S_V107               #moles de sulfuro de hidrógeno almacenado (actual) en el tanque V-101 [%]
      StorageO2_V107moles = Biogas_plant_DT.mol_O2_V107                 #moles de oxígeno almacenado (actual) en el tanque V-101 [%]
      StorageH2_V107moles = Biogas_plant_DT.mol_H2_V107                 #moles de hidrógeno almacenado (actual) en el tanque V-101 [%]

      #Humedad del biogás en humedad relativa
      Relative_humidity_V107 = Biogas_plant_DT.AT105Bv.iloc[-1]          #[%]

      #Humedad del biogás en moles
      moles_humidity_V107 = Biogas_plant_DT.mol_H2O_V107                 #[mol]

    
    
    print(biogas_input)
    print(biogas_output)

    return {}, 200