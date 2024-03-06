from flask import Flask
from flask_restful import Api, Resource, request
from flask_cors import CORS
from models import Turbine

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class ApiRunning(Resource):
  def get(self):
    return {"data": "API is running"}, 200
  
  def post(self):
    data = request.get_json()
    return data

api.add_resource(ApiRunning, "/")

api.add_resource(Turbine, "/models/turbine")

if __name__ == "__main__":
  app.run(debug=True)
