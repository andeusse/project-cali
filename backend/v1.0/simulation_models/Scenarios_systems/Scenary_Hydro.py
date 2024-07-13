from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import least_squares
import numpy as np

class Hydro_Model:
    # Inicializacion de sistema de turbinas
    def __init__(self, simulationSteps, N_ht, P_ht, name):
        self.N_ht = N_ht # Numero de turbinas hidraulicas
        self.P_ht = P_ht # Potencia nominal de cada turbina hidraulica
        self.P_max = N_ht * P_ht # Potencia maxima del sistema
        self.P_min = 0 # Potencia minima del sistema
        self.simulationSteps = simulationSteps # Número de pasos de simulación
        self.name = name # Nombre del sistema

    # Parametrizacion de turbinas de acuerdo a tipo
    def turbineType (self, type, n_t = 75, H_min = 3, H_max = 130, Q_min = 0.0001, Q_max = 0.01, f_h = 5.0):
        self.turbineType = type
        
        # Pelton
        if self.turbineType == 1:
            self.n_t = n_t
            self.H_min = 3.0
            self.H_max = 130.0
            self.Q_min = 0.0001
            self.Q_max = 0.01
            self.f_h = 0
        # Turgo
        elif self.turbineType == 2:
            self.n_t = n_t
            self.H_min = 2.0
            self.H_max = 30.0
            self.Q_min = 0.008
            self.Q_max = 0.016
            self.f_h = 0
        # Personalizada
        elif self.turbineType == 0:
            self.n_t = n_t
            self.H_min = H_min
            self.H_max = H_max
            self.Q_min = Q_min
            self.Q_max = Q_max
            self.f_h = 0
        return self.n_t, self.H_min, self.H_max, self.Q_min, self.Q_max , self.f_h
    
    # Parametrizacion de gemelo 
    def twinParameters (self, n_controller, n_inverter):
        self.n_controller = n_controller # Eficiencia controlador en % -> se optomiza con medidas de potencia
        self.n_inverter = n_inverter # Eficiencia de inversor en %
        self.delta_C = 0.6 # Coeficiente de temperatura bateria en %/°C (Se calcula entre 20-30°C)
        self.cap_bat = 150.0 # Capacidad de las baterias en Ah
        self.sigma_bat = 9.6e-7 # Coeficiente de descarga de baterias en %/s (a 20°C)
        self.n_bat = 98.0 # Eficiencia de carga y descarga de la bateria en %
        self.delta_V = -0.06 # Coeficiente de compensación de temperatura V/°C 
        self.chargeMatrix = [[-0.00152, 0.05509, 0.15782], 
                             [0.00165, -0.05758, -0.39049], 
                             [-0.00024, 0.01018, 0.52391], 
                             [-0.00014, 0.00795, 1.86557]]
        
        self.dischargeMatrix = [[0.00130, 0.00093, 0.03533],
                                [-0.00201, -0.00803, -0.08716],
                                [0.00097, 0.00892, 0.22999],
                                [-0.00021, -0.00306, 1.93286]]
     
    # Parametros operativos
    def operativeData (self, type, H = [100], Q = [0.01]):
        self.operativeDataType = type
        
        # Valor fijo ingresado por el usuario
        if self.operativeDataType == 1:
            self.H = H * self.simulationSteps
            self.Q = Q * self.simulationSteps
        # Curva Personalizada
        elif self.operativeDataType == 0:
            self.H = H
            self.Q = Q
        for i in range(len(self.H)):
            if self.H[i] > self.H_max:
                self.H[i] = self.H_max
            elif self.H[i] < self.H_min:
                self.H[i] = self.H_min
            if self.Q[i] > self.Q_max:
                self.Q[i] = self.Q_max
            elif self.Q[i] < self.Q_min:
                self.Q[i] = self.Q_min
        
        return self.H, self.Q
    
    # Calculo de potencia de las turbinas
    def PowerOutput (self):
        #Calculo de potencia de cada turbina kW
        self.P_turbine = [ ((self.n_t/100) * 1000 * 9.8 * self.H[i] * self.Q[i] * (1 - (self.f_h/100)))/1000  for i in range(len(self.H))]
        # Calculo de potencia del sistema en kW
        self.P_h = [round(self.N_ht * i,3) for i in self.P_turbine]
        # Limitación de potencia
        for i in range(len(self.P_h)):
            if self.P_h[i] > self.P_max:
                self.P_h[i] = round(self.P_max,3)

        return self.P_h
    

    def optimal_n_t(self, n_t, P_h_meas, Pressure, Flux):
        def turbinePowerOutput(n_t, P_h_meas, Pressure, Flux):      
            return ((n_t/100) * Pressure * Flux) - P_h_meas
        n_t_0 = [n_t]
        n_t = least_squares(turbinePowerOutput, x0 = n_t_0, bounds = (60, 90), args = (P_h_meas, Pressure, Flux))
        self.n_t = n_t.x[0]
        return n_t.x[0]
    
    def optimal_n_controller(self, n_controller, P_h, P_CD, P_CC_meas):
        def controllerPowerOuput(n_controller, P_h, P_CD, P_CC_meas):
            return (P_h * 1000 * n_controller / 100) - P_CD - P_CC_meas
        n_controller_0 = [n_controller]
        n_controller = least_squares(controllerPowerOuput, x0 = n_controller_0, bounds = (88, 98), args = (P_h, P_CD, P_CC_meas))
        self.n_controller = n_controller.x[0]

        return n_controller.x[0]

    # Calculo de energía generada por las turbinas   
    def EnergyOutput (self, stepTime):
        self.E_h = [0]
        for i in range(len(self.P_h)):
            self.E_h.append(round(self.E_h[i] + self.P_h[i] * stepTime,3))
        self.E_h.pop(0)
        return self.E_h
    
    def twinOutput(self, P_CA, inverterState, PF, P_CD, T_bat, V_CD, SOC_0, V_bulk, V_float, V_charge, sinkState, V_sink_on, V_sink_off, delta_t):
        
        self.inverterState = inverterState
        self.sinkState = sinkState
        self.V_CD = V_CD
        self.P_CA = P_CA
        self.PF = PF
        self.V_sink_on = V_sink_on
        self.V_sink_off = V_sink_off
        
        if self.V_CD <= V_charge or not self.inverterState:
            self.P_CA = 0.0
            self.inverterState = False
        
        self.P_CC = (self.P_h[0] * 1000 * self.n_controller / 100) - P_CD # Potencia a la salida de controlador
        self.S_CA = (self.P_CA / abs(self.PF))
        self.Q_CA = (self.PF / abs(self.PF)) * ((self.S_CA**2 - self.P_CA**2)**(1/2))
        self.P_inv = self.S_CA / (self.n_inverter / 100) # Potencia a la entrada del inversor
        
        if self.sinkState: 
            self.P_sink = self.V_CD**2 / 0.8
        else:
            self.P_sink = 0.0
                      
        # Balance de potencias
        self.P_bat = self.P_CC - self.P_inv - self.P_sink # Potencia de la bateria, + carga, - descarga
        
        # Corriente de la batería
        self.I_bat = self.P_bat / self.V_CD
        
        # Corrección de capacidad por temperatura
        self.corrected_cap_bat = self.cap_bat * (1 + (self.delta_C / 100) * (T_bat - 25))
        
        # Cálculo de parámetros A, B, C y D    
        if self.P_bat > 0:
            ABCD = np.dot(self.chargeMatrix, [self.I_bat**2, self.I_bat, 1])
        elif self.P_bat <= 0:
            ABCD = np.dot(self.dischargeMatrix, [abs(self.I_bat)**2, abs(self.I_bat), 1])
        
        # Estimación de SOC inicial a partir del voltaje
        # SOC_0 = float(np.polynomial.polynomial.Polynomial([ ABCD[3] - (V_meas - self.delta_V * (T_bat - 25)) / 12, ABCD[2], ABCD[1], ABCD[0]]).roots()[0])
        
        # Cálculo de nuevo SOC
        self.SOC = (SOC_0/100) * (1 - (self.sigma_bat * delta_t / 100) ) + ((self.I_bat * delta_t * self.n_bat / 100) / (self.corrected_cap_bat * 3600)) 
                    
        # Cálculo de voltaje de batería
        self.V_bat = 12 * np.dot(ABCD, [self.SOC**3, self.SOC**2, self.SOC, 1]) + self.delta_V * (T_bat - 25)
        
        if self.SOC > 1.0:
            self.SOC = 1.0
        
        # Actualización de voltaje de CD
        if self.P_bat > 0 and self.V_bat < V_bulk:
            self.V_CD = V_bulk
        elif self.P_bat > 0 and self.V_bat >= V_bulk:
            self.V_CD = V_float
        else: 
            self.V_CD = self.V_bat
            
       # Lógica de la disipación
        # Lógica de la disipación
        if self.V_bat > self.V_sink_on: # Cambiar por condición de voltaje
            self.sinkState = True 
        elif self.V_bat < self.V_sink_off:
            self.sinkState = False
        
        # # Corriente actualizada de la batería
        # self.I_bat = self.P_bat / self.V_CD
        
        # # Potencia actualizada de la disipación
        # if self.P_sink > 0:
        #     self.P_sink = self.V_CD**2 / 0.8
        
        # # SOC actualizado con corriente
        # self.SOC = (SOC_0) * (1 - (self.sigma_bat * delta_t / 100) ) + ((self.I_bat * delta_t * self.n_bat / 100) / (self.corrected_cap_bat * 3600))
        
        return round(self.P_CC,2), round(self.P_inv,2), round(self.P_bat,2), round(self.I_bat,2), round(self.SOC*100,3), round(self.V_bat,3), round(self.V_CD,2), self.sinkState, round(self.P_sink,2), round(self.S_CA,2), round(self.P_CA,2), round(self.Q_CA,2), self.inverterState

    # Control de potencia del sistema
    def PowerControl(self, Pref, Href): # Ingresa la potencia requerida en kW y cabeza de operación
        
        self.Pref = Pref
        self.Href = Href
        self.Qref = []
        
        for i in range(len(self.Pref)):
            
            if self.Pref[i] > self.P_max:
                self.Pref[i] = self.P_max
        
            # Definición de modelo
            self.A = self.N_ht * (self.n_t/100) * 1000 * 9.8 * self.Href[i]
            self.B = (1 - (self.f_h/100)) / 1000
    
            # Definición de función objetivo
            def objective(x):
                Q = x[0]
                f = self.Pref[i] - self.A * self.B * Q
                return f
    
            # Definición de restricciones
            def constraint1(x):
                Q = x[0]
                f = self.Pref[i] - self.A * self.B * Q
                return f
            
            # Valor inicial de flujo de agua
            x0 = [0.01]
    
            # Límites de flujo de agua
            bnds = Bounds(self.Q_min, self.Q_max)
    
            con1 = {'type': 'eq', 'fun': constraint1}
            cons = [con1]
    
            # Optimización de flujo de agua por minimización cuadrática secuencial
            solution = minimize(objective, x0, method = 'SLSQP', bounds = bnds, constraints = cons)
            
            self.Qref.append(round(solution.x[0],4))
        
        return self.Qref