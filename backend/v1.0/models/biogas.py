from flask import request
from flask_restful import Resource
from simulation_models.Biogas import BiogasModel
import pandas as pd

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

    if biogas_input["inputOperationMode"] == 1:
      pass
    elif biogas_input["inputOperationMode"] == 2:
      pass
    elif biogas_input["inputOperationMode"] == 3:
      pass
    elif biogas_input["inputOperationMode"] == 4:
      pass
    else:
      pass
    
    print(biogas_input)
    print(biogas_output)

    return {}, 200