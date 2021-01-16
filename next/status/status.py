import requests
import time
import json

para = {
    "WZ": "1"
}
usdt = 0

def threMatch():
    pass


def cal():
    filePath = r"info.json"
    with open(filePath, 'r') as file:  # file in local dir only
        userData = json.loads(file.read())


resp = requests.post("https://test-wz-app.herokuapp.com/api", json=para,)
data = resp.json()
# resp = requests.get("https://test-wz-app.herokuapp.com/api")
# print(data)
getSelData(data)
