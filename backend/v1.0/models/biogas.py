from flask import request
from flask_restful import Resource
import pandas as pd
from utils import Biogas_Start
from utils import MachineLearning_biogas_start

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

    if biogas_input["inputDigitalTwin"] == True:
      Biogas_Plant_ini = Biogas_Start.BiogasStart()
      Biogas_Plant_ini.starting(VR1 = biogas_input["anaerobicReactorVolume1"], VR2 = biogas_input["anaerobicReactorVolume2"], VG1 = biogas_input["biogasTankVolume1"], VG2 = biogas_input["biogasTankVolume2"],
                                VG3 = biogas_input["biogasTankVolume3"], tp = biogas_input["inputDigitalTwinStepTime"], rho_R101 = 1000, rho_R102=1000, OperationMode = biogas_input["inputOperationMode"])

      Biogas_Plant = Biogas_Plant_ini.data
      Biogas_Plant.GetValuesFromBiogasPlant()

    print(biogas_input)
    print(biogas_output)

    return {"model": biogas_output}, 200