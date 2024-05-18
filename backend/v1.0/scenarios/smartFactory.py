from flask import request
from flask_restful import Resource

class SmartFactory(Resource):
  def post(self):
    data = request.get_json()
    print(data)
    response = {}