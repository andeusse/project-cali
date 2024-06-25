from utils import Biogas_Start
from utils import MachineLearning_biogas_start
import time

while True:
    biogas_input = {}
    biogas_output = {}

    biogas_input["anaerobicReactorVolume1"]=30
    biogas_input["anaerobicReactorVolume2"]=70
    biogas_input["OfflineOperation"] = False
    biogas_input["biogasTankVolume1"] = 15
    biogas_input["biogasTankVolume2"] = 35
    biogas_input["biogasTankVolume3"] = 35
    biogas_input["inputOperationMode"] = 1
    biogas_input["inputSubstrateConditions"] = False
    biogas_input["inputElementalAnalysisCarbonContent"] = 40.4
    biogas_input["inputElementalAnalysisHydrogenContent"] = 5.29
    biogas_input["inputElementalAnalysisOxygenContent"] = 29.66
    biogas_input["inputElementalAnalysisNitrogenContent"] = 1.37
    biogas_input["inputElementalAnalysisSulfurContent"] = 0.211
    biogas_input["inputProximateAnalysisTotalSolids"] = 10
    biogas_input["inputProximateAnalysisVolatileSolids"] = 1.0
    biogas_input["inputProximateAnalysisDensity"]=1000
    biogas_input["inputDigitalTwin"]=True
    biogas_input["inputDigitalTwinStepTime"]=30
    biogas_input["inputDigitalTwinTrainingTime"]=0.1
    biogas_input["inputDigitalTwinForecastTime"]=1
    biogas_input["inputKineticParameterInitialValue"]=1
    biogas_input["inputSpeedLawOrder"]=1
    biogas_input["inputSpeedLawExponentialFactor"]=1
    biogas_input["inputSpeedLawStartEnergy"]=1
    biogas_input["inputPump104"] = True
    biogas_input["inputPump104HydraulicRetentionTime"] = 30
    biogas_input["inputPump104StartTime"]= 10
    biogas_input["inputPump104StartsPerDay"]= 5
    biogas_input["inputPump102"]= True
    biogas_input["inputPump102Flow"]= 2.4
    biogas_input["inputPump102StartTime"] = 10
    biogas_input["inputPump102StartsPerDay"] = 5
    biogas_input["inputPump101"]= True
    biogas_input["inputPump101Flow"] = 2.4
    biogas_input["inputPump101StartTime"] = 10
    biogas_input["inputPump101StartsPerDay"] = 5
    biogas_input["inputTemperature101_"] = False
    biogas_input["inputTemperature101"] = 35
    biogas_input["inputTemperature102_"] = False
    biogas_input["inputTemperature102"] = 35

    # biogas_input["InitialTotalSolidsR101"] = data["initialAnalysisConditions101"]["totalSubstrateSolids"]["value"]
    # biogas_input["InitialBolatileSolidsR101"] = data["initialAnalysisConditions101"]["volatileSubstrateSolids"]["value"]
    # biogas_input["InitialCcR101"] = data["initialAnalysisConditions101"]["atomicCarbonSubstrateConcetration"]["value"]
    # biogas_input["InitialChR101"] = data["initialAnalysisConditions101"]["atomicHydrogenSubstrateConcetration"]["value"]
    # biogas_input["InitialCoR101"] = data["initialAnalysisConditions101"]["atomicOxygenSubstrateConcetration"]["value"]
    # biogas_input["InitialCnR101"] = data["initialAnalysisConditions101"]["atomicNitrogenSubstrateConcetration"]["value"]
    # biogas_input["InitialCsR101"] = data["initialAnalysisConditions101"]["atomicSulfurSubstrateConcetration"]["value"]
    # biogas_input["InitialDensityR101"] = data["initialAnalysisConditions101"]["substrateDensity"]["value"]

    # biogas_input["InitialTotalSolidsR102"] = data["initialAnalysisConditions102"]["totalSubstrateSolids"]["value"]
    # biogas_input["InitialBolatileSolidsR102"] = data["initialAnalysisConditions102"]["volatileSubstrateSolids"]["value"]
    # biogas_input["InitialCcR102"] = data["initialAnalysisConditions102"]["atomicCarbonSubstrateConcetration"]["value"]
    # biogas_input["InitialChR102"] = data["initialAnalysisConditions102"]["atomicHydrogenSubstrateConcetration"]["value"]
    # biogas_input["InitialCoR102"] = data["initialAnalysisConditions102"]["atomicOxygenSubstrateConcetration"]["value"]
    # biogas_input["InitialCnR102"] = data["initialAnalysisConditions102"]["atomicNitrogenSubstrateConcetration"]["value"]
    # biogas_input["InitialCsR102"] = data["initialAnalysisConditions102"]["atomicSulfurSubstrateConcetration"]["value"]
    # biogas_input["InitialDensityR102"] = data["initialAnalysisConditions102"]["substrateDensity"]["value"]
    
    # if data.get("reset", False):                  #Enviar un flag con el boton iniciar para restablecer el singleton
    #   Biogas_Start.BiogasStart.reset_instance()
    #   MachineLearning_biogas_start.MachineLearningStart.reset_instance()

    if biogas_input["inputDigitalTwin"] == True:
      Biogas_Plant_ini = Biogas_Start.BiogasStart()
      Biogas_Plant_ini.starting(VR1 = biogas_input["anaerobicReactorVolume1"], VR2 = biogas_input["anaerobicReactorVolume2"], VG1 = biogas_input["biogasTankVolume1"], VG2 = biogas_input["biogasTankVolume2"],
                                VG3 = biogas_input["biogasTankVolume3"], tp = biogas_input["inputDigitalTwinStepTime"], rho_R101 = 1000, rho_R102=1000, OperationMode = biogas_input["inputOperationMode"])

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
      
      print(Biogas_Plant.DT_Data)
      df = Biogas_Plant.DT_Data
    
    else:
      pass

    print(biogas_input)
    print(biogas_output)

    #time.sleep(30)