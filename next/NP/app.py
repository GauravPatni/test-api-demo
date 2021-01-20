import requests
import time
import json

para = {
    "WZ": "1"
}
usdt = 0


def calProf(data):
    global usdt
    
    txnProf = []
    prof =0
    for key, curr in data["sl"].items():
        totalTxn = len(curr)
        sum =0
        
        for tn in range(totalTxn):
            if (curr[tn][0]=="U"):            
                sum = sum+  (curr[tn][5] - curr[tn][3])*usdt*0.998
            else:
                sum =sum+  (curr[tn][5] - curr[tn][3])*0.998

        prof = prof + sum   
        print(f"{key} \t{round(sum,3)}")
    
    print(f"--------------------------\ntotal  \t\t{round(prof,3)}")

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
            val = trxList[i][3]*79.15
        else:
            val = trxList[i][3]
        totalVal = totalVal + val
        totalQty = totalQty+trxList[i][1]

    return [totalVal, totalQty, totalVal*0.004]


def calIn(trxIn):
    total = len(trxIn)
    totalVal = 0
    for i in range(total):
        totalVal =totalVal+trxIn[i]

    return totalVal

def getSelData(resp):
    global usdt

    filePath = r"data.json"
    with open(filePath, 'r') as file:  # file in local dir only
        userData = json.loads(file.read())
    if userData:
        avgRate = 0
        adv = 0
        port = 0
        nowVal =0
        by = userData["by"]
        usdt = float(resp["usdtinr"]["last"])
        inVal = calIn(userData["dp"])
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
            
            
            if(tag != "usdt"):
                if(qty == 0):
                    nowVal =0
                    change =0
                    gain =0
                else:
                    nowVal = qty*last*usdt
                    change = ((nowVal-totalVal)/totalVal)*100
                    gain = nowVal-totalVal - fees
                    adv = adv + gain
            else:
                nowVal = qty*last
                gain = 0
                change =0
            port = port + nowVal
            print(
                f"{tag}  \t {round(last,3)}    \t {round(qty,3)}       \t {round(nowVal,3)}   \t {round(change,3)}     \t {round(gain,3)}")
        # print("\n Gain ", adv)
        print(f"\n In {round(inVal,1)} \tPort {round(port,1)} \tDif {round((port - inVal),1)} \tGainCal {round(adv,1)} \tSl {(port - inVal)-adv}\n")
        calProf(userData)

resp = requests.post("https://test-wz-app.herokuapp.com/api", json=para,)
data = resp.json()
# resp = requests.get("https://test-wz-app.herokuapp.com/api")
# print(data)
getSelData(data)
