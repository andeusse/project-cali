from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import least_squares
from simulation_models.CoolingTower import CoolingTower

class TwinTower:
    def __init__(self, systemName):
        self.systemName = systemName # Nombre del sistema
    
    # Parametrizacion de gemelo 
    def twinParameters (self):
        self.towerArea = 0.0225 # Area transversal de la torre en metros
        self.towerHeight = 0.580 # Altura de la torre en metros
    
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

        self.bottomWaterTemperature = towerResults[5]
        self.topAirTemperature = towerResults[6]
        self.topAirHumidity = towerResults[7] * 100
        self.powerAppliedToWater = towerResults[8] / 1000
        self.deltaPressure = towerResults[9]
        self.energyAppliedToWater = previousEnergyApplied + self.powerAppliedToWater * delta_t / 3600

        self.waterTemperatureReduction = self.bottomWaterTemperature - self.topWaterTemperature
        self.airTemperatureRise = self.topAirTemperature - self.bottomAirTemperature

        return round(self.bottomWaterTemperature,2), round(self.waterTemperatureReduction,2), round(self.topAirTemperature,2), round(self.topAirHumidity,2), round(self.airTemperatureRise,2), round(self.powerAppliedToWater,2), self.energyAppliedToWater, round(self.deltaPressure,2)