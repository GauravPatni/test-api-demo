import time
import requests

from flask import Flask, render_template, send_from_directory
from flask_restful import Resource, Api
from flask import request, Response

class API(Resource):

    def get(self):
        print('Get  REQ')
        return "Test API ", 200

    def post(self):
        req = request.get_json()
        print(req)
        if req:
            return req , 200
        else:
            return "Bad Request", 403


app = Flask(__name__)
api = Api(app)


api.add_resource(API, '/api')

print("Starting IrriCare-Pro V0.7")
app.run(host='0.0.0.0', port=3005, debug=False)


