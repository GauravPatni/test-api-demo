import requests
import time
import json
from datetime import datetime

para = {
    "WZ": "1"
}
usdt = 0

allCurr = {}

def pkDet(key,val):
    if key in allCurr:
        prev = allCurr[key]["last"]
        now = float(val["last"])
        if(now >prev):
            allCurr[key] = now
            allCurr[key]["dt"] = datetime.now()

def threMatch(ref,current):
    print(f"\n------------------{datetime.now()}-------------")
    for key, curr in ref.items():
        
        if(key[-4:]=="usdt"):
            now = float(current[key]["last"])
            ref = float(curr["last"])

            if(now >0):
                delta =  ref*0.91
                if(now < delta):
                    tag = key[:(len(key)-4)]
                    print(f"{tag} \t{round((1-now/ref),4)}%    \t{round(ref,4)} \t\t{round(now,4)}")
    

def cal():
    filePath = r"bench.json"
    with open(filePath, 'r') as file:  # file in local dir only
        userData = json.loads(file.read())


    resp = requests.post("https://test-wz-app.herokuapp.com/api", json=para,)
    data = resp.json()
    # resp = requests.get("https://test-wz-app.herokuapp.com/api")
    # print(data)
    threMatch(userData,data)


while(1):
    cal()
    time.sleep(30)