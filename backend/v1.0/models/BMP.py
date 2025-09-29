from flask import request
from flask_restful import Resource
from simulation_models.BMPModel import BMPOffline
from simulation_models.BMPModel import BMPOnlineTrainMode
from tools import DBManager
import os
import json
import numpy as np

bmp_instancesSideA = {}
bmp_instancesSideB = {}
data_instancesSideA = {}
data_instancesSideB = {}

bmp_instances_offline_SideA = {}
bmp_instances_offline_SideB = {}

class BMP(Resource):
  def get(self):
    method = request.args.get('method')
    model = request.args.get('model')
    measurement='Planta_PBM'

    DB_IP = os.getenv('DB_IP')
    DB_Port = os.getenv('DB_Port')
    DB_Bucket = os.getenv('DB_Bucket')
    DB_Organization = os.getenv('DB_Organization')
    DB_Token = os.getenv('DB_Token')

    influxDB = DBManager.InfluxDBmodel(server = 'http://' + DB_IP + ':' +  DB_Port + '/', org = DB_Organization, bucket = DB_Bucket, token = DB_Token)

    connectionState = influxDB.InfluxDBconnection()
    if not connectionState:
        return {"message":influxDB.ERROR_MESSAGE}, 503

    query = '''import "strings"
    from(bucket: "Laboratorio_Energias")
    |> range(start: 0)
    |> filter(fn: (r) => r["_measurement"] == "''' + measurement + '''")
    |> filter(fn: (r) => r["device"] == "entrenamiento")
    |> filter(fn: (r) => strings.containsStr(v: r._field, substr: "''' + method + '''"))
    |> filter(fn: (r) => strings.containsStr(v: r._field, substr: "''' + model + '''"))
    |> last()'''
    
    attempts = 1
    while attempts <= 5:
      try:
        values_df_temp = influxDB.InfluxDBreader(query)
        values_df_temp['name'] = values_df_temp['_field'].str.split('?').str[-1]
        values_df_temp['var'] = values_df_temp['_field'].str.split('?').str[-2]

        values = values_df_temp.pivot(index='name', columns='var', values='_value').to_dict(orient='index')
        trainingData = json.dumps({'names': list(values.keys()), 'values': values}, indent=1)
        
        influxDB.InfluxDBclose()
        break
      except:
        attempts += 1
      finally:
        influxDB.InfluxDBclose()

    return trainingData

  def post(self):
    data = request.get_json()
    bmp_output = {}
    # print(data)

    #Database parameters
    DB_IP = os.getenv('DB_IP')
    DB_Port = os.getenv('DB_Port')
    DB_Bucket = os.getenv('DB_Bucket')
    DB_Organization = os.getenv('DB_Organization')
    DB_Token = os.getenv('DB_Token')

    #Global twin
    name = data["name"]
    #TrainingMode = True
    TrainingMode = data["trainingMode"]
    iteration = data["iteration"]

    # SideA 
    # Operational Conditions
    StateSideA = data["isSideAOn"]                               #True: Turning on, Fals: Truning off
    stateSelectionSideA = data["stateSelection"]            #False: Online, True: offline
    measurementMethodSideA =  data["measurementMethodSideA"]     #"Pressure, VolumeDisplaced"
    ReactorVolumeSideA = data["rxnVolumeSideA"]["value"]         #Reactor Volume (mL)   
    InitialFreeVolumeSideA = data["freeVolumeSideA"]["value"]    #Free volume (mL)
    ModelSideA = data["modelSelectionSideA"]                     #Arrhenius, Gompertz, ADM1
    time_stepSideA = data["digitalTwinStepTime"]["value"]                   #Time step, seconds 
    speed_time = data["timeMultiplier"]["value"]

    #Model parameters
    KSideA = data["kineticKSideA"]["value"]
    EaSideA = data["kineticEaSideA"]["value"]
    LSideA = data["kineticLambdaSideA"]["value"]
   
    #Mixing
    MixManualSideA = data["mixManualSideA"]                      #True: manual, False:Auto
    MixVelocitySideA = data["mixVelocitySideA"]["value"]
    mixTimeSideA = data["mixTimeSideA"]["value"] 
    mixDailySideA = data["mixDailySideA"]["value"] 

    #Temperature control
    TemperatureManualSideA = data["TemperatureSideA"]["disabled"]
    TemperatureSideA = data["TemperatureSideA"]["value"]

    #pHControl
    pHManualSideA = data["pHSideA"]["disabled"]
    pHSideA = data["pHSideA"]["value"]

    #pressure control
    pressureSetPointSideA = data["pressureSetPointSideA"]["value"]

    #biogas compositions
    #R101
    xCH4R101 = data["methaneR101"]["value"]
    xCO2R101 = data["carbonDioxideR101"]["value"]
    xO2R101 = data["oxygenR101"]["value"]
    xH2SR101 = data["sulfurHydrogenR101"]["value"]
    xH2R101 = data["hydrogenR101"]["value"]
    #R102
    xCH4R102 = data["methaneR102"]["value"]
    xCO2R102 = data["carbonDioxideR102"]["value"]
    xO2R102 = data["oxygenR102"]["value"]
    xH2SR102 = data["sulfurHydrogenR102"]["value"]
    xH2R102 = data["hydrogenR102"]["value"]
    #R103
    xCH4R103 = data["methaneR103"]["value"]
    xCO2R103 = data["carbonDioxideR103"]["value"]
    xO2R103 = data["oxygenR103"]["value"]
    xH2SR103 = data["sulfurHydrogenR103"]["value"]
    xH2R103 = data["hydrogenR103"]["value"]
    #R104
    xCH4R104 = data["methaneR104"]["value"]
    xCO2R104 = data["carbonDioxideR104"]["value"]
    xO2R104 = data["oxygenR104"]["value"]
    xH2SR104 = data["sulfurHydrogenR104"]["value"]
    xH2R104 = data["hydrogenR104"]["value"]
    #R105
    xCH4R105 = data["methaneR105"]["value"]
    xCO2R105 = data["carbonDioxideR105"]["value"]
    xO2R105 = data["oxygenR105"]["value"]
    xH2SR105 = data["sulfurHydrogenR105"]["value"]
    xH2R105 = data["hydrogenR105"]["value"]

    #Initial conditions for substrate
    SubstrateNumberSideA = data["amountOfSubstratesSideA"]["value"]   #Substrate number
    MixRuleSideA = data["mixRuleSideA"]                               #Fraction, Volume, Weight

    #Estimation by fraction
    Fraction1SideA = data["substrate1CompositionSideA"]["value"]      #These could be Fraction, Volume or weight depending of mix rules
    Fraction2SideA = data["substrate2CompositionSideA"]["value"]
    Fraction3SideA = data["substrate3CompositionSideA"]["value"]
    Fraction4SideA = data["substrate4CompositionSideA"]["value"]
    WaterFractionSideA = data["waterCompositionSideA"]["value"]

    #Substrate 1 properties
    ST1SideA = data["totalSolidsSubstrate1SideA"]["value"]
    SV1SideA = data["volatileSolidsSubstrate1SIdeA"]["value"]
    rho1SideA = data["densitySubstrate1SideA"]["value"]
    Cc1SideA = data["carbonContentSubstrate1SideA"]["value"]
    Ch1SideA = data["hydrogenContentSubstrate1SideA"]["value"]
    Co1SideA = data["oxygenContentSubstrate1SideA"]["value"]
    Cn1SideA = data["nitrogenContentSubstrate1SideA"]["value"]
    Cs1SideA = data["sulfurContentSubstrate1SideA"]["value"]
    
    #Substrate 2 properties
    ST2SideA = data["totalSolidsSubstrate2SideA"]["value"]
    SV2SideA = data["volatileSolidsSubstrate2SideA"]["value"]
    rho2SideA = data["densitySubstrate2SideA"]["value"]
    Cc2SideA = data["carbonContentSubstrate2SideA"]["value"]
    Ch2SideA = data["hydrogenContentSubstrate2SideA"]["value"]
    Co2SideA = data["oxygenContentSubstrate2SideA"]["value"]
    Cn2SideA = data["nitrogenContentSubstrate2SideA"]["value"]
    Cs2SideA = data["sulfurContentSubstrate2SideA"]["value"]

    #Substrate 3 properties
    ST3SideA = data["totalSolidsSubstrate3SideA"]["value"]
    SV3SideA = data["volatileSolidsSubstrate3SideA"]["value"]
    rho3SideA = data["densitySubstrate3SideA"]["value"]
    Cc3SideA = data["carbonContentSubstrate3SideA"]["value"]
    Ch3SideA = data["hydrogenContentSubstrate3SideA"]["value"]
    Co3SideA = data["oxygenContentSubstrate3SideA"]["value"]
    Cn3SideA = data["nitrogenContentSubstrate3SideA"]["value"]
    Cs3SideA = data["sulfurContentSubstrate3SideA"]["value"]

    #Substrate 4 properties
    ST4SideA = data["totalSolidsSubstrate4SideA"]["value"]
    SV4SideA = data["volatileSolidsSubstrate4SIdeA"]["value"]
    rho4SideA = data["densitySubstrate4SideA"]["value"]
    Cc4SideA = data["carbonContentSubstrate4SideA"]["value"]
    Ch4SideA = data["hydrogenContentSubstrate4SideA"]["value"]
    Co4SideA = data["oxygenContentSubstrate4SideA"]["value"]
    Cn4SideA = data["nitrogenContentSubstrate4SideA"]["value"]
    Cs4SideA = data["sulfurContentSubstrate4SideA"]["value"]

    #Biogas compositions Manually
    biogasSideA = data["manualBiogasCompositionSideA"]            #False: Auto, True: Manual
       
    #Operation Method
    OperationMethodSideA = data["dosificationTypeSideA"]                  #NoDosing, Time, Injection
    dosificationVolumeSideA = data["dosificationVolumeSideA"]["value"]
    dailyInyectionsSideA = data["dailyInyectionsSideA"]["value"]
    TrainTimeSideA = data["testDurationSideA"]["value"] 
    TrainTimeSideA = TrainTimeSideA * 24 * 60                               #trnasform days into minutes

    # SideB 
    # Operational Conditions
    StateSideB = data["isSideBOn"]                               #True: Turning on, Fals: Truning off
    stateSelectionSideB = data["stateSelection"]            #False: Online, True: offline
    measurementMethodSideB =  data["measurementMethodSideB"]     #"Pressure, VolumeDisplaced"
    ReactorVolumeSideB = data["rxnVolumeSideB"]["value"]         #Reactor Volume (mL)   
    InitialFreeVolumeSideB = data["freeVolumeSideB"]["value"]    #Free volume (mL)
    ModelSideB = data["modelSelectionSideB"]                     #Arrhenius, Gompertz, ADM1
    time_stepSideB = data["digitalTwinStepTime"]["value"]                   #Time step, seconds 
    speed_time = data["timeMultiplier"]["value"]

    #Model parameters
    KSideB = data["kineticKSideB"]["value"]
    EaSideB = data["kineticEaSideB"]["value"]
    LSideB = data["kineticLambdaSideB"]["value"]
   
    #Mixing
    MixManualSideB = data["mixManualSideB"]                      #True: manual, False:Auto
    MixVelocitySideB = data["mixVelocitySideB"]["value"]
    mixTimeSideB = data["mixTimeSideB"]["value"] 
    mixDailySideB = data["mixDailySideB"]["value"] 

    #Temperature control
    TemperatureManualSideB = data["TemperatureSideB"]["disabled"]
    TemperatureSideB = data["TemperatureSideB"]["value"]

    #pHControl
    pHManualSideB = data["pHSideB"]["disabled"]
    pHSideB = data["pHSideB"]["value"]

    #pressure control
    pressureSetPointSideB = data["pressureSetPointSideB"]["value"]

    #biogas compositions
    #R101
    xCH4R101 = data["methaneR101"]["value"]
    xCO2R101 = data["carbonDioxideR101"]["value"]
    xO2R101 = data["oxygenR101"]["value"]
    xH2SR101 = data["sulfurHydrogenR101"]["value"]
    xH2R101 = data["hydrogenR101"]["value"]
    #R102
    xCH4R102 = data["methaneR102"]["value"]
    xCO2R102 = data["carbonDioxideR102"]["value"]
    xO2R102 = data["oxygenR102"]["value"]
    xH2SR102 = data["sulfurHydrogenR102"]["value"]
    xH2R102 = data["hydrogenR102"]["value"]
    #R103
    xCH4R103 = data["methaneR103"]["value"]
    xCO2R103 = data["carbonDioxideR103"]["value"]
    xO2R103 = data["oxygenR103"]["value"]
    xH2SR103 = data["sulfurHydrogenR103"]["value"]
    xH2R103 = data["hydrogenR103"]["value"]
    #R104
    xCH4R104 = data["methaneR104"]["value"]
    xCO2R104 = data["carbonDioxideR104"]["value"]
    xO2R104 = data["oxygenR104"]["value"]
    xH2SR104 = data["sulfurHydrogenR104"]["value"]
    xH2R104 = data["hydrogenR104"]["value"]
    #R105
    xCH4R105 = data["methaneR105"]["value"]
    xCO2R105 = data["carbonDioxideR105"]["value"]
    xO2R105 = data["oxygenR105"]["value"]
    xH2SR105 = data["sulfurHydrogenR105"]["value"]
    xH2R105 = data["hydrogenR105"]["value"]

    #Initial conditions for substrate
    SubstrateNumberSideB = data["amountOfSubstratesSideB"]["value"]   #Substrate number
    MixRuleSideB = data["mixRuleSideB"]                               #Fraction, Volume, Weight

    #Estimation by fraction
    Fraction1SideB = data["substrate1CompositionSideB"]["value"]      #These could be Fraction, Volume or weight depending of mix rules
    Fraction2SideB = data["substrate2CompositionSideB"]["value"]
    Fraction3SideB = data["substrate3CompositionSideB"]["value"]
    Fraction4SideB = data["substrate4CompositionSideB"]["value"]
    WaterFractionSideB = data["waterCompositionSideB"]["value"]

    #Substrate 1 properties
    ST1SideB = data["totalSolidsSubstrate1SideB"]["value"]
    SV1SideB = data["volatileSolidsSubstrate1SideB"]["value"]
    rho1SideB = data["densitySubstrate1SideB"]["value"]
    Cc1SideB = data["carbonContentSubstrate1SideB"]["value"]
    Ch1SideB = data["hydrogenContentSubstrate1SideB"]["value"]
    Co1SideB = data["oxygenContentSubstrate1SideB"]["value"]
    Cn1SideB = data["nitrogenContentSubstrate1SideB"]["value"]
    Cs1SideB = data["sulfurContentSubstrate1SideB"]["value"]
    
    #Substrate 2 properties
    ST2SideB = data["totalSolidsSubstrate2SideB"]["value"]
    SV2SideB = data["volatileSolidsSubstrate2SideB"]["value"]
    rho2SideB = data["densitySubstrate2SideB"]["value"]
    Cc2SideB = data["carbonContentSubstrate2SideB"]["value"]
    Ch2SideB = data["hydrogenContentSubstrate2SideB"]["value"]
    Co2SideB = data["oxygenContentSubstrate2SideB"]["value"]
    Cn2SideB = data["nitrogenContentSubstrate2SideB"]["value"]
    Cs2SideB = data["sulfurContentSubstrate2SideB"]["value"]

    #Substrate 3 properties
    ST3SideB = data["totalSolidsSubstrate3SideB"]["value"]
    SV3SideB = data["volatileSolidsSubstrate3SideB"]["value"]
    rho3SideB = data["densitySubstrate3SideB"]["value"]
    Cc3SideB = data["carbonContentSubstrate3SideB"]["value"]
    Ch3SideB = data["hydrogenContentSubstrate3SideB"]["value"]
    Co3SideB = data["oxygenContentSubstrate3SideB"]["value"]
    Cn3SideB = data["nitrogenContentSubstrate3SideB"]["value"]
    Cs3SideB = data["sulfurContentSubstrate3SideB"]["value"]

    #Substrate 4 properties
    ST4SideB = data["totalSolidsSubstrate4SideB"]["value"]
    SV4SideB = data["volatileSolidsSubstrate4SideB"]["value"]
    rho4SideB = data["densitySubstrate4SideB"]["value"]
    Cc4SideB = data["carbonContentSubstrate4SideB"]["value"]
    Ch4SideB = data["hydrogenContentSubstrate4SideB"]["value"]
    Co4SideB = data["oxygenContentSubstrate4SideB"]["value"]
    Cn4SideB = data["nitrogenContentSubstrate4SideB"]["value"]
    Cs4SideB = data["sulfurContentSubstrate4SideB"]["value"]

    #Biogas compositions Manually
    biogasSideB = data["manualBiogasCompositionSideB"]            #False: Auto, True: Manual
       
    #Operation Method
    OperationMethodSideB = data["dosificationTypeSideB"]                  #NoDosing, Time, Injection
    dosificationVolumeSideB = data["dosificationVolumeSideB"]["value"]
    dailyInyectionsSideB = data["dailyInyectionsSideB"]["value"]
    TrainTimeSideB = data["testDurationSideB"]["value"] 
    TrainTimeSideB = TrainTimeSideB * 24 * 60                               #trnasform days into minutes
    

    #%% ---- Side A - Working
    if StateSideA == True:
      user_idSideA = name + "SideA"
      user_data_sideA = name + "DataSideA"

      user_instances_SideA = [user_idSideA]
      data_instances_SideA = [user_data_sideA]
    
      if iteration == 1:   
          for key in user_instances_SideA:
            if key in bmp_instancesSideA:
              del bmp_instancesSideA[key]  
      
      if iteration == 1:
        for key in data_instances_SideA:
          if key in data_instancesSideA:
            del data_instancesSideA[key]       

      #%% Online mode with Training and getting data from interface
      if stateSelectionSideA == False and biogasSideA == False and TrainingMode == True:    #Online, biogas compounds in auto
        
        if user_idSideA not in bmp_instancesSideA:
          bmp_instancesSideA[user_idSideA] = BMPOnlineTrainMode.BMP_online(DB_IP= DB_IP, DB_Port=DB_Port, DB_Organization=DB_Organization, DB_Bucket=DB_Bucket, DB_Token=DB_Token, 
                                                                      MeasureMethod=measurementMethodSideA, ReactorVolume=ReactorVolumeSideA, InitialFreeVolume=InitialFreeVolumeSideA, 
                                                                      SubstrateNumber=SubstrateNumberSideA, MixRule=MixRuleSideA,
                                                                      Fraction1=Fraction1SideA, Fraction2=Fraction2SideA, Fraction3=Fraction3SideA, Fraction4=Fraction4SideA, WaterFraction=WaterFractionSideA,
                                                                      Volume1=Fraction1SideA, Volume2=Fraction2SideA, Volume3=Fraction3SideA, Volume4=Fraction4SideA, WaterVolume=WaterFractionSideA, 
                                                                      Weight1=Fraction1SideA, Weight2=Fraction2SideA, Weight3=Fraction3SideA, Weight4=Fraction4SideA, WaterWeight=WaterFractionSideA,
                                                                      ST1=ST1SideA, SV1=SV1SideA, rho1=rho1SideA, Cc1=Cc1SideA, Ch1=Ch1SideA, Co1=Co1SideA,Cn1=Cn1SideA, Cs1=Cs1SideA,
                                                                      ST2=ST2SideA, SV2=SV2SideA, rho2=rho2SideA, Cc2=Cc2SideA, Ch2=Ch2SideA, Co2=Co2SideA,Cn2=Cn2SideA, Cs2=Cs2SideA,
                                                                      ST3=ST3SideA, SV3=SV3SideA, rho3=rho3SideA, Cc3=Cc3SideA, Ch3=Ch3SideA, Co3=Co3SideA,Cn3=Cn3SideA, Cs3=Cs3SideA,
                                                                      ST4=ST4SideA, SV4=SV4SideA, rho4=rho4SideA, Cc4=Cc4SideA, Ch4=Ch4SideA, Co4=Co4SideA,Cn4=Cn4SideA, Cs4=Cs4SideA,
                                                                      OperationMethod = OperationMethodSideA, Model=ModelSideA)

        SideA = bmp_instancesSideA[user_idSideA]
        if user_data_sideA not in data_instancesSideA:
          SideA.GetData(SideA=True, SideB=False, TrainTime=TrainTimeSideA)
          DataSideA = SideA.PlantSideA
          DataInterfaz = SideA.PlantEstimation
          SideA.ProcessData(SideA = True, SideB = False, MeasureMethodSideA = measurementMethodSideA, MeasureMethodSideB = measurementMethodSideA, DataPlantSideA = DataSideA, DataPlantSideB = DataSideA,  
                           DataEstimation = DataInterfaz, OperationMethod = OperationMethodSideA)
          R101_data = SideA.R101_data
          R102_data = SideA.R102_data
          R103_data = SideA.R103_data
          R104_data = SideA.R104_data
          R105_data = SideA.R105_data
          if SideA.OperationMethod in ["Time", "Injection"]:
            SideA.SubstrateFeeding()
          
          R101 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R101", ReactorData = R101_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
          R102 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R102", ReactorData = R102_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
          R103 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R103", ReactorData = R103_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
          R104 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R104", ReactorData = R104_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
          R105 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R105", ReactorData = R105_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
          data_instancesSideA[user_data_sideA] = [R101, R102, R103, R104, R105]
        
        R101_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R101", ReactorData = data_instancesSideA[user_data_sideA][0], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        R102_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R102", ReactorData = data_instancesSideA[user_data_sideA][1], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        R103_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R103", ReactorData = data_instancesSideA[user_data_sideA][2], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        R104_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R104", ReactorData = data_instancesSideA[user_data_sideA][3], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        R105_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R105", ReactorData = data_instancesSideA[user_data_sideA][4], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        
        R101_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R101", ReactorData = data_instancesSideA[user_data_sideA][0], Vrxn = ReactorVolumeSideA)
        R102_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R102", ReactorData = data_instancesSideA[user_data_sideA][1], Vrxn = ReactorVolumeSideA)
        R103_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R103", ReactorData = data_instancesSideA[user_data_sideA][2], Vrxn = ReactorVolumeSideA)
        R104_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R104", ReactorData = data_instancesSideA[user_data_sideA][3], Vrxn = ReactorVolumeSideA)
        R105_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R105", ReactorData = data_instancesSideA[user_data_sideA][4], Vrxn = ReactorVolumeSideA)
        #Output variables
        #R101
        bmp_output["mixVelocityR101"] = float(R101_exit[0]) 
        bmp_output["SVR101"] = float(R101_exit[1])
        bmp_output["OCR101"] = float(R101_exit[2])
        bmp_output["STR101"] = float(R101_exit[3])
        bmp_output["XR101"] = float(R101_exit[4])
        bmp_output["PBMR101"] = float(R101_exit[5])
        bmp_output["KR101"] = float(R101_opt[0]/60)
        bmp_output["EaR101"] = float(R101_opt[1])
        bmp_output["lambdaR101"] = float(R101_opt[2])
        bmp_output["Objetive"] = float(R101_opt[3])
        bmp_output["TempR101"] = float(R101_exit[6])  
        bmp_output["pHR101"] = float(R101_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR101"] =float(R101_exit[8])
        bmp_output["carbondioxidemolR101"] = float(R101_exit[9])
        bmp_output["oxygenmolR101"] = float(R101_exit[10])
        bmp_output["hydrogensulfurmolR101"] = float(R101_exit[11])
        bmp_output["hydrogenmolR101"] = float(R101_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR101"] = float(R101_exit[13])
        bmp_output["carbondioxideconcentrationR101"] = float(R101_exit[14])
        bmp_output["oxygenconcentrationR101"] = float(R101_exit[15])
        bmp_output["hydrogensulfurconcentrationR101"] = float(R101_exit[16])
        bmp_output["hydrogenconcentrationR101"] = float(R101_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR101"] = float(R101_exit[18])
        bmp_output["carbondioxidevolR101"] = float(R101_exit[19])
        bmp_output["oxygenvolR101"] = float(R101_exit[20])
        bmp_output["hydrogensulfurvolR101"] = float(R101_exit[21])
        bmp_output["hydrogenvolR101"] = float(R101_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR101"] = float(R101_exit[23])
        bmp_output["storagebiogaspressureR101"] = float(R101_exit[24])
        bmp_output["storagebiogasR101"] = float(R101_exit[25])
        bmp_output["accumbiogasR101"] = float(R101_exit[26])
        bmp_output["EnergyR101"] = float(R101_exit[27])
        bmp_output["LHVR101"] = float(R101_exit[28])

        #R102
        bmp_output["mixVelocityR102"] = float(R102_exit[0]) 
        bmp_output["SVR102"] = float(R102_exit[1])
        bmp_output["OCR102"] = float(R102_exit[2])
        bmp_output["STR102"] = float(R102_exit[3])
        bmp_output["XR102"] = float(R102_exit[4])
        bmp_output["PBMR102"] = float(R102_exit[5])
        bmp_output["KR102"] = float(R102_opt[0]/60)
        bmp_output["EaR102"] = float(R102_opt[1])
        bmp_output["lambdaR102"] = float(R102_opt[2])
        bmp_output["Objetive"] = float(R102_opt[3])
        bmp_output["TempR102"] = float(R102_exit[6])  
        bmp_output["pHR102"] = float(R102_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR102"] =float(R102_exit[8])
        bmp_output["carbondioxidemolR102"] = float(R102_exit[9])
        bmp_output["oxygenmolR102"] = float(R102_exit[10])
        bmp_output["hydrogensulfurmolR102"] = float(R102_exit[11])
        bmp_output["hydrogenmolR102"] = float(R102_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR102"] = float(R102_exit[13])
        bmp_output["carbondioxideconcentrationR102"] = float(R102_exit[14])
        bmp_output["oxygenconcentrationR102"] = float(R102_exit[15])
        bmp_output["hydrogensulfurconcentrationR102"] = float(R102_exit[16])
        bmp_output["hydrogenconcentrationR102"] = float(R102_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR102"] = float(R102_exit[18])
        bmp_output["carbondioxidevolR102"] = float(R102_exit[19])
        bmp_output["oxygenvolR102"] = float(R102_exit[20])
        bmp_output["hydrogensulfurvolR102"] = float(R102_exit[21])
        bmp_output["hydrogenvolR102"] = float(R102_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR102"] = float(R102_exit[23])
        bmp_output["storagebiogaspressureR102"] = float(R102_exit[24])
        bmp_output["storagebiogasR102"] = float(R102_exit[25])
        bmp_output["accumbiogasR102"] = float(R102_exit[26])
        bmp_output["EnergyR102"] = float(R102_exit[27])
        bmp_output["LHVR102"] = float(R102_exit[28])

        #R103
        bmp_output["mixVelocityR103"] = float(R103_exit[0]) 
        bmp_output["SVR103"] = float(R103_exit[1])
        bmp_output["OCR103"] = float(R103_exit[2])
        bmp_output["STR103"] = float(R103_exit[3])
        bmp_output["XR103"] = float(R103_exit[4])
        bmp_output["PBMR103"] = float(R103_exit[5])
        bmp_output["KR103"] = float(R103_opt[0]/60)
        bmp_output["EaR103"] = float(R103_opt[1])
        bmp_output["lambdaR103"] = float(R103_opt[2])
        bmp_output["Objetive"] = float(R103_opt[3])
        bmp_output["TempR103"] = float(R103_exit[6])  
        bmp_output["pHR103"] = float(R103_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR103"] =float(R103_exit[8])
        bmp_output["carbondioxidemolR103"] = float(R103_exit[9])
        bmp_output["oxygenmolR103"] = float(R103_exit[10])
        bmp_output["hydrogensulfurmolR103"] = float(R103_exit[11])
        bmp_output["hydrogenmolR103"] = float(R103_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR103"] = float(R103_exit[13])
        bmp_output["carbondioxideconcentrationR103"] = float(R103_exit[14])
        bmp_output["oxygenconcentrationR103"] = float(R103_exit[15])
        bmp_output["hydrogensulfurconcentrationR103"] = float(R103_exit[16])
        bmp_output["hydrogenconcentrationR103"] = float(R103_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR103"] = float(R103_exit[18])
        bmp_output["carbondioxidevolR103"] = float(R103_exit[19])
        bmp_output["oxygenvolR103"] = float(R103_exit[20])
        bmp_output["hydrogensulfurvolR103"] = float(R103_exit[21])
        bmp_output["hydrogenvolR103"] = float(R103_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR103"] = float(R103_exit[23])
        bmp_output["storagebiogaspressureR103"] = float(R103_exit[24])
        bmp_output["storagebiogasR103"] = float(R103_exit[25])
        bmp_output["accumbiogasR103"] = float(R103_exit[26])
        bmp_output["EnergyR103"] = float(R103_exit[27])
        bmp_output["LHVR103"] = float(R103_exit[28])

        #R104
        bmp_output["mixVelocityR104"] = float(R104_exit[0]) 
        bmp_output["SVR104"] = float(R104_exit[1])
        bmp_output["OCR104"] = float(R104_exit[2])
        bmp_output["STR104"] = float(R104_exit[3])
        bmp_output["XR104"] = float(R104_exit[4])
        bmp_output["PBMR104"] = float(R104_exit[5])
        bmp_output["KR104"] = float(R104_opt[0]/60)
        bmp_output["EaR104"] = float(R104_opt[1])
        bmp_output["lambdaR104"] = float(R104_opt[2])
        bmp_output["Objetive"] = float(R104_opt[3])
        bmp_output["TempR104"] = float(R104_exit[6])  
        bmp_output["pHR104"] = float(R104_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR104"] =float(R104_exit[8])
        bmp_output["carbondioxidemolR104"] = float(R104_exit[9])
        bmp_output["oxygenmolR104"] = float(R104_exit[10])
        bmp_output["hydrogensulfurmolR104"] = float(R104_exit[11])
        bmp_output["hydrogenmolR104"] = float(R104_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR104"] = float(R104_exit[13])
        bmp_output["carbondioxideconcentrationR104"] = float(R104_exit[14])
        bmp_output["oxygenconcentrationR104"] = float(R104_exit[15])
        bmp_output["hydrogensulfurconcentrationR104"] = float(R104_exit[16])
        bmp_output["hydrogenconcentrationR104"] = float(R104_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR104"] = float(R104_exit[18])
        bmp_output["carbondioxidevolR104"] = float(R104_exit[19])
        bmp_output["oxygenvolR104"] = float(R104_exit[20])
        bmp_output["hydrogensulfurvolR104"] = float(R104_exit[21])
        bmp_output["hydrogenvolR104"] = float(R104_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR104"] = float(R104_exit[23])
        bmp_output["storagebiogaspressureR104"] = float(R104_exit[24])
        bmp_output["storagebiogasR104"] = float(R104_exit[25])
        bmp_output["accumbiogasR104"] = float(R104_exit[26])
        bmp_output["EnergyR104"] = float(R104_exit[27])
        bmp_output["LHVR104"] = float(R104_exit[28])

        #R105
        bmp_output["mixVelocityR105"] = float(R105_exit[0]) 
        bmp_output["SVR105"] = float(R105_exit[1])
        bmp_output["OCR105"] = float(R105_exit[2])
        bmp_output["STR105"] = float(R105_exit[3])
        bmp_output["XR105"] = float(R105_exit[4])
        bmp_output["PBMR105"] = float(R105_exit[5])
        bmp_output["KR105"] = float(R105_opt[0]/60)
        bmp_output["EaR105"] = float(R105_opt[1])
        bmp_output["lambdaR105"] = float(R105_opt[2])
        bmp_output["Objetive"] = float(R105_opt[3])
        bmp_output["TempR105"] = float(R105_exit[6])  
        bmp_output["pHR105"] = float(R105_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR105"] =float(R105_exit[8])
        bmp_output["carbondioxidemolR105"] = float(R105_exit[9])
        bmp_output["oxygenmolR105"] = float(R105_exit[10])
        bmp_output["hydrogensulfurmolR105"] = float(R105_exit[11])
        bmp_output["hydrogenmolR105"] = float(R105_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR105"] = float(R105_exit[13])
        bmp_output["carbondioxideconcentrationR105"] = float(R105_exit[14])
        bmp_output["oxygenconcentrationR105"] = float(R105_exit[15])
        bmp_output["hydrogensulfurconcentrationR105"] = float(R105_exit[16])
        bmp_output["hydrogenconcentrationR105"] = float(R105_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR105"] = float(R105_exit[18])
        bmp_output["carbondioxidevolR105"] = float(R105_exit[19])
        bmp_output["oxygenvolR105"] = float(R105_exit[20])
        bmp_output["hydrogensulfurvolR105"] = float(R105_exit[21])
        bmp_output["hydrogenvolR105"] = float(R105_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR105"] = float(R105_exit[23])
        bmp_output["storagebiogaspressureR105"] = float(R105_exit[24])
        bmp_output["storagebiogasR105"] = float(R105_exit[25])
        bmp_output["accumbiogasR105"] = float(R105_exit[26])
        bmp_output["EnergyR105"] = float(R105_exit[27])
        bmp_output["LHVR105"] = float(R105_exit[28])
        

      #%% Online Mode without training (just show the values from plant) without income from manual interface
      elif stateSelectionSideA == False and biogasSideA == True and TrainingMode == True:    #online with manual entrance of biogas compositions
        
        if user_idSideA not in bmp_instancesSideA:
          bmp_instancesSideA[user_idSideA] = BMPOnlineTrainMode.BMP_online(DB_IP= DB_IP, DB_Port=DB_Port, DB_Organization=DB_Organization, DB_Bucket=DB_Bucket, DB_Token=DB_Token, 
                                                                      MeasureMethod=measurementMethodSideA, ReactorVolume=ReactorVolumeSideA, InitialFreeVolume=InitialFreeVolumeSideA, 
                                                                      SubstrateNumber=SubstrateNumberSideA, MixRule=MixRuleSideA,
                                                                      Fraction1=Fraction1SideA, Fraction2=Fraction2SideA, Fraction3=Fraction3SideA, Fraction4=Fraction4SideA, WaterFraction=WaterFractionSideA,
                                                                      Volume1=Fraction1SideA, Volume2=Fraction2SideA, Volume3=Fraction3SideA, Volume4=Fraction4SideA, WaterVolume=WaterFractionSideA, 
                                                                      Weight1=Fraction1SideA, Weight2=Fraction2SideA, Weight3=Fraction3SideA, Weight4=Fraction4SideA, WaterWeight=WaterFractionSideA,
                                                                      ST1=ST1SideA, SV1=SV1SideA, rho1=rho1SideA, Cc1=Cc1SideA, Ch1=Ch1SideA, Co1=Co1SideA,Cn1=Cn1SideA, Cs1=Cs1SideA,
                                                                      ST2=ST2SideA, SV2=SV2SideA, rho2=rho2SideA, Cc2=Cc2SideA, Ch2=Ch2SideA, Co2=Co2SideA,Cn2=Cn2SideA, Cs2=Cs2SideA,
                                                                      ST3=ST3SideA, SV3=SV3SideA, rho3=rho3SideA, Cc3=Cc3SideA, Ch3=Ch3SideA, Co3=Co3SideA,Cn3=Cn3SideA, Cs3=Cs3SideA,
                                                                      ST4=ST4SideA, SV4=SV4SideA, rho4=rho4SideA, Cc4=Cc4SideA, Ch4=Ch4SideA, Co4=Co4SideA,Cn4=Cn4SideA, Cs4=Cs4SideA,
                                                                      OperationMethod = OperationMethodSideA, Model=ModelSideA)
      
        SideA = bmp_instancesSideA[user_idSideA]
        if user_data_sideA not in data_instances_SideA:
          SideA.GetData(SideA=True, SideB=False, TrainTime=TrainTimeSideA)
          DataSideA = SideA.PlantSideA
          DataInterfaz = SideA.PlantEstimation
          SideA.ProcessData(SideA = True, SideB = False, MeasureMethodSideA = measurementMethodSideA, MeasureMethodSideB = measurementMethodSideA, DataPlantSideA = DataSideA, DataPlantSideB = DataSideA,  
                           DataEstimation = DataInterfaz, OperationMethod = OperationMethodSideA)
          R101_data = SideA.R101_data
          R102_data = SideA.R102_data
          R103_data = SideA.R103_data
          R104_data = SideA.R104_data
          R105_data = SideA.R105_data
          if SideA.OperationMethod in ["Time", "Injection"]:
            SideA.SubstrateFeeding()
          
          if SideA.OperationMethod in ["Time", "Injection"]:
            SideA.SubstrateFeeding()
          
          R101 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R101", ReactorData = R101_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R101, xCO2=xCO2R101, xO2=xO2R101, xH2S=xH2SR101, XH2=xH2R101)
          R102 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R102", ReactorData = R102_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R102, xCO2=xCO2R102, xO2=xO2R102, xH2S=xH2SR102, XH2=xH2R102)
          R103 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R103", ReactorData = R103_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R103, xCO2=xCO2R103, xO2=xO2R103, xH2S=xH2SR103, XH2=xH2R103)
          R104 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R104", ReactorData = R104_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R104, xCO2=xCO2R104, xO2=xO2R104, xH2S=xH2SR104, XH2=xH2R104)
          R105 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R105", ReactorData = R105_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R105, xCO2=xCO2R105, xO2=xO2R105, xH2S=xH2SR105, XH2=xH2R105)
          data_instances_SideA[user_data_sideA] = [R101, R102, R103, R104, R105]
        
        R101_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R101", ReactorData = data_instances_SideA[user_data_sideA][0], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        R102_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R102", ReactorData = data_instances_SideA[user_data_sideA][1], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        R103_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R103", ReactorData = data_instances_SideA[user_data_sideA][2], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        R104_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R104", ReactorData = data_instances_SideA[user_data_sideA][3], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        R105_opt = SideA.ReactorOptimization(Model = ModelSideA, iterations_counts = iteration, Reactorname = "R105", ReactorData = data_instances_SideA[user_data_sideA][4], ReactorVolume = ReactorVolumeSideA, OperationMethod = OperationMethodSideA)
        
        R101_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R101", ReactorData = data_instances_SideA[user_data_sideA][0], Vrxn = ReactorVolumeSideA)
        R102_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R102", ReactorData = data_instances_SideA[user_data_sideA][1], Vrxn = ReactorVolumeSideA)
        R103_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R103", ReactorData = data_instances_SideA[user_data_sideA][2], Vrxn = ReactorVolumeSideA)
        R104_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R104", ReactorData = data_instances_SideA[user_data_sideA][3], Vrxn = ReactorVolumeSideA)
        R105_exit = SideA.exit_variable_training (iterations_counts = iteration, ReactorName = "R105", ReactorData = data_instances_SideA[user_data_sideA][4], Vrxn = ReactorVolumeSideA)
        #Output variables
        #R101
        bmp_output["mixVelocityR101"] = float(R101_exit[0]) 
        bmp_output["SVR101"] = float(R101_exit[1])
        bmp_output["OCR101"] = float(R101_exit[2])
        bmp_output["STR101"] = float(R101_exit[3])
        bmp_output["XR101"] = float(R101_exit[4])
        bmp_output["PBMR101"] = float(R101_exit[5])
        bmp_output["KR101"] = float(R101_opt[0]/60)
        bmp_output["EaR101"] = float(R101_opt[1])
        bmp_output["lambdaR101"] = float(R101_opt[2])
        bmp_output["Objetive"] = float(R101_opt[3])
        bmp_output["TempR101"] = float(R101_exit[6])  
        bmp_output["pHR101"] = float(R101_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR101"] =float(R101_exit[8])
        bmp_output["carbondioxidemolR101"] = float(R101_exit[9])
        bmp_output["oxygenmolR101"] = float(R101_exit[10])
        bmp_output["hydrogensulfurmolR101"] = float(R101_exit[11])
        bmp_output["hydrogenmolR101"] = float(R101_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR101"] = float(R101_exit[13])
        bmp_output["carbondioxideconcentrationR101"] = float(R101_exit[14])
        bmp_output["oxygenconcentrationR101"] = float(R101_exit[15])
        bmp_output["hydrogensulfurconcentrationR101"] = float(R101_exit[16])
        bmp_output["hydrogenconcentrationR101"] = float(R101_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR101"] = float(R101_exit[18])
        bmp_output["carbondioxidevolR101"] = float(R101_exit[19])
        bmp_output["oxygenvolR101"] = float(R101_exit[20])
        bmp_output["hydrogensulfurvolR101"] = float(R101_exit[21])
        bmp_output["hydrogenvolR101"] = float(R101_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR101"] = float(R101_exit[23])
        bmp_output["storagebiogaspressureR101"] = float(R101_exit[24])
        bmp_output["storagebiogasR101"] = float(R101_exit[25])
        bmp_output["accumbiogasR101"] = float(R101_exit[26])
        bmp_output["EnergyR101"] = float(R101_exit[27])
        bmp_output["LHVR101"] = float(R101_exit[28])

        #R102
        bmp_output["mixVelocityR102"] = float(R102_exit[0]) 
        bmp_output["SVR102"] = float(R102_exit[1])
        bmp_output["OCR102"] = float(R102_exit[2])
        bmp_output["STR102"] = float(R102_exit[3])
        bmp_output["XR102"] = float(R102_exit[4])
        bmp_output["PBMR102"] = float(R102_exit[5])
        bmp_output["KR102"] = float(R102_opt[0]/60)
        bmp_output["EaR102"] = float(R102_opt[1])
        bmp_output["lambdaR102"] = float(R102_opt[2])
        bmp_output["Objetive"] = float(R102_opt[3])
        bmp_output["TempR102"] = float(R102_exit[6])  
        bmp_output["pHR102"] = float(R102_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR102"] =float(R102_exit[8])
        bmp_output["carbondioxidemolR102"] = float(R102_exit[9])
        bmp_output["oxygenmolR102"] = float(R102_exit[10])
        bmp_output["hydrogensulfurmolR102"] = float(R102_exit[11])
        bmp_output["hydrogenmolR102"] = float(R102_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR102"] = float(R102_exit[13])
        bmp_output["carbondioxideconcentrationR102"] = float(R102_exit[14])
        bmp_output["oxygenconcentrationR102"] = float(R102_exit[15])
        bmp_output["hydrogensulfurconcentrationR102"] = float(R102_exit[16])
        bmp_output["hydrogenconcentrationR102"] = float(R102_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR102"] = float(R102_exit[18])
        bmp_output["carbondioxidevolR102"] = float(R102_exit[19])
        bmp_output["oxygenvolR102"] = float(R102_exit[20])
        bmp_output["hydrogensulfurvolR102"] = float(R102_exit[21])
        bmp_output["hydrogenvolR102"] = float(R102_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR102"] = float(R102_exit[23])
        bmp_output["storagebiogaspressureR102"] = float(R102_exit[24])
        bmp_output["storagebiogasR102"] = float(R102_exit[25])
        bmp_output["accumbiogasR102"] = float(R102_exit[26])
        bmp_output["EnergyR102"] = float(R102_exit[27])
        bmp_output["LHVR102"] = float(R102_exit[28])

        #R103
        bmp_output["mixVelocityR103"] = float(R103_exit[0]) 
        bmp_output["SVR103"] = float(R103_exit[1])
        bmp_output["OCR103"] = float(R103_exit[2])
        bmp_output["STR103"] = float(R103_exit[3])
        bmp_output["XR103"] = float(R103_exit[4])
        bmp_output["PBMR103"] = float(R103_exit[5])
        bmp_output["KR103"] = float(R103_opt[0]/60)
        bmp_output["EaR103"] = float(R103_opt[1])
        bmp_output["lambdaR103"] = float(R103_opt[2])
        bmp_output["Objetive"] = float(R103_opt[3])
        bmp_output["TempR103"] = float(R103_exit[6])  
        bmp_output["pHR103"] = float(R103_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR103"] =float(R103_exit[8])
        bmp_output["carbondioxidemolR103"] = float(R103_exit[9])
        bmp_output["oxygenmolR103"] = float(R103_exit[10])
        bmp_output["hydrogensulfurmolR103"] = float(R103_exit[11])
        bmp_output["hydrogenmolR103"] = float(R103_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR103"] = float(R103_exit[13])
        bmp_output["carbondioxideconcentrationR103"] = float(R103_exit[14])
        bmp_output["oxygenconcentrationR103"] = float(R103_exit[15])
        bmp_output["hydrogensulfurconcentrationR103"] = float(R103_exit[16])
        bmp_output["hydrogenconcentrationR103"] = float(R103_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR103"] = float(R103_exit[18])
        bmp_output["carbondioxidevolR103"] = float(R103_exit[19])
        bmp_output["oxygenvolR103"] = float(R103_exit[20])
        bmp_output["hydrogensulfurvolR103"] = float(R103_exit[21])
        bmp_output["hydrogenvolR103"] = float(R103_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR103"] = float(R103_exit[23])
        bmp_output["storagebiogaspressureR103"] = float(R103_exit[24])
        bmp_output["storagebiogasR103"] = float(R103_exit[25])
        bmp_output["accumbiogasR103"] = float(R103_exit[26])
        bmp_output["EnergyR103"] = float(R103_exit[27])
        bmp_output["LHVR103"] = float(R103_exit[28])

        #R104
        bmp_output["mixVelocityR104"] = float(R104_exit[0]) 
        bmp_output["SVR104"] = float(R104_exit[1])
        bmp_output["OCR104"] = float(R104_exit[2])
        bmp_output["STR104"] = float(R104_exit[3])
        bmp_output["XR104"] = float(R104_exit[4])
        bmp_output["PBMR104"] = float(R104_exit[5])
        bmp_output["KR104"] = float(R104_opt[0]/60)
        bmp_output["EaR104"] = float(R104_opt[1])
        bmp_output["lambdaR104"] = float(R104_opt[2])
        bmp_output["Objetive"] = float(R104_opt[3])
        bmp_output["TempR104"] = float(R104_exit[6])  
        bmp_output["pHR104"] = float(R104_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR104"] =float(R104_exit[8])
        bmp_output["carbondioxidemolR104"] = float(R104_exit[9])
        bmp_output["oxygenmolR104"] = float(R104_exit[10])
        bmp_output["hydrogensulfurmolR104"] = float(R104_exit[11])
        bmp_output["hydrogenmolR104"] = float(R104_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR104"] = float(R104_exit[13])
        bmp_output["carbondioxideconcentrationR104"] = float(R104_exit[14])
        bmp_output["oxygenconcentrationR104"] = float(R104_exit[15])
        bmp_output["hydrogensulfurconcentrationR104"] = float(R104_exit[16])
        bmp_output["hydrogenconcentrationR104"] = float(R104_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR104"] = float(R104_exit[18])
        bmp_output["carbondioxidevolR104"] = float(R104_exit[19])
        bmp_output["oxygenvolR104"] = float(R104_exit[20])
        bmp_output["hydrogensulfurvolR104"] = float(R104_exit[21])
        bmp_output["hydrogenvolR104"] = float(R104_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR104"] = float(R104_exit[23])
        bmp_output["storagebiogaspressureR104"] = float(R104_exit[24])
        bmp_output["storagebiogasR104"] = float(R104_exit[25])
        bmp_output["accumbiogasR104"] = float(R104_exit[26])
        bmp_output["EnergyR104"] = float(R104_exit[27])
        bmp_output["LHVR104"] = float(R104_exit[28])

        #R105
        bmp_output["mixVelocityR105"] = float(R105_exit[0]) 
        bmp_output["SVR105"] = float(R105_exit[1])
        bmp_output["OCR105"] = float(R105_exit[2])
        bmp_output["STR105"] = float(R105_exit[3])
        bmp_output["XR105"] = float(R105_exit[4])
        bmp_output["PBMR105"] = float(R105_exit[5])
        bmp_output["KR105"] = float(R105_opt[0]/60)
        bmp_output["EaR105"] = float(R105_opt[1])
        bmp_output["lambdaR105"] = float(R105_opt[2])
        bmp_output["Objetive"] = float(R105_opt[3])
        bmp_output["TempR105"] = float(R105_exit[6])  
        bmp_output["pHR105"] = float(R105_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR105"] =float(R105_exit[8])
        bmp_output["carbondioxidemolR105"] = float(R105_exit[9])
        bmp_output["oxygenmolR105"] = float(R105_exit[10])
        bmp_output["hydrogensulfurmolR105"] = float(R105_exit[11])
        bmp_output["hydrogenmolR105"] = float(R105_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR105"] = float(R105_exit[13])
        bmp_output["carbondioxideconcentrationR105"] = float(R105_exit[14])
        bmp_output["oxygenconcentrationR105"] = float(R105_exit[15])
        bmp_output["hydrogensulfurconcentrationR105"] = float(R105_exit[16])
        bmp_output["hydrogenconcentrationR105"] = float(R105_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR105"] = float(R105_exit[18])
        bmp_output["carbondioxidevolR105"] = float(R105_exit[19])
        bmp_output["oxygenvolR105"] = float(R105_exit[20])
        bmp_output["hydrogensulfurvolR105"] = float(R105_exit[21])
        bmp_output["hydrogenvolR105"] = float(R105_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR105"] = float(R105_exit[23])
        bmp_output["storagebiogaspressureR105"] = float(R105_exit[24])
        bmp_output["storagebiogasR105"] = float(R105_exit[25])
        bmp_output["accumbiogasR105"] = float(R105_exit[26])
        bmp_output["EnergyR105"] = float(R105_exit[27])
        bmp_output["LHVR105"] = float(R105_exit[28])
          
          
      #%% Online Mode without training With biogas composition from frontend
      elif stateSelectionSideA == False and biogasSideA == True and TrainingMode == False:  #running online without training
        
        if user_idSideA not in bmp_instancesSideA:
          bmp_instancesSideA[user_idSideA] = BMPOnlineTrainMode.BMP_online(DB_IP= DB_IP, DB_Port=DB_Port, DB_Organization=DB_Organization, DB_Bucket=DB_Bucket, DB_Token=DB_Token, 
                                                                      MeasureMethod=measurementMethodSideA, ReactorVolume=ReactorVolumeSideA, InitialFreeVolume=InitialFreeVolumeSideA, 
                                                                      SubstrateNumber=SubstrateNumberSideA, MixRule=MixRuleSideA,
                                                                      Fraction1=Fraction1SideA, Fraction2=Fraction2SideA, Fraction3=Fraction3SideA, Fraction4=Fraction4SideA, WaterFraction=WaterFractionSideA,
                                                                      Volume1=Fraction1SideA, Volume2=Fraction2SideA, Volume3=Fraction3SideA, Volume4=Fraction4SideA, WaterVolume=WaterFractionSideA, 
                                                                      Weight1=Fraction1SideA, Weight2=Fraction2SideA, Weight3=Fraction3SideA, Weight4=Fraction4SideA, WaterWeight=WaterFractionSideA,
                                                                      ST1=ST1SideA, SV1=SV1SideA, rho1=rho1SideA, Cc1=Cc1SideA, Ch1=Ch1SideA, Co1=Co1SideA,Cn1=Cn1SideA, Cs1=Cs1SideA,
                                                                      ST2=ST2SideA, SV2=SV2SideA, rho2=rho2SideA, Cc2=Cc2SideA, Ch2=Ch2SideA, Co2=Co2SideA,Cn2=Cn2SideA, Cs2=Cs2SideA,
                                                                      ST3=ST3SideA, SV3=SV3SideA, rho3=rho3SideA, Cc3=Cc3SideA, Ch3=Ch3SideA, Co3=Co3SideA,Cn3=Cn3SideA, Cs3=Cs3SideA,
                                                                      ST4=ST4SideA, SV4=SV4SideA, rho4=rho4SideA, Cc4=Cc4SideA, Ch4=Ch4SideA, Co4=Co4SideA,Cn4=Cn4SideA, Cs4=Cs4SideA,
                                                                      OperationMethod = OperationMethodSideA, Model=ModelSideA)
      
        SideA = bmp_instancesSideA[user_idSideA]
        
        SideA.GetData(SideA=True, SideB=False, TrainTime=TrainTimeSideA)
        DataSideA = SideA.PlantSideA
        DataInterfaz = SideA.PlantEstimation
        SideA.ProcessData(SideA = True, SideB = False, MeasureMethodSideA = measurementMethodSideA, MeasureMethodSideB = measurementMethodSideA, DataPlantSideA = DataSideA, DataPlantSideB = DataSideA,  
                          DataEstimation = DataInterfaz, OperationMethod = OperationMethodSideA)
        R101_data = SideA.R101_data
        R102_data = SideA.R102_data
        R103_data = SideA.R103_data
        R104_data = SideA.R104_data
        R105_data = SideA.R105_data
        if SideA.OperationMethod in ["Time", "Injection"]:
          SideA.SubstrateFeeding()
        
        if SideA.OperationMethod in ["Time", "Injection"]:
          SideA.SubstrateFeeding()
        
        R101 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R101", ReactorData = R101_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R101, xCO2=xCO2R101, xO2=xO2R101, xH2S=xH2SR101, XH2=xH2R101)
        R102 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R102", ReactorData = R102_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R102, xCO2=xCO2R102, xO2=xO2R102, xH2S=xH2SR102, XH2=xH2R102)
        R103 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R103", ReactorData = R103_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R103, xCO2=xCO2R103, xO2=xO2R103, xH2S=xH2SR103, XH2=xH2R103)
        R104 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R104", ReactorData = R104_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R104, xCO2=xCO2R104, xO2=xO2R104, xH2S=xH2SR104, XH2=xH2R104)
        R105 = SideA.StochoimetricExpendtire_Reactor(ReactorName="R105", ReactorData = R105_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA, xCH4=xCH4R105, xCO2=xCO2R105, xO2=xO2R105, xH2S=xH2SR105, XH2=xH2R105)
        data_instancesSideA[user_data_sideA] = [R101, R102, R103, R104, R105]
        
        R101_exit = SideA.exit_variable_online (ReactorName = "R101", ReactorData = data_instancesSideA[user_data_sideA][0], Vrxn = ReactorVolumeSideA)
        R102_exit = SideA.exit_variable_online (ReactorName = "R102", ReactorData = data_instancesSideA[user_data_sideA][1], Vrxn = ReactorVolumeSideA)
        R103_exit = SideA.exit_variable_online (ReactorName = "R103", ReactorData = data_instancesSideA[user_data_sideA][2], Vrxn = ReactorVolumeSideA)
        R104_exit = SideA.exit_variable_online (ReactorName = "R104", ReactorData = data_instancesSideA[user_data_sideA][3], Vrxn = ReactorVolumeSideA)
        R105_exit = SideA.exit_variable_online (ReactorName = "R105", ReactorData = data_instancesSideA[user_data_sideA][4], Vrxn = ReactorVolumeSideA)
        #Output variables
        #R101
        bmp_output["mixVelocityR101"] = float(R101_exit[0]) 
        bmp_output["SVR101"] = float(R101_exit[1])
        bmp_output["OCR101"] = float(R101_exit[2])
        bmp_output["STR101"] = float(R101_exit[3])
        bmp_output["XR101"] = float(R101_exit[4])
        bmp_output["PBMR101"] = float(R101_exit[5])
        bmp_output["KR101"] = float(0)
        bmp_output["EaR101"] = float(0)
        bmp_output["lambdaR101"] = float(R101_opt[2])
        bmp_output["Objetive"] = float(R101_opt[3])
        bmp_output["TempR101"] = float(R101_exit[6])  
        bmp_output["pHR101"] = float(R101_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR101"] =float(R101_exit[8])
        bmp_output["carbondioxidemolR101"] = float(R101_exit[9])
        bmp_output["oxygenmolR101"] = float(R101_exit[10])
        bmp_output["hydrogensulfurmolR101"] = float(R101_exit[11])
        bmp_output["hydrogenmolR101"] = float(R101_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR101"] = float(R101_exit[13])
        bmp_output["carbondioxideconcentrationR101"] = float(R101_exit[14])
        bmp_output["oxygenconcentrationR101"] = float(R101_exit[15])
        bmp_output["hydrogensulfurconcentrationR101"] = float(R101_exit[16])
        bmp_output["hydrogenconcentrationR101"] = float(R101_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR101"] = float(R101_exit[18])
        bmp_output["carbondioxidevolR101"] = float(R101_exit[19])
        bmp_output["oxygenvolR101"] = float(R101_exit[20])
        bmp_output["hydrogensulfurvolR101"] = float(R101_exit[21])
        bmp_output["hydrogenvolR101"] = float(R101_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR101"] = float(R101_exit[23])
        bmp_output["storagebiogaspressureR101"] = float(R101_exit[24])
        bmp_output["storagebiogasR101"] = float(R101_exit[25])
        bmp_output["accumbiogasR101"] = float(R101_exit[26])
        bmp_output["EnergyR101"] = float(R101_exit[27])
        bmp_output["LHVR101"] = float(R101_exit[28])

        #R102
        bmp_output["mixVelocityR102"] = float(R102_exit[0]) 
        bmp_output["SVR102"] = float(R102_exit[1])
        bmp_output["OCR102"] = float(R102_exit[2])
        bmp_output["STR102"] = float(R102_exit[3])
        bmp_output["XR102"] = float(R102_exit[4])
        bmp_output["PBMR102"] = float(R102_exit[5])
        bmp_output["KR102"] = float(0)
        bmp_output["EaR102"] = float(0)
        bmp_output["lambdaR102"] = float(R102_opt[2])
        bmp_output["Objetive"] = float(R102_opt[3])
        bmp_output["TempR102"] = float(R102_exit[6])  
        bmp_output["pHR102"] = float(R102_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR102"] =float(R102_exit[8])
        bmp_output["carbondioxidemolR102"] = float(R102_exit[9])
        bmp_output["oxygenmolR102"] = float(R102_exit[10])
        bmp_output["hydrogensulfurmolR102"] = float(R102_exit[11])
        bmp_output["hydrogenmolR102"] = float(R102_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR102"] = float(R102_exit[13])
        bmp_output["carbondioxideconcentrationR102"] = float(R102_exit[14])
        bmp_output["oxygenconcentrationR102"] = float(R102_exit[15])
        bmp_output["hydrogensulfurconcentrationR102"] = float(R102_exit[16])
        bmp_output["hydrogenconcentrationR102"] = float(R102_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR102"] = float(R102_exit[18])
        bmp_output["carbondioxidevolR102"] = float(R102_exit[19])
        bmp_output["oxygenvolR102"] = float(R102_exit[20])
        bmp_output["hydrogensulfurvolR102"] = float(R102_exit[21])
        bmp_output["hydrogenvolR102"] = float(R102_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR102"] = float(R102_exit[23])
        bmp_output["storagebiogaspressureR102"] = float(R102_exit[24])
        bmp_output["storagebiogasR102"] = float(R102_exit[25])
        bmp_output["accumbiogasR102"] = float(R102_exit[26])
        bmp_output["EnergyR102"] = float(R102_exit[27])
        bmp_output["LHVR102"] = float(R102_exit[28])

        #R103
        bmp_output["mixVelocityR103"] = float(R103_exit[0]) 
        bmp_output["SVR103"] = float(R103_exit[1])
        bmp_output["OCR103"] = float(R103_exit[2])
        bmp_output["STR103"] = float(R103_exit[3])
        bmp_output["XR103"] = float(R103_exit[4])
        bmp_output["PBMR103"] = float(R103_exit[5])
        bmp_output["KR103"] = float(0)
        bmp_output["EaR103"] = float(0)
        bmp_output["lambdaR103"] = float(R103_opt[2])
        bmp_output["Objetive"] = float(R103_opt[3])
        bmp_output["TempR103"] = float(R103_exit[6])  
        bmp_output["pHR103"] = float(R103_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR103"] =float(R103_exit[8])
        bmp_output["carbondioxidemolR103"] = float(R103_exit[9])
        bmp_output["oxygenmolR103"] = float(R103_exit[10])
        bmp_output["hydrogensulfurmolR103"] = float(R103_exit[11])
        bmp_output["hydrogenmolR103"] = float(R103_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR103"] = float(R103_exit[13])
        bmp_output["carbondioxideconcentrationR103"] = float(R103_exit[14])
        bmp_output["oxygenconcentrationR103"] = float(R103_exit[15])
        bmp_output["hydrogensulfurconcentrationR103"] = float(R103_exit[16])
        bmp_output["hydrogenconcentrationR103"] = float(R103_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR103"] = float(R103_exit[18])
        bmp_output["carbondioxidevolR103"] = float(R103_exit[19])
        bmp_output["oxygenvolR103"] = float(R103_exit[20])
        bmp_output["hydrogensulfurvolR103"] = float(R103_exit[21])
        bmp_output["hydrogenvolR103"] = float(R103_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR103"] = float(R103_exit[23])
        bmp_output["storagebiogaspressureR103"] = float(R103_exit[24])
        bmp_output["storagebiogasR103"] = float(R103_exit[25])
        bmp_output["accumbiogasR103"] = float(R103_exit[26])
        bmp_output["EnergyR103"] = float(R103_exit[27])
        bmp_output["LHVR103"] = float(R103_exit[28])

        #R104
        bmp_output["mixVelocityR104"] = float(R104_exit[0]) 
        bmp_output["SVR104"] = float(R104_exit[1])
        bmp_output["OCR104"] = float(R104_exit[2])
        bmp_output["STR104"] = float(R104_exit[3])
        bmp_output["XR104"] = float(R104_exit[4])
        bmp_output["PBMR104"] = float(R104_exit[5])
        bmp_output["KR104"] = float(0)
        bmp_output["EaR104"] = float(0)
        bmp_output["lambdaR104"] = float(R104_opt[2])
        bmp_output["Objetive"] = float(R104_opt[3])
        bmp_output["TempR104"] = float(R104_exit[6])  
        bmp_output["pHR104"] = float(R104_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR104"] =float(R104_exit[8])
        bmp_output["carbondioxidemolR104"] = float(R104_exit[9])
        bmp_output["oxygenmolR104"] = float(R104_exit[10])
        bmp_output["hydrogensulfurmolR104"] = float(R104_exit[11])
        bmp_output["hydrogenmolR104"] = float(R104_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR104"] = float(R104_exit[13])
        bmp_output["carbondioxideconcentrationR104"] = float(R104_exit[14])
        bmp_output["oxygenconcentrationR104"] = float(R104_exit[15])
        bmp_output["hydrogensulfurconcentrationR104"] = float(R104_exit[16])
        bmp_output["hydrogenconcentrationR104"] = float(R104_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR104"] = float(R104_exit[18])
        bmp_output["carbondioxidevolR104"] = float(R104_exit[19])
        bmp_output["oxygenvolR104"] = float(R104_exit[20])
        bmp_output["hydrogensulfurvolR104"] = float(R104_exit[21])
        bmp_output["hydrogenvolR104"] = float(R104_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR104"] = float(R104_exit[23])
        bmp_output["storagebiogaspressureR104"] = float(R104_exit[24])
        bmp_output["storagebiogasR104"] = float(R104_exit[25])
        bmp_output["accumbiogasR104"] = float(R104_exit[26])
        bmp_output["EnergyR104"] = float(R104_exit[27])
        bmp_output["LHVR104"] = float(R104_exit[28])

        #R105
        bmp_output["mixVelocityR105"] = float(R105_exit[0]) 
        bmp_output["SVR105"] = float(R105_exit[1])
        bmp_output["OCR105"] = float(R105_exit[2])
        bmp_output["STR105"] = float(R105_exit[3])
        bmp_output["XR105"] = float(R105_exit[4])
        bmp_output["PBMR105"] = float(R105_exit[5])
        bmp_output["KR105"] = float(0)
        bmp_output["EaR105"] = float(0)
        bmp_output["lambdaR105"] = float(R105_opt[2])
        bmp_output["Objetive"] = float(R105_opt[3])
        bmp_output["TempR105"] = float(R105_exit[6])  
        bmp_output["pHR105"] = float(R105_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR105"] =float(R105_exit[8])
        bmp_output["carbondioxidemolR105"] = float(R105_exit[9])
        bmp_output["oxygenmolR105"] = float(R105_exit[10])
        bmp_output["hydrogensulfurmolR105"] = float(R105_exit[11])
        bmp_output["hydrogenmolR105"] = float(R105_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR105"] = float(R105_exit[13])
        bmp_output["carbondioxideconcentrationR105"] = float(R105_exit[14])
        bmp_output["oxygenconcentrationR105"] = float(R105_exit[15])
        bmp_output["hydrogensulfurconcentrationR105"] = float(R105_exit[16])
        bmp_output["hydrogenconcentrationR105"] = float(R105_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR105"] = float(R105_exit[18])
        bmp_output["carbondioxidevolR105"] = float(R105_exit[19])
        bmp_output["oxygenvolR105"] = float(R105_exit[20])
        bmp_output["hydrogensulfurvolR105"] = float(R105_exit[21])
        bmp_output["hydrogenvolR105"] = float(R105_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR105"] = float(R105_exit[23])
        bmp_output["storagebiogaspressureR105"] = float(R105_exit[24])
        bmp_output["storagebiogasR105"] = float(R105_exit[25])
        bmp_output["accumbiogasR105"] = float(R105_exit[26])
        bmp_output["EnergyR105"] = float(R105_exit[27])
        bmp_output["LHVR105"] = float(R105_exit[28])

      #%% Online Mode without training With biogas composition from frontend
      elif stateSelectionSideA == False and biogasSideA == False and TrainingMode == False:  #running online without training
        
        if user_idSideA not in bmp_instancesSideA:
          bmp_instancesSideA[user_idSideA] = BMPOnlineTrainMode.BMP_online(DB_IP= DB_IP, DB_Port=DB_Port, DB_Organization=DB_Organization, DB_Bucket=DB_Bucket, DB_Token=DB_Token, 
                                                                      MeasureMethod=measurementMethodSideA, ReactorVolume=ReactorVolumeSideA, InitialFreeVolume=InitialFreeVolumeSideA, 
                                                                      SubstrateNumber=SubstrateNumberSideA, MixRule=MixRuleSideA,
                                                                      Fraction1=Fraction1SideA, Fraction2=Fraction2SideA, Fraction3=Fraction3SideA, Fraction4=Fraction4SideA, WaterFraction=WaterFractionSideA,
                                                                      Volume1=Fraction1SideA, Volume2=Fraction2SideA, Volume3=Fraction3SideA, Volume4=Fraction4SideA, WaterVolume=WaterFractionSideA, 
                                                                      Weight1=Fraction1SideA, Weight2=Fraction2SideA, Weight3=Fraction3SideA, Weight4=Fraction4SideA, WaterWeight=WaterFractionSideA,
                                                                      ST1=ST1SideA, SV1=SV1SideA, rho1=rho1SideA, Cc1=Cc1SideA, Ch1=Ch1SideA, Co1=Co1SideA,Cn1=Cn1SideA, Cs1=Cs1SideA,
                                                                      ST2=ST2SideA, SV2=SV2SideA, rho2=rho2SideA, Cc2=Cc2SideA, Ch2=Ch2SideA, Co2=Co2SideA,Cn2=Cn2SideA, Cs2=Cs2SideA,
                                                                      ST3=ST3SideA, SV3=SV3SideA, rho3=rho3SideA, Cc3=Cc3SideA, Ch3=Ch3SideA, Co3=Co3SideA,Cn3=Cn3SideA, Cs3=Cs3SideA,
                                                                      ST4=ST4SideA, SV4=SV4SideA, rho4=rho4SideA, Cc4=Cc4SideA, Ch4=Ch4SideA, Co4=Co4SideA,Cn4=Cn4SideA, Cs4=Cs4SideA,
                                                                      OperationMethod = OperationMethodSideA, Model=ModelSideA)

        SideA = bmp_instancesSideA[user_idSideA]
        
        SideA.GetData(SideA=True, SideB=False, TrainTime=TrainTimeSideA)
        DataSideA = SideA.PlantSideA
        DataInterfaz = SideA.PlantEstimation
        SideA.ProcessData(SideA = True, SideB = False, MeasureMethodSideA = measurementMethodSideA, MeasureMethodSideB = measurementMethodSideA, DataPlantSideA = DataSideA, DataPlantSideB = DataSideA,  
                          DataEstimation = DataInterfaz, OperationMethod = OperationMethodSideA)
        R101_data = SideA.R101_data
        R102_data = SideA.R102_data
        R103_data = SideA.R103_data
        R104_data = SideA.R104_data
        R105_data = SideA.R105_data
        if SideA.OperationMethod in ["Time", "Injection"]:
          SideA.SubstrateFeeding()
        
        R101 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R101", ReactorData = R101_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
        R102 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R102", ReactorData = R102_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
        R103 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R103", ReactorData = R103_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
        R104 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R104", ReactorData = R104_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
        R105 = SideA.StochoimetricExpendtire_Reactor_batch(ReactorName="R105", ReactorData = R105_data, Vrxn = ReactorVolumeSideA, OperationMethod=OperationMethodSideA)
        data_instancesSideA[user_data_sideA] = [R101, R102, R103, R104, R105]
        
        R101_exit = SideA.exit_variable_online (ReactorName = "R101", ReactorData = data_instancesSideA[user_data_sideA][0], Vrxn = ReactorVolumeSideA)
        R102_exit = SideA.exit_variable_online (ReactorName = "R102", ReactorData = data_instancesSideA[user_data_sideA][1], Vrxn = ReactorVolumeSideA)
        R103_exit = SideA.exit_variable_online (ReactorName = "R103", ReactorData = data_instancesSideA[user_data_sideA][2], Vrxn = ReactorVolumeSideA)
        R104_exit = SideA.exit_variable_online (ReactorName = "R104", ReactorData = data_instancesSideA[user_data_sideA][3], Vrxn = ReactorVolumeSideA)
        R105_exit = SideA.exit_variable_online (ReactorName = "R105", ReactorData = data_instancesSideA[user_data_sideA][4], Vrxn = ReactorVolumeSideA)
        #Output variables
        #R101
        bmp_output["mixVelocityR101"] = float(R101_exit[0]) 
        bmp_output["SVR101"] = float(R101_exit[1])
        bmp_output["OCR101"] = float(R101_exit[2])
        bmp_output["STR101"] = float(R101_exit[3])
        bmp_output["XR101"] = float(R101_exit[4])
        bmp_output["PBMR101"] = float(R101_exit[5])
        bmp_output["KR101"] = KSideA
        bmp_output["EaR101"] = EaSideA
        bmp_output["lambdaR101"] = LSideA
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR101"] = float(R101_exit[6])  
        bmp_output["pHR101"] = float(R101_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR101"] =float(R101_exit[8])
        bmp_output["carbondioxidemolR101"] = float(R101_exit[9])
        bmp_output["oxygenmolR101"] = float(R101_exit[10])
        bmp_output["hydrogensulfurmolR101"] = float(R101_exit[11])
        bmp_output["hydrogenmolR101"] = float(R101_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR101"] = float(R101_exit[13])
        bmp_output["carbondioxideconcentrationR101"] = float(R101_exit[14])
        bmp_output["oxygenconcentrationR101"] = float(R101_exit[15])
        bmp_output["hydrogensulfurconcentrationR101"] = float(R101_exit[16])
        bmp_output["hydrogenconcentrationR101"] = float(R101_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR101"] = float(R101_exit[18])
        bmp_output["carbondioxidevolR101"] = float(R101_exit[19])
        bmp_output["oxygenvolR101"] = float(R101_exit[20])
        bmp_output["hydrogensulfurvolR101"] = float(R101_exit[21])
        bmp_output["hydrogenvolR101"] = float(R101_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR101"] = float(R101_exit[23])
        bmp_output["storagebiogaspressureR101"] = float(R101_exit[24])
        bmp_output["storagebiogasR101"] = float(R101_exit[25])
        bmp_output["accumbiogasR101"] = float(R101_exit[26])
        bmp_output["EnergyR101"] = float(R101_exit[27])
        bmp_output["LHVR101"] = float(R101_exit[28])

        #R102
        bmp_output["mixVelocityR102"] = float(R102_exit[0]) 
        bmp_output["SVR102"] = float(R102_exit[1])
        bmp_output["OCR102"] = float(R102_exit[2])
        bmp_output["STR102"] = float(R102_exit[3])
        bmp_output["XR102"] = float(R102_exit[4])
        bmp_output["PBMR102"] = float(R102_exit[5])
        bmp_output["KR102"] = KSideA
        bmp_output["EaR102"] = EaSideA
        bmp_output["lambdaR102"] = LSideA
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR102"] = float(R102_exit[6])  
        bmp_output["pHR102"] = float(R102_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR102"] =float(R102_exit[8])
        bmp_output["carbondioxidemolR102"] = float(R102_exit[9])
        bmp_output["oxygenmolR102"] = float(R102_exit[10])
        bmp_output["hydrogensulfurmolR102"] = float(R102_exit[11])
        bmp_output["hydrogenmolR102"] = float(R102_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR102"] = float(R102_exit[13])
        bmp_output["carbondioxideconcentrationR102"] = float(R102_exit[14])
        bmp_output["oxygenconcentrationR102"] = float(R102_exit[15])
        bmp_output["hydrogensulfurconcentrationR102"] = float(R102_exit[16])
        bmp_output["hydrogenconcentrationR102"] = float(R102_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR102"] = float(R102_exit[18])
        bmp_output["carbondioxidevolR102"] = float(R102_exit[19])
        bmp_output["oxygenvolR102"] = float(R102_exit[20])
        bmp_output["hydrogensulfurvolR102"] = float(R102_exit[21])
        bmp_output["hydrogenvolR102"] = float(R102_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR102"] = float(R102_exit[23])
        bmp_output["storagebiogaspressureR102"] = float(R102_exit[24])
        bmp_output["storagebiogasR102"] = float(R102_exit[25])
        bmp_output["accumbiogasR102"] = float(R102_exit[26])
        bmp_output["EnergyR102"] = float(R102_exit[27])
        bmp_output["LHVR102"] = float(R102_exit[28])

        #R103
        bmp_output["mixVelocityR103"] = float(R103_exit[0]) 
        bmp_output["SVR103"] = float(R103_exit[1])
        bmp_output["OCR103"] = float(R103_exit[2])
        bmp_output["STR103"] = float(R103_exit[3])
        bmp_output["XR103"] = float(R103_exit[4])
        bmp_output["PBMR103"] = float(R103_exit[5])
        bmp_output["KR103"] = KSideA
        bmp_output["EaR103"] = EaSideA
        bmp_output["lambdaR103"] = LSideA
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR103"] = float(R103_exit[6])  
        bmp_output["pHR103"] = float(R103_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR103"] =float(R103_exit[8])
        bmp_output["carbondioxidemolR103"] = float(R103_exit[9])
        bmp_output["oxygenmolR103"] = float(R103_exit[10])
        bmp_output["hydrogensulfurmolR103"] = float(R103_exit[11])
        bmp_output["hydrogenmolR103"] = float(R103_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR103"] = float(R103_exit[13])
        bmp_output["carbondioxideconcentrationR103"] = float(R103_exit[14])
        bmp_output["oxygenconcentrationR103"] = float(R103_exit[15])
        bmp_output["hydrogensulfurconcentrationR103"] = float(R103_exit[16])
        bmp_output["hydrogenconcentrationR103"] = float(R103_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR103"] = float(R103_exit[18])
        bmp_output["carbondioxidevolR103"] = float(R103_exit[19])
        bmp_output["oxygenvolR103"] = float(R103_exit[20])
        bmp_output["hydrogensulfurvolR103"] = float(R103_exit[21])
        bmp_output["hydrogenvolR103"] = float(R103_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR103"] = float(R103_exit[23])
        bmp_output["storagebiogaspressureR103"] = float(R103_exit[24])
        bmp_output["storagebiogasR103"] = float(R103_exit[25])
        bmp_output["accumbiogasR103"] = float(R103_exit[26])
        bmp_output["EnergyR103"] = float(R103_exit[27])
        bmp_output["LHVR103"] = float(R103_exit[28])

        #R104
        bmp_output["mixVelocityR104"] = float(R104_exit[0]) 
        bmp_output["SVR104"] = float(R104_exit[1])
        bmp_output["OCR104"] = float(R104_exit[2])
        bmp_output["STR104"] = float(R104_exit[3])
        bmp_output["XR104"] = float(R104_exit[4])
        bmp_output["PBMR104"] = float(R104_exit[5])
        bmp_output["KR104"] = KSideA
        bmp_output["EaR104"] = EaSideA
        bmp_output["lambdaR104"] = LSideA
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR104"] = float(R104_exit[6])  
        bmp_output["pHR104"] = float(R104_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR104"] =float(R104_exit[8])
        bmp_output["carbondioxidemolR104"] = float(R104_exit[9])
        bmp_output["oxygenmolR104"] = float(R104_exit[10])
        bmp_output["hydrogensulfurmolR104"] = float(R104_exit[11])
        bmp_output["hydrogenmolR104"] = float(R104_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR104"] = float(R104_exit[13])
        bmp_output["carbondioxideconcentrationR104"] = float(R104_exit[14])
        bmp_output["oxygenconcentrationR104"] = float(R104_exit[15])
        bmp_output["hydrogensulfurconcentrationR104"] = float(R104_exit[16])
        bmp_output["hydrogenconcentrationR104"] = float(R104_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR104"] = float(R104_exit[18])
        bmp_output["carbondioxidevolR104"] = float(R104_exit[19])
        bmp_output["oxygenvolR104"] = float(R104_exit[20])
        bmp_output["hydrogensulfurvolR104"] = float(R104_exit[21])
        bmp_output["hydrogenvolR104"] = float(R104_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR104"] = float(R104_exit[23])
        bmp_output["storagebiogaspressureR104"] = float(R104_exit[24])
        bmp_output["storagebiogasR104"] = float(R104_exit[25])
        bmp_output["accumbiogasR104"] = float(R104_exit[26])
        bmp_output["EnergyR104"] = float(R104_exit[27])
        bmp_output["LHVR104"] = float(R104_exit[28])

        #R105
        bmp_output["mixVelocityR105"] = float(R105_exit[0]) 
        bmp_output["SVR105"] = float(R105_exit[1])
        bmp_output["OCR105"] = float(R105_exit[2])
        bmp_output["STR105"] = float(R105_exit[3])
        bmp_output["XR105"] = float(R105_exit[4])
        bmp_output["PBMR105"] = float(R105_exit[5])
        bmp_output["KR105"] = KSideA
        bmp_output["EaR105"] = EaSideA
        bmp_output["lambdaR105"] = LSideA
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR105"] = float(R105_exit[6])  
        bmp_output["pHR105"] = float(R105_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR105"] =float(R105_exit[8])
        bmp_output["carbondioxidemolR105"] = float(R105_exit[9])
        bmp_output["oxygenmolR105"] = float(R105_exit[10])
        bmp_output["hydrogensulfurmolR105"] = float(R105_exit[11])
        bmp_output["hydrogenmolR105"] = float(R105_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR105"] = float(R105_exit[13])
        bmp_output["carbondioxideconcentrationR105"] = float(R105_exit[14])
        bmp_output["oxygenconcentrationR105"] = float(R105_exit[15])
        bmp_output["hydrogensulfurconcentrationR105"] = float(R105_exit[16])
        bmp_output["hydrogenconcentrationR105"] = float(R105_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR105"] = float(R105_exit[18])
        bmp_output["carbondioxidevolR105"] = float(R105_exit[19])
        bmp_output["oxygenvolR105"] = float(R105_exit[20])
        bmp_output["hydrogensulfurvolR105"] = float(R105_exit[21])
        bmp_output["hydrogenvolR105"] = float(R105_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR105"] = float(R105_exit[23])
        bmp_output["storagebiogaspressureR105"] = float(R105_exit[24])
        bmp_output["storagebiogasR105"] = float(R105_exit[25])
        bmp_output["accumbiogasR105"] = float(R105_exit[26])
        bmp_output["EnergyR105"] = float(R105_exit[27])
        bmp_output["LHVR105"] = float(R105_exit[28])
          
      
      #%% Offline operation
      if stateSelectionSideA == True:    #offline
        user_id101 = data["name"] + "101"
        user_id102 = data["name"] + "102"
        user_id103 = data["name"] + "103"
        user_id104 = data["name"] + "104"
        user_id105 = data["name"] + "105"
  
        users_instancesSideA = [user_id101, user_id102, user_id103, user_id104, user_id105]   

        if iteration == 1:   
          print(iteration, flush=True)
          for key in users_instancesSideA:
            if key in bmp_instances_offline_SideA:
              del bmp_instances_offline_SideA[key]
              print(f'{key} was delted', flush=True)
        
        # R101
        if user_id101 not in bmp_instances_offline_SideA:
          bmp_instances_offline_SideA[user_id101] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideA, ReactorVolume = ReactorVolumeSideA, InitialFreeVolume = InitialFreeVolumeSideA,
                                                                              SubstrateNumber = SubstrateNumberSideA, MixRule = MixRuleSideA, 
                                                                              Fraction1 = Fraction1SideA, Fraction2 = Fraction2SideA, Fraction3 = Fraction3SideA, Fraction4 = Fraction4SideA, WaterFraction = WaterFractionSideA,
                                                                              Volume1 = Fraction1SideA, Volume2 = Fraction2SideA, Volume3 = Fraction3SideA, Volume4 = Fraction4SideA, WaterVolume = WaterFractionSideA,
                                                                              Weight1 = Fraction1SideA, Weight2 = Fraction2SideA, Weight3 = Fraction3SideA, Weight4 = Fraction4SideA, WaterWeight = WaterFractionSideA,
                                                                              ST1 = ST1SideA, SV1 = SV1SideA, rho1 = rho1SideA, Cc1 = Cc1SideA, Ch1 = Ch1SideA, Co1 = Co1SideA, Cn1 = Cn1SideA, Cs1 = Cs1SideA,
                                                                              ST2 = ST2SideA, SV2 = SV2SideA, rho2 = rho2SideA, Cc2 = Cc2SideA, Ch2 = Ch2SideA, Co2 = Co2SideA, Cn2 = Cn2SideA, Cs2 = Cs2SideA,
                                                                              ST3 = ST3SideA, SV3 = SV3SideA, rho3 = rho3SideA, Cc3 = Cc3SideA, Ch3 = Ch3SideA, Co3 = Co3SideA, Cn3 = Cn3SideA, Cs3 = Cs3SideA,
                                                                              ST4 = ST4SideA, SV4 = SV4SideA, rho4 = rho4SideA, Cc4 = Cc4SideA, Ch4 = Ch4SideA, Co4 = Co4SideA, Cn4 = Cn4SideA, Cs4 = Cs4SideA,
                                                                              OperationMethod = OperationMethodSideA, tp = time_stepSideA)  
        
        R101 = bmp_instances_offline_SideA[user_id101]

        #Mixing R101
        R101.MixControl(MixVelocity = MixVelocitySideA, MixTime = mixTimeSideA, DailyMixing = mixDailySideA, speed_time = speed_time)
        bmp_output["mixVelocityR101"] = R101.MixVelocity

        if OperationMethodSideA in ["Time", "Injection"]:
          R101.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R101.SubstrateFeed(Mode = OperationMethodSideA, Volume = dosificationVolumeSideA, Time = dailyInyectionsSideA, Inyections = dailyInyectionsSideA, Q=3.4, speed_time = speed_time)
        #reactor execution model
        R101.Reactor(model = ModelSideA, OperationMethod = OperationMethodSideA, T = TemperatureSideA + 273.15, K1 = KSideA, K2 = EaSideA, K3 = LSideA, speed_time=speed_time)
        bmp_output["SVR101"] = float(R101.SV_int) 
        bmp_output["OCR101"] = float(R101.OC)
        bmp_output["STR101"] = float(R101.ST_int)
        bmp_output["XR101"] = float(R101.x)
        bmp_output["PBMR101"] = float(R101.PBM)
        bmp_output["KR101"] = KSideA
        bmp_output["EaR101"] = EaSideA
        bmp_output["lambdaR101"] = LSideA
        bmp_output["TempR101"] = TemperatureSideA   
        bmp_output["pHR101"] = pHSideA
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR101"] =float(R101.nCH4)
        bmp_output["carbondioxidemolR101"] = float(R101.nCO2)
        bmp_output["oxygenmolR101"] = float(R101.nO2)
        bmp_output["hydrogensulfurmolR101"] = float(R101.nH2S)
        bmp_output["hydrogenmolR101"] = float(R101.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR101"] = float(R101.xCH4*100)
        bmp_output["carbondioxideconcentrationR101"] = float(R101.xCO2*100)
        bmp_output["oxygenconcentrationR101"] = float(R101.xO2*100)
        bmp_output["hydrogensulfurconcentrationR101"] = float(R101.xH2S*1000000)
        bmp_output["hydrogenconcentrationR101"] = float(R101.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR101"] = float(R101.vCH4)
        bmp_output["carbondioxidevolR101"] = float(R101.vCO2)
        bmp_output["oxygenvolR101"] = float(R101.vO2)
        bmp_output["hydrogensulfurvolR101"] = float(R101.vH2S)
        bmp_output["hydrogenvolR101"] = float(R101.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideA == "Pressure":
            R101.Measurement_by_pressure(T = TemperatureManualSideA, Pset = pressureSetPointSideA)
        elif measurementMethodSideA == "VolumeDisplaced":
            R101.Measument_by_volume(T = TemperatureManualSideA, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR101"] = float(R101.P_acum_psi)
        bmp_output["storagebiogaspressureR101"] = float(R101.P_psi)
        bmp_output["storagebiogasR101"] = float(R101.Vnorm_sto_nmL)
        bmp_output["accumbiogasR101"] = float(R101.Vnormalbiogas)
        bmp_output["LHVR101"] = float(R101.LHV_JNm3)
        bmp_output["EnergyR101"] = float(R101.Energia)
       
        R101.GlobaltimeCounter()

        # R102
        if user_id102 not in bmp_instances_offline_SideA:
          bmp_instances_offline_SideA[user_id102] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideA, ReactorVolume = ReactorVolumeSideA, InitialFreeVolume = InitialFreeVolumeSideA,
                                                                              SubstrateNumber = SubstrateNumberSideA, MixRule = MixRuleSideA, 
                                                                              Fraction1 = Fraction1SideA, Fraction2 = Fraction2SideA, Fraction3 = Fraction3SideA, Fraction4 = Fraction4SideA, WaterFraction = WaterFractionSideA,
                                                                              Volume1 = Fraction1SideA, Volume2 = Fraction2SideA, Volume3 = Fraction3SideA, Volume4 = Fraction4SideA, WaterVolume = WaterFractionSideA,
                                                                              Weight1 = Fraction1SideA, Weight2 = Fraction2SideA, Weight3 = Fraction3SideA, Weight4 = Fraction4SideA, WaterWeight = WaterFractionSideA,
                                                                              ST1 = ST1SideA, SV1 = SV1SideA, rho1 = rho1SideA, Cc1 = Cc1SideA, Ch1 = Ch1SideA, Co1 = Co1SideA, Cn1 = Cn1SideA, Cs1 = Cs1SideA,
                                                                              ST2 = ST2SideA, SV2 = SV2SideA, rho2 = rho2SideA, Cc2 = Cc2SideA, Ch2 = Ch2SideA, Co2 = Co2SideA, Cn2 = Cn2SideA, Cs2 = Cs2SideA,
                                                                              ST3 = ST3SideA, SV3 = SV3SideA, rho3 = rho3SideA, Cc3 = Cc3SideA, Ch3 = Ch3SideA, Co3 = Co3SideA, Cn3 = Cn3SideA, Cs3 = Cs3SideA,
                                                                              ST4 = ST4SideA, SV4 = SV4SideA, rho4 = rho4SideA, Cc4 = Cc4SideA, Ch4 = Ch4SideA, Co4 = Co4SideA, Cn4 = Cn4SideA, Cs4 = Cs4SideA,
                                                                              OperationMethod = OperationMethodSideA, tp = time_stepSideA)  
        
        R102 = bmp_instances_offline_SideA[user_id102]

        #Mixing R102
        R102.MixControl(MixVelocity = MixVelocitySideA, MixTime = mixTimeSideA, DailyMixing = mixDailySideA, speed_time = speed_time)
        bmp_output["mixVelocityR102"] = R102.MixVelocity

        if OperationMethodSideA in ["Time", "Injection"]:
          R102.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R102.SubstrateFeed(Mode = OperationMethodSideA, Volume = dosificationVolumeSideA, Time = dailyInyectionsSideA, Inyections = dailyInyectionsSideA, Q=3.4, speed_time = speed_time)
        #reactor execution model
        R102.Reactor(model = ModelSideA, OperationMethod = OperationMethodSideA, T = TemperatureSideA + 273.15, K1 = KSideA, K2 = EaSideA, K3 = LSideA, speed_time=speed_time)
        bmp_output["SVR102"] = float(R102.SV_int) 
        bmp_output["OCR102"] = float(R102.OC)
        bmp_output["STR102"] = float(R102.ST_int)
        bmp_output["XR102"] = float(R102.x)
        bmp_output["PBMR102"] = float(R102.PBM)
        bmp_output["KR102"] = KSideA
        bmp_output["EaR102"] = EaSideA
        bmp_output["lambdaR102"] = LSideA
        bmp_output["TempR102"] = TemperatureSideA   
        bmp_output["pHR102"] = pHSideA
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR102"] =float(R102.nCH4)
        bmp_output["carbondioxidemolR102"] = float(R102.nCO2)
        bmp_output["oxygenmolR102"] = float(R102.nO2)
        bmp_output["hydrogensulfurmolR102"] = float(R102.nH2S)
        bmp_output["hydrogenmolR102"] = float(R102.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR102"] = float(R102.xCH4*100)
        bmp_output["carbondioxideconcentrationR102"] = float(R102.xCO2*100)
        bmp_output["oxygenconcentrationR102"] = float(R102.xO2*100)
        bmp_output["hydrogensulfurconcentrationR102"] = float(R102.xH2S*1000000)
        bmp_output["hydrogenconcentrationR102"] = float(R102.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR102"] = float(R102.vCH4)
        bmp_output["carbondioxidevolR102"] = float(R102.vCO2)
        bmp_output["oxygenvolR102"] = float(R102.vO2)
        bmp_output["hydrogensulfurvolR102"] = float(R102.vH2S)
        bmp_output["hydrogenvolR102"] = float(R102.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideA == "Pressure":
            R102.Measurement_by_pressure(T = TemperatureManualSideA, Pset = pressureSetPointSideA)
        elif measurementMethodSideA == "VolumeDisplaced":
            R102.Measument_by_volume(T = TemperatureManualSideA, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR102"] = float(R102.P_acum_psi)
        bmp_output["storagebiogaspressureR102"] = float(R102.P_psi)
        bmp_output["storagebiogasR102"] = float(R102.Vnorm_sto_nmL)
        bmp_output["accumbiogasR102"] = float(R102.Vnormalbiogas)
        bmp_output["LHVR102"] = float(R102.LHV_JNm3)
        bmp_output["EnergyR102"] = float(R102.Energia)
       
        R102.GlobaltimeCounter()

        # R103
        if user_id103 not in bmp_instances_offline_SideA:
          bmp_instances_offline_SideA[user_id103] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideA, ReactorVolume = ReactorVolumeSideA, InitialFreeVolume = InitialFreeVolumeSideA,
                                                                              SubstrateNumber = SubstrateNumberSideA, MixRule = MixRuleSideA, 
                                                                              Fraction1 = Fraction1SideA, Fraction2 = Fraction2SideA, Fraction3 = Fraction3SideA, Fraction4 = Fraction4SideA, WaterFraction = WaterFractionSideA,
                                                                              Volume1 = Fraction1SideA, Volume2 = Fraction2SideA, Volume3 = Fraction3SideA, Volume4 = Fraction4SideA, WaterVolume = WaterFractionSideA,
                                                                              Weight1 = Fraction1SideA, Weight2 = Fraction2SideA, Weight3 = Fraction3SideA, Weight4 = Fraction4SideA, WaterWeight = WaterFractionSideA,
                                                                              ST1 = ST1SideA, SV1 = SV1SideA, rho1 = rho1SideA, Cc1 = Cc1SideA, Ch1 = Ch1SideA, Co1 = Co1SideA, Cn1 = Cn1SideA, Cs1 = Cs1SideA,
                                                                              ST2 = ST2SideA, SV2 = SV2SideA, rho2 = rho2SideA, Cc2 = Cc2SideA, Ch2 = Ch2SideA, Co2 = Co2SideA, Cn2 = Cn2SideA, Cs2 = Cs2SideA,
                                                                              ST3 = ST3SideA, SV3 = SV3SideA, rho3 = rho3SideA, Cc3 = Cc3SideA, Ch3 = Ch3SideA, Co3 = Co3SideA, Cn3 = Cn3SideA, Cs3 = Cs3SideA,
                                                                              ST4 = ST4SideA, SV4 = SV4SideA, rho4 = rho4SideA, Cc4 = Cc4SideA, Ch4 = Ch4SideA, Co4 = Co4SideA, Cn4 = Cn4SideA, Cs4 = Cs4SideA,
                                                                              OperationMethod = OperationMethodSideA, tp = time_stepSideA)  
        
        R103 = bmp_instances_offline_SideA[user_id103]

        #Mixing R103
        R103.MixControl(MixVelocity = MixVelocitySideA, MixTime = mixTimeSideA, DailyMixing = mixDailySideA, speed_time = speed_time)
        bmp_output["mixVelocityR103"] = R103.MixVelocity

        if OperationMethodSideA in ["Time", "Injection"]:
          R103.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R103.SubstrateFeed(Mode = OperationMethodSideA, Volume = dosificationVolumeSideA, Time = dailyInyectionsSideA, Inyections = dailyInyectionsSideA, Q=3.4, speed_time = speed_time)
        #reactor execution model
        R103.Reactor(model = ModelSideA, OperationMethod = OperationMethodSideA, T = TemperatureSideA + 273.15, K1 = KSideA, K2 = EaSideA, K3 = LSideA, speed_time=speed_time)
        bmp_output["SVR103"] = float(R103.SV_int) 
        bmp_output["OCR103"] = float(R103.OC)
        bmp_output["STR103"] = float(R103.ST_int)
        bmp_output["XR103"] = float(R103.x)
        bmp_output["PBMR103"] = float(R103.PBM)
        bmp_output["KR103"] = KSideA
        bmp_output["EaR103"] = EaSideA
        bmp_output["lambdaR103"] = LSideA
        bmp_output["TempR103"] = TemperatureSideA   
        bmp_output["pHR103"] = pHSideA
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR103"] =float(R103.nCH4)
        bmp_output["carbondioxidemolR103"] = float(R103.nCO2)
        bmp_output["oxygenmolR103"] = float(R103.nO2)
        bmp_output["hydrogensulfurmolR103"] = float(R103.nH2S)
        bmp_output["hydrogenmolR103"] = float(R103.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR103"] = float(R103.xCH4*100)
        bmp_output["carbondioxideconcentrationR103"] = float(R103.xCO2*100)
        bmp_output["oxygenconcentrationR103"] = float(R103.xO2*100)
        bmp_output["hydrogensulfurconcentrationR103"] = float(R103.xH2S*1000000)
        bmp_output["hydrogenconcentrationR103"] = float(R103.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR103"] = float(R103.vCH4)
        bmp_output["carbondioxidevolR103"] = float(R103.vCO2)
        bmp_output["oxygenvolR103"] = float(R103.vO2)
        bmp_output["hydrogensulfurvolR103"] = float(R103.vH2S)
        bmp_output["hydrogenvolR103"] = float(R103.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideA == "Pressure":
            R103.Measurement_by_pressure(T = TemperatureManualSideA, Pset = pressureSetPointSideA)
        elif measurementMethodSideA == "VolumeDisplaced":
            R103.Measument_by_volume(T = TemperatureManualSideA, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR103"] = float(R103.P_acum_psi)
        bmp_output["storagebiogaspressureR103"] = float(R103.P_psi)
        bmp_output["storagebiogasR103"] = float(R103.Vnorm_sto_nmL)
        bmp_output["accumbiogasR103"] = float(R103.Vnormalbiogas)
        bmp_output["LHVR103"] = float(R103.LHV_JNm3)
        bmp_output["EnergyR103"] = float(R103.Energia)
       
        R103.GlobaltimeCounter()

        # R104
        if user_id104 not in bmp_instances_offline_SideA:
          bmp_instances_offline_SideA[user_id104] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideA, ReactorVolume = ReactorVolumeSideA, InitialFreeVolume = InitialFreeVolumeSideA,
                                                                              SubstrateNumber = SubstrateNumberSideA, MixRule = MixRuleSideA, 
                                                                              Fraction1 = Fraction1SideA, Fraction2 = Fraction2SideA, Fraction3 = Fraction3SideA, Fraction4 = Fraction4SideA, WaterFraction = WaterFractionSideA,
                                                                              Volume1 = Fraction1SideA, Volume2 = Fraction2SideA, Volume3 = Fraction3SideA, Volume4 = Fraction4SideA, WaterVolume = WaterFractionSideA,
                                                                              Weight1 = Fraction1SideA, Weight2 = Fraction2SideA, Weight3 = Fraction3SideA, Weight4 = Fraction4SideA, WaterWeight = WaterFractionSideA,
                                                                              ST1 = ST1SideA, SV1 = SV1SideA, rho1 = rho1SideA, Cc1 = Cc1SideA, Ch1 = Ch1SideA, Co1 = Co1SideA, Cn1 = Cn1SideA, Cs1 = Cs1SideA,
                                                                              ST2 = ST2SideA, SV2 = SV2SideA, rho2 = rho2SideA, Cc2 = Cc2SideA, Ch2 = Ch2SideA, Co2 = Co2SideA, Cn2 = Cn2SideA, Cs2 = Cs2SideA,
                                                                              ST3 = ST3SideA, SV3 = SV3SideA, rho3 = rho3SideA, Cc3 = Cc3SideA, Ch3 = Ch3SideA, Co3 = Co3SideA, Cn3 = Cn3SideA, Cs3 = Cs3SideA,
                                                                              ST4 = ST4SideA, SV4 = SV4SideA, rho4 = rho4SideA, Cc4 = Cc4SideA, Ch4 = Ch4SideA, Co4 = Co4SideA, Cn4 = Cn4SideA, Cs4 = Cs4SideA,
                                                                              OperationMethod = OperationMethodSideA, tp = time_stepSideA)  
        
        R104 = bmp_instances_offline_SideA[user_id104]

        #Mixing R104
        R104.MixControl(MixVelocity = MixVelocitySideA, MixTime = mixTimeSideA, DailyMixing = mixDailySideA, speed_time = speed_time)
        bmp_output["mixVelocityR104"] = R104.MixVelocity

        if OperationMethodSideA in ["Time", "Injection"]:
          R104.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R104.SubstrateFeed(Mode = OperationMethodSideA, Volume = dosificationVolumeSideA, Time = dailyInyectionsSideA, Inyections = dailyInyectionsSideA, Q=3.4, speed_time = speed_time)
        #reactor execution model
        R104.Reactor(model = ModelSideA, OperationMethod = OperationMethodSideA, T = TemperatureSideA + 273.15, K1 = KSideA, K2 = EaSideA, K3 = LSideA, speed_time=speed_time)
        bmp_output["SVR104"] = float(R104.SV_int) 
        bmp_output["OCR104"] = float(R104.OC)
        bmp_output["STR104"] = float(R104.ST_int)
        bmp_output["XR104"] = float(R104.x)
        bmp_output["PBMR104"] = float(R104.PBM)
        bmp_output["KR104"] = KSideA
        bmp_output["EaR104"] = EaSideA
        bmp_output["lambdaR104"] = LSideA
        bmp_output["TempR104"] = TemperatureSideA   
        bmp_output["pHR104"] = pHSideA
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR104"] =float(R104.nCH4)
        bmp_output["carbondioxidemolR104"] = float(R104.nCO2)
        bmp_output["oxygenmolR104"] = float(R104.nO2)
        bmp_output["hydrogensulfurmolR104"] = float(R104.nH2S)
        bmp_output["hydrogenmolR104"] = float(R104.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR104"] = float(R104.xCH4*100)
        bmp_output["carbondioxideconcentrationR104"] = float(R104.xCO2*100)
        bmp_output["oxygenconcentrationR104"] = float(R104.xO2*100)
        bmp_output["hydrogensulfurconcentrationR104"] = float(R104.xH2S*1000000)
        bmp_output["hydrogenconcentrationR104"] = float(R104.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR104"] = float(R104.vCH4)
        bmp_output["carbondioxidevolR104"] = float(R104.vCO2)
        bmp_output["oxygenvolR104"] = float(R104.vO2)
        bmp_output["hydrogensulfurvolR104"] = float(R104.vH2S)
        bmp_output["hydrogenvolR104"] = float(R104.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideA == "Pressure":
            R104.Measurement_by_pressure(T = TemperatureManualSideA, Pset = pressureSetPointSideA)
        elif measurementMethodSideA == "VolumeDisplaced":
            R104.Measument_by_volume(T = TemperatureManualSideA, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR104"] = float(R104.P_acum_psi)
        bmp_output["storagebiogaspressureR104"] = float(R104.P_psi)
        bmp_output["storagebiogasR104"] = float(R104.Vnorm_sto_nmL)
        bmp_output["accumbiogasR104"] = float(R104.Vnormalbiogas)
        bmp_output["LHVR104"] = float(R104.LHV_JNm3)
        bmp_output["EnergyR104"] = float(R104.Energia)
       
        R104.GlobaltimeCounter()

        # R105
        if user_id105 not in bmp_instances_offline_SideA:
          bmp_instances_offline_SideA[user_id105] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideA, ReactorVolume = ReactorVolumeSideA, InitialFreeVolume = InitialFreeVolumeSideA,
                                                                              SubstrateNumber = SubstrateNumberSideA, MixRule = MixRuleSideA, 
                                                                              Fraction1 = Fraction1SideA, Fraction2 = Fraction2SideA, Fraction3 = Fraction3SideA, Fraction4 = Fraction4SideA, WaterFraction = WaterFractionSideA,
                                                                              Volume1 = Fraction1SideA, Volume2 = Fraction2SideA, Volume3 = Fraction3SideA, Volume4 = Fraction4SideA, WaterVolume = WaterFractionSideA,
                                                                              Weight1 = Fraction1SideA, Weight2 = Fraction2SideA, Weight3 = Fraction3SideA, Weight4 = Fraction4SideA, WaterWeight = WaterFractionSideA,
                                                                              ST1 = ST1SideA, SV1 = SV1SideA, rho1 = rho1SideA, Cc1 = Cc1SideA, Ch1 = Ch1SideA, Co1 = Co1SideA, Cn1 = Cn1SideA, Cs1 = Cs1SideA,
                                                                              ST2 = ST2SideA, SV2 = SV2SideA, rho2 = rho2SideA, Cc2 = Cc2SideA, Ch2 = Ch2SideA, Co2 = Co2SideA, Cn2 = Cn2SideA, Cs2 = Cs2SideA,
                                                                              ST3 = ST3SideA, SV3 = SV3SideA, rho3 = rho3SideA, Cc3 = Cc3SideA, Ch3 = Ch3SideA, Co3 = Co3SideA, Cn3 = Cn3SideA, Cs3 = Cs3SideA,
                                                                              ST4 = ST4SideA, SV4 = SV4SideA, rho4 = rho4SideA, Cc4 = Cc4SideA, Ch4 = Ch4SideA, Co4 = Co4SideA, Cn4 = Cn4SideA, Cs4 = Cs4SideA,
                                                                              OperationMethod = OperationMethodSideA, tp = time_stepSideA)  
        
        R105 = bmp_instances_offline_SideA[user_id105]

        #Mixing R105
        R105.MixControl(MixVelocity = MixVelocitySideA, MixTime = mixTimeSideA, DailyMixing = mixDailySideA, speed_time = speed_time)
        bmp_output["mixVelocityR105"] = R105.MixVelocity

        if OperationMethodSideA in ["Time", "Injection"]:
          R105.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R105.SubstrateFeed(Mode = OperationMethodSideA, Volume = dosificationVolumeSideA, Time = dailyInyectionsSideA, Inyections = dailyInyectionsSideA, Q=3.4, speed_time = speed_time)
        bmp_output["caudalSideA"] = float(R105.Qr)
        bmp_output["volumeSubstrateSideA"] = float(R105.TotalVolFeed) - 12.5
        #reactor execution model
        R105.Reactor(model = ModelSideA, OperationMethod = OperationMethodSideA, T = TemperatureSideA + 273.15, K1 = KSideA, K2 = EaSideA, K3 = LSideA, speed_time=speed_time)
        bmp_output["SVR105"] = float(R105.SV_int) 
        bmp_output["OCR105"] = float(R105.OC)
        bmp_output["STR105"] = float(R105.ST_int)
        bmp_output["XR105"] = float(R105.x)
        bmp_output["PBMR105"] = float(R105.PBM)
        bmp_output["KR105"] = KSideA
        bmp_output["EaR105"] = EaSideA
        bmp_output["lambdaR105"] = LSideA
        bmp_output["TempR105"] = TemperatureSideA   
        bmp_output["pHR105"] = pHSideA
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR105"] =float(R105.nCH4)
        bmp_output["carbondioxidemolR105"] = float(R105.nCO2)
        bmp_output["oxygenmolR105"] = float(R105.nO2)
        bmp_output["hydrogensulfurmolR105"] = float(R105.nH2S)
        bmp_output["hydrogenmolR105"] = float(R105.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR105"] = float(R105.xCH4*100)
        bmp_output["carbondioxideconcentrationR105"] = float(R105.xCO2*100)
        bmp_output["oxygenconcentrationR105"] = float(R105.xO2*100)
        bmp_output["hydrogensulfurconcentrationR105"] = float(R105.xH2S*1000000)
        bmp_output["hydrogenconcentrationR105"] = float(R105.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR105"] = float(R105.vCH4)
        bmp_output["carbondioxidevolR105"] = float(R105.vCO2)
        bmp_output["oxygenvolR105"] = float(R105.vO2)
        bmp_output["hydrogensulfurvolR105"] = float(R105.vH2S)
        bmp_output["hydrogenvolR105"] = float(R105.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideA == "Pressure":
            R105.Measurement_by_pressure(T = TemperatureManualSideA, Pset = pressureSetPointSideA)
        elif measurementMethodSideA == "VolumeDisplaced":
            R105.Measument_by_volume(T = TemperatureManualSideA, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR105"] = float(R105.P_acum_psi)
        bmp_output["storagebiogaspressureR105"] = float(R105.P_psi)
        bmp_output["storagebiogasR105"] = float(R105.Vnorm_sto_nmL)
        bmp_output["accumbiogasR105"] = float(R105.Vnormalbiogas)
        bmp_output["LHVR105"] = float(R105.LHV_JNm3)
        bmp_output["EnergyR105"] = float(R105.Energia)

        R105.GlobaltimeCounter()
    
    #%% ---- Side B - Working
    if StateSideB == True:
      user_idSideB = name + "SideA"
      user_data_sideB = name + "DataSideA"

      user_instances_SideB = [user_idSideB]
      data_instances_SideB = [user_data_sideB]
    
      if iteration == 1:   
          for key in user_instances_SideB:
            if key in bmp_instancesSideB:
              del bmp_instancesSideB[key]  
      
      if iteration == 1:
        for key in data_instances_SideB:
          if key in data_instancesSideB:
            del data_instancesSideB[key] 
      

      #%% online mode B
      if stateSelectionSideB == False and biogasSideB == False and TrainingMode == True:    #Online, biogas compounds in auto
        
        if user_idSideB not in bmp_instancesSideB:
          bmp_instancesSideB[user_idSideB] = BMPOnlineTrainMode.BMP_online(DB_IP= DB_IP, DB_Port=DB_Port, DB_Organization=DB_Organization, DB_Bucket=DB_Bucket, DB_Token=DB_Token, 
                                                                      MeasureMethod=measurementMethodSideB, ReactorVolume=ReactorVolumeSideB, InitialFreeVolume=InitialFreeVolumeSideB, 
                                                                      SubstrateNumber=SubstrateNumberSideB, MixRule=MixRuleSideB,
                                                                      Fraction1=Fraction1SideB, Fraction2=Fraction2SideB, Fraction3=Fraction3SideB, Fraction4=Fraction4SideB, WaterFraction=WaterFractionSideB,
                                                                      Volume1=Fraction1SideB, Volume2=Fraction2SideB, Volume3=Fraction3SideB, Volume4=Fraction4SideB, WaterVolume=WaterFractionSideB, 
                                                                      Weight1=Fraction1SideB, Weight2=Fraction2SideB, Weight3=Fraction3SideB, Weight4=Fraction4SideB, WaterWeight=WaterFractionSideB,
                                                                      ST1=ST1SideB, SV1=SV1SideB, rho1=rho1SideB, Cc1=Cc1SideB, Ch1=Ch1SideB, Co1=Co1SideB,Cn1=Cn1SideB, Cs1=Cs1SideB,
                                                                      ST2=ST2SideB, SV2=SV2SideB, rho2=rho2SideB, Cc2=Cc2SideB, Ch2=Ch2SideB, Co2=Co2SideB,Cn2=Cn2SideB, Cs2=Cs2SideB,
                                                                      ST3=ST3SideB, SV3=SV3SideB, rho3=rho3SideB, Cc3=Cc3SideB, Ch3=Ch3SideB, Co3=Co3SideB,Cn3=Cn3SideB, Cs3=Cs3SideB,
                                                                      ST4=ST4SideB, SV4=SV4SideB, rho4=rho4SideB, Cc4=Cc4SideB, Ch4=Ch4SideB, Co4=Co4SideB,Cn4=Cn4SideB, Cs4=Cs4SideB,
                                                                      OperationMethod = OperationMethodSideB, Model=ModelSideB)

        SideB = bmp_instancesSideB[user_idSideB]
        if user_data_sideB not in data_instancesSideB:
          SideB.GetData(SideA=False, SideB=True, TrainTime=TrainTimeSideB)
          DataSideB = SideB.PlantSideB
          DataInterfaz = SideB.PlantEstimation
          SideB.ProcessData(SideA = False, SideB = True, MeasureMethodSideA = measurementMethodSideB, MeasureMethodSideB = measurementMethodSideB, DataPlantSideA = DataSideB, DataPlantSideB = DataSideB,  
                           DataEstimation = DataInterfaz, OperationMethod = OperationMethodSideB)
          R106_data = SideB.R106_data
          R107_data = SideB.R107_data
          R108_data = SideB.R108_data
          R109_data = SideB.R109_data
          R110_data = SideB.R110_data
          if SideB.OperationMethod in ["Time", "Injection"]:
            SideB.SubstrateFeeding()
          
          R106 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R106", ReactorData = R106_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R107 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R107", ReactorData = R107_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R108 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R108", ReactorData = R108_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R109 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R109", ReactorData = R109_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R110 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R110", ReactorData = R110_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          data_instancesSideB[user_data_sideB] = [R106, R107, R108, R109, R110]
        
        R106_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R106", ReactorData = data_instancesSideB[user_data_sideB][0], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R107_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R107", ReactorData = data_instancesSideB[user_data_sideB][1], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R108_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R108", ReactorData = data_instancesSideB[user_data_sideB][2], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R109_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R109", ReactorData = data_instancesSideB[user_data_sideB][3], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R110_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R110", ReactorData = data_instancesSideB[user_data_sideB][4], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        
        R106_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R106", ReactorData = data_instancesSideB[user_data_sideB][0], Vrxn = ReactorVolumeSideB)
        R107_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R107", ReactorData = data_instancesSideB[user_data_sideB][1], Vrxn = ReactorVolumeSideB)
        R108_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R108", ReactorData = data_instancesSideB[user_data_sideB][2], Vrxn = ReactorVolumeSideB)
        R109_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R109", ReactorData = data_instancesSideB[user_data_sideB][3], Vrxn = ReactorVolumeSideB)
        R110_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R110", ReactorData = data_instancesSideB[user_data_sideB][4], Vrxn = ReactorVolumeSideB)
        #Output variables
        #R106
        bmp_output["mixVelocityR106"] = float(R106_exit[0]) 
        bmp_output["SVR106"] = float(R106_exit[1])
        bmp_output["OCR106"] = float(R106_exit[2])
        bmp_output["STR106"] = float(R106_exit[3])
        bmp_output["XR106"] = float(R106_exit[4])
        bmp_output["PBMR106"] = float(R106_exit[5])
        bmp_output["KR106"] = float(R106_opt[0]/60)
        bmp_output["EaR106"] = float(R106_opt[1])
        bmp_output["lambdaR106"] = float(R106_opt[2])
        bmp_output["Objetive"] = float(R106_opt[3])
        bmp_output["TempR106"] = float(R106_exit[6])  
        bmp_output["pHR106"] = float(R106_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR106"] =float(R106_exit[8])
        bmp_output["carbondioxidemolR106"] = float(R106_exit[9])
        bmp_output["oxygenmolR106"] = float(R106_exit[10])
        bmp_output["hydrogensulfurmolR106"] = float(R106_exit[11])
        bmp_output["hydrogenmolR106"] = float(R106_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR106"] = float(R106_exit[13])
        bmp_output["carbondioxideconcentrationR106"] = float(R106_exit[14])
        bmp_output["oxygenconcentrationR106"] = float(R106_exit[15])
        bmp_output["hydrogensulfurconcentrationR106"] = float(R106_exit[16])
        bmp_output["hydrogenconcentrationR106"] = float(R106_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR106"] = float(R106_exit[18])
        bmp_output["carbondioxidevolR106"] = float(R106_exit[19])
        bmp_output["oxygenvolR106"] = float(R106_exit[20])
        bmp_output["hydrogensulfurvolR106"] = float(R106_exit[21])
        bmp_output["hydrogenvolR106"] = float(R106_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR106"] = float(R106_exit[23])
        bmp_output["storagebiogaspressureR106"] = float(R106_exit[24])
        bmp_output["storagebiogasR106"] = float(R106_exit[25])
        bmp_output["accumbiogasR106"] = float(R106_exit[26])
        bmp_output["EnergyR106"] = float(R106_exit[27])
        bmp_output["LHVR106"] = float(R106_exit[28])

        #R107
        bmp_output["mixVelocityR107"] = float(R107_exit[0]) 
        bmp_output["SVR107"] = float(R107_exit[1])
        bmp_output["OCR107"] = float(R107_exit[2])
        bmp_output["STR107"] = float(R107_exit[3])
        bmp_output["XR107"] = float(R107_exit[4])
        bmp_output["PBMR107"] = float(R107_exit[5])
        bmp_output["KR107"] = float(R107_opt[0]/60)
        bmp_output["EaR107"] = float(R107_opt[1])
        bmp_output["lambdaR107"] = float(R107_opt[2])
        bmp_output["Objetive"] = float(R107_opt[3])
        bmp_output["TempR107"] = float(R107_exit[6])  
        bmp_output["pHR107"] = float(R107_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR107"] =float(R107_exit[8])
        bmp_output["carbondioxidemolR107"] = float(R107_exit[9])
        bmp_output["oxygenmolR107"] = float(R107_exit[10])
        bmp_output["hydrogensulfurmolR107"] = float(R107_exit[11])
        bmp_output["hydrogenmolR107"] = float(R107_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR107"] = float(R107_exit[13])
        bmp_output["carbondioxideconcentrationR107"] = float(R107_exit[14])
        bmp_output["oxygenconcentrationR107"] = float(R107_exit[15])
        bmp_output["hydrogensulfurconcentrationR107"] = float(R107_exit[16])
        bmp_output["hydrogenconcentrationR107"] = float(R107_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR107"] = float(R107_exit[18])
        bmp_output["carbondioxidevolR107"] = float(R107_exit[19])
        bmp_output["oxygenvolR107"] = float(R107_exit[20])
        bmp_output["hydrogensulfurvolR107"] = float(R107_exit[21])
        bmp_output["hydrogenvolR107"] = float(R107_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR107"] = float(R107_exit[23])
        bmp_output["storagebiogaspressureR107"] = float(R107_exit[24])
        bmp_output["storagebiogasR107"] = float(R107_exit[25])
        bmp_output["accumbiogasR107"] = float(R107_exit[26])
        bmp_output["EnergyR107"] = float(R107_exit[27])
        bmp_output["LHVR107"] = float(R107_exit[28])

        #R108
        bmp_output["mixVelocityR108"] = float(R108_exit[0]) 
        bmp_output["SVR108"] = float(R108_exit[1])
        bmp_output["OCR108"] = float(R108_exit[2])
        bmp_output["STR108"] = float(R108_exit[3])
        bmp_output["XR108"] = float(R108_exit[4])
        bmp_output["PBMR108"] = float(R108_exit[5])
        bmp_output["KR108"] = float(R108_opt[0]/60)
        bmp_output["EaR108"] = float(R108_opt[1])
        bmp_output["lambdaR108"] = float(R108_opt[2])
        bmp_output["Objetive"] = float(R108_opt[3])
        bmp_output["TempR108"] = float(R108_exit[6])  
        bmp_output["pHR108"] = float(R108_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR108"] =float(R108_exit[8])
        bmp_output["carbondioxidemolR108"] = float(R108_exit[9])
        bmp_output["oxygenmolR108"] = float(R108_exit[10])
        bmp_output["hydrogensulfurmolR108"] = float(R108_exit[11])
        bmp_output["hydrogenmolR108"] = float(R108_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR108"] = float(R108_exit[13])
        bmp_output["carbondioxideconcentrationR108"] = float(R108_exit[14])
        bmp_output["oxygenconcentrationR108"] = float(R108_exit[15])
        bmp_output["hydrogensulfurconcentrationR108"] = float(R108_exit[16])
        bmp_output["hydrogenconcentrationR108"] = float(R108_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR108"] = float(R108_exit[18])
        bmp_output["carbondioxidevolR108"] = float(R108_exit[19])
        bmp_output["oxygenvolR108"] = float(R108_exit[20])
        bmp_output["hydrogensulfurvolR108"] = float(R108_exit[21])
        bmp_output["hydrogenvolR108"] = float(R108_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR108"] = float(R108_exit[23])
        bmp_output["storagebiogaspressureR108"] = float(R108_exit[24])
        bmp_output["storagebiogasR108"] = float(R108_exit[25])
        bmp_output["accumbiogasR108"] = float(R108_exit[26])
        bmp_output["EnergyR108"] = float(R108_exit[27])
        bmp_output["LHVR108"] = float(R108_exit[28])

        #R109
        bmp_output["mixVelocityR109"] = float(R109_exit[0]) 
        bmp_output["SVR109"] = float(R109_exit[1])
        bmp_output["OCR109"] = float(R109_exit[2])
        bmp_output["STR109"] = float(R109_exit[3])
        bmp_output["XR109"] = float(R109_exit[4])
        bmp_output["PBMR109"] = float(R109_exit[5])
        bmp_output["KR109"] = float(R109_opt[0]/60)
        bmp_output["EaR109"] = float(R109_opt[1])
        bmp_output["lambdaR109"] = float(R109_opt[2])
        bmp_output["Objetive"] = float(R109_opt[3])
        bmp_output["TempR109"] = float(R109_exit[6])  
        bmp_output["pHR109"] = float(R109_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR109"] =float(R109_exit[8])
        bmp_output["carbondioxidemolR109"] = float(R109_exit[9])
        bmp_output["oxygenmolR109"] = float(R109_exit[10])
        bmp_output["hydrogensulfurmolR109"] = float(R109_exit[11])
        bmp_output["hydrogenmolR109"] = float(R109_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR109"] = float(R109_exit[13])
        bmp_output["carbondioxideconcentrationR109"] = float(R109_exit[14])
        bmp_output["oxygenconcentrationR109"] = float(R109_exit[15])
        bmp_output["hydrogensulfurconcentrationR109"] = float(R109_exit[16])
        bmp_output["hydrogenconcentrationR109"] = float(R109_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR109"] = float(R109_exit[18])
        bmp_output["carbondioxidevolR109"] = float(R109_exit[19])
        bmp_output["oxygenvolR109"] = float(R109_exit[20])
        bmp_output["hydrogensulfurvolR109"] = float(R109_exit[21])
        bmp_output["hydrogenvolR109"] = float(R109_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR109"] = float(R109_exit[23])
        bmp_output["storagebiogaspressureR109"] = float(R109_exit[24])
        bmp_output["storagebiogasR109"] = float(R109_exit[25])
        bmp_output["accumbiogasR109"] = float(R109_exit[26])
        bmp_output["EnergyR109"] = float(R109_exit[27])
        bmp_output["LHVR109"] = float(R109_exit[28])

        #R110
        bmp_output["mixVelocityR110"] = float(R110_exit[0]) 
        bmp_output["SVR110"] = float(R110_exit[1])
        bmp_output["OCR110"] = float(R110_exit[2])
        bmp_output["STR110"] = float(R110_exit[3])
        bmp_output["XR110"] = float(R110_exit[4])
        bmp_output["PBMR110"] = float(R110_exit[5])
        bmp_output["KR110"] = float(R110_opt[0]/60)
        bmp_output["EaR110"] = float(R110_opt[1])
        bmp_output["lambdaR110"] = float(R110_opt[2])
        bmp_output["Objetive"] = float(R110_opt[3])
        bmp_output["TempR110"] = float(R110_exit[6])  
        bmp_output["pHR110"] = float(R110_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR110"] =float(R110_exit[8])
        bmp_output["carbondioxidemolR110"] = float(R110_exit[9])
        bmp_output["oxygenmolR110"] = float(R110_exit[10])
        bmp_output["hydrogensulfurmolR110"] = float(R110_exit[11])
        bmp_output["hydrogenmolR110"] = float(R110_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR110"] = float(R110_exit[13])
        bmp_output["carbondioxideconcentrationR110"] = float(R110_exit[14])
        bmp_output["oxygenconcentrationR110"] = float(R110_exit[15])
        bmp_output["hydrogensulfurconcentrationR110"] = float(R110_exit[16])
        bmp_output["hydrogenconcentrationR110"] = float(R110_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR110"] = float(R110_exit[18])
        bmp_output["carbondioxidevolR110"] = float(R110_exit[19])
        bmp_output["oxygenvolR110"] = float(R110_exit[20])
        bmp_output["hydrogensulfurvolR110"] = float(R110_exit[21])
        bmp_output["hydrogenvolR110"] = float(R110_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR110"] = float(R110_exit[23])
        bmp_output["storagebiogaspressureR110"] = float(R110_exit[24])
        bmp_output["storagebiogasR110"] = float(R110_exit[25])
        bmp_output["accumbiogasR110"] = float(R110_exit[26])
        bmp_output["EnergyR110"] = float(R110_exit[27])
        bmp_output["LHVR110"] = float(R110_exit[28])
      
      if stateSelectionSideB == False and biogasSideB == True and TrainingMode == True:    #Online, biogas compounds in auto
        
        if user_idSideB not in bmp_instancesSideB:
          bmp_instancesSideB[user_idSideB] = BMPOnlineTrainMode.BMP_online(DB_IP= DB_IP, DB_Port=DB_Port, DB_Organization=DB_Organization, DB_Bucket=DB_Bucket, DB_Token=DB_Token, 
                                                                      MeasureMethod=measurementMethodSideB, ReactorVolume=ReactorVolumeSideB, InitialFreeVolume=InitialFreeVolumeSideB, 
                                                                      SubstrateNumber=SubstrateNumberSideB, MixRule=MixRuleSideB,
                                                                      Fraction1=Fraction1SideB, Fraction2=Fraction2SideB, Fraction3=Fraction3SideB, Fraction4=Fraction4SideB, WaterFraction=WaterFractionSideB,
                                                                      Volume1=Fraction1SideB, Volume2=Fraction2SideB, Volume3=Fraction3SideB, Volume4=Fraction4SideB, WaterVolume=WaterFractionSideB, 
                                                                      Weight1=Fraction1SideB, Weight2=Fraction2SideB, Weight3=Fraction3SideB, Weight4=Fraction4SideB, WaterWeight=WaterFractionSideB,
                                                                      ST1=ST1SideB, SV1=SV1SideB, rho1=rho1SideB, Cc1=Cc1SideB, Ch1=Ch1SideB, Co1=Co1SideB,Cn1=Cn1SideB, Cs1=Cs1SideB,
                                                                      ST2=ST2SideB, SV2=SV2SideB, rho2=rho2SideB, Cc2=Cc2SideB, Ch2=Ch2SideB, Co2=Co2SideB,Cn2=Cn2SideB, Cs2=Cs2SideB,
                                                                      ST3=ST3SideB, SV3=SV3SideB, rho3=rho3SideB, Cc3=Cc3SideB, Ch3=Ch3SideB, Co3=Co3SideB,Cn3=Cn3SideB, Cs3=Cs3SideB,
                                                                      ST4=ST4SideB, SV4=SV4SideB, rho4=rho4SideB, Cc4=Cc4SideB, Ch4=Ch4SideB, Co4=Co4SideB,Cn4=Cn4SideB, Cs4=Cs4SideB,
                                                                      OperationMethod = OperationMethodSideB, Model=ModelSideB)

        SideB = bmp_instancesSideB[user_idSideB]
        if user_data_sideB not in data_instancesSideB:
          SideB.GetData(SideA=False, SideB=True, TrainTime=TrainTimeSideB)
          DataSideB = SideB.PlantSideB
          DataInterfaz = SideB.PlantEstimation
          SideB.ProcessData(SideA = False, SideB = True, MeasureMethodSideA = measurementMethodSideB, MeasureMethodSideB = measurementMethodSideB, DataPlantSideA = DataSideB, DataPlantSideB = DataSideB,  
                           DataEstimation = DataInterfaz, OperationMethod = OperationMethodSideB)
          R106_data = SideB.R106_data
          R107_data = SideB.R107_data
          R108_data = SideB.R108_data
          R109_data = SideB.R109_data
          R110_data = SideB.R110_data
          if SideB.OperationMethod in ["Time", "Injection"]:
            SideB.SubstrateFeeding()
          
          R106 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R106", ReactorData = R106_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R107 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R107", ReactorData = R107_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R108 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R108", ReactorData = R108_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R109 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R109", ReactorData = R109_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R110 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R110", ReactorData = R110_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          data_instancesSideB[user_data_sideB] = [R106, R107, R108, R109, R110]
        
        R106_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R106", ReactorData = data_instancesSideB[user_data_sideB][0], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R107_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R107", ReactorData = data_instancesSideB[user_data_sideB][1], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R108_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R108", ReactorData = data_instancesSideB[user_data_sideB][2], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R109_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R109", ReactorData = data_instancesSideB[user_data_sideB][3], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R110_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R110", ReactorData = data_instancesSideB[user_data_sideB][4], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        
        R106_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R106", ReactorData = data_instancesSideB[user_data_sideB][0], Vrxn = ReactorVolumeSideB)
        R107_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R107", ReactorData = data_instancesSideB[user_data_sideB][1], Vrxn = ReactorVolumeSideB)
        R108_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R108", ReactorData = data_instancesSideB[user_data_sideB][2], Vrxn = ReactorVolumeSideB)
        R109_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R109", ReactorData = data_instancesSideB[user_data_sideB][3], Vrxn = ReactorVolumeSideB)
        R110_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R110", ReactorData = data_instancesSideB[user_data_sideB][4], Vrxn = ReactorVolumeSideB)
        #Output variables
        #R106
        bmp_output["mixVelocityR106"] = float(R106_exit[0]) 
        bmp_output["SVR106"] = float(R106_exit[1])
        bmp_output["OCR106"] = float(R106_exit[2])
        bmp_output["STR106"] = float(R106_exit[3])
        bmp_output["XR106"] = float(R106_exit[4])
        bmp_output["PBMR106"] = float(R106_exit[5])
        bmp_output["KR106"] = float(R106_opt[0]/60)
        bmp_output["EaR106"] = float(R106_opt[1])
        bmp_output["lambdaR106"] = float(R106_opt[2])
        bmp_output["Objetive"] = float(R106_opt[3])
        bmp_output["TempR106"] = float(R106_exit[6])  
        bmp_output["pHR106"] = float(R106_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR106"] =float(R106_exit[8])
        bmp_output["carbondioxidemolR106"] = float(R106_exit[9])
        bmp_output["oxygenmolR106"] = float(R106_exit[10])
        bmp_output["hydrogensulfurmolR106"] = float(R106_exit[11])
        bmp_output["hydrogenmolR106"] = float(R106_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR106"] = float(R106_exit[13])
        bmp_output["carbondioxideconcentrationR106"] = float(R106_exit[14])
        bmp_output["oxygenconcentrationR106"] = float(R106_exit[15])
        bmp_output["hydrogensulfurconcentrationR106"] = float(R106_exit[16])
        bmp_output["hydrogenconcentrationR106"] = float(R106_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR106"] = float(R106_exit[18])
        bmp_output["carbondioxidevolR106"] = float(R106_exit[19])
        bmp_output["oxygenvolR106"] = float(R106_exit[20])
        bmp_output["hydrogensulfurvolR106"] = float(R106_exit[21])
        bmp_output["hydrogenvolR106"] = float(R106_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR106"] = float(R106_exit[23])
        bmp_output["storagebiogaspressureR106"] = float(R106_exit[24])
        bmp_output["storagebiogasR106"] = float(R106_exit[25])
        bmp_output["accumbiogasR106"] = float(R106_exit[26])
        bmp_output["EnergyR106"] = float(R106_exit[27])
        bmp_output["LHVR106"] = float(R106_exit[28])

        #R107
        bmp_output["mixVelocityR107"] = float(R107_exit[0]) 
        bmp_output["SVR107"] = float(R107_exit[1])
        bmp_output["OCR107"] = float(R107_exit[2])
        bmp_output["STR107"] = float(R107_exit[3])
        bmp_output["XR107"] = float(R107_exit[4])
        bmp_output["PBMR107"] = float(R107_exit[5])
        bmp_output["KR107"] = float(R107_opt[0]/60)
        bmp_output["EaR107"] = float(R107_opt[1])
        bmp_output["lambdaR107"] = float(R107_opt[2])
        bmp_output["Objetive"] = float(R107_opt[3])
        bmp_output["TempR107"] = float(R107_exit[6])  
        bmp_output["pHR107"] = float(R107_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR107"] =float(R107_exit[8])
        bmp_output["carbondioxidemolR107"] = float(R107_exit[9])
        bmp_output["oxygenmolR107"] = float(R107_exit[10])
        bmp_output["hydrogensulfurmolR107"] = float(R107_exit[11])
        bmp_output["hydrogenmolR107"] = float(R107_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR107"] = float(R107_exit[13])
        bmp_output["carbondioxideconcentrationR107"] = float(R107_exit[14])
        bmp_output["oxygenconcentrationR107"] = float(R107_exit[15])
        bmp_output["hydrogensulfurconcentrationR107"] = float(R107_exit[16])
        bmp_output["hydrogenconcentrationR107"] = float(R107_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR107"] = float(R107_exit[18])
        bmp_output["carbondioxidevolR107"] = float(R107_exit[19])
        bmp_output["oxygenvolR107"] = float(R107_exit[20])
        bmp_output["hydrogensulfurvolR107"] = float(R107_exit[21])
        bmp_output["hydrogenvolR107"] = float(R107_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR107"] = float(R107_exit[23])
        bmp_output["storagebiogaspressureR107"] = float(R107_exit[24])
        bmp_output["storagebiogasR107"] = float(R107_exit[25])
        bmp_output["accumbiogasR107"] = float(R107_exit[26])
        bmp_output["EnergyR107"] = float(R107_exit[27])
        bmp_output["LHVR107"] = float(R107_exit[28])

        #R108
        bmp_output["mixVelocityR108"] = float(R108_exit[0]) 
        bmp_output["SVR108"] = float(R108_exit[1])
        bmp_output["OCR108"] = float(R108_exit[2])
        bmp_output["STR108"] = float(R108_exit[3])
        bmp_output["XR108"] = float(R108_exit[4])
        bmp_output["PBMR108"] = float(R108_exit[5])
        bmp_output["KR108"] = float(R108_opt[0]/60)
        bmp_output["EaR108"] = float(R108_opt[1])
        bmp_output["lambdaR108"] = float(R108_opt[2])
        bmp_output["Objetive"] = float(R108_opt[3])
        bmp_output["TempR108"] = float(R108_exit[6])  
        bmp_output["pHR108"] = float(R108_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR108"] =float(R108_exit[8])
        bmp_output["carbondioxidemolR108"] = float(R108_exit[9])
        bmp_output["oxygenmolR108"] = float(R108_exit[10])
        bmp_output["hydrogensulfurmolR108"] = float(R108_exit[11])
        bmp_output["hydrogenmolR108"] = float(R108_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR108"] = float(R108_exit[13])
        bmp_output["carbondioxideconcentrationR108"] = float(R108_exit[14])
        bmp_output["oxygenconcentrationR108"] = float(R108_exit[15])
        bmp_output["hydrogensulfurconcentrationR108"] = float(R108_exit[16])
        bmp_output["hydrogenconcentrationR108"] = float(R108_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR108"] = float(R108_exit[18])
        bmp_output["carbondioxidevolR108"] = float(R108_exit[19])
        bmp_output["oxygenvolR108"] = float(R108_exit[20])
        bmp_output["hydrogensulfurvolR108"] = float(R108_exit[21])
        bmp_output["hydrogenvolR108"] = float(R108_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR108"] = float(R108_exit[23])
        bmp_output["storagebiogaspressureR108"] = float(R108_exit[24])
        bmp_output["storagebiogasR108"] = float(R108_exit[25])
        bmp_output["accumbiogasR108"] = float(R108_exit[26])
        bmp_output["EnergyR108"] = float(R108_exit[27])
        bmp_output["LHVR108"] = float(R108_exit[28])

        #R109
        bmp_output["mixVelocityR109"] = float(R109_exit[0]) 
        bmp_output["SVR109"] = float(R109_exit[1])
        bmp_output["OCR109"] = float(R109_exit[2])
        bmp_output["STR109"] = float(R109_exit[3])
        bmp_output["XR109"] = float(R109_exit[4])
        bmp_output["PBMR109"] = float(R109_exit[5])
        bmp_output["KR109"] = float(R109_opt[0]/60)
        bmp_output["EaR109"] = float(R109_opt[1])
        bmp_output["lambdaR109"] = float(R109_opt[2])
        bmp_output["Objetive"] = float(R109_opt[3])
        bmp_output["TempR109"] = float(R109_exit[6])  
        bmp_output["pHR109"] = float(R109_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR109"] =float(R109_exit[8])
        bmp_output["carbondioxidemolR109"] = float(R109_exit[9])
        bmp_output["oxygenmolR109"] = float(R109_exit[10])
        bmp_output["hydrogensulfurmolR109"] = float(R109_exit[11])
        bmp_output["hydrogenmolR109"] = float(R109_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR109"] = float(R109_exit[13])
        bmp_output["carbondioxideconcentrationR109"] = float(R109_exit[14])
        bmp_output["oxygenconcentrationR109"] = float(R109_exit[15])
        bmp_output["hydrogensulfurconcentrationR109"] = float(R109_exit[16])
        bmp_output["hydrogenconcentrationR109"] = float(R109_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR109"] = float(R109_exit[18])
        bmp_output["carbondioxidevolR109"] = float(R109_exit[19])
        bmp_output["oxygenvolR109"] = float(R109_exit[20])
        bmp_output["hydrogensulfurvolR109"] = float(R109_exit[21])
        bmp_output["hydrogenvolR109"] = float(R109_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR109"] = float(R109_exit[23])
        bmp_output["storagebiogaspressureR109"] = float(R109_exit[24])
        bmp_output["storagebiogasR109"] = float(R109_exit[25])
        bmp_output["accumbiogasR109"] = float(R109_exit[26])
        bmp_output["EnergyR109"] = float(R109_exit[27])
        bmp_output["LHVR109"] = float(R109_exit[28])

        #R110
        bmp_output["mixVelocityR110"] = float(R110_exit[0]) 
        bmp_output["SVR110"] = float(R110_exit[1])
        bmp_output["OCR110"] = float(R110_exit[2])
        bmp_output["STR110"] = float(R110_exit[3])
        bmp_output["XR110"] = float(R110_exit[4])
        bmp_output["PBMR110"] = float(R110_exit[5])
        bmp_output["KR110"] = float(R110_opt[0]/60)
        bmp_output["EaR110"] = float(R110_opt[1])
        bmp_output["lambdaR110"] = float(R110_opt[2])
        bmp_output["Objetive"] = float(R110_opt[3])
        bmp_output["TempR110"] = float(R110_exit[6])  
        bmp_output["pHR110"] = float(R110_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR110"] =float(R110_exit[8])
        bmp_output["carbondioxidemolR110"] = float(R110_exit[9])
        bmp_output["oxygenmolR110"] = float(R110_exit[10])
        bmp_output["hydrogensulfurmolR110"] = float(R110_exit[11])
        bmp_output["hydrogenmolR110"] = float(R110_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR110"] = float(R110_exit[13])
        bmp_output["carbondioxideconcentrationR110"] = float(R110_exit[14])
        bmp_output["oxygenconcentrationR110"] = float(R110_exit[15])
        bmp_output["hydrogensulfurconcentrationR110"] = float(R110_exit[16])
        bmp_output["hydrogenconcentrationR110"] = float(R110_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR110"] = float(R110_exit[18])
        bmp_output["carbondioxidevolR110"] = float(R110_exit[19])
        bmp_output["oxygenvolR110"] = float(R110_exit[20])
        bmp_output["hydrogensulfurvolR110"] = float(R110_exit[21])
        bmp_output["hydrogenvolR110"] = float(R110_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR110"] = float(R110_exit[23])
        bmp_output["storagebiogaspressureR110"] = float(R110_exit[24])
        bmp_output["storagebiogasR110"] = float(R110_exit[25])
        bmp_output["accumbiogasR110"] = float(R110_exit[26])
        bmp_output["EnergyR110"] = float(R110_exit[27])
        bmp_output["LHVR110"] = float(R110_exit[28])
      
      if stateSelectionSideB == False and biogasSideB == True and TrainingMode == True:    #Online, biogas compounds in auto
        
        if user_idSideB not in bmp_instancesSideB:
          bmp_instancesSideB[user_idSideB] = BMPOnlineTrainMode.BMP_online(DB_IP= DB_IP, DB_Port=DB_Port, DB_Organization=DB_Organization, DB_Bucket=DB_Bucket, DB_Token=DB_Token, 
                                                                      MeasureMethod=measurementMethodSideB, ReactorVolume=ReactorVolumeSideB, InitialFreeVolume=InitialFreeVolumeSideB, 
                                                                      SubstrateNumber=SubstrateNumberSideB, MixRule=MixRuleSideB,
                                                                      Fraction1=Fraction1SideB, Fraction2=Fraction2SideB, Fraction3=Fraction3SideB, Fraction4=Fraction4SideB, WaterFraction=WaterFractionSideB,
                                                                      Volume1=Fraction1SideB, Volume2=Fraction2SideB, Volume3=Fraction3SideB, Volume4=Fraction4SideB, WaterVolume=WaterFractionSideB, 
                                                                      Weight1=Fraction1SideB, Weight2=Fraction2SideB, Weight3=Fraction3SideB, Weight4=Fraction4SideB, WaterWeight=WaterFractionSideB,
                                                                      ST1=ST1SideB, SV1=SV1SideB, rho1=rho1SideB, Cc1=Cc1SideB, Ch1=Ch1SideB, Co1=Co1SideB,Cn1=Cn1SideB, Cs1=Cs1SideB,
                                                                      ST2=ST2SideB, SV2=SV2SideB, rho2=rho2SideB, Cc2=Cc2SideB, Ch2=Ch2SideB, Co2=Co2SideB,Cn2=Cn2SideB, Cs2=Cs2SideB,
                                                                      ST3=ST3SideB, SV3=SV3SideB, rho3=rho3SideB, Cc3=Cc3SideB, Ch3=Ch3SideB, Co3=Co3SideB,Cn3=Cn3SideB, Cs3=Cs3SideB,
                                                                      ST4=ST4SideB, SV4=SV4SideB, rho4=rho4SideB, Cc4=Cc4SideB, Ch4=Ch4SideB, Co4=Co4SideB,Cn4=Cn4SideB, Cs4=Cs4SideB,
                                                                      OperationMethod = OperationMethodSideB, Model=ModelSideB)

        SideB = bmp_instancesSideB[user_idSideB]
        if user_data_sideB not in data_instancesSideB:
          SideB.GetData(SideA=False, SideB=True, TrainTime=TrainTimeSideB)
          DataSideB = SideB.PlantSideB
          DataInterfaz = SideB.PlantEstimation
          SideB.ProcessData(SideA = False, SideB = True, MeasureMethodSideA = measurementMethodSideB, MeasureMethodSideB = measurementMethodSideB, DataPlantSideA = DataSideB, DataPlantSideB = DataSideB,  
                           DataEstimation = DataInterfaz, OperationMethod = OperationMethodSideB)
          R106_data = SideB.R106_data
          R107_data = SideB.R107_data
          R108_data = SideB.R108_data
          R109_data = SideB.R109_data
          R110_data = SideB.R110_data
          if SideB.OperationMethod in ["Time", "Injection"]:
            SideB.SubstrateFeeding()
          
          R106 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R106", ReactorData = R106_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R107 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R107", ReactorData = R107_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R108 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R108", ReactorData = R108_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R109 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R109", ReactorData = R109_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          R110 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R110", ReactorData = R110_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
          data_instancesSideB[user_data_sideB] = [R106, R107, R108, R109, R110]
        
        R106_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R106", ReactorData = data_instancesSideB[user_data_sideB][0], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R107_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R107", ReactorData = data_instancesSideB[user_data_sideB][1], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R108_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R108", ReactorData = data_instancesSideB[user_data_sideB][2], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R109_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R109", ReactorData = data_instancesSideB[user_data_sideB][3], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        R110_opt = SideB.ReactorOptimization(Model = ModelSideB, iterations_counts = iteration, Reactorname = "R110", ReactorData = data_instancesSideB[user_data_sideB][4], ReactorVolume = ReactorVolumeSideB, OperationMethod = OperationMethodSideB)
        
        R106_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R106", ReactorData = data_instancesSideB[user_data_sideB][0], Vrxn = ReactorVolumeSideB)
        R107_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R107", ReactorData = data_instancesSideB[user_data_sideB][1], Vrxn = ReactorVolumeSideB)
        R108_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R108", ReactorData = data_instancesSideB[user_data_sideB][2], Vrxn = ReactorVolumeSideB)
        R109_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R109", ReactorData = data_instancesSideB[user_data_sideB][3], Vrxn = ReactorVolumeSideB)
        R110_exit = SideB.exit_variable_training (iterations_counts = iteration, ReactorName = "R110", ReactorData = data_instancesSideB[user_data_sideB][4], Vrxn = ReactorVolumeSideB)
        #Output variables
        #R106
        bmp_output["mixVelocityR106"] = float(R106_exit[0]) 
        bmp_output["SVR106"] = float(R106_exit[1])
        bmp_output["OCR106"] = float(R106_exit[2])
        bmp_output["STR106"] = float(R106_exit[3])
        bmp_output["XR106"] = float(R106_exit[4])
        bmp_output["PBMR106"] = float(R106_exit[5])
        bmp_output["KR106"] = float(R106_opt[0]/60)
        bmp_output["EaR106"] = float(R106_opt[1])
        bmp_output["lambdaR106"] = float(R106_opt[2])
        bmp_output["Objetive"] = float(R106_opt[3])
        bmp_output["TempR106"] = float(R106_exit[6])  
        bmp_output["pHR106"] = float(R106_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR106"] =float(R106_exit[8])
        bmp_output["carbondioxidemolR106"] = float(R106_exit[9])
        bmp_output["oxygenmolR106"] = float(R106_exit[10])
        bmp_output["hydrogensulfurmolR106"] = float(R106_exit[11])
        bmp_output["hydrogenmolR106"] = float(R106_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR106"] = float(R106_exit[13])
        bmp_output["carbondioxideconcentrationR106"] = float(R106_exit[14])
        bmp_output["oxygenconcentrationR106"] = float(R106_exit[15])
        bmp_output["hydrogensulfurconcentrationR106"] = float(R106_exit[16])
        bmp_output["hydrogenconcentrationR106"] = float(R106_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR106"] = float(R106_exit[18])
        bmp_output["carbondioxidevolR106"] = float(R106_exit[19])
        bmp_output["oxygenvolR106"] = float(R106_exit[20])
        bmp_output["hydrogensulfurvolR106"] = float(R106_exit[21])
        bmp_output["hydrogenvolR106"] = float(R106_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR106"] = float(R106_exit[23])
        bmp_output["storagebiogaspressureR106"] = float(R106_exit[24])
        bmp_output["storagebiogasR106"] = float(R106_exit[25])
        bmp_output["accumbiogasR106"] = float(R106_exit[26])
        bmp_output["EnergyR106"] = float(R106_exit[27])
        bmp_output["LHVR106"] = float(R106_exit[28])

        #R107
        bmp_output["mixVelocityR107"] = float(R107_exit[0]) 
        bmp_output["SVR107"] = float(R107_exit[1])
        bmp_output["OCR107"] = float(R107_exit[2])
        bmp_output["STR107"] = float(R107_exit[3])
        bmp_output["XR107"] = float(R107_exit[4])
        bmp_output["PBMR107"] = float(R107_exit[5])
        bmp_output["KR107"] = float(R107_opt[0]/60)
        bmp_output["EaR107"] = float(R107_opt[1])
        bmp_output["lambdaR107"] = float(R107_opt[2])
        bmp_output["Objetive"] = float(R107_opt[3])
        bmp_output["TempR107"] = float(R107_exit[6])  
        bmp_output["pHR107"] = float(R107_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR107"] =float(R107_exit[8])
        bmp_output["carbondioxidemolR107"] = float(R107_exit[9])
        bmp_output["oxygenmolR107"] = float(R107_exit[10])
        bmp_output["hydrogensulfurmolR107"] = float(R107_exit[11])
        bmp_output["hydrogenmolR107"] = float(R107_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR107"] = float(R107_exit[13])
        bmp_output["carbondioxideconcentrationR107"] = float(R107_exit[14])
        bmp_output["oxygenconcentrationR107"] = float(R107_exit[15])
        bmp_output["hydrogensulfurconcentrationR107"] = float(R107_exit[16])
        bmp_output["hydrogenconcentrationR107"] = float(R107_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR107"] = float(R107_exit[18])
        bmp_output["carbondioxidevolR107"] = float(R107_exit[19])
        bmp_output["oxygenvolR107"] = float(R107_exit[20])
        bmp_output["hydrogensulfurvolR107"] = float(R107_exit[21])
        bmp_output["hydrogenvolR107"] = float(R107_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR107"] = float(R107_exit[23])
        bmp_output["storagebiogaspressureR107"] = float(R107_exit[24])
        bmp_output["storagebiogasR107"] = float(R107_exit[25])
        bmp_output["accumbiogasR107"] = float(R107_exit[26])
        bmp_output["EnergyR107"] = float(R107_exit[27])
        bmp_output["LHVR107"] = float(R107_exit[28])

        #R108
        bmp_output["mixVelocityR108"] = float(R108_exit[0]) 
        bmp_output["SVR108"] = float(R108_exit[1])
        bmp_output["OCR108"] = float(R108_exit[2])
        bmp_output["STR108"] = float(R108_exit[3])
        bmp_output["XR108"] = float(R108_exit[4])
        bmp_output["PBMR108"] = float(R108_exit[5])
        bmp_output["KR108"] = float(R108_opt[0]/60)
        bmp_output["EaR108"] = float(R108_opt[1])
        bmp_output["lambdaR108"] = float(R108_opt[2])
        bmp_output["Objetive"] = float(R108_opt[3])
        bmp_output["TempR108"] = float(R108_exit[6])  
        bmp_output["pHR108"] = float(R108_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR108"] =float(R108_exit[8])
        bmp_output["carbondioxidemolR108"] = float(R108_exit[9])
        bmp_output["oxygenmolR108"] = float(R108_exit[10])
        bmp_output["hydrogensulfurmolR108"] = float(R108_exit[11])
        bmp_output["hydrogenmolR108"] = float(R108_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR108"] = float(R108_exit[13])
        bmp_output["carbondioxideconcentrationR108"] = float(R108_exit[14])
        bmp_output["oxygenconcentrationR108"] = float(R108_exit[15])
        bmp_output["hydrogensulfurconcentrationR108"] = float(R108_exit[16])
        bmp_output["hydrogenconcentrationR108"] = float(R108_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR108"] = float(R108_exit[18])
        bmp_output["carbondioxidevolR108"] = float(R108_exit[19])
        bmp_output["oxygenvolR108"] = float(R108_exit[20])
        bmp_output["hydrogensulfurvolR108"] = float(R108_exit[21])
        bmp_output["hydrogenvolR108"] = float(R108_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR108"] = float(R108_exit[23])
        bmp_output["storagebiogaspressureR108"] = float(R108_exit[24])
        bmp_output["storagebiogasR108"] = float(R108_exit[25])
        bmp_output["accumbiogasR108"] = float(R108_exit[26])
        bmp_output["EnergyR108"] = float(R108_exit[27])
        bmp_output["LHVR108"] = float(R108_exit[28])

        #R109
        bmp_output["mixVelocityR109"] = float(R109_exit[0]) 
        bmp_output["SVR109"] = float(R109_exit[1])
        bmp_output["OCR109"] = float(R109_exit[2])
        bmp_output["STR109"] = float(R109_exit[3])
        bmp_output["XR109"] = float(R109_exit[4])
        bmp_output["PBMR109"] = float(R109_exit[5])
        bmp_output["KR109"] = float(R109_opt[0]/60)
        bmp_output["EaR109"] = float(R109_opt[1])
        bmp_output["lambdaR109"] = float(R109_opt[2])
        bmp_output["Objetive"] = float(R109_opt[3])
        bmp_output["TempR109"] = float(R109_exit[6])  
        bmp_output["pHR109"] = float(R109_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR109"] =float(R109_exit[8])
        bmp_output["carbondioxidemolR109"] = float(R109_exit[9])
        bmp_output["oxygenmolR109"] = float(R109_exit[10])
        bmp_output["hydrogensulfurmolR109"] = float(R109_exit[11])
        bmp_output["hydrogenmolR109"] = float(R109_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR109"] = float(R109_exit[13])
        bmp_output["carbondioxideconcentrationR109"] = float(R109_exit[14])
        bmp_output["oxygenconcentrationR109"] = float(R109_exit[15])
        bmp_output["hydrogensulfurconcentrationR109"] = float(R109_exit[16])
        bmp_output["hydrogenconcentrationR109"] = float(R109_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR109"] = float(R109_exit[18])
        bmp_output["carbondioxidevolR109"] = float(R109_exit[19])
        bmp_output["oxygenvolR109"] = float(R109_exit[20])
        bmp_output["hydrogensulfurvolR109"] = float(R109_exit[21])
        bmp_output["hydrogenvolR109"] = float(R109_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR109"] = float(R109_exit[23])
        bmp_output["storagebiogaspressureR109"] = float(R109_exit[24])
        bmp_output["storagebiogasR109"] = float(R109_exit[25])
        bmp_output["accumbiogasR109"] = float(R109_exit[26])
        bmp_output["EnergyR109"] = float(R109_exit[27])
        bmp_output["LHVR109"] = float(R109_exit[28])

        #R110
        bmp_output["mixVelocityR110"] = float(R110_exit[0]) 
        bmp_output["SVR110"] = float(R110_exit[1])
        bmp_output["OCR110"] = float(R110_exit[2])
        bmp_output["STR110"] = float(R110_exit[3])
        bmp_output["XR110"] = float(R110_exit[4])
        bmp_output["PBMR110"] = float(R110_exit[5])
        bmp_output["KR110"] = float(R110_opt[0]/60)
        bmp_output["EaR110"] = float(R110_opt[1])
        bmp_output["lambdaR110"] = float(R110_opt[2])
        bmp_output["Objetive"] = float(R110_opt[3])
        bmp_output["TempR110"] = float(R110_exit[6])  
        bmp_output["pHR110"] = float(R110_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR110"] =float(R110_exit[8])
        bmp_output["carbondioxidemolR110"] = float(R110_exit[9])
        bmp_output["oxygenmolR110"] = float(R110_exit[10])
        bmp_output["hydrogensulfurmolR110"] = float(R110_exit[11])
        bmp_output["hydrogenmolR110"] = float(R110_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR110"] = float(R110_exit[13])
        bmp_output["carbondioxideconcentrationR110"] = float(R110_exit[14])
        bmp_output["oxygenconcentrationR110"] = float(R110_exit[15])
        bmp_output["hydrogensulfurconcentrationR110"] = float(R110_exit[16])
        bmp_output["hydrogenconcentrationR110"] = float(R110_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR110"] = float(R110_exit[18])
        bmp_output["carbondioxidevolR110"] = float(R110_exit[19])
        bmp_output["oxygenvolR110"] = float(R110_exit[20])
        bmp_output["hydrogensulfurvolR110"] = float(R110_exit[21])
        bmp_output["hydrogenvolR110"] = float(R110_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR110"] = float(R110_exit[23])
        bmp_output["storagebiogaspressureR110"] = float(R110_exit[24])
        bmp_output["storagebiogasR110"] = float(R110_exit[25])
        bmp_output["accumbiogasR110"] = float(R110_exit[26])
        bmp_output["EnergyR110"] = float(R110_exit[27])
        bmp_output["LHVR110"] = float(R110_exit[28])
      
      if stateSelectionSideB == False and biogasSideB == True and TrainingMode == False:    #Online, biogas compounds in auto, No training
        
        if user_idSideB not in bmp_instancesSideB:
          bmp_instancesSideB[user_idSideB] = BMPOnlineTrainMode.BMP_online(DB_IP= DB_IP, DB_Port=DB_Port, DB_Organization=DB_Organization, DB_Bucket=DB_Bucket, DB_Token=DB_Token, 
                                                                      MeasureMethod=measurementMethodSideB, ReactorVolume=ReactorVolumeSideB, InitialFreeVolume=InitialFreeVolumeSideB, 
                                                                      SubstrateNumber=SubstrateNumberSideB, MixRule=MixRuleSideB,
                                                                      Fraction1=Fraction1SideB, Fraction2=Fraction2SideB, Fraction3=Fraction3SideB, Fraction4=Fraction4SideB, WaterFraction=WaterFractionSideB,
                                                                      Volume1=Fraction1SideB, Volume2=Fraction2SideB, Volume3=Fraction3SideB, Volume4=Fraction4SideB, WaterVolume=WaterFractionSideB, 
                                                                      Weight1=Fraction1SideB, Weight2=Fraction2SideB, Weight3=Fraction3SideB, Weight4=Fraction4SideB, WaterWeight=WaterFractionSideB,
                                                                      ST1=ST1SideB, SV1=SV1SideB, rho1=rho1SideB, Cc1=Cc1SideB, Ch1=Ch1SideB, Co1=Co1SideB,Cn1=Cn1SideB, Cs1=Cs1SideB,
                                                                      ST2=ST2SideB, SV2=SV2SideB, rho2=rho2SideB, Cc2=Cc2SideB, Ch2=Ch2SideB, Co2=Co2SideB,Cn2=Cn2SideB, Cs2=Cs2SideB,
                                                                      ST3=ST3SideB, SV3=SV3SideB, rho3=rho3SideB, Cc3=Cc3SideB, Ch3=Ch3SideB, Co3=Co3SideB,Cn3=Cn3SideB, Cs3=Cs3SideB,
                                                                      ST4=ST4SideB, SV4=SV4SideB, rho4=rho4SideB, Cc4=Cc4SideB, Ch4=Ch4SideB, Co4=Co4SideB,Cn4=Cn4SideB, Cs4=Cs4SideB,
                                                                      OperationMethod = OperationMethodSideB, Model=ModelSideB)

        SideB = bmp_instancesSideB[user_idSideB]
        
        SideB.GetData(SideA=False, SideB=True, TrainTime=TrainTimeSideB)
        DataSideB = SideB.PlantSideB
        DataInterfaz = SideB.PlantEstimation
        SideB.ProcessData(SideA = False, SideB = True, MeasureMethodSideA = measurementMethodSideB, MeasureMethodSideB = measurementMethodSideB, DataPlantSideA = DataSideB, DataPlantSideB = DataSideB,  
                          DataEstimation = DataInterfaz, OperationMethod = OperationMethodSideB)
        R106_data = SideB.R106_data
        R107_data = SideB.R107_data
        R108_data = SideB.R108_data
        R109_data = SideB.R109_data
        R110_data = SideB.R110_data
        if SideB.OperationMethod in ["Time", "Injection"]:
          SideB.SubstrateFeeding()
        
        R106 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R106", ReactorData = R106_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        R107 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R107", ReactorData = R107_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        R108 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R108", ReactorData = R108_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        R109 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R109", ReactorData = R109_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        R110 = SideB.StochoimetricExpendtire_Reactor(ReactorName="R110", ReactorData = R110_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        data_instancesSideB[user_data_sideB] = [R106, R107, R108, R109, R110]
               
        R106_exit = SideB.exit_variable_online (iterations_counts = iteration, ReactorName = "R106", ReactorData = data_instancesSideB[user_data_sideB][0], Vrxn = ReactorVolumeSideB)
        R107_exit = SideB.exit_variable_online (iterations_counts = iteration, ReactorName = "R107", ReactorData = data_instancesSideB[user_data_sideB][1], Vrxn = ReactorVolumeSideB)
        R108_exit = SideB.exit_variable_online (iterations_counts = iteration, ReactorName = "R108", ReactorData = data_instancesSideB[user_data_sideB][2], Vrxn = ReactorVolumeSideB)
        R109_exit = SideB.exit_variable_online (iterations_counts = iteration, ReactorName = "R109", ReactorData = data_instancesSideB[user_data_sideB][3], Vrxn = ReactorVolumeSideB)
        R110_exit = SideB.exit_variable_online (iterations_counts = iteration, ReactorName = "R110", ReactorData = data_instancesSideB[user_data_sideB][4], Vrxn = ReactorVolumeSideB)
        #Output variables
        #R106
        bmp_output["mixVelocityR106"] = float(R106_exit[0]) 
        bmp_output["SVR106"] = float(R106_exit[1])
        bmp_output["OCR106"] = float(R106_exit[2])
        bmp_output["STR106"] = float(R106_exit[3])
        bmp_output["XR106"] = float(R106_exit[4])
        bmp_output["PBMR106"] = float(R106_exit[5])
        bmp_output["KR106"] = KSideB
        bmp_output["EaR106"] = EaSideB
        bmp_output["lambdaR106"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR106"] = float(R106_exit[6])  
        bmp_output["pHR106"] = float(R106_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR106"] =float(R106_exit[8])
        bmp_output["carbondioxidemolR106"] = float(R106_exit[9])
        bmp_output["oxygenmolR106"] = float(R106_exit[10])
        bmp_output["hydrogensulfurmolR106"] = float(R106_exit[11])
        bmp_output["hydrogenmolR106"] = float(R106_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR106"] = float(R106_exit[13])
        bmp_output["carbondioxideconcentrationR106"] = float(R106_exit[14])
        bmp_output["oxygenconcentrationR106"] = float(R106_exit[15])
        bmp_output["hydrogensulfurconcentrationR106"] = float(R106_exit[16])
        bmp_output["hydrogenconcentrationR106"] = float(R106_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR106"] = float(R106_exit[18])
        bmp_output["carbondioxidevolR106"] = float(R106_exit[19])
        bmp_output["oxygenvolR106"] = float(R106_exit[20])
        bmp_output["hydrogensulfurvolR106"] = float(R106_exit[21])
        bmp_output["hydrogenvolR106"] = float(R106_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR106"] = float(R106_exit[23])
        bmp_output["storagebiogaspressureR106"] = float(R106_exit[24])
        bmp_output["storagebiogasR106"] = float(R106_exit[25])
        bmp_output["accumbiogasR106"] = float(R106_exit[26])
        bmp_output["EnergyR106"] = float(R106_exit[27])
        bmp_output["LHVR106"] = float(R106_exit[28])

        #R107
        bmp_output["mixVelocityR107"] = float(R107_exit[0]) 
        bmp_output["SVR107"] = float(R107_exit[1])
        bmp_output["OCR107"] = float(R107_exit[2])
        bmp_output["STR107"] = float(R107_exit[3])
        bmp_output["XR107"] = float(R107_exit[4])
        bmp_output["PBMR107"] = float(R107_exit[5])
        bmp_output["KR107"] = KSideB
        bmp_output["EaR107"] = EaSideB
        bmp_output["lambdaR107"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR107"] = float(R107_exit[6])  
        bmp_output["pHR107"] = float(R107_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR107"] =float(R107_exit[8])
        bmp_output["carbondioxidemolR107"] = float(R107_exit[9])
        bmp_output["oxygenmolR107"] = float(R107_exit[10])
        bmp_output["hydrogensulfurmolR107"] = float(R107_exit[11])
        bmp_output["hydrogenmolR107"] = float(R107_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR107"] = float(R107_exit[13])
        bmp_output["carbondioxideconcentrationR107"] = float(R107_exit[14])
        bmp_output["oxygenconcentrationR107"] = float(R107_exit[15])
        bmp_output["hydrogensulfurconcentrationR107"] = float(R107_exit[16])
        bmp_output["hydrogenconcentrationR107"] = float(R107_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR107"] = float(R107_exit[18])
        bmp_output["carbondioxidevolR107"] = float(R107_exit[19])
        bmp_output["oxygenvolR107"] = float(R107_exit[20])
        bmp_output["hydrogensulfurvolR107"] = float(R107_exit[21])
        bmp_output["hydrogenvolR107"] = float(R107_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR107"] = float(R107_exit[23])
        bmp_output["storagebiogaspressureR107"] = float(R107_exit[24])
        bmp_output["storagebiogasR107"] = float(R107_exit[25])
        bmp_output["accumbiogasR107"] = float(R107_exit[26])
        bmp_output["EnergyR107"] = float(R107_exit[27])
        bmp_output["LHVR107"] = float(R107_exit[28])

        #R108
        bmp_output["mixVelocityR108"] = float(R108_exit[0]) 
        bmp_output["SVR108"] = float(R108_exit[1])
        bmp_output["OCR108"] = float(R108_exit[2])
        bmp_output["STR108"] = float(R108_exit[3])
        bmp_output["XR108"] = float(R108_exit[4])
        bmp_output["PBMR108"] = float(R108_exit[5])
        bmp_output["KR108"] = KSideB
        bmp_output["EaR108"] = EaSideB
        bmp_output["lambdaR108"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR108"] = float(R108_exit[6])  
        bmp_output["pHR108"] = float(R108_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR108"] =float(R108_exit[8])
        bmp_output["carbondioxidemolR108"] = float(R108_exit[9])
        bmp_output["oxygenmolR108"] = float(R108_exit[10])
        bmp_output["hydrogensulfurmolR108"] = float(R108_exit[11])
        bmp_output["hydrogenmolR108"] = float(R108_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR108"] = float(R108_exit[13])
        bmp_output["carbondioxideconcentrationR108"] = float(R108_exit[14])
        bmp_output["oxygenconcentrationR108"] = float(R108_exit[15])
        bmp_output["hydrogensulfurconcentrationR108"] = float(R108_exit[16])
        bmp_output["hydrogenconcentrationR108"] = float(R108_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR108"] = float(R108_exit[18])
        bmp_output["carbondioxidevolR108"] = float(R108_exit[19])
        bmp_output["oxygenvolR108"] = float(R108_exit[20])
        bmp_output["hydrogensulfurvolR108"] = float(R108_exit[21])
        bmp_output["hydrogenvolR108"] = float(R108_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR108"] = float(R108_exit[23])
        bmp_output["storagebiogaspressureR108"] = float(R108_exit[24])
        bmp_output["storagebiogasR108"] = float(R108_exit[25])
        bmp_output["accumbiogasR108"] = float(R108_exit[26])
        bmp_output["EnergyR108"] = float(R108_exit[27])
        bmp_output["LHVR108"] = float(R108_exit[28])

        #R109
        bmp_output["mixVelocityR109"] = float(R109_exit[0]) 
        bmp_output["SVR109"] = float(R109_exit[1])
        bmp_output["OCR109"] = float(R109_exit[2])
        bmp_output["STR109"] = float(R109_exit[3])
        bmp_output["XR109"] = float(R109_exit[4])
        bmp_output["PBMR109"] = float(R109_exit[5])
        bmp_output["KR109"] = KSideB
        bmp_output["EaR109"] = EaSideB
        bmp_output["lambdaR109"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR109"] = float(R109_exit[6])  
        bmp_output["pHR109"] = float(R109_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR109"] =float(R109_exit[8])
        bmp_output["carbondioxidemolR109"] = float(R109_exit[9])
        bmp_output["oxygenmolR109"] = float(R109_exit[10])
        bmp_output["hydrogensulfurmolR109"] = float(R109_exit[11])
        bmp_output["hydrogenmolR109"] = float(R109_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR109"] = float(R109_exit[13])
        bmp_output["carbondioxideconcentrationR109"] = float(R109_exit[14])
        bmp_output["oxygenconcentrationR109"] = float(R109_exit[15])
        bmp_output["hydrogensulfurconcentrationR109"] = float(R109_exit[16])
        bmp_output["hydrogenconcentrationR109"] = float(R109_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR109"] = float(R109_exit[18])
        bmp_output["carbondioxidevolR109"] = float(R109_exit[19])
        bmp_output["oxygenvolR109"] = float(R109_exit[20])
        bmp_output["hydrogensulfurvolR109"] = float(R109_exit[21])
        bmp_output["hydrogenvolR109"] = float(R109_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR109"] = float(R109_exit[23])
        bmp_output["storagebiogaspressureR109"] = float(R109_exit[24])
        bmp_output["storagebiogasR109"] = float(R109_exit[25])
        bmp_output["accumbiogasR109"] = float(R109_exit[26])
        bmp_output["EnergyR109"] = float(R109_exit[27])
        bmp_output["LHVR109"] = float(R109_exit[28])

        #R110
        bmp_output["mixVelocityR110"] = float(R110_exit[0]) 
        bmp_output["SVR110"] = float(R110_exit[1])
        bmp_output["OCR110"] = float(R110_exit[2])
        bmp_output["STR110"] = float(R110_exit[3])
        bmp_output["XR110"] = float(R110_exit[4])
        bmp_output["PBMR110"] = float(R110_exit[5])
        bmp_output["KR110"] = KSideB
        bmp_output["EaR110"] = EaSideB
        bmp_output["lambdaR110"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR110"] = float(R110_exit[6])  
        bmp_output["pHR110"] = float(R110_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR110"] =float(R110_exit[8])
        bmp_output["carbondioxidemolR110"] = float(R110_exit[9])
        bmp_output["oxygenmolR110"] = float(R110_exit[10])
        bmp_output["hydrogensulfurmolR110"] = float(R110_exit[11])
        bmp_output["hydrogenmolR110"] = float(R110_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR110"] = float(R110_exit[13])
        bmp_output["carbondioxideconcentrationR110"] = float(R110_exit[14])
        bmp_output["oxygenconcentrationR110"] = float(R110_exit[15])
        bmp_output["hydrogensulfurconcentrationR110"] = float(R110_exit[16])
        bmp_output["hydrogenconcentrationR110"] = float(R110_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR110"] = float(R110_exit[18])
        bmp_output["carbondioxidevolR110"] = float(R110_exit[19])
        bmp_output["oxygenvolR110"] = float(R110_exit[20])
        bmp_output["hydrogensulfurvolR110"] = float(R110_exit[21])
        bmp_output["hydrogenvolR110"] = float(R110_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR110"] = float(R110_exit[23])
        bmp_output["storagebiogaspressureR110"] = float(R110_exit[24])
        bmp_output["storagebiogasR110"] = float(R110_exit[25])
        bmp_output["accumbiogasR110"] = float(R110_exit[26])
        bmp_output["EnergyR110"] = float(R110_exit[27])
        bmp_output["LHVR110"] = float(R110_exit[28])
      
      if stateSelectionSideB == False and biogasSideB == False and TrainingMode == False:    #Online, biogas compounds in auto
        
        if user_idSideB not in bmp_instancesSideB:
          bmp_instancesSideB[user_idSideB] = BMPOnlineTrainMode.BMP_online(DB_IP= DB_IP, DB_Port=DB_Port, DB_Organization=DB_Organization, DB_Bucket=DB_Bucket, DB_Token=DB_Token, 
                                                                      MeasureMethod=measurementMethodSideB, ReactorVolume=ReactorVolumeSideB, InitialFreeVolume=InitialFreeVolumeSideB, 
                                                                      SubstrateNumber=SubstrateNumberSideB, MixRule=MixRuleSideB,
                                                                      Fraction1=Fraction1SideB, Fraction2=Fraction2SideB, Fraction3=Fraction3SideB, Fraction4=Fraction4SideB, WaterFraction=WaterFractionSideB,
                                                                      Volume1=Fraction1SideB, Volume2=Fraction2SideB, Volume3=Fraction3SideB, Volume4=Fraction4SideB, WaterVolume=WaterFractionSideB, 
                                                                      Weight1=Fraction1SideB, Weight2=Fraction2SideB, Weight3=Fraction3SideB, Weight4=Fraction4SideB, WaterWeight=WaterFractionSideB,
                                                                      ST1=ST1SideB, SV1=SV1SideB, rho1=rho1SideB, Cc1=Cc1SideB, Ch1=Ch1SideB, Co1=Co1SideB,Cn1=Cn1SideB, Cs1=Cs1SideB,
                                                                      ST2=ST2SideB, SV2=SV2SideB, rho2=rho2SideB, Cc2=Cc2SideB, Ch2=Ch2SideB, Co2=Co2SideB,Cn2=Cn2SideB, Cs2=Cs2SideB,
                                                                      ST3=ST3SideB, SV3=SV3SideB, rho3=rho3SideB, Cc3=Cc3SideB, Ch3=Ch3SideB, Co3=Co3SideB,Cn3=Cn3SideB, Cs3=Cs3SideB,
                                                                      ST4=ST4SideB, SV4=SV4SideB, rho4=rho4SideB, Cc4=Cc4SideB, Ch4=Ch4SideB, Co4=Co4SideB,Cn4=Cn4SideB, Cs4=Cs4SideB,
                                                                      OperationMethod = OperationMethodSideB, Model=ModelSideB)

        SideB = bmp_instancesSideB[user_idSideB]
        
        SideB.GetData(SideA=False, SideB=True, TrainTime=TrainTimeSideB)
        DataSideB = SideB.PlantSideB
        DataInterfaz = SideB.PlantEstimation
        SideB.ProcessData(SideA = False, SideB = True, MeasureMethodSideA = measurementMethodSideB, MeasureMethodSideB = measurementMethodSideB, DataPlantSideA = DataSideB, DataPlantSideB = DataSideB,  
                          DataEstimation = DataInterfaz, OperationMethod = OperationMethodSideB)
        R106_data = SideB.R106_data
        R107_data = SideB.R107_data
        R108_data = SideB.R108_data
        R109_data = SideB.R109_data
        R110_data = SideB.R110_data
        if SideB.OperationMethod in ["Time", "Injection"]:
          SideB.SubstrateFeeding()
        
        R106 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R106", ReactorData = R106_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        R107 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R107", ReactorData = R107_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        R108 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R108", ReactorData = R108_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        R109 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R109", ReactorData = R109_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        R110 = SideB.StochoimetricExpendtire_Reactor_batch(ReactorName="R110", ReactorData = R110_data, Vrxn = ReactorVolumeSideB, OperationMethod=OperationMethodSideB)
        data_instancesSideB[user_data_sideB] = [R106, R107, R108, R109, R110]
               
        R106_exit = SideB.exit_variable_online (ReactorName = "R106", ReactorData = data_instancesSideB[user_data_sideB][0], Vrxn = ReactorVolumeSideB)
        R107_exit = SideB.exit_variable_online (ReactorName = "R107", ReactorData = data_instancesSideB[user_data_sideB][1], Vrxn = ReactorVolumeSideB)
        R108_exit = SideB.exit_variable_online (ReactorName = "R108", ReactorData = data_instancesSideB[user_data_sideB][2], Vrxn = ReactorVolumeSideB)
        R109_exit = SideB.exit_variable_online (ReactorName = "R109", ReactorData = data_instancesSideB[user_data_sideB][3], Vrxn = ReactorVolumeSideB)
        R110_exit = SideB.exit_variable_online (ReactorName = "R110", ReactorData = data_instancesSideB[user_data_sideB][4], Vrxn = ReactorVolumeSideB)
        #Output variables
        #R106
        bmp_output["mixVelocityR106"] = float(R106_exit[0]) 
        bmp_output["SVR106"] = float(R106_exit[1])
        bmp_output["OCR106"] = float(R106_exit[2])
        bmp_output["STR106"] = float(R106_exit[3])
        bmp_output["XR106"] = float(R106_exit[4])
        bmp_output["PBMR106"] = float(R106_exit[5])
        bmp_output["KR106"] = KSideB
        bmp_output["EaR106"] = EaSideB
        bmp_output["lambdaR106"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR106"] = float(R106_exit[6])  
        bmp_output["pHR106"] = float(R106_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR106"] =float(R106_exit[8])
        bmp_output["carbondioxidemolR106"] = float(R106_exit[9])
        bmp_output["oxygenmolR106"] = float(R106_exit[10])
        bmp_output["hydrogensulfurmolR106"] = float(R106_exit[11])
        bmp_output["hydrogenmolR106"] = float(R106_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR106"] = float(R106_exit[13])
        bmp_output["carbondioxideconcentrationR106"] = float(R106_exit[14])
        bmp_output["oxygenconcentrationR106"] = float(R106_exit[15])
        bmp_output["hydrogensulfurconcentrationR106"] = float(R106_exit[16])
        bmp_output["hydrogenconcentrationR106"] = float(R106_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR106"] = float(R106_exit[18])
        bmp_output["carbondioxidevolR106"] = float(R106_exit[19])
        bmp_output["oxygenvolR106"] = float(R106_exit[20])
        bmp_output["hydrogensulfurvolR106"] = float(R106_exit[21])
        bmp_output["hydrogenvolR106"] = float(R106_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR106"] = float(R106_exit[23])
        bmp_output["storagebiogaspressureR106"] = float(R106_exit[24])
        bmp_output["storagebiogasR106"] = float(R106_exit[25])
        bmp_output["accumbiogasR106"] = float(R106_exit[26])
        bmp_output["EnergyR106"] = float(R106_exit[27])
        bmp_output["LHVR106"] = float(R106_exit[28])

        #R107
        bmp_output["mixVelocityR107"] = float(R107_exit[0]) 
        bmp_output["SVR107"] = float(R107_exit[1])
        bmp_output["OCR107"] = float(R107_exit[2])
        bmp_output["STR107"] = float(R107_exit[3])
        bmp_output["XR107"] = float(R107_exit[4])
        bmp_output["PBMR107"] = float(R107_exit[5])
        bmp_output["KR107"] = KSideB
        bmp_output["EaR107"] = EaSideB
        bmp_output["lambdaR107"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR107"] = float(R107_exit[6])  
        bmp_output["pHR107"] = float(R107_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR107"] =float(R107_exit[8])
        bmp_output["carbondioxidemolR107"] = float(R107_exit[9])
        bmp_output["oxygenmolR107"] = float(R107_exit[10])
        bmp_output["hydrogensulfurmolR107"] = float(R107_exit[11])
        bmp_output["hydrogenmolR107"] = float(R107_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR107"] = float(R107_exit[13])
        bmp_output["carbondioxideconcentrationR107"] = float(R107_exit[14])
        bmp_output["oxygenconcentrationR107"] = float(R107_exit[15])
        bmp_output["hydrogensulfurconcentrationR107"] = float(R107_exit[16])
        bmp_output["hydrogenconcentrationR107"] = float(R107_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR107"] = float(R107_exit[18])
        bmp_output["carbondioxidevolR107"] = float(R107_exit[19])
        bmp_output["oxygenvolR107"] = float(R107_exit[20])
        bmp_output["hydrogensulfurvolR107"] = float(R107_exit[21])
        bmp_output["hydrogenvolR107"] = float(R107_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR107"] = float(R107_exit[23])
        bmp_output["storagebiogaspressureR107"] = float(R107_exit[24])
        bmp_output["storagebiogasR107"] = float(R107_exit[25])
        bmp_output["accumbiogasR107"] = float(R107_exit[26])
        bmp_output["EnergyR107"] = float(R107_exit[27])
        bmp_output["LHVR107"] = float(R107_exit[28])

        #R108
        bmp_output["mixVelocityR108"] = float(R108_exit[0]) 
        bmp_output["SVR108"] = float(R108_exit[1])
        bmp_output["OCR108"] = float(R108_exit[2])
        bmp_output["STR108"] = float(R108_exit[3])
        bmp_output["XR108"] = float(R108_exit[4])
        bmp_output["PBMR108"] = float(R108_exit[5])
        bmp_output["KR108"] = KSideB
        bmp_output["EaR108"] = EaSideB
        bmp_output["lambdaR108"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR108"] = float(R108_exit[6])  
        bmp_output["pHR108"] = float(R108_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR108"] =float(R108_exit[8])
        bmp_output["carbondioxidemolR108"] = float(R108_exit[9])
        bmp_output["oxygenmolR108"] = float(R108_exit[10])
        bmp_output["hydrogensulfurmolR108"] = float(R108_exit[11])
        bmp_output["hydrogenmolR108"] = float(R108_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR108"] = float(R108_exit[13])
        bmp_output["carbondioxideconcentrationR108"] = float(R108_exit[14])
        bmp_output["oxygenconcentrationR108"] = float(R108_exit[15])
        bmp_output["hydrogensulfurconcentrationR108"] = float(R108_exit[16])
        bmp_output["hydrogenconcentrationR108"] = float(R108_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR108"] = float(R108_exit[18])
        bmp_output["carbondioxidevolR108"] = float(R108_exit[19])
        bmp_output["oxygenvolR108"] = float(R108_exit[20])
        bmp_output["hydrogensulfurvolR108"] = float(R108_exit[21])
        bmp_output["hydrogenvolR108"] = float(R108_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR108"] = float(R108_exit[23])
        bmp_output["storagebiogaspressureR108"] = float(R108_exit[24])
        bmp_output["storagebiogasR108"] = float(R108_exit[25])
        bmp_output["accumbiogasR108"] = float(R108_exit[26])
        bmp_output["EnergyR108"] = float(R108_exit[27])
        bmp_output["LHVR108"] = float(R108_exit[28])

        #R109
        bmp_output["mixVelocityR109"] = float(R109_exit[0]) 
        bmp_output["SVR109"] = float(R109_exit[1])
        bmp_output["OCR109"] = float(R109_exit[2])
        bmp_output["STR109"] = float(R109_exit[3])
        bmp_output["XR109"] = float(R109_exit[4])
        bmp_output["PBMR109"] = float(R109_exit[5])
        bmp_output["KR109"] = KSideB
        bmp_output["EaR109"] = EaSideB
        bmp_output["lambdaR109"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR109"] = float(R109_exit[6])  
        bmp_output["pHR109"] = float(R109_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR109"] =float(R109_exit[8])
        bmp_output["carbondioxidemolR109"] = float(R109_exit[9])
        bmp_output["oxygenmolR109"] = float(R109_exit[10])
        bmp_output["hydrogensulfurmolR109"] = float(R109_exit[11])
        bmp_output["hydrogenmolR109"] = float(R109_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR109"] = float(R109_exit[13])
        bmp_output["carbondioxideconcentrationR109"] = float(R109_exit[14])
        bmp_output["oxygenconcentrationR109"] = float(R109_exit[15])
        bmp_output["hydrogensulfurconcentrationR109"] = float(R109_exit[16])
        bmp_output["hydrogenconcentrationR109"] = float(R109_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR109"] = float(R109_exit[18])
        bmp_output["carbondioxidevolR109"] = float(R109_exit[19])
        bmp_output["oxygenvolR109"] = float(R109_exit[20])
        bmp_output["hydrogensulfurvolR109"] = float(R109_exit[21])
        bmp_output["hydrogenvolR109"] = float(R109_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR109"] = float(R109_exit[23])
        bmp_output["storagebiogaspressureR109"] = float(R109_exit[24])
        bmp_output["storagebiogasR109"] = float(R109_exit[25])
        bmp_output["accumbiogasR109"] = float(R109_exit[26])
        bmp_output["EnergyR109"] = float(R109_exit[27])
        bmp_output["LHVR109"] = float(R109_exit[28])

        #R110
        bmp_output["mixVelocityR110"] = float(R110_exit[0]) 
        bmp_output["SVR110"] = float(R110_exit[1])
        bmp_output["OCR110"] = float(R110_exit[2])
        bmp_output["STR110"] = float(R110_exit[3])
        bmp_output["XR110"] = float(R110_exit[4])
        bmp_output["PBMR110"] = float(R110_exit[5])
        bmp_output["KR110"] = KSideB
        bmp_output["EaR110"] = EaSideB
        bmp_output["lambdaR110"] = LSideB
        bmp_output["Objetive"] = float(0)
        bmp_output["TempR110"] = float(R110_exit[6])  
        bmp_output["pHR110"] = float(R110_exit[7])
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR110"] =float(R110_exit[8])
        bmp_output["carbondioxidemolR110"] = float(R110_exit[9])
        bmp_output["oxygenmolR110"] = float(R110_exit[10])
        bmp_output["hydrogensulfurmolR110"] = float(R110_exit[11])
        bmp_output["hydrogenmolR110"] = float(R110_exit[12]) 
        #---- Gas concentration
        bmp_output["methaneconcentrationR110"] = float(R110_exit[13])
        bmp_output["carbondioxideconcentrationR110"] = float(R110_exit[14])
        bmp_output["oxygenconcentrationR110"] = float(R110_exit[15])
        bmp_output["hydrogensulfurconcentrationR110"] = float(R110_exit[16])
        bmp_output["hydrogenconcentrationR110"] = float(R110_exit[17])
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR110"] = float(R110_exit[18])
        bmp_output["carbondioxidevolR110"] = float(R110_exit[19])
        bmp_output["oxygenvolR110"] = float(R110_exit[20])
        bmp_output["hydrogensulfurvolR110"] = float(R110_exit[21])
        bmp_output["hydrogenvolR110"] = float(R110_exit[22])
        #---- Biogas general
        bmp_output["accumbiogaspressureR110"] = float(R110_exit[23])
        bmp_output["storagebiogaspressureR110"] = float(R110_exit[24])
        bmp_output["storagebiogasR110"] = float(R110_exit[25])
        bmp_output["accumbiogasR110"] = float(R110_exit[26])
        bmp_output["EnergyR110"] = float(R110_exit[27])
        bmp_output["LHVR110"] = float(R110_exit[28])
      
      #%% Offline operation
      if stateSelectionSideA == True:    #offline
        user_id106 = data["name"] + "106"
        user_id107 = data["name"] + "107"
        user_id108 = data["name"] + "108"
        user_id109 = data["name"] + "109"
        user_id110 = data["name"] + "110"
  
        users_instancesSideB = [user_id106, user_id107, user_id108, user_id109, user_id110]   

        if iteration == 1: 
          print(iteration, flush=True)  
          for key in users_instancesSideB:
            if key in bmp_instances_offline_SideB:
              del bmp_instances_offline_SideB[key]
              print("User Was delete", flush=True)
        
        # R106
        if user_id106 not in bmp_instances_offline_SideB:
          bmp_instances_offline_SideB[user_id106] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideB, ReactorVolume = ReactorVolumeSideB, InitialFreeVolume = InitialFreeVolumeSideB,
                                                                              SubstrateNumber = SubstrateNumberSideB, MixRule = MixRuleSideB, 
                                                                              Fraction1 = Fraction1SideB, Fraction2 = Fraction2SideB, Fraction3 = Fraction3SideB, Fraction4 = Fraction4SideB, WaterFraction = WaterFractionSideB,
                                                                              Volume1 = Fraction1SideB, Volume2 = Fraction2SideB, Volume3 = Fraction3SideB, Volume4 = Fraction4SideB, WaterVolume = WaterFractionSideB,
                                                                              Weight1 = Fraction1SideB, Weight2 = Fraction2SideB, Weight3 = Fraction3SideB, Weight4 = Fraction4SideB, WaterWeight = WaterFractionSideB,
                                                                              ST1 = ST1SideB, SV1 = SV1SideB, rho1 = rho1SideB, Cc1 = Cc1SideB, Ch1 = Ch1SideB, Co1 = Co1SideB, Cn1 = Cn1SideB, Cs1 = Cs1SideB,
                                                                              ST2 = ST2SideB, SV2 = SV2SideB, rho2 = rho2SideB, Cc2 = Cc2SideB, Ch2 = Ch2SideB, Co2 = Co2SideB, Cn2 = Cn2SideB, Cs2 = Cs2SideB,
                                                                              ST3 = ST3SideB, SV3 = SV3SideB, rho3 = rho3SideB, Cc3 = Cc3SideB, Ch3 = Ch3SideB, Co3 = Co3SideB, Cn3 = Cn3SideB, Cs3 = Cs3SideB,
                                                                              ST4 = ST4SideB, SV4 = SV4SideB, rho4 = rho4SideB, Cc4 = Cc4SideB, Ch4 = Ch4SideB, Co4 = Co4SideB, Cn4 = Cn4SideB, Cs4 = Cs4SideB,
                                                                              OperationMethod = OperationMethodSideB, tp = time_stepSideB)  
        
        R106 = bmp_instances_offline_SideB[user_id106]

        #Mixing R106
        R106.MixControl(MixVelocity = MixVelocitySideB, MixTime = mixTimeSideB, DailyMixing = mixDailySideB, speed_time = speed_time)
        bmp_output["mixVelocityR106"] = R106.MixVelocity

        if OperationMethodSideB in ["Time", "Injection"]:
          R106.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R106.SubstrateFeed(Mode = OperationMethodSideB, Volume = dosificationVolumeSideB, Time = dailyInyectionsSideB, Inyections = dailyInyectionsSideB, Q=3.4, speed_time = speed_time)
        bmp_output["caudalsideB"] = float(R106.Qr)
        bmp_output["volumeSubstratesideB"] = float(R106.TotalVolFeed) - 12.5
        #reactor execution model
        R106.Reactor(model = ModelSideB, OperationMethod = OperationMethodSideB, T = TemperatureSideB + 273.15, K1 = KSideB, K2 = EaSideB, K3 = LSideB, speed_time=speed_time)
        bmp_output["SVR106"] = float(R106.SV_int) 
        bmp_output["OCR106"] = float(R106.OC)
        bmp_output["STR106"] = float(R106.ST_int)
        bmp_output["XR106"] = float(R106.x)
        bmp_output["PBMR106"] = float(R106.PBM)
        bmp_output["KR106"] = KSideB
        bmp_output["EaR106"] = EaSideB
        bmp_output["lambdaR106"] = LSideB
        bmp_output["TempR106"] = TemperatureSideB   
        bmp_output["pHR106"] = pHSideB
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR106"] =float(R106.nCH4)
        bmp_output["carbondioxidemolR106"] = float(R106.nCO2)
        bmp_output["oxygenmolR106"] = float(R106.nO2)
        bmp_output["hydrogensulfurmolR106"] = float(R106.nH2S)
        bmp_output["hydrogenmolR106"] = float(R106.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR106"] = float(R106.xCH4*100)
        bmp_output["carbondioxideconcentrationR106"] = float(R106.xCO2*100)
        bmp_output["oxygenconcentrationR106"] = float(R106.xO2*100)
        bmp_output["hydrogensulfurconcentrationR106"] = float(R106.xH2S*1000000)
        bmp_output["hydrogenconcentrationR106"] = float(R106.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR106"] = float(R106.vCH4)
        bmp_output["carbondioxidevolR106"] = float(R106.vCO2)
        bmp_output["oxygenvolR106"] = float(R106.vO2)
        bmp_output["hydrogensulfurvolR106"] = float(R106.vH2S)
        bmp_output["hydrogenvolR106"] = float(R106.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideB == "Pressure":
            R106.Measurement_by_pressure(T = TemperatureManualSideB, Pset = pressureSetPointSideB)
        elif measurementMethodSideB == "VolumeDisplaced":
            R106.Measument_by_volume(T = TemperatureManualSideB, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR106"] = float(R106.P_acum_psi)
        bmp_output["storagebiogaspressureR106"] = float(R106.P_psi)
        bmp_output["storagebiogasR106"] = float(R106.Vnorm_sto_nmL)
        bmp_output["accumbiogasR106"] = float(R106.Vnormalbiogas)
        bmp_output["LHVR106"] = float(R106.LHV_JNm3)
        bmp_output["EnergyR106"] = float(R106.Energia)

        R106.GlobaltimeCounter()

        # R107
        if user_id107 not in bmp_instances_offline_SideB:
          bmp_instances_offline_SideB[user_id107] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideB, ReactorVolume = ReactorVolumeSideB, InitialFreeVolume = InitialFreeVolumeSideB,
                                                                              SubstrateNumber = SubstrateNumberSideB, MixRule = MixRuleSideB, 
                                                                              Fraction1 = Fraction1SideB, Fraction2 = Fraction2SideB, Fraction3 = Fraction3SideB, Fraction4 = Fraction4SideB, WaterFraction = WaterFractionSideB,
                                                                              Volume1 = Fraction1SideB, Volume2 = Fraction2SideB, Volume3 = Fraction3SideB, Volume4 = Fraction4SideB, WaterVolume = WaterFractionSideB,
                                                                              Weight1 = Fraction1SideB, Weight2 = Fraction2SideB, Weight3 = Fraction3SideB, Weight4 = Fraction4SideB, WaterWeight = WaterFractionSideB,
                                                                              ST1 = ST1SideB, SV1 = SV1SideB, rho1 = rho1SideB, Cc1 = Cc1SideB, Ch1 = Ch1SideB, Co1 = Co1SideB, Cn1 = Cn1SideB, Cs1 = Cs1SideB,
                                                                              ST2 = ST2SideB, SV2 = SV2SideB, rho2 = rho2SideB, Cc2 = Cc2SideB, Ch2 = Ch2SideB, Co2 = Co2SideB, Cn2 = Cn2SideB, Cs2 = Cs2SideB,
                                                                              ST3 = ST3SideB, SV3 = SV3SideB, rho3 = rho3SideB, Cc3 = Cc3SideB, Ch3 = Ch3SideB, Co3 = Co3SideB, Cn3 = Cn3SideB, Cs3 = Cs3SideB,
                                                                              ST4 = ST4SideB, SV4 = SV4SideB, rho4 = rho4SideB, Cc4 = Cc4SideB, Ch4 = Ch4SideB, Co4 = Co4SideB, Cn4 = Cn4SideB, Cs4 = Cs4SideB,
                                                                              OperationMethod = OperationMethodSideB, tp = time_stepSideB)  
        
        R107 = bmp_instances_offline_SideB[user_id107]

        #Mixing R107
        R107.MixControl(MixVelocity = MixVelocitySideB, MixTime = mixTimeSideB, DailyMixing = mixDailySideB, speed_time = speed_time)
        bmp_output["mixVelocityR107"] = R107.MixVelocity

        if OperationMethodSideB in ["Time", "Injection"]:
          R107.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R107.SubstrateFeed(Mode = OperationMethodSideB, Volume = dosificationVolumeSideB, Time = dailyInyectionsSideB, Inyections = dailyInyectionsSideB, Q=3.4, speed_time = speed_time)
        #reactor execution model
        R107.Reactor(model = ModelSideB, OperationMethod = OperationMethodSideB, T = TemperatureSideB + 273.15, K1 = KSideB, K2 = EaSideB, K3 = LSideB, speed_time=speed_time)
        bmp_output["SVR107"] = float(R107.SV_int) 
        bmp_output["OCR107"] = float(R107.OC)
        bmp_output["STR107"] = float(R107.ST_int)
        bmp_output["XR107"] = float(R107.x)
        bmp_output["PBMR107"] = float(R107.PBM)
        bmp_output["KR107"] = KSideB
        bmp_output["EaR107"] = EaSideB
        bmp_output["lambdaR107"] = LSideB
        bmp_output["TempR107"] = TemperatureSideB   
        bmp_output["pHR107"] = pHSideB
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR107"] =float(R107.nCH4)
        bmp_output["carbondioxidemolR107"] = float(R107.nCO2)
        bmp_output["oxygenmolR107"] = float(R107.nO2)
        bmp_output["hydrogensulfurmolR107"] = float(R107.nH2S)
        bmp_output["hydrogenmolR107"] = float(R107.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR107"] = float(R107.xCH4*100)
        bmp_output["carbondioxideconcentrationR107"] = float(R107.xCO2*100)
        bmp_output["oxygenconcentrationR107"] = float(R107.xO2*100)
        bmp_output["hydrogensulfurconcentrationR107"] = float(R107.xH2S*1000000)
        bmp_output["hydrogenconcentrationR107"] = float(R107.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR107"] = float(R107.vCH4)
        bmp_output["carbondioxidevolR107"] = float(R107.vCO2)
        bmp_output["oxygenvolR107"] = float(R107.vO2)
        bmp_output["hydrogensulfurvolR107"] = float(R107.vH2S)
        bmp_output["hydrogenvolR107"] = float(R107.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideB == "Pressure":
            R107.Measurement_by_pressure(T = TemperatureManualSideB, Pset = pressureSetPointSideB)
        elif measurementMethodSideB == "VolumeDisplaced":
            R107.Measument_by_volume(T = TemperatureManualSideB, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR107"] = float(R107.P_acum_psi)
        bmp_output["storagebiogaspressureR107"] = float(R107.P_psi)
        bmp_output["storagebiogasR107"] = float(R107.Vnorm_sto_nmL)
        bmp_output["accumbiogasR107"] = float(R107.Vnormalbiogas)
        bmp_output["LHVR107"] = float(R107.LHV_JNm3)
        bmp_output["EnergyR107"] = float(R107.Energia)

        R107.GlobaltimeCounter()

        # R108
        if user_id108 not in bmp_instances_offline_SideB:
          bmp_instances_offline_SideB[user_id108] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideB, ReactorVolume = ReactorVolumeSideB, InitialFreeVolume = InitialFreeVolumeSideB,
                                                                              SubstrateNumber = SubstrateNumberSideB, MixRule = MixRuleSideB, 
                                                                              Fraction1 = Fraction1SideB, Fraction2 = Fraction2SideB, Fraction3 = Fraction3SideB, Fraction4 = Fraction4SideB, WaterFraction = WaterFractionSideB,
                                                                              Volume1 = Fraction1SideB, Volume2 = Fraction2SideB, Volume3 = Fraction3SideB, Volume4 = Fraction4SideB, WaterVolume = WaterFractionSideB,
                                                                              Weight1 = Fraction1SideB, Weight2 = Fraction2SideB, Weight3 = Fraction3SideB, Weight4 = Fraction4SideB, WaterWeight = WaterFractionSideB,
                                                                              ST1 = ST1SideB, SV1 = SV1SideB, rho1 = rho1SideB, Cc1 = Cc1SideB, Ch1 = Ch1SideB, Co1 = Co1SideB, Cn1 = Cn1SideB, Cs1 = Cs1SideB,
                                                                              ST2 = ST2SideB, SV2 = SV2SideB, rho2 = rho2SideB, Cc2 = Cc2SideB, Ch2 = Ch2SideB, Co2 = Co2SideB, Cn2 = Cn2SideB, Cs2 = Cs2SideB,
                                                                              ST3 = ST3SideB, SV3 = SV3SideB, rho3 = rho3SideB, Cc3 = Cc3SideB, Ch3 = Ch3SideB, Co3 = Co3SideB, Cn3 = Cn3SideB, Cs3 = Cs3SideB,
                                                                              ST4 = ST4SideB, SV4 = SV4SideB, rho4 = rho4SideB, Cc4 = Cc4SideB, Ch4 = Ch4SideB, Co4 = Co4SideB, Cn4 = Cn4SideB, Cs4 = Cs4SideB,
                                                                              OperationMethod = OperationMethodSideB, tp = time_stepSideB)  
        
        R108 = bmp_instances_offline_SideB[user_id108]

        #Mixing R108
        R108.MixControl(MixVelocity = MixVelocitySideB, MixTime = mixTimeSideB, DailyMixing = mixDailySideB, speed_time = speed_time)
        bmp_output["mixVelocityR108"] = R108.MixVelocity

        if OperationMethodSideB in ["Time", "Injection"]:
          R108.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R108.SubstrateFeed(Mode = OperationMethodSideB, Volume = dosificationVolumeSideB, Time = dailyInyectionsSideB, Inyections = dailyInyectionsSideB, Q=3.4, speed_time = speed_time)
        #reactor execution model
        R108.Reactor(model = ModelSideB, OperationMethod = OperationMethodSideB, T = TemperatureSideB + 273.15, K1 = KSideB, K2 = EaSideB, K3 = LSideB, speed_time=speed_time)
        bmp_output["SVR108"] = float(R108.SV_int) 
        bmp_output["OCR108"] = float(R108.OC)
        bmp_output["STR108"] = float(R108.ST_int)
        bmp_output["XR108"] = float(R108.x)
        bmp_output["PBMR108"] = float(R108.PBM)
        bmp_output["KR108"] = KSideB
        bmp_output["EaR108"] = EaSideB
        bmp_output["lambdaR108"] = LSideB
        bmp_output["TempR108"] = TemperatureSideB   
        bmp_output["pHR108"] = pHSideB
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR108"] =float(R108.nCH4)
        bmp_output["carbondioxidemolR108"] = float(R108.nCO2)
        bmp_output["oxygenmolR108"] = float(R108.nO2)
        bmp_output["hydrogensulfurmolR108"] = float(R108.nH2S)
        bmp_output["hydrogenmolR108"] = float(R108.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR108"] = float(R108.xCH4*100)
        bmp_output["carbondioxideconcentrationR108"] = float(R108.xCO2*100)
        bmp_output["oxygenconcentrationR108"] = float(R108.xO2*100)
        bmp_output["hydrogensulfurconcentrationR108"] = float(R108.xH2S*1000000)
        bmp_output["hydrogenconcentrationR108"] = float(R108.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR108"] = float(R108.vCH4)
        bmp_output["carbondioxidevolR108"] = float(R108.vCO2)
        bmp_output["oxygenvolR108"] = float(R108.vO2)
        bmp_output["hydrogensulfurvolR108"] = float(R108.vH2S)
        bmp_output["hydrogenvolR108"] = float(R108.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideB == "Pressure":
            R108.Measurement_by_pressure(T = TemperatureManualSideB, Pset = pressureSetPointSideB)
        elif measurementMethodSideB == "VolumeDisplaced":
            R108.Measument_by_volume(T = TemperatureManualSideB, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR108"] = float(R108.P_acum_psi)
        bmp_output["storagebiogaspressureR108"] = float(R108.P_psi)
        bmp_output["storagebiogasR108"] = float(R108.Vnorm_sto_nmL)
        bmp_output["accumbiogasR108"] = float(R108.Vnormalbiogas)
        bmp_output["LHVR108"] = float(R108.LHV_JNm3)
        bmp_output["EnergyR108"] = float(R108.Energia)

        R108.GlobaltimeCounter()

        # R109
        if user_id109 not in bmp_instances_offline_SideB:
          bmp_instances_offline_SideB[user_id109] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideB, ReactorVolume = ReactorVolumeSideB, InitialFreeVolume = InitialFreeVolumeSideB,
                                                                              SubstrateNumber = SubstrateNumberSideB, MixRule = MixRuleSideB, 
                                                                              Fraction1 = Fraction1SideB, Fraction2 = Fraction2SideB, Fraction3 = Fraction3SideB, Fraction4 = Fraction4SideB, WaterFraction = WaterFractionSideB,
                                                                              Volume1 = Fraction1SideB, Volume2 = Fraction2SideB, Volume3 = Fraction3SideB, Volume4 = Fraction4SideB, WaterVolume = WaterFractionSideB,
                                                                              Weight1 = Fraction1SideB, Weight2 = Fraction2SideB, Weight3 = Fraction3SideB, Weight4 = Fraction4SideB, WaterWeight = WaterFractionSideB,
                                                                              ST1 = ST1SideB, SV1 = SV1SideB, rho1 = rho1SideB, Cc1 = Cc1SideB, Ch1 = Ch1SideB, Co1 = Co1SideB, Cn1 = Cn1SideB, Cs1 = Cs1SideB,
                                                                              ST2 = ST2SideB, SV2 = SV2SideB, rho2 = rho2SideB, Cc2 = Cc2SideB, Ch2 = Ch2SideB, Co2 = Co2SideB, Cn2 = Cn2SideB, Cs2 = Cs2SideB,
                                                                              ST3 = ST3SideB, SV3 = SV3SideB, rho3 = rho3SideB, Cc3 = Cc3SideB, Ch3 = Ch3SideB, Co3 = Co3SideB, Cn3 = Cn3SideB, Cs3 = Cs3SideB,
                                                                              ST4 = ST4SideB, SV4 = SV4SideB, rho4 = rho4SideB, Cc4 = Cc4SideB, Ch4 = Ch4SideB, Co4 = Co4SideB, Cn4 = Cn4SideB, Cs4 = Cs4SideB,
                                                                              OperationMethod = OperationMethodSideB, tp = time_stepSideB)  
        
        R109 = bmp_instances_offline_SideB[user_id109]

        #Mixing R109
        R109.MixControl(MixVelocity = MixVelocitySideB, MixTime = mixTimeSideB, DailyMixing = mixDailySideB, speed_time = speed_time)
        bmp_output["mixVelocityR109"] = R109.MixVelocity

        if OperationMethodSideB in ["Time", "Injection"]:
          R109.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R109.SubstrateFeed(Mode = OperationMethodSideB, Volume = dosificationVolumeSideB, Time = dailyInyectionsSideB, Inyections = dailyInyectionsSideB, Q=3.4, speed_time = speed_time)
        #reactor execution model
        R109.Reactor(model = ModelSideB, OperationMethod = OperationMethodSideB, T = TemperatureSideB + 273.15, K1 = KSideB, K2 = EaSideB, K3 = LSideB, speed_time=speed_time)
        bmp_output["SVR109"] = float(R109.SV_int) 
        bmp_output["OCR109"] = float(R109.OC)
        bmp_output["STR109"] = float(R109.ST_int)
        bmp_output["XR109"] = float(R109.x)
        bmp_output["PBMR109"] = float(R109.PBM)
        bmp_output["KR109"] = KSideB
        bmp_output["EaR109"] = EaSideB
        bmp_output["lambdaR109"] = LSideB
        bmp_output["TempR109"] = TemperatureSideB   
        bmp_output["pHR109"] = pHSideB
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR109"] =float(R109.nCH4)
        bmp_output["carbondioxidemolR109"] = float(R109.nCO2)
        bmp_output["oxygenmolR109"] = float(R109.nO2)
        bmp_output["hydrogensulfurmolR109"] = float(R109.nH2S)
        bmp_output["hydrogenmolR109"] = float(R109.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR109"] = float(R109.xCH4*100)
        bmp_output["carbondioxideconcentrationR109"] = float(R109.xCO2*100)
        bmp_output["oxygenconcentrationR109"] = float(R109.xO2*100)
        bmp_output["hydrogensulfurconcentrationR109"] = float(R109.xH2S*1000000)
        bmp_output["hydrogenconcentrationR109"] = float(R109.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR109"] = float(R109.vCH4)
        bmp_output["carbondioxidevolR109"] = float(R109.vCO2)
        bmp_output["oxygenvolR109"] = float(R109.vO2)
        bmp_output["hydrogensulfurvolR109"] = float(R109.vH2S)
        bmp_output["hydrogenvolR109"] = float(R109.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideB == "Pressure":
            R109.Measurement_by_pressure(T = TemperatureManualSideB, Pset = pressureSetPointSideB)
        elif measurementMethodSideB == "VolumeDisplaced":
            R109.Measument_by_volume(T = TemperatureManualSideB, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR109"] = float(R109.P_acum_psi)
        bmp_output["storagebiogaspressureR109"] = float(R109.P_psi)
        bmp_output["storagebiogasR109"] = float(R109.Vnorm_sto_nmL)
        bmp_output["accumbiogasR109"] = float(R109.Vnormalbiogas)
        bmp_output["LHVR109"] = float(R109.LHV_JNm3)
        bmp_output["EnergyR109"] = float(R109.Energia)

        R109.GlobaltimeCounter()

        # R110
        if user_id110 not in bmp_instances_offline_SideB:
          bmp_instances_offline_SideB[user_id110] = BMPOffline.BMPModelOffline(MeasureMethod = measurementMethodSideB, ReactorVolume = ReactorVolumeSideB, InitialFreeVolume = InitialFreeVolumeSideB,
                                                                              SubstrateNumber = SubstrateNumberSideB, MixRule = MixRuleSideB, 
                                                                              Fraction1 = Fraction1SideB, Fraction2 = Fraction2SideB, Fraction3 = Fraction3SideB, Fraction4 = Fraction4SideB, WaterFraction = WaterFractionSideB,
                                                                              Volume1 = Fraction1SideB, Volume2 = Fraction2SideB, Volume3 = Fraction3SideB, Volume4 = Fraction4SideB, WaterVolume = WaterFractionSideB,
                                                                              Weight1 = Fraction1SideB, Weight2 = Fraction2SideB, Weight3 = Fraction3SideB, Weight4 = Fraction4SideB, WaterWeight = WaterFractionSideB,
                                                                              ST1 = ST1SideB, SV1 = SV1SideB, rho1 = rho1SideB, Cc1 = Cc1SideB, Ch1 = Ch1SideB, Co1 = Co1SideB, Cn1 = Cn1SideB, Cs1 = Cs1SideB,
                                                                              ST2 = ST2SideB, SV2 = SV2SideB, rho2 = rho2SideB, Cc2 = Cc2SideB, Ch2 = Ch2SideB, Co2 = Co2SideB, Cn2 = Cn2SideB, Cs2 = Cs2SideB,
                                                                              ST3 = ST3SideB, SV3 = SV3SideB, rho3 = rho3SideB, Cc3 = Cc3SideB, Ch3 = Ch3SideB, Co3 = Co3SideB, Cn3 = Cn3SideB, Cs3 = Cs3SideB,
                                                                              ST4 = ST4SideB, SV4 = SV4SideB, rho4 = rho4SideB, Cc4 = Cc4SideB, Ch4 = Ch4SideB, Co4 = Co4SideB, Cn4 = Cn4SideB, Cs4 = Cs4SideB,
                                                                              OperationMethod = OperationMethodSideB, tp = time_stepSideB)  
        
        R110 = bmp_instances_offline_SideB[user_id110]

        #Mixing R110
        R110.MixControl(MixVelocity = MixVelocitySideB, MixTime = mixTimeSideB, DailyMixing = mixDailySideB, speed_time = speed_time)
        bmp_output["mixVelocityR110"] = R110.MixVelocity

        if OperationMethodSideB in ["Time", "Injection"]:
          R110.MixtureCalculationFeeding()
        
        #feeding in case time or injection
        R110.SubstrateFeed(Mode = OperationMethodSideB, Volume = dosificationVolumeSideB, Time = dailyInyectionsSideB, Inyections = dailyInyectionsSideB, Q=3.4, speed_time = speed_time)
        #reactor execution model
        R110.Reactor(model = ModelSideB, OperationMethod = OperationMethodSideB, T = TemperatureSideB + 273.15, K1 = KSideB, K2 = EaSideB, K3 = LSideB, speed_time=speed_time)
        bmp_output["SVR110"] = float(R110.SV_int) 
        bmp_output["OCR110"] = float(R110.OC)
        bmp_output["STR110"] = float(R110.ST_int)
        bmp_output["XR110"] = float(R110.x)
        bmp_output["PBMR110"] = float(R110.PBM)
        bmp_output["KR110"] = KSideB
        bmp_output["EaR110"] = EaSideB
        bmp_output["lambdaR110"] = LSideB
        bmp_output["TempR110"] = TemperatureSideB   
        bmp_output["pHR110"] = pHSideB
         #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR110"] =float(R110.nCH4)
        bmp_output["carbondioxidemolR110"] = float(R110.nCO2)
        bmp_output["oxygenmolR110"] = float(R110.nO2)
        bmp_output["hydrogensulfurmolR110"] = float(R110.nH2S)
        bmp_output["hydrogenmolR110"] = float(R110.nH2)
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR110"] = float(R110.xCH4*100)
        bmp_output["carbondioxideconcentrationR110"] = float(R110.xCO2*100)
        bmp_output["oxygenconcentrationR110"] = float(R110.xO2*100)
        bmp_output["hydrogensulfurconcentrationR110"] = float(R110.xH2S*1000000)
        bmp_output["hydrogenconcentrationR110"] = float(R110.xH2*1000000)
        #---- Productos de reacción en volume [mL]
        bmp_output["methanevolR110"] = float(R110.vCH4)
        bmp_output["carbondioxidevolR110"] = float(R110.vCO2)
        bmp_output["oxygenvolR110"] = float(R110.vO2)
        bmp_output["hydrogensulfurvolR110"] = float(R110.vH2S)
        bmp_output["hydrogenvolR110"] = float(R110.vH2)
        
        #Run biogas measurement methods
        if measurementMethodSideB == "Pressure":
            R110.Measurement_by_pressure(T = TemperatureManualSideB, Pset = pressureSetPointSideB)
        elif measurementMethodSideB == "VolumeDisplaced":
            R110.Measument_by_volume(T = TemperatureManualSideB, hmax = 135, hmin = 0, Apool = 60*50)
        
        #---- Global biogas properties
        bmp_output["accumbiogaspressureR110"] = float(R110.P_acum_psi)
        bmp_output["storagebiogaspressureR110"] = float(R110.P_psi)
        bmp_output["storagebiogasR110"] = float(R110.Vnorm_sto_nmL)
        bmp_output["accumbiogasR110"] = float(R110.Vnormalbiogas)
        bmp_output["LHVR110"] = float(R110.LHV_JNm3)
        bmp_output["EnergyR110"] = float(R110.Energia)

        R110.GlobaltimeCounter()
    
    bmp_output = {
                  k: (0 if (v is None or (isinstance(v, (int, float)) and np.isnan(v))) else v)
                  for k, v in bmp_output.items()
              }

    return {"model": bmp_output}, 200