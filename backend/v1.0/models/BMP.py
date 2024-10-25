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

    offline = data["stateSelectionSideA"]
    SideA_Vrxn = data["rxnVolumeSideA"]
    SideA_vf = data["freeVolumeSideA"]
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

    # Modo Offline
    if offline == True:

      #Reactor 1
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
      bmp_output["mixVelocityR101"] = R101.MixVelocity

      #Alimentación
      R101.SubstrateFeed(Mode = SideA_FeedMode, Volume = SideA_FeedVolume, Time = SideA_FeedTime, Inyections = SideA_Injections)
      bmp_output["caudalSideA"] = R101.Qr
      bmp_output["volumeSubstrateSideA"] = R101.TotalVolFeed
      

    
    print(bmp_output)
    return {"model": bmp_output}, 200