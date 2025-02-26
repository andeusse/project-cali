from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import least_squares
import numpy as np
import random

class TwinCell:
    def __init__(self, systemName):
        self.systemName = systemName # Nombre del sistema
    
    # Parametrizacion de gemelo 
    def twinParameters (self,converterEfficiency, voltageCoefficient, flowCoefficients):
        self.n_converter = converterEfficiency
        self.voltageCoefficient = voltageCoefficient
        self.flowCoefficients = flowCoefficients
    
    def optimal_voltageCoefficients(self, cellVoltage_meas, cellCurrent_meas, inputFanPercentage):
        # def cellVoltage(voltageCoefficients, cellVoltage_meas, cellCurrent_meas, inputFanPercentage):
        #     return cellVoltage_meas - (voltageCoefficients[0]*17.2 - voltageCoefficients[1]*12.55529151*cellCurrent_meas + voltageCoefficients[2]*13.2196722*cellCurrent_meas**2 - voltageCoefficients[3]*7.84413473*cellCurrent_meas**3 + voltageCoefficients[4]*2.40358984*cellCurrent_meas**4 - voltageCoefficients[5]*0.3615*cellCurrent_meas**5 + 0.02106*cellCurrent_meas**6 - voltageCoefficients[6]*0.1*inputFanPercentage + voltageCoefficients[7]*0.001066*inputFanPercentage**2)
        # voltageCoefficients_0 = (1,) * 8
        # voltageCoefficients = least_squares(cellVoltage, x0 = voltageCoefficients_0, bounds = ([-10] * 8, [10] * 8), args = (cellVoltage_meas, cellCurrent_meas, inputFanPercentage))
        # self.voltageCoefficients = voltageCoefficients.x
        # return self.voltageCoefficients
        def cellVoltage(voltageCoefficient, cellVoltage_meas, cellCurrent_meas, inputFanPercentage):
            return cellVoltage_meas - (0.0725*cellCurrent_meas**6 - 1.0604*cellCurrent_meas**5 + 6.0632*cellCurrent_meas**4 - 17.22*cellCurrent_meas**3 + 25.516*cellCurrent_meas**2 - voltageCoefficient*21.223*cellCurrent_meas + 16.4 + 0.01*inputFanPercentage)
        voltageCoefficient_0 = 1.0
        voltageCoefficient = least_squares(cellVoltage, x0 = voltageCoefficient_0, bounds = (0.5,1.5), args = (cellVoltage_meas, cellCurrent_meas, inputFanPercentage))
        self.voltageCoefficient = voltageCoefficient.x[0]
        return self.voltageCoefficient
    
    def optimal_flowCoefficients(self, hydrogenFlow_meas, cellCurrent_meas):
        def hydrogenFlow(flowCoefficients, hydrogenFlow_meas, cellCurrent_meas):
            return hydrogenFlow_meas - (151.29*cellCurrent_meas + 23.533 + flowCoefficients)
        flowCoefficients_0 = 0.0
        flowCoefficients = least_squares(hydrogenFlow, x0 = flowCoefficients_0, bounds = (-100.0, 100.0), args = (hydrogenFlow_meas, cellCurrent_meas))
        self.flowCoefficients = flowCoefficients.x[0]
        return self.flowCoefficients

    def optimal_n_converter(self, cellSelfFeedingPower_meas, lightsPower_meas, cellPower_meas, electronicLoadPower_meas):
        if cellSelfFeedingPower_meas + lightsPower_meas > 0:
            def converterPower(n_converter, cellSelfFeedingPower, lightsPower, cellPower, electronicLoadPower):
                return cellPower - electronicLoadPower - (cellSelfFeedingPower + lightsPower) / n_converter
            n_converter_0 = 0.9
            n_converter = least_squares(converterPower, x0 = n_converter_0, bounds = (0, 1.2), args = (cellSelfFeedingPower_meas, lightsPower_meas, cellPower_meas, electronicLoadPower_meas))
            self.n_converter = n_converter.x[0]
            return n_converter.x[0]
        
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
        
        # if inputFanPercentage < 90:
        #     self.cellVoltage = 16.9 - 13.2672427*self.cellCurrent + 13.5756291*self.cellCurrent**2 - 6.66323789*self.cellCurrent**3 + 1.21415288*self.cellCurrent**4 - 0.0005*self.cellCurrent**5 - 0.0155*self.cellCurrent**6 - 0.0111392658*inputFanPercentage + 0.00015*inputFanPercentage**2
        # else:
        # self.cellVoltage = self.voltageCoefficients[0]*17.2 - self.voltageCoefficients[1]*12.55529151*self.cellCurrent + self.voltageCoefficients[2]*13.23*self.cellCurrent**2 - self.voltageCoefficients[3]*7.84413473*self.cellCurrent**3 + self.voltageCoefficients[4]*2.40358984*self.cellCurrent**4 - self.voltageCoefficients[5]*0.3615*self.cellCurrent**5 + 0.02106*self.cellCurrent**6 - self.voltageCoefficients[6]*0.1*inputFanPercentage + self.voltageCoefficients[7]*0.001066*inputFanPercentage**2
        
        # self.cellVoltage = 17.2 - 16.5*self.cellCurrent + 14.15*self.cellCurrent**2 - 7.79*self.cellCurrent**3 + 2.374*self.cellCurrent**4 - 0.3615*self.cellCurrent**5 + 0.02105*self.cellCurrent**6 + 0.007*inputFanPercentage

        self.cellVoltage = 0.0725*self.cellCurrent**6 - 1.0604*self.cellCurrent**5 + 6.0632*self.cellCurrent**4 - 17.22*self.cellCurrent**3 + 25.516*self.cellCurrent**2 - self.voltageCoefficient*21.223*self.cellCurrent + 16.4 + 0.01*inputFanPercentage

        if self.cellVoltage <= 5.5 or self.cellCurrent > 4.5:
            self.cellCurrent = 0.0
            self.cellVoltage = 5.5
            self.electronicLoadCurrent = 0.0
            self.cellSelfFeedingPower = 0.0
            self.lightsPower = 0.0
        
        self.cellPower = self.cellCurrent * self.cellVoltage
        # self.hydrogenFlow = self.flowCoefficients[0]*0.63173435*self.cellCurrent**5 - self.flowCoefficients[1]*4.45717449*self.cellCurrent**4 + self.flowCoefficients[2]*8.93813509*self.cellCurrent**3 - self.flowCoefficients[3]*1.38222392*self.cellCurrent**2 + self.flowCoefficients[4]*145.33329002*self.cellCurrent + self.flowCoefficients[5]*11.05591085
        self.hydrogenFlow = 151.29*self.cellCurrent + 23.533 + self.flowCoefficients
        # standardHydrogenFlow = (273.15 / 101325) * ((101325 + 127553) * self.hydrogenFlow) / (35.0 + 273.15)
        standardHydrogenFlow = self.hydrogenFlow
        self.cellEfficiency = 100 * ((self.cellPower * 60) / (10.8 * standardHydrogenFlow))

        self.electronicLoadVoltage = self.cellVoltage
        self.electronicLoadPower = self.electronicLoadCurrent * self.electronicLoadVoltage

        self.cellGeneratedEnergy = (previousGeneratedEnergy + self.cellPower * delta_t / 3600)
        
        return self.hydrogenFlow, self.cellCurrent, self.cellVoltage, self.cellPower, self.electronicLoadVoltage, self.electronicLoadCurrent, self.electronicLoadPower, self.cellEfficiency, self.cellGeneratedEnergy, self.n_converter*100, self.cellSelfFeedingPower, self.lightsPower
