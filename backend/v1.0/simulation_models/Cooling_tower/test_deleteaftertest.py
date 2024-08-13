# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 10:52:31 2024

@author: Sergio
"""

import PengRobinson as PR

Air = PR.EosPengRobinson()
Air.AirCompositions(T = 300, RH = 10, P=101325)
Air.Z_mix()
print(Air.Z_v)
Air.fugacity()
print(Air.phi_v)
Air.Enthalpy()
print(Air.H_v)

Water = PR.EosPengRobinson()
Water.WaterComposition(T = 298.15, P=101325)
Water.Z_mix()
print(Water.Z_l)
Water.fugacity()
print(Water.phi_l)
Water.Enthalpy()
print(Water.H_l)



