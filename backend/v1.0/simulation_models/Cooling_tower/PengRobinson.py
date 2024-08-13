import numpy as np
import scipy.integrate as integrate

class EosPengRobinson:
    def __init__ (self):
        self.components = {'H2O': {'Tc': 647.1, 'Pc': 22.064e6, 'omega': 0.344},
                            'O2': {'Tc': 154.6, 'Pc': 5.043e6, 'omega': 0.022},
                            'N2': {'Tc': 126.2, 'Pc': 3.395e6, 'omega': 0.04}}
        self.kij = np.array([[0, 0.3, 0.1241006],[0.3, 0, 0.3],[0.1241006, 0.3, 0]])  #interaction coefficients
        self.R = 8.314                                                              #Universal constans of gases [j/molK]
        self.Tref = 298.15                                                          #standard reference temperature
        self.Cp = {'H2O': {'A':32.24, 'B': 1.92E-3, 'C':1.055E-5, 'D': -3.59E-9},
                   'O2': {'A':2.811E+1, 'B': -3.68E-6, 'C':1.746E-5, 'D': -1.065E-8},
                   'N2': {'A':3.115E+1, 'B': -1.357E-2, 'C': 2.680E-5, 'D': -1.168E-8}}
        self.component_list = ['H2O', 'O2', 'N2'] 

    def AirCompositions (self, T, RH, P):
        self.T = T        #Kelvin
        self.RH = RH      #percentage 
        self.P = P        #Pascal absolute pressure

        Tcel = self.T - 273.15
        Psat = 6.1078*10**((12.27*Tcel)/(Tcel + 273.15))   #This units are in hPa
        Psat = Psat * 100                                  #convert pressure to Pa  
        P_H2O = self.RH/100 * Psat
        self.w = 0.622 * (P_H2O)/(self.P + P_H2O)               #kgH2O / kgdry air
        
        #Basis 100 estimation of air composition
        w_air = 100/(self.w + 1)
        w_H2O = self.w*w_air
        self.x_H2O =   w_H2O/(w_air + w_H2O)
        self.x_O2 = (w_air/(w_air + w_H2O))*0.21
        self.x_N2 = (w_air/(w_air + w_H2O))*0.79
        self.MW_air = 18.01528*self.x_H2O + 32*self.x_O2 + 28*self.x_N2
        self.x = {'H2O': self.x_H2O, 'O2': self.x_O2, 'N2': self.x_N2}
    
    def WaterComposition (self, T, P):
        self.T = T        #Kelvin
        self.P = P        #Pascal

        self.x_H2O = 1
        self.x_O2 = 0
        self.x_N2 = 0
        self.MW_H2O = 18.01528*self.x_H2O + 32*self.x_O2 + 28*self.x_N2
        self.x = {'H2O': self.x_H2O, 'O2': self.x_O2, 'N2': self.x_N2}

    def  Z_mix (self):
        def a_i (T, Tc, Pc, omega):
            a_c = 0.45724 * (self.R ** 2) * (Tc ** 2) / Pc
            kappa = 0.37464 + 1.54226 * omega - 0.26992 * (omega ** 2)
            return a_c * (1 + kappa * (1 - np.sqrt(T / Tc)))**2
        
        def b_i (Tc, Pc):
            return 0.07789 * self.R * Tc / Pc
        
        def cubic_eq (A, B):
            c2 = B - 1
            c1 = A - 3 * B ** 2 - 2 * B
            c0 = B ** 3 + B ** 2 - A * B
            Z_roots = np.roots([1, c2, c1, c0])
            Z_roots = Z_roots[np.isreal(Z_roots)]
            Z_roots = np.real(Z_roots)
            Z_l = min(Z_roots)
            Z_v = max(Z_roots)
            return (Z_l, Z_v)
        
        self.a = {}
        self.b = {}
        for comp in self.components:
            self.a[comp] = a_i(self.T, self.components[comp]['Tc'], self.components[comp]['Pc'], self.components[comp]['omega'])
            self.b[comp] = b_i(self.components[comp]['Tc'], self.components[comp]['Pc'])
        
        #Calculate mixture parameters
        self.a_mix = sum([self.x[i] * self.x[j] * np.sqrt(self.a[i] * self.a[j]) * (1 - self.kij[self.component_list.index(i)][self.component_list.index(j)]) for i in self.components for j in self.components])
        self.b_mix = sum([self.x[i] * self.b[i] for i in self.components])

        self.A_mix = self.a_mix * self.P / (self.R ** 2 * self.T ** 2)
        self.B_mix = self.b_mix * self.P / (self.R * self.T)

        self.Z_l, self.Z_v = cubic_eq (self.A_mix, self.B_mix)
    
    def fugacity (self):
        
        def fugacity_coeff(Z, A, B, a, b, a_mix, b_mix, P, T):
            term1 = b / b_mix * (Z - 1)
            term2 = np.log(Z - B)
            term3 = A / (2 * np.sqrt(2) * B) * (2 * np.sqrt(a / a_mix) - b / b_mix) * \
                    np.log((Z + (1 + np.sqrt(2)) * B) / (Z + (1 - np.sqrt(2)) * B))
            ln_phi = term1 - term2 - term3
            return np.exp(ln_phi)
        
        phi_l = {comp: fugacity_coeff(self.Z_l, self.A_mix, self.B_mix, self.a[comp], self.b[comp], self.a_mix, self.b_mix, self.P, self.T) for comp in self.x}
        phi_v = {comp: fugacity_coeff(self.Z_v, self.A_mix, self.B_mix, self.a[comp], self.b[comp], self.a_mix, self.b_mix, self.P, self.T) for comp in self.x}
        self.phi_l = phi_l
        self.phi_v = phi_v
        self.f_l = {comp: self.x[comp] * phi_l[comp] * self.P for comp in self.x}
        self.f_v = {comp: self.x[comp] * phi_v[comp] * self.P for comp in self.x}
    
    def Enthalpy (self):

        def H_ig (T, A, B, C, D):
            return A + B*T + C*T**2 + D*T**3
        
        T_ref = 298.15    #kelvin

        H_igs = {}
        for component, coefficients in self.Cp.items():
            A = coefficients['A']
            B = coefficients['B']
            C = coefficients['C']
            D = coefficients['D']
            integral_result, error = integrate.quad(H_ig, T_ref, self.T, args=(A, B, C, D))
            H_igs[component] = integral_result
        
        H_ig_mix = sum(self.x[comp] * H_igs[comp] for comp in self.x)
        
        def H_dep(Z, A, B, T):
            return self.R * T * (Z - 1 - A / (2 * np.sqrt(2) * B) * np.log((Z + (1 + np.sqrt(2)) * B) / (Z + (1 - np.sqrt(2)) * B)))
        
        H_dep_l = H_dep(self.Z_l, self.A_mix, self.B_mix, self.T)
        H_dep_v = H_dep(self.Z_v, self.A_mix, self.B_mix, self.T)

        self.H_l = H_ig_mix + H_dep_l
        self.H_v = H_ig_mix + H_dep_v
    
    def ergun_preddure_drop (self, L, mu, epsilon, U, dp):
        self.Vm_mix_l = self.Z_l * self.R * self.T / self.P


        




    

        



        
    
    

        










            
            



        

        