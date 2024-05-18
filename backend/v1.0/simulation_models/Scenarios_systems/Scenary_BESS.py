import math
from scipy.optimize import minimize
from scipy.optimize import Bounds

class BESS_Model:
    # Inicializacion de baterias
    def __init__(self, simulationSteps, E_b, P_cMax, P_cMin, P_dMax, P_dMin, name):
        self.E_b = E_b # Capacidad de almacenamiento total de energia de las baterias en kWh
        self.P_cMax = P_cMax # potencia de carga maxima
        self.P_cMin = P_cMin # potencia de carga minima
        self.P_dMax = P_dMax # potencia de descarga maxima
        self.P_dMin = P_dMin # potencia de descarga minima
        self.simulationSteps = simulationSteps # Número de pasos de simulación
        self.name = name # Nombre del sistema

    # Parametrizacion del BESS
    def batteryType (self, type, gamma_sd = 2.5, eta_bc = 98.0, eta_bd = 98.0):
        self.batteryType = type
        
        # Baterias sistemas Laboratorio
        if self.batteryType == 1:
            self.gamma_sd = 2.5
            self.eta_bc = 98.0
            self.eta_bd = 98.0
        # Personalizado   
        elif self.batteryType == 0:
            self.gamma_sd = gamma_sd
            self.eta_bc = eta_bc
            self.eta_bd = eta_bd
        
        return self.gamma_sd, self.eta_bc, self.eta_bd
    
    # Parametrizacion de parametros operativos
    def operativeData (self, type, SOC_0, P_bc = [0.0], P_bd = [0.0]):
        self.operativeDataType = type       
        self.SOC = []
        self.SOC.append(SOC_0)
        # Valor fijo ingresado por el usuario
        if self.operativeDataType == 1:
            self.P_bc = P_bc * self.simulationSteps
            self.P_bd = P_bd * self.simulationSteps
        # Curva Personalizada
        elif self.operativeDataType == 0:
            self.P_bc = P_bc
            self.P_bd = P_bd
        return self.P_bc+[0.0], self.P_bd+[0.0]
    
    # Calculo de estado de carga SOC del sistema
    def SOCOutput (self, stepTime):
        #Calculo de SOC de baterias
        for i in range(len(self.P_bc)):
            SOCnew = self.SOC[i] * (1 - (self.gamma_sd/100)/(720/stepTime))+(((self.eta_bc/100) * self.P_bc[i] * stepTime - (1 / (self.eta_bd/100)) * self.P_bd[i] * stepTime) / self.E_b)*100
            if SOCnew < 0.0:
                SOCnew = 0.0
            elif SOCnew > 100.0:
                SOCnew = 100.0
            self.SOC.append(round(SOCnew,3))
        return self.SOC, [value * self.E_b/100.0 for value in self.SOC]
        
    # Control de estado de carga del sistema
    def SOCControl(self, SOCref, SOC_0, stepTime): # Ingresa el estado de carga requerido y el inicial en %
        
        self.SOCref = SOCref
        self.SOC_0 = SOC_0
        self.Tcref = []
        self.Tdref = []
        
        for SOC in self.SOCref:
        
            # Definición de modelo
            self.A = (1 - (self.gamma_sd/100)/(720/stepTime))
            self.B = 100 / self.E_b
            self.C = (self.eta_bc/100) * self.P_cMax * stepTime
            self.D = (1 / (self.eta_bd/100)) * self.P_dMax * stepTime
            
            # Definición de función de estado de carga por pasos  
            if (SOC >= SOC_0):
                # Definición de función objetivo de carga
                def objective(x):
                    t = x[0]
                    f = SOC - (SOC_0 * math.pow(self.A,t+1) + (self.C * math.pow(self.A,t) * t ) * self.B)
                    return f
        
                # Definición de restricciones de carga
                def constraint1(x):
                    t = x[0]
                    f = SOC - (SOC_0 * math.pow(self.A,t+1) + (self.C * math.pow(self.A,t) * t ) * self.B)
                    return f
                
                # Valor inicial de tiempo de carga
                x0 = [1.0]
        
                # Límites de tiempo de carga
                bnds = Bounds(0.0, 9999.9)
        
                con1 = {'type': 'eq', 'fun': constraint1}
                cons = [con1]
        
                # Optimización de tiempo de carga por minimización cuadrática secuencial
                solution = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
                
                self.Tcref.append(round(solution.x[0],3))
                self.Tdref.append(0.0)
            
            else:
                # Definición de función objetivo de descarga
                def objective(x):
                    t = x[0]
                    f = SOC - (SOC_0 * math.pow(self.A,t+1) + (- self.D * t / math.pow(self.A,t)) * self.B)
                    return f
        
                # Definición de restricciones de descarga
                def constraint1(x):
                    t = x[0]
                    f = SOC - (SOC_0 * math.pow(self.A,t+1) + (- self.D * t / math.pow(self.A,t)) * self.B)
                    return f
                
                # Valor inicial de tiempo de descarga
                x0 = [1.0]
        
                # Límites de tiempo de descarga
                bnds = Bounds(0.0, 9999.9)
        
                con1 = {'type': 'eq', 'fun': constraint1}
                cons = [con1]
        
                # Optimización de tiempo de descarga por minimización cuadrática secuencial
                solution = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
                
                self.Tcref.append(0.0)
                self.Tdref.append(round(solution.x[0],3))
                
            SOC_0 = SOC
        
        SOC_results = [self.SOC_0] + self.SOCref
        
        return SOC_results, [value * self.E_b/100.0 for value in SOC_results], self.Tcref+[0.0], self.Tdref+[0.0]