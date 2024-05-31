import math
from scipy.optimize import minimize
from scipy.optimize import Bounds
from scipy.optimize import least_squares
import numpy as np
import random

class TwinPVWF:
    def __init__(self, systemName):
        self.systemName = systemName # Nombre del sistema
        self.monoModule = False
        self.polyModule = False
        self.flexiModule = False
        self.cdteModule = False
        self.f_PV = 1.0
        self.n_WT = 1.0
        self.Vmpp_monoModule = 17.08
        self.Vmpp_polyModule = 16.85
        self.Vmpp_flexiModule = 18.0
        self.Vmpp_cdteModule = 43.6

    # Parametrizacion de modulo de acuerdo a tipo
    def moduleType(self, type):
        # Silicio Monocristalino
        if type == 1:
            self.P_PM = 100.0
            self.G_0 = 1000
            self.u_PM = -0.39
            self.T_cSTC = 25
            self.T_cNOCT = 45
            self.T_aNOCT = 20
            self.G_NOCT = 800
            self.n_c = 15.44
            self.monoModule = True
        # Silicio Policristalino
        elif type == 2:
            self.P_PM = 100.0
            self.G_0 = 1000
            self.u_PM = -0.39
            self.T_cSTC = 25
            self.T_cNOCT = 45
            self.T_aNOCT = 20
            self.G_NOCT = 800
            self.n_c = 15.44
            self.polyModule = True
        # Silicio Monocristalino de Pelicula Delgada
        elif type == 3:
            self.P_PM = 100.0
            self.G_0 = 1000
            self.u_PM = -0.42
            self.T_cSTC = 25
            self.T_cNOCT = 45
            self.T_aNOCT = 20
            self.G_NOCT = 800
            self.n_c = 15.43
            self.flexiModule = True
        # Telururo de Cadmio    
        elif type == 4:
            self.P_PM = 77.5
            self.G_0 = 1000
            self.u_PM = -0.25
            self.T_cSTC = 25
            self.T_cNOCT = 42
            self.T_aNOCT = 20
            self.G_NOCT = 800
            self.n_c = 11.0
            self.cdteModule = True
        
        return self.f_PV, self.G_0, self.u_PM, self.T_cSTC, self.T_cNOCT, self.T_aNOCT, self.G_NOCT, self.n_c
    
    # Calculo de potencia del sistema
    def PV_PowerOutput(self):
        # Calculo de temperatura del modulo
        self.T_cm = round((self.T_a + self.G * ((self.T_cNOCT-self.T_aNOCT) / self.G_NOCT) * (1 - ((self.n_c/100) / 0.9))), 4)
        # Calculo de potencia de cada modulo
        self.P_PVm = (self.f_PV * (self.G / self.G_0) * self.P_PM * (1 + ((self.u_PM/100) * (self.T_cm - self.T_cSTC))))
        return self.P_PVm, self.T_cm
    
    # Calculo de potencia del sistema
    def WT_PowerOutput(self, turbineState, ro, V_a):
        self.turbineState = turbineState
        self.ro = ro
        self.V_a = V_a
        self.P_WM = 200.0
        self.H_R = 1
        self.H_A = 1
        self.Z_0 = 0.03
        self.V_C = 2.0
        self.V_N = 11.5
        self.V_F = 65.0
        self.diameter = 1.24
        if not turbineState or self.cdteModule or not self.parallel:
            self.P_WT = 0.0
        else:
            # Calculo de velocidad ajustada por altura
            self.V_r = self.V_a * (math.log(self.H_R/self.Z_0, math.e) / math.log(self.H_A/self.Z_0, math.e))
            #Calculo de potencia de cada aero generador
            if (self.V_r > self.V_C and self.V_r < self.V_N):
                P_wtSTP = self.n_WT * self.P_WM * (((self.V_r**2) - (self.V_C**2)) / ((self.V_N**2) - (self.V_C**2)))
            elif (self.V_r >= self.V_N and self.V_r < self.V_F):
                P_wtSTP = self.n_WT * self.P_WM
            elif (self.V_r <= self.V_C or self.V_r >= self.V_F):
                P_wtSTP = 0
            # Ajuste de potencia por densidad de aire
            self.P_WT = (self.ro / 1.225) * P_wtSTP
        return round(self.P_WT,2)
    
    def arrayPowerOutput(self, monoModule, polyModule, flexiModule, cdteModule, T_a, G_1, G_2):
        self.monoModule = monoModule
        self.polyModule = polyModule
        self.flexiModule = flexiModule
        self.cdteModule = cdteModule
        self.T_a = T_a
        self.G_1 = G_1
        self.G_2 = G_2
        self.P_PV = 0.0
        
        self.Tc_mono = T_a
        self.Tc_poly = T_a
        self.Tc_flexi = T_a
        self.Tc_cdte = T_a

        if cdteModule:
                self.moduleType(4)
                self.G = G_2
                self.P_PV += self.PV_PowerOutput()[0]
                self.Tc_cdte = self.PV_PowerOutput()[1]
        else:
            if monoModule:
                self.moduleType(1)
                self.G = G_1
                self.P_PV += self.PV_PowerOutput()[0]
                self.Tc_mono = self.PV_PowerOutput()[1]

            if polyModule:
                self.moduleType(2)
                self.G = G_1
                self.P_PV += self.PV_PowerOutput()[0]
                self.Tc_poly = self.PV_PowerOutput()[1]
            
            if flexiModule:
                self.moduleType(3)
                self.G = G_2
                self.P_PV += self.PV_PowerOutput()[0]
                self.Tc_flexi = self.PV_PowerOutput()[1]

        return self.P_PV, self.Tc_mono, self.Tc_poly, self.Tc_flexi, self.Tc_cdte

    # Parametrizacion de gemelo 
    def twinParameters (self, n_controller, n_inverter, n_hybrid, batteries, parallel):
        self.parallel = parallel
        self.n_controller = n_controller # Eficiencia controlador en % -> se optomiza con medidas de potencia
        self.n_inverter = n_inverter # Eficiencia de inversor en %
        self.n_hybrid = n_hybrid # Eficiencia de inversor hibrido en %
        self.delta_C = 0.6 # Coeficiente de temperatura bateria en %/°C (Se calcula entre 20-30°C)
        self.sigma_bat = 9.6e-7 # Coeficiente de descarga de baterias en %/s (a 20°C)
        self.n_bat = 98.0 # Eficiencia de carga y descarga de la bateria en %
        self.chargeMatrix = [[-0.00152, 0.05509, 0.15782], 
                             [0.00165, -0.05758, -0.39049], 
                             [-0.00024, 0.01018, 0.52391], 
                             [-0.00014, 0.00795, 1.86557]]
        
        self.dischargeMatrix = [[0.00130, 0.00093, 0.03533],
                                [-0.00201, -0.00803, -0.08716],
                                [0.00097, 0.00892, 0.22999],
                                [-0.00021, -0.00306, 1.93286]]
        if self.parallel:
            if batteries == 1:
                self.cap_bat = 50.0 # Capacidad de las baterias en Ah
                self.delta_V = -0.015 # Coeficiente de compensación de temperatura V/°C
                self.chargeCurrent = 12.5 # Corriente de carga máxima
            else:
                self.cap_bat = 100.0 # Capacidad de las baterias en Ah
                self.delta_V = -0.015 # Coeficiente de compensación de temperatura V/°C
                self.chargeCurrent = 25.0 # Corriente de carga máxima
        else:
            self.cap_bat = 100.0 # Capacidad de las baterias en Ah
            self.delta_V = -0.03 # Coeficiente de compensación de temperatura V/°C
            self.chargeCurrent = 12.5 # Corriente de carga máxima

    def optimal_f_PV(self, P_PV_meas):
        def optimal_PV_PowerOutput(f_PV, P_PV_meas):
            self.f_PV = f_PV[0]
            return self.arrayPowerOutput(self.monoModule, self.polyModule, self.flexiModule, self.cdteModule, self.T_a, self.G_1, self.G_2)[0] - P_PV_meas
        f_PV_0 = 1.0
        f_PV = least_squares(optimal_PV_PowerOutput, x0 = f_PV_0, bounds = (0.8, 1.2), args = [P_PV_meas])
        self.f_PV = f_PV.x[0]*random.uniform(0.98,1.02)
        return f_PV.x[0]
    
    def optimal_n_WT(self, P_WT_meas):
        def optimal_WT_PowerOutput(n_WT, P_WT_meas):
            self.n_WT = n_WT[0]
            return self.WT_PowerOutput(self.turbineState, self.ro, self.V_a) - P_WT_meas
        n_WT_0 = 1.0
        n_WT = least_squares(optimal_WT_PowerOutput, x0 = n_WT_0, bounds = (0.8, 1.2), args = [P_WT_meas])
        self.n_WT = n_WT.x[0]*random.uniform(0.98,1.02)
        return n_WT.x[0]
    
    def optimal_n_controller(self, P_CD, P_CC_meas):
        def controllerPowerOuput(n_controller, P_CD, P_CC_meas):
            self.n_controller = n_controller[0]
            return ((self.P_PV + self.P_WT) * self.n_controller / 100) - (P_CD / (self.n_controller / 100)) - P_CC_meas
        n_controller_0 = self.n_controller
        n_controller = least_squares(controllerPowerOuput, x0 = n_controller_0, bounds = (80.0, 98.0), args = (P_CD, P_CC_meas))
        self.n_controller = n_controller.x[0]
        return n_controller.x[0]
    
    def offgridTwinOutput(self, inverterState, P_CA, PF, P_CD, T_bat, V_CD, SOC, V_bulk, V_float, V_charge, V_PV, V_WT, V_CDload, V_CA, delta_t):
        
        self.inverterState = inverterState
        self.V_CD = V_CD
        self.PF = PF
        self.P_CD = P_CD

        if V_PV == 0.0:
            if self.cdteModule:
                self.V_PV = self.Vmpp_cdteModule
            elif self.parallel:
                self.V_PV = max(self.monoModule * self.Vmpp_monoModule, self.polyModule * self.Vmpp_polyModule, self.flexiModule * self.Vmpp_flexiModule)
            else:
                self.V_PV = self.monoModule * self.Vmpp_monoModule + self.polyModule * self.Vmpp_polyModule + self.flexiModule * self.Vmpp_flexiModule
        else:
            self.V_PV = V_PV
        
        if V_WT == 0.0:
            self.V_WT = 12.0
        else:
            self.V_WT = V_WT
        
        if V_CDload == 0.0:
            self.V_CDload = 12.0
        else:
            self.V_CDload = V_CDload
            
        if V_CA == 0.0:
            self.V_CA = 120.0
        else:
            self.V_CA = V_CA

        if self.cdteModule or not self.parallel:
            self.P_CA = P_CA
        else:
            self.inverterState = False
        
        if self.V_CD <= V_charge or not self.inverterState:
            self.P_CA = 0.0
            self.inverterState = False
        
        # if ((self.P_PV + self.P_WT) * self.n_controller / 100) < (self.P_CD / (self.n_controller / 100)):
        #     self.P_CD = 0.0
        
        self.P_CC = ((self.P_PV + self.P_WT) * self.n_controller / 100) - (self.P_CD / (self.n_controller / 100)) # Potencia a la salida de controlador
        self.S_CA = (self.P_CA / abs(self.PF)) # Potencia aparente a la salida del inversor
        self.Q_CA = (self.PF / abs(self.PF)) * ((self.S_CA**2 - self.P_CA**2)**(1/2)) # Potencia reactiva a la salida del inversor
        self.P_inv = self.S_CA / (self.n_inverter / 100) # Potencia a la entrada del inversor
                      
        # Balance de potencias
        self.P_bat = self.P_CC - self.P_inv # Potencia de la bateria, + carga, - descarga
        
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
        # SOC = float(np.polynomial.polynomial.Polynomial([ ABCD[3] - (V_meas - self.delta_V * (T_bat - 25)) / 12, ABCD[2], ABCD[1], ABCD[0]]).roots()[0])
        
        # Cálculo de nuevo SOC
        self.SOC = (SOC/100) * (1 - (self.sigma_bat * delta_t / 100) ) + ((self.I_bat * delta_t * self.n_bat / 100) / (self.corrected_cap_bat * 3600)) 
        
        # Cálculo de voltaje de batería
        if self.parallel:
            self.V_bat = 6 * np.dot(ABCD, [self.SOC**3, self.SOC**2, self.SOC, 1]) + self.delta_V * (T_bat - 25)
        else:
            self.V_bat = 12 * np.dot(ABCD, [self.SOC**3, self.SOC**2, self.SOC, 1]) + self.delta_V * (T_bat - 25)
        
        if self.SOC > 1.0:
            self.SOC = 1.0
            self.P_bat = (self.sigma_bat * delta_t / 100)
            self.I_bat = self.P_bat / self.V_CD
            self.P_CC = self.P_bat + self.P_inv
        
        # Actualización de voltaje de CD
        if self.P_bat > 0 and self.V_bat < V_bulk:
            self.V_CD = V_bulk
        elif self.P_bat > 0 and self.V_bat >= V_bulk:
            self.V_CD = V_float
        else: 
            self.V_CD = self.V_bat
        
        if self.V_PV > 0.0:
            self.I_PV = self.P_PV / self.V_PV
        else:
            self.I_PV = 0.0
        self.I_WT = self.P_WT / (self.V_WT * ((3)**(1/2)))
        self.I_CD = self.P_CD / self.V_CDload
        self.I_CC = self.P_CC / self.V_CD
        self.I_CA = self.S_CA / self.V_CA
        self.I_inv = self.P_inv / self.V_CD
        
        return round(self.P_CC,2), round(self.P_inv,2), round(self.P_bat,2), round(self.V_PV,2), round(self.V_WT,2), round(self.V_CDload,2), round(self.SOC*100,3), round(self.V_bat,3), round(self.V_CD,2), round(self.V_CA,2), round(self.S_CA,2), round(self.P_CA,2), round(self.Q_CA,2), round(self.P_CD,2), self.inverterState, round(self.I_PV,2), round(self.I_WT,2), round(self.I_CD,2), round(self.I_CC,2), round(self.I_bat,2), round(self.I_CA,2), round(self.I_inv,2)
    
    
    def ongridTwinOutput(self, gridState, P_CA, PF, T_bat, V_CD, SOC, V_bulk, V_float, V_charge, chargeCycle, V_PV, V_grid, V_CA, delta_t):
        
        self.gridState = gridState
        self.P_CA = P_CA
        self.V_CD = V_CD
        self.PF = PF
        if V_PV == 0.0:
            self.V_PV = self.monoModule * self.Vmpp_monoModule + self.polyModule * self.Vmpp_polyModule + self.flexiModule * self.Vmpp_flexiModule
        else:
            self.V_PV = V_PV
        
        if V_grid == 0.0:
            self.V_grid = 120.0
        else:
            self.V_grid = V_grid
        
        if V_CA == 0.0:
            self.V_CA = 120.0
        else:
            self.V_CA = V_CA
        
        if SOC >= 100.0:
            chargeCycle = False

        self.S_CA = (self.P_CA / abs(self.PF)) # Potencia aparente a la salida del inversor
        self.Q_CA = (self.PF / abs(self.PF)) * ((self.S_CA**2 - self.P_CA**2)**(1/2)) # Potencia reactiva a la salida del inversor
        self.P_inv = self.S_CA / (self.n_hybrid / 100) # Potencia a la entrada del inversor

        if self.gridState:            
            self.P_bat = self.V_CD * self.chargeCurrent
            chargeCycle = True
            
            if SOC >= 100.0:
                self.P_bat = 0.0
                chargeCycle = False

            self.P_grid = self.P_inv + self.P_bat - (self.P_PV * self.n_hybrid / 100)
            # Corriente de la batería
            self.I_bat = self.P_bat / self.V_CD
        else:
            self.P_grid = 0.0
            self.P_bat = (self.P_PV * self.n_hybrid / 100) - self.P_inv # Potencia de la bateria, + carga, - descarga
            if SOC > 50.0 and chargeCycle:
                chargeCycle = False
            if SOC <= 50.0 and chargeCycle and self.P_bat < 0.0:
                self.P_bat = 0.0
                self.P_inv = 0.0
                self.P_CA = 0.0
                self.Q_CA = 0.0
                self.S_CA = 0.0
            if self.V_CD <= V_charge and self.P_bat < 0.0:
                chargeCycle = True
                self.P_bat = (self.P_PV * self.n_hybrid / 100)
                self.P_inv = 0.0
                self.P_CA = 0.0
                self.Q_CA = 0.0
                self.S_CA = 0.0
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
        # SOC = float(np.polynomial.polynomial.Polynomial([ ABCD[3] - (V_meas - self.delta_V * (T_bat - 25)) / 12, ABCD[2], ABCD[1], ABCD[0]]).roots()[0])
        
        # Cálculo de nuevo SOC
        self.SOC = (SOC/100) * (1 - (self.sigma_bat * delta_t / 100) ) + ((self.I_bat * delta_t * self.n_bat / 100) / (self.corrected_cap_bat * 3600)) 
                    
        # Cálculo de voltaje de batería
        self.V_bat = 12 * np.dot(ABCD, [self.SOC**3, self.SOC**2, self.SOC, 1]) + self.delta_V * (T_bat - 25)
        
        if self.SOC > 1.0:
            self.SOC = 1.0
            self.P_bat = (self.sigma_bat * delta_t / 100)
            self.I_bat = self.P_bat / self.V_CD
        
        # Actualización de voltaje de CD
        if self.P_bat > 0 and self.V_bat < V_bulk:
            self.V_CD = V_bulk
        elif self.P_bat > 0 and self.V_bat >= V_bulk:
            self.V_CD = V_float
        else: 
            self.V_CD = self.V_bat

        if self.V_PV > 0.0:
            self.I_PV = self.P_PV / self.V_PV
        else:
            self.I_PV = 0.0
        self.I_grid = self.P_grid / self.V_grid
        self.I_CA = self.S_CA / self.V_CA
        
        return round(self.P_grid,2), round(self.P_inv,2), round(self.P_bat,2), round(self.V_grid,2), round(self.V_PV,2), round(self.SOC*100,3), round(self.V_bat,3), round(self.V_CD,2), round(self.V_CA,2), round(self.S_CA,2), round(self.P_CA,2), round(self.Q_CA,2), self.gridState, chargeCycle, round(self.I_PV,2), round(self.I_bat,2), round(self.I_grid,2), round(self.I_CA,2)
    