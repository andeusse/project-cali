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
    P_CD = 0.0 if data["inputDirectCurrentPower"] == False else 2.4
    T_bat = 30.0 # Leen base de datos
    SOC = data["batteryStateOfCharge"]["value"]
    print(SOC)
    V_CD = 25.0
    # V_CD = data["directCurrentVoltage"]["value"]
    print(V_CD)
    V_bulk = data["controllerChargeVoltageBulk"]["value"]
    V_float = data["controllerChargeVoltageFloat"]["value"]
    V_charge = data["controllerChargingMinimunVoltage"]["value"]
    V_sink_on = data["controllerSinkOnVoltage"]["value"]
    V_sink_off = data["controllerSinkOffVoltage"]["value"]
    sinkState = False if data["controllerInitialState"] == "Apagada" else True
    inverterState = True # Leen base de datos
    delta_t = 5.0 # Delta de tiempo de la simulación en s -> se define un valor por defecto

    n_controller = data["controllerEfficiency"]["value"]
    n_inverter = data["inverterEfficiency"]["value"]

    hydroSystem = Twin_Hydro.Hydro_twin(name)
    P_h_meas = 500 # Leen base de datos
    P_CC_meas = 450 # Leen base de datos
    V_CA = 120 # Leen base de datos

    hydroSystem.turbineType(turbineType)
    P_h = hydroSystem.PowerOutput(pressure, flux)
    hydroSystem.twinParameters(n_controller, n_inverter)
    hydroSystem.optimal_n_t(hydroSystem.n_t, P_h_meas, pressure, flux)
    P_h = hydroSystem.PowerOutput(pressure, flux)
    hydroSystem.optimal_n_controller(n_controller, P_h, P_CD, P_CC_meas)
    results = hydroSystem.twinOutput(P_CA, inverterState, PF, P_CD, T_bat, V_CD, SOC, 
                                     V_bulk, V_float, V_charge, sinkState, V_sink_on, V_sink_off, delta_t,hydroSystem.V_t,V_CA)

    turbine = {}

    turbine["turbinePower"] = P_h

    turbine["controllerPower"] = results[0]
    turbine["inverterInputPower"] = results[1]
    turbine["batteryPower"] = results[2]
    turbine["turbineVoltage"] = results[3]
    turbine["inverterOutputVoltage"] = results[4]
    turbine["batteryStateOfCharge"] = results[5]
    print(results[5])
    turbine["batteryVoltage"] = results[6]
    turbine["directCurrentVoltage"] = results[7]
    print(results[7])
    turbine["sinkLoadState"] = results[8]
    turbine["sinkLoadPower"] = results[9]
    turbine["inverterApparentPower"] = results[10]
    turbine["inverterActivePower"] = results[11]
    turbine["inverterReactivePower"] = results[12]
    turbine["inverterState"] = results[13]
    turbine["turbineCurrent"] = results[14]
    turbine["controllerCurrent"] = results[15]
    turbine["batteryCurrent"] = results[16]
    turbine["inverterOutputCurrent"] = results[17]
    turbine["inverterInputCurrent"] = results[18]

    return {"model": turbine}