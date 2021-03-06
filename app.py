import time
import requests

from flask import Flask, render_template, send_from_directory
from flask_restful import Resource, Api
from flask import request, Response

from updates import UPD











def getData():
  resp = requests.get("https://api.wazirx.com/api/v2/tickers")
  data = resp.json()
  return data



class API(Resource):

    def get(self):
        print('Get  REQ V2')
        return "Test API V2", 200

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
api.add_resource(UPD, '/updates')

print("Starting api")
# app.run(host='0.0.0.0', port=3005, debug=False)

if __name__ == "__main__":
  app.run()
