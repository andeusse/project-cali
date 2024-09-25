from simulation_models.CoolingTower import PengRobinson as PR
# import PengRobinson as PR               #Delete or comment After test              
from scipy.optimize import fsolve
from scipy.optimize import minimize
import numpy as np
import psychrolib

class coolingTowerModel:
    def __init__ (self, PackedType, L, A):  #L: Largo de la torre en metros, A: area transversal de la torre en metros cuadrados, epsilon: Porosidad de la torre, dp: Diametro de las partículas del lecho (m)
        self.PacketType = PackedType
        self.L = L
        self.A = A
        self.PacketType = PackedType
        if PackedType == "Structured":
            self.epsilon = 0.15
            self.dp = 0.01
        if PackedType == "CurvedSlats":
            self.epsilon = 0.08
            self.dp = 0.0058
        if PackedType == "FlatSlats":
            self.epsilon = 0.1
            self.dp = 0.0085    

    def towerBalance (self, T_Lin, P_atm, Fv_Lin, T_vin, Fv_vin, RH_air_in):
        self.T_Lin = T_Lin              #Temperatura agua caliente a la entrada [K]
        self.P_atm = P_atm              #Presión atmosférica                    [Pa]
        self.Fv_Lin = Fv_Lin            #Flujo volumétrico de agua a la entrada [m3/s] 
        self.T_vin = T_vin              #Temperatura de entrada aire            [K]   
        self.Fv_vin = Fv_vin            #Flujo volumétrico de aire a la entrada [m3/s]
        self.RH_air_in = RH_air_in      #Humedad relativa del aire a la entrada [%] (valor entre 0 y 1)
        self.u_air = self.Fv_vin/self.A
        self.u_water = self.Fv_Lin/self.A

        def systemOneStage (vars):
            NL1_H2O, NL1_O2, NL1_N2, NV1_H2O, NV1_O2, NV1_N2, T1 = vars    #vars for stage 1

            ##Liquid currents
            #Current L0
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T = self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = self.Fv_Lin / Water_0.Vm_mix_l
            NL0_H2O = NL0 * Water_0.x_H2O
            NL0_O2 = NL0 * Water_0.x_O2
            NL0_N2 = NL0 * Water_0.x_N2

            #Current L1
            NL1 = NL1_H2O + NL1_O2 + NL1_N2
            xL1_H2O = NL1_H2O / NL1
            xL1_O2 = NL1_O2 / NL1
            xL1_N2 = NL1_N2 / NL1
            Water_1 = PR.EosPengRobinson()
            Water_1.WaterComposition(T = T1, P = self.P_atm, xH2O = xL1_H2O, x_O2 = xL1_O2, x_N2 = xL1_N2)
            Water_1.Z_mix()
            Water_1.MolarVolume()
            Water_1.Enthalpy()
            Water_1.fugacity()

            ##Gas currents
            #Current V1
            NV1 = NV1_H2O + NV1_O2 + NV1_N2
            xV1_H2O = NV1_H2O / NV1
            xV1_O2 = NV1_O2 / NV1
            xV1_N2 = NV1_N2 / NV1
            Air_1 = PR.EosPengRobinson()
            Air_1.AirComposition_out(T = T1, P = self.P_atm, x_H2O = xV1_H2O, x_O2 = xV1_O2, x_N2 = xV1_N2)
            Air_1.Z_mix()
            Air_1.MolarVolume()
            Air_1.Enthalpy()
            Air_1.fugacity()

            #Current V2
            Air_2 = PR.EosPengRobinson()
            Air_2.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_2.Z_mix()
            Air_2.MolarVolume()
            Air_2.Enthalpy()
            NV2 = Fv_vin / Air_2.Vm_mix_v
            NV2_H2O = NV2 * Air_2.x_H2O
            NV2_O2 = NV2 * Air_2.x_O2
            NV2_N2 = NV2 * Air_2.x_N2

            ## Equation system Stage 1
            # mass balances
            H2O_1 = (NL0_H2O + NV2_H2O) - (NL1_H2O + NV1_H2O)
            O2_1 = (NL0_O2 + NV2_O2) - (NL1_O2 + NV1_O2)
            N2_1 = (NL0_N2 + NV2_N2) - (NL1_N2 + NV1_N2)
            # Equilibrium
            Eq_H2O_1 = (Water_1.x_H2O * Water_1.phi_l['H2O']) - (Air_1.x_H2O * Air_1.phi_v['H2O'])
            Eq_O2_1 = (Water_1.x_O2 * Water_1.phi_l['O2']) - (Air_1.x_O2 * Air_1.phi_v['O2'])
            Eq_N2_1 = (Water_1.x_N2 * Water_1.phi_l['N2']) - (Air_1.x_N2 * Air_1.phi_v['N2'])
            # Energy balance
            Energy_1 = (NL0 * Water_0.H_l + NV2 * Air_2.H_v) - (NL1 * Water_1.H_l + NV1 * Air_1.H_v)


            return H2O_1, O2_1, N2_1, Eq_H2O_1, Eq_O2_1, Eq_N2_1, Energy_1
        
        def systemTwoStages (vars):
            NL1_H2O, NL1_O2, NL1_N2, NV1_H2O, NV1_O2, NV1_N2, T1, \
            NL2_H2O, NL2_O2, NL2_N2, NV2_H2O, NV2_O2, NV2_N2, T2  = vars    #vars for stage 1

            ##Liquid currents
            #Current L0
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T = self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = self.Fv_Lin / Water_0.Vm_mix_l
            NL0_H2O = NL0 * Water_0.x_H2O
            NL0_O2 = NL0 * Water_0.x_O2
            NL0_N2 = NL0 * Water_0.x_N2

            #Current L1
            NL1 = NL1_H2O + NL1_O2 + NL1_N2
            xL1_H2O = NL1_H2O / NL1
            xL1_O2 = NL1_O2 / NL1
            xL1_N2 = NL1_N2 / NL1
            Water_1 = PR.EosPengRobinson()
            Water_1.WaterComposition(T = T1, P = self.P_atm, xH2O = xL1_H2O, x_O2 = xL1_O2, x_N2 = xL1_N2)
            Water_1.Z_mix()
            Water_1.MolarVolume()
            Water_1.Enthalpy()
            Water_1.fugacity()

            #Current L2
            NL2 = NL2_H2O + NL2_O2 + NL2_N2
            xL2_H2O = NL2_H2O / NL2
            xL2_O2 = NL2_O2 / NL2
            xL2_N2 = NL2_N2 / NL2
            Water_2 = PR.EosPengRobinson()
            Water_2.WaterComposition(T = T2, P = self.P_atm, xH2O = xL2_H2O, x_O2 = xL2_O2, x_N2 = xL2_N2)
            Water_2.Z_mix()
            Water_2.MolarVolume()
            Water_2.Enthalpy()
            Water_2.fugacity()

            ##Gas currents
            #Current V1
            NV1 = NV1_H2O + NV1_O2 + NV1_N2
            xV1_H2O = NV1_H2O / NV1
            xV1_O2 = NV1_O2 / NV1
            xV1_N2 = NV1_N2 / NV1
            Air_1 = PR.EosPengRobinson()
            Air_1.AirComposition_out(T = T1, P = self.P_atm, x_H2O = xV1_H2O, x_O2 = xV1_O2, x_N2 = xV1_N2)
            Air_1.Z_mix()
            Air_1.MolarVolume()
            Air_1.Enthalpy()
            Air_1.fugacity()

            #Current V2
            NV2 = NV2_H2O + NV2_O2 + NV2_N2
            xV2_H2O = NV2_H2O / NV2
            xV2_O2 = NV2_O2 / NV2
            xV2_N2 = NV2_N2 / NV2
            Air_2 = PR.EosPengRobinson()
            Air_2.AirComposition_out(T = T2, P = self.P_atm, x_H2O = xV2_H2O, x_O2 = xV2_O2, x_N2 = xV2_N2)
            Air_2.Z_mix()
            Air_2.MolarVolume()
            Air_2.Enthalpy()
            Air_2.fugacity()

            #Current V3
            Air_3 = PR.EosPengRobinson()
            Air_3.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_3.Z_mix()
            Air_3.MolarVolume()
            Air_3.Enthalpy()
            NV3 = Fv_vin / Air_3.Vm_mix_v
            NV3_H2O = NV3 * Air_3.x_H2O
            NV3_O2 = NV3 * Air_3.x_O2
            NV3_N2 = NV3 * Air_3.x_N2

            ## Equation system Stage 1
            # mass balances
            H2O_1 = (NL0_H2O + NV2_H2O) - (NL1_H2O + NV1_H2O)
            O2_1 = (NL0_O2 + NV2_O2) - (NL1_O2 + NV1_O2)
            N2_1 = (NL0_N2 + NV2_N2) - (NL1_N2 + NV1_N2)
            # Equilibrium
            Eq_H2O_1 = (Water_1.x_H2O * Water_1.phi_l['H2O']) - (Air_1.x_H2O * Air_1.phi_v['H2O'])
            Eq_O2_1 = (Water_1.x_O2 * Water_1.phi_l['O2']) - (Air_1.x_O2 * Air_1.phi_v['O2'])
            Eq_N2_1 = (Water_1.x_N2 * Water_1.phi_l['N2']) - (Air_1.x_N2 * Air_1.phi_v['N2'])
            # Energy balance
            Energy_1 = (NL0 * Water_0.H_l + NV2 * Air_2.H_v) - (NL1 * Water_1.H_l + NV1 * Air_1.H_v)

            ## Equation system Stage 2
            # mass balances
            H2O_2 = (NL1_H2O + NV3_H2O) - (NL2_H2O + NV2_H2O)
            O2_2 = (NL1_O2 + NV3_O2) - (NL2_O2 + NV2_O2)
            N2_2 = (NL1_N2 + NV3_N2) - (NL2_N2 + NV2_N2)
            # Equilibrium
            Eq_H2O_2 = (Water_2.x_H2O * Water_2.phi_l['H2O']) - (Air_2.x_H2O * Air_2.phi_v['H2O'])
            Eq_O2_2 = (Water_2.x_O2 * Water_2.phi_l['O2']) - (Air_2.x_O2 * Air_2.phi_v['O2'])
            Eq_N2_2 = (Water_2.x_N2 * Water_2.phi_l['N2']) - (Air_2.x_N2 * Air_2.phi_v['N2'])
            # Energy balance
            Energy_2 = (NL1 * Water_1.H_l + NV3 * Air_3.H_v) - (NL2 * Water_2.H_l + NV2 * Air_2.H_v)

            return H2O_1, O2_1, N2_1, Eq_H2O_1, Eq_O2_1, Eq_N2_1, Energy_1, \
                   H2O_2, O2_2, N2_2, Eq_H2O_2, Eq_O2_2, Eq_N2_2, Energy_2 
        
        def systemThreeStages (vars):
            NL1_H2O, NL1_O2, NL1_N2, NV1_H2O, NV1_O2, NV1_N2, T1, \
            NL2_H2O, NL2_O2, NL2_N2, NV2_H2O, NV2_O2, NV2_N2, T2,\
            NL3_H2O, NL3_O2, NL3_N2, NV3_H2O, NV3_O2, NV3_N2, T3  = vars    #vars for stage 1

            ##Liquid currents
            #Current L0
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T = self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = self.Fv_Lin / Water_0.Vm_mix_l
            NL0_H2O = NL0 * Water_0.x_H2O
            NL0_O2 = NL0 * Water_0.x_O2
            NL0_N2 = NL0 * Water_0.x_N2

            #Current L1
            NL1 = NL1_H2O + NL1_O2 + NL1_N2
            xL1_H2O = NL1_H2O / NL1
            xL1_O2 = NL1_O2 / NL1
            xL1_N2 = NL1_N2 / NL1
            Water_1 = PR.EosPengRobinson()
            Water_1.WaterComposition(T = T1, P = self.P_atm, xH2O = xL1_H2O, x_O2 = xL1_O2, x_N2 = xL1_N2)
            Water_1.Z_mix()
            Water_1.MolarVolume()
            Water_1.Enthalpy()
            Water_1.fugacity()

            #Current L2
            NL2 = NL2_H2O + NL2_O2 + NL2_N2
            xL2_H2O = NL2_H2O / NL2
            xL2_O2 = NL2_O2 / NL2
            xL2_N2 = NL2_N2 / NL2
            Water_2 = PR.EosPengRobinson()
            Water_2.WaterComposition(T = T2, P = self.P_atm, xH2O = xL2_H2O, x_O2 = xL2_O2, x_N2 = xL2_N2)
            Water_2.Z_mix()
            Water_2.MolarVolume()
            Water_2.Enthalpy()
            Water_2.fugacity()

            #Current L3
            NL3 = NL3_H2O + NL3_O2 + NL3_N2
            xL3_H2O = NL3_H2O / NL3
            xL3_O2 = NL3_O2 / NL3
            xL3_N2 = NL3_N2 / NL3
            Water_3 = PR.EosPengRobinson()
            Water_3.WaterComposition(T = T3, P = self.P_atm, xH2O = xL3_H2O, x_O2 = xL3_O2, x_N2 = xL3_N2)
            Water_3.Z_mix()
            Water_3.MolarVolume()
            Water_3.Enthalpy()
            Water_3.fugacity()

            ##Gas currents
            #Current V1
            NV1 = NV1_H2O + NV1_O2 + NV1_N2
            xV1_H2O = NV1_H2O / NV1
            xV1_O2 = NV1_O2 / NV1
            xV1_N2 = NV1_N2 / NV1
            Air_1 = PR.EosPengRobinson()
            Air_1.AirComposition_out(T = T1, P = self.P_atm, x_H2O = xV1_H2O, x_O2 = xV1_O2, x_N2 = xV1_N2)
            Air_1.Z_mix()
            Air_1.MolarVolume()
            Air_1.Enthalpy()
            Air_1.fugacity()

            #Current V2
            NV2 = NV2_H2O + NV2_O2 + NV2_N2
            xV2_H2O = NV2_H2O / NV2
            xV2_O2 = NV2_O2 / NV2
            xV2_N2 = NV2_N2 / NV2
            Air_2 = PR.EosPengRobinson()
            Air_2.AirComposition_out(T = T2, P = self.P_atm, x_H2O = xV2_H2O, x_O2 = xV2_O2, x_N2 = xV2_N2)
            Air_2.Z_mix()
            Air_2.MolarVolume()
            Air_2.Enthalpy()
            Air_2.fugacity()

            #Current V3
            NV3 = NV3_H2O + NV3_O2 + NV3_N2
            xV3_H2O = NV3_H2O / NV3
            xV3_O2 = NV3_O2 / NV3
            xV3_N2 = NV3_N2 / NV3
            Air_3 = PR.EosPengRobinson()
            Air_3.AirComposition_out(T = T3, P = self.P_atm, x_H2O = xV3_H2O, x_O2 = xV3_O2, x_N2 = xV3_N2)
            Air_3.Z_mix()
            Air_3.MolarVolume()
            Air_3.Enthalpy()
            Air_3.fugacity()

            #Current V4
            Air_4 = PR.EosPengRobinson()
            Air_4.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_4.Z_mix()
            Air_4.MolarVolume()
            Air_4.Enthalpy()
            NV4 = Fv_vin / Air_4.Vm_mix_v
            NV4_H2O = NV4 * Air_4.x_H2O
            NV4_O2 = NV4 * Air_4.x_O2
            NV4_N2 = NV4 * Air_4.x_N2

            ## Equation system Stage 1
            # mass balances
            H2O_1 = (NL0_H2O + NV2_H2O) - (NL1_H2O + NV1_H2O)
            O2_1 = (NL0_O2 + NV2_O2) - (NL1_O2 + NV1_O2)
            N2_1 = (NL0_N2 + NV2_N2) - (NL1_N2 + NV1_N2)
            # Equilibrium
            Eq_H2O_1 = (Water_1.x_H2O * Water_1.phi_l['H2O']) - (Air_1.x_H2O * Air_1.phi_v['H2O'])
            Eq_O2_1 = (Water_1.x_O2 * Water_1.phi_l['O2']) - (Air_1.x_O2 * Air_1.phi_v['O2'])
            Eq_N2_1 = (Water_1.x_N2 * Water_1.phi_l['N2']) - (Air_1.x_N2 * Air_1.phi_v['N2'])
            # Energy balance
            Energy_1 = (NL0 * Water_0.H_l + NV2 * Air_2.H_v) - (NL1 * Water_1.H_l + NV1 * Air_1.H_v)

            ## Equation system Stage 2
            # mass balances
            H2O_2 = (NL1_H2O + NV3_H2O) - (NL2_H2O + NV2_H2O)
            O2_2 = (NL1_O2 + NV3_O2) - (NL2_O2 + NV2_O2)
            N2_2 = (NL1_N2 + NV3_N2) - (NL2_N2 + NV2_N2)
            # Equilibrium
            Eq_H2O_2 = (Water_2.x_H2O * Water_2.phi_l['H2O']) - (Air_2.x_H2O * Air_2.phi_v['H2O'])
            Eq_O2_2 = (Water_2.x_O2 * Water_2.phi_l['O2']) - (Air_2.x_O2 * Air_2.phi_v['O2'])
            Eq_N2_2 = (Water_2.x_N2 * Water_2.phi_l['N2']) - (Air_2.x_N2 * Air_2.phi_v['N2'])
            # Energy balance
            Energy_2 = (NL1 * Water_1.H_l + NV3 * Air_3.H_v) - (NL2 * Water_2.H_l + NV2 * Air_2.H_v)

            ## Equation system Stage 3
            # mass balances
            H2O_3 = (NL2_H2O + NV4_H2O) - (NL3_H2O + NV3_H2O)
            O2_3 = (NL2_O2 + NV4_O2) - (NL3_O2 + NV3_O2)
            N2_3 = (NL2_N2 + NV4_N2) - (NL3_N2 + NV3_N2)
            # Equilibrium
            Eq_H2O_3 = (Water_3.x_H2O * Water_3.phi_l['H2O']) - (Air_3.x_H2O * Air_3.phi_v['H2O'])
            Eq_O2_3 = (Water_3.x_O2 * Water_3.phi_l['O2']) - (Air_3.x_O2 * Air_3.phi_v['O2'])
            Eq_N2_3 = (Water_3.x_N2 * Water_2.phi_l['N2']) - (Air_3.x_N2 * Air_3.phi_v['N2'])
            # Energy balance
            Energy_3 = (NL2 * Water_2.H_l + NV4 * Air_4.H_v) - (NL3 * Water_3.H_l + NV3 * Air_3.H_v)

            return H2O_1, O2_1, N2_1, Eq_H2O_1, Eq_O2_1, Eq_N2_1, Energy_1, \
                   H2O_2, O2_2, N2_2, Eq_H2O_2, Eq_O2_2, Eq_N2_2, Energy_2, \
                   H2O_3, O2_3, N2_3, Eq_H2O_3, Eq_O2_3, Eq_N2_3, Energy_3 
        
        def systemFourStages (vars):
            NL1_H2O, NL1_O2, NL1_N2, NV1_H2O, NV1_O2, NV1_N2, T1,\
            NL2_H2O, NL2_O2, NL2_N2, NV2_H2O, NV2_O2, NV2_N2, T2,\
            NL3_H2O, NL3_O2, NL3_N2, NV3_H2O, NV3_O2, NV3_N2, T3,\
            NL4_H2O, NL4_O2, NL4_N2, NV4_H2O, NV4_O2, NV4_N2, T4 = vars    #vars for stage 1

            ##Liquid currents
            #Current L0
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T = self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = self.Fv_Lin / Water_0.Vm_mix_l
            NL0_H2O = NL0 * Water_0.x_H2O
            NL0_O2 = NL0 * Water_0.x_O2
            NL0_N2 = NL0 * Water_0.x_N2

            #Current L1
            NL1 = NL1_H2O + NL1_O2 + NL1_N2
            xL1_H2O = NL1_H2O / NL1
            xL1_O2 = NL1_O2 / NL1
            xL1_N2 = NL1_N2 / NL1
            Water_1 = PR.EosPengRobinson()
            Water_1.WaterComposition(T = T1, P = self.P_atm, xH2O = xL1_H2O, x_O2 = xL1_O2, x_N2 = xL1_N2)
            Water_1.Z_mix()
            Water_1.MolarVolume()
            Water_1.Enthalpy()
            Water_1.fugacity()

            #Current L2
            NL2 = NL2_H2O + NL2_O2 + NL2_N2
            xL2_H2O = NL2_H2O / NL2
            xL2_O2 = NL2_O2 / NL2
            xL2_N2 = NL2_N2 / NL2
            Water_2 = PR.EosPengRobinson()
            Water_2.WaterComposition(T = T2, P = self.P_atm, xH2O = xL2_H2O, x_O2 = xL2_O2, x_N2 = xL2_N2)
            Water_2.Z_mix()
            Water_2.MolarVolume()
            Water_2.Enthalpy()
            Water_2.fugacity()

            #Current L3
            NL3 = NL3_H2O + NL3_O2 + NL3_N2
            xL3_H2O = NL3_H2O / NL3
            xL3_O2 = NL3_O2 / NL3
            xL3_N2 = NL3_N2 / NL3
            Water_3 = PR.EosPengRobinson()
            Water_3.WaterComposition(T = T3, P = self.P_atm, xH2O = xL3_H2O, x_O2 = xL3_O2, x_N2 = xL3_N2)
            Water_3.Z_mix()
            Water_3.MolarVolume()
            Water_3.Enthalpy()
            Water_3.fugacity()

            #Current L4
            NL4 = NL4_H2O + NL4_O2 + NL4_N2
            xL4_H2O = NL4_H2O / NL4
            xL4_O2 = NL4_O2 / NL4
            xL4_N2 = NL4_N2 / NL4
            Water_4 = PR.EosPengRobinson()
            Water_4.WaterComposition(T = T4, P = self.P_atm, xH2O = xL4_H2O, x_O2 = xL4_O2, x_N2 = xL4_N2)
            Water_4.Z_mix()
            Water_4.MolarVolume()
            Water_4.Enthalpy()
            Water_4.fugacity()

            ##Gas currents
            #Current V1
            NV1 = NV1_H2O + NV1_O2 + NV1_N2
            xV1_H2O = NV1_H2O / NV1
            xV1_O2 = NV1_O2 / NV1
            xV1_N2 = NV1_N2 / NV1
            Air_1 = PR.EosPengRobinson()
            Air_1.AirComposition_out(T = T1, P = self.P_atm, x_H2O = xV1_H2O, x_O2 = xV1_O2, x_N2 = xV1_N2)
            Air_1.Z_mix()
            Air_1.MolarVolume()
            Air_1.Enthalpy()
            Air_1.fugacity()

            #Current V2
            NV2 = NV2_H2O + NV2_O2 + NV2_N2
            xV2_H2O = NV2_H2O / NV2
            xV2_O2 = NV2_O2 / NV2
            xV2_N2 = NV2_N2 / NV2
            Air_2 = PR.EosPengRobinson()
            Air_2.AirComposition_out(T = T2, P = self.P_atm, x_H2O = xV2_H2O, x_O2 = xV2_O2, x_N2 = xV2_N2)
            Air_2.Z_mix()
            Air_2.MolarVolume()
            Air_2.Enthalpy()
            Air_2.fugacity()

            #Current V3
            NV3 = NV3_H2O + NV3_O2 + NV3_N2
            xV3_H2O = NV3_H2O / NV3
            xV3_O2 = NV3_O2 / NV3
            xV3_N2 = NV3_N2 / NV3
            Air_3 = PR.EosPengRobinson()
            Air_3.AirComposition_out(T = T3, P = self.P_atm, x_H2O = xV3_H2O, x_O2 = xV3_O2, x_N2 = xV3_N2)
            Air_3.Z_mix()
            Air_3.MolarVolume()
            Air_3.Enthalpy()
            Air_3.fugacity()

            #Current V4
            NV4 = NV4_H2O + NV4_O2 + NV4_N2
            xV4_H2O = NV4_H2O / NV4
            xV4_O2 = NV4_O2 / NV4
            xV4_N2 = NV4_N2 / NV4
            Air_4 = PR.EosPengRobinson()
            Air_4.AirComposition_out(T = T4, P = self.P_atm, x_H2O = xV4_H2O, x_O2 = xV4_O2, x_N2 = xV4_N2)
            Air_4.Z_mix()
            Air_4.MolarVolume()
            Air_4.Enthalpy()
            Air_4.fugacity()

            #Current V5
            Air_5 = PR.EosPengRobinson()
            Air_5.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_5.Z_mix()
            Air_5.MolarVolume()
            Air_5.Enthalpy()
            NV5 = Fv_vin / Air_5.Vm_mix_v
            NV5_H2O = NV5 * Air_5.x_H2O
            NV5_O2 = NV5 * Air_5.x_O2
            NV5_N2 = NV5 * Air_5.x_N2

            ## Equation system Stage 1
            # mass balances
            H2O_1 = (NL0_H2O + NV2_H2O) - (NL1_H2O + NV1_H2O)
            O2_1 = (NL0_O2 + NV2_O2) - (NL1_O2 + NV1_O2)
            N2_1 = (NL0_N2 + NV2_N2) - (NL1_N2 + NV1_N2)
            # Equilibrium
            Eq_H2O_1 = (Water_1.x_H2O * Water_1.phi_l['H2O']) - (Air_1.x_H2O * Air_1.phi_v['H2O'])
            Eq_O2_1 = (Water_1.x_O2 * Water_1.phi_l['O2']) - (Air_1.x_O2 * Air_1.phi_v['O2'])
            Eq_N2_1 = (Water_1.x_N2 * Water_1.phi_l['N2']) - (Air_1.x_N2 * Air_1.phi_v['N2'])
            # Energy balance
            Energy_1 = (NL0 * Water_0.H_l + NV2 * Air_2.H_v) - (NL1 * Water_1.H_l + NV1 * Air_1.H_v)

            ## Equation system Stage 2
            # mass balances
            H2O_2 = (NL1_H2O + NV3_H2O) - (NL2_H2O + NV2_H2O)
            O2_2 = (NL1_O2 + NV3_O2) - (NL2_O2 + NV2_O2)
            N2_2 = (NL1_N2 + NV3_N2) - (NL2_N2 + NV2_N2)
            # Equilibrium
            Eq_H2O_2 = (Water_2.x_H2O * Water_2.phi_l['H2O']) - (Air_2.x_H2O * Air_2.phi_v['H2O'])
            Eq_O2_2 = (Water_2.x_O2 * Water_2.phi_l['O2']) - (Air_2.x_O2 * Air_2.phi_v['O2'])
            Eq_N2_2 = (Water_2.x_N2 * Water_2.phi_l['N2']) - (Air_2.x_N2 * Air_2.phi_v['N2'])
            # Energy balance
            Energy_2 = (NL1 * Water_1.H_l + NV3 * Air_3.H_v) - (NL2 * Water_2.H_l + NV2 * Air_2.H_v)

            ## Equation system Stage 3
            # mass balances
            H2O_3 = (NL2_H2O + NV4_H2O) - (NL3_H2O + NV3_H2O)
            O2_3 = (NL2_O2 + NV4_O2) - (NL3_O2 + NV3_O2)
            N2_3 = (NL2_N2 + NV4_N2) - (NL3_N2 + NV3_N2)
            # Equilibrium
            Eq_H2O_3 = (Water_3.x_H2O * Water_3.phi_l['H2O']) - (Air_3.x_H2O * Air_3.phi_v['H2O'])
            Eq_O2_3 = (Water_3.x_O2 * Water_3.phi_l['O2']) - (Air_3.x_O2 * Air_3.phi_v['O2'])
            Eq_N2_3 = (Water_3.x_N2 * Water_3.phi_l['N2']) - (Air_3.x_N2 * Air_3.phi_v['N2'])
            # Energy balance
            Energy_3 = (NL2 * Water_2.H_l + NV4 * Air_4.H_v) - (NL3 * Water_3.H_l + NV3 * Air_3.H_v)

            ## Equation system Stage 4
            # mass balances
            H2O_4 = (NL3_H2O + NV5_H2O) - (NL4_H2O + NV4_H2O)
            O2_4 = (NL3_O2 + NV5_O2) - (NL4_O2 + NV4_O2)
            N2_4 = (NL3_N2 + NV5_N2) - (NL4_N2 + NV4_N2)
            # Equilibrium
            Eq_H2O_4 = (Water_4.x_H2O * Water_4.phi_l['H2O']) - (Air_4.x_H2O * Air_4.phi_v['H2O'])
            Eq_O2_4 = (Water_4.x_O2 * Water_4.phi_l['O2']) - (Air_4.x_O2 * Air_4.phi_v['O2'])
            Eq_N2_4 = (Water_4.x_N2 * Water_4.phi_l['N2']) - (Air_4.x_N2 * Air_4.phi_v['N2'])
            # Energy balance
            Energy_4 = (NL3 * Water_3.H_l + NV5 * Air_5.H_v) - (NL4 * Water_4.H_l + NV4 * Air_4.H_v)

            return H2O_1, O2_1, N2_1, Eq_H2O_1, Eq_O2_1, Eq_N2_1, Energy_1, \
                   H2O_2, O2_2, N2_2, Eq_H2O_2, Eq_O2_2, Eq_N2_2, Energy_2, \
                   H2O_3, O2_3, N2_3, Eq_H2O_3, Eq_O2_3, Eq_N2_3, Energy_3, \
                   H2O_4, O2_4, N2_4, Eq_H2O_4, Eq_O2_4, Eq_N2_4, Energy_4
        
        def systemFiveStages (vars):
            NL1_H2O, NL1_O2, NL1_N2, NV1_H2O, NV1_O2, NV1_N2, T1,\
            NL2_H2O, NL2_O2, NL2_N2, NV2_H2O, NV2_O2, NV2_N2, T2,\
            NL3_H2O, NL3_O2, NL3_N2, NV3_H2O, NV3_O2, NV3_N2, T3,\
            NL4_H2O, NL4_O2, NL4_N2, NV4_H2O, NV4_O2, NV4_N2, T4,\
            NL5_H2O, NL5_O2, NL5_N2, NV5_H2O, NV5_O2, NV5_N2, T5 = vars    #vars for stage 1

            ##Liquid currents
            #Current L0
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T = self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = self.Fv_Lin / Water_0.Vm_mix_l
            NL0_H2O = NL0 * Water_0.x_H2O
            NL0_O2 = NL0 * Water_0.x_O2
            NL0_N2 = NL0 * Water_0.x_N2

            #Current L1
            NL1 = NL1_H2O + NL1_O2 + NL1_N2
            xL1_H2O = NL1_H2O / NL1
            xL1_O2 = NL1_O2 / NL1
            xL1_N2 = NL1_N2 / NL1
            Water_1 = PR.EosPengRobinson()
            Water_1.WaterComposition(T = T1, P = self.P_atm, xH2O = xL1_H2O, x_O2 = xL1_O2, x_N2 = xL1_N2)
            Water_1.Z_mix()
            Water_1.MolarVolume()
            Water_1.Enthalpy()
            Water_1.fugacity()

            #Current L2
            NL2 = NL2_H2O + NL2_O2 + NL2_N2
            xL2_H2O = NL2_H2O / NL2
            xL2_O2 = NL2_O2 / NL2
            xL2_N2 = NL2_N2 / NL2
            Water_2 = PR.EosPengRobinson()
            Water_2.WaterComposition(T = T2, P = self.P_atm, xH2O = xL2_H2O, x_O2 = xL2_O2, x_N2 = xL2_N2)
            Water_2.Z_mix()
            Water_2.MolarVolume()
            Water_2.Enthalpy()
            Water_2.fugacity()

            #Current L3
            NL3 = NL3_H2O + NL3_O2 + NL3_N2
            xL3_H2O = NL3_H2O / NL3
            xL3_O2 = NL3_O2 / NL3
            xL3_N2 = NL3_N2 / NL3
            Water_3 = PR.EosPengRobinson()
            Water_3.WaterComposition(T = T3, P = self.P_atm, xH2O = xL3_H2O, x_O2 = xL3_O2, x_N2 = xL3_N2)
            Water_3.Z_mix()
            Water_3.MolarVolume()
            Water_3.Enthalpy()
            Water_3.fugacity()

            #Current L4
            NL4 = NL4_H2O + NL4_O2 + NL4_N2
            xL4_H2O = NL4_H2O / NL4
            xL4_O2 = NL4_O2 / NL4
            xL4_N2 = NL4_N2 / NL4
            Water_4 = PR.EosPengRobinson()
            Water_4.WaterComposition(T = T4, P = self.P_atm, xH2O = xL4_H2O, x_O2 = xL4_O2, x_N2 = xL4_N2)
            Water_4.Z_mix()
            Water_4.MolarVolume()
            Water_4.Enthalpy()
            Water_4.fugacity()

            #Current L5
            NL5 = NL5_H2O + NL5_O2 + NL5_N2
            xL5_H2O = NL5_H2O / NL5
            xL5_O2 = NL5_O2 / NL5
            xL5_N2 = NL5_N2 / NL5
            Water_5 = PR.EosPengRobinson()
            Water_5.WaterComposition(T = T5, P = self.P_atm, xH2O = xL5_H2O, x_O2 = xL5_O2, x_N2 = xL5_N2)
            Water_5.Z_mix()
            Water_5.MolarVolume()
            Water_5.Enthalpy()
            Water_5.fugacity()

            ##Gas currents
            #Current V1
            NV1 = NV1_H2O + NV1_O2 + NV1_N2
            xV1_H2O = NV1_H2O / NV1
            xV1_O2 = NV1_O2 / NV1
            xV1_N2 = NV1_N2 / NV1
            Air_1 = PR.EosPengRobinson()
            Air_1.AirComposition_out(T = T1, P = self.P_atm, x_H2O = xV1_H2O, x_O2 = xV1_O2, x_N2 = xV1_N2)
            Air_1.Z_mix()
            Air_1.MolarVolume()
            Air_1.Enthalpy()
            Air_1.fugacity()

            #Current V2
            NV2 = NV2_H2O + NV2_O2 + NV2_N2
            xV2_H2O = NV2_H2O / NV2
            xV2_O2 = NV2_O2 / NV2
            xV2_N2 = NV2_N2 / NV2
            Air_2 = PR.EosPengRobinson()
            Air_2.AirComposition_out(T = T2, P = self.P_atm, x_H2O = xV2_H2O, x_O2 = xV2_O2, x_N2 = xV2_N2)
            Air_2.Z_mix()
            Air_2.MolarVolume()
            Air_2.Enthalpy()
            Air_2.fugacity()

            #Current V3
            NV3 = NV3_H2O + NV3_O2 + NV3_N2
            xV3_H2O = NV3_H2O / NV3
            xV3_O2 = NV3_O2 / NV3
            xV3_N2 = NV3_N2 / NV3
            Air_3 = PR.EosPengRobinson()
            Air_3.AirComposition_out(T = T3, P = self.P_atm, x_H2O = xV3_H2O, x_O2 = xV3_O2, x_N2 = xV3_N2)
            Air_3.Z_mix()
            Air_3.MolarVolume()
            Air_3.Enthalpy()
            Air_3.fugacity()

            #Current V4
            NV4 = NV4_H2O + NV4_O2 + NV4_N2
            xV4_H2O = NV4_H2O / NV4
            xV4_O2 = NV4_O2 / NV4
            xV4_N2 = NV4_N2 / NV4
            Air_4 = PR.EosPengRobinson()
            Air_4.AirComposition_out(T = T4, P = self.P_atm, x_H2O = xV4_H2O, x_O2 = xV4_O2, x_N2 = xV4_N2)
            Air_4.Z_mix()
            Air_4.MolarVolume()
            Air_4.Enthalpy()
            Air_4.fugacity()

            #Current V5
            NV5 = NV5_H2O + NV5_O2 + NV5_N2
            xV5_H2O = NV5_H2O / NV5
            xV5_O2 = NV5_O2 / NV5
            xV5_N2 = NV5_N2 / NV5
            Air_5 = PR.EosPengRobinson()
            Air_5.AirComposition_out(T = T5, P = self.P_atm, x_H2O = xV5_H2O, x_O2 = xV5_O2, x_N2 = xV5_N2)
            Air_5.Z_mix()
            Air_5.MolarVolume()
            Air_5.Enthalpy()
            Air_5.fugacity()

            #Current V6
            Air_6 = PR.EosPengRobinson()
            Air_6.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_6.Z_mix()
            Air_6.MolarVolume()
            Air_6.Enthalpy()
            NV6 = Fv_vin / Air_6.Vm_mix_v
            NV6_H2O = NV6 * Air_6.x_H2O
            NV6_O2 = NV6 * Air_6.x_O2
            NV6_N2 = NV6 * Air_6.x_N2

            ## Equation system Stage 1
            # mass balances
            H2O_1 = (NL0_H2O + NV2_H2O) - (NL1_H2O + NV1_H2O)
            O2_1 = (NL0_O2 + NV2_O2) - (NL1_O2 + NV1_O2)
            N2_1 = (NL0_N2 + NV2_N2) - (NL1_N2 + NV1_N2)
            # Equilibrium
            Eq_H2O_1 = (Water_1.x_H2O * Water_1.phi_l['H2O']) - (Air_1.x_H2O * Air_1.phi_v['H2O'])
            Eq_O2_1 = (Water_1.x_O2 * Water_1.phi_l['O2']) - (Air_1.x_O2 * Air_1.phi_v['O2'])
            Eq_N2_1 = (Water_1.x_N2 * Water_1.phi_l['N2']) - (Air_1.x_N2 * Air_1.phi_v['N2'])
            # Energy balance
            Energy_1 = (NL0 * Water_0.H_l + NV2 * Air_2.H_v) - (NL1 * Water_1.H_l + NV1 * Air_1.H_v)

            ## Equation system Stage 2
            # mass balances
            H2O_2 = (NL1_H2O + NV3_H2O) - (NL2_H2O + NV2_H2O)
            O2_2 = (NL1_O2 + NV3_O2) - (NL2_O2 + NV2_O2)
            N2_2 = (NL1_N2 + NV3_N2) - (NL2_N2 + NV2_N2)
            # Equilibrium
            Eq_H2O_2 = (Water_2.x_H2O * Water_2.phi_l['H2O']) - (Air_2.x_H2O * Air_2.phi_v['H2O'])
            Eq_O2_2 = (Water_2.x_O2 * Water_2.phi_l['O2']) - (Air_2.x_O2 * Air_2.phi_v['O2'])
            Eq_N2_2 = (Water_2.x_N2 * Water_2.phi_l['N2']) - (Air_2.x_N2 * Air_2.phi_v['N2'])
            # Energy balance
            Energy_2 = (NL1 * Water_1.H_l + NV3 * Air_3.H_v) - (NL2 * Water_2.H_l + NV2 * Air_2.H_v)

            ## Equation system Stage 3
            # mass balances
            H2O_3 = (NL2_H2O + NV4_H2O) - (NL3_H2O + NV3_H2O)
            O2_3 = (NL2_O2 + NV4_O2) - (NL3_O2 + NV3_O2)
            N2_3 = (NL2_N2 + NV4_N2) - (NL3_N2 + NV3_N2)
            # Equilibrium
            Eq_H2O_3 = (Water_3.x_H2O * Water_3.phi_l['H2O']) - (Air_3.x_H2O * Air_3.phi_v['H2O'])
            Eq_O2_3 = (Water_3.x_O2 * Water_3.phi_l['O2']) - (Air_3.x_O2 * Air_3.phi_v['O2'])
            Eq_N2_3 = (Water_3.x_N2 * Water_3.phi_l['N2']) - (Air_3.x_N2 * Air_3.phi_v['N2'])
            # Energy balance
            Energy_3 = (NL2 * Water_2.H_l + NV4 * Air_4.H_v) - (NL3 * Water_3.H_l + NV3 * Air_3.H_v)

            ## Equation system Stage 4
            # mass balances
            H2O_4 = (NL3_H2O + NV5_H2O) - (NL4_H2O + NV4_H2O)
            O2_4 = (NL3_O2 + NV5_O2) - (NL4_O2 + NV4_O2)
            N2_4 = (NL3_N2 + NV5_N2) - (NL4_N2 + NV4_N2)
            # Equilibrium
            Eq_H2O_4 = (Water_4.x_H2O * Water_4.phi_l['H2O']) - (Air_4.x_H2O * Air_4.phi_v['H2O'])
            Eq_O2_4 = (Water_4.x_O2 * Water_4.phi_l['O2']) - (Air_4.x_O2 * Air_4.phi_v['O2'])
            Eq_N2_4 = (Water_4.x_N2 * Water_4.phi_l['N2']) - (Air_4.x_N2 * Air_4.phi_v['N2'])
            # Energy balance
            Energy_4 = (NL3 * Water_3.H_l + NV5 * Air_5.H_v) - (NL4 * Water_4.H_l + NV4 * Air_4.H_v)

            ## Equation system Stage 5
            # mass balances
            H2O_5 = (NL4_H2O + NV6_H2O) - (NL5_H2O + NV5_H2O)
            O2_5 = (NL4_O2 + NV6_O2) - (NL5_O2 + NV5_O2)
            N2_5 = (NL4_N2 + NV6_N2) - (NL5_N2 + NV5_N2)
            # Equilibrium
            Eq_H2O_5 = (Water_5.x_H2O * Water_5.phi_l['H2O']) - (Air_5.x_H2O * Air_5.phi_v['H2O'])
            Eq_O2_5 = (Water_5.x_O2 * Water_5.phi_l['O2']) - (Air_5.x_O2 * Air_5.phi_v['O2'])
            Eq_N2_5 = (Water_5.x_N2 * Water_5.phi_l['N2']) - (Air_5.x_N2 * Air_5.phi_v['N2'])
            # Energy balance
            Energy_5 = (NL4 * Water_4.H_l + NV6 * Air_6.H_v) - (NL5 * Water_5.H_l + NV5 * Air_5.H_v)


            return H2O_1, O2_1, N2_1, Eq_H2O_1, Eq_O2_1, Eq_N2_1, Energy_1, \
                   H2O_2, O2_2, N2_2, Eq_H2O_2, Eq_O2_2, Eq_N2_2, Energy_2, \
                   H2O_3, O2_3, N2_3, Eq_H2O_3, Eq_O2_3, Eq_N2_3, Energy_3, \
                   H2O_4, O2_4, N2_4, Eq_H2O_4, Eq_O2_4, Eq_N2_4, Energy_4, \
                   H2O_5, O2_5, N2_5, Eq_H2O_5, Eq_O2_5, Eq_N2_5, Energy_5
        
        def systemSixStages (vars):
            NL1_H2O, NL1_O2, NL1_N2, NV1_H2O, NV1_O2, NV1_N2, T1,\
            NL2_H2O, NL2_O2, NL2_N2, NV2_H2O, NV2_O2, NV2_N2, T2,\
            NL3_H2O, NL3_O2, NL3_N2, NV3_H2O, NV3_O2, NV3_N2, T3,\
            NL4_H2O, NL4_O2, NL4_N2, NV4_H2O, NV4_O2, NV4_N2, T4,\
            NL5_H2O, NL5_O2, NL5_N2, NV5_H2O, NV5_O2, NV5_N2, T5,\
            NL6_H2O, NL6_O2, NL6_N2, NV6_H2O, NV6_O2, NV6_N2, T6= vars    #vars for stage 1

            ##Liquid currents
            #Current L0
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T = self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = self.Fv_Lin / Water_0.Vm_mix_l
            NL0_H2O = NL0 * Water_0.x_H2O
            NL0_O2 = NL0 * Water_0.x_O2
            NL0_N2 = NL0 * Water_0.x_N2

            #Current L1
            NL1 = NL1_H2O + NL1_O2 + NL1_N2
            xL1_H2O = NL1_H2O / NL1
            xL1_O2 = NL1_O2 / NL1
            xL1_N2 = NL1_N2 / NL1
            Water_1 = PR.EosPengRobinson()
            Water_1.WaterComposition(T = T1, P = self.P_atm, xH2O = xL1_H2O, x_O2 = xL1_O2, x_N2 = xL1_N2)
            Water_1.Z_mix()
            Water_1.MolarVolume()
            Water_1.Enthalpy()
            Water_1.fugacity()

            #Current L2
            NL2 = NL2_H2O + NL2_O2 + NL2_N2
            xL2_H2O = NL2_H2O / NL2
            xL2_O2 = NL2_O2 / NL2
            xL2_N2 = NL2_N2 / NL2
            Water_2 = PR.EosPengRobinson()
            Water_2.WaterComposition(T = T2, P = self.P_atm, xH2O = xL2_H2O, x_O2 = xL2_O2, x_N2 = xL2_N2)
            Water_2.Z_mix()
            Water_2.MolarVolume()
            Water_2.Enthalpy()
            Water_2.fugacity()

            #Current L3
            NL3 = NL3_H2O + NL3_O2 + NL3_N2
            xL3_H2O = NL3_H2O / NL3
            xL3_O2 = NL3_O2 / NL3
            xL3_N2 = NL3_N2 / NL3
            Water_3 = PR.EosPengRobinson()
            Water_3.WaterComposition(T = T3, P = self.P_atm, xH2O = xL3_H2O, x_O2 = xL3_O2, x_N2 = xL3_N2)
            Water_3.Z_mix()
            Water_3.MolarVolume()
            Water_3.Enthalpy()
            Water_3.fugacity()

            #Current L4
            NL4 = NL4_H2O + NL4_O2 + NL4_N2
            xL4_H2O = NL4_H2O / NL4
            xL4_O2 = NL4_O2 / NL4
            xL4_N2 = NL4_N2 / NL4
            Water_4 = PR.EosPengRobinson()
            Water_4.WaterComposition(T = T4, P = self.P_atm, xH2O = xL4_H2O, x_O2 = xL4_O2, x_N2 = xL4_N2)
            Water_4.Z_mix()
            Water_4.MolarVolume()
            Water_4.Enthalpy()
            Water_4.fugacity()

            #Current L5
            NL5 = NL5_H2O + NL5_O2 + NL5_N2
            xL5_H2O = NL5_H2O / NL5
            xL5_O2 = NL5_O2 / NL5
            xL5_N2 = NL5_N2 / NL5
            Water_5 = PR.EosPengRobinson()
            Water_5.WaterComposition(T = T5, P = self.P_atm, xH2O = xL5_H2O, x_O2 = xL5_O2, x_N2 = xL5_N2)
            Water_5.Z_mix()
            Water_5.MolarVolume()
            Water_5.Enthalpy()
            Water_5.fugacity()

            #Current L6
            NL6 = NL6_H2O + NL6_O2 + NL6_N2
            xL6_H2O = NL6_H2O / NL6
            xL6_O2 = NL6_O2 / NL6
            xL6_N2 = NL6_N2 / NL6
            Water_6 = PR.EosPengRobinson()
            Water_6.WaterComposition(T = T6, P = self.P_atm, xH2O = xL6_H2O, x_O2 = xL6_O2, x_N2 = xL6_N2)
            Water_6.Z_mix()
            Water_6.MolarVolume()
            Water_6.Enthalpy()
            Water_6.fugacity()

            ##Gas currents
            #Current V1
            NV1 = NV1_H2O + NV1_O2 + NV1_N2
            xV1_H2O = NV1_H2O / NV1
            xV1_O2 = NV1_O2 / NV1
            xV1_N2 = NV1_N2 / NV1
            Air_1 = PR.EosPengRobinson()
            Air_1.AirComposition_out(T = T1, P = self.P_atm, x_H2O = xV1_H2O, x_O2 = xV1_O2, x_N2 = xV1_N2)
            Air_1.Z_mix()
            Air_1.MolarVolume()
            Air_1.Enthalpy()
            Air_1.fugacity()

            #Current V2
            NV2 = NV2_H2O + NV2_O2 + NV2_N2
            xV2_H2O = NV2_H2O / NV2
            xV2_O2 = NV2_O2 / NV2
            xV2_N2 = NV2_N2 / NV2
            Air_2 = PR.EosPengRobinson()
            Air_2.AirComposition_out(T = T2, P = self.P_atm, x_H2O = xV2_H2O, x_O2 = xV2_O2, x_N2 = xV2_N2)
            Air_2.Z_mix()
            Air_2.MolarVolume()
            Air_2.Enthalpy()
            Air_2.fugacity()

            #Current V3
            NV3 = NV3_H2O + NV3_O2 + NV3_N2
            xV3_H2O = NV3_H2O / NV3
            xV3_O2 = NV3_O2 / NV3
            xV3_N2 = NV3_N2 / NV3
            Air_3 = PR.EosPengRobinson()
            Air_3.AirComposition_out(T = T3, P = self.P_atm, x_H2O = xV3_H2O, x_O2 = xV3_O2, x_N2 = xV3_N2)
            Air_3.Z_mix()
            Air_3.MolarVolume()
            Air_3.Enthalpy()
            Air_3.fugacity()

            #Current V4
            NV4 = NV4_H2O + NV4_O2 + NV4_N2
            xV4_H2O = NV4_H2O / NV4
            xV4_O2 = NV4_O2 / NV4
            xV4_N2 = NV4_N2 / NV4
            Air_4 = PR.EosPengRobinson()
            Air_4.AirComposition_out(T = T4, P = self.P_atm, x_H2O = xV4_H2O, x_O2 = xV4_O2, x_N2 = xV4_N2)
            Air_4.Z_mix()
            Air_4.MolarVolume()
            Air_4.Enthalpy()
            Air_4.fugacity()

            #Current V5
            NV5 = NV5_H2O + NV5_O2 + NV5_N2
            xV5_H2O = NV5_H2O / NV5
            xV5_O2 = NV5_O2 / NV5
            xV5_N2 = NV5_N2 / NV5
            Air_5 = PR.EosPengRobinson()
            Air_5.AirComposition_out(T = T5, P = self.P_atm, x_H2O = xV5_H2O, x_O2 = xV5_O2, x_N2 = xV5_N2)
            Air_5.Z_mix()
            Air_5.MolarVolume()
            Air_5.Enthalpy()
            Air_5.fugacity()

            #Current V6
            NV6 = NV6_H2O + NV6_O2 + NV6_N2
            xV6_H2O = NV6_H2O / NV6
            xV6_O2 = NV6_O2 / NV6
            xV6_N2 = NV6_N2 / NV6
            Air_6 = PR.EosPengRobinson()
            Air_6.AirComposition_out(T = T6, P = self.P_atm, x_H2O = xV6_H2O, x_O2 = xV6_O2, x_N2 = xV6_N2)
            Air_6.Z_mix()
            Air_6.MolarVolume()
            Air_6.Enthalpy()
            Air_6.fugacity()

            #Current V7
            Air_7 = PR.EosPengRobinson()
            Air_7.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_7.Z_mix()
            Air_7.MolarVolume()
            Air_7.Enthalpy()
            NV7 = Fv_vin / Air_7.Vm_mix_v
            NV7_H2O = NV7 * Air_7.x_H2O
            NV7_O2 = NV7 * Air_7.x_O2
            NV7_N2 = NV7 * Air_7.x_N2

            ## Equation system Stage 1
            # mass balances
            H2O_1 = (NL0_H2O + NV2_H2O) - (NL1_H2O + NV1_H2O)
            O2_1 = (NL0_O2 + NV2_O2) - (NL1_O2 + NV1_O2)
            N2_1 = (NL0_N2 + NV2_N2) - (NL1_N2 + NV1_N2)
            # Equilibrium
            Eq_H2O_1 = (Water_1.x_H2O * Water_1.phi_l['H2O']) - (Air_1.x_H2O * Air_1.phi_v['H2O'])
            Eq_O2_1 = (Water_1.x_O2 * Water_1.phi_l['O2']) - (Air_1.x_O2 * Air_1.phi_v['O2'])
            Eq_N2_1 = (Water_1.x_N2 * Water_1.phi_l['N2']) - (Air_1.x_N2 * Air_1.phi_v['N2'])
            # Energy balance
            Energy_1 = (NL0 * Water_0.H_l + NV2 * Air_2.H_v) - (NL1 * Water_1.H_l + NV1 * Air_1.H_v)

            ## Equation system Stage 2
            # mass balances
            H2O_2 = (NL1_H2O + NV3_H2O) - (NL2_H2O + NV2_H2O)
            O2_2 = (NL1_O2 + NV3_O2) - (NL2_O2 + NV2_O2)
            N2_2 = (NL1_N2 + NV3_N2) - (NL2_N2 + NV2_N2)
            # Equilibrium
            Eq_H2O_2 = (Water_2.x_H2O * Water_2.phi_l['H2O']) - (Air_2.x_H2O * Air_2.phi_v['H2O'])
            Eq_O2_2 = (Water_2.x_O2 * Water_2.phi_l['O2']) - (Air_2.x_O2 * Air_2.phi_v['O2'])
            Eq_N2_2 = (Water_2.x_N2 * Water_2.phi_l['N2']) - (Air_2.x_N2 * Air_2.phi_v['N2'])
            # Energy balance
            Energy_2 = (NL1 * Water_1.H_l + NV3 * Air_3.H_v) - (NL2 * Water_2.H_l + NV2 * Air_2.H_v)

            ## Equation system Stage 3
            # mass balances
            H2O_3 = (NL2_H2O + NV4_H2O) - (NL3_H2O + NV3_H2O)
            O2_3 = (NL2_O2 + NV4_O2) - (NL3_O2 + NV3_O2)
            N2_3 = (NL2_N2 + NV4_N2) - (NL3_N2 + NV3_N2)
            # Equilibrium
            Eq_H2O_3 = (Water_3.x_H2O * Water_3.phi_l['H2O']) - (Air_3.x_H2O * Air_3.phi_v['H2O'])
            Eq_O2_3 = (Water_3.x_O2 * Water_3.phi_l['O2']) - (Air_3.x_O2 * Air_3.phi_v['O2'])
            Eq_N2_3 = (Water_3.x_N2 * Water_3.phi_l['N2']) - (Air_3.x_N2 * Air_3.phi_v['N2'])
            # Energy balance
            Energy_3 = (NL2 * Water_2.H_l + NV4 * Air_4.H_v) - (NL3 * Water_3.H_l + NV3 * Air_3.H_v)

            ## Equation system Stage 4
            # mass balances
            H2O_4 = (NL3_H2O + NV5_H2O) - (NL4_H2O + NV4_H2O)
            O2_4 = (NL3_O2 + NV5_O2) - (NL4_O2 + NV4_O2)
            N2_4 = (NL3_N2 + NV5_N2) - (NL4_N2 + NV4_N2)
            # Equilibrium
            Eq_H2O_4 = (Water_4.x_H2O * Water_4.phi_l['H2O']) - (Air_4.x_H2O * Air_4.phi_v['H2O'])
            Eq_O2_4 = (Water_4.x_O2 * Water_4.phi_l['O2']) - (Air_4.x_O2 * Air_4.phi_v['O2'])
            Eq_N2_4 = (Water_4.x_N2 * Water_4.phi_l['N2']) - (Air_4.x_N2 * Air_4.phi_v['N2'])
            # Energy balance
            Energy_4 = (NL3 * Water_3.H_l + NV5 * Air_5.H_v) - (NL4 * Water_4.H_l + NV4 * Air_4.H_v)

            ## Equation system Stage 5
            # mass balances
            H2O_5 = (NL4_H2O + NV6_H2O) - (NL5_H2O + NV5_H2O)
            O2_5 = (NL4_O2 + NV6_O2) - (NL5_O2 + NV5_O2)
            N2_5 = (NL4_N2 + NV6_N2) - (NL5_N2 + NV5_N2)
            # Equilibrium
            Eq_H2O_5 = (Water_5.x_H2O * Water_5.phi_l['H2O']) - (Air_5.x_H2O * Air_5.phi_v['H2O'])
            Eq_O2_5 = (Water_5.x_O2 * Water_5.phi_l['O2']) - (Air_5.x_O2 * Air_5.phi_v['O2'])
            Eq_N2_5 = (Water_5.x_N2 * Water_5.phi_l['N2']) - (Air_5.x_N2 * Air_5.phi_v['N2'])
            # Energy balance
            Energy_5 = (NL4 * Water_4.H_l + NV6 * Air_6.H_v) - (NL5 * Water_5.H_l + NV5 * Air_5.H_v)

            ## Equation system Stage 6
            # mass balances
            H2O_6 = (NL5_H2O + NV7_H2O) - (NL6_H2O + NV6_H2O)
            O2_6 = (NL5_O2 + NV7_O2) - (NL6_O2 + NV6_O2)
            N2_6 = (NL5_N2 + NV7_N2) - (NL6_N2 + NV6_N2)
            # Equilibrium
            Eq_H2O_6 = (Water_6.x_H2O * Water_6.phi_l['H2O']) - (Air_6.x_H2O * Air_6.phi_v['H2O'])
            Eq_O2_6 = (Water_6.x_O2 * Water_6.phi_l['O2']) - (Air_6.x_O2 * Air_6.phi_v['O2'])
            Eq_N2_6 = (Water_6.x_N2 * Water_6.phi_l['N2']) - (Air_6.x_N2 * Air_6.phi_v['N2'])
            # Energy balance
            Energy_6 = (NL5 * Water_5.H_l + NV7 * Air_7.H_v) - (NL6 * Water_6.H_l + NV6 * Air_6.H_v)


            return H2O_1, O2_1, N2_1, Eq_H2O_1, Eq_O2_1, Eq_N2_1, Energy_1, \
                   H2O_2, O2_2, N2_2, Eq_H2O_2, Eq_O2_2, Eq_N2_2, Energy_2, \
                   H2O_3, O2_3, N2_3, Eq_H2O_3, Eq_O2_3, Eq_N2_3, Energy_3, \
                   H2O_4, O2_4, N2_4, Eq_H2O_4, Eq_O2_4, Eq_N2_4, Energy_4, \
                   H2O_5, O2_5, N2_5, Eq_H2O_5, Eq_O2_5, Eq_N2_5, Energy_5, \
                   H2O_6, O2_6, N2_6, Eq_H2O_6, Eq_O2_6, Eq_N2_6, Energy_6
        
        def systemSevenStages (vars):
            NL1_H2O, NL1_O2, NL1_N2, NV1_H2O, NV1_O2, NV1_N2, T1,\
            NL2_H2O, NL2_O2, NL2_N2, NV2_H2O, NV2_O2, NV2_N2, T2,\
            NL3_H2O, NL3_O2, NL3_N2, NV3_H2O, NV3_O2, NV3_N2, T3,\
            NL4_H2O, NL4_O2, NL4_N2, NV4_H2O, NV4_O2, NV4_N2, T4,\
            NL5_H2O, NL5_O2, NL5_N2, NV5_H2O, NV5_O2, NV5_N2, T5,\
            NL6_H2O, NL6_O2, NL6_N2, NV6_H2O, NV6_O2, NV6_N2, T6,\
            NL7_H2O, NL7_O2, NL7_N2, NV7_H2O, NV7_O2, NV7_N2, T7,= vars    #vars for stage 1

            ##Liquid currents
            #Current L0
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T = self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = self.Fv_Lin / Water_0.Vm_mix_l
            NL0_H2O = NL0 * Water_0.x_H2O
            NL0_O2 = NL0 * Water_0.x_O2
            NL0_N2 = NL0 * Water_0.x_N2

            #Current L1
            NL1 = NL1_H2O + NL1_O2 + NL1_N2
            xL1_H2O = NL1_H2O / NL1
            xL1_O2 = NL1_O2 / NL1
            xL1_N2 = NL1_N2 / NL1
            Water_1 = PR.EosPengRobinson()
            Water_1.WaterComposition(T = T1, P = self.P_atm, xH2O = xL1_H2O, x_O2 = xL1_O2, x_N2 = xL1_N2)
            Water_1.Z_mix()
            Water_1.MolarVolume()
            Water_1.Enthalpy()
            Water_1.fugacity()

            #Current L2
            NL2 = NL2_H2O + NL2_O2 + NL2_N2
            xL2_H2O = NL2_H2O / NL2
            xL2_O2 = NL2_O2 / NL2
            xL2_N2 = NL2_N2 / NL2
            Water_2 = PR.EosPengRobinson()
            Water_2.WaterComposition(T = T2, P = self.P_atm, xH2O = xL2_H2O, x_O2 = xL2_O2, x_N2 = xL2_N2)
            Water_2.Z_mix()
            Water_2.MolarVolume()
            Water_2.Enthalpy()
            Water_2.fugacity()

            #Current L3
            NL3 = NL3_H2O + NL3_O2 + NL3_N2
            xL3_H2O = NL3_H2O / NL3
            xL3_O2 = NL3_O2 / NL3
            xL3_N2 = NL3_N2 / NL3
            Water_3 = PR.EosPengRobinson()
            Water_3.WaterComposition(T = T3, P = self.P_atm, xH2O = xL3_H2O, x_O2 = xL3_O2, x_N2 = xL3_N2)
            Water_3.Z_mix()
            Water_3.MolarVolume()
            Water_3.Enthalpy()
            Water_3.fugacity()

            #Current L4
            NL4 = NL4_H2O + NL4_O2 + NL4_N2
            xL4_H2O = NL4_H2O / NL4
            xL4_O2 = NL4_O2 / NL4
            xL4_N2 = NL4_N2 / NL4
            Water_4 = PR.EosPengRobinson()
            Water_4.WaterComposition(T = T4, P = self.P_atm, xH2O = xL4_H2O, x_O2 = xL4_O2, x_N2 = xL4_N2)
            Water_4.Z_mix()
            Water_4.MolarVolume()
            Water_4.Enthalpy()
            Water_4.fugacity()

            #Current L5
            NL5 = NL5_H2O + NL5_O2 + NL5_N2
            xL5_H2O = NL5_H2O / NL5
            xL5_O2 = NL5_O2 / NL5
            xL5_N2 = NL5_N2 / NL5
            Water_5 = PR.EosPengRobinson()
            Water_5.WaterComposition(T = T5, P = self.P_atm, xH2O = xL5_H2O, x_O2 = xL5_O2, x_N2 = xL5_N2)
            Water_5.Z_mix()
            Water_5.MolarVolume()
            Water_5.Enthalpy()
            Water_5.fugacity()

            #Current L6
            NL6 = NL6_H2O + NL6_O2 + NL6_N2
            xL6_H2O = NL6_H2O / NL6
            xL6_O2 = NL6_O2 / NL6
            xL6_N2 = NL6_N2 / NL6
            Water_6 = PR.EosPengRobinson()
            Water_6.WaterComposition(T = T6, P = self.P_atm, xH2O = xL6_H2O, x_O2 = xL6_O2, x_N2 = xL6_N2)
            Water_6.Z_mix()
            Water_6.MolarVolume()
            Water_6.Enthalpy()
            Water_6.fugacity()

            #Current L7
            NL7 = NL7_H2O + NL7_O2 + NL7_N2
            xL7_H2O = NL7_H2O / NL7
            xL7_O2 = NL7_O2 / NL7
            xL7_N2 = NL7_N2 / NL7
            Water_7 = PR.EosPengRobinson()
            Water_7.WaterComposition(T = T7, P = self.P_atm, xH2O = xL7_H2O, x_O2 = xL7_O2, x_N2 = xL7_N2)
            Water_7.Z_mix()
            Water_7.MolarVolume()
            Water_7.Enthalpy()
            Water_7.fugacity()

            ##Gas currents
            #Current V1
            NV1 = NV1_H2O + NV1_O2 + NV1_N2
            xV1_H2O = NV1_H2O / NV1
            xV1_O2 = NV1_O2 / NV1
            xV1_N2 = NV1_N2 / NV1
            Air_1 = PR.EosPengRobinson()
            Air_1.AirComposition_out(T = T1, P = self.P_atm, x_H2O = xV1_H2O, x_O2 = xV1_O2, x_N2 = xV1_N2)
            Air_1.Z_mix()
            Air_1.MolarVolume()
            Air_1.Enthalpy()
            Air_1.fugacity()

            #Current V2
            NV2 = NV2_H2O + NV2_O2 + NV2_N2
            xV2_H2O = NV2_H2O / NV2
            xV2_O2 = NV2_O2 / NV2
            xV2_N2 = NV2_N2 / NV2
            Air_2 = PR.EosPengRobinson()
            Air_2.AirComposition_out(T = T2, P = self.P_atm, x_H2O = xV2_H2O, x_O2 = xV2_O2, x_N2 = xV2_N2)
            Air_2.Z_mix()
            Air_2.MolarVolume()
            Air_2.Enthalpy()
            Air_2.fugacity()

            #Current V3
            NV3 = NV3_H2O + NV3_O2 + NV3_N2
            xV3_H2O = NV3_H2O / NV3
            xV3_O2 = NV3_O2 / NV3
            xV3_N2 = NV3_N2 / NV3
            Air_3 = PR.EosPengRobinson()
            Air_3.AirComposition_out(T = T3, P = self.P_atm, x_H2O = xV3_H2O, x_O2 = xV3_O2, x_N2 = xV3_N2)
            Air_3.Z_mix()
            Air_3.MolarVolume()
            Air_3.Enthalpy()
            Air_3.fugacity()

            #Current V4
            NV4 = NV4_H2O + NV4_O2 + NV4_N2
            xV4_H2O = NV4_H2O / NV4
            xV4_O2 = NV4_O2 / NV4
            xV4_N2 = NV4_N2 / NV4
            Air_4 = PR.EosPengRobinson()
            Air_4.AirComposition_out(T = T4, P = self.P_atm, x_H2O = xV4_H2O, x_O2 = xV4_O2, x_N2 = xV4_N2)
            Air_4.Z_mix()
            Air_4.MolarVolume()
            Air_4.Enthalpy()
            Air_4.fugacity()

            #Current V5
            NV5 = NV5_H2O + NV5_O2 + NV5_N2
            xV5_H2O = NV5_H2O / NV5
            xV5_O2 = NV5_O2 / NV5
            xV5_N2 = NV5_N2 / NV5
            Air_5 = PR.EosPengRobinson()
            Air_5.AirComposition_out(T = T5, P = self.P_atm, x_H2O = xV5_H2O, x_O2 = xV5_O2, x_N2 = xV5_N2)
            Air_5.Z_mix()
            Air_5.MolarVolume()
            Air_5.Enthalpy()
            Air_5.fugacity()

            #Current V6
            NV6 = NV6_H2O + NV6_O2 + NV6_N2
            xV6_H2O = NV6_H2O / NV6
            xV6_O2 = NV6_O2 / NV6
            xV6_N2 = NV6_N2 / NV6
            Air_6 = PR.EosPengRobinson()
            Air_6.AirComposition_out(T = T6, P = self.P_atm, x_H2O = xV6_H2O, x_O2 = xV6_O2, x_N2 = xV6_N2)
            Air_6.Z_mix()
            Air_6.MolarVolume()
            Air_6.Enthalpy()
            Air_6.fugacity()

            #Current V7
            NV7 = NV7_H2O + NV7_O2 + NV7_N2
            xV7_H2O = NV7_H2O / NV7
            xV7_O2 = NV7_O2 / NV7
            xV7_N2 = NV7_N2 / NV7
            Air_7 = PR.EosPengRobinson()
            Air_7.AirComposition_out(T = T7, P = self.P_atm, x_H2O = xV7_H2O, x_O2 = xV7_O2, x_N2 = xV7_N2)
            Air_7.Z_mix()
            Air_7.MolarVolume()
            Air_7.Enthalpy()
            Air_7.fugacity()

            #Current V8
            Air_8 = PR.EosPengRobinson()
            Air_8.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_8.Z_mix()
            Air_8.MolarVolume()
            Air_8.Enthalpy()
            NV8 = Fv_vin / Air_8.Vm_mix_v
            NV8_H2O = NV8 * Air_8.x_H2O
            NV8_O2 = NV8 * Air_8.x_O2
            NV8_N2 = NV8 * Air_8.x_N2

            ## Equation system Stage 1
            # mass balances
            H2O_1 = (NL0_H2O + NV2_H2O) - (NL1_H2O + NV1_H2O)
            O2_1 = (NL0_O2 + NV2_O2) - (NL1_O2 + NV1_O2)
            N2_1 = (NL0_N2 + NV2_N2) - (NL1_N2 + NV1_N2)
            # Equilibrium
            Eq_H2O_1 = (Water_1.x_H2O * Water_1.phi_l['H2O']) - (Air_1.x_H2O * Air_1.phi_v['H2O'])
            Eq_O2_1 = (Water_1.x_O2 * Water_1.phi_l['O2']) - (Air_1.x_O2 * Air_1.phi_v['O2'])
            Eq_N2_1 = (Water_1.x_N2 * Water_1.phi_l['N2']) - (Air_1.x_N2 * Air_1.phi_v['N2'])
            # Energy balance
            Energy_1 = (NL0 * Water_0.H_l + NV2 * Air_2.H_v) - (NL1 * Water_1.H_l + NV1 * Air_1.H_v)

            ## Equation system Stage 2
            # mass balances
            H2O_2 = (NL1_H2O + NV3_H2O) - (NL2_H2O + NV2_H2O)
            O2_2 = (NL1_O2 + NV3_O2) - (NL2_O2 + NV2_O2)
            N2_2 = (NL1_N2 + NV3_N2) - (NL2_N2 + NV2_N2)
            # Equilibrium
            Eq_H2O_2 = (Water_2.x_H2O * Water_2.phi_l['H2O']) - (Air_2.x_H2O * Air_2.phi_v['H2O'])
            Eq_O2_2 = (Water_2.x_O2 * Water_2.phi_l['O2']) - (Air_2.x_O2 * Air_2.phi_v['O2'])
            Eq_N2_2 = (Water_2.x_N2 * Water_2.phi_l['N2']) - (Air_2.x_N2 * Air_2.phi_v['N2'])
            # Energy balance
            Energy_2 = (NL1 * Water_1.H_l + NV3 * Air_3.H_v) - (NL2 * Water_2.H_l + NV2 * Air_2.H_v)

            ## Equation system Stage 3
            # mass balances
            H2O_3 = (NL2_H2O + NV4_H2O) - (NL3_H2O + NV3_H2O)
            O2_3 = (NL2_O2 + NV4_O2) - (NL3_O2 + NV3_O2)
            N2_3 = (NL2_N2 + NV4_N2) - (NL3_N2 + NV3_N2)
            # Equilibrium
            Eq_H2O_3 = (Water_3.x_H2O * Water_3.phi_l['H2O']) - (Air_3.x_H2O * Air_3.phi_v['H2O'])
            Eq_O2_3 = (Water_3.x_O2 * Water_3.phi_l['O2']) - (Air_3.x_O2 * Air_3.phi_v['O2'])
            Eq_N2_3 = (Water_3.x_N2 * Water_3.phi_l['N2']) - (Air_3.x_N2 * Air_3.phi_v['N2'])
            # Energy balance
            Energy_3 = (NL2 * Water_2.H_l + NV4 * Air_4.H_v) - (NL3 * Water_3.H_l + NV3 * Air_3.H_v)

            ## Equation system Stage 4
            # mass balances
            H2O_4 = (NL3_H2O + NV5_H2O) - (NL4_H2O + NV4_H2O)
            O2_4 = (NL3_O2 + NV5_O2) - (NL4_O2 + NV4_O2)
            N2_4 = (NL3_N2 + NV5_N2) - (NL4_N2 + NV4_N2)
            # Equilibrium
            Eq_H2O_4 = (Water_4.x_H2O * Water_4.phi_l['H2O']) - (Air_4.x_H2O * Air_4.phi_v['H2O'])
            Eq_O2_4 = (Water_4.x_O2 * Water_4.phi_l['O2']) - (Air_4.x_O2 * Air_4.phi_v['O2'])
            Eq_N2_4 = (Water_4.x_N2 * Water_4.phi_l['N2']) - (Air_4.x_N2 * Air_4.phi_v['N2'])
            # Energy balance
            Energy_4 = (NL3 * Water_3.H_l + NV5 * Air_5.H_v) - (NL4 * Water_4.H_l + NV4 * Air_4.H_v)

            ## Equation system Stage 5
            # mass balances
            H2O_5 = (NL4_H2O + NV6_H2O) - (NL5_H2O + NV5_H2O)
            O2_5 = (NL4_O2 + NV6_O2) - (NL5_O2 + NV5_O2)
            N2_5 = (NL4_N2 + NV6_N2) - (NL5_N2 + NV5_N2)
            # Equilibrium
            Eq_H2O_5 = (Water_5.x_H2O * Water_5.phi_l['H2O']) - (Air_5.x_H2O * Air_5.phi_v['H2O'])
            Eq_O2_5 = (Water_5.x_O2 * Water_5.phi_l['O2']) - (Air_5.x_O2 * Air_5.phi_v['O2'])
            Eq_N2_5 = (Water_5.x_N2 * Water_5.phi_l['N2']) - (Air_5.x_N2 * Air_5.phi_v['N2'])
            # Energy balance
            Energy_5 = (NL4 * Water_4.H_l + NV6 * Air_6.H_v) - (NL5 * Water_5.H_l + NV5 * Air_5.H_v)

            ## Equation system Stage 6
            # mass balances
            H2O_6 = (NL5_H2O + NV7_H2O) - (NL6_H2O + NV6_H2O)
            O2_6 = (NL5_O2 + NV7_O2) - (NL6_O2 + NV6_O2)
            N2_6 = (NL5_N2 + NV7_N2) - (NL6_N2 + NV6_N2)
            # Equilibrium
            Eq_H2O_6 = (Water_6.x_H2O * Water_6.phi_l['H2O']) - (Air_6.x_H2O * Air_6.phi_v['H2O'])
            Eq_O2_6 = (Water_6.x_O2 * Water_6.phi_l['O2']) - (Air_6.x_O2 * Air_6.phi_v['O2'])
            Eq_N2_6 = (Water_6.x_N2 * Water_6.phi_l['N2']) - (Air_6.x_N2 * Air_6.phi_v['N2'])
            # Energy balance
            Energy_6 = (NL5 * Water_5.H_l + NV7 * Air_7.H_v) - (NL6 * Water_6.H_l + NV6 * Air_6.H_v)

            ## Equation system Stage 7
            # mass balances
            H2O_7 = (NL6_H2O + NV8_H2O) - (NL7_H2O + NV7_H2O)
            O2_7 = (NL6_O2 + NV8_O2) - (NL7_O2 + NV7_O2)
            N2_7 = (NL6_N2 + NV8_N2) - (NL7_N2 + NV7_N2)
            # Equilibrium
            Eq_H2O_7 = (Water_7.x_H2O * Water_7.phi_l['H2O']) - (Air_7.x_H2O * Air_7.phi_v['H2O'])
            Eq_O2_7 = (Water_7.x_O2 * Water_7.phi_l['O2']) - (Air_7.x_O2 * Air_7.phi_v['O2'])
            Eq_N2_7 = (Water_7.x_N2 * Water_7.phi_l['N2']) - (Air_7.x_N2 * Air_7.phi_v['N2'])
            # Energy balance
            Energy_7 = (NL6 * Water_6.H_l + NV8 * Air_8.H_v) - (NL7 * Water_7.H_l + NV7 * Air_7.H_v)


            return H2O_1, O2_1, N2_1, Eq_H2O_1, Eq_O2_1, Eq_N2_1, Energy_1, \
                   H2O_2, O2_2, N2_2, Eq_H2O_2, Eq_O2_2, Eq_N2_2, Energy_2, \
                   H2O_3, O2_3, N2_3, Eq_H2O_3, Eq_O2_3, Eq_N2_3, Energy_3, \
                   H2O_4, O2_4, N2_4, Eq_H2O_4, Eq_O2_4, Eq_N2_4, Energy_4, \
                   H2O_5, O2_5, N2_5, Eq_H2O_5, Eq_O2_5, Eq_N2_5, Energy_5, \
                   H2O_6, O2_6, N2_6, Eq_H2O_6, Eq_O2_6, Eq_N2_6, Energy_6, \
                   H2O_7, O2_7, N2_7, Eq_H2O_7, Eq_O2_7, Eq_N2_7, Energy_7
        
        def systemEightStages (vars):
            NL1_H2O, NL1_O2, NL1_N2, NV1_H2O, NV1_O2, NV1_N2, T1,\
            NL2_H2O, NL2_O2, NL2_N2, NV2_H2O, NV2_O2, NV2_N2, T2,\
            NL3_H2O, NL3_O2, NL3_N2, NV3_H2O, NV3_O2, NV3_N2, T3,\
            NL4_H2O, NL4_O2, NL4_N2, NV4_H2O, NV4_O2, NV4_N2, T4,\
            NL5_H2O, NL5_O2, NL5_N2, NV5_H2O, NV5_O2, NV5_N2, T5,\
            NL6_H2O, NL6_O2, NL6_N2, NV6_H2O, NV6_O2, NV6_N2, T6,\
            NL7_H2O, NL7_O2, NL7_N2, NV7_H2O, NV7_O2, NV7_N2, T7,\
            NL8_H2O, NL8_O2, NL8_N2, NV8_H2O, NV8_O2, NV8_N2, T8 = vars    #vars for stage 1

            ##Liquid currents
            #Current L0
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T = self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = self.Fv_Lin / Water_0.Vm_mix_l
            NL0_H2O = NL0 * Water_0.x_H2O
            NL0_O2 = NL0 * Water_0.x_O2
            NL0_N2 = NL0 * Water_0.x_N2

            #Current L1
            NL1 = NL1_H2O + NL1_O2 + NL1_N2
            xL1_H2O = NL1_H2O / NL1
            xL1_O2 = NL1_O2 / NL1
            xL1_N2 = NL1_N2 / NL1
            Water_1 = PR.EosPengRobinson()
            Water_1.WaterComposition(T = T1, P = self.P_atm, xH2O = xL1_H2O, x_O2 = xL1_O2, x_N2 = xL1_N2)
            Water_1.Z_mix()
            Water_1.MolarVolume()
            Water_1.Enthalpy()
            Water_1.fugacity()

            #Current L2
            NL2 = NL2_H2O + NL2_O2 + NL2_N2
            xL2_H2O = NL2_H2O / NL2
            xL2_O2 = NL2_O2 / NL2
            xL2_N2 = NL2_N2 / NL2
            Water_2 = PR.EosPengRobinson()
            Water_2.WaterComposition(T = T2, P = self.P_atm, xH2O = xL2_H2O, x_O2 = xL2_O2, x_N2 = xL2_N2)
            Water_2.Z_mix()
            Water_2.MolarVolume()
            Water_2.Enthalpy()
            Water_2.fugacity()

            #Current L3
            NL3 = NL3_H2O + NL3_O2 + NL3_N2
            xL3_H2O = NL3_H2O / NL3
            xL3_O2 = NL3_O2 / NL3
            xL3_N2 = NL3_N2 / NL3
            Water_3 = PR.EosPengRobinson()
            Water_3.WaterComposition(T = T3, P = self.P_atm, xH2O = xL3_H2O, x_O2 = xL3_O2, x_N2 = xL3_N2)
            Water_3.Z_mix()
            Water_3.MolarVolume()
            Water_3.Enthalpy()
            Water_3.fugacity()

            #Current L4
            NL4 = NL4_H2O + NL4_O2 + NL4_N2
            xL4_H2O = NL4_H2O / NL4
            xL4_O2 = NL4_O2 / NL4
            xL4_N2 = NL4_N2 / NL4
            Water_4 = PR.EosPengRobinson()
            Water_4.WaterComposition(T = T4, P = self.P_atm, xH2O = xL4_H2O, x_O2 = xL4_O2, x_N2 = xL4_N2)
            Water_4.Z_mix()
            Water_4.MolarVolume()
            Water_4.Enthalpy()
            Water_4.fugacity()

            #Current L5
            NL5 = NL5_H2O + NL5_O2 + NL5_N2
            xL5_H2O = NL5_H2O / NL5
            xL5_O2 = NL5_O2 / NL5
            xL5_N2 = NL5_N2 / NL5
            Water_5 = PR.EosPengRobinson()
            Water_5.WaterComposition(T = T5, P = self.P_atm, xH2O = xL5_H2O, x_O2 = xL5_O2, x_N2 = xL5_N2)
            Water_5.Z_mix()
            Water_5.MolarVolume()
            Water_5.Enthalpy()
            Water_5.fugacity()

            #Current L6
            NL6 = NL6_H2O + NL6_O2 + NL6_N2
            xL6_H2O = NL6_H2O / NL6
            xL6_O2 = NL6_O2 / NL6
            xL6_N2 = NL6_N2 / NL6
            Water_6 = PR.EosPengRobinson()
            Water_6.WaterComposition(T = T6, P = self.P_atm, xH2O = xL6_H2O, x_O2 = xL6_O2, x_N2 = xL6_N2)
            Water_6.Z_mix()
            Water_6.MolarVolume()
            Water_6.Enthalpy()
            Water_6.fugacity()

            #Current L7
            NL7 = NL7_H2O + NL7_O2 + NL7_N2
            xL7_H2O = NL7_H2O / NL7
            xL7_O2 = NL7_O2 / NL7
            xL7_N2 = NL7_N2 / NL7
            Water_7 = PR.EosPengRobinson()
            Water_7.WaterComposition(T = T7, P = self.P_atm, xH2O = xL7_H2O, x_O2 = xL7_O2, x_N2 = xL7_N2)
            Water_7.Z_mix()
            Water_7.MolarVolume()
            Water_7.Enthalpy()
            Water_7.fugacity()

            #Current L8
            NL8 = NL8_H2O + NL8_O2 + NL8_N2
            xL8_H2O = NL8_H2O / NL8
            xL8_O2 = NL8_O2 / NL8
            xL8_N2 = NL8_N2 / NL8
            Water_8 = PR.EosPengRobinson()
            Water_8.WaterComposition(T = T8, P = self.P_atm, xH2O = xL8_H2O, x_O2 = xL8_O2, x_N2 = xL8_N2)
            Water_8.Z_mix()
            Water_8.MolarVolume()
            Water_8.Enthalpy()
            Water_8.fugacity()

            ##Gas currents
            #Current V1
            NV1 = NV1_H2O + NV1_O2 + NV1_N2
            xV1_H2O = NV1_H2O / NV1
            xV1_O2 = NV1_O2 / NV1
            xV1_N2 = NV1_N2 / NV1
            Air_1 = PR.EosPengRobinson()
            Air_1.AirComposition_out(T = T1, P = self.P_atm, x_H2O = xV1_H2O, x_O2 = xV1_O2, x_N2 = xV1_N2)
            Air_1.Z_mix()
            Air_1.MolarVolume()
            Air_1.Enthalpy()
            Air_1.fugacity()

            #Current V2
            NV2 = NV2_H2O + NV2_O2 + NV2_N2
            xV2_H2O = NV2_H2O / NV2
            xV2_O2 = NV2_O2 / NV2
            xV2_N2 = NV2_N2 / NV2
            Air_2 = PR.EosPengRobinson()
            Air_2.AirComposition_out(T = T2, P = self.P_atm, x_H2O = xV2_H2O, x_O2 = xV2_O2, x_N2 = xV2_N2)
            Air_2.Z_mix()
            Air_2.MolarVolume()
            Air_2.Enthalpy()
            Air_2.fugacity()

            #Current V3
            NV3 = NV3_H2O + NV3_O2 + NV3_N2
            xV3_H2O = NV3_H2O / NV3
            xV3_O2 = NV3_O2 / NV3
            xV3_N2 = NV3_N2 / NV3
            Air_3 = PR.EosPengRobinson()
            Air_3.AirComposition_out(T = T3, P = self.P_atm, x_H2O = xV3_H2O, x_O2 = xV3_O2, x_N2 = xV3_N2)
            Air_3.Z_mix()
            Air_3.MolarVolume()
            Air_3.Enthalpy()
            Air_3.fugacity()

            #Current V4
            NV4 = NV4_H2O + NV4_O2 + NV4_N2
            xV4_H2O = NV4_H2O / NV4
            xV4_O2 = NV4_O2 / NV4
            xV4_N2 = NV4_N2 / NV4
            Air_4 = PR.EosPengRobinson()
            Air_4.AirComposition_out(T = T4, P = self.P_atm, x_H2O = xV4_H2O, x_O2 = xV4_O2, x_N2 = xV4_N2)
            Air_4.Z_mix()
            Air_4.MolarVolume()
            Air_4.Enthalpy()
            Air_4.fugacity()

            #Current V5
            NV5 = NV5_H2O + NV5_O2 + NV5_N2
            xV5_H2O = NV5_H2O / NV5
            xV5_O2 = NV5_O2 / NV5
            xV5_N2 = NV5_N2 / NV5
            Air_5 = PR.EosPengRobinson()
            Air_5.AirComposition_out(T = T5, P = self.P_atm, x_H2O = xV5_H2O, x_O2 = xV5_O2, x_N2 = xV5_N2)
            Air_5.Z_mix()
            Air_5.MolarVolume()
            Air_5.Enthalpy()
            Air_5.fugacity()

            #Current V6
            NV6 = NV6_H2O + NV6_O2 + NV6_N2
            xV6_H2O = NV6_H2O / NV6
            xV6_O2 = NV6_O2 / NV6
            xV6_N2 = NV6_N2 / NV6
            Air_6 = PR.EosPengRobinson()
            Air_6.AirComposition_out(T = T6, P = self.P_atm, x_H2O = xV6_H2O, x_O2 = xV6_O2, x_N2 = xV6_N2)
            Air_6.Z_mix()
            Air_6.MolarVolume()
            Air_6.Enthalpy()
            Air_6.fugacity()

            #Current V7
            NV7 = NV7_H2O + NV7_O2 + NV7_N2
            xV7_H2O = NV7_H2O / NV7
            xV7_O2 = NV7_O2 / NV7
            xV7_N2 = NV7_N2 / NV7
            Air_7 = PR.EosPengRobinson()
            Air_7.AirComposition_out(T = T7, P = self.P_atm, x_H2O = xV7_H2O, x_O2 = xV7_O2, x_N2 = xV7_N2)
            Air_7.Z_mix()
            Air_7.MolarVolume()
            Air_7.Enthalpy()
            Air_7.fugacity()

            #Current V8
            NV8 = NV8_H2O + NV8_O2 + NV8_N2
            xV8_H2O = NV8_H2O / NV8
            xV8_O2 = NV8_O2 / NV8
            xV8_N2 = NV8_N2 / NV8
            Air_8 = PR.EosPengRobinson()
            Air_8.AirComposition_out(T = T8, P = self.P_atm, x_H2O = xV8_H2O, x_O2 = xV8_O2, x_N2 = xV8_N2)
            Air_8.Z_mix()
            Air_8.MolarVolume()
            Air_8.Enthalpy()
            Air_8.fugacity()

            #Current V9
            Air_9 = PR.EosPengRobinson()
            Air_9.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_9.Z_mix()
            Air_9.MolarVolume()
            Air_9.Enthalpy()
            NV9 = Fv_vin / Air_9.Vm_mix_v
            NV9_H2O = NV9 * Air_9.x_H2O
            NV9_O2 = NV9 * Air_9.x_O2
            NV9_N2 = NV9 * Air_9.x_N2

            ## Equation system Stage 1
            # mass balances
            H2O_1 = (NL0_H2O + NV2_H2O) - (NL1_H2O + NV1_H2O)
            O2_1 = (NL0_O2 + NV2_O2) - (NL1_O2 + NV1_O2)
            N2_1 = (NL0_N2 + NV2_N2) - (NL1_N2 + NV1_N2)
            # Equilibrium
            Eq_H2O_1 = (Water_1.x_H2O * Water_1.phi_l['H2O']) - (Air_1.x_H2O * Air_1.phi_v['H2O'])
            Eq_O2_1 = (Water_1.x_O2 * Water_1.phi_l['O2']) - (Air_1.x_O2 * Air_1.phi_v['O2'])
            Eq_N2_1 = (Water_1.x_N2 * Water_1.phi_l['N2']) - (Air_1.x_N2 * Air_1.phi_v['N2'])
            # Energy balance
            Energy_1 = (NL0 * Water_0.H_l + NV2 * Air_2.H_v) - (NL1 * Water_1.H_l + NV1 * Air_1.H_v)

            ## Equation system Stage 2
            # mass balances
            H2O_2 = (NL1_H2O + NV3_H2O) - (NL2_H2O + NV2_H2O)
            O2_2 = (NL1_O2 + NV3_O2) - (NL2_O2 + NV2_O2)
            N2_2 = (NL1_N2 + NV3_N2) - (NL2_N2 + NV2_N2)
            # Equilibrium
            Eq_H2O_2 = (Water_2.x_H2O * Water_2.phi_l['H2O']) - (Air_2.x_H2O * Air_2.phi_v['H2O'])
            Eq_O2_2 = (Water_2.x_O2 * Water_2.phi_l['O2']) - (Air_2.x_O2 * Air_2.phi_v['O2'])
            Eq_N2_2 = (Water_2.x_N2 * Water_2.phi_l['N2']) - (Air_2.x_N2 * Air_2.phi_v['N2'])
            # Energy balance
            Energy_2 = (NL1 * Water_1.H_l + NV3 * Air_3.H_v) - (NL2 * Water_2.H_l + NV2 * Air_2.H_v)

            ## Equation system Stage 3
            # mass balances
            H2O_3 = (NL2_H2O + NV4_H2O) - (NL3_H2O + NV3_H2O)
            O2_3 = (NL2_O2 + NV4_O2) - (NL3_O2 + NV3_O2)
            N2_3 = (NL2_N2 + NV4_N2) - (NL3_N2 + NV3_N2)
            # Equilibrium
            Eq_H2O_3 = (Water_3.x_H2O * Water_3.phi_l['H2O']) - (Air_3.x_H2O * Air_3.phi_v['H2O'])
            Eq_O2_3 = (Water_3.x_O2 * Water_3.phi_l['O2']) - (Air_3.x_O2 * Air_3.phi_v['O2'])
            Eq_N2_3 = (Water_3.x_N2 * Water_3.phi_l['N2']) - (Air_3.x_N2 * Air_3.phi_v['N2'])
            # Energy balance
            Energy_3 = (NL2 * Water_2.H_l + NV4 * Air_4.H_v) - (NL3 * Water_3.H_l + NV3 * Air_3.H_v)

            ## Equation system Stage 4
            # mass balances
            H2O_4 = (NL3_H2O + NV5_H2O) - (NL4_H2O + NV4_H2O)
            O2_4 = (NL3_O2 + NV5_O2) - (NL4_O2 + NV4_O2)
            N2_4 = (NL3_N2 + NV5_N2) - (NL4_N2 + NV4_N2)
            # Equilibrium
            Eq_H2O_4 = (Water_4.x_H2O * Water_4.phi_l['H2O']) - (Air_4.x_H2O * Air_4.phi_v['H2O'])
            Eq_O2_4 = (Water_4.x_O2 * Water_4.phi_l['O2']) - (Air_4.x_O2 * Air_4.phi_v['O2'])
            Eq_N2_4 = (Water_4.x_N2 * Water_4.phi_l['N2']) - (Air_4.x_N2 * Air_4.phi_v['N2'])
            # Energy balance
            Energy_4 = (NL3 * Water_3.H_l + NV5 * Air_5.H_v) - (NL4 * Water_4.H_l + NV4 * Air_4.H_v)

            ## Equation system Stage 5
            # mass balances
            H2O_5 = (NL4_H2O + NV6_H2O) - (NL5_H2O + NV5_H2O)
            O2_5 = (NL4_O2 + NV6_O2) - (NL5_O2 + NV5_O2)
            N2_5 = (NL4_N2 + NV6_N2) - (NL5_N2 + NV5_N2)
            # Equilibrium
            Eq_H2O_5 = (Water_5.x_H2O * Water_5.phi_l['H2O']) - (Air_5.x_H2O * Air_5.phi_v['H2O'])
            Eq_O2_5 = (Water_5.x_O2 * Water_5.phi_l['O2']) - (Air_5.x_O2 * Air_5.phi_v['O2'])
            Eq_N2_5 = (Water_5.x_N2 * Water_5.phi_l['N2']) - (Air_5.x_N2 * Air_5.phi_v['N2'])
            # Energy balance
            Energy_5 = (NL4 * Water_4.H_l + NV6 * Air_6.H_v) - (NL5 * Water_5.H_l + NV5 * Air_5.H_v)

            ## Equation system Stage 6
            # mass balances
            H2O_6 = (NL5_H2O + NV7_H2O) - (NL6_H2O + NV6_H2O)
            O2_6 = (NL5_O2 + NV7_O2) - (NL6_O2 + NV6_O2)
            N2_6 = (NL5_N2 + NV7_N2) - (NL6_N2 + NV6_N2)
            # Equilibrium
            Eq_H2O_6 = (Water_6.x_H2O * Water_6.phi_l['H2O']) - (Air_6.x_H2O * Air_6.phi_v['H2O'])
            Eq_O2_6 = (Water_6.x_O2 * Water_6.phi_l['O2']) - (Air_6.x_O2 * Air_6.phi_v['O2'])
            Eq_N2_6 = (Water_6.x_N2 * Water_6.phi_l['N2']) - (Air_6.x_N2 * Air_6.phi_v['N2'])
            # Energy balance
            Energy_6 = (NL5 * Water_5.H_l + NV7 * Air_7.H_v) - (NL6 * Water_6.H_l + NV6 * Air_6.H_v)

            ## Equation system Stage 7
            # mass balances
            H2O_7 = (NL6_H2O + NV8_H2O) - (NL7_H2O + NV7_H2O)
            O2_7 = (NL6_O2 + NV8_O2) - (NL7_O2 + NV7_O2)
            N2_7 = (NL6_N2 + NV8_N2) - (NL7_N2 + NV7_N2)
            # Equilibrium
            Eq_H2O_7 = (Water_7.x_H2O * Water_7.phi_l['H2O']) - (Air_7.x_H2O * Air_7.phi_v['H2O'])
            Eq_O2_7 = (Water_7.x_O2 * Water_7.phi_l['O2']) - (Air_7.x_O2 * Air_7.phi_v['O2'])
            Eq_N2_7 = (Water_7.x_N2 * Water_7.phi_l['N2']) - (Air_7.x_N2 * Air_7.phi_v['N2'])
            # Energy balance
            Energy_7 = (NL6 * Water_6.H_l + NV8 * Air_8.H_v) - (NL7 * Water_7.H_l + NV7 * Air_7.H_v)

            ## Equation system Stage 8
            # mass balances
            H2O_8 = (NL7_H2O + NV9_H2O) - (NL8_H2O + NV8_H2O)
            O2_8 = (NL7_O2 + NV9_O2) - (NL8_O2 + NV8_O2)
            N2_8 = (NL7_N2 + NV9_N2) - (NL8_N2 + NV8_N2)
            # Equilibrium
            Eq_H2O_8 = (Water_8.x_H2O * Water_8.phi_l['H2O']) - (Air_8.x_H2O * Air_8.phi_v['H2O'])
            Eq_O2_8 = (Water_8.x_O2 * Water_8.phi_l['O2']) - (Air_8.x_O2 * Air_8.phi_v['O2'])
            Eq_N2_8 = (Water_8.x_N2 * Water_8.phi_l['N2']) - (Air_8.x_N2 * Air_8.phi_v['N2'])
            # Energy balance
            Energy_8 = (NL7 * Water_7.H_l + NV9 * Air_9.H_v) - (NL8 * Water_8.H_l + NV8 * Air_8.H_v)


            return H2O_1, O2_1, N2_1, Eq_H2O_1, Eq_O2_1, Eq_N2_1, Energy_1, \
                   H2O_2, O2_2, N2_2, Eq_H2O_2, Eq_O2_2, Eq_N2_2, Energy_2, \
                   H2O_3, O2_3, N2_3, Eq_H2O_3, Eq_O2_3, Eq_N2_3, Energy_3, \
                   H2O_4, O2_4, N2_4, Eq_H2O_4, Eq_O2_4, Eq_N2_4, Energy_4, \
                   H2O_5, O2_5, N2_5, Eq_H2O_5, Eq_O2_5, Eq_N2_5, Energy_5, \
                   H2O_6, O2_6, N2_6, Eq_H2O_6, Eq_O2_6, Eq_N2_6, Energy_6, \
                   H2O_7, O2_7, N2_7, Eq_H2O_7, Eq_O2_7, Eq_N2_7, Energy_7, \
                   H2O_8, O2_8, N2_8, Eq_H2O_8, Eq_O2_8, Eq_N2_8, Energy_8, 
        
        if self.PacketType == "Structured":
            initial_conditions = [1, 0, 0, 0, 0.21, 0.79, 300]
            result = fsolve(systemOneStage, initial_conditions)
            self.numpySolution = [abs(x) for x in result]

            initial_conditions_2 = list(self.numpySolution) + list(self.numpySolution)
            result_2 = fsolve(systemTwoStages, initial_conditions_2)
        
            initial_conditions_3 = list(result_2) + list(result_2[0:7])
            result_3 = fsolve(systemThreeStages, initial_conditions_3)
    
            initial_conditions_4 = list(result_3) + list(result_3[0:7])
            result_4 = fsolve(systemFourStages, initial_conditions_4)

            initial_conditions_5 = list(result_4) + list(result_4[0:7])
            result_5 = fsolve(systemFiveStages, initial_conditions_5)

            initial_conditions_6 = list(result_5) + list(result_5[0:7])
            result_6 = fsolve(systemSixStages, initial_conditions_6)

            initial_conditions_7 = list(result_6) + list(result_6[0:7])
            result_7 = fsolve(systemSevenStages, initial_conditions_7)

            initial_conditions_8 = list(result_4) + list(result_4)
            result_8 =fsolve(systemEightStages, initial_conditions_8)

            #Humidity ratio top
            W_top = (result_8[3]*18.015)/(result_8[4]*31.999+result_8[5]*28.014)
            psychrolib.SetUnitSystem(psychrolib.SI)
            RH_top = psychrolib.GetRelHumFromHumRatio(result_8[6]-273.15, W_top, self.P_atm)
            
            #Caida de presión
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T=self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = (self.Fv_Lin)/Water_0.Vm_mix_l
            Water_0.ergun_pressure_drop(current = "Water", L=self.L, epsilon = self.epsilon, u = self.u_water, dp = self.dp)

            Water_8 = PR.EosPengRobinson()
            NL8 = result_8[49] + result_8[50] +  result_8[51]
            x8_H2O = result_8[49]/NL8
            x8_O2 = result_8[50]/NL8 
            x8_N2 = result_8[51]/NL8 
            Water_8.WaterComposition(T=result_8[55], P = self.P_atm, xH2O = x8_H2O, x_O2 = x8_O2, x_N2 = x8_N2)
            Water_8.Z_mix()
            Water_8.MolarVolume()
            Water_8.Enthalpy()

            Air_0 = PR.EosPengRobinson()
            Air_0.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_0.Z_mix()
            Air_0.MolarVolume()
            Air_0.ergun_pressure_drop(current= "Air", L = self.L, epsilon = self.epsilon, u = self.u_air, dp = self.dp)

            #Energy Balance
            Energy = (NL0*Water_0.H_l - NL8*Water_8.H_l)/1000000

            self.solution = list(result_8[0:5])
            self.solution.append(result_8[55])
            self.solution.append(result_8[6])
            self.solution.append(RH_top)
            self.solution.append(Energy)
            self.solution.append(Air_0.delta_P - Water_0.delta_P)
        
        elif self.PacketType == "CurvedSlats":
            initial_conditions = [1, 0, 0, 0, 0.21, 0.79, 300]
            result = fsolve(systemOneStage, initial_conditions)
            self.numpySolution = [abs(x) for x in result]

            initial_conditions_2 = list(self.numpySolution) + list(self.numpySolution)
            result_2 = fsolve(systemTwoStages, initial_conditions_2)
        
            initial_conditions_3 = list(result_2) + list(result_2[0:7])
            result_3 = fsolve(systemThreeStages, initial_conditions_3)
            
            initial_conditions_4 = list(result_3) + list(result_3[0:7])
            result_4 = fsolve(systemFourStages, initial_conditions_4)
            
            #Humidity ratio top
            W_top = (result_4[3]*18.015)/(result_4[4]*31.999+result_4[5]*28.014)
            psychrolib.SetUnitSystem(psychrolib.SI)
            RH_top = psychrolib.GetRelHumFromHumRatio(result_4[6]-273.15, W_top, self.P_atm)

            #Caida de presión
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T=self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = (self.Fv_Lin)/Water_0.Vm_mix_l
            Water_0.ergun_pressure_drop(current = "Water", L=self.L, epsilon = self.epsilon, u = self.u_water, dp = self.dp)

            Water_4 = PR.EosPengRobinson()
            NL4 = result_4[21] + result_4[22] +  result_4[23]
            x4_H2O = result_4[21]/NL4
            x4_O2 = result_4[22]/NL4 
            x4_N2 = result_4[23]/NL4 
            Water_4.WaterComposition(T=result_4[27], P = self.P_atm, xH2O = x4_H2O, x_O2 = x4_O2, x_N2 = x4_N2)
            Water_4.Z_mix()
            Water_4.MolarVolume()
            Water_4.Enthalpy()

            Energy = (NL0*Water_0.H_l - NL4*Water_4.H_l)/1000000

            Air_0 = PR.EosPengRobinson()
            Air_0.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_0.Z_mix()
            Air_0.MolarVolume()
            Air_0.ergun_pressure_drop(current= "Air", L = self.L, epsilon = self.epsilon, u = self.u_air, dp = self.dp)
            
            self.solution = list(result_4[0:5])
            self.solution.append(result_4[27])
            self.solution.append(result_4[6])
            self.solution.append(RH_top)
            self.solution.append(Energy)
            self.solution.append(Air_0.delta_P - Water_0.delta_P)
        
        elif self.PacketType == "FlatSlats":
            initial_conditions = [1, 0, 0, 0, 0.21, 0.79, 300]
            result = fsolve(systemOneStage, initial_conditions)
            self.numpySolution = [abs(x) for x in result]
            
            initial_conditions_2 = list(self.numpySolution) + list(self.numpySolution)
            result_2 = fsolve(systemTwoStages, initial_conditions_2)

            #Humidity ratio top
            W_top = (result_2[3]*18.015)/(result_2[4]*31.999+result_2[5]*28.014)
            psychrolib.SetUnitSystem(psychrolib.SI)
            RH_top = psychrolib.GetRelHumFromHumRatio(result_2[6]-273.15, W_top, self.P_atm)

            #Caida de presión
            Water_0 = PR.EosPengRobinson()
            Water_0.WaterComposition(T=self.T_Lin, P = self.P_atm, xH2O = 1, x_O2 = 1e-15, x_N2 = 1e-15)
            Water_0.Z_mix()
            Water_0.MolarVolume()
            Water_0.Enthalpy()
            NL0 = (self.Fv_Lin)/Water_0.Vm_mix_l
            Water_0.ergun_pressure_drop(current = "Water", L=self.L, epsilon = self.epsilon, u = self.u_water, dp = self.dp)

            Water_2 = PR.EosPengRobinson()
            NL2 = result_2[7] + result_2[8] +  result_2[9]
            x2_H2O = result_2[7]/NL2
            x2_O2 = result_2[8]/NL2
            x2_N2 = result_2[9]/NL2 
            Water_2.WaterComposition(T=result_2[13], P = self.P_atm, xH2O = x2_H2O, x_O2 = x2_O2, x_N2 = x2_N2)
            Water_2.Z_mix()
            Water_2.MolarVolume()
            Water_2.Enthalpy()

            Energy = (NL0*Water_0.H_l - NL2*Water_2.H_l)/1000000

            Air_0 = PR.EosPengRobinson()
            Air_0.AirCompositions_in(T = self.T_vin, RH = self.RH_air_in, P = self.P_atm)
            Air_0.Z_mix()
            Air_0.MolarVolume()
            Air_0.ergun_pressure_drop(current= "Air", L = self.L, epsilon = self.epsilon, u = self.u_air, dp = self.dp)

            self.solution = list(result_2[0:5])
            self.solution.append(result_2[13])
            self.solution.append(result_2[6])
            self.solution.append(RH_top)
            self.solution.append(Energy)
            self.solution.append(Air_0.delta_P - Water_0.delta_P)


# TowerOneStage = coolingTowerModel("Structured", 0.580, 0.0225)
# TowerOneStage.towerBalance(T_Lin = 40+273.15, P_atm = 90017, Fv_Lin = (0.3/1000)/60, T_vin = 20+273.15, Fv_vin=1/60, RH_air_in = 57.4)
# print(TowerOneStage.solution)