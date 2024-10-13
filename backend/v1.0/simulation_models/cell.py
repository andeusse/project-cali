from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import least_squares
import numpy as np
import random

class TwinCell:
    def __init__(self, systemName):
        self.systemName = systemName # Nombre del sistema
    
    # Parametrizacion de gemelo 
    def twinParameters (self):
        self.n_converter = 0.9

    def optimal_n_converter(self, cellSelfFeedingPower_meas, lightsPower_meas, cellPower_meas, electronicLoadPower_meas):
        if cellSelfFeedingPower_meas + lightsPower_meas > 0:
            def converterPower(n_converter, cellSelfFeedingPower, lightsPower, cellPower, electronicLoadPower):
                return cellPower - electronicLoadPower - (cellSelfFeedingPower + lightsPower) / n_converter
            n_converter_0 = 0.9
            n_converter = least_squares(converterPower, x0 = n_converter_0, bounds = (0.5, 0.99), args = (cellSelfFeedingPower_meas, lightsPower_meas, cellPower_meas, electronicLoadPower_meas))
            self.n_converter = n_converter.x[0]
            return n_converter.x[0]
        else:
            self.n_converter = 0.9
            return self.n_converter
        
    def twinOutput(self, previousCellVoltage, inputFanPercentage, electronicLoadMode, inputElectronicLoad, lightsPower, cellSelfFeedingPower, previousGeneratedEnergy, delta_t):
        
        self.cellSelfFeedingPower = cellSelfFeedingPower
        self.lightsPower = lightsPower

        if electronicLoadMode == "Current":
          self.electronicLoadCurrent = inputElectronicLoad
        elif electronicLoadMode == "Power":
          self.electronicLoadCurrent = inputElectronicLoad / previousCellVoltage
        elif electronicLoadMode == "Resistance":
          if inputElectronicLoad < 2.0: inputElectronicLoad = 2.0
          self.electronicLoadCurrent = previousCellVoltage / inputElectronicLoad

        self.cellCurrent = self.electronicLoadCurrent + ((cellSelfFeedingPower + lightsPower) / self.n_converter) / previousCellVoltage
        
        # if inputCellTemperature >= 41.0:
        #     voltageDrop = 0.07*self.cellCurrent**2 - 0.03*self.cellCurrent + 0.01
        # elif inputCellTemperature >= 37.0:
        #     voltageDrop = 0.05*self.cellCurrent**2 - 0.01*self.cellCurrent + 0.04
        # else:
        #     voltageDrop = 0.16331836*self.cellCurrent - 0.05462165
        
        # self.cellVoltage = 0.0128870679*self.cellCurrent**6 - 0.220519195*self.cellCurrent**5 + 1.48692377*self.cellCurrent**4 - 5.03979764*self.cellCurrent**3 + 9.11309881*self.cellCurrent**2 - 10.1063984*self.cellCurrent + 16.650003 - voltageDrop*(inputCellTemperature - 32.0)
        if inputFanPercentage < 100:
            self.cellVoltage = 16.9 - 13.2672427*self.cellCurrent + 13.5756291*self.cellCurrent**2 - 6.66323789*self.cellCurrent**3 + 1.21415288*self.cellCurrent**4 - 0.0005*self.cellCurrent**5 - 0.016*self.cellCurrent**6 - 0.0111392658*inputFanPercentage + 0.00015*inputFanPercentage**2
        else:
            self.cellVoltage = 16.8 - 12.55529151*self.cellCurrent + 13.2196722*self.cellCurrent**2 - 7.84413473*self.cellCurrent**3 + 2.40358984*self.cellCurrent**4 - 0.36143254*self.cellCurrent**5 - 0.02101814*self.cellCurrent**6
        
        if self.cellVoltage <= 5.8:
            self.cellCurrent = 0.0
            self.cellVoltage = 5.8
            self.electronicLoadCurrent = 0.0
            self.cellSelfFeedingPower = 0.0
            self.lightsPower = 0.0
        self.cellPower = self.cellCurrent * self.cellVoltage
        self.hydrogenFlow = 0.63173435*self.cellCurrent**5 - 4.45717449*self.cellCurrent**4 + 8.93813509*self.cellCurrent**3 - 1.38222392*self.cellCurrent**2 + 145.33329002*self.cellCurrent + 11.05591085
        # standardHydrogenFlow = (273.15 / 101325) * ((101325 + 34473.8) * self.hydrogenFlow) / (inputCellTemperature + 273.15)
        standardHydrogenFlow = (273.15 / 101325) * ((101325 + 34473.8) * self.hydrogenFlow) / (40.0 + 273.15)
        self.cellEfficiency = 100 * ((self.cellPower * 60) / (10.8 * standardHydrogenFlow))

        self.electronicLoadVoltage = self.cellVoltage
        self.electronicLoadPower = self.electronicLoadCurrent * self.electronicLoadVoltage

        self.cellGeneratedEnergy = (previousGeneratedEnergy + 1000 * self.cellPower * delta_t / 3600)
        
        return round(self.hydrogenFlow,2), round(self.cellCurrent,2), round(self.cellVoltage,3), round(self.cellPower,2), round(self.electronicLoadVoltage,2), round(self.electronicLoadCurrent,2), round(self.electronicLoadPower,2), round(self.cellEfficiency,1), round(self.cellGeneratedEnergy,2), round(self.n_converter*100,1), round(self.cellSelfFeedingPower,2), round(self.lightsPower,2)
