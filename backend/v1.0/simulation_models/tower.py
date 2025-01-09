from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import least_squares
from simulation_models.CoolingTower import CoolingTower
import random

class TwinTower:
    def __init__(self, systemName):
        self.systemName = systemName # Nombre del sistema
    
    # Parametrizacion de gemelo 
    def twinParameters (self, waterCorrectionFactor, airCorrectionFactor, humidityCorrectionFactor):
        self.waterCorrectionFactor = waterCorrectionFactor
        self.airCorrectionFactor = airCorrectionFactor
        self.humidityCorrectionFactor = humidityCorrectionFactor
        self.towerArea = 0.0225 # Area transversal de la torre en metros cuadrados
        self.towerHeight = 0.580 # Altura de la torre en metros
        # self.waterCorrectionFactor = 1.0
        # self.airCorrectionFactor = 1.0
    
    def optimal_waterOutput(self, bottomWaterTemperature_meas):
        def optimal_waterTemperatureOutput(waterCorrectionFactor, bottomWaterTemperature_meas):
            self.waterCorrectionFactor = waterCorrectionFactor[0]
            return self.waterCorrectionFactor * (self.bottomWaterTemperature - 273.15) - bottomWaterTemperature_meas
        waterCorrectionFactor_0 = 1.0
        waterCorrectionFactor = least_squares(optimal_waterTemperatureOutput, x0 = waterCorrectionFactor_0, bounds = (0.1, 2.0), args = [bottomWaterTemperature_meas])
        self.waterCorrectionFactor = waterCorrectionFactor.x[0]*random.uniform(0.98,1.02)
        return waterCorrectionFactor.x[0]
    
    def optimal_airOutput(self, topAirTemperature_meas):
        def optimal_airTemperatureOutput(airCorrectionFactor, topAirTemperature_meas):
            self.airCorrectionFactor = airCorrectionFactor[0]
            return self.airCorrectionFactor * (self.topAirTemperature - 273.15) - topAirTemperature_meas
        airCorrectionFactor_0 = 1.0
        airCorrectionFactor = least_squares(optimal_airTemperatureOutput, x0 = airCorrectionFactor_0, bounds = (0.1, 2.0), args = [topAirTemperature_meas])
        self.airCorrectionFactor = airCorrectionFactor.x[0]*random.uniform(0.98,1.02)
        return airCorrectionFactor.x[0]
    
    def optimal_humidityOutput(self, topAirHumidity_meas):
        def optimal_airHumidityOutput(humidityCorrectionFactor, topAirHumidity_meas):
            self.humidityCorrectionFactor = humidityCorrectionFactor[0]
            return self.humidityCorrectionFactor * self.topAirHumidity - topAirHumidity_meas
        humidityCorrectionFactor_0 = 1.0
        humidityCorrectionFactor = least_squares(optimal_airHumidityOutput, x0 = humidityCorrectionFactor_0, bounds = (0.1, 2.0), args = [topAirHumidity_meas])
        self.humidityCorrectionFactor = humidityCorrectionFactor.x[0]*random.uniform(0.98,1.02)
        return humidityCorrectionFactor.x[0]
    
    def twinOutput(self, PackedType, topWaterFlow, topWaterTemperature, bottomAirFlow, bottomAirTemperature, bottomAirHumidity, atmosphericPressure, previousEnergyApplied, delta_t):
        if topWaterFlow <= 1.6e-6:
            topWaterFlow = 1.6e-6
        self.topWaterFlow = topWaterFlow
        self.topWaterTemperature = topWaterTemperature
        self.bottomAirFlow = bottomAirFlow
        self.bottomAirTemperature = bottomAirTemperature
        self.bottomAirHumidity = bottomAirHumidity
        self.atmosphericPressure = atmosphericPressure

        towerModel = CoolingTower.coolingTowerModel(PackedType =  PackedType, L = self.towerHeight, A = self.towerArea)
        towerModel.towerBalance(self.topWaterTemperature, self.atmosphericPressure, self.topWaterFlow, self.bottomAirTemperature, self.bottomAirFlow, self.bottomAirHumidity)
        towerResults = towerModel.solution

        self.bottomWaterTemperature = self.waterCorrectionFactor * (towerResults[5] - 273.15) + 273.15
        self.topAirTemperature = self.airCorrectionFactor * (towerResults[6] - 273.15) + 273.15
        self.topAirHumidity = self.humidityCorrectionFactor * (towerResults[7] * 100)
        self.powerAppliedToWater = towerResults[8] / 1000
        self.deltaPressure = towerResults[9]
        self.energyAppliedToWater = previousEnergyApplied + self.powerAppliedToWater * delta_t / 3600

        self.waterTemperatureReduction = self.bottomWaterTemperature - self.topWaterTemperature
        self.airTemperatureRise = self.topAirTemperature - self.bottomAirTemperature

        return round(self.bottomWaterTemperature,2), round(self.waterTemperatureReduction,2), round(self.topAirTemperature,2), round(self.topAirHumidity,2), round(self.airTemperatureRise,2), round(self.powerAppliedToWater,2), self.energyAppliedToWater, round(self.deltaPressure,2)
