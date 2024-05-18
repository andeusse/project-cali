import math
from scipy.optimize import minimize

class PV_Model:
    # Inicializacion de granja solar
    def __init__(self, simulationSteps, N_PV, P_PM, name):
        self.N_PV = N_PV # Numero de modulos
        self.P_PM = P_PM # Potencia pico nominal de cada modulo en W
        self.P_max = N_PV * P_PM / 1000 # Potencia maxima del sistema
        self.P_min = 0 # Potencia minima del sistema
        self.simulationSteps = simulationSteps # Número de pasos de simulación
        self.name = name # Nombre del sistema

    # Parametrizacion de modulo de acuerdo a tipo
    def moduleType (self, type, f_PV = 1.0, G_0 = 1000.0, u_PM = -0.39, T_cSTC = 25.0, T_cNOCT = 45.0, T_aNOCT = 20.0, G_NOCT = 800.0, n_c = 15.44):
        self.moduleType = type
        
        # Silicio Monocristalino
        if self.moduleType == 1:
            self.f_PV = 1
            self.G_0 = 1000
            self.u_PM = -0.39
            self.T_cSTC = 25
            self.T_cNOCT = 45
            self.T_aNOCT = 20
            self.G_NOCT = 800
            self.n_c = 15.44
        # Silicio Policristalino
        elif self.moduleType == 2:
            self.f_PV = 1
            self.G_0 = 1000
            self.u_PM = -0.39
            self.T_cSTC = 25
            self.T_cNOCT = 45
            self.T_aNOCT = 20
            self.G_NOCT = 800
            self.n_c = 15.44
        # Silicio Monocristalino de Pelicula Delgada
        elif self.moduleType == 3:
            self.f_PV = 1
            self.G_0 = 1000
            self.u_PM = -0.42
            self.T_cSTC = 25
            self.T_cNOCT = 45
            self.T_aNOCT = 20
            self.G_NOCT = 800
            self.n_c = 15.43
        # Telururo de Cadmio    
        elif self.moduleType == 4:
            self.f_PV = 1
            self.G_0 = 1000
            self.u_PM = -0.25
            self.T_cSTC = 25
            self.T_cNOCT = 42
            self.T_aNOCT = 20
            self.G_NOCT = 800
            self.n_c = 11.0
        # Personalizado
        elif self.moduleType == 0:
            self.f_PV = f_PV
            self.G_0 = G_0
            self.u_PM = u_PM
            self.T_cSTC = T_cSTC
            self.T_cNOCT = T_cNOCT
            self.T_aNOCT = T_aNOCT
            self.G_NOCT = G_NOCT
            self.n_c = n_c
        return self.f_PV, self.G_0, self.u_PM, self.T_cSTC, self.T_cNOCT, self.T_aNOCT, self.G_NOCT, self.n_c
    
    # Parametrizacion de informacion meteorologica
    def meteorologicalData (self, type, T_a = [25.0], G = [1000.0]):
        self.meteorologicalDataType = type
        
        # Valor fijo ingresado por el usuario
        if self.meteorologicalDataType == 1:
            self.T_a = T_a * self.simulationSteps
            self.G = G * self.simulationSteps
        # Curvas tipicas escaladas con valores maximos
        elif self.meteorologicalDataType == 2:
            T_profile = [0.6452, 0.6129, 0.6129, 0.5968, 0.5806, 0.5806, 0.5806, 0.5710, 0.6774, 0.7258, 0.7742, 0.8226, 0.8387, 0.9032, 0.9355, 0.9355, 1.0000, 0.9032, 0.8387, 0.8065, 0.7742, 0.7258, 0.7097, 0.6935]
            G_profile = [0.0000, 0.0001, 0.0004, 0.0017, 0.0061, 0.0194, 0.0531, 0.1252, 0.2547, 0.4469, 0.6762, 0.8825, 0.9934, 0.9644, 0.8075, 0.5832, 0.3633, 0.1952, 0.0904, 0.0361, 0.0125, 0.0037, 0.0009, 0.0002]
            self.T_a = [i * T_a[0] for i in T_profile]
            self.G = [i * G[0] for i in G_profile]
        # Curva Personalizada
        elif self.meteorologicalDataType == 0:
            self.T_a = T_a
            self.G = G
        return self.T_a, self.G
    
    # Calculo de potencia del sistema
    def PowerOutput (self):
        # Calculo de temperatura del modulo
        self.T_c = [round((self.T_a[i] + self.G[i] * ((self.T_cNOCT-self.T_aNOCT) / self.G_NOCT) * (1 - ((self.n_c/100) / 0.9))), 4) for i in range(len(self.T_a))]
        #Calculo de potencia de cada modulo
        self.P_module = [(self.f_PV * (self.G[i] / self.G_0) * self.P_PM * (1 + ((self.u_PM/100) * (self.T_c[i] - self.T_cSTC)))) for i in range(len(self.G))]
        # Calculo de potencia del sistema en kW
        self.P_PV = [round((self.N_PV * i) / 1000, 4) for i in self.P_module]
        return self.P_PV
    
    # Calculo de energía generada
    def EnergyOutput (self, stepTime):
        self.E_PV = [0]
        for i in range(len(self.P_PV)):
            self.E_PV.append(round(self.E_PV[i] + self.P_PV[i] * stepTime,3))
        self.E_PV.pop(0)
        return self.E_PV

    # Control de potencia del sistema
    def PowerControl(self, Pref): # Ingresa la potencia requerida en kW
        
        self.Pref = Pref
        self.Gref = []
        self.Tref = []
        
        for P in self.Pref:
                    
            # Definición de modelo
            self.A = (self.N_PV * self.f_PV * self.P_PM / (self.G_0 * 1000.0)) * (1 - (self.u_PM/100) * self.T_cSTC)
            self.B = (self.N_PV * self.f_PV * self.P_PM / (self.G_0 * 1000.0)) * (self.u_PM/100)
            self.C = ((self.T_cNOCT - self.T_aNOCT) / (self.G_NOCT)) * (1 - (self.n_c/100) / 0.9)
    
            # Definición de función objetivo
            def objective(x):
                G = x[0]
                T = x[1]
                f = P - (self.A * G + self.B * G * T + self.B * self.C * math.pow(G, 2))
                return f
    
            # Definición de restricciones
            def constraint1(x):
                G = x[0]
                T = x[1]
                f = P - (self.A * G + self.B * G * T + self.B * self.C * math.pow(G, 2))
                return f
            
            # Relación ajustada de irradiancia - temperatura
            def constraint2(x):
                G = x[0]
                T = x[1]
                f = 0.014 * G + 17.0 - T
                return f
            
            # Valores iniciales de irradiancia y temperatura
            x0 = [1000.0, 25.0]
    
            # Límites de irradiancia y temperatura
            bnds = ((0.0, 1400.0), (10.0, 40.0))
    
            con1 = {'type': 'eq', 'fun': constraint1}
            con2 = {'type': 'eq', 'fun': constraint2}
            cons = [con1, con2]
    
            # Optimización de irradiancia y temperatura por minimización cuadrática secuencial
            solution = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
            
            self.Gref.append(round(solution.x[0],3))
            self.Tref.append(round(solution.x[1],3))
        
        return self.Gref, self.Tref