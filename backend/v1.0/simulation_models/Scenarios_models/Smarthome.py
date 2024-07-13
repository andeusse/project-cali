from simulation_models.Scenarios_models import Scenary
import pandas as pd

class Smarthome:
    def __init__(self, N_PV=0, N_BESS=0, N_Biogas=0, N_Demand=1, operationType=1, simulationSteps=24, stepTime=1): # Ingresan parámetros de número de elementos, tipo de operación (1=Manual, 2=Auto) y pasos de simulación
        self.N_PV = N_PV # Número de generadores fotovoltaicos (PV)
        self.N_Biogas = N_Biogas # Número de generadores biogas
        self.N_Hydro = 0 # Número de generadores hidráulicos (Hydro)
        self.N_WF = 0 # Número de generadores eólicos (WF)
        self.N_BESS = N_BESS # Número de sistemas de baterías (BESS)
        self.N_Demand = N_Demand # Número de elementos de demanda
        self.operationType = operationType # Tipo de operación del escenario (1=Manual, 2=Auto)
        self.simulationSteps = simulationSteps # Pasos de simulación del escenario
        self.stepTime = stepTime
        
        self.scenary = Scenary.Scenary_Model(self.N_PV, self.N_BESS, self.N_Hydro, self.N_WF, self.N_Biogas, self.N_Demand, self.operationType, self.simulationSteps, self.stepTime)
        
    def resourcesDefinition(self, PV_Names = ['PV'], moduleNumbers = [0], modulePowers = [0.0], moduleTypes = [1], f_PV = [1.0], G_0 = [1000.0], u_PM = [-0.39], T_cSTC = [25.0], T_cNOCT = [45.0], T_aNOCT = [20.0], G_NOCT = [800.0], n_c = [15.44], 
                            BESS_Names = ['BESS'], batteryTypes = [1], batteryEnergy = [0.0], chargePower_Max = [0.0], chargePower_Min = [0.0], dischargePower_Max = [0.0], dischargePower_Min = [0.0], gamma_sd = [2.5], eta_bc = [98.0], eta_bd = [98.0], 
                            biogasNames = ['Biogas'], timestep=1, days=60, reactorVolume1=[30], reactorVolume2=[70], heightRelation1=[2], heightRelation2=[2], heatTransfer1=[0.05], heatTransfer2=[0.05], Tset1=[35], tolerancia1=[3], Tset2=[35], tolerancia2=[3], Cci=[0.4], Chi=[0.05], Coi=[0.2], Csi=[0.01], ST=[0.1], rho_sus=[998], Tin_sus=[20], Pin_sus=[350], vin_sus=[0.139], DeltaP=[5], Patm=[100], Tamb=[15], genEfficiency = [0.4], ratedPower = [10],
                            demandNames = ['Demand'], demandTypes=[2], demandPowersSet=[1.0]):
        
        self.scenary.PVElements(PV_Names, moduleNumbers, modulePowers, moduleTypes, f_PV, G_0, u_PM, T_cSTC, T_cNOCT, T_aNOCT, G_NOCT, n_c)
        self.scenary.BESSElements(BESS_Names, batteryTypes, batteryEnergy, chargePower_Max, chargePower_Min, dischargePower_Max, dischargePower_Min, gamma_sd, eta_bc, eta_bd)
        self.scenary.BiogasElements(biogasNames, timestep, days, reactorVolume1, reactorVolume2, heightRelation1, heightRelation2, heatTransfer1, heatTransfer2)
        self.scenary.BiogasParameters(Tset1, tolerancia1, Tset2, tolerancia2, Cci, Chi, Coi, Csi, ST, rho_sus, Tin_sus, Pin_sus, vin_sus, DeltaP, Patm, Tamb, genEfficiency, ratedPower)
        self.scenary.DemandElements(demandNames, demandTypes, demandPowersSet)
    
    def operation(self, PV_MeteorologicalDataType = 2, temperature = [25.0], irradiance = [1000.0], 
                  BESS_OperativeDataType = 0, initialSOC = [100.0], chargePower = [0.0], dischargePower = [0.0], 
                  biogasStages = [1],
                  weights = [0.0]):
    
        PVpower = self.scenary.PVGeneration(PV_MeteorologicalDataType, temperature, irradiance)
        BESS_SOC,chargeP,dischargeP = self.scenary.BESSSOC(BESS_OperativeDataType, initialSOC, chargePower, dischargePower)
        Biogaspower = self.scenary.BiogasGeneration(biogasStages)
        Demandpower = self.scenary.DemandPower()
        Gridpower = self.scenary.GridPower()
        
        # if self.operationType == 1:
        #     self.results_df = pd.concat([PVpower, BESS_SOC, chargeP, dischargeP, Biogaspower, Gridpower, Demandpower], axis = 1)
        #     if self.N_BESS > 0:    
        #         self.results_df.drop(index=self.results_df.index[-1],axis=0,inplace=True)
            
        if self.operationType == 1:
            if self.N_BESS > 0:
                self.results_df = pd.concat([PVpower, BESS_SOC, chargeP, dischargeP, Biogaspower, Gridpower, Demandpower], axis = 1)
                self.results_df.drop(index=self.results_df.index[-1],axis=0,inplace=True)
            else:
                self.results_df = pd.concat([PVpower, Biogaspower, Gridpower, Demandpower], axis = 1)   
        
        elif self.operationType == 2:
            self.results_df = self.scenary.AutomaticPowerCalculation(weights)[0]
            
        return self.results_df