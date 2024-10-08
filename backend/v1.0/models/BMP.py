from flask import request
from flask_restful import Resource


class BMP(Resource):
  def post(self):
    data = request.get_json()

    bmp_input = {}
    bmp_output = {}

    MixRule = data["substrate1CompositionSideA"]["variableString"]

    print(MixRule)
    return {"model": bmp_output}, 200