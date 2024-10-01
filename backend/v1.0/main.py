from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS
from models import Turbine, Solar, Biogas, coolingTower, hydrogenCell
from scenarios import SmartHome, SmartCity, SmartFactory

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class ApiRunning(Resource):
  def get(self):
    return {"data": "API is running"}, 200

api.add_resource(ApiRunning, "/")

api.add_resource(Turbine, "/models/turbine")

api.add_resource(Solar, "/models/solar")

api.add_resource(Biogas, "/models/biogas")

api.add_resource(coolingTower, "/models/coolingTower")

api.add_resource(hydrogenCell, "/models/hydrogenCell")

api.add_resource(SmartCity, "/scenarios/smartcity")

api.add_resource(SmartFactory, "/scenarios/smartfactory")

api.add_resource(SmartHome, "/scenarios/smarthome")

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
