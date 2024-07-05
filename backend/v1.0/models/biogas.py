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

    biogas_input["name"] = data["name"]
    biogas_input["anaerobicReactorVolume1"]=data["anaerobicReactorVolume1"]["value"]
    biogas_input["anaerobicReactorVolume2"]=data["anaerobicReactorVolume2"]["value"]
    biogas_input["OfflineOperation"] = data["inputOfflineOperation"]
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
    biogas_input["inputTemperature101_"] = data["inputTemperature101"]['disabled']
    biogas_input["inputTemperature101"]=data["inputTemperature101"]["value"]
    biogas_input["inputTemperature102_"] = data["inputTemperature102"]['disabled']
    biogas_input["inputTemperature102"]=data["inputTemperature102"]["value"]
    
    biogas_input["InitialTotalSolidsR101"] = data["initialAnalysisConditions101"]["totalSubstrateSolids"]["value"]
    biogas_input["InitialBolatileSolidsR101"] = data["initialAnalysisConditions101"]["volatileSubstrateSolids"]["value"]
    biogas_input["InitialCcR101"] = data["initialAnalysisConditions101"]["atomicCarbonSubstrateConcetration"]["value"]
    biogas_input["InitialChR101"] = data["initialAnalysisConditions101"]["atomicHydrogenSubstrateConcetration"]["value"]
    biogas_input["InitialCoR101"] = data["initialAnalysisConditions101"]["atomicOxygenSubstrateConcetration"]["value"]
    biogas_input["InitialCnR101"] = data["initialAnalysisConditions101"]["atomicNitrogenSubstrateConcetration"]["value"]
    biogas_input["InitialCsR101"] = data["initialAnalysisConditions101"]["atomicSulfurSubstrateConcetration"]["value"]
    biogas_input["InitialDensityR101"] = data["initialAnalysisConditions101"]["substrateDensity"]["value"]

    biogas_input["InitialTotalSolidsR102"] = data["initialAnalysisConditions102"]["totalSubstrateSolids"]["value"]
    biogas_input["InitialBolatileSolidsR102"] = data["initialAnalysisConditions102"]["volatileSubstrateSolids"]["value"]
    biogas_input["InitialCcR102"] = data["initialAnalysisConditions102"]["atomicCarbonSubstrateConcetration"]["value"]
    biogas_input["InitialChR102"] = data["initialAnalysisConditions102"]["atomicHydrogenSubstrateConcetration"]["value"]
    biogas_input["InitialCoR102"] = data["initialAnalysisConditions102"]["atomicOxygenSubstrateConcetration"]["value"]
    biogas_input["InitialCnR102"] = data["initialAnalysisConditions102"]["atomicNitrogenSubstrateConcetration"]["value"]
    biogas_input["InitialCsR102"] = data["initialAnalysisConditions102"]["atomicSulfurSubstrateConcetration"]["value"]
    biogas_input["InitialDensityR102"] = data["initialAnalysisConditions102"]["substrateDensity"]["value"]
    
    if data.get("reset", False):                  #Enviar un flag con el boton iniciar para restablecer el singleton
      Biogas_Start.BiogasStart.reset_instance()
      MachineLearning_biogas_start.MachineLearningStart.reset_instance()
      Biogas_Simulation_Start.BiogasSimulationStart.reset_instance()

    if biogas_input["inputDigitalTwin"] == True: # Modo Gemelo On

      Biogas_Plant_ini = Biogas_Start.BiogasStart()
      Biogas_Plant_ini.starting(VR1 = biogas_input["anaerobicReactorVolume1"], VR2 = biogas_input["anaerobicReactorVolume2"], VG1 = biogas_input["biogasTankVolume1"], VG2 = biogas_input["biogasTankVolume2"],
                                VG3 = biogas_input["biogasTankVolume3"], tp = biogas_input["inputDigitalTwinStepTime"], ST_R101 = biogas_input["InitialTotalSolidsR101"], SV_R101 = biogas_input["InitialBolatileSolidsR101"], 
                                Cc_R101 = biogas_input["InitialCcR101"] , Ch_R101 = biogas_input["InitialChR101"], Co_R101 = biogas_input["InitialCoR101"], Cn_R101 = biogas_input["InitialCnR101"], Cs_R101 = biogas_input["InitialCsR101"], 
                                rho_R101 = biogas_input["InitialDensityR101"],ST_R102 = biogas_input["InitialTotalSolidsR102"], SV_R102 = biogas_input["InitialBolatileSolidsR102"], 
                                Cc_R102 = biogas_input["InitialCcR102"] , Ch_R102 = biogas_input["InitialChR102"], Co_R102 = biogas_input["InitialCoR102"], Cn_R102 = biogas_input["InitialCnR102"], Cs_R102 = biogas_input["InitialCsR102"], 
                                rho_R102 = biogas_input["InitialDensityR102"] , OperationMode = biogas_input["inputOperationMode"])

      Biogas_Plant = Biogas_Plant_ini.data
      Biogas_Plant.GetValuesFromBiogasPlant()
      Biogas_Plant.Substrate_conditions(manual_substrate=biogas_input["inputSubstrateConditions"], Cc = biogas_input["inputElementalAnalysisCarbonContent"], Ch = biogas_input["inputElementalAnalysisHydrogenContent"],
                                        Co = biogas_input["inputElementalAnalysisOxygenContent"], Cn = biogas_input["inputElementalAnalysisNitrogenContent"], Cs = biogas_input["inputElementalAnalysisSulfurContent"],
                                        rho = biogas_input["inputProximateAnalysisDensity"], ST = biogas_input["inputProximateAnalysisTotalSolids"], SV = biogas_input["inputProximateAnalysisVolatileSolids"])
      Biogas_Plant.Pump104(manual_P104=biogas_input["inputPump104"], TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
      Biogas_Plant.Pump101(manual_P101=biogas_input["inputPump101"], FT_P101=biogas_input["inputPump101StartsPerDay"], TTO_P101=biogas_input["inputPump101StartTime"], Q_P101=biogas_input["inputPump101Flow"])
      Biogas_Plant.Pump102(manual_P102=biogas_input["inputPump102"], FT_P102=biogas_input["inputPump102StartsPerDay"], TTO_P102=biogas_input["inputPump102StartTime"], Q_P102=biogas_input["inputPump102Flow"])
      Biogas_Plant.Temperature_R101(manual_temp_R101=biogas_input["inputTemperature101_"], Temp_R101=biogas_input["inputTemperature101"])
      Biogas_Plant.Temperature_R102(manual_temp_R102=biogas_input["inputTemperature102_"], Temp_R102=biogas_input["inputTemperature102"])
      Biogas_Plant.V_101_DT()
      Biogas_Plant.V_102_DT()
      Biogas_Plant.V_107_DT()
      Biogas_Plant.R101_DT()
      Biogas_Plant.R102_DT()
      Biogas_Plant.Energy_Biogas()
      Biogas_Plant.StorageData()

      Biogas_learning_ini = MachineLearning_biogas_start.MachineLearningStart()
      Biogas_learning_ini.starting(t_train= data["inputDigitalTwinTrainingTime"]["value"], OperationMode = biogas_input["inputOperationMode"], Model = "Arrhenius", A_R101 = 1, 
                                   B_R101 = 1, C_R101=1, A_R102=1, B_R102=1, C_R102=1, VR1 = data["anaerobicReactorVolume1"]["value"], VR2 = data["anaerobicReactorVolume2"]["value"])
      Biogas_learning = Biogas_learning_ini.data
      Biogas_learning.Get_data_DT(DataBase = Biogas_Plant.DT_Data)
      Biogas_learning.DT_time_and_data()
      Biogas_learning.Optimization(t_predict=data["inputDigitalTwinForecastTime"]["value"])
      
      # Exit variables for Gemelo On
    
      #Variables for TK-100
      biogas_output["Mix_TK100"] = Biogas_Plant.SE_107                                                   #RPM
      biogas_output["Mwsus"] = Biogas_Plant.MW_sustrato                                                  #g/mol   
      biogas_output["n"] = Biogas_Plant.n
      biogas_output["a"] = Biogas_Plant.a
      biogas_output["b"] = Biogas_Plant.b
      biogas_output["c"] = Biogas_Plant.c
      biogas_output["d"] = Biogas_Plant.d
      biogas_output["TotalSolidsInletR101"] = Biogas_Plant.Csus_ini_ST*Biogas_Plant.MW_sustrato          #g/L
      biogas_output["VolatileSolidsInletR101"] = Biogas_Plant.Csus_ini*Biogas_Plant.MW_sustrato          #g/L

      #Variables for Pump_104
      biogas_output["Organic_charge_R101_in"] = Biogas_Plant.organic_charge_R101_in                      #g/L-dia
      biogas_output["Pump104Flow"] = Biogas_Plant.Q_P104
      
      #Variables inside of R_101
      biogas_output["Temp_R101"] = Biogas_Plant.Temp_R101                                                #°c                                       
      biogas_output["pH_R101"] = Biogas_Plant.AT_101                                                     #No units 
      biogas_output["STsus_R101"] = Biogas_Plant.ST_R101                                                 #% 
      biogas_output["SVsus_R101"] = Biogas_Plant.SV_R101                                                 #% 
      biogas_output["Csus_exp_train_R101"] = Biogas_Plant.Csus_ini_R101                                  #mol/L
      biogas_output["Mix_R101"] = Biogas_Plant.SE_108                                                    #RPM 

      #Variable out R_101
      biogas_output["Organic_charge_R101_out"] = Biogas_Plant.organic_charge_R101_out                    #g/L-dia

      #Variable for V101
      biogas_output["StorageBiogasVolumeV101"] = Biogas_Plant.V_normal_V101                              #NL
      biogas_output["AcumBiogasVolumenV101"] = Biogas_Plant.Vnormal_acum_V101                            #NL
      biogas_output["StorageBiogasPressureV101"] = Biogas_Plant.PT103                                    #psi
      biogas_output["AcumBiogasPressureV101"] = Biogas_Plant.Pacum_V101                                  #psi
      
      biogas_output["StorageCH4_V101Volume"] = Biogas_Plant.V_normal_CH4_V101                            #NL
      biogas_output["StorageCO2_V101Volume"] = Biogas_Plant.V_normal_CO2_V101                            #NL
      biogas_output["StorageH2S_V101Volume"] = Biogas_Plant.V_normal_H2S_V101                            #NL
      biogas_output["StorageO2_V101Volume"] = Biogas_Plant.V_normal_O2_V101                              #NL
      biogas_output["StorageH2_V101Volume"] = Biogas_Plant.V_normal_H2_V101                              #NL
      biogas_output["StorageNH3_V101Volume"] = Biogas_Plant.V_normal_NH3_V101                            #NL

      biogas_output["StorageCH4_V101Concentration"] = Biogas_Plant.AT103A1                               #%
      biogas_output["StorageCO2_V101Concentration"] = Biogas_Plant.AT103A2                               #% 
      biogas_output["StorageH2S_V101Concentration"] = Biogas_Plant.AT103A3                               #ppm
      biogas_output["StorageO2_V101Concentration"] = Biogas_Plant.AT103A4                                #%
      biogas_output["StorageH2_V101Concentration"] = Biogas_Plant.AT103A5                                #ppm
      biogas_output["StorageNH3_V101Concentration"] = Biogas_Plant.AT103A6                               #ppm

      biogas_output["StorageCH4_V101moles"] = Biogas_Plant.mol_CH4_V101                                  #mol
      biogas_output["StorageCO2_V101moles"] = Biogas_Plant.mol_CO2_V101                                  #mol
      biogas_output["StorageH2S_V101moles"] = Biogas_Plant.mol_H2S_V101                                  #mol
      biogas_output["StorageO2_V101moles"] = Biogas_Plant.mol_O2_V101                                    #mol
      biogas_output["StorageH2_V101moles"] = Biogas_Plant.mol_H2_V101                                    #mol
      biogas_output["StorageNH3_V101moles"] = Biogas_Plant.mol_NH3_V101                                  #mol

      #Variable for V102
      biogas_output["StorageBiogasVolumeV102"] = Biogas_Plant.V_normal_V102                              #NL
      biogas_output["AcumBiogasVolumenV102"] = Biogas_Plant.Vnormal_acum_V102                            #NL
      biogas_output["StorageBiogasPressureV102"] = Biogas_Plant.PT104                                    #psi
      biogas_output["AcumBiogasPressureV102"] = Biogas_Plant.Pacum_V102                                  #psi
      
      biogas_output["StorageCH4_V102Volume"] = Biogas_Plant.V_normal_CH4_V102                            #NL
      biogas_output["StorageCO2_V102Volume"] = Biogas_Plant.V_normal_CO2_V102                            #NL
      biogas_output["StorageH2S_V102Volume"] = Biogas_Plant.V_normal_H2S_V102                            #NL
      biogas_output["StorageO2_V102Volume"] = Biogas_Plant.V_normal_O2_V102                              #NL
      biogas_output["StorageH2_V102Volume"] = Biogas_Plant.V_normal_H2_V102                              #NL
      biogas_output["StorageNH3_V102Volume"] = Biogas_Plant.V_normal_NH3_V102                            #NL

      biogas_output["StorageCH4_V102Concentration"] = Biogas_Plant.AT104A1                               #%
      biogas_output["StorageCO2_V102Concentration"] = Biogas_Plant.AT104A2                               #% 
      biogas_output["StorageH2S_V102Concentration"] = Biogas_Plant.AT104A3                               #ppm
      biogas_output["StorageO2_V102Concentration"] = Biogas_Plant.AT104A4                                #%
      biogas_output["StorageH2_V102Concentration"] = Biogas_Plant.AT104A5                                #ppm
      biogas_output["StorageNH3_V102Concentration"] = Biogas_Plant.AT104A6                               #ppm

      biogas_output["StorageCH4_V102moles"] = Biogas_Plant.mol_CH4_V102                                  #mol
      biogas_output["StorageCO2_V102moles"] = Biogas_Plant.mol_CO2_V102                                  #mol
      biogas_output["StorageH2S_V102moles"] = Biogas_Plant.mol_H2S_V102                                  #mol
      biogas_output["StorageO2_V102moles"] = Biogas_Plant.mol_O2_V102                                    #mol
      biogas_output["StorageH2_V102moles"] = Biogas_Plant.mol_H2_V102                                    #mol
      biogas_output["StorageNH3_V102moles"] = Biogas_Plant.mol_NH3_V102                                  #mol

    else:  #Modo Gemelo Off

      Biogas_Plant_ini = Biogas_Simulation_Start.BiogasSimulationStart()
      Biogas_Plant_ini.starting(VR1 = biogas_input["anaerobicReactorVolume1"], VR2 = biogas_input["anaerobicReactorVolume2"], VG1 = biogas_input["biogasTankVolume1"], VG2 = biogas_input["biogasTankVolume2"],
                                VG3 = biogas_input["biogasTankVolume3"], tp = biogas_input["inputDigitalTwinStepTime"], ST_R101 = biogas_input["InitialTotalSolidsR101"], SV_R101 = biogas_input["InitialBolatileSolidsR101"],
                                Cc_R101 = biogas_input["InitialCcR101"], Ch_R101 = biogas_input["InitialChR101"], Co_R101 = biogas_input["InitialCoR101"], Cn_R101 = biogas_input["InitialCnR101"], Cs_R101 = biogas_input["InitialCsR101"], 
                                rho_R101 = biogas_input["InitialDensityR101"],ST_R102 = biogas_input["InitialTotalSolidsR102"], SV_R102 = biogas_input["InitialBolatileSolidsR102"], 
                                Cc_R102 = biogas_input["InitialCcR102"] , Ch_R102 = biogas_input["InitialChR102"], Co_R102 = biogas_input["InitialCoR102"], Cn_R102 = biogas_input["InitialCnR102"], Cs_R102 = biogas_input["InitialCsR102"], 
                                rho_R102 = biogas_input["InitialDensityR102"] , OperationMode = biogas_input["inputOperationMode"])
      Biogas_Plant = Biogas_Plant_ini.data
      Biogas_Plant.Substrate_conditions(Cc = biogas_input["inputElementalAnalysisCarbonContent"], Ch = biogas_input["inputElementalAnalysisHydrogenContent"],
                                        Co = biogas_input["inputElementalAnalysisOxygenContent"], Cn = biogas_input["inputElementalAnalysisNitrogenContent"], Cs = biogas_input["inputElementalAnalysisSulfurContent"],
                                        rho = biogas_input["inputProximateAnalysisDensity"], ST = biogas_input["inputProximateAnalysisTotalSolids"], SV = biogas_input["inputProximateAnalysisVolatileSolids"])
      
      Biogas_Plant.Pump104(TRH=biogas_input["inputPump104HydraulicRetentionTime"], FT_P104=biogas_input["inputPump104StartsPerDay"], TTO_P104=biogas_input["inputPump104StartTime"])
      Biogas_Plant.Pump101(FT_P101=biogas_input["inputPump101StartsPerDay"], TTO_P101=biogas_input["inputPump101StartTime"], Q_P101=biogas_input["inputPump101Flow"])
      Biogas_Plant.Pump102(FT_P102=biogas_input["inputPump102StartsPerDay"], TTO_P102=biogas_input["inputPump102StartTime"], Q_P102=biogas_input["inputPump102Flow"])
      Biogas_Plant.Mixing_R101(FT_mixin_R101=24, TTO_mixing_R101= 30, RPM_R101=20)
      Biogas_Plant.Mixing_R102(FT_mixin_R102=5, TTO_mixing_R102=10, RPM_R102=50)
      Biogas_Plant.Data_simulation(Temperature_R101 = biogas_input["inputTemperature101"], Temperature_R102 = biogas_input["inputTemperature102"])
      Biogas_Plant.ReactorSimulation(Model = "Arrhenius", A_R101=100, B_R101 = 1000000, C_R101=1, A_R102=100, B_R102=1000000, C_R102=1, pH_R101 = 6.5, pH_R102 = 7)


      print(Biogas_Plant.Operation_Data)
      print(Biogas_Plant.mol_CH4_R101)
      # print(Biogas_Plant.x_R101)
      # try:
      #   print(Biogas_Plant.x_R102)
      # except NameError:
      #   pass



    # #print(biogas_input)
    #print(biogas_output)

    return {"model": biogas_output}, 200