from flask import request
from flask_restful import Resource

class SmartHome(Resource):
  def post(self):
    data = request.get_json()
    print(data)
    response = {}
    return response