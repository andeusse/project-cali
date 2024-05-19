import xalglib
import pandas as pd
from simulation_models.Scenarios_systems import BiogasModel as BM
from simulation_models.Scenarios_systems import Scenary_Hydro
from simulation_models.Scenarios_systems import Scenary_PV
from simulation_models.Scenarios_systems import Scenary_WF

class Dispatcher:
    # Inicialización del modelo de optimización con los elementos creados en el escenario (ver script Scenario.py)
    def __init__(self, simulationSteps, stepTime, resourceWeights, PV_Elements, biogasElements, hydroElements, WF_Elements, BESS_Elements, loadProfile, G_Profile, T_Profile, H_Profile, Q_Profile, V_Profile):
        
        self.simulationSteps = simulationSteps # Pasos de simulación definidos por el usuarios
        self.stepTime = stepTime # Equivalencia de tiempo en horas de cada paso de simulación
        temp=[]
        for i in range(simulationSteps): temp.append(resourceWeights)
        self.weights = pd.DataFrame(temp).transpose() # Orden de prioridad de despacho de los generadores
        self.PV_Elements = PV_Elements # Elementos de recurso PV
        self.BESS_Elements = BESS_Elements # Elementos de recurso BESS
        self.hydroElements = hydroElements # Elementos de recurso Hydro
        self.WF_Elements = WF_Elements # Elementos de recurso Wind Farm
        self.biogasElements = biogasElements # Elementos de recurso Biogas
        self.loadProfile = loadProfile # Perfil de demanda de potencia
        self.G_Profile = G_Profile # Perfil de irradiancia solar
        self.T_Profile = T_Profile # Perfil de temperatura
        self.H_Profile = H_Profile # Perfil de cabeza de agua
        self.Q_Profile = Q_Profile # Perfil de caudal de agua
        self.V_Profile = V_Profile # Perfil de velocidad de viento
    
    # Función de cálculo óptimo de potencia para cada elemento del escenario
    def dispatchCalculation(self):
        #  Function Callback
        def function(x, param):
            func = 0
            for i in range(len(x)):
                func = func + x[i]*Cost[i]
            return func
        
        # Estructuración del problema de optimización
        x = []
        bndl = []
        bndu = []
        columns = []
        InitialBESSEnergy = []
        
        # Definición de condiciones de frontera para cada tipo de recurso
        for i in range(len(self.PV_Elements)):
            x.append(0.0)
            bndl.append(self.PV_Elements[i].P_min)
            bndu.append(self.PV_Elements[i].P_max)
            columns.append(self.PV_Elements[i].name)
            
        for i in range(len(self.BESS_Elements)):
            x.append(0.0)
            x.append(0.0)
            InitialBESSEnergy.append(self.BESS_Elements[i].SOC[0]*self.BESS_Elements[i].E_b/100)
            bndl.append(self.BESS_Elements[i].P_cMax*-1)
            bndl.append(self.BESS_Elements[i].P_dMin)
            bndu.append(self.BESS_Elements[i].P_cMin)        
            bndu.append(self.BESS_Elements[i].P_dMax)
            columns.append(self.BESS_Elements[i].name + "_ChargePower")
            columns.append(self.BESS_Elements[i].name + "_DischargePower")
            
        for i in range(len(self.hydroElements)):
            x.append(0.0)
            bndl.append(self.hydroElements[i].P_min)
            bndu.append(self.hydroElements[i].P_max)
            columns.append(self.hydroElements[i].name)
            
        for i in range(len(self.WF_Elements)):
            x.append(0.0)
            bndl.append(self.WF_Elements[i].P_min)
            bndu.append(self.WF_Elements[i].P_max)
            columns.append(self.WF_Elements[i].name)
        
        for i in range(len(self.biogasElements)):
            x.append(0.0)
            bndl.append(self.biogasElements[i].P_min)
            bndu.append(self.biogasElements[i].P_max)
            columns.append(self.biogasElements[i].name)
        
        # Definición de límites de potencia de red externa
        x.append(self.loadProfile[0])
        bndl.append(-1e6) # Límite de 10^6 kW de exportación del escenario
        bndu.append(1e6) # Límite de 10^6 kW de importación del escenario
        columns.append("Grid")
            
        for j in range(len(self.BESS_Elements)):
            columns.append(self.BESS_Elements[j].name + "_Energy")
            
        for j in range(len(self.BESS_Elements)):
            columns.append(self.BESS_Elements[j].name + "_SOC" )
        
        scales = [1] * len(x)
        self.real_dispatch = []
        
        # Ajuste de error del optimizador
        epsg = 0
        epsf = 0
        epsx = 0
        maxits = 0
        diffstep = 1.0e-6
        
        # Identificación de pasos de simulación de menor y mayor demanda
        minTime = self.loadProfile.idxmin()
        maxTime = self.loadProfile.idxmax()
        
        hasRunBiogas = [False]*len(self.biogasElements)
        constrain_Biogas = [0]*len(self.biogasElements)
        
        # Cálculo continuo del despacho para cada paso de simulación
        for i in range(self.simulationSteps):
            # Linear constrains
            LinearConstrains = []
            LinearConstrainsType = []
            
            # Definición de restricciones para cada tipo de recurso
            for j in range(len(self.PV_Elements)):
                GenericConstrain = [0] * len(x)
                
                # Restricción de potencia generada a partir del modelo de PV
                PV_Model = Scenary_PV.PV_Model(self.PV_Elements[j].simulationSteps, self.PV_Elements[j].N_PV, self.PV_Elements[j].P_PM, self.PV_Elements[j].name)
                PV_Model.moduleType(self.PV_Elements[j].moduleType, self.PV_Elements[j].f_PV, self.PV_Elements[j].G_0, self.PV_Elements[j].u_PM, self.PV_Elements[j].T_cSTC, self.PV_Elements[j].T_cNOCT, self.PV_Elements[j].T_aNOCT, self.PV_Elements[j].G_NOCT, self.PV_Elements[j].n_c)
                PV_Model.meteorologicalData(0, [self.T_Profile[j][i]], [self.G_Profile[j][i]])
                
                constrain_PV = PV_Model.PowerOutput()[0]
                
                GenericConstrain[j] = 1
                GenericConstrain.append(constrain_PV)
                LinearConstrains.append(GenericConstrain)
                LinearConstrainsType.append(0)
                
            for j in range(len(self.BESS_Elements)):
                GenericConstrain = [0] * len(x)
                
                # Restricción de potencias de carga y descarga del BESS
                constrain_BESS_1 = 1 - (self.BESS_Elements[j].gamma_sd/100.0/720.0)
                constrain_BESS_2 = self.BESS_Elements[j].eta_bc/100.0
                constrain_BESS_3 = 1 / (self.BESS_Elements[j].eta_bd/100.0)
                InitialBESSEnergy[j] = constrain_BESS_1*InitialBESSEnergy[j]-constrain_BESS_2*x[(j*2) + 
                                       len(self.PV_Elements)]-constrain_BESS_3*x[(j*2) + len(self.PV_Elements) + 1]
                
                GenericConstrain[(j*2) + len(self.PV_Elements)] = -constrain_BESS_2
                GenericConstrain[(j*2) + len(self.PV_Elements) + 1] = -constrain_BESS_3
                GenericConstrain.append(self.BESS_Elements[j].E_b*0.2-constrain_BESS_1*InitialBESSEnergy[j])
                LinearConstrains.append(GenericConstrain)
                LinearConstrainsType.append(1)
                
                GenericConstrain = [0] * len(x)
                GenericConstrain[(j*2) + len(self.PV_Elements)] = -constrain_BESS_2
                GenericConstrain[(j*2) + len(self.PV_Elements) + 1] = -constrain_BESS_3
                GenericConstrain.append(self.BESS_Elements[j].E_b-constrain_BESS_1*InitialBESSEnergy[j])
                LinearConstrains.append(GenericConstrain)
                LinearConstrainsType.append(-1)
                
            for j in range(len(self.hydroElements)):
                GenericConstrain = [0] * len(x)
                
                # Restricción de potencia generada a partir del modelo de Hydro
                hydroModel = Scenary_Hydro.Hydro_Model(self.hydroElements[j].simulationSteps, self.hydroElements[j].N_ht, self.hydroElements[j].P_ht, self.hydroElements[j].name)
                hydroModel.turbineType(self.hydroElements[j].turbineType, self.hydroElements[j].n_t, self.hydroElements[j].H_min, self.hydroElements[j].H_max, self.hydroElements[j].Q_min, self.hydroElements[j].Q_max, self.hydroElements[j].f_h)
                hydroModel.operativeData(0, [self.H_Profile[j][i]], [self.Q_Profile[j][i]])
                
                constrain_Hydro = hydroModel.PowerOutput()[0]
                
                if constrain_Hydro > self.hydroElements[j].P_max:
                    constrain_Hydro = self.hydroElements[j].P_max

                GenericConstrain[j + len(self.PV_Elements) + len(self.BESS_Elements)*2] = 1
                GenericConstrain.append(constrain_Hydro)
                LinearConstrains.append(GenericConstrain)
                LinearConstrainsType.append(-1)
                
            for j in range(len(self.WF_Elements)):
                GenericConstrain = [0] * len(x)
                
                # Restricción de potencia generada a partir del modelo de Wind Farm
                WF_Model = Scenary_WF.WF_Model(self.WF_Elements[j].simulationSteps, self.WF_Elements[j].N_WT, self.WF_Elements[j].P_WM, self.WF_Elements[j].name)
                WF_Model.turbineType(self.WF_Elements[j].turbineType, self.WF_Elements[j].H_R, self.WF_Elements[j].H_A, self.WF_Elements[j].Z_0, self.WF_Elements[j].V_C, self.WF_Elements[j].V_N, self.WF_Elements[j].V_F)
                WF_Model.meteorologicalData(0, self.WF_Elements[j].ro, [self.V_Profile[j][i]])
                
                constrain_WF = WF_Model.PowerOutput()[0]
                
                if constrain_WF > self.WF_Elements[j].P_max:
                    constrain_WF = self.WF_Elements[j].P_max

                GenericConstrain[j + len(self.PV_Elements) + len(self.BESS_Elements)*2 + len(self.hydroElements)] = 1
                GenericConstrain.append(constrain_WF)
                LinearConstrains.append(GenericConstrain)
                LinearConstrainsType.append(0)
                        
            for j in range(len(self.biogasElements)):
                GenericConstrain = [0] * len(x)
                
                if not hasRunBiogas[j]:
                
                    # Restricción de potencia generada a partir del modelo de Biogas
                    biogasModel = BM.biogas_model(self.biogasElements[j].tp, self.biogasElements[j].dias, self.biogasElements[j].V1, self.biogasElements[j].V2, self.biogasElements[j].L_H1, self.biogasElements[j].L_H2, 
                                                  self.biogasElements[j].U1, self.biogasElements[j].U2)
                    biogasModel.ReloadThermo()
                    biogasModel.TemperatureControlParameters(self.biogasElements[j].Tset1, self.biogasElements[j].tolerancia1, self.biogasElements[j].Tset2, self.biogasElements[j].tolerancia2)
                    biogasModel.SubstrateProperties(self.biogasElements[j].Cci, self.biogasElements[j].Chi, self.biogasElements[j].Coi, self.biogasElements[j].Csi, self.biogasElements[j].ST, self.biogasElements[j].rho_sus, 
                                                    self.biogasElements[j].Tin_sus, self.biogasElements[j].Pin_sus, self.biogasElements[j].vin_sus, self.biogasElements[j].DeltaP)  
                    biogasModel.KineticsParameters(k_c=0.05, k_h=0.01, k_o=0.01, k_s=0.001, k_n=0.001, k_ch4=0.015, k_co2=0.035,
                                                              k_h2s=0.002, k_nh3=0.002, Ea_c=100000, Ea_h=100000, Ea_o=20000, Ea_s=200000, 
                                                              Ea_n=200000, Ea_ch4=500, Ea_co2=100, Ea_h2s=1500, Ea_nh3=1000)
                    biogasModel.TermicFluidParameters(vin_termico1=600, vin_termico2=600, Tin_termico=50, Pin_termico=35, DT_termico1=0.1, DT_termico2=0.1, DP_termico1=5, DP_termico2=7)
                    biogasModel.AmbientalParameters(self.biogasElements[j].Patm, self.biogasElements[j].Tamb)
                    biogasModel.AbsoluteVariables()
                    biogasModel.HeatExchangeAreas()
                    biogasModel.TimeVectorEstimation()
                    biogasModel.BoundaryConditionsR1()
                    biogasModel.Reactor1Simulation()
                    biogasModel.BoundaryConditionsR2()
                    biogasModel.Reactor2Simulation()
                    biogasModel.ScenariosResults()
                    biogasModel.GeneratorParameters(self.biogasElements[j].genEfficiency, self.biogasElements[j].P_max)
                    
                    constrain_Biogas[j] = biogasModel.PowerOutput()[-1]
                    
                    hasRunBiogas[j] = True

                GenericConstrain[j + len(self.PV_Elements) + len(self.BESS_Elements)*2 + len(self.hydroElements) + len(self.WF_Elements)] = 1
                GenericConstrain.append(constrain_Biogas[j])
                LinearConstrains.append(GenericConstrain)
                LinearConstrainsType.append(-1)
                
            # Restricción de carga demandada en el escenario (toda la carga se debe atender)
            LoadConstrain = [1] * len(x)
            LoadConstrain.append(self.loadProfile[i])
            LinearConstrains.append(LoadConstrain)
            LinearConstrainsType.append(0)
            
            Cost = self.weights.iloc[:,i]
            
            # Administración inteligente del BESS de acuerdo con los periodos de mínima y máxima demanda
            for j in range(len(self.BESS_Elements)):
                constrain_BESS_1 = 1 - (self.BESS_Elements[j].gamma_sd/100.0/720.0)
                constrain_BESS_2 = self.BESS_Elements[j].eta_bc/100.0
                constrain_BESS_3 = 1 / (self.BESS_Elements[j].eta_bd/100.0)
                if minTime < maxTime:
                    if i >= maxTime:
                        pass
                    elif minTime-1 <= i:
                        if InitialBESSEnergy[j] - bndl[(j*2) + len(self.PV_Elements)] < self.BESS_Elements[j].E_b:
                            GenericConstrain = [0] * len(x)
                            GenericConstrain[(j*2) + len(self.PV_Elements)] = 1
                            GenericConstrain.append(bndl[(j*2) + len(self.PV_Elements)])
                            LinearConstrains.append(GenericConstrain)
                        elif InitialBESSEnergy[j] == self.BESS_Elements[j].E_b:
                            GenericConstrain = [0] * len(x)
                            GenericConstrain[(j*2) + len(self.PV_Elements)] = 1
                            GenericConstrain.append(-InitialBESSEnergy[j]*(self.BESS_Elements[j].gamma_sd/100.0/720.0)/constrain_BESS_2)
                            LinearConstrains.append(GenericConstrain)     
                        else:
                            GenericConstrain = [0] * len(x)
                            GenericConstrain[(j*2) + len(self.PV_Elements)] = 1
                            GenericConstrain.append(-(self.BESS_Elements[j].E_b-constrain_BESS_1*InitialBESSEnergy[j])/constrain_BESS_2)
                            LinearConstrains.append(GenericConstrain)  
                        GenericConstrain = [0] * len(x)
                        GenericConstrain[(j*2) + len(self.PV_Elements) + 1] = 1
                        GenericConstrain.append(0)
                        LinearConstrains.append(GenericConstrain)
                        LinearConstrainsType.extend([0,0])
                    elif InitialBESSEnergy[j] > self.BESS_Elements[j].E_b*0.2:
                        GenericConstrain = [0] * len(x)
                        GenericConstrain[(j*2) + len(self.PV_Elements)] = 1
                        GenericConstrain.append(-InitialBESSEnergy[j]*(self.BESS_Elements[j].gamma_sd/100.0/720.0)/constrain_BESS_2)
                        LinearConstrains.append(GenericConstrain)
                        
                        GenericConstrain = [0] * len(x)
                        GenericConstrain[(j*2) + len(self.PV_Elements) + 1] = 1
                        GenericConstrain.append(0)
                        LinearConstrains.append(GenericConstrain)
                        LinearConstrainsType.extend([0,0])
                else:        
                    if minTime-1 <= i:
                        if InitialBESSEnergy[j] - bndl[(j*2) + len(self.PV_Elements)] < self.BESS_Elements[j].E_b:   
                            GenericConstrain = [0] * len(x)
                            GenericConstrain[(j*2) + len(self.PV_Elements)] = 1
                            GenericConstrain.append(bndl[(j*2) + len(self.PV_Elements)])
                            LinearConstrains.append(GenericConstrain)
                        elif InitialBESSEnergy[j] == self.BESS_Elements[j].E_b:
                            GenericConstrain = [0] * len(x)
                            GenericConstrain[(j*2) + len(self.PV_Elements)] = 1
                            GenericConstrain.append(-InitialBESSEnergy[j]*(self.BESS_Elements[j].gamma_sd/100/720)/constrain_BESS_2)
                            LinearConstrains.append(GenericConstrain)
                        else:
                            GenericConstrain = [0] * len(x)
                            GenericConstrain[(j*2) + len(self.PV_Elements)] = 1
                            GenericConstrain.append(-(self.BESS_Elements[j].E_b-constrain_BESS_1*InitialBESSEnergy[j])/constrain_BESS_2)
                            LinearConstrains.append(GenericConstrain)
                        GenericConstrain = [0] * len(x)
                        GenericConstrain[(j*2) + len(self.PV_Elements) + 1] = 1
                        GenericConstrain.append(0)
                        LinearConstrains.append(GenericConstrain)
                        LinearConstrainsType.extend([0,0])
                    elif i >= maxTime:
                        pass
                    elif InitialBESSEnergy[j] > self.BESS_Elements[j].E_b*0.2:
                        GenericConstrain = [0] * len(x)
                        GenericConstrain[(j*2) + len(self.PV_Elements)] = 1
                        GenericConstrain.append(-InitialBESSEnergy[j]*(self.BESS_Elements[j].gamma_sd/100/720)/constrain_BESS_2)
                        LinearConstrains.append(GenericConstrain)
                        
                        GenericConstrain = [0] * len(x)
                        GenericConstrain[(j*2) + len(self.PV_Elements) + 1] = 1
                        GenericConstrain.append(0)
                        LinearConstrains.append(GenericConstrain)
                        LinearConstrainsType.extend([0,0])
            
            # for j in range(len(self.biogasElements)):
            #     CurrentFuelSupply = FuelSupplies.iloc[[i]].values.tolist()[0]
            #     GenericConstrain = [0] * len(x)
            #     constrain_Biogas = 1/(self.biogasElements[j].LHV_biogas*self.biogasElements[j].eta_biogas)
            #     if InitialBiogasVolume[j] >= self.biogasElements[j].Biogas_Volume_max:
            #         if InitialBiogasVolume[j]+CurrentFuelSupply[j]-self.biogasElements[j].Biogas_Volume_min >= self.biogasElements[j].Biogas_P_max*constrain_Biogas:
            #             GenericConstrain[j + len(self.PV_Elements) + len(self.BESS_Elements)*2 + len(self.hydroElements) + len(self.WF_Elements)] = 1
            #             GenericConstrain.append(self.biogasElements[j].Biogas_P_max)
            #         else:
            #             GenericConstrain[j + len(self.PV_Elements) + len(self.BESS_Elements)*2 + len(self.hydroElements) + len(self.WF_Elements)] = constrain_Biogas
            #             GenericConstrain.append(InitialBiogasVolume[j]+CurrentFuelSupply[j]-self.biogasElements[j].Biogas_Volume_min)
            #         LinearConstrains.append(GenericConstrain)
            #         LinearConstrainsType.append(0)
            
            # Definición de variables self para visulaizar fuera de clase
            self.x = x
            self.bndl = bndl
            self.bndu = bndu
            self.LinearConstrains = LinearConstrains
            self.LinearConstrainsType = LinearConstrainsType
            self.scales = scales
            
            # Parametrización de la función minbleic para optimización lineal de la librería Alglib
            states = xalglib.minbleiccreatef(x, diffstep)
            xalglib.minbleicsetbc(states, bndl, bndu)
            xalglib.minbleicsetlc(states, LinearConstrains, LinearConstrainsType)
            xalglib.minbleicsetscale(states, scales)
            xalglib.minbleicsetcond(states, epsg, epsf, epsx, maxits)
                                   
            # Ejecución de la optimización mediante función minbleicoptimize
            xalglib.minbleicoptimize_f(states, function)
            x, rep = xalglib.minbleicresults(states)
                
            temp = x.copy()
            
            for j in range(len(InitialBESSEnergy)):
                temp.append(InitialBESSEnergy[j])
                
            for j in range(len(InitialBESSEnergy)):
                temp.append((InitialBESSEnergy[j]/self.BESS_Elements[j].E_b)*100)
                
            # for j in range(len(InitialBiogasVolume)):
            #     temp.append(InitialBiogasVolume[j])
                
            self.real_dispatch.append(temp)
            
        # Creación de dataframe con resultados de optimización
        self.real_df = pd.DataFrame(self.real_dispatch)
        self.real_df = self.real_df.round(3)
        self.real_df.columns = columns
        
        return self.real_df