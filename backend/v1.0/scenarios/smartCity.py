from flask import request
from flask_restful import Resource
from simulation_models.Scenarios_models import Smartcity

class SmartCity(Resource):
  def post(self):
    data = request.get_json()
    print(data)

    if data['operationMode'] == 'Manual':
      operationType = 1
    else:
      operationType = 2
    
    simulationSteps = data['steps']['value']
    
    if data['stepUnit'] == 'Second':
      stepTime = data['stepTime']['value'] / 3600
    elif data['stepUnit'] == 'Minute':
      stepTime = data['stepTime']['value'] / 60
    elif data['stepUnit'] == 'Hour':
      stepTime = data['stepTime']['value']
    elif data['stepUnit'] == 'Day':
      stepTime = data['stepTime']['value'] * 24

    solarSystemNumber = data['solarSystemNumber']['value']
    biogasSystemNumber = data['biogasSystemNumber']['value']
    batterySystemNumber = data['batterySystemNumber']['value']
    hydraulicSystemNumber = data['hydraulicSystemNumber']['value']
    windSystemNumber = data['windSystemNumber']['value']
    loadSystemNumber = data['loadSystemNumber']['value']

    smartcity_model = Smartcity.Smartcity(N_PV=solarSystemNumber, N_BESS=batterySystemNumber, N_Hydro=hydraulicSystemNumber,
                                           N_WF=windSystemNumber, N_Biogas=biogasSystemNumber, N_Demand=loadSystemNumber,
                                             operationType=operationType, simulationSteps=simulationSteps, stepTime=stepTime)

    PV_Names = []
    moduleNumbers = []
    modulePowers = []
    moduleTypes = []
    deratingFactor = []
    efficiency = []
    nominalIrradiance = []
    testIrradiance = []
    nominalTemperature = []
    testTemperature = []
    operatingTemperature = []
    temperatureVariationCoefficient = []

    for solarSystem in data['solarSystems']:
      PV_Names.append(solarSystem['name'])
      moduleNumbers.append(solarSystem['modulesNumber']['value'])
      modulePowers.append(solarSystem['modulePower']['value'])
      if solarSystem['type'] == 'MonocrystallinePanel':
        moduleTypes.append(1)
      elif solarSystem['type'] == 'PolicrystallinePanel':
        moduleTypes.append(2)
      elif solarSystem['type'] == 'FlexPanel':
        moduleTypes.append(3)
      elif solarSystem['type'] == 'CadmiumTelluridePanel':
        moduleTypes.append(4)
      elif solarSystem['type'] == 'Custom':
        moduleTypes.append(0)
        deratingFactor.append(solarSystem['deratingFactor']['value'])
        efficiency.append(solarSystem['efficiency']['value'])
        nominalIrradiance.append(solarSystem['nominalIrradiance']['value'])
        testIrradiance.append(solarSystem['testIrradiance']['value'])
        nominalTemperature.append(solarSystem['nominalTemperature']['value'])
        testTemperature.append(solarSystem['testTemperature']['value'])
        operatingTemperature.append(solarSystem['operatingTemperature']['value'])
        temperatureVariationCoefficient.append(solarSystem['temperatureVariationCoefficient']['value'])

    BESS_Names = []
    batteryTypes = []
    storageCapacity = []
    maxChargePower = []
    minChargePower = []
    maxDischargePower = []
    minDischargePower = []
    stateOfCharge = []
    selfDischargeCoefficient = []
    chargeEfficiency = []
    dischargeEfficiency = []

    for batterySystem in data['batterySystems']:
      BESS_Names.append(batterySystem['name'])
      storageCapacity.append(batterySystem['storageCapacity']['value'])
      maxChargePower.append(batterySystem['maxChargePower']['value'])
      minChargePower.append(batterySystem['minChargePower']['value'])
      maxDischargePower.append(batterySystem['maxDischargePower']['value'])
      minDischargePower.append(batterySystem['minDischargePower']['value'])
      stateOfCharge.append(batterySystem['stateOfCharge']['value'])
      if batterySystem['type'] == 'Gel':
        batteryTypes.append(1)
      elif batterySystem['type'] == 'Custom':
        batteryTypes.append(0)
        selfDischargeCoefficient.append(batterySystem['selfDischargeCoefficient']['value'])
        chargeEfficiency.append(batterySystem['chargeEfficiency']['value'])
        dischargeEfficiency.append(batterySystem['dischargeEfficiency']['value'])

    hydroNames = []
    turbineNumbers = []
    turbinePowers = []
    turbineTypes = []
    efficiency = []
    frictionLosses = []
    minimumWaterHead = []
    maximumWaterHead = []
    minimumWaterFlow = []
    maximumWaterFlow = []

    for hydraulicSystem in data['hydraulicSystems']:
      hydroNames.append(hydraulicSystem['name'])
      turbineNumbers.append(hydraulicSystem['turbineNumber']['value'])
      turbinePowers.append(hydraulicSystem['nominalPower']['value'])
      if hydraulicSystem['type'] == 'Pelton':
        turbineTypes.append(1)
      if hydraulicSystem['type'] == 'Turgo':
        turbineTypes.append(2)
      elif hydraulicSystem['type'] == 'Custom':
        turbineTypes.append(0)
        efficiency.append(hydraulicSystem['efficiency']['value'])
        frictionLosses.append(hydraulicSystem['frictionLosses']['value'])
        minimumWaterHead.append(hydraulicSystem['minimumWaterHead']['value'])
        maximumWaterHead.append(hydraulicSystem['maximumWaterHead']['value'])
        minimumWaterFlow.append(hydraulicSystem['minimumWaterFlow']['value'])
        maximumWaterFlow.append(hydraulicSystem['maximumWaterFlow']['value'])

    windNames = []
    windTurbineNumbers = []
    windTurbinePowers = []
    windTurbineTypes = []
    airDensity = []
    rotorHeight = []
    anemometerHeight = []
    ratedWindSpeed = []
    lowerCutoffWindSpeed = []
    upperCutoffWindSpeed = []
    surfaceRoughnessLength = []

    for windSystem in data['windSystems']:
      windNames.append(windSystem['name'])
      windTurbineNumbers.append(windSystem['turbineNumber']['value'])
      windTurbinePowers.append(windSystem['nominalPower']['value'])
      if windSystem['type'] == 'Laboratory':
        windTurbineTypes.append(1)
      elif windSystem['type'] == 'Custom':
        windTurbineTypes.append(0)
        airDensity.append(windSystem['airDensity']['value'])
        rotorHeight.append(windSystem['rotorHeight']['value'])
        anemometerHeight.append(windSystem['anemometerHeight']['value'])
        ratedWindSpeed.append(windSystem['ratedWindSpeed']['value'])
        lowerCutoffWindSpeed.append(windSystem['lowerCutoffWindSpeed']['value'])
        upperCutoffWindSpeed.append(windSystem['upperCutoffWindSpeed']['value'])
        surfaceRoughnessLength.append(windSystem['surfaceRoughnessLength']['value'])

    loadNames = []
    loadTypes = []
    loadPowers = []

    for loadSystem in data['loadSystems']:
      loadNames.append(loadSystem['name'])
      loadTypes.append(loadSystem['informationMode'])
      if loadSystem['informationMode'] == 'Fixed':
        loadTypes.append(1)
        loadPowers.append(loadSystem['power']['value'])
      elif loadSystem['informationMode'] == 'Residential':
        loadTypes.append(2)
        loadPowers.append(loadSystem['peakPower']['value'])
      elif loadSystem['informationMode'] == 'Commercial':
        loadTypes.append(3)
        loadPowers.append(loadSystem['peakPower']['value'])
      elif loadSystem['informationMode'] == 'Industrial':
        loadTypes.append(4)
        loadPowers.append(loadSystem['peakPower']['value'])
      elif loadSystem['informationMode'] == 'Custom':
        loadTypes.append(0)
        loadPowers.append(loadSystem['powerArray']['value'])

    # biogasNames = ['Biogas_1','Biogas_2']

    # smartcity_model.resourcesDefinition(PV_Names = PV_Names, moduleNumbers = moduleNumbers, modulePowers = modulePowers, moduleTypes = moduleTypes, f_PV = deratingFactor, G_0 = testIrradiance, u_PM = temperatureVariationCoefficient, T_cSTC = testTemperature, T_cNOCT = nominalTemperature, T_aNOCT = operatingTemperature, G_NOCT = nominalIrradiance, n_c = efficiency, 
    #                         BESS_Names = BESS_Names, batteryTypes = batteryTypes, batteryEnergy = storageCapacity, chargePower_Max = maxChargePower, chargePower_Min = minChargePower, dischargePower_Max = maxDischargePower, dischargePower_Min = minDischargePower, gamma_sd = selfDischargeCoefficient, eta_bc = chargeEfficiency, eta_bd = dischargeEfficiency, 
    #                         hydroNames = hydroNames, turbineNumbers = turbineNumbers, turbinePowers = turbinePowers, turbineTypes = turbineTypes, n_t = efficiency, H_min = minimumWaterHead, H_max = maximumWaterHead, Q_min = minimumWaterFlow, Q_max = maximumWaterFlow, f_h = frictionLosses, 
    #                         WF_Names = windNames, windTurbineNumbers = windTurbineNumbers, windTurbinePowers = windTurbinePowers, windTurbineTypes = windTurbineTypes, H_R = rotorHeight, H_A = anemometerHeight, Z_0 = surfaceRoughnessLength, V_C = lowerCutoffWindSpeed, V_N = ratedWindSpeed, V_F = upperCutoffWindSpeed, 
    #                         biogasNames = , timestep = , days = , reactorVolume1 = , reactorVolume2 = , heightRelation1 = , heightRelation2 = , heatTransfer1 = , heatTransfer2 = , Tset1 = , tolerancia1 = , Tset2 = , tolerancia2 = , Cci = , Chi = , Coi = , Csi = , ST = , rho_sus = , Tin_sus = , Pin_sus = , vin_sus = , DeltaP = , Patm = , Tamb = , genEfficiency = , ratedPower = , 
    #                         demandNames = loadNames, demandTypes = loadTypes, demandPowersSet = loadPowers)

    # # Operación manual

    # irradiance = [(random.uniform(500,1000)) for i in range(simulationSteps)]
    # temperature = [(random.uniform(20,30)) for i in range(simulationSteps)]
    # head = [(random.uniform(20,30)) for i in range(simulationSteps)]
    # flux = [(random.uniform(0.003,0.01)) for i in range(simulationSteps)]
    # batcharge1 = [(random.uniform(0,5)) for i in range(simulationSteps)]
    # batcharge2 = [(random.uniform(0,50)) for i in range(simulationSteps)]
    # batcharge3 = [(random.uniform(0,50)) for i in range(simulationSteps)]
    # batdischarge1 = [(random.uniform(0,5)) for i in range(simulationSteps)]
    # batdischarge2 = [(random.uniform(0,50)) for i in range(simulationSteps)]
    # batdischarge3 = [(random.uniform(0,50)) for i in range(simulationSteps)]
    # wind = [(random.uniform(5,12)) for i in range(simulationSteps)]
    # weights = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 3.0, 4.0, 1.0, 1.0, 1.0, 2.0, 3.0, 5.0]

    # 'solarSystems': ['informationMode': 'Fixed', 'radiation': {'disabled': False, 'value': 800, 'tooltip': 'Irradiancia solar', 'unit': 'W / m²', 'variableString': 'Irradiancia solar', 'min': 0, 'max': 1500, 'step': 100}, 'temperature': {'disabled': False, 'value': 25, 'tooltip': 'Temperatura ambiente', 'unit': '°C', 'variableString': 'Temperatura ambiente', 'min': -10, 'max': 50}, 'radiationArray': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'temperatureArray': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    # 'batterySystems': ['informationMode': 'Fixed', 'chargePowerArray': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'dischargePowerArray': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}],
    # 'hydraulicSystems': ['informationMode': 'Fixed', 'waterHeadArray': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'waterFlowArray': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}],
    # 'windSystems': ['informationMode': 'Fixed', 'windSpeedArray': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Results_df = smartcity_model.operation(PV_MeteorologicalDataType=0, temperature=temperature, irradiance=irradiance, 
    #               BESS_OperativeDataType=0, initialSOC=[50,50,50], chargePower=[batcharge1,batcharge2,batcharge3], dischargePower= [batdischarge1,batdischarge2,batdischarge3], 
    #               hydroOperativeDataType=0, head=[head,head,head], flux=[flux,flux,flux], 
    #               WF_MeteorologicalDataType=0, airDensity = 1.112, windSpeed=[wind,wind,wind],
    #               weights = weights)

    # Results = Results_df.to_json(orient='split')

    response = {}
    return response