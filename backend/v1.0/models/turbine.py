from flask import request
from flask_restful import Resource

class Turbine(Resource):
  def post(self):
    data = request.get_json()
    print(data["controllerEfficiency"])
    return {"data": data}, 200
  
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
    },
    "required": ["name"],
}