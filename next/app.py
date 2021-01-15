import requests
import time
import json

para = {
    "WZ": "1"
}
usdt = 0


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


def calValue(trxList):
    global usdt
    total = len(trxList)
    totalVal = 0
    totalQty = 0
    for i in range(total):
        if (trxList[0][0] == "U"):
            val = trxList[i][3]*79
        else:
            val = trxList[i][3]
        totalVal = totalVal + val
        totalQty = totalQty+trxList[i][1]

    return [totalVal, totalQty,totalVal*0.004]


def getSelData(resp):
    global usdt

    filePath = r"data.json"
    with open(filePath, 'r') as file:  # file in local dir only
        userData = json.loads(file.read())
    if userData:
        avgRate = 0
        adv = 0
        by = userData["by"]
        usdt = float(resp["usdtinr"]["last"])
        print("USDT ", usdt)
        print("\n")
        for key, val in by.items():
            # print(f"{key} {val}")
            stkData = calValue(val)
            # print(stkData)
            totalVal = stkData[0]
            qty = stkData[1]
            fees = stkData[2]
            curr = resp[key]
            tag = curr["base_unit"]
            last = float(curr["last"])
            nowVal = qty*last*usdt
            change = ((nowVal-totalVal)/totalVal)*100
            gain = nowVal-totalVal -fees

            if(tag != "usdt"):
                adv = adv + gain
                print(
                    f"{tag}  \t {round(last,3)}    \t {round(qty,3)}       \t {round(nowVal,3)}   \t {round(change,3)}     \t {round(gain,3)}")
        print("\n Gain ", adv)


resp = requests.post("https://test-wz-app.herokuapp.com/api", json=para,)
data = resp.json()
# resp = requests.get("https://test-wz-app.herokuapp.com/api")
# print(data)
getSelData(data)
