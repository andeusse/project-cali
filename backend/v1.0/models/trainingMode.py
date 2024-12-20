from flask import request
from flask_restful import Resource
import os

class TrainingMode(Resource):
  def post(self):
    data = request.get_json()
    if(data["password"]==os.getenv("TrainingModePassword")):
      return {"succeed" : True}
    return {"succeed" : False}