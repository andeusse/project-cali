from simulation_models.Scenarios_systems import Scenary_BESS
from simulation_models.Scenarios_systems import BiogasModel as Scenary_BM
from simulation_models.Scenarios_systems import Scenary_Hydro
from simulation_models.Scenarios_systems import Scenary_PV
from simulation_models.Scenarios_systems import Scenary_WF
from simulation_models.Scenarios_systems import Scenary_Demand
from simulation_models.Scenarios_systems import Scenary_Optimizer
import pandas as pd

class Scenary_Model:
    # Inicializacion de variables del escenario
    def __init__(self, N_PV=0, N_BESS=0, N_Hydro=0, N_WF=0, N_Biogas=0, N_Demand=1, operationType=1, simulationSteps=24, stepTime = 1): # Ingresan parámetros de número de elementos, tipo de operación (1=Manual, 2=Auto) y pasos de simulación
        self.N_PV = N_PV # Número de generadores fotovoltaicos (PV)
        self.N_Biogas = N_Biogas # Número de generadores biogas
        self.N_Hydro = N_Hydro # Número de generadores hidráulicos (Hydro)
        self.N_WF = N_WF # Número de generadores eólicos (WF)
        self.N_BESS = N_BESS # Número de sistemas de baterías (BESS)
        self.N_Demand = N_Demand # Número de elementos de demanda
        self.operationType = operationType # Tipo de operación del escenario (1=Manual, 2=Auto)
        self.simulationSteps = simulationSteps # Pasos de simulación del escenario
        self.stepTime = stepTime # Equivalencia de tiempo en horas de cada paso de simulación (ejm. 0.1 = 6 minutos)
        self.T_Profile = [] # Perfil de temperatura ambiente
        self.G_Profile = [] # Perfil de irradiancia solar
        self.H_Profile = [] # Perfil de cabeza de agua
        self.Q_Profile = [] # Perfil de caudal de agua
        self.V_Profile = [] # Perfil de velocidad de viento
        self.PV_Elements = [] # Inicialización del objeto que contiene los modelos PV
        self.PV_Powers = pd.DataFrame() # Creación de dataframe para resultados de los modelos PV
        self.biogasElements = []# Inicialización del objeto que contiene los modelos Biogas
        self.biogasPowers = pd.DataFrame() # Creación de dataframe para resultados de los modelos Biogas
        self.hydroElements = [] # Inicialización del objeto que contiene los modelos Hydro
        self.hydroPowers = pd.DataFrame() # Creación de dataframe para resultados de los modelos Hydro
        self.WF_Elements = [] # Inicialización del objeto que contiene los modelos Wind Farm
        self.WF_Powers = pd.DataFrame() # Creación de dataframe para resultados de los modelos WF
        self.BESS_Elements = [] # Inicialización del objeto que contiene los modelos BESS
        self.BESS_SOC = pd.DataFrame() # Creación de dataframe para resultados de estado de carga (SOC) de los modelos BESS
        self.dischargePowers = pd.DataFrame() # Creación de dataframe para resultados de potencia de descarga de los modelos BESS
        self.chargePowers = pd.DataFrame() # Creación de dataframe para resultados de potencia de carga de los modelos BESS
        self.demandElements = [] # Inicialización del objeto que contiene los modelos Demanda
        self.demandPowers = pd.DataFrame() # Creación de dataframe para resultados de los modelos de demanda
        
        if self.N_PV == 0:
            self.PV_Powers = pd.DataFrame([0]*self.simulationSteps)
        
        if self.N_BESS == 0:
            self.BESS_SOC = pd.DataFrame([0]*self.simulationSteps)
            self.chargePowers = pd.DataFrame([0]*self.simulationSteps)
            self.dischargePowers = pd.DataFrame([0]*self.simulationSteps)
            self.BESS_PowerResults = pd.DataFrame([0]*self.simulationSteps)
            
        if self.N_Hydro == 0:
            self.hydroPowers = pd.DataFrame([0]*self.simulationSteps)
                
        if self.N_WF == 0:
            self.WF_Powers = pd.DataFrame([0]*self.simulationSteps)
            
        if self.N_Biogas == 0:
            self.biogasPowers = pd.DataFrame([0]*self.simulationSteps)
        
        if self.N_Demand == 0:
            self.demandPowers = pd.DataFrame([0]*self.simulationSteps)
    
    # Creación de los elementos PV con base en sus parámetros constructivos   
    def PVElements (self, PV_Names,moduleNumbers, modulePowers, moduleTypes, f_PV = [1.0], G_0 = [1000.0], u_PM = [-0.39], T_cSTC = [25.0], 
                    T_cNOCT = [45.0], T_aNOCT = [20.0], G_NOCT = [800.0], n_c = [15.44]):
        self.PV_Names = PV_Names
        
        j=0
        
        for i in range(self.N_PV):
            self.PV_Elements.append(Scenary_PV.PV_Model(self.simulationSteps, moduleNumbers[i], modulePowers[i], self.PV_Names[i]))
            if moduleTypes[i] == 0:
                self.PV_Elements[i].moduleType(moduleTypes[i], f_PV[j], G_0[j], u_PM[j], T_cSTC[j], T_cNOCT[j], T_aNOCT[j], G_NOCT[j], n_c[j])
                j+=1
            else:
                self.PV_Elements[i].moduleType(moduleTypes[i])
            
        return self.PV_Elements
    
    # Cálculo de potencia de los elementos PV con base en sus parámetros operativos        
    def PVGeneration (self, PV_MeteorologicalDataType, temperature = [25.0], irradiance = [1000.0]):
        self.PV_Powers = pd.DataFrame(columns = self.PV_Names)
        
        for i in range(self.N_PV):
            self.T_Profile.append(self.PV_Elements[i].meteorologicalData(PV_MeteorologicalDataType[i], temperature[i], irradiance[i])[0])
            self.G_Profile.append(self.PV_Elements[i].meteorologicalData(PV_MeteorologicalDataType[i], temperature[i], irradiance[i])[1])
        
        if self.operationType == 1:
            for i in range(self.N_PV):
                self.PV_Powers[self.PV_Names[i]] = self.PV_Elements[i].PowerOutput()
            return self.PV_Powers
        elif self.operationType == 2:
            return 0
    
    # Creación de los elementos BESS con base en sus parámetros constructivos     
    def BESSElements (self, BESS_Names, batteryTypes, batteryEnergy, chargePower_Max, chargePower_Min, dischargePower_Max, dischargePower_Min, 
                      gamma_sd = [2.5], eta_bc = [98.0], eta_bd = [98.0]):
        self.BESS_Names = BESS_Names
        self.BESS_SOC_Names = [name + '_SOC' for name in self.BESS_Names]
        self.BESS_chargeNames = [name + '_ChargePower' for name in BESS_Names]
        self.BESS_dischargeNames = [name + '_DischargePower' for name in BESS_Names]
        
        j=0
        
        for i in range(self.N_BESS):
            self.BESS_Elements.append(Scenary_BESS.BESS_Model(self.simulationSteps, batteryEnergy[i], chargePower_Max[i], chargePower_Min[i], 
                                                      dischargePower_Max[i], dischargePower_Min[i], self.BESS_Names[i]))
            if batteryTypes[i]==0:
                self.BESS_Elements[i].batteryType(batteryTypes[i], gamma_sd[j], eta_bc[j], eta_bd[j])
                j+=1
            else:
                self.BESS_Elements[i].batteryType(batteryTypes[i])
            
        return self.BESS_Elements
    
    # Cálculo de estado de carga de los elementos BESS con base en sus parámetros operativos
    def BESSSOC (self, BESS_OperativeDataType, initialSOC = [100.0], chargePower = [0.0], dischargePower = [0.0]):
        self.BESS_SOC = pd.DataFrame(columns = self.BESS_SOC_Names)
        self.chargePowers = pd.DataFrame(chargePower).transpose()
        self.chargePowers.columns = self.BESS_chargeNames
        self.dischargePowers = pd.DataFrame(dischargePower).transpose()
        self.dischargePowers.columns = self.BESS_dischargeNames
        
        for i in range(self.N_BESS):
            self.BESS_Elements[i].operativeData(BESS_OperativeDataType[i], initialSOC[i], chargePower[i], dischargePower[i])
        
        if self.operationType == 1:
            for i in range(self.N_BESS):
                self.BESS_SOC[self.BESS_SOC_Names[i]] = self.BESS_Elements[i].SOCOutput(self.stepTime)[0]
            return self.BESS_SOC, self.chargePowers*(-1), self.dischargePowers
        elif self.operationType == 2:
            return 0, 0, 0
    
    # Creación de los elementos Hydro con base en sus parámetros constructivos 
    def HydroElements (self, hydroNames, turbineNumbers, turbinePowers, turbineTypes, n_t = [0.7], H_min = [3.0], H_max = [130.0], Q_min = [0.0001], 
                       Q_max = [0.01], f_h = [0.05]):
        self.hydroNames = hydroNames
        
        j=0
        
        for i in range(self.N_Hydro):
            self.hydroElements.append(Scenary_Hydro.Hydro_Model(self.simulationSteps, turbineNumbers[i], turbinePowers[i], self.hydroNames[i]))
            if turbineTypes[i]==0:
                self.hydroElements[i].turbineType(turbineTypes[i], n_t[j], H_min[j], H_max[j], Q_min[j], Q_max[j], f_h[j])
                j+=1
            else:
                self.hydroElements[i].turbineType(turbineTypes[i])
            
        return self.hydroElements
    
    # Cálculo de potencia de los elementos Hydro con base en sus parámetros operativos
    def HydroGeneration (self, hydroOperativeDataType, head = [100.0], flux = [0.005]):
        self.hydroPowers = pd.DataFrame(columns = self.hydroNames)
        
        for i in range(self.N_Hydro):
            self.H_Profile.append(self.hydroElements[i].operativeData(hydroOperativeDataType[i], head[i], flux[i])[0])
            self.Q_Profile.append(self.hydroElements[i].operativeData(hydroOperativeDataType[i], head[i], flux[i])[1])
        
        if self.operationType == 1:
            for i in range(self.N_Hydro):
                self.hydroPowers[self.hydroNames[i]] = self.hydroElements[i].PowerOutput()
            return self.hydroPowers
        elif self.operationType == 2:
        #     self.hydroOperativeDataType = hydroOperativeDataType
        #     self.head = head
        #     self.flux = flux
            return 0
        
    # Creación de los elementos Wind Farm con base en sus parámetros constructivos 
    def WFElements (self, WF_Names, turbineNumbers, turbinePowers, turbineTypes, H_R = [1.0], H_A = [1.0], Z_0 = [0.03], V_C = [2.5], V_N = [11.5], 
                    V_F = [45.0]):
        self.WF_Names = WF_Names
        j=0
        
        for i in range(self.N_WF):
            self.WF_Elements.append(Scenary_WF.WF_Model(self.simulationSteps, turbineNumbers[i], turbinePowers[i], self.WF_Names[i]))
            if turbineTypes[i]==0:
                self.WF_Elements[i].turbineType(turbineTypes[i], H_R[j], H_A[j], Z_0[j], V_C[j], V_N[j], V_F[j])
                j+=1
            else:
                self.WF_Elements[i].turbineType(turbineTypes[i])
            
        return self.WF_Elements
    
    # Cálculo de potencia de los elementos Wind Farm con base en sus parámetros operativos
    def WFGeneration (self, WF_MeteorologicalDataType, airDensity = 1.112, windSpeed = [5.0]):
        self.WF_Powers = pd.DataFrame(columns = self.WF_Names)
        
        for i in range(self.N_WF):
            self.V_Profile.append(self.WF_Elements[i].meteorologicalData(WF_MeteorologicalDataType[i], airDensity, windSpeed[i]))
        
        if self.operationType == 1:
            for i in range(self.N_WF):
                self.WF_Powers[self.WF_Names[i]] = self.WF_Elements[i].PowerOutput()
            return self.WF_Powers
        elif self.operationType == 2:
            # self.WF_MeteorologicalDataType = WF_MeteorologicalDataType
            # self.airDensity = airDensity
            # self.windSpeed = windSpeed
            return 0
            
    
    # Creación de los elementos Biogas con base en sus parámetros constructivos   
    def BiogasElements (self, biogasNames, timestep=1, days=60, reactorVolume1=[30], reactorVolume2=[70], heightRelation1=[2], heightRelation2=[2], 
                        heatTransfer1=[0.05], heatTransfer2=[0.05]):
        self.biogasNames = biogasNames
        
        for i in range(self.N_Biogas):
            self.biogasElements.append(Scenary_BM.biogas_model(timestep, days, reactorVolume1[i], reactorVolume2[i], heightRelation1[i], heightRelation2[i], 
                                heatTransfer1[i], heatTransfer2[i], self.biogasNames[i]))
            
        return self.biogasElements
    
    # Definición de los parámetros termoquímicos de los elementos Biogas
    def BiogasParameters (self, Tset1=[35], tolerancia1=[3], Tset2=[35], tolerancia2=[3], Cci=[0.4], Chi=[0.05], Coi=[0.2], Csi=[0.01], ST=[0.1], 
                          rho_sus=[998], Tin_sus=[20], Pin_sus=[350], vin_sus=[0.139], DeltaP=[5], Patm=[100], Tamb=[15], genEfficiency = [0.4], ratedPower = [10]):
    
        for i in range(self.N_Biogas):
            self.biogasElements[i].ReloadThermo()
            self.biogasElements[i].TemperatureControlParameters(Tset1[i], tolerancia1[i], Tset2[i], tolerancia2[i])
            self.biogasElements[i].SubstrateProperties(Cci[i], Chi[i], Coi[i], Csi[i], ST[i], rho_sus[i], Tin_sus[i], Pin_sus[i], vin_sus[i], DeltaP[i])  
            self.biogasElements[i].KineticsParameters(k_c=0.05, k_h=0.01, k_o=0.01, k_s=0.001, k_n=0.001, k_ch4=0.015, k_co2=0.035,
                                                      k_h2s=0.002, k_nh3=0.002, Ea_c=100000, Ea_h=100000, Ea_o=20000, Ea_s=200000, 
                                                      Ea_n=200000, Ea_ch4=500, Ea_co2=100, Ea_h2s=1500, Ea_nh3=1000)
            self.biogasElements[i].TermicFluidParameters(vin_termico1=600, vin_termico2=600, Tin_termico=50, Pin_termico=35, DT_termico1=0.1, DT_termico2=0.1, DP_termico1=5, DP_termico2=7)
            self.biogasElements[i].AmbientalParameters(Patm[i], Tamb[i])
            self.biogasElements[i].GeneratorParameters(genEfficiency[i], ratedPower[i])
    
    # Cálculo de potencia de los elementos Biogas con base en sus parámetros operativos
    def BiogasGeneration (self):
        self.biogasPowers = pd.DataFrame(columns = self.biogasNames)
        
        if self.operationType == 1:
            for i in range(self.N_Biogas):
                
                self.biogasElements[i].AbsoluteVariables()
                self.biogasElements[i].HeatExchangeAreas()
                self.biogasElements[i].TimeVectorEstimation()
                self.biogasElements[i].BoundaryConditionsR1()
                self.biogasElements[i].Reactor1Simulation()
                self.biogasElements[i].BoundaryConditionsR2()
                self.biogasElements[i].Reactor2Simulation()
                self.biogasElements[i].ScenariosResults()
                
                self.biogasPowers[self.biogasNames[i]] = [self.biogasElements[i].PowerOutput()[-1]]*self.simulationSteps
                
                # print(self.biogasPowers)
            return self.biogasPowers
        elif self.operationType == 2:
            return 0
    
    # Creación de los elementos Demanda con base en sus parámetros constructivos
    def DemandElements (self, demandNames, demandTypes, demandPowersSet):
        self.demandNames = demandNames
        
        self.demandTypes = demandTypes
        self.demandPowersSet = demandPowersSet
        
        for i in range(self.N_Demand):
            self.demandElements.append(Scenary_Demand.Demand_Model(self.simulationSteps, demandTypes[i], self.demandNames[i], demandPowersSet[i]))
            
        return self.demandElements        
    
    # Cálculo de potencia de los elementos Demanda con base en su configuración anterior
    def DemandPower(self):
        self.demandPowers = pd.DataFrame(columns=self.demandNames)
        
        for i in range(self.N_Demand):
            self.demandPowers[self.demandNames[i]] = self.demandElements[i].Demand()
        self.loadProfile = self.demandPowers.sum(axis=1)
        return self.demandPowers*(-1)
    
    # Cálculo de potencia de la Red Externa balanceando generación-demanda
    def GridPower(self):
                
        if self.operationType == 1:
            gridPowers = - (pd.DataFrame(self.PV_Powers.sum(axis=1) + self.hydroPowers.sum(axis=1) + self.WF_Powers.sum(axis=1) + self.biogasPowers.sum(axis=1) + self.dischargePowers.sum(axis=1)
                                         - self.chargePowers.sum(axis=1) - self.demandPowers.sum(axis=1)))
            gridPowers.columns = ["Grid"]
            return gridPowers
        elif self.operationType == 2:
            return 0
    
    # Cálculo óptimo de la potencia de cada recurso para modo de operación automática del escenario
    def AutomaticPowerCalculation(self, resourceWeights):
        
        if self.operationType == 1:
            print("ERROR: El modo de operación se ha configurado como manual")
        elif self.operationType == 2:
            # Verificación de consistencia de datos ingresados
            if len(resourceWeights) != self.N_PV + 2*self.N_BESS + self.N_Hydro + self.N_WF + self.N_Biogas + 1:
                print("ERROR: El tamaño del vector de pesos debe coincidir con la cantidad de recursos de generación")
                PowerCalculationResults = 0
                PV_PowerResults = 0
                self.BESS_PowerResults = 0
                hydroPowerResults = 0
                WF_PowerResults = 0
                biogasPowerResults = 0
                gridPowerResults = 0
                demandPowerResults = 0
                BESS_SOC_Results = 0
                
            else:
                # Ejecución de la optimización utilizando la clase Optimizer
                self.PowerCalculationModel = Scenary_Optimizer.Dispatcher(self.simulationSteps, self.stepTime, resourceWeights, self.PV_Elements, self.biogasElements,
                                                                  self.hydroElements, self.WF_Elements, self.BESS_Elements, self.loadProfile, 
                                                                  self.G_Profile, self.T_Profile, self.H_Profile, self.Q_Profile, self.V_Profile)
                PowerCalculationResults = self.PowerCalculationModel.dispatchCalculation()
                
                PV_PowerResults = PowerCalculationResults.iloc[:, 0 : self.N_PV]
                df_temp = PowerCalculationResults.iloc[:, self.N_PV : self.N_PV + 2*self.N_BESS]
                if self.N_BESS > 0:
                    self.BESS_PowerResults = pd.DataFrame(columns=self.BESS_Names)
                for i in range(0, 2*self.N_BESS, 2):
                    self.BESS_PowerResults[self.BESS_Names[int(i/2)]] = df_temp.iloc[:, i].add(df_temp.iloc[:, i + 1], fill_value=0)
                hydroPowerResults = PowerCalculationResults.iloc[:, self.N_PV + 2*self.N_BESS : self.N_PV + 2*self.N_BESS + self.N_Hydro]
                WF_PowerResults = PowerCalculationResults.iloc[:, self.N_PV + 2*self.N_BESS + self.N_Hydro : self.N_PV + 2*self.N_BESS + self.N_Hydro + self.N_WF]
                biogasPowerResults = PowerCalculationResults.iloc[:, self.N_PV + 2*self.N_BESS + self.N_Hydro + self.N_WF : self.N_PV + 2*self.N_BESS + self.N_Hydro + self.N_WF + self.N_Biogas]
                gridPowerResults = PowerCalculationResults.iloc[:, self.N_PV + 2*self.N_BESS + self.N_Hydro + self.N_WF + self.N_Biogas]
                demandPowerResults = self.demandPowers*(-1)
                BESS_SOC_Results = PowerCalculationResults.iloc[:, self.N_PV + 2*self.N_BESS + self.N_Hydro + self.N_WF + self.N_Biogas + 1 + self.N_BESS : self.N_PV + 2*self.N_BESS + self.N_Hydro + self.N_WF + self.N_Biogas + 1 + 2*self.N_BESS]
                
                PowerCalculationResults = pd.concat([PowerCalculationResults, demandPowerResults], axis = 1)
                
            return PowerCalculationResults, PV_PowerResults, self.BESS_PowerResults, hydroPowerResults, WF_PowerResults, biogasPowerResults, demandPowerResults, gridPowerResults, BESS_SOC_Results
