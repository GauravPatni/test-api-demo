import time
import requests

from flask import Flask, render_template, send_from_directory
from flask_restful import Resource, Api
from flask import request, Response


def getData():
  resp = requests.get("https://api.wazirx.com/api/v2/tickers")
  data = resp.json()
  return data



class API(Resource):

    def get(self):
        print('Get  REQ')
        return "Test API", 200

    def post(self):
        req = request.get_json()
        print(req)
        if req:
          if "WZ" in req:
            return getData() , 200
          return "Bad Info Request", 403
        else:
            return "Bad Request", 403





app = Flask(__name__)
api = Api(app)


api.add_resource(API, '/api')

print("Starting api")
# app.run(host='0.0.0.0', port=3005, debug=False)


