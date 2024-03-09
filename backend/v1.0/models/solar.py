from flask import request
from flask_restful import Resource

class Solar(Resource):
  def post(self):
    data = request.get_json()
    return {"data": data}, 200