from flask import request
from flask_restful import Resource
from simulation_models.BMPModel import BMPOffline

bmp_instances = {}

class BMP(Resource):
  def post(self):
    data = request.get_json()
    bmp_output = {}
    
    iteration = data["iteration"]
    Side = data["plantOperation"]
    user_id101 = data["name"] + "101"
    user_id102 = data["name"] + "102"
    user_id103 = data["name"] + "103"
    user_id104 = data["name"] + "104"
    user_id105 = data["name"] + "105"
    user_id106 = data["name"] + "106"
    user_id107 = data["name"] + "107"
    user_id108 = data["name"] + "108"
    user_id109 = data["name"] + "109"
    user_id110 = data["name"] + "110"
    
    users_instances = [user_id101, user_id102, user_id103, user_id104, user_id105,
                            user_id106, user_id107, user_id108, user_id109, user_id110]
    
    if iteration == 1:
      if users_instances is bmp_instances:
        del bmp_instances[user_id101]
        del bmp_instances[user_id102]
        del bmp_instances[user_id103]
        del bmp_instances[user_id104]
        del bmp_instances[user_id105]
        del bmp_instances[user_id106]
        del bmp_instances[user_id107]
        del bmp_instances[user_id108]
        del bmp_instances[user_id109]
        del bmp_instances[user_id110]
          
    # SIDE A -------------
    #lado A condiciones condiciones generales
    offlineA = data["stateSelectionSideA"]
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
    if offlineA == True:
      if Side == "SideA":
        #---- Reactor 1
        if user_id101 not in bmp_instances:
          bmp_instances[user_id101] = BMPOffline.BMPModelOffline(Vrxn = SideA_Vrxn, Vf=SideA_vf, tp=SideA_tp)
        R101 = bmp_instances[user_id101]
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
        if user_id102 not in bmp_instances:
          bmp_instances[user_id102] = BMPOffline.BMPModelOffline(Vrxn = SideA_Vrxn, Vf=SideA_vf, tp=SideA_tp)
        R102 = bmp_instances[user_id102]
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
        if user_id103 not in bmp_instances:
          bmp_instances[user_id103] = BMPOffline.BMPModelOffline(Vrxn = SideA_Vrxn, Vf=SideA_vf, tp=SideA_tp)
        R103 = bmp_instances[user_id103]
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
        
        # ----- Reactor 4
        if user_id104 not in bmp_instances:
          bmp_instances[user_id104] = BMPOffline.BMPModelOffline(Vrxn = SideA_Vrxn, Vf=SideA_vf, tp=SideA_tp)
        R104 = bmp_instances[user_id104]
        R104.MixtureCalculation(substratesNumber = SideA_substrateNumber, MixtureRule = SideA_MixRule, WaterFraction = SideA_Water, WaterVolume = SideA_Water, WaterWeight = SideA_Water, 
                                Fraction1 = SideA_Fraction1, Volume1 = SideA_Fraction1, Weight1 = SideA_Fraction1, TS1 = SideA_TS1, VS1 = SideA_VS1, rho1 = SideA_rho1, Cc1 = SideA_Cc1, Hc1 = SideA_Ch1, Oc1 = SideA_Co1, Nc1 = SideA_Cn1, Sc1 = SideA_Cs1,
                                Fraction2 = SideA_Fraction2, Volume2 = SideA_Fraction2, Weight2 = SideA_Fraction2, TS2 = SideA_TS2, VS2 = SideA_VS2, rho2 = SideA_rho2, Cc2 = SideA_Cc2, Hc2 = SideA_Ch2, Oc2 = SideA_Co2, Nc2 = SideA_Cn2, Sc2 = SideA_Cs2,
                                Fraction3 = SideA_Fraction3, Volume3 = SideA_Fraction3, Weight3 = SideA_Fraction3, TS3 = SideA_TS3, VS3 = SideA_VS3, rho3 = SideA_rho3, Cc3 = SideA_Cc3, Hc3 = SideA_Ch3, Oc3 = SideA_Co3, Nc3 = SideA_Cn3, Sc3 = SideA_Cs3,
                                Fraction4 = SideA_Fraction4, Volume4 = SideA_Fraction4, Weight4 = SideA_Fraction4, TS4 = SideA_TS4, VS4 = SideA_VS4, rho4 = SideA_rho4, Cc4 = SideA_Cc4, Hc4 = SideA_Ch4, Oc4 = SideA_Co4, Nc4 = SideA_Cn4, Sc4 = SideA_Cs4)
        
        #Agitación
        R104.MixControl(MixVelocity = SideA_MixVelocity, MixTime = SideA_MixTime, DailyMixing = SideA_DailyMixing)
        #---- Salidas Agitación
        bmp_output["mixVelocityR104"] = R104.MixVelocity

        #Alimentación
        R104.SubstrateFeed(Mode = SideA_FeedMode, Volume = SideA_FeedVolume, Time = SideA_FeedTime, Inyections = SideA_Injections, Q=1)
        #---- Salidas alimentación
        bmp_output["caudalSideA"] = R104.Qr
        bmp_output["volumeSubstrateSideA"] = R104.TotalVolFeed

        #Reactor
        R104.Reactor(model = SideA_Model, pH = SideA_pH, T = SideA_Temperatura, K1 = SideA_K1, K2 = SideA_K2, K3 = SideA_K3)
        #---- Salidas reactor R104
        bmp_output["SVR104"] = R104.SV 
        bmp_output["OCR104"] = R104.OC
        bmp_output["STR104"] = R104.ST
        bmp_output["XR104"] = R104.x
        bmp_output["KR104"] = R104.K1
        bmp_output["EaR104"] = R104.K2
        bmp_output["lambdaR104"] = R104.K3
        bmp_output["TempR104"] = R104.T   
        bmp_output["pHR104"] = R104.pH
        #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR104"] = R104.mol_CH4
        bmp_output["carbondioxidemolR104"] = R104.mol_CO2
        bmp_output["oxygenmolR104"] = R104.mol_O2
        bmp_output["hydrogensulfurmolR104"] = R104.mol_H2S
        bmp_output["hydrogenmolR104"] = R104.mol_H2
        #---- Productos de reacción en vol normal [mL]
        R104.CompoundsUnits()
        bmp_output["methanevolR104"] = R104.Vnormal_CH4
        bmp_output["carbondioxidevolR104"] = R104.Vnormal_CO2
        bmp_output["oxygenvolR104"] = R104.Vnormal_O2
        bmp_output["hydrogensulfurvolR104"] = R104.Vnormal_H2S
        bmp_output["hydrogenvolR104"] = R104.Vnormal_H2
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR104"] = R104.x_CH4
        bmp_output["carbondioxideconcentrationR104"] = R104.x_CO2
        bmp_output["oxygenconcentrationR104"] = R104.x_O2
        bmp_output["hydrogensulfurconcentrationR104"] = R104.x_H2S
        bmp_output["hydrogenconcentrationR104"] = R104.x_H2
        #---- Biogás Volumen acumulado [mL]
        bmp_output["accumbiogasR104"] = R104.Vbiogas
        #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
        R104.PressurebyBiogas()
        if SideA_measurementMethod == "Pressure":
          bmp_output["accumbiogaspressureR104"] = R104.P_acum
          bmp_output["storagebiogaspressureR104"] = R104.P_storage
          bmp_output["storagebiogasR104"] = R104.V_storage
        #Volumen desplazado
        else:
          R104.poolSensor()
          bmp_output["poolLevelR104"] = R104.hpool
          bmp_output["poolTempR104"] = R104.Tpool
          bmp_output["poolPressureR104"] = R104.Ppool
        #Biogas energy
        R104.biogasEnergy()
        bmp_output["LHVR104"] = R104.LHV
        bmp_output["EnergyR104"] = R104.TotalBiogasEnergy
        bmp_output["PBMR104"] = R104.PBM
        
        # ----- Reactor 5
        if user_id105 not in bmp_instances:
          bmp_instances[user_id105] = BMPOffline.BMPModelOffline(Vrxn = SideA_Vrxn, Vf=SideA_vf, tp=SideA_tp)
        R105 = bmp_instances[user_id105]
        R105.MixtureCalculation(substratesNumber = SideA_substrateNumber, MixtureRule = SideA_MixRule, WaterFraction = SideA_Water, WaterVolume = SideA_Water, WaterWeight = SideA_Water, 
                                Fraction1 = SideA_Fraction1, Volume1 = SideA_Fraction1, Weight1 = SideA_Fraction1, TS1 = SideA_TS1, VS1 = SideA_VS1, rho1 = SideA_rho1, Cc1 = SideA_Cc1, Hc1 = SideA_Ch1, Oc1 = SideA_Co1, Nc1 = SideA_Cn1, Sc1 = SideA_Cs1,
                                Fraction2 = SideA_Fraction2, Volume2 = SideA_Fraction2, Weight2 = SideA_Fraction2, TS2 = SideA_TS2, VS2 = SideA_VS2, rho2 = SideA_rho2, Cc2 = SideA_Cc2, Hc2 = SideA_Ch2, Oc2 = SideA_Co2, Nc2 = SideA_Cn2, Sc2 = SideA_Cs2,
                                Fraction3 = SideA_Fraction3, Volume3 = SideA_Fraction3, Weight3 = SideA_Fraction3, TS3 = SideA_TS3, VS3 = SideA_VS3, rho3 = SideA_rho3, Cc3 = SideA_Cc3, Hc3 = SideA_Ch3, Oc3 = SideA_Co3, Nc3 = SideA_Cn3, Sc3 = SideA_Cs3,
                                Fraction4 = SideA_Fraction4, Volume4 = SideA_Fraction4, Weight4 = SideA_Fraction4, TS4 = SideA_TS4, VS4 = SideA_VS4, rho4 = SideA_rho4, Cc4 = SideA_Cc4, Hc4 = SideA_Ch4, Oc4 = SideA_Co4, Nc4 = SideA_Cn4, Sc4 = SideA_Cs4)
        
        #Agitación
        R105.MixControl(MixVelocity = SideA_MixVelocity, MixTime = SideA_MixTime, DailyMixing = SideA_DailyMixing)
        #---- Salidas Agitación
        bmp_output["mixVelocityR105"] = R105.MixVelocity

        #Alimentación
        R105.SubstrateFeed(Mode = SideA_FeedMode, Volume = SideA_FeedVolume, Time = SideA_FeedTime, Inyections = SideA_Injections, Q=1)
        #---- Salidas alimentación
        bmp_output["caudalSideA"] = R105.Qr
        bmp_output["volumeSubstrateSideA"] = R105.TotalVolFeed

        #Reactor
        R105.Reactor(model = SideA_Model, pH = SideA_pH, T = SideA_Temperatura, K1 = SideA_K1, K2 = SideA_K2, K3 = SideA_K3)
        #---- Salidas reactor R105
        bmp_output["SVR105"] = R105.SV 
        bmp_output["OCR105"] = R105.OC
        bmp_output["STR105"] = R105.ST
        bmp_output["XR105"] = R105.x
        bmp_output["KR105"] = R105.K1
        bmp_output["EaR105"] = R105.K2
        bmp_output["lambdaR105"] = R105.K3
        bmp_output["TempR105"] = R105.T   
        bmp_output["pHR105"] = R105.pH
        #---- Productos de reacción en moles [mol]
        bmp_output["methanemolR105"] = R105.mol_CH4
        bmp_output["carbondioxidemolR105"] = R105.mol_CO2
        bmp_output["oxygenmolR105"] = R105.mol_O2
        bmp_output["hydrogensulfurmolR105"] = R105.mol_H2S
        bmp_output["hydrogenmolR105"] = R105.mol_H2
        #---- Productos de reacción en vol normal [mL]
        R105.CompoundsUnits()
        bmp_output["methanevolR105"] = R105.Vnormal_CH4
        bmp_output["carbondioxidevolR105"] = R105.Vnormal_CO2
        bmp_output["oxygenvolR105"] = R105.Vnormal_O2
        bmp_output["hydrogensulfurvolR105"] = R105.Vnormal_H2S
        bmp_output["hydrogenvolR105"] = R105.Vnormal_H2
        #---- Productos de reacción en concentracion [%]
        bmp_output["methaneconcentrationR105"] = R105.x_CH4
        bmp_output["carbondioxideconcentrationR105"] = R105.x_CO2
        bmp_output["oxygenconcentrationR105"] = R105.x_O2
        bmp_output["hydrogensulfurconcentrationR105"] = R105.x_H2S
        bmp_output["hydrogenconcentrationR105"] = R105.x_H2
        #---- Biogás Volumen acumulado [mL]
        bmp_output["accumbiogasR105"] = R105.Vbiogas
        #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
        R105.PressurebyBiogas()
        if SideA_measurementMethod == "Pressure":
          bmp_output["accumbiogaspressureR105"] = R105.P_acum
          bmp_output["storagebiogaspressureR105"] = R105.P_storage
          bmp_output["storagebiogasR105"] = R105.V_storage
        #Volumen desplazado
        else:
          R105.poolSensor()
          bmp_output["poolLevelR105"] = R105.hpool
          bmp_output["poolTempR105"] = R105.Tpool
          bmp_output["poolPressureR105"] = R105.Ppool
        #Biogas energy
        R105.biogasEnergy()
        bmp_output["LHVR105"] = R105.LHV
        bmp_output["EnergyR105"] = R105.TotalBiogasEnergy
        bmp_output["PBMR105"] = R105.PBM
        
        # print(R101.Csus_ini_SV)
        # print(R101.Csus_ini)
        # print(R101.counterReactor)
         
    # else: #Lado A Aquí las funciones del modo Online
    #   pass
    
    # #lado B condiciones condiciones generales
    # offlineB = data["stateSelectionSideB"]
    # SideB_measurementMethod = data["measurementMethodSideB"]
    
    # #lado condiciones de corrida
    # SideB_Vrxn = data["rxnVolumeSideB"]["value"]
    # SideB_vf = data["freeVolumeSideB"]["value"]
    # SideB_tp = data["timeStepSideB"]["value"]
    # SideB_MixRule = data["substrate1CompositionSideB"]["variableString"]
    # SideB_substrateNumber = data["amountOfSubstratesSideB"]["value"]
    # SideB_Water = data["waterCompositionSideB"]["value"]
    
    # #sustrato 1
    # SideB_Fraction1 = data["substrate1CompositionSideB"]["value"]
    # SideB_TS1 = data ["totalSolidsSubstrate1SideB"]["value"]
    # SideB_VS1 = data["volatileSolidsSubstrate1SideB"]["value"]
    # SideB_rho1 = data["densitySubstrate1SideB"]["value"]
    # SideB_Cc1 = data["carbonContentSubstrate1SideB"]["value"]
    # SideB_Ch1 = data["hydrogenContentSubstrate1SideB"]["value"]
    # SideB_Co1 = data["oxygenContentSubstrate1SideB"]["value"]
    # SideB_Cn1 = data["nitrogenContentSubstrate1SideB"]["value"]
    # SideB_Cs1 = data["sulfurContentSubstrate1SideB"]["value"]
    # #sustrato 2
    # SideB_Fraction2 = data["substrate2CompositionSideB"]["value"]
    # SideB_TS2 = data ["totalSolidsSubstrate2SideB"]["value"]
    # SideB_VS2 = data["volatileSolidsSubstrate2SideB"]["value"]
    # SideB_rho2 = data["densitySubstrate2SideB"]["value"]
    # SideB_Cc2 = data["carbonContentSubstrate2SideB"]["value"]
    # SideB_Ch2 = data["hydrogenContentSubstrate2SideB"]["value"]
    # SideB_Co2 = data["oxygenContentSubstrate2SideB"]["value"]
    # SideB_Cn2 = data["nitrogenContentSubstrate2SideB"]["value"]
    # SideB_Cs2 = data["sulfurContentSubstrate2SideB"]["value"]
    # #sustrato 3
    # SideB_Fraction3 = data["substrate3CompositionSideB"]["value"]
    # SideB_TS3 = data ["totalSolidsSubstrate3SideB"]["value"]
    # SideB_VS3 = data["volatileSolidsSubstrate3SideB"]["value"]
    # SideB_rho3 = data["densitySubstrate3SideB"]["value"]
    # SideB_Cc3 = data["carbonContentSubstrate3SideB"]["value"]
    # SideB_Ch3 = data["hydrogenContentSubstrate3SideB"]["value"]
    # SideB_Co3 = data["oxygenContentSubstrate3SideB"]["value"]
    # SideB_Cn3 = data["nitrogenContentSubstrate3SideB"]["value"]
    # SideB_Cs3 = data["sulfurContentSubstrate3SideB"]["value"]
    # #sustrato 4
    # SideB_Fraction4 = data["substrate4CompositionSideB"]["value"]
    # SideB_TS4 = data ["totalSolidsSubstrate4SideB"]["value"]
    # SideB_VS4 = data["volatileSolidsSubstrate4SideB"]["value"]
    # SideB_rho4 = data["densitySubstrate4SideB"]["value"]
    # SideB_Cc4 = data["carbonContentSubstrate4SideB"]["value"]
    # SideB_Ch4 = data["hydrogenContentSubstrate4SideB"]["value"]
    # SideB_Co4 = data["oxygenContentSubstrate4SideB"]["value"]
    # SideB_Cn4 = data["nitrogenContentSubstrate4SideB"]["value"]
    # SideB_Cs4 = data["sulfurContentSubstrate4SideB"]["value"]
    # #mixControl
    # SideB_ManualMix = data["mixManualSideB"]
    # SideB_MixVelocity = data["mixVelocitySideB"]["value"]
    # SideB_MixTime = data["mixTimeSideB"]["value"]
    # SideB_DailyMixing = data["mixDailySideB"]["value"]
    # #Control Feed
    # SideB_ManualFeed = data["feefManualSideB"]
    # SideB_FeedMode = data["dosificationTypeSideB"]
    # SideB_FeedVolume = data["dosificationVolumeSideB"]["value"]
    # SideB_FeedTime = data["dailyInyectionsByTimeSideB"]["value"]
    # SideB_Injections = data["dailyInyectionsSideB"]["value"]
    # #Reactor
    # SideB_Model = data["modelSelectionSideB"]
    # SideB_pHauto = data["pHSideB"]["disabled"]
    # SideB_pH = data["pHSideB"]["value"]
    # SideB_Temperatura = data["TemperatureSideB"]["value"]
    # SideB_K1 = data["kineticKSideB"]["value"]
    # SideB_K2 = data["kineticEaSideB"]["value"]
    # SideB_K3 = data["kineticLambdaSideB"]["value"]
    
    # # Modo Offline
    # if offlineB == True:

    #   #---- Reactor 6
    #   if user106 is not bmp_instances:
    #     bmp_instances[user106] = bmp_simulation_start.BMPSimulationStart()
    #   R106_ini = bmp_instances[user106]
    #   R106_ini.starting(Vrxn = SideB_Vrxn, Vf=SideB_vf, tp=SideB_tp)
    #   R106 = R106_ini.data
    #   R106.MixtureCalculation(substratesNumber = SideB_substrateNumber, MixtureRule = SideB_MixRule, WaterFraction = SideB_Water, WaterVolume = SideB_Water, WaterWeight = SideB_Water, 
    #                           Fraction1 = SideB_Fraction1, Volume1 = SideB_Fraction1, Weight1 = SideB_Fraction1, TS1 = SideB_TS1, VS1 = SideB_VS1, rho1 = SideB_rho1, Cc1 = SideB_Cc1, Hc1 = SideB_Ch1, Oc1 = SideB_Co1, Nc1 = SideB_Cn1, Sc1 = SideB_Cs1,
    #                           Fraction2 = SideB_Fraction2, Volume2 = SideB_Fraction2, Weight2 = SideB_Fraction2, TS2 = SideB_TS2, VS2 = SideB_VS2, rho2 = SideB_rho2, Cc2 = SideB_Cc2, Hc2 = SideB_Ch2, Oc2 = SideB_Co2, Nc2 = SideB_Cn2, Sc2 = SideB_Cs2,
    #                           Fraction3 = SideB_Fraction3, Volume3 = SideB_Fraction3, Weight3 = SideB_Fraction3, TS3 = SideB_TS3, VS3 = SideB_VS3, rho3 = SideB_rho3, Cc3 = SideB_Cc3, Hc3 = SideB_Ch3, Oc3 = SideB_Co3, Nc3 = SideB_Cn3, Sc3 = SideB_Cs3,
    #                           Fraction4 = SideB_Fraction4, Volume4 = SideB_Fraction4, Weight4 = SideB_Fraction4, TS4 = SideB_TS4, VS4 = SideB_VS4, rho4 = SideB_rho4, Cc4 = SideB_Cc4, Hc4 = SideB_Ch4, Oc4 = SideB_Co4, Nc4 = SideB_Cn4, Sc4 = SideB_Cs4)
      
    #   #Agitación
    #   R106.MixControl(MixVelocity = SideB_MixVelocity, MixTime = SideB_MixTime, DailyMixing = SideB_DailyMixing)
    #   #---- Salidas Agitación
    #   bmp_output["mixVelocityR106"] = R106.MixVelocity

    #   #Alimentación
    #   R106.SubstrateFeed(Mode = SideB_FeedMode, Volume = SideB_FeedVolume, Time = SideB_FeedTime, Inyections = SideB_Injections, Q=1)
    #   #---- Salidas alimentación
    #   bmp_output["caudalSideB"] = R106.Qr
    #   bmp_output["volumeSubstrateSideB"] = R106.TotalVolFeed

    #   #Reactor
    #   R106.Reactor(model = SideB_Model, pH = SideB_pH, T = SideB_Temperatura, K1 = SideB_K1, K2 = SideB_K2, K3 = SideB_K3)
    #   #---- Salidas reactor R106
    #   bmp_output["SVR106"] = R106.SV 
    #   bmp_output["OCR106"] = R106.OC
    #   bmp_output["STR106"] = R106.ST
    #   bmp_output["XR106"] = R106.x
    #   bmp_output["KR106"] = R106.K1
    #   bmp_output["EaR106"] = R106.K2
    #   bmp_output["lambdaR106"] = R106.K3
    #   bmp_output["TempR106"] = R106.T   
    #   bmp_output["pHR106"] = R106.pH
    #   #---- Productos de reacción en moles [mol]
    #   bmp_output["methanemolR106"] = R106.mol_CH4
    #   bmp_output["carbondioxidemolR106"] = R106.mol_CO2
    #   bmp_output["oxygenmolR106"] = R106.mol_O2
    #   bmp_output["hydrogensulfurmolR106"] = R106.mol_H2S
    #   bmp_output["hydrogenmolR106"] = R106.mol_H2
    #   #---- Productos de reacción en vol normal [mL]
    #   R106.CompoundsUnits()
    #   bmp_output["methanevolR106"] = R106.Vnormal_CH4
    #   bmp_output["carbondioxidevolR106"] = R106.Vnormal_CO2
    #   bmp_output["oxygenvolR106"] = R106.Vnormal_O2
    #   bmp_output["hydrogensulfurvolR106"] = R106.Vnormal_H2S
    #   bmp_output["hydrogenvolR106"] = R106.Vnormal_H2
    #   #---- Productos de reacción en concentracion [%]
    #   bmp_output["methaneconcentrationR106"] = R106.x_CH4
    #   bmp_output["carbondioxideconcentrationR106"] = R106.x_CO2
    #   bmp_output["oxygenconcentrationR106"] = R106.x_O2
    #   bmp_output["hydrogensulfurconcentrationR106"] = R106.x_H2S
    #   bmp_output["hydrogenconcentrationR106"] = R106.x_H2
    #   #---- Biogás Volumen acumulado [mL]
    #   bmp_output["accumbiogasR106"] = R106.Vbiogas
    #   #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
    #   R106.PressurebyBiogas()
    #   if SideB_measurementMethod == "Pressure":
    #     bmp_output["accumbiogaspressureR106"] = R106.P_acum
    #     bmp_output["storagebiogaspressureR106"] = R106.P_storage
    #     bmp_output["storagebiogasR106"] = R106.V_storage
    #   #Volumen desplazado
    #   else:
    #     R106.poolSensor()
    #     bmp_output["poolLevelR106"] = R106.hpool
    #     bmp_output["poolTempR106"] = R106.Tpool
    #     bmp_output["poolPressureR106"] = R106.Ppool
    #   #Biogas energy
    #   R106.biogasEnergy()
    #   bmp_output["LHVR106"] = R106.LHV
    #   bmp_output["EnergyR106"] = R106.TotalBiogasEnergy
    #   bmp_output["PBMR106"] = R106.PBM
      
    #   #---- Reactor 7
    #   if user107 is not bmp_instances:
    #     bmp_instances[user107] = bmp_simulation_start.BMPSimulationStart()
    #   R107_ini = bmp_instances[user107]
    #   R107_ini.starting(Vrxn = SideB_Vrxn, Vf=SideB_vf, tp=SideB_tp)
    #   R107 = R107_ini.data
    #   R107.MixtureCalculation(substratesNumber = SideB_substrateNumber, MixtureRule = SideB_MixRule, WaterFraction = SideB_Water, WaterVolume = SideB_Water, WaterWeight = SideB_Water, 
    #                           Fraction1 = SideB_Fraction1, Volume1 = SideB_Fraction1, Weight1 = SideB_Fraction1, TS1 = SideB_TS1, VS1 = SideB_VS1, rho1 = SideB_rho1, Cc1 = SideB_Cc1, Hc1 = SideB_Ch1, Oc1 = SideB_Co1, Nc1 = SideB_Cn1, Sc1 = SideB_Cs1,
    #                           Fraction2 = SideB_Fraction2, Volume2 = SideB_Fraction2, Weight2 = SideB_Fraction2, TS2 = SideB_TS2, VS2 = SideB_VS2, rho2 = SideB_rho2, Cc2 = SideB_Cc2, Hc2 = SideB_Ch2, Oc2 = SideB_Co2, Nc2 = SideB_Cn2, Sc2 = SideB_Cs2,
    #                           Fraction3 = SideB_Fraction3, Volume3 = SideB_Fraction3, Weight3 = SideB_Fraction3, TS3 = SideB_TS3, VS3 = SideB_VS3, rho3 = SideB_rho3, Cc3 = SideB_Cc3, Hc3 = SideB_Ch3, Oc3 = SideB_Co3, Nc3 = SideB_Cn3, Sc3 = SideB_Cs3,
    #                           Fraction4 = SideB_Fraction4, Volume4 = SideB_Fraction4, Weight4 = SideB_Fraction4, TS4 = SideB_TS4, VS4 = SideB_VS4, rho4 = SideB_rho4, Cc4 = SideB_Cc4, Hc4 = SideB_Ch4, Oc4 = SideB_Co4, Nc4 = SideB_Cn4, Sc4 = SideB_Cs4)
      
    #   #Agitación
    #   R107.MixControl(MixVelocity = SideB_MixVelocity, MixTime = SideB_MixTime, DailyMixing = SideB_DailyMixing)
    #   #---- Salidas Agitación
    #   bmp_output["mixVelocityR107"] = R107.MixVelocity

    #   #Alimentación
    #   R107.SubstrateFeed(Mode = SideB_FeedMode, Volume = SideB_FeedVolume, Time = SideB_FeedTime, Inyections = SideB_Injections, Q=1)
    #   #---- Salidas alimentación
    #   bmp_output["caudalSideB"] = R107.Qr
    #   bmp_output["volumeSubstrateSideB"] = R107.TotalVolFeed

    #   #Reactor
    #   R107.Reactor(model = SideB_Model, pH = SideB_pH, T = SideB_Temperatura, K1 = SideB_K1, K2 = SideB_K2, K3 = SideB_K3)
    #   #---- Salidas reactor R107
    #   bmp_output["SVR107"] = R107.SV 
    #   bmp_output["OCR107"] = R107.OC
    #   bmp_output["STR107"] = R107.ST
    #   bmp_output["XR107"] = R107.x
    #   bmp_output["KR107"] = R107.K1
    #   bmp_output["EaR107"] = R107.K2
    #   bmp_output["lambdaR107"] = R107.K3
    #   bmp_output["TempR107"] = R107.T   
    #   bmp_output["pHR107"] = R107.pH
    #   #---- Productos de reacción en moles [mol]
    #   bmp_output["methanemolR107"] = R107.mol_CH4
    #   bmp_output["carbondioxidemolR107"] = R107.mol_CO2
    #   bmp_output["oxygenmolR107"] = R107.mol_O2
    #   bmp_output["hydrogensulfurmolR107"] = R107.mol_H2S
    #   bmp_output["hydrogenmolR107"] = R107.mol_H2
    #   #---- Productos de reacción en vol normal [mL]
    #   R107.CompoundsUnits()
    #   bmp_output["methanevolR107"] = R107.Vnormal_CH4
    #   bmp_output["carbondioxidevolR107"] = R107.Vnormal_CO2
    #   bmp_output["oxygenvolR107"] = R107.Vnormal_O2
    #   bmp_output["hydrogensulfurvolR107"] = R107.Vnormal_H2S
    #   bmp_output["hydrogenvolR107"] = R107.Vnormal_H2
    #   #---- Productos de reacción en concentracion [%]
    #   bmp_output["methaneconcentrationR107"] = R107.x_CH4
    #   bmp_output["carbondioxideconcentrationR107"] = R107.x_CO2
    #   bmp_output["oxygenconcentrationR107"] = R107.x_O2
    #   bmp_output["hydrogensulfurconcentrationR107"] = R107.x_H2S
    #   bmp_output["hydrogenconcentrationR107"] = R107.x_H2
    #   #---- Biogás Volumen acumulado [mL]
    #   bmp_output["accumbiogasR107"] = R107.Vbiogas
    #   #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
    #   R107.PressurebyBiogas()
    #   if SideB_measurementMethod == "Pressure":
    #     bmp_output["accumbiogaspressureR107"] = R107.P_acum
    #     bmp_output["storagebiogaspressureR107"] = R107.P_storage
    #     bmp_output["storagebiogasR107"] = R107.V_storage
    #   #Volumen desplazado
    #   else:
    #     R107.poolSensor()
    #     bmp_output["poolLevelR107"] = R107.hpool
    #     bmp_output["poolTempR107"] = R107.Tpool
    #     bmp_output["poolPressureR107"] = R107.Ppool
    #   #Biogas energy
    #   R107.biogasEnergy()
    #   bmp_output["LHVR107"] = R107.LHV
    #   bmp_output["EnergyR107"] = R107.TotalBiogasEnergy
    #   bmp_output["PBMR107"] = R107.PBM
      
    #   #---- Reactor 8
    #   if user108 is not bmp_instances:
    #     bmp_instances[user108] = bmp_simulation_start.BMPSimulationStart()
    #   R108_ini = bmp_instances[user108]
    #   R108_ini.starting(Vrxn = SideB_Vrxn, Vf=SideB_vf, tp=SideB_tp)
    #   R108 = R108_ini.data
    #   R108.MixtureCalculation(substratesNumber = SideB_substrateNumber, MixtureRule = SideB_MixRule, WaterFraction = SideB_Water, WaterVolume = SideB_Water, WaterWeight = SideB_Water, 
    #                           Fraction1 = SideB_Fraction1, Volume1 = SideB_Fraction1, Weight1 = SideB_Fraction1, TS1 = SideB_TS1, VS1 = SideB_VS1, rho1 = SideB_rho1, Cc1 = SideB_Cc1, Hc1 = SideB_Ch1, Oc1 = SideB_Co1, Nc1 = SideB_Cn1, Sc1 = SideB_Cs1,
    #                           Fraction2 = SideB_Fraction2, Volume2 = SideB_Fraction2, Weight2 = SideB_Fraction2, TS2 = SideB_TS2, VS2 = SideB_VS2, rho2 = SideB_rho2, Cc2 = SideB_Cc2, Hc2 = SideB_Ch2, Oc2 = SideB_Co2, Nc2 = SideB_Cn2, Sc2 = SideB_Cs2,
    #                           Fraction3 = SideB_Fraction3, Volume3 = SideB_Fraction3, Weight3 = SideB_Fraction3, TS3 = SideB_TS3, VS3 = SideB_VS3, rho3 = SideB_rho3, Cc3 = SideB_Cc3, Hc3 = SideB_Ch3, Oc3 = SideB_Co3, Nc3 = SideB_Cn3, Sc3 = SideB_Cs3,
    #                           Fraction4 = SideB_Fraction4, Volume4 = SideB_Fraction4, Weight4 = SideB_Fraction4, TS4 = SideB_TS4, VS4 = SideB_VS4, rho4 = SideB_rho4, Cc4 = SideB_Cc4, Hc4 = SideB_Ch4, Oc4 = SideB_Co4, Nc4 = SideB_Cn4, Sc4 = SideB_Cs4)
      
    #   #Agitación
    #   R108.MixControl(MixVelocity = SideB_MixVelocity, MixTime = SideB_MixTime, DailyMixing = SideB_DailyMixing)
    #   #---- Salidas Agitación
    #   bmp_output["mixVelocityR108"] = R108.MixVelocity

    #   #Alimentación
    #   R108.SubstrateFeed(Mode = SideB_FeedMode, Volume = SideB_FeedVolume, Time = SideB_FeedTime, Inyections = SideB_Injections, Q=1)
    #   #---- Salidas alimentación
    #   bmp_output["caudalSideB"] = R108.Qr
    #   bmp_output["volumeSubstrateSideB"] = R108.TotalVolFeed

    #   #Reactor
    #   R108.Reactor(model = SideB_Model, pH = SideB_pH, T = SideB_Temperatura, K1 = SideB_K1, K2 = SideB_K2, K3 = SideB_K3)
    #   #---- Salidas reactor R108
    #   bmp_output["SVR108"] = R108.SV 
    #   bmp_output["OCR108"] = R108.OC
    #   bmp_output["STR108"] = R108.ST
    #   bmp_output["XR108"] = R108.x
    #   bmp_output["KR108"] = R108.K1
    #   bmp_output["EaR108"] = R108.K2
    #   bmp_output["lambdaR108"] = R108.K3
    #   bmp_output["TempR108"] = R108.T   
    #   bmp_output["pHR108"] = R108.pH
    #   #---- Productos de reacción en moles [mol]
    #   bmp_output["methanemolR108"] = R108.mol_CH4
    #   bmp_output["carbondioxidemolR108"] = R108.mol_CO2
    #   bmp_output["oxygenmolR108"] = R108.mol_O2
    #   bmp_output["hydrogensulfurmolR108"] = R108.mol_H2S
    #   bmp_output["hydrogenmolR108"] = R108.mol_H2
    #   #---- Productos de reacción en vol normal [mL]
    #   R108.CompoundsUnits()
    #   bmp_output["methanevolR108"] = R108.Vnormal_CH4
    #   bmp_output["carbondioxidevolR108"] = R108.Vnormal_CO2
    #   bmp_output["oxygenvolR108"] = R108.Vnormal_O2
    #   bmp_output["hydrogensulfurvolR108"] = R108.Vnormal_H2S
    #   bmp_output["hydrogenvolR108"] = R108.Vnormal_H2
    #   #---- Productos de reacción en concentracion [%]
    #   bmp_output["methaneconcentrationR108"] = R108.x_CH4
    #   bmp_output["carbondioxideconcentrationR108"] = R108.x_CO2
    #   bmp_output["oxygenconcentrationR108"] = R108.x_O2
    #   bmp_output["hydrogensulfurconcentrationR108"] = R108.x_H2S
    #   bmp_output["hydrogenconcentrationR108"] = R108.x_H2
    #   #---- Biogás Volumen acumulado [mL]
    #   bmp_output["accumbiogasR108"] = R108.Vbiogas
    #   #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
    #   R108.PressurebyBiogas()
    #   if SideB_measurementMethod == "Pressure":
    #     bmp_output["accumbiogaspressureR108"] = R108.P_acum
    #     bmp_output["storagebiogaspressureR108"] = R108.P_storage
    #     bmp_output["storagebiogasR108"] = R108.V_storage
    #   #Volumen desplazado
    #   else:
    #     R108.poolSensor()
    #     bmp_output["poolLevelR108"] = R108.hpool
    #     bmp_output["poolTempR108"] = R108.Tpool
    #     bmp_output["poolPressureR108"] = R108.Ppool
    #   #Biogas energy
    #   R108.biogasEnergy()
    #   bmp_output["LHVR108"] = R108.LHV
    #   bmp_output["EnergyR108"] = R108.TotalBiogasEnergy
    #   bmp_output["PBMR108"] = R108.PBM
      
    #   #---- Reactor 9
    #   if user109 is not bmp_instances:
    #     bmp_instances[user109] = bmp_simulation_start.BMPSimulationStart()
    #   R109_ini = bmp_instances[user109]
    #   R109_ini.starting(Vrxn = SideB_Vrxn, Vf=SideB_vf, tp=SideB_tp)
    #   R109 = R109_ini.data
    #   R109.MixtureCalculation(substratesNumber = SideB_substrateNumber, MixtureRule = SideB_MixRule, WaterFraction = SideB_Water, WaterVolume = SideB_Water, WaterWeight = SideB_Water, 
    #                           Fraction1 = SideB_Fraction1, Volume1 = SideB_Fraction1, Weight1 = SideB_Fraction1, TS1 = SideB_TS1, VS1 = SideB_VS1, rho1 = SideB_rho1, Cc1 = SideB_Cc1, Hc1 = SideB_Ch1, Oc1 = SideB_Co1, Nc1 = SideB_Cn1, Sc1 = SideB_Cs1,
    #                           Fraction2 = SideB_Fraction2, Volume2 = SideB_Fraction2, Weight2 = SideB_Fraction2, TS2 = SideB_TS2, VS2 = SideB_VS2, rho2 = SideB_rho2, Cc2 = SideB_Cc2, Hc2 = SideB_Ch2, Oc2 = SideB_Co2, Nc2 = SideB_Cn2, Sc2 = SideB_Cs2,
    #                           Fraction3 = SideB_Fraction3, Volume3 = SideB_Fraction3, Weight3 = SideB_Fraction3, TS3 = SideB_TS3, VS3 = SideB_VS3, rho3 = SideB_rho3, Cc3 = SideB_Cc3, Hc3 = SideB_Ch3, Oc3 = SideB_Co3, Nc3 = SideB_Cn3, Sc3 = SideB_Cs3,
    #                           Fraction4 = SideB_Fraction4, Volume4 = SideB_Fraction4, Weight4 = SideB_Fraction4, TS4 = SideB_TS4, VS4 = SideB_VS4, rho4 = SideB_rho4, Cc4 = SideB_Cc4, Hc4 = SideB_Ch4, Oc4 = SideB_Co4, Nc4 = SideB_Cn4, Sc4 = SideB_Cs4)
      
    #   #Agitación
    #   R109.MixControl(MixVelocity = SideB_MixVelocity, MixTime = SideB_MixTime, DailyMixing = SideB_DailyMixing)
    #   #---- Salidas Agitación
    #   bmp_output["mixVelocityR109"] = R109.MixVelocity

    #   #Alimentación
    #   R109.SubstrateFeed(Mode = SideB_FeedMode, Volume = SideB_FeedVolume, Time = SideB_FeedTime, Inyections = SideB_Injections, Q=1)
    #   #---- Salidas alimentación
    #   bmp_output["caudalSideB"] = R109.Qr
    #   bmp_output["volumeSubstrateSideB"] = R109.TotalVolFeed

    #   #Reactor
    #   R109.Reactor(model = SideB_Model, pH = SideB_pH, T = SideB_Temperatura, K1 = SideB_K1, K2 = SideB_K2, K3 = SideB_K3)
    #   #---- Salidas reactor R109
    #   bmp_output["SVR109"] = R109.SV 
    #   bmp_output["OCR109"] = R109.OC
    #   bmp_output["STR109"] = R109.ST
    #   bmp_output["XR109"] = R109.x
    #   bmp_output["KR109"] = R109.K1
    #   bmp_output["EaR109"] = R109.K2
    #   bmp_output["lambdaR109"] = R109.K3
    #   bmp_output["TempR109"] = R109.T   
    #   bmp_output["pHR109"] = R109.pH
    #   #---- Productos de reacción en moles [mol]
    #   bmp_output["methanemolR109"] = R109.mol_CH4
    #   bmp_output["carbondioxidemolR109"] = R109.mol_CO2
    #   bmp_output["oxygenmolR109"] = R109.mol_O2
    #   bmp_output["hydrogensulfurmolR109"] = R109.mol_H2S
    #   bmp_output["hydrogenmolR109"] = R109.mol_H2
    #   #---- Productos de reacción en vol normal [mL]
    #   R109.CompoundsUnits()
    #   bmp_output["methanevolR109"] = R109.Vnormal_CH4
    #   bmp_output["carbondioxidevolR109"] = R109.Vnormal_CO2
    #   bmp_output["oxygenvolR109"] = R109.Vnormal_O2
    #   bmp_output["hydrogensulfurvolR109"] = R109.Vnormal_H2S
    #   bmp_output["hydrogenvolR109"] = R109.Vnormal_H2
    #   #---- Productos de reacción en concentracion [%]
    #   bmp_output["methaneconcentrationR109"] = R109.x_CH4
    #   bmp_output["carbondioxideconcentrationR109"] = R109.x_CO2
    #   bmp_output["oxygenconcentrationR109"] = R109.x_O2
    #   bmp_output["hydrogensulfurconcentrationR109"] = R109.x_H2S
    #   bmp_output["hydrogenconcentrationR109"] = R109.x_H2
    #   #---- Biogás Volumen acumulado [mL]
    #   bmp_output["accumbiogasR109"] = R109.Vbiogas
    #   #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
    #   R109.PressurebyBiogas()
    #   if SideB_measurementMethod == "Pressure":
    #     bmp_output["accumbiogaspressureR109"] = R109.P_acum
    #     bmp_output["storagebiogaspressureR109"] = R109.P_storage
    #     bmp_output["storagebiogasR109"] = R109.V_storage
    #   #Volumen desplazado
    #   else:
    #     R109.poolSensor()
    #     bmp_output["poolLevelR109"] = R109.hpool
    #     bmp_output["poolTempR109"] = R109.Tpool
    #     bmp_output["poolPressureR109"] = R109.Ppool
    #   #Biogas energy
    #   R109.biogasEnergy()
    #   bmp_output["LHVR109"] = R109.LHV
    #   bmp_output["EnergyR109"] = R109.TotalBiogasEnergy
    #   bmp_output["PBMR109"] = R109.PBM
      
    #   #---- Reactor 10
    #   if user110 is not bmp_instances:
    #     bmp_instances[user110] = bmp_simulation_start.BMPSimulationStart()
    #   R110_ini = bmp_instances[user110]
    #   R110_ini.starting(Vrxn = SideB_Vrxn, Vf=SideB_vf, tp=SideB_tp)
    #   R110 = R110_ini.data
    #   R110.MixtureCalculation(substratesNumber = SideB_substrateNumber, MixtureRule = SideB_MixRule, WaterFraction = SideB_Water, WaterVolume = SideB_Water, WaterWeight = SideB_Water, 
    #                           Fraction1 = SideB_Fraction1, Volume1 = SideB_Fraction1, Weight1 = SideB_Fraction1, TS1 = SideB_TS1, VS1 = SideB_VS1, rho1 = SideB_rho1, Cc1 = SideB_Cc1, Hc1 = SideB_Ch1, Oc1 = SideB_Co1, Nc1 = SideB_Cn1, Sc1 = SideB_Cs1,
    #                           Fraction2 = SideB_Fraction2, Volume2 = SideB_Fraction2, Weight2 = SideB_Fraction2, TS2 = SideB_TS2, VS2 = SideB_VS2, rho2 = SideB_rho2, Cc2 = SideB_Cc2, Hc2 = SideB_Ch2, Oc2 = SideB_Co2, Nc2 = SideB_Cn2, Sc2 = SideB_Cs2,
    #                           Fraction3 = SideB_Fraction3, Volume3 = SideB_Fraction3, Weight3 = SideB_Fraction3, TS3 = SideB_TS3, VS3 = SideB_VS3, rho3 = SideB_rho3, Cc3 = SideB_Cc3, Hc3 = SideB_Ch3, Oc3 = SideB_Co3, Nc3 = SideB_Cn3, Sc3 = SideB_Cs3,
    #                           Fraction4 = SideB_Fraction4, Volume4 = SideB_Fraction4, Weight4 = SideB_Fraction4, TS4 = SideB_TS4, VS4 = SideB_VS4, rho4 = SideB_rho4, Cc4 = SideB_Cc4, Hc4 = SideB_Ch4, Oc4 = SideB_Co4, Nc4 = SideB_Cn4, Sc4 = SideB_Cs4)
      
    #   #Agitación
    #   R110.MixControl(MixVelocity = SideB_MixVelocity, MixTime = SideB_MixTime, DailyMixing = SideB_DailyMixing)
    #   #---- Salidas Agitación
    #   bmp_output["mixVelocityR110"] = R110.MixVelocity

    #   #Alimentación
    #   R110.SubstrateFeed(Mode = SideB_FeedMode, Volume = SideB_FeedVolume, Time = SideB_FeedTime, Inyections = SideB_Injections, Q=1)
    #   #---- Salidas alimentación
    #   bmp_output["caudalSideB"] = R110.Qr
    #   bmp_output["volumeSubstrateSideB"] = R110.TotalVolFeed

    #   #Reactor
    #   R110.Reactor(model = SideB_Model, pH = SideB_pH, T = SideB_Temperatura, K1 = SideB_K1, K2 = SideB_K2, K3 = SideB_K3)
    #   #---- Salidas reactor R110
    #   bmp_output["SVR110"] = R110.SV 
    #   bmp_output["OCR110"] = R110.OC
    #   bmp_output["STR110"] = R110.ST
    #   bmp_output["XR110"] = R110.x
    #   bmp_output["KR110"] = R110.K1
    #   bmp_output["EaR110"] = R110.K2
    #   bmp_output["lambdaR110"] = R110.K3
    #   bmp_output["TempR110"] = R110.T   
    #   bmp_output["pHR110"] = R110.pH
    #   #---- Productos de reacción en moles [mol]
    #   bmp_output["methanemolR110"] = R110.mol_CH4
    #   bmp_output["carbondioxidemolR110"] = R110.mol_CO2
    #   bmp_output["oxygenmolR110"] = R110.mol_O2
    #   bmp_output["hydrogensulfurmolR110"] = R110.mol_H2S
    #   bmp_output["hydrogenmolR110"] = R110.mol_H2
    #   #---- Productos de reacción en vol normal [mL]
    #   R110.CompoundsUnits()
    #   bmp_output["methanevolR110"] = R110.Vnormal_CH4
    #   bmp_output["carbondioxidevolR110"] = R110.Vnormal_CO2
    #   bmp_output["oxygenvolR110"] = R110.Vnormal_O2
    #   bmp_output["hydrogensulfurvolR110"] = R110.Vnormal_H2S
    #   bmp_output["hydrogenvolR110"] = R110.Vnormal_H2
    #   #---- Productos de reacción en concentracion [%]
    #   bmp_output["methaneconcentrationR110"] = R110.x_CH4
    #   bmp_output["carbondioxideconcentrationR110"] = R110.x_CO2
    #   bmp_output["oxygenconcentrationR110"] = R110.x_O2
    #   bmp_output["hydrogensulfurconcentrationR110"] = R110.x_H2S
    #   bmp_output["hydrogenconcentrationR110"] = R110.x_H2
    #   #---- Biogás Volumen acumulado [mL]
    #   bmp_output["accumbiogasR110"] = R110.Vbiogas
    #   #---- Biogas Presión y volumen almacenado solo para la opción de almacenamiento por presión
    #   R110.PressurebyBiogas()
    #   if SideB_measurementMethod == "Pressure":
    #     bmp_output["accumbiogaspressureR110"] = R110.P_acum
    #     bmp_output["storagebiogaspressureR110"] = R110.P_storage
    #     bmp_output["storagebiogasR110"] = R110.V_storage
    #   #Volumen desplazado
    #   else:
    #     R110.poolSensor()
    #     bmp_output["poolLevelR110"] = R110.hpool
    #     bmp_output["poolTempR110"] = R110.Tpool
    #     bmp_output["poolPressureR110"] = R110.Ppool
    #   #Biogas energy
    #   R110.biogasEnergy()
    #   bmp_output["LHVR110"] = R110.LHV
    #   bmp_output["EnergyR110"] = R110.TotalBiogasEnergy
    #   bmp_output["PBMR110"] = R110.PBM
      
    #   print(bmp_instances)
    
    return {"model": bmp_output}, 200