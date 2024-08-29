from flask import request
from flask_restful import Resource
import pandas as pd
from utils import Biogas_Start
from utils import MachineLearning_biogas_start
from utils import Biogas_Simulation_Start

class Biogas(Resource):
  def post(self):
    data = request.get_json()
     
    biogas_input = {}
    biogas_output = {}

    biogas_input["reset"] = data["restartFlag"]

    if biogas_input["reset"] == True:                  
      Biogas_Start.BiogasStart.reset_instance()
      MachineLearning_biogas_start.MachineLearningStart.reset_instance()
      Biogas_Simulation_Start.BiogasSimulationStart.reset_instance()
    
    #Operación Planta
    biogas_input["VR1"] = data["anaerobicReactorVolume1"]["value"]
    biogas_input["VR2"] = data["anaerobicReactorVolume2"]["value"]
    biogas_input["OperationMode"] = data["inputOperationMode"]

    #Tanques de biogás
    biogas_input["VG1"] = data["biogasTankVolume1"]["value"]
    biogas_input["VG2"] = data["biogasTankVolume2"]["value"]
    biogas_input["VG3"] = data["biogasTankVolume3"]["value"]

    #Parámetros del gemelo
    biogas_input["DigitalTwin"] = data["digitalTwinState"]
    biogas_input["tp"] = data["digitalTwinStepTime"]["value"]
    biogas_input["t_pred"] = data["digitalTwinForecastTime"]["value"]

    #Parámetros cinéticos
    biogas_input["OperationModel"] = data["operationModelType"]
    biogas_input["A_R101"] = data["exponentialFactorR101"]["value"]
    biogas_input["B_R101"] = data["activationEnergyR101"]["value"]
    biogas_input["C_R101"] = data["lambdaR101"]["value"]
    biogas_input["A_R102"] = data["exponentialFactorR102"]["value"]
    biogas_input["B_R102"] = data["activationEnergyR102"]["value"]
    biogas_input["C_R102"] = data["lambdaR102"]["value"]

    #Tratamiento biogas
    biogas_input["Dab_1"] = data["difussionCoefficientTower1"]["value"]
    biogas_input["W1"] =  data["adsorbentWeightTower1"]["value"]
    biogas_input["L1"] = data["lengthTower1"]["value"]
    biogas_input["Dab_2"] = data["difussionCoefficientTower2"]["value"]
    biogas_input["W2"] =  data["adsorbentWeightTower2"]["value"]
    biogas_input["L2"] = data["lengthTower2"]["value"]
    biogas_input["Dab_3"] = data["difussionCoefficientTower3"]["value"]
    biogas_input["W3"] =  data["adsorbentWeightTower3"]["value"]
    biogas_input["L3"] = data["lengthTower3"]["value"]

    #Condiciones iniciales de los reactores
    biogas_input["ST_R101"] = data["initialAnalysisConditionsR101"]["totalSubstrateSolids"]["value"]
    biogas_input["SV_R101"] = data["initialAnalysisConditionsR101"]["volatileSubstrateSolids"]["value"]
    biogas_input["rho_R101"] = data["initialAnalysisConditionsR101"]["substrateDensity"]["value"]
    biogas_input["Cc_R101"] = data["initialAnalysisConditionsR101"]["atomicCarbonSubstrateConcetration"]["value"]
    biogas_input["Ch_R101"] = data["initialAnalysisConditionsR101"]["atomicHydrogenSubstrateConcetration"]["value"]
    biogas_input["Co_R101"] = data["initialAnalysisConditionsR101"]["atomicOxygenSubstrateConcetration"]["value"]
    biogas_input["Cn_R101"] = data["initialAnalysisConditionsR101"]["atomicNitrogenSubstrateConcetration"]["value"]
    biogas_input["Cs_R101"] = data["initialAnalysisConditionsR101"]["atomicSulfurSubstrateConcetration"]["value"]

    biogas_input["ST_R102"] = data["initialAnalysisConditionsR102"]["totalSubstrateSolids"]["value"]
    biogas_input["SV_R102"] = data["initialAnalysisConditionsR102"]["volatileSubstrateSolids"]["value"]
    biogas_input["rho_R102"] = data["initialAnalysisConditionsR102"]["substrateDensity"]["value"]
    biogas_input["Cc_R102"] = data["initialAnalysisConditionsR102"]["atomicCarbonSubstrateConcetration"]["value"]
    biogas_input["Ch_R102"] = data["initialAnalysisConditionsR102"]["atomicHydrogenSubstrateConcetration"]["value"]
    biogas_input["Co_R102"] = data["initialAnalysisConditionsR102"]["atomicOxygenSubstrateConcetration"]["value"]
    biogas_input["Cn_R102"] = data["initialAnalysisConditionsR102"]["atomicNitrogenSubstrateConcetration"]["value"]
    biogas_input["Cs_R102"] = data["initialAnalysisConditionsR102"]["atomicSulfurSubstrateConcetration"]["value"]


    # Variables de operación
    ##Condiciones del sustrato - Tanque de premezcla
    biogas_input["manual_substrate"] = data["inputSubstrateConditions"]
    biogas_input["Cc"] = data["inputElementalAnalysisCarbonContent"]["value"]
    biogas_input["Ch"] = data["inputElementalAnalysisHydrogenContent"]["value"]
    biogas_input["Co"] = data["inputElementalAnalysisOxygenContent"]["value"]  
    biogas_input["Cn"] = data["inputElementalAnalysisNitrogenContent"]["value"]
    biogas_input["Cs"] = data["inputElementalAnalysisSulfurContent"]["value"]
    biogas_input["ST"] = data["inputProximateAnalysisTotalSolids"]["value"]
    biogas_input["SV"] = data["inputProximateAnalysisVolatileSolids"]["value"]
    biogas_input["rho"] = data["inputProximateAnalysisDensity"]["value"]

    ##Condiciones de la bomba P-104
    biogas_input["manual_P104"] = data["inputPump104"]
    biogas_input["TRH"] = data["inputPump104HydraulicRetentionTime"]["value"]
    biogas_input["TTO_P104"] = data["inputPump104StartTime"]["value"]
    biogas_input["FT_P104"] = data["inputPump104StartsPerDay"]["value"]

    #condiciones de la bomba P-101
    biogas_input["manual_P101"] = data["inputPump101"]
    biogas_input["Q_P101"] = data["inputPump101Flow"]["value"]
    biogas_input["TTO_P101"] = data["inputPump101StartTime"]["value"]
    biogas_input["FT_P101"] = data["inputPump101StartsPerDay"]["value"]

    #condiciones de la bomba P-102
    biogas_input["manual_P102"] = data["inputPump102"]
    biogas_input["Q_P102"] = data["inputPump102Flow"]["value"]
    biogas_input["TTO_P102"] = data["inputPump102StartTime"]["value"]
    biogas_input["FT_P102"] = data["inputPump102StartsPerDay"]["value"]

    #Condiciones TK100 premezcla
    biogas_input["manual_mixing_TK100"] = data["inputMixTK100"]
    biogas_input["FT_mixing_TK100"] = data["inputStartsPerDayMixTK100"]["value"]
    biogas_input["TTO_mixing_TK100"] = data["inputStartTimeMixTK100"]["value"]
    biogas_input["RPM_TK100"] = data["inputSpeedMixTK100"]["value"]

    #condiciones del reactor R101
    ## Agitación R101
    biogas_input["manual_mixing_R101"] = data["inputMixR101"]
    biogas_input["FT_mixing_R101"] = data["inputStartsPerDayMixR101"]["value"]
    biogas_input["TTO_mixing_R101"] = data["inputStartTimeMixR101"]["value"]
    biogas_input["RPM_R101"] = data["inputSpeedMixR101"]["value"]
    ## Temperatura R101
    biogas_input["manual_Temperature_R101"] = data["inputTemperatureR101"]['disabled']
    biogas_input["Temperature_R101"] = data["inputTemperatureR101"]['value']
    ## pH R101
    biogas_input["manual_pH_R101"] = data["inputPHR101"]['disabled']
    biogas_input["pH_R101"] = data["inputPHR101"]['value']

    #condiciones del reactor R102
    ## Agitación R102
    biogas_input["manual_mixing_R102"] = data["inputMixR102"]
    biogas_input["FT_mixing_R102"] = data["inputStartsPerDayMixR102"]["value"]
    biogas_input["TTO_mixing_R102"] = data["inputStartTimeMixR102"]["value"]
    biogas_input["RPM_R102"] = data["inputSpeedMixR102"]["value"]
    ## Temperatura R102
    biogas_input["manual_Temperature_R102"] = data["inputTemperatureR102"]['disabled']
    biogas_input["Temperature_R102"] = data["inputTemperatureR102"]['value']
    ## pH R102
    biogas_input["manual_pH_R102"] = data["inputPHR102"]['disabled']
    biogas_input["pH_R102"] = data["inputPHR102"]['value']

    #Condiciones de la torre de adsorción 1
    biogas_input["D1"] = data["difussionCoefficientTower1"]["value"]
    biogas_input["W1"] = data["adsorbentWeightTower1"]["value"]
    biogas_input["L1"] = data["lengthTower1"]["value"]

    #Condiciones de la torre de adsorción 2
    biogas_input["D2"] = data["difussionCoefficientTower2"]["value"]
    biogas_input["W2"] = data["adsorbentWeightTower2"]["value"]
    biogas_input["L2"] = data["lengthTower2"]["value"]

     #Condiciones de la torre de adsorción 3
    biogas_input["D3"] = data["difussionCoefficientTower3"]["value"]
    biogas_input["W3"] = data["adsorbentWeightTower3"]["value"]
    biogas_input["L3"] = data["lengthTower3"]["value"]

    if biogas_input["DigitalTwin"] == True: # Modo Gemelo On

      Biogas_Plant_ini = Biogas_Start.BiogasStart()
      Biogas_Plant_ini.starting(VR1 = biogas_input["VR1"], VR2 = biogas_input["VR2"], VG1 = biogas_input["VG1"], VG2 = biogas_input["VG2"],
                                VG3 = biogas_input["VG3"], tp = biogas_input["tp"], ST_R101 = biogas_input["ST_R101"], SV_R101 = biogas_input["SV_R101"],
                                Cc_R101 = biogas_input["Cc_R101"], Ch_R101 = biogas_input["Ch_R101"], Co_R101 = biogas_input["Co_R101"],
                                Cn_R101 = biogas_input["Cn_R101"], Cs_R101 = biogas_input["Cs_R101"], rho_R101 = biogas_input["rho_R101"],
                                ST_R102 = biogas_input["ST_R102"], SV_R102 = biogas_input["SV_R102"], Cc_R102 = biogas_input["Cc_R102"] ,
                                Ch_R102 = biogas_input["Ch_R102"], Co_R102 = biogas_input["Co_R102"], Cn_R102 = biogas_input["Cn_R102"],
                                Cs_R102 = biogas_input["Cs_R102"], rho_R102 = biogas_input["rho_R102"], OperationMode = biogas_input["OperationMode"])
    
      Biogas_Plant = Biogas_Plant_ini.data
      Biogas_Plant.GetValuesFromBiogasPlant()
      Biogas_Plant.Substrate_conditions(manual_substrate = biogas_input["manual_substrate"],Cc = biogas_input["Cc"], Ch = biogas_input["Ch"], Co =  biogas_input["Co"],
                                        Cn = biogas_input["Cn"], Cs = biogas_input["Cs"], rho = biogas_input["rho"], ST = biogas_input["ST"], SV = biogas_input["SV"])
      Biogas_Plant.pHR101(manual_pH_R101 = biogas_input["manual_pH_R101"], pH = biogas_input["pH_R101"])
      Biogas_Plant.pHR102(manual_pH_R102 = biogas_input["pH_R102"], pH = biogas_input["pH_R102"])
      Biogas_Plant.Pump104(manual_P104 = biogas_input["manual_P104"], TRH = biogas_input["TRH"], FT_P104 = biogas_input["FT_P104"], TTO_P104 = biogas_input["TTO_P104"])
      Biogas_Plant.Pump101(manual_P101 = biogas_input["manual_P101"], FT_P101 = biogas_input["FT_P101"], TTO_P101 = biogas_input["TTO_P101"], Q_P101 = biogas_input["Q_P101"])
      Biogas_Plant.Pump102(manual_P102 = biogas_input["manual_P102"], FT_P102 = biogas_input["FT_P102"], TTO_P102 = biogas_input["TTO_P102"], Q_P102 = biogas_input["Q_P102"])
      Biogas_Plant.Mixing_TK100(manual_mixing = biogas_input["manual_mixing_TK100"], FT_mixing_TK100 = biogas_input["FT_mixing_TK100"], TTO_mixing_TK100 = biogas_input["TTO_mixing_TK100"],
                                 RPM_TK100 = biogas_input["RPM_TK100"])
      Biogas_Plant.Mixing_R101(manual_mixing = biogas_input["manual_mixing_R101"], FT_mixing_R101 = biogas_input["FT_mixing_R101"], TTO_mixing_R101 = biogas_input["TTO_mixing_R101"],
                                 RPM_R101 = biogas_input["RPM_R101"])
      Biogas_Plant.Mixing_R102(manual_mixing = biogas_input["manual_mixing_R102"], FT_mixing_R102 = biogas_input["FT_mixing_R102"], TTO_mixing_R102 = biogas_input["TTO_mixing_R102"],
                                 RPM_R102 = biogas_input["RPM_R102"])
      Biogas_Plant.Temperature_R101(manual_temp_R101 = biogas_input["manual_Temperature_R101"], Temp_R101 = biogas_input["Temperature_R101"])
      Biogas_Plant.Temperature_R102(manual_temp_R102 = biogas_input["manual_Temperature_R102"], Temp_R102 = biogas_input["Temperature_R102"])
      Biogas_Plant.V_101_DT()
      Biogas_Plant.V_102_DT()
      Biogas_Plant.V_107_DT()
      Biogas_Plant.R101_DT()
      Biogas_Plant.R102_DT()
      Biogas_Plant.Energy_Biogas()
      Biogas_Plant.StorageData()
      
      Biogas_learning_ini = MachineLearning_biogas_start.MachineLearningStart()
      Biogas_learning_ini.starting(t_train= biogas_input["t_pred"]*2, OperationMode = biogas_input["OperationMode"], Model = biogas_input["OperationModel"], A_R101 = biogas_input["A_R101"], 
                                   B_R101 = biogas_input["B_R101"], C_R101=biogas_input["C_R101"], A_R102=biogas_input["A_R102"], B_R102=biogas_input["B_R102"], 
                                   C_R102=biogas_input["C_R102"], VR1 = biogas_input["VR1"], VR2 = biogas_input["VR1"])
      Biogas_learning = Biogas_learning_ini.data
      Biogas_learning.Get_data_DT(DataBase = Biogas_Plant.DT_Data)
      Biogas_learning.DT_time_and_data()
      Biogas_learning.Optimization()
      Biogas_learning.StorageData()

      #sustrato
      biogas_output["n"] = Biogas_Plant.n
      biogas_output["a"] = Biogas_Plant.a
      biogas_output["b"] = Biogas_Plant.b
      biogas_output["c"] = Biogas_Plant.c
      biogas_output["d"] = Biogas_Plant.d

      #Tanque de premezcla
      biogas_output["Mix_Velocity_TK100"] = Biogas_Plant.RPM_TK100
      biogas_output["C_sv"] = Biogas_Plant.Csv
      biogas_output["SV"] = Biogas_Plant.SV
      biogas_output["C_st"] = Biogas_Plant.Cst
      biogas_output["ST"] = Biogas_Plant.ST

      #bomba P104
      biogas_output["Pump104Flow"] = Biogas_Plant.Q_P104

      #Reactor R101
      biogas_output["Mix_Velocity_R101"] = Biogas_Plant.RPM_R101
      biogas_output["C_sv_R101"] = Biogas_Plant.SV_R101_gL
      biogas_output["SV_R101"] = Biogas_Plant.SV_R101
      biogas_output["C_st_R101"] = Biogas_Plant.ST_R101_gl
      biogas_output["ST_R101"] = Biogas_Plant.ST_R101
      biogas_output["Organic_Charge_R101"] = Biogas_Plant.organic_charge_R101
      biogas_output["pH_R101"] = Biogas_Plant.pH_R101
      biogas_output["Temp_R101"] = Biogas_Plant.Temp_R101
      biogas_output["x_R101"] = Biogas_Plant.X_R101
      #modelo cinético
      if biogas_input["OperationModel"] == "Arrhenius":
        biogas_output["K_R101"] = Biogas_learning.K_R101
        biogas_output["Ea_R101"] = Biogas_learning.Ea_R101


      

    else:  #Modo Gemelo Off

      Biogas_Plant_ini = Biogas_Simulation_Start.BiogasSimulationStart()
      Biogas_Plant_ini.starting(VR1 = biogas_input["VR1"], VR2 = biogas_input["VR2"], VG1 = biogas_input["VG1"], VG2 = biogas_input["VG2"], VG3 = biogas_input["VG3"],
                                tp = biogas_input["tp"], ST_R101 = biogas_input["ST_R101"], SV_R101 = biogas_input["SV_R101"], Cc_R101 = biogas_input["Cc_R101"],
                                Ch_R101 = biogas_input["Ch_R101"], Co_R101 = biogas_input["Co_R101"], Cn_R101 = biogas_input["Cn_R101"], Cs_R101 = biogas_input["Cs_R101"], 
                                rho_R101 = biogas_input["rho_R101"], ST_R102 = biogas_input["ST_R102"], SV_R102 = biogas_input["SV_R102"], Cc_R102 = biogas_input["Cc_R102"], 
                                Ch_R102 = biogas_input["Ch_R102"], Co_R102 = biogas_input["Co_R102"], Cn_R102 = biogas_input["Cn_R102"], Cs_R102 = biogas_input["Cs_R102"], 
                                rho_R102 = biogas_input["rho_R102"] , OperationMode = biogas_input["OperationMode"])
      Biogas_Plant = Biogas_Plant_ini.data
      Biogas_Plant.Substrate_conditions(Cc = biogas_input["Cc"], Ch = biogas_input["Ch"], Co = biogas_input["Co"], Cn = biogas_input["Cn"], Cs = biogas_input["Cs"],
                                        rho = biogas_input["rho"], ST = biogas_input["ST"], SV = biogas_input["SV"])
      
      Biogas_Plant.Pump104(TRH=biogas_input["TRH"], FT_P104=biogas_input["FT_P104"], TTO_P104=biogas_input["TTO_P104"])
      Biogas_Plant.Pump101(FT_P101=biogas_input["FT_P101"], TTO_P101=biogas_input["TTO_P101"], Q_P101=biogas_input["Q_P101"])
      Biogas_Plant.Pump102(FT_P102=biogas_input["FT_P102"], TTO_P102=biogas_input["TTO_P102"], Q_P102=biogas_input["Q_P102"])
      Biogas_Plant.Mixing_TK100(FT_mixin_TK100 = biogas_input["FT_mixing_TK100"], TTO_mixing_TK100 = biogas_input["TTO_mixing_TK100"], RPM_TK100 = biogas_input["RPM_TK100"])
      Biogas_Plant.Mixing_R101(FT_mixin_R101 = biogas_input["FT_mixing_R101"], TTO_mixing_R101 = biogas_input["TTO_mixing_R101"], RPM_R101 = biogas_input["RPM_R101"])
      Biogas_Plant.Mixing_R102(FT_mixin_R102 = biogas_input["FT_mixing_R102"], TTO_mixing_R102=biogas_input["TTO_mixing_R102"], RPM_R102=biogas_input["RPM_R102"])
      Biogas_Plant.Data_simulation(Temperature_R101 = biogas_input["Temperature_R101"], Temperature_R102 = biogas_input["Temperature_R102"], pH_R101 = biogas_input["pH_R101"], pH_R102 = biogas_input["pH_R102"])
      Biogas_Plant.ReactorSimulation(Model = biogas_input["OperationModel"], A_R101 = biogas_input["A_R101"], B_R101 = biogas_input["B_R101"], C_R101 = biogas_input["C_R101"], 
                                     A_R102 = biogas_input["A_R102"], B_R102 = biogas_input["B_R102"], C_R102 = biogas_input["C_R102"])
      Biogas_Plant.V101()
      Biogas_Plant.V102()
      Biogas_Plant.Biogas_treatment(D1 = biogas_input["D1"], W1 = biogas_input["W1"], L1 = biogas_input["L1"], 
                                    D2 = biogas_input["D2"], W2 = biogas_input["W2"], L2 = biogas_input["L2"],
                                    D3 = biogas_input["D3"], W3 = biogas_input["W3"], L3 = biogas_input["L3"])
      Biogas_Plant.V107()

      #Resultados del análisis elemental
      biogas_output["n"] = Biogas_Plant.n
      biogas_output["a"] = Biogas_Plant.a
      biogas_output["b"] = Biogas_Plant.b
      biogas_output["c"] = Biogas_Plant.c
      biogas_output["d"] = Biogas_Plant.d

      #Condiciones de premezcla o predigestión
      biogas_output["Mix_Velocity_TK100"] = Biogas_Plant.RPM_TK100
      biogas_output["C_sv"] = Biogas_Plant.Csv
      biogas_output["SV"] = Biogas_Plant.SV
      biogas_output["C_st"] = Biogas_Plant.Cst
      biogas_output["ST"] = Biogas_Plant.ST

      #Salida de la bomba P_104
      biogas_output["Pump104Flow"] = Biogas_Plant.Q_P104

      #Reactor R101
      biogas_output["Mix_Velocity_R101"] = Biogas_Plant.RPM_R101
      biogas_output["C_sv_R101"] = Biogas_Plant.SV_R101_gL/100
      biogas_output["SV_R101"] = Biogas_Plant.SV_R101_p
      biogas_output["C_st_R101"] = Biogas_Plant.ST_R101/100*Biogas_Plant.rho
      biogas_output["ST_R101"] = Biogas_Plant.ST_R101
      biogas_output["Organic_Charge_R101"] = float(Biogas_Plant.Organic_charge_R101)  #Revisar con eusse
      biogas_output["pH_R101"] = Biogas_Plant.pH_R101
      biogas_output["Temp_R101"] = Biogas_Plant.Temp_R101
      biogas_output["x_R101"] = Biogas_Plant.x_R101 *100
      
      if biogas_input["OperationModel"] == "Arrhenius":  # revisar con eusse
        biogas_output["K_R101"] = Biogas_Plant.K_R101
        biogas_output["Ea_R101"] = Biogas_Plant.Ea_R101
      elif biogas_input["OperationModel"] == "ADM1": 
        biogas_output["K_R101"] = Biogas_Plant.K_R101
      elif biogas_input["OperationModel"] == "Gompertz":
        biogas_output["K_R101"] = Biogas_Plant.ym_R101
        biogas_output["Ea_R101"] = Biogas_Plant.U_R101
        biogas_output["Lambda_R101"] = Biogas_Plant.L_R101
      
      #Condiciones de modos de operación
      if biogas_input["OperationMode"] == "Modo3":
        
        #BombaP101
        biogas_output["Pump101Flow"] = Biogas_Plant.Q_P101

        #Reactor R102
        biogas_output["Mix_Velocity_R102"] = Biogas_Plant.RPM_R102
        biogas_output["pH_R102"] = Biogas_Plant.pH_R102
        biogas_output["Temp_R102"] = Biogas_Plant.Temp_R102
        biogas_output["C_sv_R102"] = Biogas_Plant.SV_R102_gL/100
        biogas_output["SV_R102"] = Biogas_Plant.ST_R102
        biogas_output["C-st_R102"] = Biogas_Plant.ST_R102/100 * Biogas_Plant.rho
        biogas_output["ST_R102"] = Biogas_Plant.ST_R102
        biogas_output["Organic_Charge_R102"] = float(Biogas_Plant.Organic_charge_R102)
        biogas_output["x_R102"] = Biogas_Plant.X_R102 *100

        if biogas_input["OperationModel"] == "Arrhenius":  # revisar con eusse
          biogas_output["K_R102"] = Biogas_Plant.K_R102
          biogas_output["Ea_R102"] = Biogas_Plant.Ea_R102
        elif biogas_input["OperationModel"] == "ADM1": 
          biogas_output["K_R102"] = Biogas_Plant.K_R102
        elif biogas_input["OperationModel"] == "Gompertz":
          biogas_output["K_R102"] = Biogas_Plant.ym_R102
          biogas_output["Ea_R102"] = Biogas_Plant.U_R102
          biogas_output["Lambda_R102"] = Biogas_Plant.L_R102
        
      elif biogas_input["OperationMode"] in ["Modo4", "Modo5"]:
        #BombaP101
        biogas_output["Pump101Flow"] = Biogas_Plant.Q_P101
        #BombaP102
        biogas_output["Pump102Flow"] = Biogas_Plant.Q_P102

        #Reactor R102
        biogas_output["Mix_Velocity_R102"] = Biogas_Plant.RPM_R102
        biogas_output["pH_R102"] = Biogas_Plant.pH_R102
        biogas_output["Temp_R102"] = Biogas_Plant.Temp_R102
        biogas_output["C_sv_R102"] = Biogas_Plant.SV_R102_gL/100
        biogas_output["SV_R102"] = Biogas_Plant.ST_R102
        biogas_output["C_st_R102"] = Biogas_Plant.ST_R102/100 * Biogas_Plant.rho
        biogas_output["ST_R102"] = Biogas_Plant.ST_R102
        biogas_output["Organic_Charge_R102"] = float(Biogas_Plant.Organic_charge_R102)
        biogas_output["x_R102"] = Biogas_Plant.x_R102 * 100

        if biogas_input["OperationModel"] == "Arrhenius":  # revisar con eusse
          biogas_output["K_R102"] = Biogas_Plant.K_R102
          biogas_output["Ea_R102"] = Biogas_Plant.Ea_R102
        elif biogas_input["OperationModel"] == "ADM1": 
          biogas_output["K_R102"] = Biogas_Plant.K_R102
        elif biogas_input["OperationModel"] == "Gompertz":
          biogas_output["K_R102"] = Biogas_Plant.ym_R102
          biogas_output["Ea_R102"] = Biogas_Plant.U_R102
          biogas_output["Lambda_R102"] = Biogas_Plant.L_R102
        
      #V101
      biogas_output["AcumBiogasVolumenV101"] = Biogas_Plant.Vnormal_bio_acum_V101
      biogas_output["StorageBiogasVolumeV101"] = Biogas_Plant.Vnormal_bio_V101
      biogas_output["AcumBiogasPressureV101"] = Biogas_Plant.Pacum_bio_V101
      biogas_output["StorageBiogasPressureV101"] = Biogas_Plant.Pstorage_bio_V101

      ## Metano
      biogas_output["StorageCH4_V101Volume"] = Biogas_Plant.Vnormal_CH4_V101
      biogas_output["StorageCH4_V101Concentration"] = Biogas_Plant.x_CH4_V101*100
      biogas_output["StorageCH4_V101moles"] = Biogas_Plant.mol_CH4_V101

      ## Dióxido de carbono
      biogas_output["StorageCO2_V101Volume"] = Biogas_Plant.Vnormal_CO2_V101
      biogas_output["StorageCO2_V101Concentration"] = Biogas_Plant.x_CO2_V101*100
      biogas_output["StorageCO2_V101moles"] = Biogas_Plant.mol_CO2_V101

      ## Sulfuro de de hidrógeno
      biogas_output["StorageH2S_V101Volume"] = Biogas_Plant.Vnormal_H2S_V101
      biogas_output["StorageH2S_V101Concentration"] = Biogas_Plant.x_H2S_V101*1000000
      biogas_output["StorageH2S_V101moles"] = Biogas_Plant.mol_H2S_V101

      ## Oxígeno
      biogas_output["StorageO2_V101Volume"] = Biogas_Plant.Vnormal_O2_V101
      biogas_output["StorageO2_V101Concentration"] = Biogas_Plant.x_O2_V101*100
      biogas_output["StorageO2_V101moles"] = Biogas_Plant.mol_O2_V101

      ## Amonio
      biogas_output["StorageNH3_V101Volume"] = Biogas_Plant.Vnormal_NH3_V101
      biogas_output["StorageNH3_V101Concentration"] = Biogas_Plant.x_NH3_V101*1000000
      biogas_output["StorageNH3_V101moles"] = Biogas_Plant.mol_NH3_V101

      ## Hidrógeno
      biogas_output["StorageH2_V101Volume"] = Biogas_Plant.Vnormal_H2_V101
      biogas_output["StorageH2_V101Concentration"] = Biogas_Plant.x_H2_V101*1000000
      biogas_output["StorageH2_V101moles"] = Biogas_Plant.mol_H2_V101

      #Agua
      biogas_output["moles_humidity_V101"] = Biogas_Plant.mol_H2O_V101
      biogas_output["Relative_humidity_V101"] = Biogas_Plant.RH_V101

      #Energía
      biogas_output["StorageEnergy_V101"] = Biogas_Plant.Energy_V101/3600

      #V102
      biogas_output["AcumBiogasVolumenV102"] = Biogas_Plant.Vnormal_bio_acum_V102
      biogas_output["StorageBiogasVolumeV102"] = Biogas_Plant.Vnormal_bio_V102
      biogas_output["AcumBiogasPressureV102"] = Biogas_Plant.Pacum_bio_V102
      biogas_output["StorageBiogasPressureV102"] = Biogas_Plant.Pstorage_bio_V102

      ## Metano
      biogas_output["StorageCH4_V102Volume"] = Biogas_Plant.Vnormal_CH4_V102
      biogas_output["StorageCH4_V102Concentration"] = Biogas_Plant.x_CH4_V102*100
      biogas_output["StorageCH4_V102moles"] = Biogas_Plant.mol_CH4_V102

      ## Dióxido de carbono
      biogas_output["StorageCO2_V102Volume"] = Biogas_Plant.Vnormal_CO2_V102
      biogas_output["StorageCO2_V102Concentration"] = Biogas_Plant.x_CO2_V102*100
      biogas_output["StorageCO2_V102moles"] = Biogas_Plant.mol_CO2_V102

      ## Sulfuro de de hidrógeno
      biogas_output["StorageH2S_V102Volume"] = Biogas_Plant.Vnormal_H2S_V102
      biogas_output["StorageH2S_V102Concentration"] = Biogas_Plant.x_H2S_V102*1000000
      biogas_output["StorageH2S_V102moles"] = Biogas_Plant.mol_H2S_V102

      ## Oxígeno
      biogas_output["StorageO2_V102Volume"] = Biogas_Plant.Vnormal_O2_V102
      biogas_output["StorageO2_V102Concentration"] = Biogas_Plant.x_O2_V102*100
      biogas_output["StorageO2_V102moles"] = Biogas_Plant.mol_O2_V102

      ## Amonio
      biogas_output["StorageNH3_V102Volume"] = Biogas_Plant.Vnormal_NH3_V102
      biogas_output["StorageNH3_V102Concentration"] = Biogas_Plant.x_NH3_V102*1000000
      biogas_output["StorageNH3_V102moles"] = Biogas_Plant.mol_NH3_V102

      ## Hidrógeno
      biogas_output["StorageH2_V102Volume"] = Biogas_Plant.Vnormal_H2_V102
      biogas_output["StorageH2_V102Concentration"] = Biogas_Plant.x_H2_V102*1000000
      biogas_output["StorageH2_V102moles"] = Biogas_Plant.mol_H2_V102

      #Agua
      biogas_output["moles_humidity_V102"] = Biogas_Plant.mol_H2O_V102
      biogas_output["Relative_humidity_V102"] = Biogas_Plant.RH_V102

      #Energía
      biogas_output["StorageEnergy_V102"] = Biogas_Plant.Energy_V102/3600

      #Biogas Treatment
      biogas_output["ads_NH3_bt"] = Biogas_Plant.mol_NH3_ads
      biogas_output["ads_H2S_bt"] = Biogas_Plant.mol_H2S_ads
      biogas_output["ads_H2O_bt"] = Biogas_Plant.mol_H2O_ads
      biogas_output["x_bt"] = Biogas_Plant.x_tower*100

      #V107
      biogas_output["AcumBiogasVolumenV107"] = Biogas_Plant.Vnormal_bio_acum_V107
      biogas_output["StorageBiogasVolumeV107"] = Biogas_Plant.Vnormal_bio_V107
      biogas_output["AcumBiogasPressureV107"] = Biogas_Plant.Pacum_bio_V107
      biogas_output["StorageBiogasPressureV107"] = Biogas_Plant.Pstorage_bio_V107

      ## Metano
      biogas_output["StorageCH4_V107Volume"] = Biogas_Plant.Vnormal_CH4_V107
      biogas_output["StorageCH4_V107Concentration"] = Biogas_Plant.x_CH4_V107*100
      biogas_output["StorageCH4_V107moles"] = Biogas_Plant.mol_CH4_V107

      ## Dióxido de carbono
      biogas_output["StorageCO2_V107Volume"] = Biogas_Plant.Vnormal_CO2_V107
      biogas_output["StorageCO2_V107Concentration"] = Biogas_Plant.x_CO2_V107*100
      biogas_output["StorageCO2_V107moles"] = Biogas_Plant.mol_CO2_V107

      ## Sulfuro de de hidrógeno
      biogas_output["StorageH2S_V107Volume"] = Biogas_Plant.Vnormal_H2S_V107
      biogas_output["StorageH2S_V107Concentration"] = Biogas_Plant.x_H2S_V107*1000000
      biogas_output["StorageH2S_V107moles"] = Biogas_Plant.mol_H2S_V107

      ## Oxígeno
      biogas_output["StorageO2_V107Volume"] = Biogas_Plant.Vnormal_O2_V107
      biogas_output["StorageO2_V107Concentration"] = Biogas_Plant.x_O2_V107*100
      biogas_output["StorageO2_V107moles"] = Biogas_Plant.mol_O2_V107

      ## Amonio
      biogas_output["StorageNH3_V107Volume"] = Biogas_Plant.Vnormal_NH3_V107
      biogas_output["StorageNH3_V107Concentration"] = Biogas_Plant.x_NH3_V107*1000000
      biogas_output["StorageNH3_V107moles"] = Biogas_Plant.mol_NH3_V107

      ## Hidrógeno
      biogas_output["StorageH2_V107Volume"] = Biogas_Plant.Vnormal_H2_V107
      biogas_output["StorageH2_V107Concentration"] = Biogas_Plant.x_H2_V107*1000000
      biogas_output["StorageH2_V107moles"] = Biogas_Plant.mol_H2_V107

      #Agua
      biogas_output["moles_humidity_V107"] = Biogas_Plant.mol_H2O_V107
      biogas_output["Relative_humidity_V107"] = Biogas_Plant.RH_V107

      #Energía
      biogas_output["StorageEnergy_V107"] = Biogas_Plant.Energy_V107/3600

    
      

    return {"model": biogas_output}, 200