from flask import request
from flask_restful import Resource
from simulation_models.Biogas import TrainingModel
from simulation_models.Biogas import Biogas_Model_Simulation
from tools import DBManager
import pandas as pd
import os
import json

biogas_instances = {}
users_instances = []

class Biogas(Resource):

  def get(self):
    mode = request.args.get('mode')
    model = request.args.get('model')
    measurement='Planta_Biogas'

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
    |> filter(fn: (r) => strings.containsStr(v: r._field, substr: "''' + mode + '''"))
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
    
    print(trainingData, flush=True)
    return trainingData

  def post(self):
    data = request.get_json()
    biogas_output = {}

    #Database parameters
    DB_IP = os.getenv('DB_IP')
    DB_Port = os.getenv('DB_Port')
    DB_Bucket = os.getenv('DB_Bucket')
    DB_Organization = os.getenv('DB_Organization')
    DB_Token = os.getenv('DB_Token')

    #Online-offline consulting state
    Online = data["digitalTwinState"]
    OfflineEntranceVariables = data["inputOfflineOperation"]
    TrainingState = data["trainingMode"]
    iteration = data["iteration"]
    user = data["name"]

    #Creation and verification of instances according to the name of the user
    if iteration == 1:   
      for key in users_instances:
        if key in biogas_instances:
          del biogas_instances[key]
          print(f'User {key} deleted', flush=True)
          users_instances.remove(key)
      users_instances.append(user)
    print("biogas instances", biogas_instances, flush=True)

    #Online Mode -- all variables from plant   
    if (Online == True and OfflineEntranceVariables == False):  #Modo On and variables from plant
      
      # Variables to start the class
      #Training time Consult the past in the biogas plant
      t_train = data["digitalTwinForecastTime"]["value"]*60
      #R101 initial conditions
      ST_ini_R101 = data["initialAnalysisConditionsR101"]["totalSubstrateSolids"]["value"]
      SV_ini_R101 = data["initialAnalysisConditionsR101"]["volatileSubstrateSolids"]["value"]
      Cc_ini_R101 = data["initialAnalysisConditionsR101"]["atomicCarbonSubstrateConcetration"]["value"]
      Ch_ini_R101 = data["initialAnalysisConditionsR101"]["atomicHydrogenSubstrateConcetration"]["value"]
      Co_ini_R101 = data["initialAnalysisConditionsR101"]["atomicOxygenSubstrateConcetration"]["value"]
      Cn_ini_R101 = data["initialAnalysisConditionsR101"]["atomicNitrogenSubstrateConcetration"]["value"]
      Cs_ini_R101 = data["initialAnalysisConditionsR101"]["atomicSulfurSubstrateConcetration"]["value"]
      rho_ini_R101 = data["initialAnalysisConditionsR101"]["substrateDensity"]["value"]

      #R102 initial conditions
      ST_ini_R102 = data["initialAnalysisConditionsR102"]["totalSubstrateSolids"]["value"]
      SV_ini_R102 = data["initialAnalysisConditionsR102"]["volatileSubstrateSolids"]["value"]
      Cc_ini_R102 = data["initialAnalysisConditionsR102"]["atomicCarbonSubstrateConcetration"]["value"]
      Ch_ini_R102 = data["initialAnalysisConditionsR102"]["atomicHydrogenSubstrateConcetration"]["value"]
      Co_ini_R102 = data["initialAnalysisConditionsR102"]["atomicOxygenSubstrateConcetration"]["value"]
      Cn_ini_R102 = data["initialAnalysisConditionsR102"]["atomicNitrogenSubstrateConcetration"]["value"]
      Cs_ini_R102 = data["initialAnalysisConditionsR102"]["atomicSulfurSubstrateConcetration"]["value"]
      rho_ini_R102 = data["initialAnalysisConditionsR102"]["substrateDensity"]["value"]
      
      #constructive parameters for biogas tank storage
      Volume_V101 = data["biogasTankVolume1"]["value"]
      Volume_V102 = data["biogasTankVolume2"]["value"]
      Volume_V107 = data["biogasTankVolume3"]["value"]
      if user not in biogas_instances:
        biogas_instances[user] = TrainingModel.Training_offline(DB_IP = DB_IP, DB_Port = DB_Port, DB_Organization = DB_Organization, DB_Bucket = DB_Bucket, DB_Token = DB_Token,
                                                                    t_train = t_train, ST_ini_R101=ST_ini_R101, SV_ini_R101=SV_ini_R101, Cc_R101 = Cc_ini_R101, Ch_R101=Ch_ini_R101, Co_R101=Co_ini_R101, Cn_R101=Cn_ini_R101, Cs_R101=Cs_ini_R101, rho_R101=rho_ini_R101, Volume_V101 = Volume_V101,  
                                                                    ST_ini_R102 = ST_ini_R102, SV_ini_R102 = SV_ini_R102, Cc_R102 = Cc_ini_R102, Ch_R102 = Ch_ini_R102, Co_R102 = Co_ini_R102, Cn_R102 = Cn_ini_R102, Cs_R102 = Cs_ini_R102, rho_R102 = rho_ini_R102, 
                                                                    Volume_V102 = Volume_V102, Volume_V107 = Volume_V107)
      biogas_plant = biogas_instances[user]
      biogas_plant.getData()
      biogas_plant.LimitReagentCalculation()
      Model = data["operationModelType"]
      biogas_plant.StochoimetricExpenditure(Model=Model)
      #biogas_plant.TrainMode2.to_csv("TraningMode2.csv")
      if Model == "Arrhenius":
        biogas_plant.OptimizationArrhenius(resolution = 5)
        biogas_output["K_R101"] = abs(biogas_plant.K_mean_R101)
        biogas_output["Ea_R101"] = abs(biogas_plant.Ea_mean_R101)
      if Model == "ADM1":
        biogas_plant.OptimizationADM1(resolution = 140)
        biogas_output["K_R101"] = abs(biogas_plant.K_mean_R101)
      if Model == "Gompertz":
        biogas_plant.OptimizationGompertz(resolution=1000)
        biogas_output["K_R101"] = biogas_plant.ym_R101
        biogas_output["Ea_R101"] = biogas_plant.U_R101
        biogas_output["Lambda_R101"] = biogas_plant.L_R101

      biogas_plant.V101model1_2()
      biogas_plant.V102model1_2()
      biogas_plant.V107model1_2()
      biogas_plant.biogas_treatment_optimization(W_feSO4=154.46, W_silica=3997.79)        
    
      # -------------Exit variables to front 
      # substrate conditions
      #General Conditions
      biogas_output["operationMode"] = biogas_plant.Operation_mode
      # TK-100
      biogas_output["n"] = biogas_plant.n
      biogas_output["a"] = biogas_plant.a
      biogas_output["b"] = biogas_plant.b
      biogas_output["c"] = biogas_plant.c
      biogas_output["d"] = biogas_plant.d
      biogas_output["Mix_Velocity_TK100"] = biogas_plant.Mix_Velocity_TK100
      biogas_output["C_sv"] = biogas_plant.Csv_sus_gl                            #gSV/L
      biogas_output["SV"] = biogas_plant.SV
      biogas_output["C_st"] = biogas_plant.Cst_sus_gl
      biogas_output["ST"] = biogas_plant.ST
      # P104
      biogas_output["Pump104Flow"] = biogas_plant.P104
      # R101
      biogas_output["Mix_Velocity_R101"] = biogas_plant.Mix_Velocity_R101
      biogas_output["pH_R101"] = biogas_plant.pH_R101
      biogas_output["Temp_R101"] = biogas_plant.T_R101
      biogas_output["C_sv_R101"] = biogas_plant.Csus_ini_SV_R101_gl-50
      biogas_output["SV_R101"] = (biogas_plant.SV_R101*100)-5
      biogas_output["C_st_R101"] = biogas_plant.Csus_ini_ST_R101_gl-50
      biogas_output["ST_R101"] = (biogas_plant.ST_R101*100)-4
      biogas_output["Organic_Charge_R101"] = biogas_plant.OC_R101
      biogas_output["x_R101"] = biogas_plant.x_R101*100
      # P101
      biogas_output["Pump101Flow"] = biogas_plant.P101
      # V101
      biogas_output["AcumBiogasPressureV101"] = biogas_plant.Pacum_V101
      biogas_output["StorageBiogasPressureV101"] = biogas_plant.P_V101
      biogas_output["AcumBiogasVolumenV101"] = biogas_plant.Vnorm_bio_V101*1000
      biogas_output["StorageBiogasVolumeV101"] = biogas_plant.Vnorm_bio_sto_V101*1000
      biogas_output["StorageCH4_V101Volume"] = biogas_plant.VCH4_acum_V101
      biogas_output["StorageCH4_V101Concentration"] = biogas_plant.xCH4_V101
      biogas_output["StorageCH4_V101moles"] = biogas_plant.mol_acum_CH4_V101
      biogas_output["StorageCO2_V101Volume"] = biogas_plant.VCO2_acum_V101
      biogas_output["StorageCO2_V101Concentration"] = biogas_plant.xCO2_V101
      biogas_output["StorageCO2_V101moles"] = biogas_plant.mol_acum_CO2_V101
      biogas_output["StorageH2S_V101Volume"] = biogas_plant.VH2S_acum_V101
      biogas_output["StorageH2S_V101Concentration"] = biogas_plant.xH2S_V101
      biogas_output["StorageH2S_V101moles"] = biogas_plant.mol_acum_H2S_V101
      biogas_output["StorageO2_V101Volume"] = biogas_plant.VO2_acum_V101
      biogas_output["StorageO2_V101Concentration"] = biogas_plant.xO2_V101
      biogas_output["StorageO2_V101moles"] = biogas_plant.mol_acum_O2_V101
      biogas_output["StorageH2_V101Volume"] = biogas_plant.VH2_acum_V101
      biogas_output["StorageH2_V101Concentration"] = biogas_plant.xH2_V101
      biogas_output["StorageH2_V101moles"] = biogas_plant.mol_acum_H2_V101
      biogas_output["StorageNH3_V101Volume"] = biogas_plant.VNH3_acum_V101
      biogas_output["StorageNH3_V101Concentration"] = biogas_plant.xNH3_V101
      biogas_output["StorageNH3_V101moles"] = biogas_plant.mol_acum_H2_V101
      biogas_output["moles_humidity_V101"] = biogas_plant.mol_acum_H2O_V101
      biogas_output["Relative_humidity_V101"] = biogas_plant.RH_V101
      biogas_output["StorageEnergy_V101"] = biogas_plant.Energy_V101/3600
      # V102
      biogas_output["AcumBiogasPressureV102"] = biogas_plant.Pacum_V102
      biogas_output["StorageBiogasPressureV102"] = biogas_plant.P_V102
      biogas_output["AcumBiogasVolumenV102"] = biogas_plant.Vnorm_bio_V102*1000
      biogas_output["StorageBiogasVolumeV102"] = biogas_plant.Vnorm_bio_sto_V102*1000
      biogas_output["StorageCH4_V102Volume"] = biogas_plant.VCH4_acum_V102
      biogas_output["StorageCH4_V102Concentration"] = biogas_plant.xCH4_V102
      biogas_output["StorageCH4_V102moles"] = biogas_plant.mol_acum_CH4_V102
      biogas_output["StorageCO2_V102Volume"] = biogas_plant.VCO2_acum_V102
      biogas_output["StorageCO2_V102Concentration"] = biogas_plant.xCO2_V102
      biogas_output["StorageCO2_V102moles"] = biogas_plant.mol_acum_CO2_V102
      biogas_output["StorageH2S_V102Volume"] = biogas_plant.VH2S_acum_V102
      biogas_output["StorageH2S_V102Concentration"] = biogas_plant.xH2S_V102
      biogas_output["StorageH2S_V102moles"] = biogas_plant.mol_acum_H2S_V102
      biogas_output["StorageO2_V102Volume"] = biogas_plant.VO2_acum_V102
      biogas_output["StorageO2_V102Concentration"] = biogas_plant.xO2_V102
      biogas_output["StorageO2_V102moles"] = biogas_plant.mol_acum_O2_V102
      biogas_output["StorageH2_V102Volume"] = biogas_plant.VH2_acum_V102
      biogas_output["StorageH2_V102Concentration"] = biogas_plant.xH2_V102
      biogas_output["StorageH2_V102moles"] = biogas_plant.mol_acum_H2_V102
      biogas_output["StorageNH3_V102Volume"] = biogas_plant.VNH3_acum_V102
      biogas_output["StorageNH3_V102Concentration"] = biogas_plant.xNH3_V102
      biogas_output["StorageNH3_V102moles"] = biogas_plant.mol_acum_H2_V102
      biogas_output["moles_humidity_V102"] = biogas_plant.mol_acum_H2O_V102
      biogas_output["Relative_humidity_V102"] = biogas_plant.RH_V102
      biogas_output["StorageEnergy_V102"] = biogas_plant.Energy_V102/3600
      # V107
      biogas_output["AcumBiogasPressureV107"] = biogas_plant.Pacum_V107
      biogas_output["StorageBiogasPressureV107"] = biogas_plant.P_V107
      biogas_output["AcumBiogasVolumenV107"] = biogas_plant.Vnorm_bio_V107*1000
      biogas_output["StorageBiogasVolumeV107"] = biogas_plant.Vnorm_bio_sto_V107*1000
      biogas_output["StorageCH4_V107Volume"] = biogas_plant.VCH4_acum_V107
      biogas_output["StorageCH4_V107Concentration"] = biogas_plant.xCH4_V107
      biogas_output["StorageCH4_V107moles"] = biogas_plant.mol_acum_CH4_V107
      biogas_output["StorageCO2_V107Volume"] = biogas_plant.VCO2_acum_V107
      biogas_output["StorageCO2_V107Concentration"] = biogas_plant.xCO2_V107
      biogas_output["StorageCO2_V107moles"] = biogas_plant.mol_acum_CO2_V107
      biogas_output["StorageH2S_V107Volume"] = biogas_plant.VH2S_acum_V107
      biogas_output["StorageH2S_V107Concentration"] = biogas_plant.xH2S_V107
      biogas_output["StorageH2S_V107moles"] = biogas_plant.mol_acum_H2S_V107
      biogas_output["StorageO2_V107Volume"] = biogas_plant.VO2_acum_V107
      biogas_output["StorageO2_V107Concentration"] = biogas_plant.xO2_V107
      biogas_output["StorageO2_V107moles"] = biogas_plant.mol_acum_O2_V107
      biogas_output["StorageH2_V107Volume"] = biogas_plant.VH2_acum_V107
      biogas_output["StorageH2_V107Concentration"] = biogas_plant.xH2_V107
      biogas_output["StorageH2_V107moles"] = biogas_plant.mol_acum_H2_V107
      biogas_output["StorageNH3_V107Volume"] = biogas_plant.VNH3_acum_V107
      biogas_output["StorageNH3_V107Concentration"] = biogas_plant.xNH3_V107
      biogas_output["StorageNH3_V107moles"] = biogas_plant.mol_acum_H2_V107
      biogas_output["moles_humidity_V107"] = biogas_plant.mol_acum_H2O_V107
      biogas_output["Relative_humidity_V107"] = biogas_plant.RH_V107
      biogas_output["StorageEnergy_V107"] = biogas_plant.Energy_V107/3600
      #Treatment biogas
      biogas_output["ads_NH3_bt"] = biogas_plant.mol_NH3_ads
      biogas_output["ads_H2S_bt"] = biogas_plant.mol_H2S_ads
      biogas_output["ads_H2O_bt"] = biogas_plant.mol_H2O_ads
      biogas_output["x_bt"] = biogas_plant.Xglobal * 100

      if TrainingState == True:
        biogas_plant.StorageData (name = user)

    #offline variables offline  
    if (Online == False and OfflineEntranceVariables == True):  #Modo Offline and variables from plant
      
      #Operación planta
      VR1 = data["anaerobicReactorVolume1"]["value"]
      VR2 = data["anaerobicReactorVolume2"]["value"]
      OperationMode = data["inputOperationMode"]
      Model = data["operationModelType"]

      #Tanques biogás
      VG1 = data["biogasTankVolume1"]["value"]        #1.6 factor de corrección de planta (biogás perdido en tuberías y reservorios)
      VG2 = data["biogasTankVolume1"]["value"]
      VG3 = data["biogasTankVolume3"]["value"]

      #paso de tiempo
      tp = data["digitalTwinStepTime"]["value"]
      #Acelerador de la simulacion
      time_accelator = data["timeMultiplier"]["value"]
      #TraininData = data["selectedTrainingData"]["value"] Con el retorno del front entrenar la red en el init
      
      # Kinetics parameters for R101
      K_R101 = data["exponentialFactorR101"]["value"]
      Ea_R101 = data["activationEnergyR101"]["value"]
      L_R101 = data["lambdaR101"]["value"]
      pH_R101 = data["inputPHR101"]["value"]

      #Kinetics parameters for R102
      K_R102 = data["exponentialFactorR102"]["value"]
      Ea_R102 = data["activationEnergyR102"]["value"]
      L_R102 = data["lambdaR102"]["value"]

      #initial conditions from frontEnd for R101
      ST_ini_R101 = data["initialAnalysisConditionsR101"]["totalSubstrateSolids"]["value"]
      SV_ini_R101 = data["initialAnalysisConditionsR101"]["volatileSubstrateSolids"]["value"]
      Cc_ini_R101 = data["initialAnalysisConditionsR101"]["atomicCarbonSubstrateConcetration"]["value"]
      Ch_ini_R101 = data["initialAnalysisConditionsR101"]["atomicHydrogenSubstrateConcetration"]["value"]
      Co_ini_R101 = data["initialAnalysisConditionsR101"]["atomicOxygenSubstrateConcetration"]["value"]
      Cn_ini_R101 = data["initialAnalysisConditionsR101"]["atomicNitrogenSubstrateConcetration"]["value"]
      Cs_ini_R101 = data["initialAnalysisConditionsR101"]["atomicSulfurSubstrateConcetration"]["value"]
      rho_ini_R101 = data["initialAnalysisConditionsR101"]["substrateDensity"]["value"]
      Temp_R101 = data["inputTemperatureR101"]["value"]

      #initial conditions from frontEnd for R102
      ST_ini_R102 = data["initialAnalysisConditionsR102"]["totalSubstrateSolids"]["value"]
      SV_ini_R102 = data["initialAnalysisConditionsR102"]["volatileSubstrateSolids"]["value"]
      Cc_ini_R102 = data["initialAnalysisConditionsR102"]["atomicCarbonSubstrateConcetration"]["value"]
      Ch_ini_R102 = data["initialAnalysisConditionsR102"]["atomicHydrogenSubstrateConcetration"]["value"]
      Co_ini_R102 = data["initialAnalysisConditionsR102"]["atomicOxygenSubstrateConcetration"]["value"]
      Cn_ini_R102 = data["initialAnalysisConditionsR102"]["atomicNitrogenSubstrateConcetration"]["value"]
      Cs_ini_R102 = data["initialAnalysisConditionsR102"]["atomicSulfurSubstrateConcetration"]["value"]
      rho_ini_R102 = data["initialAnalysisConditionsR102"]["substrateDensity"]["value"]

      #substrate conditions
      Cc = data["inputElementalAnalysisCarbonContent"]["value"]
      Ch = data["inputElementalAnalysisHydrogenContent"]["value"]
      Co = data["inputElementalAnalysisOxygenContent"]["value"]
      Cn = data["inputElementalAnalysisNitrogenContent"]["value"]
      Cs = data["inputElementalAnalysisSulfurContent"]["value"]
      rho = data["inputProximateAnalysisDensity"]["value"]
      ST = data["inputProximateAnalysisTotalSolids"]["value"]
      SV = data["inputProximateAnalysisVolatileSolids"]["value"]

      #pump 104 conditions
      TRH = data["inputPump104HydraulicRetentionTime"]["value"]
      FT_P104 = data["inputPump104StartsPerDay"]["value"]
      TTO_P104 = data["inputPump104StartTime"]["value"]

      #Pump 101 conditions
      FT_P101 = data["inputPump101StartsPerDay"]["value"]
      TTO_P101 = data["inputPump101StartTime"]["value"]
      Q_P101 = data["inputPump101Flow"]["value"]

      #Pump 102 conditions
      FT_P102 = data["inputPump102StartsPerDay"]["value"]
      TTO_P102 = data["inputPump102StartTime"]["value"]
      Q_P102 = data["inputPump102Flow"]["value"]

      #Mixer TK100
      FT_mixin_TK100 = data["inputStartsPerDayMixTK100"]["value"]
      TTO_mixing_TK100 = data["inputStartTimeMixTK100"]["value"]
      RPM_TK100 = data["inputSpeedMixTK100"]["value"]

      #Mixer R101
      FT_mixin_R101 = data["inputStartsPerDayMixR101"]["value"]
      TTO_mixing_R101 = data["inputStartTimeMixR101"]["value"]
      RPM_R101 = data["inputSpeedMixR101"]["value"]

      #Mixer R102
      FT_mixin_R102 = data["inputStartsPerDayMixR102"]["value"]
      TTO_mixing_R102 = data["inputStartTimeMixR102"]["value"]
      RPM_R102 = data["inputSpeedMixR102"]["value"]

      #Temperature R101
      T_R101 = data["inputTemperatureR101"]["value"]

      #PH R101
      pH_R101 = data["inputPHR101"]["value"]

      #Temperature R102
      T_R102 = data["inputTemperatureR101"]["value"]

      #PH R102
      pH_R102 = data["inputPHR102"]["value"]

      if user not in biogas_instances:
         biogas_instances[user] = Biogas_Model_Simulation.BiogasPlantSimulation(VR1 = VR1, VR2 = VR2, VG1=VG1, VG2 = VG2, VG3 = VG3, tp = tp,
                                                                ST_R101 = ST_ini_R101, SV_R101 = SV_ini_R101, Cc_R101 = Cc_ini_R101, Ch_R101 = Ch_ini_R101, Co_R101 = Co_ini_R101, Cn_R101 = Cn_ini_R101, Cs_R101 = Cs_ini_R101, rho_R101 = rho_ini_R101,
                                                                ST_R102 = ST_ini_R102, SV_R102 = SV_ini_R102, Cc_R102 = Cc_ini_R102, Ch_R102 = Ch_ini_R102, Co_R102 = Co_ini_R102, Cn_R102 = Cn_ini_R102, Cs_R102 = Cs_ini_R102, rho_R102 = rho_ini_R102,
                                                                OperationMode = OperationMode)
      
      #All offline Mode1
      if OperationMode == "Modo1":
        biogas_plant = biogas_instances[user]
        biogas_plant.Substrate_conditions(Cc = Cc, Ch = Ch, Co = Co, Cn = Cn, Cs = Cs, ST = ST, SV = SV, rho = rho)
        biogas_plant.Pump104(TRH = TRH, FT_P104 = FT_P104, TTO_P104 = TTO_P104, time_accelerator=time_accelator)
        biogas_plant.Mixing_TK100(FT_mixin_TK100 = FT_mixin_TK100, TTO_mixing_TK100 = TTO_mixing_TK100, RPM_TK100 = RPM_TK100)
        biogas_plant.Mixing_R101(FT_mixin_R101 = FT_mixin_R101, TTO_mixing_R101 = TTO_mixing_R101, RPM_R101 = RPM_R101)


        if Model == "Arrhenius":
          reactor_R101 = biogas_plant.Reactor101Simulation_ArrheniusModel(Operation=1, VR = VR1, Qin_1=biogas_plant.Q_P104v,
                                                                                Csus_in1 = biogas_plant.Csus_ini, K = K_R101,
                                                                                Ea = Ea_R101, T = T_R101, pH = pH_R101)
          biogas_output["K_R101"] = K_R101
          biogas_output["Ea_R101"] = Ea_R101

        elif Model == "ADM1":
          reactor_R101 = biogas_plant.Reactor101Simulation_ADM1(Operation=1, VR = VR1, Qin_1 = biogas_plant.Q_P104v,
                                                                    Csus_in1 = biogas_plant.Csus_ini, K = K_R101)
          biogas_output["K_R101"] = K_R101

        elif Model == "Gompertz":
          reactor_R101 = biogas_plant.Reactor101Simulation_Gompertz(Operation=1, ym = K_R101, U = Ea_R101, Lambda = L_R101, 
                                                                        Qin_1 = biogas_plant.Q_P104v)
          biogas_output["K_R101"] = K_R101
          biogas_output["Ea_R101"] = Ea_R101
          biogas_output["Lambda_R101"] = L_R101
        
        biogas_plant.V101_mode1(Pset=50, Model=Model)
        biogas_plant.V102_mode1(Pset=50)
        biogas_plant.V107_mode1(Pset=50)
        biogas_plant.biogas_treatment_model1(W_fe2O3=154.46, K_H2S=5/14.6955, K_NH3=0.2/14.6955, K_H2O=1/14.6955, w_carbon=3510.32, w_silica=3997.79, qmax_H2O=0.0167, qmax_H2S=0.00088, qmax_NH3=0.00101)
        biogas_plant.time_counter()

        #Exit Variables Mode 1
        #TK100
        biogas_output["n"] = biogas_plant.n
        biogas_output["a"] = biogas_plant.a
        biogas_output["b"] = biogas_plant.b
        biogas_output["c"] = biogas_plant.c
        biogas_output["d"] = biogas_plant.d
        biogas_output["Mix_Velocity_TK100"] = biogas_plant.RPM_TK100
        biogas_output["C_sv"] = biogas_plant.Csv                              #gSV/L
        biogas_output["SV"] = biogas_plant.SV
        biogas_output["C_st"] = biogas_plant.Cst
        biogas_output["ST"] = biogas_plant.ST
        # P104
        biogas_output["Pump104Flow"] = biogas_plant.Q_P104_Lh
        # R101
        biogas_output["Mix_Velocity_R101"] = biogas_plant.RPM_R101
        biogas_output["pH_R101"] = pH_R101
        biogas_output["Temp_R101"] = Temp_R101
        biogas_output["C_sv_R101"] = biogas_plant.SV_R101_gl
        biogas_output["SV_R101"] = biogas_plant.SV_R101_p*100
        biogas_output["C_st_R101"] = biogas_plant.ST_R101_gl
        biogas_output["ST_R101"] = biogas_plant.ST_R101_p*100
        biogas_output["Organic_Charge_R101"] = biogas_plant.Organic_Charge_R101
        biogas_output["x_R101"] = biogas_plant.x_R101*100
        # V101
        biogas_output["AcumBiogasPressureV101"] = biogas_plant.Pacum_V101
        biogas_output["StorageBiogasPressureV101"] = biogas_plant.Pstorage_V101
        biogas_output["AcumBiogasVolumenV101"] = biogas_plant.Vacum_std_V101
        biogas_output["StorageBiogasVolumeV101"] = biogas_plant.Vstorage_std_V101
        biogas_output["StorageCH4_V101Volume"] = biogas_plant.Vol_acum_CH4_V101
        biogas_output["StorageCH4_V101Concentration"] = biogas_plant.xCH4_V101*100
        biogas_output["StorageCH4_V101moles"] = biogas_plant.molCH4_acum_V101
        biogas_output["StorageCO2_V101Volume"] = biogas_plant.Vol_acum_CO2_V101
        biogas_output["StorageCO2_V101Concentration"] = biogas_plant.xCO2_V101*100
        biogas_output["StorageCO2_V101moles"] = biogas_plant.molCO2_acum_V101
        biogas_output["StorageH2S_V101Volume"] = biogas_plant.Vol_acum_H2S_V101
        biogas_output["StorageH2S_V101Concentration"] = biogas_plant.xH2S_V101*1000000
        biogas_output["StorageH2S_V101moles"] = biogas_plant.molH2S_acum_V101
        biogas_output["StorageO2_V101Volume"] = biogas_plant.Vol_acum_O2_V101
        biogas_output["StorageO2_V101Concentration"] = biogas_plant.xO2_V101*100
        biogas_output["StorageO2_V101moles"] = biogas_plant.molO2_acum_V101
        biogas_output["StorageH2_V101Volume"] = biogas_plant.Vol_acum_H2_V101
        biogas_output["StorageH2_V101Concentration"] = biogas_plant.xH2_V101*1000000
        biogas_output["StorageH2_V101moles"] = biogas_plant.molH2_acum_V101
        biogas_output["StorageNH3_V101Volume"] = biogas_plant.Vol_acum_NH3_V101
        biogas_output["StorageNH3_V101Concentration"] = biogas_plant.xNH3_V101*1000000
        biogas_output["StorageNH3_V101moles"] = biogas_plant.molNH3_acum_V101
        biogas_output["moles_humidity_V101"] = biogas_plant.molH2O_acum_V101
        biogas_output["Relative_humidity_V101"] = biogas_plant.RH_V101
        biogas_output["StorageEnergy_V101"] = biogas_plant.Energy_V101/3600
        # V102
        biogas_output["AcumBiogasPressureV102"] = biogas_plant.Pacum_V102
        biogas_output["StorageBiogasPressureV102"] = biogas_plant.Pstorage_V102
        biogas_output["AcumBiogasVolumenV102"] = biogas_plant.Vacum_std_V102
        biogas_output["StorageBiogasVolumeV102"] = biogas_plant.Vstorage_std_V102
        biogas_output["StorageCH4_V102Volume"] = biogas_plant.Vol_acum_CH4_V102
        biogas_output["StorageCH4_V102Concentration"] = biogas_plant.xCH4_V102*100
        biogas_output["StorageCH4_V102moles"] = biogas_plant.molCH4_acum_V102
        biogas_output["StorageCO2_V102Volume"] = biogas_plant.Vol_acum_CO2_V102
        biogas_output["StorageCO2_V102Concentration"] = biogas_plant.xCO2_V102*100
        biogas_output["StorageCO2_V102moles"] = biogas_plant.molCO2_acum_V102
        biogas_output["StorageH2S_V102Volume"] = biogas_plant.Vol_acum_H2S_V102
        biogas_output["StorageH2S_V102Concentration"] = biogas_plant.xH2S_V102*1000000
        biogas_output["StorageH2S_V102moles"] = biogas_plant.molH2S_acum_V102
        biogas_output["StorageO2_V102Volume"] = biogas_plant.Vol_acum_O2_V102
        biogas_output["StorageO2_V102Concentration"] = biogas_plant.xO2_V102*100
        biogas_output["StorageO2_V102moles"] = biogas_plant.molO2_acum_V102
        biogas_output["StorageH2_V102Volume"] = biogas_plant.Vol_acum_H2_V102
        biogas_output["StorageH2_V102Concentration"] = biogas_plant.xH2_V102*1000000
        biogas_output["StorageH2_V102moles"] = biogas_plant.molH2_acum_V102
        biogas_output["StorageNH3_V102Volume"] = biogas_plant.Vol_acum_NH3_V102
        biogas_output["StorageNH3_V102Concentration"] = biogas_plant.xNH3_V102*1000000
        biogas_output["StorageNH3_V102moles"] = biogas_plant.molNH3_acum_V102
        biogas_output["moles_humidity_V102"] = biogas_plant.molH2O_acum_V102
        biogas_output["Relative_humidity_V102"] = biogas_plant.RH_V102
        biogas_output["StorageEnergy_V102"] = biogas_plant.Energy_V102/3600
        # V107
        biogas_output["AcumBiogasPressureV107"] = biogas_plant.Pacum_V107
        biogas_output["StorageBiogasPressureV107"] = biogas_plant.Pstorage_V107
        biogas_output["AcumBiogasVolumenV107"] = biogas_plant.Vacum_std_V107
        biogas_output["StorageBiogasVolumeV107"] = biogas_plant.Vstorage_std_V107
        biogas_output["StorageCH4_V107Volume"] = biogas_plant.Vol_acum_CH4_V107
        biogas_output["StorageCH4_V107Concentration"] = biogas_plant.xCH4_V107*100
        biogas_output["StorageCH4_V107moles"] = biogas_plant.molCH4_acum_V107
        biogas_output["StorageCO2_V107Volume"] = biogas_plant.Vol_acum_CO2_V107
        biogas_output["StorageCO2_V107Concentration"] = biogas_plant.xCO2_V107*100
        biogas_output["StorageCO2_V107moles"] = biogas_plant.molCO2_acum_V107
        biogas_output["StorageH2S_V107Volume"] = biogas_plant.Vol_acum_H2S_V107
        biogas_output["StorageH2S_V107Concentration"] = biogas_plant.xH2S_V107*1000000
        biogas_output["StorageH2S_V107moles"] = biogas_plant.molH2S_acum_V107
        biogas_output["StorageO2_V107Volume"] = biogas_plant.Vol_acum_O2_V107
        biogas_output["StorageO2_V107Concentration"] = biogas_plant.xO2_V107*100
        biogas_output["StorageO2_V107moles"] = biogas_plant.molO2_acum_V107
        biogas_output["StorageH2_V107Volume"] = biogas_plant.Vol_acum_H2_V107
        biogas_output["StorageH2_V107Concentration"] = biogas_plant.xH2_V107*1000000
        biogas_output["StorageH2_V107moles"] = biogas_plant.molH2_acum_V107
        biogas_output["StorageNH3_V107Volume"] = biogas_plant.Vol_acum_NH3_V107
        biogas_output["StorageNH3_V107Concentration"] = biogas_plant.xNH3_V107*1000000
        biogas_output["StorageNH3_V107moles"] = biogas_plant.molNH3_acum_V107
        biogas_output["moles_humidity_V107"] = biogas_plant.molH2O_acum_V107
        biogas_output["Relative_humidity_V107"] = biogas_plant.RH_V107
        biogas_output["StorageEnergy_V107"] = biogas_plant.Energy_V107/3600
        #biogasTreatment
        biogas_output["ads_NH3_bt"] = biogas_plant.mol_NH3_ads_acum
        biogas_output["ads_H2S_bt"] = biogas_plant.mol_H2S_ads_acum
        biogas_output["ads_H2O_bt"] = biogas_plant.mol_H2O_ads_acum
        biogas_output["x_bt"] = biogas_plant.Xglobal * 100

      elif OperationMode == "Modo2":
        biogas_plant = biogas_instances[user]
        biogas_plant.Substrate_conditions(Cc = Cc, Ch = Ch, Co = Co, Cn = Cn, Cs = Cs, ST = ST, SV = SV, rho = rho)
        biogas_plant.Pump104(TRH = TRH, FT_P104 = FT_P104, TTO_P104 = TTO_P104, time_accelerator=time_accelator)
        biogas_plant.Pump101(FT_P101=24, TTO_P101=TTO_P101, Q_P101=Q_P101)
        biogas_plant.Mixing_TK100(FT_mixin_TK100 = FT_mixin_TK100, TTO_mixing_TK100 = TTO_mixing_TK100, RPM_TK100 = RPM_TK100)
        biogas_plant.Mixing_R101(FT_mixin_R101 = FT_mixin_R101, TTO_mixing_R101 = TTO_mixing_R101, RPM_R101 = RPM_R101)

        if Model == "Arrhenius":
          reactor_R101 = biogas_plant.Reactor101Simulation_ArrheniusModel(Operation=1, VR = VR1, Qin_1=biogas_plant.Q_P104v,
                                                                                Csus_in1 = biogas_plant.Csus_ini, K = K_R101,
                                                                                Ea = Ea_R101, T = T_R101, pH = pH_R101)
          biogas_output["K_R101"] = K_R101
          biogas_output["Ea_R101"] = Ea_R101

        elif Model == "ADM1":
          reactor_R101 = biogas_plant.Reactor101Simulation_ADM1(Operation=1, VR = VR1, Qin_1 = biogas_plant.Q_P104v,
                                                                    Csus_in1 = biogas_plant.Csus_ini, K = K_R101)
          biogas_output["K_R101"] = K_R101

        elif Model == "Gompertz":
          reactor_R101 = biogas_plant.Reactor101Simulation_Gompertz(Operation=1, ym = K_R101, U = Ea_R101, Lambda = L_R101, 
                                                                        Qin_1 = biogas_plant.Q_P104v)
          biogas_output["K_R101"] = K_R101
          biogas_output["Ea_R101"] = Ea_R101
          biogas_output["Lambda_R101"] = L_R101
        
        biogas_plant.V101_mode1(Pset=50, Model=Model)
        biogas_plant.V102_mode1(Pset=50)
        biogas_plant.V107_mode1(Pset=50)
        biogas_plant.biogas_treatment_model1(W_fe2O3=154.46, K_H2S=5/14.6955, K_NH3=0.2/14.6955, K_H2O=1/14.6955, w_carbon=3510.32, w_silica=3997.79, qmax_H2O=0.0167, qmax_H2S=0.00088, qmax_NH3=0.00101)
        biogas_plant.time_counter()
      
        #Exit Variables Mode 2
        #TK100
        biogas_output["n"] = biogas_plant.n
        biogas_output["a"] = biogas_plant.a
        biogas_output["b"] = biogas_plant.b
        biogas_output["c"] = biogas_plant.c
        biogas_output["d"] = biogas_plant.d
        biogas_output["Mix_Velocity_TK100"] = biogas_plant.RPM_TK100
        biogas_output["C_sv"] = biogas_plant.Csv                              #gSV/L
        biogas_output["SV"] = biogas_plant.SV
        biogas_output["C_st"] = biogas_plant.Cst
        biogas_output["ST"] = biogas_plant.ST
        # P104
        biogas_output["Pump104Flow"] = biogas_plant.Q_P104_Lh
        #P101
        biogas_output["Pump101Flow"] = biogas_plant.Q_P101
        # R101
        biogas_output["Mix_Velocity_R101"] = biogas_plant.RPM_R101
        biogas_output["pH_R101"] = pH_R101
        biogas_output["Temp_R101"] = Temp_R101
        biogas_output["C_sv_R101"] = biogas_plant.SV_R101_gl
        biogas_output["SV_R101"] = biogas_plant.SV_R101_p*100
        biogas_output["C_st_R101"] = biogas_plant.ST_R101_gl
        biogas_output["ST_R101"] = biogas_plant.ST_R101_p*100
        biogas_output["Organic_Charge_R101"] = biogas_plant.Organic_Charge_R101
        biogas_output["x_R101"] = biogas_plant.x_R101*100
        # V101
        biogas_output["AcumBiogasPressureV101"] = biogas_plant.Pacum_V101
        biogas_output["StorageBiogasPressureV101"] = biogas_plant.Pstorage_V101
        biogas_output["AcumBiogasVolumenV101"] = biogas_plant.Vacum_std_V101
        biogas_output["StorageBiogasVolumeV101"] = biogas_plant.Vstorage_std_V101
        biogas_output["StorageCH4_V101Volume"] = biogas_plant.Vol_acum_CH4_V101
        biogas_output["StorageCH4_V101Concentration"] = biogas_plant.xCH4_V101*100
        biogas_output["StorageCH4_V101moles"] = biogas_plant.molCH4_acum_V101
        biogas_output["StorageCO2_V101Volume"] = biogas_plant.Vol_acum_CO2_V101
        biogas_output["StorageCO2_V101Concentration"] = biogas_plant.xCO2_V101*100
        biogas_output["StorageCO2_V101moles"] = biogas_plant.molCO2_acum_V101
        biogas_output["StorageH2S_V101Volume"] = biogas_plant.Vol_acum_H2S_V101
        biogas_output["StorageH2S_V101Concentration"] = biogas_plant.xH2S_V101*1000000
        biogas_output["StorageH2S_V101moles"] = biogas_plant.molH2S_acum_V101
        biogas_output["StorageO2_V101Volume"] = biogas_plant.Vol_acum_O2_V101
        biogas_output["StorageO2_V101Concentration"] = biogas_plant.xO2_V101*100
        biogas_output["StorageO2_V101moles"] = biogas_plant.molO2_acum_V101
        biogas_output["StorageH2_V101Volume"] = biogas_plant.Vol_acum_H2_V101
        biogas_output["StorageH2_V101Concentration"] = biogas_plant.xH2_V101*1000000
        biogas_output["StorageH2_V101moles"] = biogas_plant.molH2_acum_V101
        biogas_output["StorageNH3_V101Volume"] = biogas_plant.Vol_acum_NH3_V101
        biogas_output["StorageNH3_V101Concentration"] = biogas_plant.xNH3_V101*1000000
        biogas_output["StorageNH3_V101moles"] = biogas_plant.molNH3_acum_V101
        biogas_output["moles_humidity_V101"] = biogas_plant.molH2O_acum_V101
        biogas_output["Relative_humidity_V101"] = biogas_plant.RH_V101
        biogas_output["StorageEnergy_V101"] = biogas_plant.Energy_V101/3600
        # V102
        biogas_output["AcumBiogasPressureV102"] = biogas_plant.Pacum_V102
        biogas_output["StorageBiogasPressureV102"] = biogas_plant.Pstorage_V102
        biogas_output["AcumBiogasVolumenV102"] = biogas_plant.Vacum_std_V102
        biogas_output["StorageBiogasVolumeV102"] = biogas_plant.Vstorage_std_V102
        biogas_output["StorageCH4_V102Volume"] = biogas_plant.Vol_acum_CH4_V102
        biogas_output["StorageCH4_V102Concentration"] = biogas_plant.xCH4_V102*100
        biogas_output["StorageCH4_V102moles"] = biogas_plant.molCH4_acum_V102
        biogas_output["StorageCO2_V102Volume"] = biogas_plant.Vol_acum_CO2_V102
        biogas_output["StorageCO2_V102Concentration"] = biogas_plant.xCO2_V102*100
        biogas_output["StorageCO2_V102moles"] = biogas_plant.molCO2_acum_V102
        biogas_output["StorageH2S_V102Volume"] = biogas_plant.Vol_acum_H2S_V102
        biogas_output["StorageH2S_V102Concentration"] = biogas_plant.xH2S_V102*1000000
        biogas_output["StorageH2S_V102moles"] = biogas_plant.molH2S_acum_V102
        biogas_output["StorageO2_V102Volume"] = biogas_plant.Vol_acum_O2_V102
        biogas_output["StorageO2_V102Concentration"] = biogas_plant.xO2_V102*100
        biogas_output["StorageO2_V102moles"] = biogas_plant.molO2_acum_V102
        biogas_output["StorageH2_V102Volume"] = biogas_plant.Vol_acum_H2_V102
        biogas_output["StorageH2_V102Concentration"] = biogas_plant.xH2_V102*1000000
        biogas_output["StorageH2_V102moles"] = biogas_plant.molH2_acum_V102
        biogas_output["StorageNH3_V102Volume"] = biogas_plant.Vol_acum_NH3_V102
        biogas_output["StorageNH3_V102Concentration"] = biogas_plant.xNH3_V102*1000000
        biogas_output["StorageNH3_V102moles"] = biogas_plant.molNH3_acum_V102
        biogas_output["moles_humidity_V102"] = biogas_plant.molH2O_acum_V102
        biogas_output["Relative_humidity_V102"] = biogas_plant.RH_V102
        biogas_output["StorageEnergy_V102"] = biogas_plant.Energy_V102/3600
        # V107
        biogas_output["AcumBiogasPressureV107"] = biogas_plant.Pacum_V107
        biogas_output["StorageBiogasPressureV107"] = biogas_plant.Pstorage_V107
        biogas_output["AcumBiogasVolumenV107"] = biogas_plant.Vacum_std_V107
        biogas_output["StorageBiogasVolumeV107"] = biogas_plant.Vstorage_std_V107
        biogas_output["StorageCH4_V107Volume"] = biogas_plant.Vol_acum_CH4_V107
        biogas_output["StorageCH4_V107Concentration"] = biogas_plant.xCH4_V107*100
        biogas_output["StorageCH4_V107moles"] = biogas_plant.molCH4_acum_V107
        biogas_output["StorageCO2_V107Volume"] = biogas_plant.Vol_acum_CO2_V107
        biogas_output["StorageCO2_V107Concentration"] = biogas_plant.xCO2_V107*100
        biogas_output["StorageCO2_V107moles"] = biogas_plant.molCO2_acum_V107
        biogas_output["StorageH2S_V107Volume"] = biogas_plant.Vol_acum_H2S_V107
        biogas_output["StorageH2S_V107Concentration"] = biogas_plant.xH2S_V107*1000000
        biogas_output["StorageH2S_V107moles"] = biogas_plant.molH2S_acum_V107
        biogas_output["StorageO2_V107Volume"] = biogas_plant.Vol_acum_O2_V107
        biogas_output["StorageO2_V107Concentration"] = biogas_plant.xO2_V107*100
        biogas_output["StorageO2_V107moles"] = biogas_plant.molO2_acum_V107
        biogas_output["StorageH2_V107Volume"] = biogas_plant.Vol_acum_H2_V107
        biogas_output["StorageH2_V107Concentration"] = biogas_plant.xH2_V107*1000000
        biogas_output["StorageH2_V107moles"] = biogas_plant.molH2_acum_V107
        biogas_output["StorageNH3_V107Volume"] = biogas_plant.Vol_acum_NH3_V107
        biogas_output["StorageNH3_V107Concentration"] = biogas_plant.xNH3_V107*1000000
        biogas_output["StorageNH3_V107moles"] = biogas_plant.molNH3_acum_V107
        biogas_output["moles_humidity_V107"] = biogas_plant.molH2O_acum_V107
        biogas_output["Relative_humidity_V107"] = biogas_plant.RH_V107
        biogas_output["StorageEnergy_V107"] = biogas_plant.Energy_V107/3600
        #biogasTreatment
        biogas_output["ads_NH3_bt"] = biogas_plant.mol_NH3_ads_acum
        biogas_output["ads_H2S_bt"] = biogas_plant.mol_H2S_ads_acum
        biogas_output["ads_H2O_bt"] = biogas_plant.mol_H2O_ads_acum
        biogas_output["x_bt"] = biogas_plant.Xglobal * 100

      elif OperationMode == "Modo3":
        biogas_plant = biogas_instances[user]
        biogas_plant.Substrate_conditions(Cc = Cc, Ch = Ch, Co = Co, Cn = Cn, Cs = Cs, ST = ST, SV = SV, rho = rho)
        biogas_plant.Pump104(TRH = TRH, FT_P104 = FT_P104, TTO_P104 = TTO_P104, time_accelerator=time_accelator)
        biogas_plant.Mixing_TK100(FT_mixin_TK100=FT_mixin_TK100, TTO_mixing_TK100 = TTO_mixing_TK100, RPM_TK100=RPM_TK100)
        biogas_plant.Mixing_R101(FT_mixin_R101=FT_mixin_R101, TTO_mixing_R101=TTO_mixing_R101, RPM_R101=RPM_R101)
        biogas_plant.Mixing_R102(FT_mixin_R102=FT_mixin_R102, TTO_mixing_R102=TTO_mixing_R102, RPM_R102=RPM_R102)

        if Model == "Arrhenius":
            biogas_plant.Reactor101Simulation_ArrheniusModel(Operation=1, VR=VR1, Qin_1=biogas_plant.Q_P104v, Csus_in1=biogas_plant.Csus_ini,
                                                              K=K_R101, Ea=Ea_R101, T=T_R101, pH = pH_R101)
            biogas_plant.Reactor102Simulation_ArrheniusModel(Operation=1, VR=VR2, Qin_1=biogas_plant.Q_P104v, Csus_in1=biogas_plant.Csus_ini_R101,
                                                              K = K_R102, Ea=Ea_R102, T=T_R102, pH = pH_R102)
            
            biogas_output["K_R101"] = K_R101
            biogas_output["Ea_R101"] = Ea_R101
            biogas_output["K_R102"] = K_R102
            biogas_output["Ea_R102"] = Ea_R102

        if Model == "ADM1":
            biogas_plant.Reactor101Simulation_ADM1(Operation=1, VR=VR1, Qin_1=biogas_plant.Q_P104v, Csus_in1 = biogas_plant.Csus_ini, K=K_R101)
            biogas_plant.Reactor102Simulation_ADM1(Operation=1, VR=VR2, Qin_1=biogas_plant.Q_P104v, Csus_in1=biogas_plant.Csus_ini_R101, K=K_R102)
            
            biogas_output["K_R101"] = K_R101
            biogas_output["K_R102"] = K_R102
          
        if Model == "Gompertz":
            biogas_plant.Reactor101Simulation_Gompertz(Operation=1, ym = K_R101, U = Ea_R101, Lambda = L_R101, Qin_1=biogas_plant.Q_P104v)
            biogas_plant.Reactor102Simulation_Gompertz(Operation=1, ym = K_R102, U = Ea_R102, Lambda = L_R102, Qin_1 = biogas_plant.Q_P104v)
            
            biogas_output["K_R101"] = K_R101
            biogas_output["Ea_R101"] = Ea_R101
            biogas_output["Lambda_R101"] = L_R101
            biogas_output["K_R102"] = K_R102
            biogas_output["Ea_R102"] = Ea_R102
            biogas_output["Lambda_R102"] = L_R102
            
        biogas_plant.V101_mode1(Pset = 50, Model = Model)
        biogas_plant.V102_mode2(Pset = 50)
        biogas_plant.V107_mode1(Pset = 50)
        biogas_plant.biogas_treatment_model1(W_fe2O3=154.46, K_H2S=5/14.6955, K_NH3=0.2/14.6955, K_H2O=(1/14.6955), w_carbon=3510.32, w_silica=3997.79, qmax_H2O=0.000167, qmax_H2S=0.00088, qmax_NH3=0.00101, k2_H2O=0.01)
        biogas_plant.time_counter()

        #Exit Variables Mode 3
        #TK100
        biogas_output["n"] = biogas_plant.n
        biogas_output["a"] = biogas_plant.a
        biogas_output["b"] = biogas_plant.b
        biogas_output["c"] = biogas_plant.c
        biogas_output["d"] = biogas_plant.d
        biogas_output["Mix_Velocity_TK100"] = biogas_plant.RPM_TK100
        biogas_output["C_sv"] = biogas_plant.Csv                              #gSV/L
        biogas_output["SV"] = biogas_plant.SV
        biogas_output["C_st"] = biogas_plant.Cst
        biogas_output["ST"] = biogas_plant.ST
        # P104
        biogas_output["Pump104Flow"] = biogas_plant.Q_P104_Lh
        #P101
        biogas_output["Pump101Flow"] = biogas_plant.Q_P104_Lh
        # R101
        biogas_output["Mix_Velocity_R101"] = biogas_plant.RPM_R101
        biogas_output["pH_R101"] = pH_R101
        biogas_output["Temp_R101"] = T_R101
        biogas_output["C_sv_R101"] = biogas_plant.SV_R101_gl
        biogas_output["SV_R101"] = biogas_plant.SV_R101_p*100
        biogas_output["C_st_R101"] = biogas_plant.ST_R101_gl
        biogas_output["ST_R101"] = biogas_plant.ST_R101_p*100
        biogas_output["Organic_Charge_R101"] = biogas_plant.Organic_Charge_R101
        biogas_output["x_R101"] = biogas_plant.x_R101*100
        # R102
        biogas_output["Mix_Velocity_R102"] = biogas_plant.RPM_R102
        biogas_output["pH_R102"] = pH_R102
        biogas_output["Temp_R102"] = T_R102
        biogas_output["C_sv_R102"] = biogas_plant.SV_R102_gl
        biogas_output["SV_R102"] = biogas_plant.SV_R102_p*100
        biogas_output["C_st_R102"] = biogas_plant.ST_R102_gl
        biogas_output["ST_R102"] = biogas_plant.ST_R102_p*100
        biogas_output["Organic_Charge_R102"] = biogas_plant.Organic_Charge_R102
        biogas_output["x_R102"] = biogas_plant.x_R102*100
        # V101
        biogas_output["AcumBiogasPressureV101"] = biogas_plant.Pacum_V101
        biogas_output["StorageBiogasPressureV101"] = biogas_plant.Pstorage_V101
        biogas_output["AcumBiogasVolumenV101"] = biogas_plant.Vacum_std_V101
        biogas_output["StorageBiogasVolumeV101"] = biogas_plant.Vstorage_std_V101
        biogas_output["StorageCH4_V101Volume"] = biogas_plant.Vol_acum_CH4_V101
        biogas_output["StorageCH4_V101Concentration"] = biogas_plant.xCH4_V101*100
        biogas_output["StorageCH4_V101moles"] = biogas_plant.molCH4_acum_V101
        biogas_output["StorageCO2_V101Volume"] = biogas_plant.Vol_acum_CO2_V101
        biogas_output["StorageCO2_V101Concentration"] = biogas_plant.xCO2_V101*100
        biogas_output["StorageCO2_V101moles"] = biogas_plant.molCO2_acum_V101
        biogas_output["StorageH2S_V101Volume"] = biogas_plant.Vol_acum_H2S_V101
        biogas_output["StorageH2S_V101Concentration"] = biogas_plant.xH2S_V101*1000000
        biogas_output["StorageH2S_V101moles"] = biogas_plant.molH2S_acum_V101
        biogas_output["StorageO2_V101Volume"] = biogas_plant.Vol_acum_O2_V101
        biogas_output["StorageO2_V101Concentration"] = biogas_plant.xO2_V101*100
        biogas_output["StorageO2_V101moles"] = biogas_plant.molO2_acum_V101
        biogas_output["StorageH2_V101Volume"] = biogas_plant.Vol_acum_H2_V101
        biogas_output["StorageH2_V101Concentration"] = biogas_plant.xH2_V101*1000000
        biogas_output["StorageH2_V101moles"] = biogas_plant.molH2_acum_V101
        biogas_output["StorageNH3_V101Volume"] = biogas_plant.Vol_acum_NH3_V101
        biogas_output["StorageNH3_V101Concentration"] = biogas_plant.xNH3_V101*1000000
        biogas_output["StorageNH3_V101moles"] = biogas_plant.molNH3_acum_V101
        biogas_output["moles_humidity_V101"] = biogas_plant.molH2O_acum_V101
        biogas_output["Relative_humidity_V101"] = biogas_plant.RH_V101
        biogas_output["StorageEnergy_V101"] = biogas_plant.Energy_V101/3600
        # V102
        biogas_output["AcumBiogasPressureV102"] = biogas_plant.Pacum_V102
        biogas_output["StorageBiogasPressureV102"] = biogas_plant.Pstorage_V102
        biogas_output["AcumBiogasVolumenV102"] = biogas_plant.Vacum_std_V102
        biogas_output["StorageBiogasVolumeV102"] = biogas_plant.Vstorage_std_V102
        biogas_output["StorageCH4_V102Volume"] = biogas_plant.Vol_acum_CH4_V102
        biogas_output["StorageCH4_V102Concentration"] = biogas_plant.xCH4_V102*100
        biogas_output["StorageCH4_V102moles"] = biogas_plant.molCH4_acum_V102
        biogas_output["StorageCO2_V102Volume"] = biogas_plant.Vol_acum_CO2_V102
        biogas_output["StorageCO2_V102Concentration"] = biogas_plant.xCO2_V102*100
        biogas_output["StorageCO2_V102moles"] = biogas_plant.molCO2_acum_V102
        biogas_output["StorageH2S_V102Volume"] = biogas_plant.Vol_acum_H2S_V102
        biogas_output["StorageH2S_V102Concentration"] = biogas_plant.xH2S_V102*1000000
        biogas_output["StorageH2S_V102moles"] = biogas_plant.molH2S_acum_V102
        biogas_output["StorageO2_V102Volume"] = biogas_plant.Vol_acum_O2_V102
        biogas_output["StorageO2_V102Concentration"] = biogas_plant.xO2_V102*100
        biogas_output["StorageO2_V102moles"] = biogas_plant.molO2_acum_V102
        biogas_output["StorageH2_V102Volume"] = biogas_plant.Vol_acum_H2_V102
        biogas_output["StorageH2_V102Concentration"] = biogas_plant.xH2_V102*1000000
        biogas_output["StorageH2_V102moles"] = biogas_plant.molH2_acum_V102
        biogas_output["StorageNH3_V102Volume"] = biogas_plant.Vol_acum_NH3_V102
        biogas_output["StorageNH3_V102Concentration"] = biogas_plant.xNH3_V102*1000000
        biogas_output["StorageNH3_V102moles"] = biogas_plant.molNH3_acum_V102
        biogas_output["moles_humidity_V102"] = biogas_plant.molH2O_acum_V102
        biogas_output["Relative_humidity_V102"] = biogas_plant.RH_V102
        biogas_output["StorageEnergy_V102"] = biogas_plant.Energy_V102/3600
        # V107
        biogas_output["AcumBiogasPressureV107"] = biogas_plant.Pacum_V107
        biogas_output["StorageBiogasPressureV107"] = biogas_plant.Pstorage_V107
        biogas_output["AcumBiogasVolumenV107"] = biogas_plant.Vacum_std_V107
        biogas_output["StorageBiogasVolumeV107"] = biogas_plant.Vstorage_std_V107
        biogas_output["StorageCH4_V107Volume"] = biogas_plant.Vol_acum_CH4_V107
        biogas_output["StorageCH4_V107Concentration"] = biogas_plant.xCH4_V107*100
        biogas_output["StorageCH4_V107moles"] = biogas_plant.molCH4_acum_V107
        biogas_output["StorageCO2_V107Volume"] = biogas_plant.Vol_acum_CO2_V107
        biogas_output["StorageCO2_V107Concentration"] = biogas_plant.xCO2_V107*100
        biogas_output["StorageCO2_V107moles"] = biogas_plant.molCO2_acum_V107
        biogas_output["StorageH2S_V107Volume"] = biogas_plant.Vol_acum_H2S_V107
        biogas_output["StorageH2S_V107Concentration"] = biogas_plant.xH2S_V107*1000000
        biogas_output["StorageH2S_V107moles"] = biogas_plant.molH2S_acum_V107
        biogas_output["StorageO2_V107Volume"] = biogas_plant.Vol_acum_O2_V107
        biogas_output["StorageO2_V107Concentration"] = biogas_plant.xO2_V107*100
        biogas_output["StorageO2_V107moles"] = biogas_plant.molO2_acum_V107
        biogas_output["StorageH2_V107Volume"] = biogas_plant.Vol_acum_H2_V107
        biogas_output["StorageH2_V107Concentration"] = biogas_plant.xH2_V107*1000000
        biogas_output["StorageH2_V107moles"] = biogas_plant.molH2_acum_V107
        biogas_output["StorageNH3_V107Volume"] = biogas_plant.Vol_acum_NH3_V107
        biogas_output["StorageNH3_V107Concentration"] = biogas_plant.xNH3_V107*1000000
        biogas_output["StorageNH3_V107moles"] = biogas_plant.molNH3_acum_V107
        biogas_output["moles_humidity_V107"] = biogas_plant.molH2O_acum_V107
        biogas_output["Relative_humidity_V107"] = biogas_plant.RH_V107
        biogas_output["StorageEnergy_V107"] = biogas_plant.Energy_V107/3600
        #biogasTreatment
        biogas_output["ads_NH3_bt"] = biogas_plant.mol_NH3_ads_acum
        biogas_output["ads_H2S_bt"] = biogas_plant.mol_H2S_ads_acum
        biogas_output["ads_H2O_bt"] = biogas_plant.mol_H2O_ads_acum
        biogas_output["x_bt"] = biogas_plant.Xglobal * 100







    
    


    #Entrance variables for Training

    # biogas_input["iteration"] = data["iteration"]
    # biogas_input["name"] = data["name"]
    # UserKeys = []
    # UserKeys.append(biogas_input["name"])
    # if biogas_input["iteration"] == 1:
    #   for key in UserKeys:
    #     if key in biogas_instances:
    #       del biogas_instances[key]
    #   # if biogas_input["name"] is biogas_instances:
    #   #   del biogas_instance["name"]

    #   Biogas_Simulation_Start.BiogasSimulationStart.reset_instance()
    #   Biogas_Start.BiogasStart.reset_instance()
    #   MachineLearning_biogas_start.MachineLearningStart.reset_instance()
    
          
    # #Operación Planta
    # biogas_input["VR1"] = data["anaerobicReactorVolume1"]["value"]
    # biogas_input["VR2"] = data["anaerobicReactorVolume2"]["value"]
    # biogas_input["OperationMode"] = data["inputOperationMode"]
    
    # #Tanques de biogás
    # biogas_input["VG1"] = data["biogasTankVolume1"]["value"]
    # biogas_input["VG2"] = data["biogasTankVolume2"]["value"]
    # biogas_input["VG3"] = data["biogasTankVolume3"]["value"]

    # #Parámetros del gemelo
    # biogas_input["DigitalTwin"] = data["digitalTwinState"]
    # biogas_input["tp"] = data["digitalTwinStepTime"]["value"]
    # biogas_input["t_pred"] = data["digitalTwinForecastTime"]["value"]

    # #Parámetros cinéticos
    # biogas_input["OperationModel"] = data["operationModelType"]
    # biogas_input["A_R101"] = data["exponentialFactorR101"]["value"]
    # biogas_input["B_R101"] = data["activationEnergyR101"]["value"]
    # biogas_input["C_R101"] = data["lambdaR101"]["value"]
    # biogas_input["A_R102"] = data["exponentialFactorR102"]["value"]
    # biogas_input["B_R102"] = data["activationEnergyR102"]["value"]
    # biogas_input["C_R102"] = data["lambdaR102"]["value"]

    # #Tratamiento biogas
    # biogas_input["Dab_1"] = data["difussionCoefficientTower1"]["value"]
    # biogas_input["W1"] =  data["adsorbentWeightTower1"]["value"]
    # biogas_input["L1"] = data["lengthTower1"]["value"]
    # biogas_input["Dab_2"] = data["difussionCoefficientTower2"]["value"]
    # biogas_input["W2"] =  data["adsorbentWeightTower2"]["value"]
    # biogas_input["L2"] = data["lengthTower2"]["value"]
    # biogas_input["Dab_3"] = data["difussionCoefficientTower3"]["value"]
    # biogas_input["W3"] =  data["adsorbentWeightTower3"]["value"]
    # biogas_input["L3"] = data["lengthTower3"]["value"]

    # #Condiciones iniciales de los reactores
    # biogas_input["ST_R101"] = data["initialAnalysisConditionsR101"]["totalSubstrateSolids"]["value"]
    # biogas_input["SV_R101"] = data["initialAnalysisConditionsR101"]["volatileSubstrateSolids"]["value"]
    # biogas_input["rho_R101"] = data["initialAnalysisConditionsR101"]["substrateDensity"]["value"]
    # biogas_input["Cc_R101"] = data["initialAnalysisConditionsR101"]["atomicCarbonSubstrateConcetration"]["value"]
    # biogas_input["Ch_R101"] = data["initialAnalysisConditionsR101"]["atomicHydrogenSubstrateConcetration"]["value"]
    # biogas_input["Co_R101"] = data["initialAnalysisConditionsR101"]["atomicOxygenSubstrateConcetration"]["value"]
    # biogas_input["Cn_R101"] = data["initialAnalysisConditionsR101"]["atomicNitrogenSubstrateConcetration"]["value"]
    # biogas_input["Cs_R101"] = data["initialAnalysisConditionsR101"]["atomicSulfurSubstrateConcetration"]["value"]

    # biogas_input["ST_R102"] = data["initialAnalysisConditionsR102"]["totalSubstrateSolids"]["value"]
    # biogas_input["SV_R102"] = data["initialAnalysisConditionsR102"]["volatileSubstrateSolids"]["value"]
    # biogas_input["rho_R102"] = data["initialAnalysisConditionsR102"]["substrateDensity"]["value"]
    # biogas_input["Cc_R102"] = data["initialAnalysisConditionsR102"]["atomicCarbonSubstrateConcetration"]["value"]
    # biogas_input["Ch_R102"] = data["initialAnalysisConditionsR102"]["atomicHydrogenSubstrateConcetration"]["value"]
    # biogas_input["Co_R102"] = data["initialAnalysisConditionsR102"]["atomicOxygenSubstrateConcetration"]["value"]
    # biogas_input["Cn_R102"] = data["initialAnalysisConditionsR102"]["atomicNitrogenSubstrateConcetration"]["value"]
    # biogas_input["Cs_R102"] = data["initialAnalysisConditionsR102"]["atomicSulfurSubstrateConcetration"]["value"]


    # # Variables de operación
    # ##Condiciones del sustrato - Tanque de premezcla
    # biogas_input["manual_substrate"] = data["inputSubstrateConditions"]
    # biogas_input["Cc"] = data["inputElementalAnalysisCarbonContent"]["value"]
    # biogas_input["Ch"] = data["inputElementalAnalysisHydrogenContent"]["value"]
    # biogas_input["Co"] = data["inputElementalAnalysisOxygenContent"]["value"]  
    # biogas_input["Cn"] = data["inputElementalAnalysisNitrogenContent"]["value"]
    # biogas_input["Cs"] = data["inputElementalAnalysisSulfurContent"]["value"]
    # biogas_input["ST"] = data["inputProximateAnalysisTotalSolids"]["value"]
    # biogas_input["SV"] = data["inputProximateAnalysisVolatileSolids"]["value"]
    # biogas_input["rho"] = data["inputProximateAnalysisDensity"]["value"]

    # ##Condiciones de la bomba P-104
    # biogas_input["manual_P104"] = data["inputPump104"]
    # biogas_input["TRH"] = data["inputPump104HydraulicRetentionTime"]["value"]
    # biogas_input["TTO_P104"] = data["inputPump104StartTime"]["value"]
    # biogas_input["FT_P104"] = data["inputPump104StartsPerDay"]["value"]

    # #condiciones de la bomba P-101
    # biogas_input["manual_P101"] = data["inputPump101"]
    # biogas_input["Q_P101"] = data["inputPump101Flow"]["value"]
    # biogas_input["TTO_P101"] = data["inputPump101StartTime"]["value"]
    # biogas_input["FT_P101"] = data["inputPump101StartsPerDay"]["value"]

    # #condiciones de la bomba P-102
    # biogas_input["manual_P102"] = data["inputPump102"]
    # biogas_input["Q_P102"] = data["inputPump102Flow"]["value"]
    # biogas_input["TTO_P102"] = data["inputPump102StartTime"]["value"]
    # biogas_input["FT_P102"] = data["inputPump102StartsPerDay"]["value"]

    # #Condiciones TK100 premezcla
    # biogas_input["manual_mixing_TK100"] = data["inputMixTK100"]
    # biogas_input["FT_mixing_TK100"] = data["inputStartsPerDayMixTK100"]["value"]
    # biogas_input["TTO_mixing_TK100"] = data["inputStartTimeMixTK100"]["value"]
    # biogas_input["RPM_TK100"] = data["inputSpeedMixTK100"]["value"]

    # #condiciones del reactor R101
    # ## Agitación R101
    # biogas_input["manual_mixing_R101"] = data["inputMixR101"]
    # biogas_input["FT_mixing_R101"] = data["inputStartsPerDayMixR101"]["value"]
    # biogas_input["TTO_mixing_R101"] = data["inputStartTimeMixR101"]["value"]
    # biogas_input["RPM_R101"] = data["inputSpeedMixR101"]["value"]
    # ## Temperatura R101
    # biogas_input["manual_Temperature_R101"] = data["inputTemperatureR101"]['disabled']
    # biogas_input["Temperature_R101"] = data["inputTemperatureR101"]['value']
    # ## pH R101
    # biogas_input["manual_pH_R101"] = data["inputPHR101"]['disabled']
    # biogas_input["pH_R101"] = data["inputPHR101"]['value']

    # #condiciones del reactor R102
    # ## Agitación R102
    # biogas_input["manual_mixing_R102"] = data["inputMixR102"]
    # biogas_input["FT_mixing_R102"] = data["inputStartsPerDayMixR102"]["value"]
    # biogas_input["TTO_mixing_R102"] = data["inputStartTimeMixR102"]["value"]
    # biogas_input["RPM_R102"] = data["inputSpeedMixR102"]["value"]
    # ## Temperatura R102
    # biogas_input["manual_Temperature_R102"] = data["inputTemperatureR102"]['disabled']
    # biogas_input["Temperature_R102"] = data["inputTemperatureR102"]['value']
    # ## pH R102
    # biogas_input["manual_pH_R102"] = data["inputPHR102"]['disabled']
    # biogas_input["pH_R102"] = data["inputPHR102"]['value']

    # #Condiciones de la torre de adsorción 1
    # biogas_input["D1"] = data["difussionCoefficientTower1"]["value"]
    # biogas_input["W1"] = data["adsorbentWeightTower1"]["value"]
    # biogas_input["L1"] = data["lengthTower1"]["value"]

    # #Condiciones de la torre de adsorción 2
    # biogas_input["D2"] = data["difussionCoefficientTower2"]["value"]
    # biogas_input["W2"] = data["adsorbentWeightTower2"]["value"]
    # biogas_input["L2"] = data["lengthTower2"]["value"]

    #  #Condiciones de la torre de adsorción 3
    # biogas_input["D3"] = data["difussionCoefficientTower3"]["value"]
    # biogas_input["W3"] = data["adsorbentWeightTower3"]["value"]
    # biogas_input["L3"] = data["lengthTower3"]["value"]

    # if biogas_input["DigitalTwin"] == True: # Modo Gemelo On

    #   Biogas_Plant_ini = Biogas_Start.BiogasStart()
    #   Biogas_Plant_ini.starting(VR1 = biogas_input["VR1"], VR2 = biogas_input["VR2"], VG1 = biogas_input["VG1"], VG2 = biogas_input["VG2"],
    #                             VG3 = biogas_input["VG3"], tp = biogas_input["tp"], ST_R101 = biogas_input["ST_R101"], SV_R101 = biogas_input["SV_R101"],
    #                             Cc_R101 = biogas_input["Cc_R101"], Ch_R101 = biogas_input["Ch_R101"], Co_R101 = biogas_input["Co_R101"],
    #                             Cn_R101 = biogas_input["Cn_R101"], Cs_R101 = biogas_input["Cs_R101"], rho_R101 = biogas_input["rho_R101"],
    #                             ST_R102 = biogas_input["ST_R102"], SV_R102 = biogas_input["SV_R102"], Cc_R102 = biogas_input["Cc_R102"] ,
    #                             Ch_R102 = biogas_input["Ch_R102"], Co_R102 = biogas_input["Co_R102"], Cn_R102 = biogas_input["Cn_R102"],
    #                             Cs_R102 = biogas_input["Cs_R102"], rho_R102 = biogas_input["rho_R102"], OperationMode = biogas_input["OperationMode"])
    
    #   Biogas_Plant = Biogas_Plant_ini.data
    #   Biogas_Plant.GetValuesFromBiogasPlant()
    #   Biogas_Plant.Substrate_conditions(manual_substrate = biogas_input["manual_substrate"],Cc = biogas_input["Cc"], Ch = biogas_input["Ch"], Co =  biogas_input["Co"],
    #                                     Cn = biogas_input["Cn"], Cs = biogas_input["Cs"], rho = biogas_input["rho"], ST = biogas_input["ST"], SV = biogas_input["SV"])
    #   Biogas_Plant.pHR101(manual_pH_R101 = biogas_input["manual_pH_R101"], pH = biogas_input["pH_R101"])
    #   Biogas_Plant.pHR102(manual_pH_R102 = biogas_input["pH_R102"], pH = biogas_input["pH_R102"])
    #   Biogas_Plant.Pump104(manual_P104 = biogas_input["manual_P104"], TRH = biogas_input["TRH"], FT_P104 = biogas_input["FT_P104"], TTO_P104 = biogas_input["TTO_P104"])
    #   Biogas_Plant.Pump101(manual_P101 = biogas_input["manual_P101"], FT_P101 = biogas_input["FT_P101"], TTO_P101 = biogas_input["TTO_P101"], Q_P101 = biogas_input["Q_P101"])
    #   Biogas_Plant.Pump102(manual_P102 = biogas_input["manual_P102"], FT_P102 = biogas_input["FT_P102"], TTO_P102 = biogas_input["TTO_P102"], Q_P102 = biogas_input["Q_P102"])
    #   Biogas_Plant.Mixing_TK100(manual_mixing = biogas_input["manual_mixing_TK100"], FT_mixing_TK100 = biogas_input["FT_mixing_TK100"], TTO_mixing_TK100 = biogas_input["TTO_mixing_TK100"],
    #                              RPM_TK100 = biogas_input["RPM_TK100"])
    #   Biogas_Plant.Mixing_R101(manual_mixing = biogas_input["manual_mixing_R101"], FT_mixing_R101 = biogas_input["FT_mixing_R101"], TTO_mixing_R101 = biogas_input["TTO_mixing_R101"],
    #                              RPM_R101 = biogas_input["RPM_R101"])
    #   Biogas_Plant.Mixing_R102(manual_mixing = biogas_input["manual_mixing_R102"], FT_mixing_R102 = biogas_input["FT_mixing_R102"], TTO_mixing_R102 = biogas_input["TTO_mixing_R102"],
    #                              RPM_R102 = biogas_input["RPM_R102"])
    #   Biogas_Plant.Temperature_R101(manual_temp_R101 = biogas_input["manual_Temperature_R101"], Temp_R101 = biogas_input["Temperature_R101"])
    #   Biogas_Plant.Temperature_R102(manual_temp_R102 = biogas_input["manual_Temperature_R102"], Temp_R102 = biogas_input["Temperature_R102"])
    #   Biogas_Plant.V_101_DT()
    #   Biogas_Plant.V_102_DT()
    #   Biogas_Plant.V_107_DT()
    #   Biogas_Plant.R101_DT()
    #   Biogas_Plant.R102_DT()
    #   Biogas_Plant.Energy_Biogas()
    #   Biogas_Plant.StorageData()
      
    #   Biogas_learning_ini = MachineLearning_biogas_start.MachineLearningStart()
    #   Biogas_learning_ini.starting(t_train= biogas_input["t_pred"]*2, OperationMode = biogas_input["OperationMode"], Model = biogas_input["OperationModel"], A_R101 = biogas_input["A_R101"], 
    #                                B_R101 = biogas_input["B_R101"], C_R101=biogas_input["C_R101"], A_R102=biogas_input["A_R102"], B_R102=biogas_input["B_R102"], 
    #                                C_R102=biogas_input["C_R102"], VR1 = biogas_input["VR1"], VR2 = biogas_input["VR1"])
    #   Biogas_learning = Biogas_learning_ini.data
    #   Biogas_learning.Get_data_DT(DataBase = Biogas_Plant.DT_Data)
    #   Biogas_learning.DT_time_and_data()
    #   Biogas_learning.Optimization()
    #   Biogas_learning.StorageData()

    #   #sustrato
    #   biogas_output["n"] = Biogas_Plant.n
    #   biogas_output["a"] = Biogas_Plant.a
    #   biogas_output["b"] = Biogas_Plant.b
    #   biogas_output["c"] = Biogas_Plant.c
    #   biogas_output["d"] = Biogas_Plant.d

    #   #Tanque de premezcla
    #   biogas_output["Mix_Velocity_TK100"] = Biogas_Plant.RPM_TK100
    #   biogas_output["C_sv"] = Biogas_Plant.Csv
    #   biogas_output["SV"] = Biogas_Plant.SV
    #   biogas_output["C_st"] = Biogas_Plant.Cst
    #   biogas_output["ST"] = Biogas_Plant.ST

    #   #bomba P104
    #   biogas_output["Pump104Flow"] = Biogas_Plant.Q_P104

    #   #Reactor R101
    #   biogas_output["Mix_Velocity_R101"] = Biogas_Plant.RPM_R101
    #   biogas_output["C_sv_R101"] = Biogas_Plant.SV_R101_gL
    #   biogas_output["SV_R101"] = Biogas_Plant.SV_R101_p
    #   biogas_output["C_st_R101"] = Biogas_Plant.ST_R101_gl
    #   biogas_output["ST_R101"] = Biogas_Plant.ST_R101
    #   biogas_output["Organic_Charge_R101"] = Biogas_Plant.organic_charge_R101
    #   biogas_output["pH_R101"] = Biogas_Plant.pH_R101
    #   biogas_output["Temp_R101"] = Biogas_Plant.Temp_R101
    #   biogas_output["x_R101"] = Biogas_Plant.X_R101
      
      
    #   #modelo cinético
    #   if biogas_input["OperationModel"] == "Arrhenius":
    #     biogas_output["K_R101"] = Biogas_learning.K_R101
    #     biogas_output["Ea_R101"] = Biogas_learning.Ea_R101


    # else:  #Modo Gemelo Off
      
    #   if biogas_input["name"] not in biogas_instances:
    #     biogas_instances[biogas_input["name"]] = Biogas_Simulation_Start.BiogasSimulationStart()
      
    #   biogas_instance = biogas_instances[biogas_input["name"]]
      
    #   biogas_instance.starting(VR1 = biogas_input["VR1"], VR2 = biogas_input["VR2"], VG1 = biogas_input["VG1"], VG2 = biogas_input["VG2"], VG3 = biogas_input["VG3"],
    #                             tp = biogas_input["tp"], ST_R101 = biogas_input["ST_R101"], SV_R101 = biogas_input["SV_R101"], Cc_R101 = biogas_input["Cc_R101"],
    #                             Ch_R101 = biogas_input["Ch_R101"], Co_R101 = biogas_input["Co_R101"], Cn_R101 = biogas_input["Cn_R101"], Cs_R101 = biogas_input["Cs_R101"], 
    #                             rho_R101 = biogas_input["rho_R101"], ST_R102 = biogas_input["ST_R102"], SV_R102 = biogas_input["SV_R102"], Cc_R102 = biogas_input["Cc_R102"], 
    #                             Ch_R102 = biogas_input["Ch_R102"], Co_R102 = biogas_input["Co_R102"], Cn_R102 = biogas_input["Cn_R102"], Cs_R102 = biogas_input["Cs_R102"], 
    #                             rho_R102 = biogas_input["rho_R102"] , OperationMode = biogas_input["OperationMode"])
    #   Biogas_Plant = biogas_instance.data
    #   Biogas_Plant.Substrate_conditions(Cc = biogas_input["Cc"], Ch = biogas_input["Ch"], Co = biogas_input["Co"], Cn = biogas_input["Cn"], Cs = biogas_input["Cs"],
    #                                     rho = biogas_input["rho"], ST = biogas_input["ST"], SV = biogas_input["SV"])
      
    #   Biogas_Plant.Pump104(TRH=biogas_input["TRH"], FT_P104=biogas_input["FT_P104"], TTO_P104=biogas_input["TTO_P104"])
    #   Biogas_Plant.Pump101(FT_P101=biogas_input["FT_P101"], TTO_P101=biogas_input["TTO_P101"], Q_P101=biogas_input["Q_P101"])
    #   Biogas_Plant.Pump102(FT_P102=biogas_input["FT_P102"], TTO_P102=biogas_input["TTO_P102"], Q_P102=biogas_input["Q_P102"])
    #   Biogas_Plant.Mixing_TK100(FT_mixin_TK100 = biogas_input["FT_mixing_TK100"], TTO_mixing_TK100 = biogas_input["TTO_mixing_TK100"], RPM_TK100 = biogas_input["RPM_TK100"])
    #   Biogas_Plant.Mixing_R101(FT_mixin_R101 = biogas_input["FT_mixing_R101"], TTO_mixing_R101 = biogas_input["TTO_mixing_R101"], RPM_R101 = biogas_input["RPM_R101"])
    #   Biogas_Plant.Mixing_R102(FT_mixin_R102 = biogas_input["FT_mixing_R102"], TTO_mixing_R102=biogas_input["TTO_mixing_R102"], RPM_R102=biogas_input["RPM_R102"])
    #   Biogas_Plant.Data_simulation(Temperature_R101 = biogas_input["Temperature_R101"], Temperature_R102 = biogas_input["Temperature_R102"], pH_R101 = biogas_input["pH_R101"], pH_R102 = biogas_input["pH_R102"])
    #   Biogas_Plant.ReactorSimulation(Model = biogas_input["OperationModel"], A_R101 = biogas_input["A_R101"], B_R101 = biogas_input["B_R101"], C_R101 = biogas_input["C_R101"], 
    #                                  A_R102 = biogas_input["A_R102"], B_R102 = biogas_input["B_R102"], C_R102 = biogas_input["C_R102"])
    #   Biogas_Plant.V101()
    #   Biogas_Plant.V102()
    #   Biogas_Plant.Biogas_treatment(D1 = biogas_input["D1"], W1 = biogas_input["W1"], L1 = biogas_input["L1"], 
    #                                 D2 = biogas_input["D2"], W2 = biogas_input["W2"], L2 = biogas_input["L2"],
    #                                 D3 = biogas_input["D3"], W3 = biogas_input["W3"], L3 = biogas_input["L3"])
    #   Biogas_Plant.V107()

    #   #Resultados del análisis elemental
    #   biogas_output["n"] = Biogas_Plant.n
    #   biogas_output["a"] = Biogas_Plant.a
    #   biogas_output["b"] = Biogas_Plant.b
    #   biogas_output["c"] = Biogas_Plant.c
    #   biogas_output["d"] = Biogas_Plant.d

    #   #Condiciones de premezcla o predigestión
    #   biogas_output["Mix_Velocity_TK100"] = Biogas_Plant.RPM_TK100
    #   biogas_output["C_sv"] = Biogas_Plant.Csv
    #   biogas_output["SV"] = Biogas_Plant.SV
    #   biogas_output["C_st"] = Biogas_Plant.Cst
    #   biogas_output["ST"] = Biogas_Plant.ST

    #   #Salida de la bomba P_104
    #   biogas_output["Pump104Flow"] = Biogas_Plant.Q_P104

    #   #Reactor R101
    #   biogas_output["Mix_Velocity_R101"] = Biogas_Plant.RPM_R101
    #   biogas_output["C_sv_R101"] = Biogas_Plant.SV_R101_gL/100
    #   biogas_output["SV_R101"] = Biogas_Plant.SV_R101_p
    #   biogas_output["C_st_R101"] = Biogas_Plant.ST_R101/100*Biogas_Plant.rho
    #   biogas_output["ST_R101"] = Biogas_Plant.ST_R101
    #   biogas_output["Organic_Charge_R101"] = float(Biogas_Plant.Organic_charge_R101)  #Revisar con eusse
    #   biogas_output["pH_R101"] = Biogas_Plant.pH_R101
    #   biogas_output["Temp_R101"] = Biogas_Plant.Temp_R101
    #   biogas_output["x_R101"] = Biogas_Plant.x_R101 *100
      
    #   if biogas_input["OperationModel"] == "Arrhenius":  # revisar con eusse
    #     biogas_output["K_R101"] = Biogas_Plant.K_R101
    #     biogas_output["Ea_R101"] = Biogas_Plant.Ea_R101
    #   elif biogas_input["OperationModel"] == "ADM1": 
    #     biogas_output["K_R101"] = Biogas_Plant.K_R101
    #   elif biogas_input["OperationModel"] == "Gompertz":
    #     biogas_output["K_R101"] = Biogas_Plant.ym_R101
    #     biogas_output["Ea_R101"] = Biogas_Plant.U_R101
    #     biogas_output["Lambda_R101"] = Biogas_Plant.L_R101
      
    #   #Condiciones de modos de operación
    #   if biogas_input["OperationMode"] == "Modo3":
        
    #     #BombaP101
    #     biogas_output["Pump101Flow"] = Biogas_Plant.Q_P101

    #     #Reactor R102
    #     biogas_output["Mix_Velocity_R102"] = Biogas_Plant.RPM_R102
    #     biogas_output["pH_R102"] = Biogas_Plant.pH_R102
    #     biogas_output["Temp_R102"] = Biogas_Plant.Temp_R102
    #     biogas_output["C_sv_R102"] = Biogas_Plant.SV_R102_gL/100
    #     biogas_output["SV_R102"] = Biogas_Plant.SV_R102_p
    #     biogas_output["C_st_R102"] = Biogas_Plant.ST_R102/100 * Biogas_Plant.rho
    #     biogas_output["ST_R102"] = Biogas_Plant.ST_R102
    #     biogas_output["Organic_Charge_R102"] = float(Biogas_Plant.Organic_charge_R102)
    #     biogas_output["x_R102"] = Biogas_Plant.x_R102 *100

    #     if biogas_input["OperationModel"] == "Arrhenius":  # revisar con eusse
    #       biogas_output["K_R102"] = Biogas_Plant.K_R102
    #       biogas_output["Ea_R102"] = Biogas_Plant.Ea_R102
    #     elif biogas_input["OperationModel"] == "ADM1": 
    #       biogas_output["K_R102"] = Biogas_Plant.K_R102
    #     elif biogas_input["OperationModel"] == "Gompertz":
    #       biogas_output["K_R102"] = Biogas_Plant.ym_R102
    #       biogas_output["Ea_R102"] = Biogas_Plant.U_R102
    #       biogas_output["Lambda_R102"] = Biogas_Plant.L_R102
        
    #   elif biogas_input["OperationMode"] in ["Modo4", "Modo5"]:
    #     #BombaP101
    #     biogas_output["Pump101Flow"] = Biogas_Plant.Q_P101
    #     #BombaP102
    #     biogas_output["Pump102Flow"] = Biogas_Plant.Q_P102

    #     #Reactor R102
    #     biogas_output["Mix_Velocity_R102"] = Biogas_Plant.RPM_R102
    #     biogas_output["pH_R102"] = Biogas_Plant.pH_R102
    #     biogas_output["Temp_R102"] = Biogas_Plant.Temp_R102
    #     biogas_output["C_sv_R102"] = Biogas_Plant.SV_R102_gL/100
    #     biogas_output["SV_R102"] = Biogas_Plant.SV_R102_p
    #     biogas_output["C_st_R102"] = Biogas_Plant.ST_R102/100 * Biogas_Plant.rho
    #     biogas_output["ST_R102"] = Biogas_Plant.ST_R102
    #     biogas_output["Organic_Charge_R102"] = float(Biogas_Plant.Organic_charge_R102)
    #     biogas_output["x_R102"] = Biogas_Plant.x_R102 * 100

    #     if biogas_input["OperationModel"] == "Arrhenius":  # revisar con eusse
    #       biogas_output["K_R102"] = Biogas_Plant.K_R102
    #       biogas_output["Ea_R102"] = Biogas_Plant.Ea_R102
    #     elif biogas_input["OperationModel"] == "ADM1": 
    #       biogas_output["K_R102"] = Biogas_Plant.K_R102
    #     elif biogas_input["OperationModel"] == "Gompertz":
    #       biogas_output["K_R102"] = Biogas_Plant.ym_R102
    #       biogas_output["Ea_R102"] = Biogas_Plant.U_R102
    #       biogas_output["Lambda_R102"] = Biogas_Plant.L_R102
        
    #   #V101
    #   biogas_output["AcumBiogasVolumenV101"] = Biogas_Plant.Vnormal_bio_acum_V101
    #   biogas_output["StorageBiogasVolumeV101"] = Biogas_Plant.Vnormal_bio_V101
    #   biogas_output["AcumBiogasPressureV101"] = Biogas_Plant.Pacum_bio_V101
    #   biogas_output["StorageBiogasPressureV101"] = Biogas_Plant.Pstorage_bio_V101

    #   ## Metano
    #   biogas_output["StorageCH4_V101Volume"] = Biogas_Plant.Vnormal_CH4_V101
    #   biogas_output["StorageCH4_V101Concentration"] = Biogas_Plant.x_CH4_V101*100
    #   biogas_output["StorageCH4_V101moles"] = Biogas_Plant.mol_CH4_V101

    #   ## Dióxido de carbono
    #   biogas_output["StorageCO2_V101Volume"] = Biogas_Plant.Vnormal_CO2_V101
    #   biogas_output["StorageCO2_V101Concentration"] = Biogas_Plant.x_CO2_V101*100
    #   biogas_output["StorageCO2_V101moles"] = Biogas_Plant.mol_CO2_V101

    #   ## Sulfuro de de hidrógeno
    #   biogas_output["StorageH2S_V101Volume"] = Biogas_Plant.Vnormal_H2S_V101
    #   biogas_output["StorageH2S_V101Concentration"] = Biogas_Plant.x_H2S_V101*1000000
    #   biogas_output["StorageH2S_V101moles"] = Biogas_Plant.mol_H2S_V101

    #   ## Oxígeno
    #   biogas_output["StorageO2_V101Volume"] = Biogas_Plant.Vnormal_O2_V101
    #   biogas_output["StorageO2_V101Concentration"] = Biogas_Plant.x_O2_V101*100
    #   biogas_output["StorageO2_V101moles"] = Biogas_Plant.mol_O2_V101

    #   ## Amonio
    #   biogas_output["StorageNH3_V101Volume"] = Biogas_Plant.Vnormal_NH3_V101
    #   biogas_output["StorageNH3_V101Concentration"] = Biogas_Plant.x_NH3_V101*1000000
    #   biogas_output["StorageNH3_V101moles"] = Biogas_Plant.mol_NH3_V101

    #   ## Hidrógeno
    #   biogas_output["StorageH2_V101Volume"] = Biogas_Plant.Vnormal_H2_V101
    #   biogas_output["StorageH2_V101Concentration"] = Biogas_Plant.x_H2_V101*1000000
    #   biogas_output["StorageH2_V101moles"] = Biogas_Plant.mol_H2_V101

    #   #Agua
    #   biogas_output["moles_humidity_V101"] = Biogas_Plant.mol_H2O_V101
    #   biogas_output["Relative_humidity_V101"] = Biogas_Plant.RH_V101

    #   #Energía
    #   biogas_output["StorageEnergy_V101"] = Biogas_Plant.Energy_V101/3600

    #   #V102
    #   biogas_output["AcumBiogasVolumenV102"] = Biogas_Plant.Vnormal_bio_acum_V102
    #   biogas_output["StorageBiogasVolumeV102"] = Biogas_Plant.Vnormal_bio_V102
    #   biogas_output["AcumBiogasPressureV102"] = Biogas_Plant.Pacum_bio_V102
    #   biogas_output["StorageBiogasPressureV102"] = Biogas_Plant.Pstorage_bio_V102

    #   ## Metano
    #   biogas_output["StorageCH4_V102Volume"] = Biogas_Plant.Vnormal_CH4_V102
    #   biogas_output["StorageCH4_V102Concentration"] = Biogas_Plant.x_CH4_V102*100
    #   biogas_output["StorageCH4_V102moles"] = Biogas_Plant.mol_CH4_V102

    #   ## Dióxido de carbono
    #   biogas_output["StorageCO2_V102Volume"] = Biogas_Plant.Vnormal_CO2_V102
    #   biogas_output["StorageCO2_V102Concentration"] = Biogas_Plant.x_CO2_V102*100
    #   biogas_output["StorageCO2_V102moles"] = Biogas_Plant.mol_CO2_V102

    #   ## Sulfuro de de hidrógeno
    #   biogas_output["StorageH2S_V102Volume"] = Biogas_Plant.Vnormal_H2S_V102
    #   biogas_output["StorageH2S_V102Concentration"] = Biogas_Plant.x_H2S_V102*1000000
    #   biogas_output["StorageH2S_V102moles"] = Biogas_Plant.mol_H2S_V102

    #   ## Oxígeno
    #   biogas_output["StorageO2_V102Volume"] = Biogas_Plant.Vnormal_O2_V102
    #   biogas_output["StorageO2_V102Concentration"] = Biogas_Plant.x_O2_V102*100
    #   biogas_output["StorageO2_V102moles"] = Biogas_Plant.mol_O2_V102

    #   ## Amonio
    #   biogas_output["StorageNH3_V102Volume"] = Biogas_Plant.Vnormal_NH3_V102
    #   biogas_output["StorageNH3_V102Concentration"] = Biogas_Plant.x_NH3_V102*1000000
    #   biogas_output["StorageNH3_V102moles"] = Biogas_Plant.mol_NH3_V102

    #   ## Hidrógeno
    #   biogas_output["StorageH2_V102Volume"] = Biogas_Plant.Vnormal_H2_V102
    #   biogas_output["StorageH2_V102Concentration"] = Biogas_Plant.x_H2_V102*1000000
    #   biogas_output["StorageH2_V102moles"] = Biogas_Plant.mol_H2_V102

    #   #Agua
    #   biogas_output["moles_humidity_V102"] = Biogas_Plant.mol_H2O_V102
    #   biogas_output["Relative_humidity_V102"] = Biogas_Plant.RH_V102

    #   #Energía
    #   biogas_output["StorageEnergy_V102"] = Biogas_Plant.Energy_V102/3600

    #   #Biogas Treatment
    #   biogas_output["ads_NH3_bt"] = Biogas_Plant.mol_NH3_ads
    #   biogas_output["ads_H2S_bt"] = Biogas_Plant.mol_H2S_ads
    #   biogas_output["ads_H2O_bt"] = Biogas_Plant.mol_H2O_ads
    #   biogas_output["x_bt"] = Biogas_Plant.x_tower*100

    #   #V107
    #   biogas_output["AcumBiogasVolumenV107"] = Biogas_Plant.Vnormal_bio_acum_V107
    #   biogas_output["StorageBiogasVolumeV107"] = Biogas_Plant.Vnormal_bio_V107
    #   biogas_output["AcumBiogasPressureV107"] = Biogas_Plant.Pacum_bio_V107
    #   biogas_output["StorageBiogasPressureV107"] = Biogas_Plant.Pstorage_bio_V107

    #   ## Metano
    #   biogas_output["StorageCH4_V107Volume"] = Biogas_Plant.Vnormal_CH4_V107
    #   biogas_output["StorageCH4_V107Concentration"] = Biogas_Plant.x_CH4_V107*100
    #   biogas_output["StorageCH4_V107moles"] = Biogas_Plant.mol_CH4_V107

    #   ## Dióxido de carbono
    #   biogas_output["StorageCO2_V107Volume"] = Biogas_Plant.Vnormal_CO2_V107
    #   biogas_output["StorageCO2_V107Concentration"] = Biogas_Plant.x_CO2_V107*100
    #   biogas_output["StorageCO2_V107moles"] = Biogas_Plant.mol_CO2_V107

    #   ## Sulfuro de de hidrógeno
    #   biogas_output["StorageH2S_V107Volume"] = Biogas_Plant.Vnormal_H2S_V107
    #   biogas_output["StorageH2S_V107Concentration"] = Biogas_Plant.x_H2S_V107*1000000
    #   biogas_output["StorageH2S_V107moles"] = Biogas_Plant.mol_H2S_V107

    #   ## Oxígeno
    #   biogas_output["StorageO2_V107Volume"] = Biogas_Plant.Vnormal_O2_V107
    #   biogas_output["StorageO2_V107Concentration"] = Biogas_Plant.x_O2_V107*100
    #   biogas_output["StorageO2_V107moles"] = Biogas_Plant.mol_O2_V107

    #   ## Amonio
    #   biogas_output["StorageNH3_V107Volume"] = Biogas_Plant.Vnormal_NH3_V107
    #   biogas_output["StorageNH3_V107Concentration"] = Biogas_Plant.x_NH3_V107*1000000
    #   biogas_output["StorageNH3_V107moles"] = Biogas_Plant.mol_NH3_V107

    #   ## Hidrógeno
    #   biogas_output["StorageH2_V107Volume"] = Biogas_Plant.Vnormal_H2_V107
    #   biogas_output["StorageH2_V107Concentration"] = Biogas_Plant.x_H2_V107*1000000
    #   biogas_output["StorageH2_V107moles"] = Biogas_Plant.mol_H2_V107

    #   #Agua
    #   biogas_output["moles_humidity_V107"] = Biogas_Plant.mol_H2O_V107
    #   biogas_output["Relative_humidity_V107"] = Biogas_Plant.RH_V107

    #   #Energía
    #   biogas_output["StorageEnergy_V107"] = Biogas_Plant.Energy_V107/3600

    
      

    return {"model": biogas_output}, 200