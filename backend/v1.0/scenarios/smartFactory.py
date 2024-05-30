from flask import request
from flask_restful import Resource
from simulation_models.Scenarios_models import Smartfactory

class SmartFactory(Resource):
  def post(self):
    data = request.get_json()
    # print(data)

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

    loadSystemNumber = data['loadSystemNumber']['value']

    smartfactory_model = Smartfactory.Smartfactory(N_PV=solarSystemNumber, N_Biogas=biogasSystemNumber, N_Demand=loadSystemNumber,
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
    informationMode = []
    radiations = []
    temperatures = []

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
      
      if solarSystem['informationMode'] == 'Fixed':
        informationMode.append(1)
        radiations.append([solarSystem['radiation']['value']])
        temperatures.append([solarSystem['temperature']['value']])
      elif solarSystem['informationMode'] == 'Typical':
        informationMode.append(2)
        radiations.append([solarSystem['radiation']['value']])
        temperatures.append([solarSystem['temperature']['value']])
      elif solarSystem['informationMode'] == 'Custom':
        informationMode.append(0)
        radiations.append(solarSystem['radiationArray'])
        temperatures.append(solarSystem['temperatureArray'])

    loadNames = []
    loadTypes = []
    loadPowers = []

    for loadSystem in data['loadSystems']:
      loadNames.append(loadSystem['name'])
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
        loadPowers.append(loadSystem['powerArray'])

    biogasNames = []
    stabilizationDays = []
    ambientPressure = []
    ambientTemperature = []
    electricGeneratorPower = []
    electricGeneratorEfficiency = []
    reactorVolume1 = []
    reactorVolume2 = []
    diameterHeightRatio1 = []
    diameterHeightRatio2 = []
    heatTransferCoefficient1 = []
    heatTransferCoefficient2 = []
    temperatureSetpoint1 = []
    temperatureSetpoint2 = []
    controllerTolerance1 = []
    controllerTolerance2 = []
    carbonConcentration = []
    hydrogenConcentration = []
    oxygenConcentration = []
    sulfurConcentration = []
    totalConcentration = []
    substrateDensity = []
    substrateTemperature = []
    substratePressure = []
    substrateFlow = []
    substratePresurreDrop = []

    for biogasSystem in data['biogasSystems']:
      biogasNames.append(biogasSystem['name'])
      stabilizationDays.append(biogasSystem['stabilizationDays']['value'])
      ambientPressure.append(biogasSystem['ambientPressure']['value'])
      ambientTemperature.append(biogasSystem['ambientTemperature']['value'])
      electricGeneratorPower.append(biogasSystem['electricGeneratorPower']['value'])
      electricGeneratorEfficiency.append(biogasSystem['electricGeneratorEfficiency']['value'])
      reactorVolume1.append(biogasSystem['reactorVolume1']['value'])
      reactorVolume2.append(biogasSystem['reactorVolume2']['value'])
      diameterHeightRatio1.append(biogasSystem['diameterHeightRatio1']['value'])
      diameterHeightRatio2.append(biogasSystem['diameterHeightRatio2']['value'])
      heatTransferCoefficient1.append(biogasSystem['heatTransferCoefficient1']['value'])
      heatTransferCoefficient2.append(biogasSystem['heatTransferCoefficient2']['value'])
      temperatureSetpoint1.append(biogasSystem['temperatureSetpoint1']['value'])
      temperatureSetpoint2.append(biogasSystem['temperatureSetpoint2']['value'])
      controllerTolerance1.append(biogasSystem['controllerTolerance1']['value'])
      controllerTolerance2.append(biogasSystem['controllerTolerance2']['value'])
      carbonConcentration.append(biogasSystem['carbonConcentration']['value']/100)
      hydrogenConcentration.append(biogasSystem['hydrogenConcentration']['value']/100)
      oxygenConcentration.append(biogasSystem['oxygenConcentration']['value']/100)
      sulfurConcentration.append(biogasSystem['sulfurConcentration']['value']/100)
      totalConcentration.append(biogasSystem['totalConcentration']['value']/100)
      substrateDensity.append(biogasSystem['substrateDensity']['value'])
      substrateTemperature.append(biogasSystem['substrateTemperature']['value'])
      substratePressure.append(biogasSystem['substratePressure']['value'])
      substrateFlow.append(biogasSystem['substrateFlow']['value'])
      substratePresurreDrop.append(biogasSystem['substratePresurreDrop']['value'])

    smartfactory_model.resourcesDefinition(PV_Names = PV_Names, moduleNumbers = moduleNumbers, modulePowers = modulePowers, moduleTypes = moduleTypes, f_PV = deratingFactor, G_0 = testIrradiance, u_PM = temperatureVariationCoefficient, T_cSTC = testTemperature, T_cNOCT = nominalTemperature, T_aNOCT = operatingTemperature, G_NOCT = nominalIrradiance, n_c = efficiency, 
                                           biogasNames = biogasNames, timestep = 1, days = stabilizationDays, reactorVolume1 = reactorVolume1, reactorVolume2 = reactorVolume2, heightRelation1 = diameterHeightRatio1, heightRelation2 = diameterHeightRatio2, heatTransfer1 = heatTransferCoefficient1, heatTransfer2 = heatTransferCoefficient2, Tset1 = temperatureSetpoint1, tolerancia1 = controllerTolerance1, Tset2 = temperatureSetpoint2, tolerancia2 = controllerTolerance2, Cci = carbonConcentration, Chi = hydrogenConcentration, Coi = oxygenConcentration, Csi = sulfurConcentration, ST = totalConcentration, rho_sus = substrateDensity, Tin_sus = substrateTemperature, Pin_sus = substratePressure, vin_sus = substrateFlow, DeltaP = substratePresurreDrop, Patm = ambientPressure, Tamb = ambientTemperature, genEfficiency = electricGeneratorEfficiency, ratedPower = electricGeneratorPower, 
                                           demandNames = loadNames, demandTypes = loadTypes, demandPowersSet = loadPowers)

    idList = []
    weightList = []
    for item in data['priorityList']:
      idList.append(item['id'])
    for system in data['solarSystems']:
      id = system['id']
      weightList.append(idList.index(id))
    for system in data['biogasSystems']:
      id = system['id']
      weightList.append(idList.index(id))
    weightList.append(len(data['priorityList']))

    # print(weightList)
    results_df = smartfactory_model.operation(PV_MeteorologicalDataType = informationMode, temperature = temperatures, irradiance = radiations, 
                                              weights = weightList)

    results_df = results_df.reindex(sorted(results_df.columns), axis=1)

    response = results_df.to_json(orient='split')
    # print(response)

    return response