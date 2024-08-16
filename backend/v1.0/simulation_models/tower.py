from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import least_squares
from simulation_models.CoolingTower import CoolingTower

class TwinTower:
    def __init__(self, systemName):
        self.systemName = systemName # Nombre del sistema

    # Parametrizacion de turbinas de acuerdo a tipo
    def fillType(self, type):
        # Listones planos
        if type == 'FlatSlats':
            self.fillDensity = 16 # Densidad de relleno del empaque
        # Listones curvos
        elif type == 'CurvedSlats':
            self.fillDensity = 25 # Densidad de relleno del empaque
        # Estructurado
        elif type == 'Structured':
            self.fillDensity = 226 # Densidad de relleno del empaque
        return self.fillDensity
    
    # Parametrizacion de gemelo 
    def twinParameters (self):
        self.towerArea = 0.0225 # Area transversal de la torre en metros
        self.towerHeight = 0.580 # Altura de la torre en metros
    
    # def optimal_n_t(self, n_t, P_h_meas, Pressure, Flux):
    #     def turbinePowerOutput(n_t, P_h_meas, Pressure, Flux):      
    #         return ((n_t/100) * Pressure * Flux) - P_h_meas
    #     n_t_0 = n_t
    #     n_t = least_squares(turbinePowerOutput, x0 = n_t_0, bounds = (30, 90), args = (P_h_meas, Pressure, Flux))
    #     self.n_t = n_t.x[0]*random.uniform(0.98,1.02)
    #     return n_t.x[0]
    
    def twinOutput(self, topWaterFlow, topWaterTemperature, oldBottomWaterTemperature, bottomAirFlow, bottomAirTemperature, bottomAirHumidity, atmosphericPressure):
        self.topWaterFlow = topWaterFlow
        self.topWaterTemperature = topWaterTemperature
        self.oldBottomWaterTemperature = oldBottomWaterTemperature
        self.bottomAirFlow = bottomAirFlow
        self.bottomAirTemperature = bottomAirTemperature
        self.bottomAirHumidity = bottomAirHumidity
        self.atmosphericPressure = atmosphericPressure
        epsilon = 0.8
        dp = 0.005

        towerModel = CoolingTower.coolingTowerModel(self.towerHeight, self.towerArea, epsilon, dp)
        towerModel.towerBalance(self.topWaterTemperature, self.atmosphericPressure, self.topWaterFlow, self.bottomAirTemperature, self.bottomAirFlow, self.bottomAirHumidity)
        towerResults = towerModel.solution

        self.bottomWaterTemperature = towerResults[6]
        self.topAirTemperature = towerResults[6]
        
        self.topAirHumidity = self.bottomAirHumidity
        
        self.energyAppliedToWater = self.topWaterTemperature - self.oldBottomWaterTemperature

        self.waterTemperatureReduction = self.bottomWaterTemperature - self.topWaterTemperature
        self.airTemperatureRise = self.topAirTemperature - self.bottomAirTemperature

        return round(self.bottomWaterTemperature,2), round(self.waterTemperatureReduction,2), round(self.topAirTemperature,2), round(self.topAirHumidity,2), round(self.airTemperatureRise), round(self.energyAppliedToWater)