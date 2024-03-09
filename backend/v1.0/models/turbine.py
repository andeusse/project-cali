from flask import request
from flask_restful import Resource
from simulation_models import Twin_Hydro

class Turbine(Resource):
  def post(self):
    data = request.get_json()

    name = data["name"]

    turbineType = 1 if data["turbineType"] == "Pelton" else 2
    pressure = data["inputPressure"]["value"]

    flux = data["inputFlow"]["value"]
    P_CA = data["inputActivePower"]["value"]
    PF = data["inputPowerFactor"]["value"]
    P_CD = 0 if data["inputDirectCurrentPower"] == False else 2.4
    T_bat = 30.0 # Leen base de datos
    SOC_0 = data["batteryStateOfCharge"]["value"]
    V_CD = 25.0 # Leen base de datos
    V_bulk = data["controllerChargeVoltageBulk"]["value"]
    V_float = data["controllerChargeVoltageFloat"]["value"]
    V_charge = data["controllerChargingMinimunVoltage"]["value"]
    V_sink_on = data["controllerSinkOnVoltage"]["value"]
    V_sink_off = data["controllerSinkOffVoltage"]["value"]
    sinkState = False if data["controllerInitialState"] == "Apagada" else True
    inverterState = True # Leen base de datos
    delta_t = 1.0 # Delta de tiempo de la simulación en s -> se define un valor por defecto

    n_controller = data["controllerEfficiency"]["value"]
    n_inverter = data["inverterEfficiency"]["value"]

    hydroSystem = Twin_Hydro.Hydro_twin(name)
    P_h_meas = 10 # Leen base de datos
    P_CC_meas = 10 # Leen base de datos
    V_CA = 120 # Leen base de datos

    hydroSystem.turbineType(turbineType)
    P_h = hydroSystem.PowerOutput(pressure, flux)
    hydroSystem.twinParameters(n_controller, n_inverter)
    hydroSystem.optimal_n_t(hydroSystem.n_t, P_h_meas, pressure, flux)
    hydroSystem.optimal_n_controller(n_controller, P_h, P_CD, P_CC_meas)
    results = hydroSystem.twinOutput(P_CA, inverterState, PF, P_CD, T_bat, V_CD, SOC_0, 
                                     V_bulk, V_float, V_charge, sinkState, V_sink_on, V_sink_off, delta_t,hydroSystem.V_t,V_CA)

    turbine = {}

    turbine["controllerPower"] = results[0]
    turbine["inverterInputPower"] = results[1]
    turbine["batteryPower"] = results[2]
    turbine["batteryStateOfCharge"] = results[3]
    turbine["batteryVoltage"] = results[4]
    turbine["directCurrentVoltage"] = results[5]
    turbine["sinkLoadState"] = results[6]
    turbine["sinkLoadPower"] = results[7]
    turbine["inverterApparentPower"] = results[8]
    turbine["inverterActivePower"] = results[9]
    turbine["inverterReactivePower"] = results[10]
    turbine["inverterState"] = results[11]
    turbine["turbineCurrent"] = results[12]
    turbine["controllerCurrent"] = results[13]
    turbine["batteryCurrent"] = results[14]
    turbine["inverterOutputCurrent"] = results[15]
    turbine["inverterInputCurrent"] = results[16]

    return {"model": turbine}, 200