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
                            VG3 = biogas_input["biogasTankVolume3"], tp = biogas_input["inputDigitalTwinStepTime"], ST_R101 = biogas_input["InitialTotalSolidsR101"], SV_R101 = biogas_input["InitialBolatileSolidsR101"],
                            Cc_R101 = biogas_input["InitialCcR101"], Ch_R101=biogas_input["InitialChR101"], Co_R101 = biogas_input["InitialCoR101"], Cn_R101 = biogas_input["InitialCnR101"],
                            Cs_R101 = biogas_input["InitialCsR101"], rho_R101 = biogas_input["InitialDensityR101"], ST_R102 = biogas_input["InitialTotalSolidsR102"], SV_R102 = biogas_input["InitialBolatileSolidsR102"],
                            Cc_R102 = biogas_input["InitialCcR102"], Ch_R102=biogas_input["InitialChR102"], Co_R102 = biogas_input["InitialCoR102"], Cn_R102 = biogas_input["InitialCnR102"],
                            Cs_R102 = biogas_input["InitialCsR102"], rho_R102 = biogas_input["InitialDensityR102"], OperationMode=biogas_input["inputOperationMode"])
      
      Biogas_plant = Biogas_Plant_ini.data
      Biogas_plant.GetValuesFromBiogasPlant()
      Biogas_plant.Substrate_conditions(Offline = biogas_input["OfflineOperation"], manual_sustrate = biogas_input["inputSubstrateConditions"], ST = biogas_input["inputProximateAnalysisTotalSolids"],
                                        SV = biogas_input["inputProximateAnalysisVolatileSolids"], Cc = biogas_input["inputElementalAnalysisCarbonContent"], Ch = biogas_input["inputElementalAnalysisHydrogenContent"],
                                        Co = biogas_input["inputElementalAnalysisOxygenContent"], Cn = biogas_input["inputElementalAnalysisNitrogenContent"], Cs = biogas_input["inputElementalAnalysisSulfurContent"],
                                        rho = biogas_input["inputProximateAnalysisDensity"])
  
      if biogas_input["inputOperationMode"] == 1:
        Biogas_plant.Pump104_Operation_1_2(manual_P104 = biogas_input["inputPump104"], TRH = biogas_input["inputPump104HydraulicRetentionTime"], FT_P104 = biogas_input["inputPump104StartsPerDay"],
                                           TTO_P104 = biogas_input["inputPump104StartTime"])
        Biogas_plant.Temperature_R101(manual_temp_R101 = biogas_input["inputTemperature101_"], Temp_R101 = biogas_input["inputTemperature101"])

        Biogas_plant.V_101_DT()
        Biogas_plant.V_102_DT()
        Biogas_plant.V_107_DT()

        Biogas_plant.R101_DT_operation_1()

        Biogas_plant.Energy_Biogas()
        Biogas_plant.StorageData()

        if len(Biogas_plant.DT_Data)>4:
          Machine_learning_ini = MachineLearning_biogas_start.MachineLearningStart()
          Machine_learning_ini.starting(t_train = biogas_input["inputDigitalTwinTrainingTime"], OperationMode = biogas_input["inputOperationMode"], Kini = biogas_input["inputKineticParameterInitialValue"], Eaini=1,
                                        VR1 = biogas_input["anaerobicReactorVolume1"])
          Machine_learning = Machine_learning_ini.data
          Machine_learning.Get_data_DT(Biogas_plant.DT_Data)
          Machine_learning.DT_time_and_data()
          Machine_learning.Operation_1_Optimization()
          Machine_learning.StorageData()

          K_R101 = Machine_learning.K_R101
          Ea_R101 = Machine_learning.Ea_R101
          X_R101 = Machine_learning.X_R101*100


    

    Csus_exp_train_R101 = Biogas_plant.Csus_ini_R101
    STsus_R101 = Biogas_plant.ST_R101
    Svsus_R101 = Biogas_plant.SV_R101
    FlowExit_R101 = Biogas_plant.Q_P104
    VolatileSolidsInletR101 = Biogas_plant.Csus_ini
    TotalSolidsInletR101 = Biogas_plant.Csus_ini_ST
    Mwsus = Biogas_plant.MW_sustrato
    n = Biogas_plant.n
    a = Biogas_plant.a
    b = Biogas_plant.b
    c = Biogas_plant.c
    d = Biogas_plant.d
    Pump104Flow = Biogas_plant.Q_P104

    StorageBiogasVolumeV101 = Biogas_plant.V_normal_V101
    AcumBiogasVolumenV101 = Biogas_plant.Vnormal_acum_V101
    StorageBiogasPressureV101 = Biogas_plant.PT103v.iloc[-1]
    AcumBiogasPressureV101 = Biogas_plant.Pacum_V101
    StorageCH4_V101Volume = Biogas_plant.V_normal_CH4_V101
    StorageCO2_V101Volume = Biogas_plant.V_normal_CO2_V101
    StorageH2S_V101Volume = Biogas_plant.V_normal_H2S_V101
    StorageO2_V101Volume = Biogas_plant.V_normal_O2_V101
    StorageH2_V101Volume = Biogas_plant.V_normal_H2_V101
    StorageCH4_V101Concentration = Biogas_plant.AT103A1v.iloc[-1]
    StorageCO2_V101Concentration = Biogas_plant.AT103A2v.iloc[-1]
    StorageH2S_V101Concentration = Biogas_plant.AT103A3v.iloc[-1]
    StorageO2_V101Concentration = Biogas_plant.AT103A4v.iloc[-1]
    StorageH2_V101Concentration = Biogas_plant.AT103A5v.iloc[-1]
    StorageCH4_V101moles = Biogas_plant.mol_CH4_V101
    StorageCO2_V101moles = Biogas_plant.mol_CO2_V101
    StorageH2S_V101moles = Biogas_plant.mol_H2S_V101
    StorageO2_V101moles = Biogas_plant.mol_O2_V101
    StorageH2_V101moles = Biogas_plant.mol_H2_V101
    moles_humidity_V101 = Biogas_plant.mol_H2O_V101
    Relative_humidity_V101 = Biogas_plant.RH_V101*100
    StorageEnergy_V101 = Biogas_plant.Energy_V101/3600

    StorageBiogasVolumeV102 = Biogas_plant.V_normal_V102
    AcumBiogasVolumenV102 = Biogas_plant.Vnormal_acum_V102
    StorageBiogasPressureV102 = Biogas_plant.PT103v.iloc[-1]
    AcumBiogasPressureV102 = Biogas_plant.Pacum_V102
    StorageCH4_V102Volume = Biogas_plant.V_normal_CH4_V102
    StorageCO2_V102Volume = Biogas_plant.V_normal_CO2_V102
    StorageH2S_V102Volume = Biogas_plant.V_normal_H2S_V102
    StorageO2_V102Volume = Biogas_plant.V_normal_O2_V102
    StorageH2_V102Volume = Biogas_plant.V_normal_H2_V102
    StorageCH4_V102Concentration = Biogas_plant.AT104A1v.iloc[-1]
    StorageCO2_V102Concentration = Biogas_plant.AT104A2v.iloc[-1]
    StorageH2S_V102Concentration = Biogas_plant.AT104A3v.iloc[-1]
    StorageO2_V102Concentration = Biogas_plant.AT104A4v.iloc[-1]
    StorageH2_V102Concentration = Biogas_plant.AT104A5v.iloc[-1]
    StorageCH4_V102moles = Biogas_plant.mol_CH4_V102
    StorageCO2_V102moles = Biogas_plant.mol_CO2_V102
    StorageH2S_V102moles = Biogas_plant.mol_H2S_V102
    StorageO2_V102moles = Biogas_plant.mol_O2_V102
    StorageH2_V102moles = Biogas_plant.mol_H2_V102
    moles_humidity_V102 = Biogas_plant.mol_H2O_V102
    Relative_humidity_V102 = Biogas_plant.RH_V102*100
    StorageEnergy_V102 = Biogas_plant.Energy_V102/3600

    StorageBiogasVolumeV107 = Biogas_plant.V_normal_V107
    AcumBiogasVolumenV107 = Biogas_plant.Vnormal_acum_V107
    StorageBiogasPressureV107 = Biogas_plant.PT103v.iloc[-1]
    AcumBiogasPressureV107 = Biogas_plant.Pacum_V107
    StorageCH4_V107Volume = Biogas_plant.V_normal_CH4_V107
    StorageCO2_V107Volume = Biogas_plant.V_normal_CO2_V107
    StorageH2S_V107Volume = Biogas_plant.V_normal_H2S_V107
    StorageO2_V107Volume = Biogas_plant.V_normal_O2_V107
    StorageH2_V107Volume = Biogas_plant.V_normal_H2_V107
    StorageCH4_V107Concentration = Biogas_plant.AT105A1v.iloc[-1]
    StorageCO2_V107Concentration = Biogas_plant.AT105A2v.iloc[-1]
    StorageH2S_V107Concentration = Biogas_plant.AT105A3v.iloc[-1]
    StorageO2_V107Concentration = Biogas_plant.AT105A4v.iloc[-1]
    StorageH2_V107Concentration = Biogas_plant.AT105A5v.iloc[-1]
    StorageCH4_V107moles = Biogas_plant.mol_CH4_V107
    StorageCO2_V107moles = Biogas_plant.mol_CO2_V107
    StorageH2S_V107moles = Biogas_plant.mol_H2S_V107
    StorageO2_V107moles = Biogas_plant.mol_O2_V107
    StorageH2_V107moles = Biogas_plant.mol_H2_V107
    moles_humidity_V107 = Biogas_plant.mol_H2O_V107
    Relative_humidity_V107 = Biogas_plant.RH_V107*100
    StorageEnergy_V107 = Biogas_plant.Energy_V107/3600

    
    #Machine learning exit variables 
    try:
      biogas_output["K_R101"] = K_R101
      biogas_output["Ea_R101"] = Ea_R101
      biogas_output["x_R101"] = X_R101 
    except NameError:
      biogas_output["K_R101"] = 0
      biogas_output["Ea_R101"] = 0
      biogas_output["x_R101"] = 0 

    biogas_output["Csus_exp_train_R101"] =  Csus_exp_train_R101
    biogas_output["STsus_R101"] = STsus_R101*100
    biogas_output["Svsus_R101"] = Svsus_R101*100
    biogas_output["FlowExit_R101"] = FlowExit_R101
    biogas_output["VolatileSolidsInletR101"] =VolatileSolidsInletR101
    biogas_output["TotalSolidsInletR101"] = TotalSolidsInletR101
    biogas_output["Mwsus"] = Mwsus
    biogas_output["n"] = n
    biogas_output["a"] = a
    biogas_output["b"] = b
    biogas_output["c"] = c
    biogas_output["d"] = d
    biogas_output["Pump104Flow"] = Pump104Flow

    biogas_output["StorageBiogasVolumeV101"] = StorageBiogasVolumeV101
    biogas_output["AcumBiogasVolumenV101"] = AcumBiogasVolumenV101
    biogas_output["StorageBiogasPressureV101"] = StorageBiogasPressureV101
    biogas_output["AcumBiogasPressureV101"] = AcumBiogasPressureV101
    biogas_output["StorageCH4_V101Volume"] = StorageCH4_V101Volume
    biogas_output["StorageCO2_V101Volume"] = StorageCO2_V101Volume
    biogas_output["StorageH2S_V101Volume"] = StorageH2S_V101Volume
    biogas_output["StorageO2_V101Volume"] = StorageO2_V101Volume
    biogas_output["StorageH2_V101Volume"] = StorageH2_V101Volume
    biogas_output["StorageCH4_V101Concentration"] = StorageCH4_V101Concentration
    biogas_output["StorageCO2_V101Concentration"] = StorageCO2_V101Concentration
    biogas_output["StorageH2S_V101Concentration"] = StorageH2S_V101Concentration
    biogas_output["StorageO2_V101Concentration"] = StorageO2_V101Concentration
    biogas_output["StorageH2_V101Concentration"] = StorageH2_V101Concentration
    biogas_output["StorageCH4_V101moles"] = StorageCH4_V101moles
    biogas_output["StorageCO2_V101moles"] = StorageCO2_V101moles
    biogas_output["StorageH2S_V101moles"] = StorageH2S_V101moles
    biogas_output["StorageO2_V101moles"] = StorageO2_V101moles
    biogas_output["StorageH2_V101moles"] = StorageH2_V101moles
    biogas_output["moles_humidity_V101"] = moles_humidity_V101
    biogas_output["Relative_humidity_V101"] = Relative_humidity_V101 
    biogas_output["StorageEnergy_V101"] = StorageEnergy_V101

    biogas_output["StorageBiogasVolumeV102"] = StorageBiogasVolumeV102
    biogas_output["AcumBiogasVolumenV102"] = AcumBiogasVolumenV102
    biogas_output["StorageBiogasPressureV102"] = StorageBiogasPressureV102
    biogas_output["AcumBiogasPressureV102"] = AcumBiogasPressureV102
    biogas_output["StorageCH4_V102Volume"] = StorageCH4_V102Volume
    biogas_output["StorageCO2_V102Volume"] = StorageCO2_V102Volume
    biogas_output["StorageH2S_V102Volume"] = StorageH2S_V102Volume
    biogas_output["StorageO2_V102Volume"] = StorageO2_V102Volume
    biogas_output["StorageH2_V102Volume"] = StorageH2_V102Volume
    biogas_output["StorageCH4_V102Concentration"] = StorageCH4_V102Concentration
    biogas_output["StorageCO2_V102Concentration"] = StorageCO2_V102Concentration
    biogas_output["StorageH2S_V102Concentration"] = StorageH2S_V102Concentration
    biogas_output["StorageO2_V102Concentration"] = StorageO2_V102Concentration
    biogas_output["StorageH2_V102Concentration"] = StorageH2_V102Concentration
    biogas_output["StorageCH4_V102moles"] = StorageCH4_V102moles
    biogas_output["StorageCO2_V102moles"] = StorageCO2_V102moles
    biogas_output["StorageH2S_V102moles"] = StorageH2S_V102moles
    biogas_output["StorageO2_V102moles"] = StorageO2_V102moles
    biogas_output["StorageH2_V102moles"] = StorageH2_V102moles
    biogas_output["moles_humidity_V102"] = moles_humidity_V102
    biogas_output["Relative_humidity_V102"] = Relative_humidity_V102 
    biogas_output["StorageEnergy_V102"] = StorageEnergy_V102

    biogas_output["StorageBiogasVolumeV107"] = StorageBiogasVolumeV107
    biogas_output["AcumBiogasVolumenV107"] = AcumBiogasVolumenV107
    biogas_output["StorageBiogasPressureV107"] = StorageBiogasPressureV107
    biogas_output["AcumBiogasPressureV107"] = AcumBiogasPressureV107
    biogas_output["StorageCH4_V107Volume"] = StorageCH4_V107Volume
    biogas_output["StorageCO2_V107Volume"] = StorageCO2_V107Volume
    biogas_output["StorageH2S_V107Volume"] = StorageH2S_V107Volume
    biogas_output["StorageO2_V107Volume"] = StorageO2_V107Volume
    biogas_output["StorageH2_V107Volume"] = StorageH2_V107Volume
    biogas_output["StorageCH4_V107Concentration"] = StorageCH4_V107Concentration
    biogas_output["StorageCO2_V107Concentration"] = StorageCO2_V107Concentration
    biogas_output["StorageH2S_V107Concentration"] = StorageH2S_V107Concentration
    biogas_output["StorageO2_V107Concentration"] = StorageO2_V107Concentration
    biogas_output["StorageH2_V107Concentration"] = StorageH2_V107Concentration
    biogas_output["StorageCH4_V107moles"] = StorageCH4_V107moles
    biogas_output["StorageCO2_V107moles"] = StorageCO2_V107moles
    biogas_output["StorageH2S_V107moles"] = StorageH2S_V107moles
    biogas_output["StorageO2_V107moles"] = StorageO2_V107moles
    biogas_output["StorageH2_V107moles"] = StorageH2_V107moles
    biogas_output["moles_humidity_V107"] = moles_humidity_V107
    biogas_output["Relative_humidity_V107"] = Relative_humidity_V107 
    biogas_output["StorageEnergy_V107"] = StorageEnergy_V107
    
    print(biogas_input)
    print(biogas_output)

    return {"model": biogas_output}, 200