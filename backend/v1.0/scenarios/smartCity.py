from flask import request
from flask_restful import Resource
from simulation_models.Scenarios_models import Smartcity

class SmartCity(Resource):
  def post(self):
    data = request.get_json()
    # data = {'name': 'Nombre', 'operationMode': 'Automatic', 'steps': {'disabled': False, 'value': 24, 'tooltip': 'Número de pasos a simular', 'unit': '', 'variableString':'Número de pasos', 'min': 1, 'max': 10000}, 'stepTime': {'disabled': False, 'value': 1, 'tooltip': 'Tiempo por paso', 'unit': '', 'variableString': 'Tiempo por paso', 'min': 0.1, 'max': 100, 'step': 0.1}, 'stepUnit': 'Hour', 'solarSystemNumber': {'disabled': False, 'value': 3, 'tooltip': 'Número de sistemas solares', 'unit': '', 'variableString': 'Sistemas solares', 'min': 0, 'max': 100}, 'biogasSystemNumber': {'disabled': False, 'value': 2, 'tooltip': 'Número de sistemas de biogás', 'unit': '', 'variableString': 'Sistemas de biogás', 'min': 0, 'max': 100}, 'loadSystemNumber': {'disabled': False, 'value': 2, 'tooltip': 'Número de cargas', 'unit': '', 'variableString': 'Número de cargas', 'min': 1, 'max': 100}, 'houseArea': {'disabled': False, 'value': 100, 'tooltip': 'Área de la casa', 'unit': 'm²', 'variableString': 'Área de la casa', 'min': 1, 'max': 1000}, 'batterySystemNumber': {'disabled': False, 'value': 3, 'tooltip': 'Número de sistemas de baterías', 'unit': '', 'variableString': 'Sistemas de baterías', 'min': 0, 'max': 100}, 'hydraulicSystemNumber': {'disabled': False, 'value': 0, 'tooltip': 'Número de sistemas hidráulicos', 'unit': '', 'variableString': 'Sistemas hidráulicos', 'min': 0, 'max': 100}, 'windSystemNumber': {'disabled': False, 'value': 3, 'tooltip': 'Número de sistemas de eólicos', 'unit': '', 'variableString': 'Sistemas eólicos', 'min': 0, 'max': 100}, 'solarSystems': [{'id': 'e2d5321b-71d5-4d07-bcaa-b005fdece7b5', 'name': 'PV_1', 'modulesNumber': {'disabled': False, 'value': 100, 'tooltip': 'Número de módulos solares', 'unit': '', 'variableString': 'Módulos solares', 'min': 1, 'max': 100000}, 'modulePower': {'disabled': False, 'value': 500, 'tooltip': 'Potencia pico de cada módulo', 'unit': 'W', 'variableString': 'Potencia pico', 'min': 1, 'max': 1000}, 'informationMode': 'Typical', 'type': 'PolicrystallinePanel', 'deratingFactor': {'disabled': False, 'value': 1, 'tooltip': 'Factor de reducción de la potencia', 'unit': '', 'variableString': 'f', 'variableSubString': 'pu', 'min': 0.7, 'max': 1, 'step': 0.01}, 'efficiency': {'disabled': True, 'value': 15.44, 'tooltip': 'Eficiencia del panel', 'unit': '%', 'variableString': 'η', 'variableSubString': 'C'}, 'nominalIrradiance': {'disabled': True, 'value': 800, 'tooltip': 'Irradiancia a condiciones nominales de operación', 'unit': 'W / m²', 'variableString': 'G', 'variableSubString': 'NOCT'}, 'testIrradiance': {'disabled': True, 'value': 1000, 'tooltip': 'Irradiancia a condiciones estándar de prueba', 'unit': 'W / m²', 'variableString': 'G', 'variableSubString': 'STC'}, 'nominalTemperature': {'disabled': True, 'value': 45, 'tooltip': 'Temperatura del módulo en condiciones nominales de operación', 'unit': '°C', 'variableString': 'Tc', 'variableSubString': 'NOCT'}, 'testTemperature': {'disabled': True, 'value': 25, 'tooltip': 'Temperatura del módulo en condiciones estándar de prueba', 'unit': '°C', 'variableString': 'Tc', 'variableSubString': 'STC'}, 'operatingTemperature': {'disabled': True, 'value': 20, 'tooltip': 'Temperatura ambiente normal de operación', 'unit': '°C', 'variableString': 'Ta', 'variableSubString': 'NOCT'}, 'temperatureVariationCoefficient': {'disabled': True, 'value': -0.39, 'tooltip': 'Coeficiente de variación de la potencia con la temperatura', 'unit': '% / °C', 'variableString': 'μ', 'variableSubString': 'pm'}, 'radiation': {'disabled': False, 'value': 1000, 'tooltip': 'Irradiancia solar máxima', 'unit': 'W / m²', 'variableString': 'Irradiancia solar máxima', 'min': 0, 'max': 2000, 'step': 100}, 'temperature': {'disabled': False, 'value': 30, 'tooltip': 'Temperatura ambiente máxima', 'unit': '°C', 'variableString': 'Temperatura ambiente máxima', 'min': 0, 'max': 50}, 'radiationArray': [800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800], 'temperatureArray': [23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23]}, {'id': 'aa102da3-dcbd-4154-802a-3e8e610e95a7', 'name': 'PV_2', 'modulesNumber': {'disabled': False, 'value': 100, 'tooltip': 'Número de módulos solares', 'unit': '', 'variableString': 'Módulos solares', 'min': 1, 'max': 100000}, 'modulePower': {'disabled': False, 'value': 500, 'tooltip': 'Potencia pico de cada módulo', 'unit': 'W', 'variableString': 'Potencia pico', 'min': 1, 'max': 1000}, 'informationMode': 'Custom', 'type': 'PolicrystallinePanel', 'deratingFactor': {'disabled': False, 'value': 1, 'tooltip': 'Factor de reducción de la potencia', 'unit': '', 'variableString': 'f', 'variableSubString': 'pu', 'min': 0.7, 'max': 1, 'step': 0.01}, 'efficiency': {'disabled': True, 'value': 15.44, 'tooltip': 'Eficiencia del panel', 'unit': '%', 'variableString': 'η', 'variableSubString': 'C'}, 'nominalIrradiance': {'disabled': True, 'value': 800, 'tooltip': 'Irradiancia a condiciones nominales de operación', 'unit': 'W / m²', 'variableString': 'G', 'variableSubString': 'NOCT'}, 'testIrradiance': {'disabled': True, 'value': 1000, 'tooltip': 'Irradiancia a condiciones estándar de prueba', 'unit': 'W / m²', 'variableString': 'G', 'variableSubString': 'STC'}, 'nominalTemperature': {'disabled': True, 'value': 45, 'tooltip': 'Temperatura del módulo en condiciones nominales de operación', 'unit': '°C', 'variableString': 'Tc', 'variableSubString': 'NOCT'}, 'testTemperature': {'disabled': True, 'value': 25, 'tooltip': 'Temperatura del módulo en condiciones estándar de prueba', 'unit': '°C', 'variableString': 'Tc', 'variableSubString': 'STC'}, 'operatingTemperature': {'disabled': True, 'value': 20, 'tooltip': 'Temperatura ambiente normal de operación', 'unit': '°C', 'variableString': 'Ta', 'variableSubString': 'NOCT'}, 'temperatureVariationCoefficient': {'disabled': True, 'value': -0.39, 'tooltip': 'Coeficiente de variación de la potencia con la temperatura', 'unit': '% / °C', 'variableString': 'μ', 'variableSubString': 'pm'}, 'radiation': {'disabled': False, 'value': 1000, 'tooltip': 'Irradiancia solar máxima', 'unit': 'W / m²', 'variableString': 'Irradiancia solar máxima', 'min': 0, 'max': 2000, 'step': 100}, 'temperature': {'disabled': False, 'value': 25, 'tooltip': 'Temperatura ambiente máxima', 'unit': '°C', 'variableString': 'Temperatura ambiente máxima', 'min': 0, 'max': 50}, 'radiationArray': [886.9007401, 748.6836652, 678.4357334, 668.5010533, 749.3861498, 914.3795929, 807.0359946, 787.4412652, 935.0991283, 651.1321925, 783.473348, 584.3206664, 693.6099034, 583.424133, 961.1913315, 844.4784487, 735.2265455, 895.2347874, 652.7471749, 863.3193837, 908.9522809, 617.7576233, 585.239792, 682.6457625], 'temperatureArray': [26.6406184, 29.14161794, 22.66407588, 21.83412425, 24.99566144, 26.77217479, 26.24275654, 22.72024844, 26.20245338, 20.76579914, 27.62838187, 23.64181032, 27.62841812, 26.63286304, 22.3354729, 27.7721105, 23.90694185, 23.18890039, 23.7477095, 28.76460827, 27.78844832, 24.14481082, 29.29604729, 25.96269799]}, {'id': '6f4b8974-9884-44a0-a1d4-6c80b2dd9163', 'name': 'PV_3', 'modulesNumber': {'disabled': False, 'value': 100, 'tooltip': 'Número de módulos solares', 'unit': '', 'variableString': 'Módulos solares', 'min': 1, 'max': 100000}, 'modulePower': {'disabled': False, 'value': 500, 'tooltip': 'Potencia pico de cada módulo', 'unit': 'W', 'variableString': 'Potencia pico', 'min': 1, 'max': 1000}, 'informationMode': 'Custom', 'type': 'Custom', 'deratingFactor': {'disabled': False, 'value': 1, 'tooltip': 'Factor de reducción de la potencia', 'unit': '', 'variableString': 'f', 'variableSubString': 'pu', 'min': 0, 'max': 1, 'step': 0.01}, 'efficiency': {'disabled': False, 'value': 15.44, 'tooltip': 'Eficiencia del panel', 'unit': '%', 'variableString': 'η', 'variableSubString': 'C', 'min': 0, 'max': 100}, 'nominalIrradiance': {'disabled': False, 'value': 800, 'tooltip': 'Irradiancia a condiciones nominales de operación', 'unit': 'W / m²', 'variableString': 'G', 'variableSubString': 'NOCT', 'min': 0, 'max': 1500, 'step': 100}, 'testIrradiance': {'disabled': False, 'value': 1000, 'tooltip': 'Irradiancia a condiciones estándar de prueba', 'unit': 'W / m²', 'variableString': 'G', 'variableSubString': 'STC', 'min': 0, 'max': 1500, 'step': 100}, 'nominalTemperature': {'disabled': False, 'value': 45, 'tooltip': 'Temperatura del módulo en condiciones nominales de operación', 'unit': '°C', 'variableString': 'Tc', 'variableSubString': 'NOCT', 'min': 0, 'max': 100}, 'testTemperature': {'disabled': False, 'value': 25, 'tooltip': 'Temperatura del módulo en condiciones estándar de prueba', 'unit': '°C', 'variableString': 'Tc', 'variableSubString': 'STC', 'min': 0, 'max': 100}, 'operatingTemperature': {'disabled': False, 'value': 20, 'tooltip': 'Temperatura ambiente normal de operación', 'unit': '°C', 'variableString': 'Ta', 'variableSubString': 'NOCT', 'min': 0, 'max': 100}, 'temperatureVariationCoefficient': {'disabled': False, 'value': -0.39, 'tooltip': 'Coeficiente de variación de la potencia con la temperatura', 'unit': '% / °C', 'variableString': 'μ', 'variableSubString': 'pm', 'min': -10, 'max': 0, 'step': 0.1}, 'radiation': {'disabled': False, 'value': 1000, 'tooltip': 'Irradiancia solar máxima', 'unit': 'W / m²', 'variableString': 'Irradiancia solar máxima', 'min': 0, 'max': 2000, 'step': 100}, 'temperature': {'disabled': False, 'value': 30, 'tooltip': 'Temperatura ambiente máxima', 'unit': '°C', 'variableString': 'Temperatura ambiente máxima', 'min': 0, 'max': 50}, 'radiationArray': [820.1320022, 580.1932761, 789.0194549, 932.4342755, 986.9320042, 626.9852323, 566.8908419, 811.376324, 577.1010429, 570.8581729, 629.0126579, 579.7227169, 667.3188665, 844.9895182, 957.7196421, 593.4438346, 887.3589, 832.055698, 698.199453, 695.9034041, 700.6461705, 607.520755, 833.0485517, 523.0740524], 'temperatureArray': [21.23119987, 24.05234929, 28.98690896, 27.00130281, 28.23863603, 20.12174606, 20.70692502, 22.8759851, 20.69370076, 29.62085992, 26.06595357, 28.86377722, 23.44909741, 26.06039633, 23.24103, 23.46678537, 28.51246914, 25.5045642, 20.58404411, 27.90464144, 20.09982255, 21.38418122, 28.86044754, 23.52954477]}], 'batterySystems': [{'id': '96058b71-e502-4b09-87c1-997893384336', 'name': 'BESS_1', 'storageCapacity': {'disabled': False, 'value': 10, 'tooltip': 'Capacidad de almacenamiento', 'unit': 'kWh', 'variableString': 'Capacidad almacenamiento', 'min': 0.1, 'max': 10000, 'step': 0.1}, 'maxChargePower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia máxima de carga', 'unit': 'kW', 'variableString': 'Potencia máxima de carga', 'min': 0.1, 'max': 10000, 'step': 0.1}, 'minChargePower': {'disabled': False, 'value': 0, 'tooltip': 'Potencia mínima de carga', 'unit': 'kW', 'variableString': 'Potencia mínima de carga', 'min': 0.1, 'max': 50, 'step': 0.1}, 'maxDischargePower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia máxima de descarga', 'unit': 'kW', 'variableString': 'Potencia máxima de descarga', 'min': 0.1, 'max': 10000, 'step': 0.1}, 'minDischargePower': {'disabled': False, 'value': 0, 'tooltip': 'Potencia mínima de descarga', 'unit': 'kW', 'variableString': 'Potencia mínima de descarga', 'min': 0.1, 'max': 5, 'step': 0.1}, 'stateOfCharge': {'disabled': False, 'value': 50, 'tooltip': 'Estado de carga inicial', 'unit': '', 'variableString': 'SOC', 'min': 0, 'max': 100}, 'informationMode': 'Custom', 'type': 'Gel', 'selfDischargeCoefficient': {'disabled': True, 'value': 2.5, 'tooltip': 'Coeficiente de autodescarga', 'unit': '%/mes', 'variableString': 'Coeficiente de autodescarga'}, 'chargeEfficiency': {'disabled': True, 'value': 98, 'tooltip': 'Eficiencia de carga', 'unit': '%', 'variableString': 'Eficiencia de carga'}, 'dischargeEfficiency': {'disabled': True, 'value': 98, 'tooltip': 'Eficiencia de descarga', 'unit': '%', 'variableString': 'Eficiencia de descarga'}, 'chargePower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia de carga', 'unit': 'kW', 'variableString': 'Potencia de carga', 'min': 0, 'max': 50}, 'dischargePower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia de descarga', 'unit': 'kW', 'variableString': 'Potencia de descarga', 'min': 0.1, 'max': 5}, 'chargePowerArray': [4.326903704, 2.587252286, 3.522755473, 3.590907823, 2.477643453, 3.997178588, 1.28289995, 3.482715488, 4.463514907, 4.363996753, 2.782801468, 1.35087614, 3.312035719, 3.222018731, 3.665937455, 4.257640641, 3.478602815, 2.060375932, 3.972059803, 1.653877663, 0.900568489, 1.372909378, 0.61994532, 1.164890133], 'dischargePowerArray': [2.338060792, 4.057266999, 3.013940056, 3.426345001, 3.400976687, 1.415027507, 4.854932141, 4.067797955, 1.468250948, 1.589924758, 2.725280767, 3.325994169, 2.742256144, 3.618168541, 1.961683066, 2.964702078, 3.345833353, 0.788599488, 0.131622846, 3.797334843, 3.086002529, 2.447950505, 4.761658264, 4.63566989]}, {'id': 'b9e0d6c5-cdf0-4b82-bdb0-657527f86f3e', 'name': 'BESS_2', 'storageCapacity': {'disabled': False, 'value': 100, 'tooltip': 'Capacidad de almacenamiento', 'unit': 'kWh', 'variableString': 'Capacidad almacenamiento', 'min': 0.1, 'max': 10000, 'step': 0.1}, 'maxChargePower': {'disabled': False, 'value': 50, 'tooltip': 'Potencia máxima de carga', 'unit': 'kW', 'variableString': 'Potencia máxima de carga', 'min': 0.1, 'max': 10000, 'step': 0.1}, 'minChargePower': {'disabled': False, 'value': 0, 'tooltip': 'Potencia mínima de carga', 'unit': 'kW', 'variableString': 'Potencia mínima de carga', 'min': 0.1, 'max': 50, 'step': 0.1}, 'maxDischargePower': {'disabled': False, 'value': 50, 'tooltip': 'Potencia máxima de descarga', 'unit': 'kW', 'variableString': 'Potencia máxima de descarga', 'min': 0.1, 'max': 10000, 'step': 0.1}, 'minDischargePower': {'disabled': False, 'value': 0.1, 'tooltip': 'Potencia mínima de descarga', 'unit': 'kW', 'variableString': 'Potencia mínima de descarga', 'min': 0.1, 'max': 50, 'step': 0.1}, 'stateOfCharge': {'disabled': False, 'value': 50, 'tooltip': 'Estado de carga inicial', 'unit': '', 'variableString': 'SOC', 'min': 0, 'max': 100}, 'informationMode': 'Custom', 'type': 'Custom', 'selfDischargeCoefficient': {'disabled': False, 'value': 2.5, 'tooltip': 'Coeficiente de autodescarga', 'unit': '%/mes', 'variableString': 'Coeficiente de autodescarga', 'min': 0, 'max': 100}, 'chargeEfficiency': {'disabled': False, 'value': 98, 'tooltip': 'Eficiencia de carga', 'unit': '%', 'variableString': 'Eficiencia de carga', 'min': 0, 'max': 100}, 'dischargeEfficiency': {'disabled': False, 'value': 98, 'tooltip': 'Eficiencia de descarga', 'unit': '%', 'variableString': 'Eficiencia de descarga', 'min': 0, 'max': 100}, 'chargePower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia de carga', 'unit': 'kW', 'variableString': 'Potencia de carga', 'min': 0, 'max': 50}, 'dischargePower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia de descarga', 'unit': 'kW', 'variableString': 'Potencia de descarga', 'min': 0.1, 'max': 5}, 'chargePowerArray': [14.83317863, 30.13110482, 46.93588303, 28.39233167, 2.441556612, 36.75844798, 3.58993144, 6.882622635, 35.1348952, 49.90997418, 7.919875802, 42.13229139, 0.913584458, 34.67096892, 26.57802402, 32.31900891, 8.713706566, 0.112126999, 22.5110399, 21.50337639, 49.28073869, 43.35681051, 32.3723316, 5.912496252], 'dischargePowerArray': [13.77389867, 15.50701581, 36.82973905, 11.79381633, 18.40831355, 42.81483775, 11.37970472, 45.21331326, 7.613892687, 8.066801891, 45.81565961, 23.73849037, 27.97419091, 9.961755459, 41.43386489, 21.04172163, 8.179091506, 2.67327138, 25.90549111, 5.082957839, 29.47353462, 29.21604014, 20.78430743, 45.49325462]}, {'id': 'cabdb898-8e2a-49f0-804e-80fcc259290b', 'name': 'BESS_3', 'storageCapacity': {'disabled': False, 'value': 100, 'tooltip': 'Capacidad de almacenamiento', 'unit': 'kWh', 'variableString': 'Capacidad almacenamiento', 'min': 0.1, 'max': 10000, 'step': 0.1}, 'maxChargePower': {'disabled': False, 'value': 50, 'tooltip': 'Potencia máxima de carga', 'unit': 'kW', 'variableString': 'Potencia máxima de carga', 'min': 0.1, 'max': 10000, 'step': 0.1}, 'minChargePower': {'disabled': False, 'value': 0, 'tooltip': 'Potencia mínima de carga', 'unit': 'kW', 'variableString': 'Potencia mínima de carga', 'min': 0.1, 'max': 50, 'step': 0.1}, 'maxDischargePower': {'disabled': False, 'value': 50, 'tooltip': 'Potencia máxima de descarga', 'unit': 'kW', 'variableString': 'Potencia máxima de descarga', 'min': 0.1, 'max': 10000, 'step': 0.1}, 'minDischargePower': {'disabled': False, 'value': 0, 'tooltip': 'Potencia mínima de descarga', 'unit': 'kW', 'variableString': 'Potencia mínima de descarga', 'min': 0.1, 'max': 5, 'step': 0.1}, 'stateOfCharge': {'disabled': False, 'value': 50, 'tooltip': 'Estado de carga inicial', 'unit': '', 'variableString': 'SOC', 'min': 0, 'max': 100}, 'informationMode': 'Custom', 'type': 'Custom', 'selfDischargeCoefficient': {'disabled': False, 'value': 3, 'tooltip': 'Coeficiente de autodescarga', 'unit': '%/mes', 'variableString': 'Coeficiente de autodescarga', 'min': 0, 'max': 100}, 'chargeEfficiency': {'disabled': False, 'value': 90, 'tooltip': 'Eficiencia de carga', 'unit': '%', 'variableString': 'Eficiencia de carga', 'min': 0, 'max': 100}, 'dischargeEfficiency': {'disabled': False, 'value': 90, 'tooltip': 'Eficiencia de descarga', 'unit': '%', 'variableString': 'Eficiencia de descarga', 'min': 0, 'max': 100}, 'chargePower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia de carga', 'unit': 'kW', 'variableString': 'Potencia de carga', 'min': 0, 'max': 50}, 'dischargePower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia de descarga', 'unit': 'kW', 'variableString': 'Potencia de descarga', 'min': 0.1, 'max': 5}, 'chargePowerArray': [23.67640327, 25.86637722, 18.25382746, 47.68162347, 3.127187645, 35.43416828, 30.35829083, 28.84999885, 43.89867607, 44.84741522, 38.24387829, 1.528583455, 45.97239036, 46.84762987, 3.226349216, 3.263873508, 36.62058944, 42.45468058, 48.70958999, 41.53144616, 20.34318065, 21.32157403, 33.61944456, 35.92528559], 'dischargePowerArray': [38.62828585, 16.023651, 26.63146233, 2.905372418, 14.50850992, 40.75121285, 41.97436981, 4.042485276, 2.295928974, 9.082267837, 27.58596116, 30.431743, 42.65657013, 5.309229791, 45.15748359, 6.410732151, 21.63572854, 25.40028814, 4.134043539, 11.58742358, 23.42571645, 22.49778302, 0.385886917, 20.95851639]}], 'hydraulicSystems': [], 'biogasSystems': [{'id': 'f3a93829-c390-49a0-b03f-37c9ca292134', 'name': 'Biogas_1', 'stabilizationDays': {'disabled': False, 'value': 90, 'tooltip': 'Días de estabilización', 'unit': 'días', 'variableString': 'Días de estabilización', 'min': 1, 'max': 365}, 'ambientPressure': {'disabled': False, 'value': 100, 'tooltip': 'Presión ambiente', 'unit': 'kPa', 'variableString': 'Presión ambiente', 'min': 1, 'max': 200}, 'ambientTemperature': {'disabled': False, 'value': 15, 'tooltip': 'Temperatura ambiente', 'unit': '°C', 'variableString': 'Temperatura ambiente', 'min': 5, 'max': 40}, 'electricGeneratorPower': {'disabled': False, 'value': 100, 'tooltip': 'Potencia de generador eléctrico', 'unit': 'kW', 'variableString': 'Potencia de generador eléctrico', 'min': 0.1, 'max': 100000, 'step': 0.1}, 'electricGeneratorEfficiency': {'disabled': False, 'value': 30, 'tooltip': 'Eficiencia de generador eléctrico', 'unit': '%', 'variableString': 'Eficiencia de generador eléctrico', 'min': 1, 'max': 100}, 'type': 'Custom', 'phaseNumber': 'Phase2', 'reactorVolume1': {'disabled': False, 'value': 300, 'tooltip': 'Volumen de reactor 1', 'unit': 'L', 'variableString': 'Volumen de reactor 1', 'min': 30, 'max': 3000, 'step': 10}, 'reactorVolume2': {'disabled': False, 'value': 700, 'tooltip': 'Volumen de reactor 2', 'unit': 'L', 'variableString': 'Volumen de reactor 2', 'min': 30, 'max': 3000, 'step': 10}, 'diameterHeightRatio1': {'disabled': False, 'value': 2, 'tooltip': 'Relación diámetro-altura 1', 'unit': '', 'variableString': 'Relación diámetro-altura 1', 'min': 1.5, 'max': 2.5, 'step': 0.1}, 'diameterHeightRatio2': {'disabled': False, 'value': 2, 'tooltip': 'Relación diámetro-altura 2', 'unit': '', 'variableString': 'Relación diámetro-altura 2', 'min': 1.5, 'max': 2.5, 'step': 0.1}, 'heatTransferCoefficient1': {'disabled': False, 'value': 0.05, 'tooltip': 'Coeficiente transferencia de calor 1', 'unit': 'W / m² * K', 'variableString': 'Coeficiente transferencia de calor 1', 'min': 0.01, 'max': 1, 'step': 0.01}, 'heatTransferCoefficient2': {'disabled': False, 'value': 0.05, 'tooltip': 'Coeficiente transferencia de calor 2', 'unit': 'W / m² * K', 'variableString': 'Coeficiente transferencia de calor 2', 'min': 0.01, 'max': 1, 'step': 0.01}, 'temperatureSetpoint1': {'disabled': False, 'value': 35, 'tooltip': 'Setpoint temperatura 1', 'unit': '°C', 'variableString': 'Setpoint temperatura 1', 'min': 15, 'max': 55}, 'temperatureSetpoint2': {'disabled': False, 'value': 35, 'tooltip': 'Setpoint temperatura 2', 'unit': '°C', 'variableString': 'Setpoint temperatura 2', 'min': 15, 'max': 55}, 'controllerTolerance1': {'disabled': False, 'value': 3, 'tooltip': 'Tolerancia controlador 1', 'unit': '°C', 'variableString': 'Tolerancia controlador 1', 'min': 2, 'max': 5, 'step': 0.1}, 'controllerTolerance2': {'disabled': False, 'value': 3, 'tooltip': 'Tolerancia controlador 2', 'unit': '°C', 'variableString': 'Tolerancia controlador 2', 'min': 2, 'max': 5, 'step': 0.1}, 'carbonConcentration': {'disabled': False, 'value': 40, 'tooltip': 'Concentración Carbono en base seca', 'unit': '%', 'variableString': 'Concentración Carbono', 'min': 0.1, 'max': 100, 'step': 0.1}, 'hydrogenConcentration': {'disabled': False, 'value': 5, 'tooltip': 'Concentración Hidrógeno en base seca', 'unit': '%', 'variableString': 'Concentración Hidrógeno', 'min': 0.1, 'max': 100, 'step': 0.1}, 'oxygenConcentration': {'disabled': False, 'value': 20, 'tooltip': 'Concentración Oxígeno en base seca', 'unit': '%', 'variableString': 'Concentración Oxígeno', 'min': 0.1, 'max': 100, 'step': 0.1}, 'sulfurConcentration': {'disabled': False, 'value': 1, 'tooltip': 'Concentración Azufre en base seca', 'unit': '%', 'variableString': 'Concentración Azufre', 'min': 0.1, 'max': 100, 'step': 0.1}, 'totalConcentration': {'disabled': False, 'value': 10, 'tooltip': 'Concentración solidos totales', 'unit': '%', 'variableString': 'Concentración solidos totales', 'min': 0.1, 'max': 100, 'step': 0.1}, 'substrateDensity': {'disabled': False, 'value': 998, 'tooltip': 'Densidad sustrato', 'unit': 'g / L', 'variableString': 'Densidad sustrato', 'min': 100, 'max': 2000, 'step': 10}, 'substrateTemperature': {'disabled': False, 'value': 20, 'tooltip': 'Temperatura entrada sustrato', 'unit': '°C', 'variableString': 'Temperatura entrada sustrato', 'min': 10, 'max': 40}, 'substratePressure': {'disabled': False, 'value': 350, 'tooltip': 'Presión entrada sustrato', 'unit': 'kPa', 'variableString': 'Presión entrada sustrato', 'min': 100, 'max': 1000, 'step': 10}, 'substrateFlow': {'disabled': False, 'value': 0.139, 'tooltip': 'Flujo entrada sustrato', 'unit': 'L / h', 'variableString': 'Flujo entrada sustrato', 'min': 0, 'max': 1000}, 'substratePresurreDrop': {'disabled': False, 'value': 5, 'tooltip': 'Caída de presión sustrato', 'unit': 'kPa', 'variableString': 'Caída de presión sustrato', 'min': 0, 'max': 100}}, {'id': 'dcb162bb-6363-4d4a-bb60-2582c89eeb43', 'name': 'Biogas_2', 'stabilizationDays': {'disabled': False, 'value': 90, 'tooltip': 'Días de estabilización', 'unit': 'días', 'variableString': 'Días de estabilización', 'min': 1, 'max': 365}, 'ambientPressure': {'disabled': False, 'value': 100, 'tooltip': 'Presión ambiente', 'unit': 'kPa', 'variableString': 'Presión ambiente', 'min': 1, 'max': 200}, 'ambientTemperature': {'disabled': False, 'value': 15, 'tooltip': 'Temperatura ambiente', 'unit': '°C', 'variableString': 'Temperatura ambiente', 'min': 5, 'max': 40}, 'electricGeneratorPower': {'disabled': False, 'value': 100, 'tooltip': 'Potencia de generador eléctrico', 'unit': 'kW', 'variableString': 'Potencia de generador eléctrico', 'min': 0.1, 'max': 100000, 'step': 0.1}, 'electricGeneratorEfficiency': {'disabled': False, 'value': 30, 'tooltip': 'Eficiencia de generador eléctrico', 'unit': '%', 'variableString': 'Eficiencia de generador eléctrico', 'min': 1, 'max': 100}, 'type': 'Custom', 'phaseNumber': 'Phase2', 'reactorVolume1': {'disabled': False, 'value': 300, 'tooltip': 'Volumen de reactor 1', 'unit': 'L', 'variableString': 'Volumen de reactor 1', 'min': 30, 'max': 3000, 'step': 10}, 'reactorVolume2': {'disabled': False, 'value': 700, 'tooltip': 'Volumen de reactor 2', 'unit': 'L', 'variableString': 'Volumen de reactor 2', 'min': 30, 'max': 3000, 'step': 10}, 'diameterHeightRatio1': {'disabled': False, 'value': 2, 'tooltip': 'Relación diámetro-altura 1', 'unit': '', 'variableString': 'Relación diámetro-altura 1', 'min': 1.5, 'max': 2.5, 'step': 0.1}, 'diameterHeightRatio2': {'disabled': False, 'value': 2, 'tooltip': 'Relación diámetro-altura 2', 'unit': '', 'variableString': 'Relación diámetro-altura 2', 'min': 1.5, 'max': 2.5, 'step': 0.1}, 'heatTransferCoefficient1': {'disabled': False, 'value': 0.05, 'tooltip': 'Coeficiente transferencia de calor 1', 'unit': 'W / m² * K', 'variableString': 'Coeficiente transferencia de calor 1', 'min': 0.01, 'max': 1, 'step': 0.01}, 'heatTransferCoefficient2': {'disabled': False, 'value': 0.05, 'tooltip': 'Coeficiente transferencia de calor 2', 'unit': 'W / m² * K', 'variableString': 'Coeficiente transferencia de calor 2', 'min': 0.01, 'max': 1, 'step': 0.01}, 'temperatureSetpoint1': {'disabled': False, 'value': 35, 'tooltip': 'Setpoint temperatura 1', 'unit': '°C', 'variableString': 'Setpoint temperatura 1', 'min': 15, 'max': 55}, 'temperatureSetpoint2': {'disabled': False, 'value': 35, 'tooltip': 'Setpoint temperatura 2', 'unit': '°C', 'variableString': 'Setpoint temperatura 2', 'min': 15, 'max': 55}, 'controllerTolerance1': {'disabled': False, 'value': 3, 'tooltip': 'Tolerancia controlador 1', 'unit': '°C', 'variableString': 'Tolerancia controlador 1', 'min': 2, 'max': 5, 'step': 0.1}, 'controllerTolerance2': {'disabled': False, 'value': 3, 'tooltip': 'Tolerancia controlador 2', 'unit': '°C', 'variableString': 'Tolerancia controlador 2', 'min': 2, 'max': 5, 'step': 0.1}, 'carbonConcentration': {'disabled': False, 'value': 40, 'tooltip': 'Concentración Carbono en base seca', 'unit': '%', 'variableString': 'Concentración Carbono', 'min': 0.1, 'max': 100, 'step': 0.1}, 'hydrogenConcentration': {'disabled': False, 'value': 5, 'tooltip': 'Concentración Hidrógeno en base seca', 'unit': '%', 'variableString': 'Concentración Hidrógeno', 'min': 0.1, 'max': 100, 'step': 0.1}, 'oxygenConcentration': {'disabled': False, 'value': 20, 'tooltip': 'Concentración Oxígeno en base seca', 'unit': '%', 'variableString': 'Concentración Oxígeno', 'min': 0.1, 'max': 100, 'step': 0.1}, 'sulfurConcentration': {'disabled': False, 'value': 1, 'tooltip': 'Concentración Azufre en base seca', 'unit': '%', 'variableString': 'Concentración Azufre', 'min': 0.1, 'max': 100, 'step': 0.1}, 'totalConcentration': {'disabled': False, 'value': 10, 'tooltip': 'Concentración solidos totales', 'unit': '%', 'variableString': 'Concentración solidos totales', 'min': 0.1, 'max': 100, 'step': 0.1}, 'substrateDensity': {'disabled': False, 'value': 998, 'tooltip': 'Densidad sustrato', 'unit': 'g / L', 'variableString': 'Densidad sustrato', 'min': 100, 'max': 2000, 'step': 10}, 'substrateTemperature': {'disabled': False, 'value': 20, 'tooltip': 'Temperatura entrada sustrato', 'unit': '°C', 'variableString': 'Temperatura entrada sustrato', 'min': 10, 'max': 40}, 'substratePressure': {'disabled': False, 'value': 350, 'tooltip': 'Presión entrada sustrato', 'unit': 'kPa', 'variableString': 'Presión entrada sustrato', 'min': 100, 'max': 1000, 'step': 10}, 'substrateFlow': {'disabled': False, 'value': 0.139, 'tooltip': 'Flujo entrada sustrato', 'unit': 'L / h', 'variableString': 'Flujo entrada sustrato', 'min': 0, 'max': 1000}, 'substratePresurreDrop': {'disabled': False, 'value': 5, 'tooltip': 'Caída de presión sustrato', 'unit': 'kPa', 'variableString': 'Caída de presión sustrato', 'min': 0, 'max': 100}}], 'loadSystems': [{'id': '8a06655a-c1cd-4659-a0b5-fef72a0737b7', 'name': 'Load 1', 'informationMode': 'Custom', 'power': {'disabled': False, 'value': 100, 'tooltip': 'Potencia de demanda', 'unit': 'kW', 'variableString': 'Potencia de demanda', 'min': 0.1, 'max': 1000000, 'step': 0.1}, 'peakPower': {'disabled': False, 'value': 100, 'tooltip': 'Potencia de demanda pico', 'unit': 'kW', 'variableString': 'Potencia de demanda pico', 'min': 0.1, 'max': 1000000, 'step': 0.1}, 'powerArray': [82.29397787, 124.6062351, 109.1707492, 126.8017999, 119.7800052, 91.45332241, 111.50248, 105.0139192, 129.1052996, 131.1300667, 118.355387, 116.1358893, 121.2376873, 87.48296859, 106.7785582, 137.9724845, 92.45618363, 127.5873888, 144.7801862, 134.3187353, 145.6666495, 130.2579674, 105.2199595, 144.9882754]}, {'id': '155d4919-b961-41ec-8936-2fdcbdd7d9d4', 'name': 'Load 2', 'informationMode': 'Custom', 'power': {'disabled': False, 'value': 100, 'tooltip': 'Potencia de demanda', 'unit': 'kW', 'variableString': 'Potencia de demanda', 'min': 0.1, 'max': 1000000, 'step': 0.1}, 'peakPower': {'disabled': False, 'value': 100, 'tooltip': 'Potencia de demanda pico', 'unit': 'kW', 'variableString': 'Potencia de demanda pico', 'min': 0.1, 'max': 1000000, 'step': 0.1}, 'powerArray': [82.29397787, 124.6062351, 109.1707492, 126.8017999, 119.7800052, 91.45332241, 111.50248, 105.0139192, 129.1052996, 131.1300667, 118.355387, 116.1358893, 121.2376873, 87.48296859, 106.7785582, 137.9724845, 92.45618363, 127.5873888, 144.7801862, 134.3187353, 145.6666495, 130.2579674, 105.2199595, 144.9882754]}], 'windSystems': [{'id': '220f9962-f5c7-413c-905e-2bc536f2c17a', 'name': 'Wind_1', 'turbineNumber': {'disabled': False, 'value': 10, 'tooltip': 'Número de turbinas', 'unit': '', 'variableString': 'Número de turbinas', 'min': 1, 'max': 100}, 'nominalPower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia nominal de cada turbina', 'unit': 'kW', 'variableString': 'Potencia nominal', 'min': 0.1, 'max': 100000, 'step': 0.1}, 'airDensity': {'disabled': False, 'value': 1.112, 'tooltip': 'Densidad del aire', 'unit': 'kg / m³', 'variableString': 'Densidad del aire', 'min': 0.1, 'max': 10, 'step': 0.1}, 'type': 'Laboratory', 'informationMode': 'Custom', 'peakPower': {'disabled': True, 'value': 200, 'tooltip': 'Potencia pico del aerogenerador', 'unit': 'W', 'variableString': 'Potencia pico'}, 'rotorHeight': {'disabled': False, 'value': 1.5, 'tooltip': 'Altura del rotor del aerogenerador', 'unit': 'm', 'variableString': 'H', 'variableSubString': 'r', 'min': 0, 'max': 10, 'step': 0.1}, 'anemometerHeight': {'disabled': False, 'value': 1.5, 'tooltip': 'Altura del anemómetro', 'unit': 'm', 'variableString': 'H', 'variableSubString': 'a', 'min': 0, 'max': 10, 'step': 0.1}, 'ratedWindSpeed': {'disabled': True, 'value': 11.5, 'tooltip': 'Velocidad de viento nominal', 'unit': 'm / s', 'variableString': 'V', 'variableSubString': 'n'}, 'lowerCutoffWindSpeed': {'disabled': True, 'value': 2, 'tooltip': 'Velocidad de viento de corte inferior', 'unit': 'm / s', 'variableString': 'V', 'variableSubString': 'c'}, 'upperCutoffWindSpeed': {'disabled': True, 'value': 65, 'tooltip': 'Velocidad de viento de corte superior', 'unit': 'm / s', 'variableString': 'V', 'variableSubString': 'f'}, 'surfaceRoughnessLength': {'disabled': True, 'value': 2, 'tooltip': 'Longitud de rugosidad superficial', 'unit': 'm', 'variableString': 'Longitud de rugosidad superficial'}, 'windSpeed': {'disabled': False, 'value': 11.5, 'tooltip': 'Velocidad del viento máxima', 'unit': 'm / s', 'variableString': 'Velocidad del viento máxima', 'min': 2.5, 'max': 45}, 'windSpeedArray': [9.730236528, 10.70330295, 9.057665303, 11.5145074, 11.007425, 5.627997735, 7.779331296, 9.514958506, 10.22944375, 8.323321245, 9.656021912, 6.860429887, 7.266942851, 5.806956834, 10.47199963, 6.033968909, 7.256978239, 5.050459551, 7.98541463, 8.407245026, 9.677723033, 11.40983382, 9.564924275, 11.49436422]}, {'id': 'f6523504-a3e6-4960-976a-e1a1cb6490c3', 'name': 'Wind_2', 'turbineNumber': {'disabled': False, 'value': 10, 'tooltip': 'Número de turbinas', 'unit': '', 'variableString': 'Número de turbinas', 'min': 1, 'max': 100}, 'nominalPower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia nominal de cada turbina', 'unit': 'kW', 'variableString': 'Potencia nominal', 'min': 0.1, 'max': 100000, 'step': 0.1}, 'airDensity': {'disabled': False, 'value': 1.112, 'tooltip': 'Densidad del aire', 'unit': 'kg / m³', 'variableString': 'Densidad del aire', 'min': 0.1, 'max': 10, 'step': 0.1}, 'type': 'Custom', 'informationMode': 'Custom', 'peakPower': {'disabled': True, 'value': 200, 'tooltip': 'Potencia pico del aerogenerador', 'unit': 'W', 'variableString': 'Potencia pico'}, 'rotorHeight': {'disabled': False, 'value': 1, 'tooltip': 'Altura del rotor del aerogenerador', 'unit': 'm', 'variableString': 'H', 'variableSubString': 'r', 'min': 1, 'max': 300}, 'anemometerHeight': {'disabled': False, 'value': 1, 'tooltip': 'Altura del anemómetro', 'unit': 'm', 'variableString': 'H', 'variableSubString': 'a', 'min': 1, 'max': 300}, 'ratedWindSpeed': {'disabled': False, 'value': 11.5, 'tooltip': 'Velocidad de viento nominal', 'unit': 'm / s', 'variableString': 'V', 'variableSubString': 'n', 'min': 1, 'max': 100}, 'lowerCutoffWindSpeed': {'disabled': False, 'value': 2.5, 'tooltip': 'Velocidad de viento de corte inferior', 'unit': 'm / s', 'variableString': 'V', 'variableSubString': 'c', 'min': 1, 'max': 100}, 'upperCutoffWindSpeed': {'disabled': False, 'value': 45, 'tooltip': 'Velocidad de viento de corte superior', 'unit': 'm / s', 'variableString': 'V', 'variableSubString': 'f', 'min': 10, 'max': 200}, 'surfaceRoughnessLength': {'disabled': False, 'value': 0.03, 'tooltip': 'Longitud de rugosidad superficial', 'unit': 'm', 'variableString': 'Longitud de rugosidad superficial', 'min': 0.0001, 'max': 10}, 'windSpeed': {'disabled': False, 'value': 11.5, 'tooltip': 'Velocidad del viento máxima', 'unit': 'm / s', 'variableString': 'Velocidad del viento máxima', 'min': 2.5, 'max': 45}, 'windSpeedArray': [9.730236528, 10.70330295, 9.057665303, 11.5145074, 11.007425, 5.627997735, 7.779331296, 9.514958506, 10.22944375, 8.323321245, 9.656021912, 6.860429887, 7.266942851, 5.806956834, 10.47199963, 6.033968909, 7.256978239, 5.050459551, 7.98541463, 8.407245026, 9.677723033, 11.40983382, 9.564924275, 11.49436422]}, {'id': '22dacb84-c078-4741-817c-9447d43e294b', 'name': 'Wind_3', 'turbineNumber': {'disabled': False, 'value': 10, 'tooltip': 'Número de turbinas', 'unit': '', 'variableString': 'Número de turbinas', 'min': 1, 'max': 100}, 'nominalPower': {'disabled': False, 'value': 5, 'tooltip': 'Potencia nominal de cada turbina', 'unit': 'kW', 'variableString': 'Potencia nominal', 'min': 0.1, 'max': 100000, 'step': 0.1}, 'airDensity': {'disabled': False, 'value': 1.112, 'tooltip': 'Densidad del aire', 'unit': 'kg / m³', 'variableString': 'Densidad del aire', 'min': 0.1, 'max': 10, 'step': 0.1}, 'type': 'Custom', 'informationMode': 'Custom', 'peakPower': {'disabled': True, 'value': 200, 'tooltip': 'Potencia pico del aerogenerador', 'unit': 'W', 'variableString': 'Potencia pico'}, 'rotorHeight': {'disabled': False, 'value': 3, 'tooltip': 'Altura del rotor del aerogenerador', 'unit': 'm', 'variableString': 'H', 'variableSubString': 'r', 'min': 1, 'max': 300}, 'anemometerHeight': {'disabled': False, 'value': 1, 'tooltip': 'Altura del anemómetro', 'unit': 'm', 'variableString': 'H', 'variableSubString': 'a', 'min': 1, 'max': 300}, 'ratedWindSpeed': {'disabled': False, 'value': 10, 'tooltip': 'Velocidad de viento nominal', 'unit': 'm / s', 'variableString': 'V', 'variableSubString': 'n', 'min': 1, 'max': 100}, 'lowerCutoffWindSpeed': {'disabled': False, 'value': 2, 'tooltip': 'Velocidad de viento de corte inferior', 'unit': 'm / s', 'variableString': 'V', 'variableSubString': 'c', 'min': 1, 'max': 100}, 'upperCutoffWindSpeed': {'disabled': False, 'value': 40, 'tooltip': 'Velocidad de viento de corte superior', 'unit': 'm / s', 'variableString': 'V', 'variableSubString': 'f', 'min': 10, 'max': 200}, 'surfaceRoughnessLength': {'disabled': False, 'value': 0.01, 'tooltip': 'Longitud de rugosidad superficial', 'unit': 'm', 'variableString': 'Longitud de rugosidad superficial', 'min': 0.0001, 'max': 10}, 'windSpeed': {'disabled': False, 'value': 11.5, 'tooltip': 'Velocidad del viento máxima', 'unit': 'm / s', 'variableString': 'Velocidad del viento máxima', 'min': 2.5, 'max': 45}, 'windSpeedArray': [9.730236528, 10.70330295, 9.057665303, 11.5145074, 11.007425, 5.627997735, 7.779331296, 9.514958506, 10.22944375, 8.323321245, 9.656021912, 6.860429887, 7.266942851, 5.806956834, 10.47199963, 6.033968909, 7.256978239, 5.050459551, 7.98541463, 8.407245026, 9.677723033, 11.40983382, 9.564924275, 11.49436422]}], 'priorityList': [{'id': 'e2d5321b-71d5-4d07-bcaa-b005fdece7b5', 'name': 'PV_1'}, {'id': 'aa102da3-dcbd-4154-802a-3e8e610e95a7', 'name': 'PV_2'}, {'id': '6f4b8974-9884-44a0-a1d4-6c80b2dd9163', 'name': 'PV_3'}, {'id': '220f9962-f5c7-413c-905e-2bc536f2c17a', 'name': 'Wind_1'}, {'id': 'f6523504-a3e6-4960-976a-e1a1cb6490c3', 'name': 'Wind_2'}, {'id': '22dacb84-c078-4741-817c-9447d43e294b', 'name': 'Wind_3'}, {'id': 'f3a93829-c390-49a0-b03f-37c9ca292134', 'name': 'Biogas_1'}, {'id': 'dcb162bb-6363-4d4a-bb60-2582c89eeb43', 'name': 'Biogas_2'}]}
    # print(data)

    if data['operationMode'] == 'Manual':
      operationType = 1
    else:
      operationType = 2
    
    simulationSteps = data['steps']['value']
    
    if data['stepUnit'] == 'Second':
      stepTime = data['stepTime']['value'] / 3600
    elif data['stepUnit'] == 'Minute':
      stepTime = data['stepTime']['value'] / 60
    elif data['stepUnit'] == 'Hour':
      stepTime = data['stepTime']['value']
    elif data['stepUnit'] == 'Day':
      stepTime = data['stepTime']['value'] * 24

    solarSystemNumber = data['solarSystemNumber']['value']
    biogasSystemNumber = data['biogasSystemNumber']['value']
    batterySystemNumber = data['batterySystemNumber']['value']
    hydraulicSystemNumber = data['hydraulicSystemNumber']['value']
    windSystemNumber = data['windSystemNumber']['value']
    loadSystemNumber = data['loadSystemNumber']['value']

    smartcity_model = Smartcity.Smartcity(N_PV=solarSystemNumber, N_BESS=batterySystemNumber, N_Hydro=hydraulicSystemNumber,
                                           N_WF=windSystemNumber, N_Biogas=biogasSystemNumber, N_Demand=loadSystemNumber,
                                             operationType=operationType, simulationSteps=simulationSteps, stepTime=stepTime)

    PV_Names = []
    moduleNumbers = []
    modulePowers = []
    moduleTypes = []
    deratingFactor = []
    efficiency = []
    nominalIrradiance = []
    testIrradiance = []
    nominalTemperature = []
    testTemperature = []
    operatingTemperature = []
    temperatureVariationCoefficient = []
    informationMode = []
    radiations = []
    temperatures = []

    for solarSystem in data['solarSystems']:
      PV_Names.append(solarSystem['name'])
      moduleNumbers.append(solarSystem['modulesNumber']['value'])
      modulePowers.append(solarSystem['modulePower']['value'])
      
      if solarSystem['type'] == 'MonocrystallinePanel':
        moduleTypes.append(1)
      elif solarSystem['type'] == 'PolicrystallinePanel':
        moduleTypes.append(2)
      elif solarSystem['type'] == 'FlexPanel':
        moduleTypes.append(3)
      elif solarSystem['type'] == 'CadmiumTelluridePanel':
        moduleTypes.append(4)
      elif solarSystem['type'] == 'Custom':
        moduleTypes.append(0)
        deratingFactor.append(solarSystem['deratingFactor']['value'])
        efficiency.append(solarSystem['efficiency']['value'])
        nominalIrradiance.append(solarSystem['nominalIrradiance']['value'])
        testIrradiance.append(solarSystem['testIrradiance']['value'])
        nominalTemperature.append(solarSystem['nominalTemperature']['value'])
        testTemperature.append(solarSystem['testTemperature']['value'])
        operatingTemperature.append(solarSystem['operatingTemperature']['value'])
        temperatureVariationCoefficient.append(solarSystem['temperatureVariationCoefficient']['value'])
      
      if solarSystem['informationMode'] == 'Fixed':
        informationMode.append(1)
        radiations.append([solarSystem['radiation']['value']])
        temperatures.append([solarSystem['temperature']['value']])
      elif solarSystem['informationMode'] == 'Typical':
        informationMode.append(2)
        radiations.append([solarSystem['radiation']['value']])
        temperatures.append([solarSystem['temperature']['value']])
      elif solarSystem['informationMode'] == 'Custom':
        informationMode.append(0)
        radiations.append(solarSystem['radiationArray'])
        temperatures.append(solarSystem['temperatureArray'])

    BESS_Names = []
    batteryTypes = []
    storageCapacity = []
    maxChargePower = []
    minChargePower = []
    maxDischargePower = []
    minDischargePower = []
    stateOfCharge = []
    selfDischargeCoefficient = []
    chargeEfficiency = []
    dischargeEfficiency = []
    batteryInformationMode = []
    chargePowers = []
    dischargePowers = [] 

    for batterySystem in data['batterySystems']:
      BESS_Names.append(batterySystem['name'])
      storageCapacity.append(batterySystem['storageCapacity']['value'])
      maxChargePower.append(batterySystem['maxChargePower']['value'])
      minChargePower.append(batterySystem['minChargePower']['value'])
      maxDischargePower.append(batterySystem['maxDischargePower']['value'])
      minDischargePower.append(batterySystem['minDischargePower']['value'])
      stateOfCharge.append(batterySystem['stateOfCharge']['value'])
      if batterySystem['type'] == 'Gel':
        batteryTypes.append(1)
      elif batterySystem['type'] == 'Custom':
        batteryTypes.append(0)
        selfDischargeCoefficient.append(batterySystem['selfDischargeCoefficient']['value'])
        chargeEfficiency.append(batterySystem['chargeEfficiency']['value'])
        dischargeEfficiency.append(batterySystem['dischargeEfficiency']['value'])

      if batterySystem['informationMode'] == 'Fixed':
        batteryInformationMode.append(1)
        chargePowers.append([batterySystem['chargePower']['value']])
        dischargePowers.append([batterySystem['dischargePower']['value']])
      elif batterySystem['informationMode'] == 'Custom':
        batteryInformationMode.append(0)
        chargePowers.append(batterySystem['chargePowerArray'])
        dischargePowers.append(batterySystem['dischargePowerArray'])

    hydroNames = []
    turbineNumbers = []
    turbinePowers = []
    turbineTypes = []
    turbineEfficiency = []
    frictionLosses = []
    minimumWaterHead = []
    maximumWaterHead = []
    minimumWaterFlow = []
    maximumWaterFlow = []
    turbineInformationMode = []
    waterHeads = []
    waterFlows = []    

    for hydraulicSystem in data['hydraulicSystems']:
      hydroNames.append(hydraulicSystem['name'])
      turbineNumbers.append(hydraulicSystem['turbineNumber']['value'])
      turbinePowers.append(hydraulicSystem['nominalPower']['value'])

      if hydraulicSystem['type'] == 'Pelton':
        turbineTypes.append(1)
      if hydraulicSystem['type'] == 'Turgo':
        turbineTypes.append(2)
      elif hydraulicSystem['type'] == 'Custom':
        turbineTypes.append(0)
        turbineEfficiency.append(hydraulicSystem['efficiency']['value'])
        frictionLosses.append(hydraulicSystem['frictionLosses']['value'])
        minimumWaterHead.append(hydraulicSystem['minimumWaterHead']['value'])
        maximumWaterHead.append(hydraulicSystem['maximumWaterHead']['value'])
        minimumWaterFlow.append(hydraulicSystem['minimumWaterFlow']['value'])
        maximumWaterFlow.append(hydraulicSystem['maximumWaterFlow']['value'])
      
      if hydraulicSystem['informationMode'] == 'Fixed':
        turbineInformationMode.append(1)
        waterHeads.append([hydraulicSystem['waterHead']['value']])
        waterFlows.append([hydraulicSystem['waterFlow']['value']])
      elif hydraulicSystem['informationMode'] == 'Custom':
        turbineInformationMode.append(0)
        waterHeads.append(hydraulicSystem['waterHeadArray'])
        waterFlows.append(hydraulicSystem['waterFlowArray'])

    windNames = []
    windTurbineNumbers = []
    windTurbinePowers = []
    windTurbineTypes = []
    airDensity = []
    rotorHeight = []
    anemometerHeight = []
    ratedWindSpeed = []
    lowerCutoffWindSpeed = []
    upperCutoffWindSpeed = []
    surfaceRoughnessLength = []
    windInformationMode = []
    windSpeeds = []

    for windSystem in data['windSystems']:
      windNames.append(windSystem['name'])
      windTurbineNumbers.append(windSystem['turbineNumber']['value'])
      windTurbinePowers.append(windSystem['nominalPower']['value'])
      airDensity.append(windSystem['airDensity']['value'])
      
      if windSystem['type'] == 'Laboratory':
        windTurbineTypes.append(1)
      elif windSystem['type'] == 'Custom':
        windTurbineTypes.append(0)
        rotorHeight.append(windSystem['rotorHeight']['value'])
        anemometerHeight.append(windSystem['anemometerHeight']['value'])
        ratedWindSpeed.append(windSystem['ratedWindSpeed']['value'])
        lowerCutoffWindSpeed.append(windSystem['lowerCutoffWindSpeed']['value'])
        upperCutoffWindSpeed.append(windSystem['upperCutoffWindSpeed']['value'])
        surfaceRoughnessLength.append(windSystem['surfaceRoughnessLength']['value'])
      
      if windSystem['informationMode'] == 'Fixed':
        windInformationMode.append(1)
        windSpeeds.append([windSystem['windSpeed']['value']])
      elif windSystem['informationMode'] == 'Typical':
        windInformationMode.append(2)
        windSpeeds.append([windSystem['windSpeed']['value']])
      elif windSystem['informationMode'] == 'Custom':
        windInformationMode.append(0)
        windSpeeds.append(windSystem['windSpeedArray'])

    loadNames = []
    loadTypes = []
    loadPowers = []

    for loadSystem in data['loadSystems']:
      loadNames.append(loadSystem['name'])
      if loadSystem['informationMode'] == 'Fixed':
        loadTypes.append(1)
        loadPowers.append(loadSystem['power']['value'])
      elif loadSystem['informationMode'] == 'Residential':
        loadTypes.append(2)
        loadPowers.append(loadSystem['peakPower']['value'])
      elif loadSystem['informationMode'] == 'Commercial':
        loadTypes.append(3)
        loadPowers.append(loadSystem['peakPower']['value'])
      elif loadSystem['informationMode'] == 'Industrial':
        loadTypes.append(4)
        loadPowers.append(loadSystem['peakPower']['value'])
      elif loadSystem['informationMode'] == 'Custom':
        loadTypes.append(0)
        loadPowers.append(loadSystem['powerArray'])

    biogasNames = []
    stabilizationDays = []
    ambientPressure = []
    ambientTemperature = []
    electricGeneratorPower = []
    electricGeneratorEfficiency = []
    reactorVolume1 = []
    reactorVolume2 = []
    diameterHeightRatio1 = []
    diameterHeightRatio2 = []
    heatTransferCoefficient1 = []
    heatTransferCoefficient2 = []
    temperatureSetpoint1 = []
    temperatureSetpoint2 = []
    controllerTolerance1 = []
    controllerTolerance2 = []
    carbonConcentration = []
    hydrogenConcentration = []
    oxygenConcentration = []
    sulfurConcentration = []
    totalConcentration = []
    substrateDensity = []
    substrateTemperature = []
    substratePressure = []
    substrateFlow = []
    substratePresurreDrop = []

    for biogasSystem in data['biogasSystems']:
      biogasNames.append(biogasSystem['name'])
      stabilizationDays.append(biogasSystem['stabilizationDays']['value'])
      ambientPressure.append(biogasSystem['ambientPressure']['value'])
      ambientTemperature.append(biogasSystem['ambientTemperature']['value'])
      electricGeneratorPower.append(biogasSystem['electricGeneratorPower']['value'])
      electricGeneratorEfficiency.append(biogasSystem['electricGeneratorEfficiency']['value'])
      reactorVolume1.append(biogasSystem['reactorVolume1']['value'])
      reactorVolume2.append(biogasSystem['reactorVolume2']['value'])
      diameterHeightRatio1.append(biogasSystem['diameterHeightRatio1']['value'])
      diameterHeightRatio2.append(biogasSystem['diameterHeightRatio2']['value'])
      heatTransferCoefficient1.append(biogasSystem['heatTransferCoefficient1']['value'])
      heatTransferCoefficient2.append(biogasSystem['heatTransferCoefficient2']['value'])
      temperatureSetpoint1.append(biogasSystem['temperatureSetpoint1']['value'])
      temperatureSetpoint2.append(biogasSystem['temperatureSetpoint2']['value'])
      controllerTolerance1.append(biogasSystem['controllerTolerance1']['value'])
      controllerTolerance2.append(biogasSystem['controllerTolerance2']['value'])
      carbonConcentration.append(biogasSystem['carbonConcentration']['value']/100)
      hydrogenConcentration.append(biogasSystem['hydrogenConcentration']['value']/100)
      oxygenConcentration.append(biogasSystem['oxygenConcentration']['value']/100)
      sulfurConcentration.append(biogasSystem['sulfurConcentration']['value']/100)
      totalConcentration.append(biogasSystem['totalConcentration']['value']/100)
      substrateDensity.append(biogasSystem['substrateDensity']['value'])
      substrateTemperature.append(biogasSystem['substrateTemperature']['value'])
      substratePressure.append(biogasSystem['substratePressure']['value'])
      substrateFlow.append(biogasSystem['substrateFlow']['value'])
      substratePresurreDrop.append(biogasSystem['substratePresurreDrop']['value'])

    smartcity_model.resourcesDefinition(PV_Names = PV_Names, moduleNumbers = moduleNumbers, modulePowers = modulePowers, moduleTypes = moduleTypes, f_PV = deratingFactor, G_0 = testIrradiance, u_PM = temperatureVariationCoefficient, T_cSTC = testTemperature, T_cNOCT = nominalTemperature, T_aNOCT = operatingTemperature, G_NOCT = nominalIrradiance, n_c = efficiency, 
                            BESS_Names = BESS_Names, batteryTypes = batteryTypes, batteryEnergy = storageCapacity, chargePower_Max = maxChargePower, chargePower_Min = minChargePower, dischargePower_Max = maxDischargePower, dischargePower_Min = minDischargePower, gamma_sd = selfDischargeCoefficient, eta_bc = chargeEfficiency, eta_bd = dischargeEfficiency, 
                            hydroNames = hydroNames, turbineNumbers = turbineNumbers, turbinePowers = turbinePowers, turbineTypes = turbineTypes, n_t = turbineEfficiency, H_min = minimumWaterHead, H_max = maximumWaterHead, Q_min = minimumWaterFlow, Q_max = maximumWaterFlow, f_h = frictionLosses, 
                            WF_Names = windNames, windTurbineNumbers = windTurbineNumbers, windTurbinePowers = windTurbinePowers, windTurbineTypes = windTurbineTypes, H_R = rotorHeight, H_A = anemometerHeight, Z_0 = surfaceRoughnessLength, V_C = lowerCutoffWindSpeed, V_N = ratedWindSpeed, V_F = upperCutoffWindSpeed, 
                            biogasNames = biogasNames, timestep = 1, days = stabilizationDays, reactorVolume1 = reactorVolume1, reactorVolume2 = reactorVolume2, heightRelation1 = diameterHeightRatio1, heightRelation2 = diameterHeightRatio2, heatTransfer1 = heatTransferCoefficient1, heatTransfer2 = heatTransferCoefficient2, Tset1 = temperatureSetpoint1, tolerancia1 = controllerTolerance1, Tset2 = temperatureSetpoint2, tolerancia2 = controllerTolerance2, Cci = carbonConcentration, Chi = hydrogenConcentration, Coi = oxygenConcentration, Csi = sulfurConcentration, ST = totalConcentration, rho_sus = substrateDensity, Tin_sus = substrateTemperature, Pin_sus = substratePressure, vin_sus = substrateFlow, DeltaP = substratePresurreDrop, Patm = ambientPressure, Tamb = ambientTemperature, genEfficiency = electricGeneratorEfficiency, ratedPower = electricGeneratorPower, 
                            demandNames = loadNames, demandTypes = loadTypes, demandPowersSet = loadPowers)

    idList = []
    weightList = []
    for item in data['priorityList']:
      idList.append(item['id'])
    for system in data['solarSystems']:
      id = system['id']
      weightList.append(idList.index(id))
    for system in data['batterySystems']:
      weightList.append(0)
      weightList.append(0)
    for system in data['hydraulicSystems']:
      id = system['id']
      weightList.append(idList.index(id))
    for system in data['windSystems']:
      id = system['id']
      weightList.append(idList.index(id))
    for system in data['biogasSystems']:
      id = system['id']
      weightList.append(idList.index(id))
    weightList.append(len(data['priorityList']))

    # print(weightList)
    results_df = smartcity_model.operation(PV_MeteorologicalDataType = informationMode, temperature = temperatures, irradiance = radiations, 
                  BESS_OperativeDataType = batteryInformationMode, initialSOC = stateOfCharge, chargePower = chargePowers, dischargePower = dischargePowers, 
                  hydroOperativeDataType = turbineInformationMode, head = waterHeads, flux = waterFlows, 
                  WF_MeteorologicalDataType = windInformationMode, airDensity = airDensity, windSpeed = windSpeeds,
                  weights = weightList)

    response = results_df.to_json(orient='split')
    # print('#########################################################################')
    # print(response)

    return response