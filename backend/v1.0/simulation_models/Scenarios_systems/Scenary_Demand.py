class Demand_Model:
    # Inicializacion de perfiles de demanda
    def __init__(self, simulationSteps, type, name, d_max = [10]):
        
        self.simulationSteps = simulationSteps # Número de pasos de simulación
        self.demandType = type # Tipo de demanda
        self.name = name # Nombre del sistema
        
        # Curva Personalizada
        if self.demandType == 0:
            self.demand = d_max
        # Valor fijo ingresado por el usuario
        elif self.demandType == 1:
            self.demand = [d_max] * self.simulationSteps
        # Demanda residencial
        elif self.demandType == 2:
            # Perfil de dia de la semana
            weekdayProfile = [0.4318, 0.4449, 0.4290, 0.4354, 0.5573, 0.7157, 0.7548, 0.7294, 0.7098, 0.4887, 0.5083, 0.5300, 0.4405, 0.4694, 0.4704, 0.4355, 0.4482, 0.4854, 0.9356, 0.9901, 1.0000, 0.7862, 0.6174, 0.5794]
            weekdayDemand = [i * d_max for i in weekdayProfile]
            # Perfil de dia sabado
            # saturdayProfile = [0.4318, 0.4449, 0.4290, 0.4354, 0.4973, 0.6557, 0.6948, 0.6694, 0.6498, 0.4887, 0.4483, 0.4700, 0.4405, 0.4694, 0.4704, 0.4355, 0.4482, 0.4854, 0.8756, 0.9301, 0.9400, 0.7262, 0.5574, 0.5194]
            # saturdayDemand = [i * d_max for i in saturdayProfile]
            # # Perfil de dia domingo
            # sundayProfile = [0.4318, 0.4449, 0.4290, 0.4354, 0.4573, 0.6157, 0.6548, 0.6294, 0.6098, 0.4887, 0.4083, 0.4300, 0.4405, 0.4694, 0.4704, 0.4355, 0.4482, 0.4854, 0.8356, 0.8901, 0.9000, 0.6862, 0.5174, 0.4794]
            # sundayDemand = [i * d_max for i in sundayProfile]
            
            demand = []
            demand.append(weekdayDemand)
            # [demand.append(weekdayDemand) for i in range(5)]
            # demand.append(saturdayDemand)
            # demand.append(sundayDemand)
            self.demand = demand[0]
        # Demanda comercial
        elif self.demandType == 3:
            # Perfil de dia de la semana
            weekdayProfile = [0.3799, 0.3570, 0.3420, 0.3363, 0.3332, 0.3363, 0.3908, 0.4582, 0.5921, 0.6798, 0.8796, 0.9533, 0.9948, 1.0000, 0.9969, 0.9979, 0.9974, 0.9761, 0.9419, 0.9263, 0.8300, 0.6900, 0.4925, 0.4200]
            weekdayDemand = [i * d_max for i in weekdayProfile]
            # Perfil de dia sabado
            # saturdayProfile = [0.3799, 0.3570, 0.3420, 0.3363, 0.3332, 0.3363, 0.3908, 0.4582, 0.5921, 0.6798, 0.8796, 0.9533, 0.9948, 1.0000, 0.9969, 0.9979, 0.9974, 0.9761, 0.9419, 0.9263, 0.9100, 0.7700, 0.5725, 0.4200]
            # saturdayDemand = [i * d_max for i in saturdayProfile]
            # # Perfil de dia domingo
            # sundayProfile = [0.3600, 0.3570, 0.3420, 0.3363, 0.3332, 0.3363, 0.3908, 0.4582, 0.5921, 0.6798, 0.8796, 0.9533, 0.9948, 1.0000, 0.9969, 0.9979, 0.9974, 0.9761, 0.9419, 0.8663, 0.7700, 0.6300, 0.4325, 0.3600]
            # sundayDemand = [i * d_max for i in sundayProfile]
            
            demand = []
            demand.append(weekdayDemand)
            # [demand.append(weekdayDemand) for i in range(5)]
            # demand.append(saturdayDemand)
            # demand.append(sundayDemand)
            self.demand = demand[0]
        # Demanda industrial
        elif self.demandType == 4:
            # Perfil de dia de la semana
            weekdayProfile = [0.1646, 0.1620, 0.1592, 0.1596, 0.1920, 0.3734, 0.7309, 0.8570, 0.9302, 0.9547, 0.9686, 0.9420, 0.9665, 1.0000, 0.9706, 0.9683, 0.6830, 0.5655, 0.4897, 0.3967, 0.3567, 0.2858, 0.1774, 0.16140]
            weekdayDemand = [i * d_max for i in weekdayProfile]
            # # Perfil de dia sabado
            # saturdayProfile = [0.1593, 0.1582, 0.1577, 0.1591, 0.1655, 0.2925, 0.7444, 0.8204, 0.8695, 0.9037, 0.9139, 0.8387, 0.8438, 0.8952, 0.8777, 0.7965, 0.3690, 0.2789, 0.3291, 0.3001, 0.2286, 0.1667, 0.1633, 0.1547]
            # saturdayDemand = [i * d_max for i in saturdayProfile]
            # # Perfil de dia domingo
            # sundayProfile = [0.1523, 0.1527, 0.1512, 0.1540, 0.1503, 0.2380, 0.6185, 0.7029, 0.7033, 0.7386, 0.7365, 0.6837, 0.5998, 0.5958, 0.2495, 0.2257, 0.2101, 0.2107, 0.2158, 0.1562, 0.1575, 0.1588, 0.1581, 0.1556]
            # sundayDemand = [i * d_max for i in sundayProfile]
            
            demand = []
            demand.append(weekdayDemand)
            # [demand.append(weekdayDemand) for i in range(5)]
            # demand.append(saturdayDemand)
            # demand.append(sundayDemand)
            self.demand = demand[0]

    def Demand (self):
        return self.demand
       
            


