from flask import request
from flask_restful import Resource
from utils import bmp_simulation_start


class BMP(Resource):
  def post(self):
    data = request.get_json()
    bmp_output = {}

    # SIDE A -------------
    iteration = data["iteration"]

    if iteration == 1:
      bmp_simulation_start.BMPSimulationStart.reset_instance()

    #lado A condiciones condiciones generales
    offline = data["stateSelectionSideA"]
    SideA_measurementMethod = data["measurementMethodSideA"]

    #lado condiciones de corrida
    SideA_Vrxn = data["rxnVolumeSideA"]["value"]
    SideA_vf = data["freeVolumeSideA"]["value"]
    SideA_tp = data["timeStepSideA"]["value"]
    SideA_MixRule = data["substrate1CompositionSideA"]["variableString"]
    SideA_substrateNumber = data["amountOfSubstratesSideA"]["value"]
    SideA_Water = data["waterCompositionSideA"]["value"]
    #sustrato 1
    SideA_Fraction1 = data["substrate1CompositionSideA"]["value"]
    SideA_TS1 = data ["totalSolidsSubstrate1SideA"]["value"]
    SideA_VS1 = data["volatileSolidsSubstrate1SIdeA"]["value"]
    SideA_rho1 = data["densitySubstrate1SideA"]["value"]
    SideA_Cc1 = data["carbonContentSubstrate1SideA"]["value"]
    SideA_Ch1 = data["hydrogenContentSubstrate1SideA"]["value"]
    SideA_Co1 = data["oxygenContentSubstrate1SideA"]["value"]
    SideA_Cn1 = data["nitrogenContentSubstrate1SideA"]["value"]
    SideA_Cs1 = data["sulfurContentSubstrate1SideA"]["value"]
    #sustrato 2
    SideA_Fraction2 = data["substrate2CompositionSideA"]["value"]
    SideA_TS2 = data ["totalSolidsSubstrate2SideA"]["value"]
    SideA_VS2 = data["volatileSolidsSubstrate2SideA"]["value"]
    SideA_rho2 = data["densitySubstrate2SideA"]["value"]
    SideA_Cc2 = data["carbonContentSubstrate2SideA"]["value"]
    SideA_Ch2 = data["hydrogenContentSubstrate2SideA"]["value"]
    SideA_Co2 = data["oxygenContentSubstrate2SideA"]["value"]
    SideA_Cn2 = data["nitrogenContentSubstrate2SideA"]["value"]
    SideA_Cs2 = data["sulfurContentSubstrate2SideA"]["value"]
    #sustrato 3
    SideA_Fraction3 = data["substrate3CompositionSideA"]["value"]
    SideA_TS3 = data ["totalSolidsSubstrate3SideA"]["value"]
    SideA_VS3 = data["volatileSolidsSubstrate3SideA"]["value"]
    SideA_rho3 = data["densitySubstrate3SideA"]["value"]
    SideA_Cc3 = data["carbonContentSubstrate3SideA"]["value"]
    SideA_Ch3 = data["hydrogenContentSubstrate3SideA"]["value"]
    SideA_Co3 = data["oxygenContentSubstrate3SideA"]["value"]
    SideA_Cn3 = data["nitrogenContentSubstrate3SideA"]["value"]
    SideA_Cs3 = data["sulfurContentSubstrate3SideA"]["value"]
    #sustrato 4
    SideA_Fraction4 = data["substrate4CompositionSideA"]["value"]
    SideA_TS4 = data ["totalSolidsSubstrate4SideA"]["value"]
    SideA_VS4 = data["volatileSolidsSubstrate4SIdeA"]["value"]
    SideA_rho4 = data["densitySubstrate4SideA"]["value"]
    SideA_Cc4 = data["carbonContentSubstrate4SideA"]["value"]
    SideA_Ch4 = data["hydrogenContentSubstrate4SideA"]["value"]
    SideA_Co4 = data["oxygenContentSubstrate4SideA"]["value"]
    SideA_Cn4 = data["nitrogenContentSubstrate4SideA"]["value"]
    SideA_Cs4 = data["sulfurContentSubstrate4SideA"]["value"]
    #mixControl
    SideA_ManualMix = data["mixManualSideA"]
    SideA_MixVelocity = data["mixVelocitySideA"]["value"]
    SideA_MixTime = data["mixTimeSideA"]["value"]
    SideA_DailyMixing = data["mixDailySideA"]["value"]
    #Control Feed
    SideA_ManualFeed = data["feefManualSideA"]
    SideA_FeedMode = data["dosificationTypeSideA"]
    SideA_FeedVolume = data["dosificationVolumeSideA"]["value"]
    SideA_FeedTime = data["dailyInyectionsByTimeSideA"]["value"]
    SideA_Injections = data["dailyInyectionsSideA"]["value"]
    #Reactor
    SideA_Model = data["modelSelectionSideA"]
    SideA_pHauto = data["pHSideA"]["disabled"]
    SideA_pH = data["pHSideA"]["value"]
    SideA_Temperatura = data["TemperatureSideA"]["value"]
    SideA_K1 = data["kineticKSideA"]["value"]
    SideA_K2 = data["kineticEaSideA"]["value"]
    SideA_K3 = data["kineticLambdaSideA"]["value"]

    # Modo Offline
    if offline == True:

      #---- Reactor 1
      R101_ini = bmp_simulation_start.BMPSimulationStart()
      R101_ini.starting(Vrxn = SideA_Vrxn, Vf=SideA_vf, tp=SideA_tp)
      R101 = R101_ini.data
      R101.MixtureCalculation(substratesNumber = SideA_substrateNumber, MixtureRule = SideA_MixRule, WaterFraction = SideA_Water, WaterVolume = SideA_Water, WaterWeight = SideA_Water, 
                              Fraction1 = SideA_Fraction1, Volume1 = SideA_Fraction1, Weight1 = SideA_Fraction1, TS1 = SideA_TS1, VS1 = SideA_VS1, rho1 = SideA_rho1, Cc1 = SideA_Cc1, Hc1 = SideA_Ch1, Oc1 = SideA_Co1, Nc1 = SideA_Cn1, Sc1 = SideA_Cs1,
                              Fraction2 = SideA_Fraction2, Volume2 = SideA_Fraction2, Weight2 = SideA_Fraction2, TS2 = SideA_TS2, VS2 = SideA_VS2, rho2 = SideA_rho2, Cc2 = SideA_Cc2, Hc2 = SideA_Ch2, Oc2 = SideA_Co2, Nc2 = SideA_Cn2, Sc2 = SideA_Cs2,
                              Fraction3 = SideA_Fraction3, Volume3 = SideA_Fraction3, Weight3 = SideA_Fraction3, TS3 = SideA_TS3, VS3 = SideA_VS3, rho3 = SideA_rho3, Cc3 = SideA_Cc3, Hc3 = SideA_Ch3, Oc3 = SideA_Co3, Nc3 = SideA_Cn3, Sc3 = SideA_Cs3,
                              Fraction4 = SideA_Fraction4, Volume4 = SideA_Fraction4, Weight4 = SideA_Fraction4, TS4 = SideA_TS4, VS4 = SideA_VS4, rho4 = SideA_rho4, Cc4 = SideA_Cc4, Hc4 = SideA_Ch4, Oc4 = SideA_Co4, Nc4 = SideA_Cn4, Sc4 = SideA_Cs4)
      
      #Agitación
      R101.MixControl(MixVelocity = SideA_MixVelocity, MixTime = SideA_MixTime, DailyMixing = SideA_DailyMixing)
      #---- Salidas Agitación
      bmp_output["mixVelocityR101"] = R101.MixVelocity

      #Alimentación
      R101.SubstrateFeed(Mode = SideA_FeedMode, Volume = SideA_FeedVolume, Time = SideA_FeedTime, Inyections = SideA_Injections, Q=1)
      #---- Salidas alimentación
      bmp_output["caudalSideA"] = R101.Qr
      bmp_output["volumeSubstrateSideA"] = R101.TotalVolFeed

      #Reactor
      R101.Reactor(model = SideA_Model, pH = SideA_pH, T = SideA_Temperatura, K1 = SideA_K1, K2 = SideA_K2, K3 = SideA_K3)
      #---- Salidas reactor R101
      bmp_output["SVR101"] = R101.SV 
      bmp_output["OCR101"] = R101.OC
      bmp_output["STR101"] = R101.ST
      bmp_output["XR101"] = R101.x
      bmp_output["KR101"] = R101.K1
      bmp_output["EaR101"] = R101.K2
      bmp_output["lambdaR101"] = R101.K3
      bmp_output["TempR101"] = R101.T   
      bmp_output["pHR101"] = R101.pH
      #---- Productos de reacción en moles [mol]
      bmp_output["methanemolR101"] = R101.mol_CH4
      bmp_output["carbondioxidemolR101"] = R101.mol_CO2
      bmp_output["oxygenmolR101"] = R101.mol_O2
      bmp_output["hydrogensulfurmolR101"] = R101.mol_H2S
      bmp_output["hydrogenmolR101"] = R101.mol_H2
      #---- Productos de reacción en vol normal [mL]
      R101.CompoundsUnits()
      bmp_output["methanevolR101"] = R101.Vnormal_CH4
      bmp_output["carbondioxidevolR101"] = R101.Vnormal_CO2
      bmp_output["oxygenvolR101"] = R101.Vnormal_O2
      bmp_output["hydrogensulfurvolR101"] = R101.Vnormal_H2S
      bmp_output["hydrogenvolR101"] = R101.Vnormal_H2
      #---- Productos de reacción en concentracion [%]
      bmp_output["methaneconcentrationR101"] = R101.x_CH4
      bmp_output["carbondioxideconcentrationR101"] = R101.x_CO2
      bmp_output["oxygenconcentrationR101"] = R101.x_O2
      bmp_output["hydrogensulfurconcentrationR101"] = R101.x_H2S
      bmp_output["hydrogenconcentrationR101"] = R101.x_H2
      #---- Biogás Volumen acumulado [mL]
      bmp_output["accumbiogasR101"] = R101.Vbiogas
      #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
      R101.PressurebyBiogas()
      if SideA_measurementMethod == "Pressure":
        bmp_output["accumbiogaspressureR101"] = R101.P_acum
        bmp_output["storagebiogaspressureR101"] = R101.P_storage
        bmp_output["storagebiogasR101"] = R101.V_storage
      #Volumen desplazado
      else:
        R101.poolSensor()
        bmp_output["poolLevelR101"] = R101.hpool
        bmp_output["poolTempR101"] = R101.Tpool
        bmp_output["poolPressureR101"] = R101.Ppool
      #Biogas energy
      R101.biogasEnergy()
      bmp_output["LHVR101"] = R101.LHV
      bmp_output["EnergyR101"] = R101.TotalBiogasEnergy
      bmp_output["PBMR101"] = R101.PBM
      
      # ----- Reactor 2
      R102_ini = bmp_simulation_start.BMPSimulationStart()
      R102_ini.starting(Vrxn = SideA_Vrxn, Vf=SideA_vf, tp=SideA_tp)
      R102 = R102_ini.data
      R102.MixtureCalculation(substratesNumber = SideA_substrateNumber, MixtureRule = SideA_MixRule, WaterFraction = SideA_Water, WaterVolume = SideA_Water, WaterWeight = SideA_Water, 
                              Fraction1 = SideA_Fraction1, Volume1 = SideA_Fraction1, Weight1 = SideA_Fraction1, TS1 = SideA_TS1, VS1 = SideA_VS1, rho1 = SideA_rho1, Cc1 = SideA_Cc1, Hc1 = SideA_Ch1, Oc1 = SideA_Co1, Nc1 = SideA_Cn1, Sc1 = SideA_Cs1,
                              Fraction2 = SideA_Fraction2, Volume2 = SideA_Fraction2, Weight2 = SideA_Fraction2, TS2 = SideA_TS2, VS2 = SideA_VS2, rho2 = SideA_rho2, Cc2 = SideA_Cc2, Hc2 = SideA_Ch2, Oc2 = SideA_Co2, Nc2 = SideA_Cn2, Sc2 = SideA_Cs2,
                              Fraction3 = SideA_Fraction3, Volume3 = SideA_Fraction3, Weight3 = SideA_Fraction3, TS3 = SideA_TS3, VS3 = SideA_VS3, rho3 = SideA_rho3, Cc3 = SideA_Cc3, Hc3 = SideA_Ch3, Oc3 = SideA_Co3, Nc3 = SideA_Cn3, Sc3 = SideA_Cs3,
                              Fraction4 = SideA_Fraction4, Volume4 = SideA_Fraction4, Weight4 = SideA_Fraction4, TS4 = SideA_TS4, VS4 = SideA_VS4, rho4 = SideA_rho4, Cc4 = SideA_Cc4, Hc4 = SideA_Ch4, Oc4 = SideA_Co4, Nc4 = SideA_Cn4, Sc4 = SideA_Cs4)
      
      #Agitación
      R102.MixControl(MixVelocity = SideA_MixVelocity, MixTime = SideA_MixTime, DailyMixing = SideA_DailyMixing)
      #---- Salidas Agitación
      bmp_output["mixVelocityR102"] = R102.MixVelocity

      #Alimentación
      R102.SubstrateFeed(Mode = SideA_FeedMode, Volume = SideA_FeedVolume, Time = SideA_FeedTime, Inyections = SideA_Injections, Q=1)
      #---- Salidas alimentación
      bmp_output["caudalSideA"] = R102.Qr
      bmp_output["volumeSubstrateSideA"] = R102.TotalVolFeed

      #Reactor
      R102.Reactor(model = SideA_Model, pH = SideA_pH, T = SideA_Temperatura, K1 = SideA_K1, K2 = SideA_K2, K3 = SideA_K3)
      #---- Salidas reactor R102
      bmp_output["SVR102"] = R102.SV 
      bmp_output["OCR102"] = R102.OC
      bmp_output["STR102"] = R102.ST
      bmp_output["XR102"] = R102.x
      bmp_output["KR102"] = R102.K1
      bmp_output["EaR102"] = R102.K2
      bmp_output["lambdaR102"] = R102.K3
      bmp_output["TempR102"] = R102.T   
      bmp_output["pHR102"] = R102.pH
      #---- Productos de reacción en moles [mol]
      bmp_output["methanemolR102"] = R102.mol_CH4
      bmp_output["carbondioxidemolR102"] = R102.mol_CO2
      bmp_output["oxygenmolR102"] = R102.mol_O2
      bmp_output["hydrogensulfurmolR102"] = R102.mol_H2S
      bmp_output["hydrogenmolR102"] = R102.mol_H2
      #---- Productos de reacción en vol normal [mL]
      R102.CompoundsUnits()
      bmp_output["methanevolR102"] = R102.Vnormal_CH4
      bmp_output["carbondioxidevolR102"] = R102.Vnormal_CO2
      bmp_output["oxygenvolR102"] = R102.Vnormal_O2
      bmp_output["hydrogensulfurvolR102"] = R102.Vnormal_H2S
      bmp_output["hydrogenvolR102"] = R102.Vnormal_H2
      #---- Productos de reacción en concentracion [%]
      bmp_output["methaneconcentrationR102"] = R102.x_CH4
      bmp_output["carbondioxideconcentrationR102"] = R102.x_CO2
      bmp_output["oxygenconcentrationR102"] = R102.x_O2
      bmp_output["hydrogensulfurconcentrationR102"] = R102.x_H2S
      bmp_output["hydrogenconcentrationR102"] = R102.x_H2
      #---- Biogás Volumen acumulado [mL]
      bmp_output["accumbiogasR102"] = R102.Vbiogas
      #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
      R102.PressurebyBiogas()
      if SideA_measurementMethod == "Pressure":
        bmp_output["accumbiogaspressureR102"] = R102.P_acum
        bmp_output["storagebiogaspressureR102"] = R102.P_storage
        bmp_output["storagebiogasR102"] = R102.V_storage
      #Volumen desplazado
      else:
        R102.poolSensor()
        bmp_output["poolLevelR102"] = R102.hpool
        bmp_output["poolTempR102"] = R102.Tpool
        bmp_output["poolPressureR102"] = R102.Ppool
      #Biogas energy
      R102.biogasEnergy()
      bmp_output["LHVR102"] = R102.LHV
      bmp_output["EnergyR102"] = R102.TotalBiogasEnergy
      bmp_output["PBMR102"] = R102.PBM
      
      # ----- Reactor 3
      R103_ini = bmp_simulation_start.BMPSimulationStart()
      R103_ini.starting(Vrxn = SideA_Vrxn, Vf=SideA_vf, tp=SideA_tp)
      R103 = R103_ini.data
      R103.MixtureCalculation(substratesNumber = SideA_substrateNumber, MixtureRule = SideA_MixRule, WaterFraction = SideA_Water, WaterVolume = SideA_Water, WaterWeight = SideA_Water, 
                              Fraction1 = SideA_Fraction1, Volume1 = SideA_Fraction1, Weight1 = SideA_Fraction1, TS1 = SideA_TS1, VS1 = SideA_VS1, rho1 = SideA_rho1, Cc1 = SideA_Cc1, Hc1 = SideA_Ch1, Oc1 = SideA_Co1, Nc1 = SideA_Cn1, Sc1 = SideA_Cs1,
                              Fraction2 = SideA_Fraction2, Volume2 = SideA_Fraction2, Weight2 = SideA_Fraction2, TS2 = SideA_TS2, VS2 = SideA_VS2, rho2 = SideA_rho2, Cc2 = SideA_Cc2, Hc2 = SideA_Ch2, Oc2 = SideA_Co2, Nc2 = SideA_Cn2, Sc2 = SideA_Cs2,
                              Fraction3 = SideA_Fraction3, Volume3 = SideA_Fraction3, Weight3 = SideA_Fraction3, TS3 = SideA_TS3, VS3 = SideA_VS3, rho3 = SideA_rho3, Cc3 = SideA_Cc3, Hc3 = SideA_Ch3, Oc3 = SideA_Co3, Nc3 = SideA_Cn3, Sc3 = SideA_Cs3,
                              Fraction4 = SideA_Fraction4, Volume4 = SideA_Fraction4, Weight4 = SideA_Fraction4, TS4 = SideA_TS4, VS4 = SideA_VS4, rho4 = SideA_rho4, Cc4 = SideA_Cc4, Hc4 = SideA_Ch4, Oc4 = SideA_Co4, Nc4 = SideA_Cn4, Sc4 = SideA_Cs4)
      
      #Agitación
      R103.MixControl(MixVelocity = SideA_MixVelocity, MixTime = SideA_MixTime, DailyMixing = SideA_DailyMixing)
      #---- Salidas Agitación
      bmp_output["mixVelocityR103"] = R103.MixVelocity

      #Alimentación
      R103.SubstrateFeed(Mode = SideA_FeedMode, Volume = SideA_FeedVolume, Time = SideA_FeedTime, Inyections = SideA_Injections, Q=1)
      #---- Salidas alimentación
      bmp_output["caudalSideA"] = R103.Qr
      bmp_output["volumeSubstrateSideA"] = R103.TotalVolFeed

      #Reactor
      R103.Reactor(model = SideA_Model, pH = SideA_pH, T = SideA_Temperatura, K1 = SideA_K1, K2 = SideA_K2, K3 = SideA_K3)
      #---- Salidas reactor R103
      bmp_output["SVR103"] = R103.SV 
      bmp_output["OCR103"] = R103.OC
      bmp_output["STR103"] = R103.ST
      bmp_output["XR103"] = R103.x
      bmp_output["KR103"] = R103.K1
      bmp_output["EaR103"] = R103.K2
      bmp_output["lambdaR103"] = R103.K3
      bmp_output["TempR103"] = R103.T   
      bmp_output["pHR103"] = R103.pH
      #---- Productos de reacción en moles [mol]
      bmp_output["methanemolR103"] = R103.mol_CH4
      bmp_output["carbondioxidemolR103"] = R103.mol_CO2
      bmp_output["oxygenmolR103"] = R103.mol_O2
      bmp_output["hydrogensulfurmolR103"] = R103.mol_H2S
      bmp_output["hydrogenmolR103"] = R103.mol_H2
      #---- Productos de reacción en vol normal [mL]
      R103.CompoundsUnits()
      bmp_output["methanevolR103"] = R103.Vnormal_CH4
      bmp_output["carbondioxidevolR103"] = R103.Vnormal_CO2
      bmp_output["oxygenvolR103"] = R103.Vnormal_O2
      bmp_output["hydrogensulfurvolR103"] = R103.Vnormal_H2S
      bmp_output["hydrogenvolR103"] = R103.Vnormal_H2
      #---- Productos de reacción en concentracion [%]
      bmp_output["methaneconcentrationR103"] = R103.x_CH4
      bmp_output["carbondioxideconcentrationR103"] = R103.x_CO2
      bmp_output["oxygenconcentrationR103"] = R103.x_O2
      bmp_output["hydrogensulfurconcentrationR103"] = R103.x_H2S
      bmp_output["hydrogenconcentrationR103"] = R103.x_H2
      #---- Biogás Volumen acumulado [mL]
      bmp_output["accumbiogasR103"] = R103.Vbiogas
      #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
      R103.PressurebyBiogas()
      if SideA_measurementMethod == "Pressure":
        bmp_output["accumbiogaspressureR103"] = R103.P_acum
        bmp_output["storagebiogaspressureR103"] = R103.P_storage
        bmp_output["storagebiogasR103"] = R103.V_storage
      #Volumen desplazado
      else:
        R103.poolSensor()
        bmp_output["poolLevelR103"] = R103.hpool
        bmp_output["poolTempR103"] = R103.Tpool
        bmp_output["poolPressureR103"] = R103.Ppool
      #Biogas energy
      R103.biogasEnergy()
      bmp_output["LHVR103"] = R103.LHV
      bmp_output["EnergyR103"] = R103.TotalBiogasEnergy
      bmp_output["PBMR103"] = R103.PBM
      
      
      
      
      

    print(bmp_output)
    return {"model": bmp_output}, 200