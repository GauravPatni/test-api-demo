import requests
import time
import json

para = {
    "WZ": "1"
}


def calAvgRate(trxList):
    total = len(trxList)
    totalVol = 0
    for i in range(total):
        totalVol = totalVol+trxList[i][0]

    avgRt = 0
    for i in range(total):
        valCurr = trxList[i][0]
        perc = valCurr/totalVol

        avgRt = avgRt+trxList[i][1]*perc
    # avgRt=avgRt/total

    # print(f"{totalVol} {avgRt}")
    return [totalVol, totalVol/avgRt, avgRt]  # total , qty


def getSelData(resp):
    print("\n")
    filePath = r"data.json"
    with open(filePath, 'r') as file:  # file in local dir only
        userData = json.loads(file.read())
    if userData:
        avgRate = 0
        adv =0
        for key, val in userData.items():
            # print(f"{key} {val}")
            initVal = calAvgRate(val)
            curr = resp[key]
            tag = curr["base_unit"]
            last = float(curr["last"])
            change = ((last/initVal[2])-1)*100
            gain = initVal[0] * change/100 * 78.2
            inrVol = initVal[1] * last *78.2
            if(tag != "usdt"):
                adv = adv+ gain
                print(
                f"{tag}  \t {round(initVal[1],3)}    \t {round(initVal[0],3)}   \t {round(initVal[2],3)}     \t {round(last,3)}     \t{round(change,2)}      \t{round(inrVol,1)}      \t{round(gain,1)}   \t {round(adv,1)}")
        print("\n Gain ",adv)

resp = requests.post("https://test-wz-app.herokuapp.com/api", json=para,)
data = resp.json()
# resp = requests.get("https://test-wz-app.herokuapp.com/api")
# print(data)
getSelData(data)
