import math
from scipy.optimize import minimize
from scipy.optimize import Bounds

class WF_Model:
    # Inicializacion de granja eolica
    def __init__(self, simulationSteps, N_WT, P_WM, name):
        self.N_WT = N_WT # Numero de turbinas eolicas
        self.P_WM = P_WM # Potencia pico nominal de cada turbina eolica en kW
        self.P_max = N_WT * P_WM # Potencia maxima del sistema
        self.P_min = 0 # Potencia minima del sistema
        self.simulationSteps = simulationSteps # Número de pasos de simulación
        self.name = name # Nombre del sistema

    # Parametrizacion de la turbina eolica
    def turbineType (self, type, H_R = 1.0, H_A = 1.0, Z_0 = 0.03, V_C = 2.5, V_N = 11.5, V_F = 45.0):
        self.turbineType = type
        
        # Turbina Laboratorio
        if self.turbineType == 1:
            self.H_R = 1
            self.H_A = 1
            self.Z_0 = 0.03
            self.V_C = 2
            self.V_N = 11.5
            self.V_F = 65
        # Personalizado   
        elif self.turbineType == 0:
            self.H_R = H_R
            self.H_A = H_A
            self.Z_0 = Z_0
            self.V_C = V_C
            self.V_N = V_N
            self.V_F = V_F
        
        return self.H_R, self.H_A, self.Z_0, self.V_C, self.V_N, self.V_F
    
    # Parametrizacion de informacion meteorologica
    def meteorologicalData (self, type, ro = 1.112, V_a = [5]):
        self.meteorologicalDataType = type
        self.ro = ro
        
        # Valor fijo ingresado por el usuario
        if self.meteorologicalDataType == 1:
            self.V_a = V_a * self.simulationSteps
        # Curvas tipicas escaladas con valores maximos
        elif self.meteorologicalDataType == 2:
            V_profile = [0.41935, 0.51613, 0.58065, 0.58065, 0.41935, 0.45161, 0.35484, 0.22581, 0.12903, 0.29032, 0.38710, 0.32258, 0.38710, 0.37097, 0.35484, 0.30645, 0.35484, 0.93548, 1.00000, 0.90323, 0.35484, 0.32258, 0.32258, 0.35484]
            self.V_a = [i * V_a[0] for i in V_profile]
        # Curva Personalizada
        elif self.meteorologicalDataType == 0:
            self.V_a = V_a
        return self.V_a
    
    # Calculo de potencia del sistema
    def PowerOutput (self):
        # Calculo de velocidad ajustada por altura
        self.V_r = [i * (math.log(self.H_R/self.Z_0, math.e) / math.log(self.H_A/self.Z_0, math.e)) for i in self.V_a]
        #Calculo de potencia de cada aero generador
        P_wtSTP = []
        for i in self.V_r:
            if (i > self.V_C and i < self.V_N):
                P_wtSTP.append(self.P_WM * (((i**2) - (self.V_C**2)) / ((self.V_N**2) - (self.V_C**2))))
            elif (i >= self.V_N and i < self.V_F):
                P_wtSTP.append(self.P_WM)
            elif (i <= self.V_C or i > self.V_F):
                P_wtSTP.append(0)
        self.P_wtSTP = P_wtSTP
        # Ajuste de potencia por densidad de aire
        self.P_wt = [(self.ro / 1.225) * i for i in self.P_wtSTP]
        # Calculo de potencia del sistema en kW
        self.P_WF = [round(self.N_WT * i,3) for i in self.P_wt]
        return self.P_WF
    
    # Calculo de energía generada    
    def EnergyOutput (self, stepTime):
        self.E_WF = [0]
        for i in range(len(self.P_WF)):
            self.E_WF.append(round(self.E_WF[i] + self.P_WF[i] * stepTime,3))
        self.E_WF.pop(0)
        return self.E_WF
    
    # Control de potencia del sistema
    def PowerControl(self, Pref): # Ingresa la potencia requerida en kW
        
        self.Pref = Pref
        self.Vref = []
        
        for P in self.Pref:
        
            # Definición de modelo
            self.A = math.log(self.H_R/self.Z_0, math.e) / math.log(self.H_A/self.Z_0, math.e)
            self.B = self.N_WT * self.P_WM * (1 / (math.pow(self.V_N,2) - math.pow(self.V_C,2)))
            self.C = math.pow(self.V_C,2)
            self.D = self.ro / 1.225
            
            # Definición de función de potencia por pasos
            if (P >= self.D * self.N_WT * self.P_WM):
                self.Vref.append(round((self.V_N + 1.0) / self.A, 3))
    
            elif (P > 0.0 and P < self.D * self.N_WT * self.P_WM):
                # Definición de función objetivo
                def objective(x):
                    V = x[0]
                    f = P - self.D * (self.B * (math.pow(self.A * V,2) - self.C))
                    return f
        
                # Definición de restricciones
                def constraint1(x):
                    V = x[0]
                    f = P - self.D * (self.B * (math.pow(self.A * V,2) - self.C))
                    return f
                
                # Valor inicial de velocidad de viento
                x0 = [5.0]
        
                # Límites de velocidad de viento
                bnds = Bounds(self.V_C, self.V_F)
        
                con1 = {'type': 'eq', 'fun': constraint1}
                cons = [con1]
        
                # Optimización de velocidad de viento por minimización cuadrática secuencial
                solution = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
                
                self.Vref.append(round(solution.x[0],3))
            
            elif (P == 0):
                self.Vref.append(round((self.V_C - 1.0)/ self.A, 3))
        
        return self.Vref