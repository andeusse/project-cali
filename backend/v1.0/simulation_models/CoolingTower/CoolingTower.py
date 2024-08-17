
from simulation_models.CoolingTower import PengRobinson as PR
from scipy.optimize import fsolve
import numpy as np

class coolingTowerModel:
    def __init__ (self, L, A, epsilon, dp):  #L: Largo de la torre en metros, A: area transversal de la torre en metros cuadrados, epsilon: Porosidad de la torre, dp: Diametro de las partículas del lecho (m)
        self.L = L
        self.epsilon = epsilon
        self.dp = dp
        self.A = A
    
    def towerBalance (self, T_Lin, P_atm, Fv_Lin, T_vin, Fv_vin, RH_air_in):
        self.T_Lin = T_Lin              #Temperatura agua caliente a la entrada [K]
        self.P_atm = P_atm              #Presión atmosférica                    [Pa]
        self.Fv_Lin = Fv_Lin            #Flujo volumétrico de agua a la entrada [m3/s] 
        self.T_vin = T_vin              #Temperatura de entrada aire            [K]   
        self.Fv_vin = Fv_vin            #Flujo volumétrico de aire a la entrada [m3/s]
        self.RH_air_in = RH_air_in      #Humedad relativa del aire a la entrada [%] (numero 60% es 60)
        self.u = self.Fv_vin/self.A
        Air_in = PR.EosPengRobinson()
        Air_out = PR.EosPengRobinson()
        Water_in = PR.EosPengRobinson()
        Water_out = PR.EosPengRobinson()
        
        Air_in.AirCompositions_in(T = self.T_vin, RH = RH_air_in, P = self.P_atm)
        Air_in.Z_mix()
        Air_in.MolarVolume()
        Air_in.fugacity()
        Air_in.Enthalpy()

        Water_in.WaterComposition(T = self.T_Lin, P = self.P_atm, xH2O = 1, x_N2 = 0, x_O2 = 0)
        Water_in.Z_mix()
        Water_in.MolarVolume()
        Water_in.fugacity()
        Water_in.Enthalpy()

        def systemequations (vars):
            N_H2O_l_out, N_H2O_v_out, N_O2_l_out, N_O2_v_out, N_N2_l_out, N_N2_v_out, Ttop = vars
            
            N_l_out = N_H2O_l_out + N_O2_l_out + N_N2_l_out
            N_v_out = N_H2O_v_out + N_O2_v_out + N_N2_v_out
            
            x_H2O_l_out = N_H2O_l_out / N_l_out
            x_O2_l_out = N_O2_l_out / N_l_out
            x_N2_l_out = N_N2_l_out / N_l_out
            
            x_H2O_v_out = N_H2O_v_out / N_v_out
            x_O2_v_out = N_O2_v_out / N_v_out
            x_N2_v_out = N_N2_v_out / N_v_out

            Water_out.WaterComposition(T = Ttop, P=self.P_atm, xH2O = x_H2O_l_out, x_O2 = x_O2_l_out, x_N2 = x_N2_l_out)
            Water_out.Z_mix()
            Water_out.fugacity()
            Water_out.Enthalpy()

            Air_out.AirComposition_out(T = Ttop, P = self.P_atm, x_H2O = x_H2O_v_out, x_O2 = x_O2_v_out, x_N2 = x_N2_v_out)
            Air_out.Z_mix()
            Air_out.fugacity()
            Air_out.Enthalpy()

            #Moles de agua que entran
            N_l_in = self.Fv_Lin / Water_in.Vm_mix_l
            N_H2O_l_in = N_l_in * Water_in.x_H2O
            N_O2_l_in = N_l_in  * Water_in.x_O2
            N_N2_l_in = N_l_in * Water_in.x_N2

            #Moles de aire que entras
            N_v_in = self.Fv_vin / Air_in.Vm_mix_v
            N_H2O_v_in = N_v_in * Air_in.x_H2O
            N_O2_v_in = N_v_in  * Air_in.x_O2
            N_N2_v_in = N_v_in * Air_in.x_N2

            #Balances de Materia
            H2O = (N_H2O_l_in + N_H2O_v_in) - (N_H2O_l_out +  N_H2O_v_out)
            O2 = (N_O2_l_in + N_O2_v_in) - (N_O2_l_out + N_O2_v_out)
            N2 = (N_N2_l_in + N_N2_v_in) - (N_N2_l_out + N_N2_v_out)

            #Balance de energía
            Energia = (N_l_in * Water_in.H_l + N_v_in * Air_in.H_v) - (N_l_out * Water_out.H_l + N_v_in * Air_out.H_v)

            #Equilibrio
            EqH2O = (Air_out.x_H2O * Air_out.phi_v['H2O']) - (Water_out.x_H2O * Water_out.phi_l['H2O'])
            EqO2 = (Air_out.x_O2 * Air_out.phi_v['O2']) - (Water_out.x_O2 * Water_out.phi_l['O2'])
            EqN2 = (Air_out.x_N2 * Air_out.phi_v['N2']) - (Water_out.x_N2 * Water_out.phi_l['N2'])
             

            return H2O, O2, N2, Energia, EqH2O, EqO2, EqN2
        
        initial_values = [1, 0.01, 0.01, 0.21, 0.0001, 0.79, 300]
        numpysolution = fsolve(systemequations, initial_values)

        N_out_v = numpysolution[1] + numpysolution[3] + numpysolution[5] 
        xH2O_v_out = numpysolution[1]/N_out_v
        x_O2_v_out = numpysolution[3]/N_out_v
        x_N2_v_out = numpysolution[5]/N_out_v
        Ttop = numpysolution[6] - abs(np.random.normal(1.3,0.01))


        Air_out.relativeHumidityTop(x_H2O=xH2O_v_out, x_O2=x_O2_v_out, x_N2=x_N2_v_out, T=Ttop)
        self.RH_v_out = Air_out.RH
        self.w_v_out = Air_out.w
        self.solution = list(numpysolution)
        self.solution.append(T_vin + abs(np.random.normal(0.5,0.01)))
        self.solution.append(self.RH_v_out)

        powerBalance = (self.Fv_Lin / Water_in.Vm_mix_l)*(Water_in.H_l - Water_out.H_l)
        self.solution.append(powerBalance)
        
        

        
        
   
            
            



