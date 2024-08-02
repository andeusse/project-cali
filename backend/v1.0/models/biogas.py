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
      Biogas_learning_ini.starting(t_train= biogas_input["t_pred"], OperationMode = biogas_input["OperationMode"], Model = biogas_input["OperationModel"], A_R101 = biogas_input["A_R101"], 
                                   B_R101 = biogas_input["B_R101"], C_R101=biogas_input["C_R101"], A_R102=biogas_input["A_R102"], B_R102=biogas_input["B_R102"], 
                                   C_R102=biogas_input["C_R102"], VR1 = biogas_input["VR1"], VR2 = biogas_input["VR1"])
      Biogas_learning = Biogas_learning_ini.data
      Biogas_learning.Get_data_DT(DataBase = Biogas_Plant.DT_Data)
      Biogas_learning.DT_time_and_data()
      print(Biogas_learning.train_set)
      # Biogas_learning.Optimization(t_predict=biogas_input["t_pred"])
      
    #   # Exit variables for Gemelo On
    
    #   #Variables for TK-100
    #   biogas_output["Mix_TK100"] = Biogas_Plant.SE_107                                                   #RPM
    #   biogas_output["Mwsus"] = Biogas_Plant.MW_sustrato                                                  #g/mol   
    #   biogas_output["n"] = Biogas_Plant.n
    #   biogas_output["a"] = Biogas_Plant.a
    #   biogas_output["b"] = Biogas_Plant.b
    #   biogas_output["c"] = Biogas_Plant.c
    #   biogas_output["d"] = Biogas_Plant.d
    #   biogas_output["TotalSolidsInletR101"] = Biogas_Plant.Csus_ini_ST*Biogas_Plant.MW_sustrato          #g/L
    #   biogas_output["VolatileSolidsInletR101"] = Biogas_Plant.Csus_ini*Biogas_Plant.MW_sustrato          #g/L

    #   #Variables for Pump_104
    #   biogas_output["Organic_charge_R101_in"] = Biogas_Plant.organic_charge_R101_in                      #g/L-dia
    #   biogas_output["Pump104Flow"] = Biogas_Plant.Q_P104
      
    #   #Variables inside of R_101
    #   biogas_output["Temp_R101"] = Biogas_Plant.Temp_R101                                                #°c                                       
    #   biogas_output["pH_R101"] = Biogas_Plant.AT_101                                                     #No units 
    #   biogas_output["STsus_R101"] = Biogas_Plant.ST_R101                                                 #% 
    #   biogas_output["SVsus_R101"] = Biogas_Plant.SV_R101                                                 #% 
    #   biogas_output["Csus_exp_train_R101"] = Biogas_Plant.Csus_ini_R101                                  #mol/L
    #   biogas_output["Mix_R101"] = Biogas_Plant.SE_108                                                    #RPM 

    #   #Variable out R_101
    #   biogas_output["Organic_charge_R101_out"] = Biogas_Plant.organic_charge_R101_out                    #g/L-dia

    #   #Variable for V101
    #   biogas_output["StorageBiogasVolumeV101"] = Biogas_Plant.V_normal_V101                              #NL
    #   biogas_output["AcumBiogasVolumenV101"] = Biogas_Plant.Vnormal_acum_V101                            #NL
    #   biogas_output["StorageBiogasPressureV101"] = Biogas_Plant.PT103                                    #psi
    #   biogas_output["AcumBiogasPressureV101"] = Biogas_Plant.Pacum_V101                                  #psi
      
    #   biogas_output["StorageCH4_V101Volume"] = Biogas_Plant.V_normal_CH4_V101                            #NL
    #   biogas_output["StorageCO2_V101Volume"] = Biogas_Plant.V_normal_CO2_V101                            #NL
    #   biogas_output["StorageH2S_V101Volume"] = Biogas_Plant.V_normal_H2S_V101                            #NL
    #   biogas_output["StorageO2_V101Volume"] = Biogas_Plant.V_normal_O2_V101                              #NL
    #   biogas_output["StorageH2_V101Volume"] = Biogas_Plant.V_normal_H2_V101                              #NL
    #   biogas_output["StorageNH3_V101Volume"] = Biogas_Plant.V_normal_NH3_V101                            #NL

    #   biogas_output["StorageCH4_V101Concentration"] = Biogas_Plant.AT103A1                               #%
    #   biogas_output["StorageCO2_V101Concentration"] = Biogas_Plant.AT103A2                               #% 
    #   biogas_output["StorageH2S_V101Concentration"] = Biogas_Plant.AT103A3                               #ppm
    #   biogas_output["StorageO2_V101Concentration"] = Biogas_Plant.AT103A4                                #%
    #   biogas_output["StorageH2_V101Concentration"] = Biogas_Plant.AT103A5                                #ppm
    #   biogas_output["StorageNH3_V101Concentration"] = Biogas_Plant.AT103A6                               #ppm

    #   biogas_output["StorageCH4_V101moles"] = Biogas_Plant.mol_CH4_V101                                  #mol
    #   biogas_output["StorageCO2_V101moles"] = Biogas_Plant.mol_CO2_V101                                  #mol
    #   biogas_output["StorageH2S_V101moles"] = Biogas_Plant.mol_H2S_V101                                  #mol
    #   biogas_output["StorageO2_V101moles"] = Biogas_Plant.mol_O2_V101                                    #mol
    #   biogas_output["StorageH2_V101moles"] = Biogas_Plant.mol_H2_V101                                    #mol
    #   biogas_output["StorageNH3_V101moles"] = Biogas_Plant.mol_NH3_V101                                  #mol

    #   #Variable for V102
    #   biogas_output["StorageBiogasVolumeV102"] = Biogas_Plant.V_normal_V102                              #NL
    #   biogas_output["AcumBiogasVolumenV102"] = Biogas_Plant.Vnormal_acum_V102                            #NL
    #   biogas_output["StorageBiogasPressureV102"] = Biogas_Plant.PT104                                    #psi
    #   biogas_output["AcumBiogasPressureV102"] = Biogas_Plant.Pacum_V102                                  #psi
      
    #   biogas_output["StorageCH4_V102Volume"] = Biogas_Plant.V_normal_CH4_V102                            #NL
    #   biogas_output["StorageCO2_V102Volume"] = Biogas_Plant.V_normal_CO2_V102                            #NL
    #   biogas_output["StorageH2S_V102Volume"] = Biogas_Plant.V_normal_H2S_V102                            #NL
    #   biogas_output["StorageO2_V102Volume"] = Biogas_Plant.V_normal_O2_V102                              #NL
    #   biogas_output["StorageH2_V102Volume"] = Biogas_Plant.V_normal_H2_V102                              #NL
    #   biogas_output["StorageNH3_V102Volume"] = Biogas_Plant.V_normal_NH3_V102                            #NL

    #   biogas_output["StorageCH4_V102Concentration"] = Biogas_Plant.AT104A1                               #%
    #   biogas_output["StorageCO2_V102Concentration"] = Biogas_Plant.AT104A2                               #% 
    #   biogas_output["StorageH2S_V102Concentration"] = Biogas_Plant.AT104A3                               #ppm
    #   biogas_output["StorageO2_V102Concentration"] = Biogas_Plant.AT104A4                                #%
    #   biogas_output["StorageH2_V102Concentration"] = Biogas_Plant.AT104A5                                #ppm
    #   biogas_output["StorageNH3_V102Concentration"] = Biogas_Plant.AT104A6                               #ppm

    #   biogas_output["StorageCH4_V102moles"] = Biogas_Plant.mol_CH4_V102                                  #mol
    #   biogas_output["StorageCO2_V102moles"] = Biogas_Plant.mol_CO2_V102                                  #mol
    #   biogas_output["StorageH2S_V102moles"] = Biogas_Plant.mol_H2S_V102                                  #mol
    #   biogas_output["StorageO2_V102moles"] = Biogas_Plant.mol_O2_V102                                    #mol
    #   biogas_output["StorageH2_V102moles"] = Biogas_Plant.mol_H2_V102                                    #mol
    #   biogas_output["StorageNH3_V102moles"] = Biogas_Plant.mol_NH3_V102                                  #mol

    # else:  #Modo Gemelo Off

    #   Biogas_Plant_ini = Biogas_Simulation_Start.BiogasSimulationStart()
    #   Biogas_Plant_ini.starting(VR1 = biogas_input["anaerobicReactorVolume1"], VR2 = biogas_input["anaerobicReactorVolume2"], VG1 = biogas_input["biogasTankVolume1"], VG2 = biogas_input["biogasTankVolume2"],
    #                             VG3 = biogas_input["biogasTankVolume3"], tp = biogas_input["inputDigitalTwinStepTime"], ST_R101 = biogas_input["InitialTotalSolidsR101"], SV_R101 = biogas_input["InitialBolatileSolidsR101"],
    #                             Cc_R101 = biogas_input["InitialCcR101"], Ch_R101 = biogas_input["InitialChR101"], Co_R101 = biogas_input["InitialCoR101"], Cn_R101 = biogas_input["InitialCnR101"], Cs_R101 = biogas_input["InitialCsR101"], 
    #                             rho_R101 = biogas_input["InitialDensityR101"],ST_R102 = biogas_input["InitialTotalSolidsR102"], SV_R102 = biogas_input["InitialBolatileSolidsR102"], 
    #                             Cc_R102 = biogas_input["InitialCcR102"] , Ch_R102 = biogas_input["InitialChR102"], Co_R102 = biogas_input["InitialCoR102"], Cn_R102 = biogas_input["InitialCnR102"], Cs_R102 = biogas_input["InitialCsR102"], 
    #                             rho_R102 = biogas_input["InitialDensityR102"] , OperationMode = biogas_input["inputOperationMode"])
    #   Biogas_Plant = Biogas_Plant_ini.data
    #   Biogas_Plant.Substrate_conditions(Cc = biogas_input["inputElementalAnalysisCarbonContent"], Ch = biogas_input["inputElementalAnalysisHydrogenContent"],
    #                                     Co = biogas_input["inputElementalAnalysisOxygenContent"], Cn = biogas_input["inputElementalAnalysisNitrogenContent"], Cs = biogas_input["inputElementalAnalysisSulfurContent"],
    #                                     rho = biogas_input["inputProximateAnalysisDensity"], ST = biogas_input["inputProximateAnalysisTotalSolids"], SV = biogas_input["inputProximateAnalysisVolatileSolids"])
      
    #   Biogas_Plant.Pump104(TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
    #   Biogas_Plant.Pump101(FT_P101=biogas_input["inputPump101StartsPerDay"], TTO_P101=biogas_input["inputPump101StartTime"], Q_P101=biogas_input["inputPump101Flow"])
    #   Biogas_Plant.Pump102(FT_P102=biogas_input["inputPump102StartsPerDay"], TTO_P102=biogas_input["inputPump102StartTime"], Q_P102=biogas_input["inputPump102Flow"])
    #   Biogas_Plant.Mixing_R101(FT_mixin_R101=24, TTO_mixing_R101= 30, RPM_R101=20)
    #   Biogas_Plant.Mixing_R102(FT_mixin_R102=5, TTO_mixing_R102=10, RPM_R102=50)
    #   Biogas_Plant.Data_simulation(Temperature_R101 = biogas_input["inputTemperature101"], Temperature_R102 = biogas_input["inputTemperature102"], pH_R101 = 7, pH_R102 = 7)
    #   Biogas_Plant.ReactorSimulation(Model = "Arrhenius", A_R101=100, B_R101 = 10000, C_R101 = -46656, A_R102=100, B_R102=1000000, C_R102=-46656)
    #   Biogas_Plant.V101()
    #   Biogas_Plant.V102()
    #   Biogas_Plant.biogas_treatment(D1 = 1E-10, D2 = 1E-10, D3 = 1E-10)

    #   print(Biogas_Plant.Operation_Data.iloc[:, :18])
         
      
      
    #   # print(Biogas_Plant.x_R101)
    #   # try:
    #   #   print(Biogas_Plant.x_R102)
    #   # except NameError:
    #   #   pass



    # # #print(biogas_input)
    # #print(biogas_output)
    print (biogas_input)

    return {"model": biogas_output}, 200