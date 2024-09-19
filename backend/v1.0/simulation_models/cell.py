from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import least_squares
from simulation_models.CoolingTower import CoolingTower

class TwinCell:
    def __init__(self, systemName):
        self.systemName = systemName # Nombre del sistema

    # Parametrizacion de turbinas de acuerdo a tipo
    def lightsPower(self, lightsMode, lightsConnected):
        if lightsConnected:
            # Encendido luces en serie
            if lightsMode == 'Parallel':
                self.lightsPower = 9.0
            # Encendido luces en paralelo
            elif lightsMode == 'Series':
                self.lightsPower = 3.0
        else:
            self.lightsPower = 0.0
    
    # Parametrizacion de gemelo 
    def twinParameters (self):
        a = 1
        
    def twinOutput(self, inputCellTemperature, inputElectronicLoadCurrent, cellSelfFeeding, previousGeneratedEnergy, delta_t):
        
        if cellSelfFeeding:
            self.cellSelfFeedingPower = 6.0
        else:
            self.cellSelfFeedingPower = 0.0

        self.cellCurrent = inputElectronicLoadCurrent
        self.hydrogenFlow = 0.63173435*self.cellCurrent^5 - 4.45717449*self.cellCurrent^4 + 8.93813509*self.cellCurrent^3 - 1.38222392*self.cellCurrent^2 + 145.33329002*self.cellCurrent + 11.05591085
        
        if inputCellTemperature >= 41:
            voltageDrop = 0.07*self.cellCurrent^2 - 0.03*self.cellCurrent + 0.01
        elif inputCellTemperature >= 37:
            voltageDrop = 0.05*self.cellCurrent^2 - 0.01*self.cellCurrent + 0.04
        else:
            voltageDrop = 0.16331836*self.cellCurrent - 0.05462165
        
        self.cellVoltage = 0.0128870679*self.cellCurrent^6 - 0.220519195*self.cellCurrent^5 + 1.48692377*self.cellCurrent^4 - 5.03979764*self.cellCurrent^3 + 9.11309881*self.cellCurrent^2 - 10.1063984*self.cellCurrent + 16.650003 - voltageDrop*(inputCellTemperature - 32)
        self.cellPower = self.cellCurrent * self.cellVoltage
        standardHydrogenFlow = (273.15 / 14.6959) * ((14.6959 + 5) * self.hydrogenFlow) / (inputCellTemperature + 273.15)
        self.cellEfficiency = 100 * ((self.cellPower * 60) / (10.8 * standardHydrogenFlow))

        self.electronicLoadVoltage = self.cellVoltage
        self.electronicLoadPower = inputElectronicLoadCurrent * self.electronicLoadVoltage

        self.cellGeneratedEnergy = 1000 + (previousGeneratedEnergy + self.cellPower * delta_t / 3600)
        
        return round(self.hydrogenFlow,2), round(self.cellCurrent,2), round(self.cellVoltage,2), round(self.cellPower,2), round(self.electronicLoadVoltage,2), round(self.electronicLoadPower,2), round(self.cellSelfFeedingPower,2), round(self.lightsPower,2), round(self.cellEfficiency,1), round(self.cellGeneratedEnergy,2)