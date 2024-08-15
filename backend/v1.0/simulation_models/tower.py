from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import least_squares
from simulation_models.Biogas import ThermoProperties as TP

class CoolingTower:
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
        self.towerHeight = 0.645 # Altura de la torre en metros
    
    # # Calculo de potencia de las turbinas
    # def PowerOutput (self, Pressure, Flux):
    #     self.Press = Pressure
    #     self.Q = Flux
    #     #Calculo de potencia de la turbina kW
    #     self.P_h = ((self.n_t/100) * self.Press * self.Q * (1 - (self.f_h/100)))

    #     return self.P_h
        
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

        self.bottomWaterTemperature = self.topWaterTemperature

        self.topAirTemperature = self.bottomAirTemperature
        
        self.topAirHumidity = self.bottomAirHumidity
        
        self.energyAppliedToWater = self.topWaterTemperature - self.oldBottomWaterTemperature

        self.waterTemperatureReduction = self.topWaterTemperature - self.bottomWaterTemperature
        self.airTemperatureRise = self.topAirTemperature - self.bottomAirTemperature

        return round(self.bottomWaterTemperature,2), round(self.waterTemperatureReduction,2), round(self.topAirTemperature,2), round(self.topAirHumidity,2), round(self.airTemperatureRise), round(self.energyAppliedToWater)