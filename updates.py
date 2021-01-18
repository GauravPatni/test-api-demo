import requests
import datetime
from pycoingecko import CoinGeckoAPI
import time

from flask import Flask, render_template, send_from_directory
from flask_restful import Resource, Api
from flask import request, Response


cg = CoinGeckoAPI()

gDict = {}
gIdList = []
currNow = None


class UPD(Resource):

    def get(self):
        print('Get  Updates V1')
        return "Test API", 200

    def post(self):
        req = request.get_json()
        print(req)
        if req:
            if "UD" in req:
                return prepareReply(), 200
            return "Bad Info Request", 403
        else:
            return "Bad Request", 403


def updateCurrStatus():
    global gIdList

    try:
        mkDataList = []
        gDict.clear()
        for pNo in range(1, 6, 1):
            mkLen = 0
            mkDataList = cg.get_coins_markets(
                vs_currency='usd', ids=gIdList, per_page=50, page=pNo, price_change_percentage='1h,24h')

            for mkData in mkDataList:
                gDict[mkData["id"]] = mkData
            if (mkLen < 50):
                break

        # print(f"Global Id   {len(gIdList)}")
        # print(f"Global Dict {len(gDict)}")

        return True
    except:
        print("Error: updateCurrStatus")
        return False


def preSupportedWzCurr():
    global gIdList

    try:
        cSymbolList = cg.get_coins_list()
        cgLen = len(cSymbolList)
        para = {"WZ": 1}
        resp = requests.post(
            "https://api.wazirx.com/api/v2/tickers", json=para,)
        wData = resp.json()
        if wData:
            for key, val in wData.items():
                if(key[-4:] == "usdt"):
                    for cIndex in range(cgLen):
                        if (key[:-4] == cSymbolList[cIndex]["symbol"]):
                            gIdList.append(cSymbolList[cIndex]["id"])

            # print(gIdList)
            # print("\n\n")
            # stat = updateCurrStatus()
            # return stat
            return True
    except:
        print("Error: preSupportedWzCurr")
        False


def Analyze():
    rply = ""
    if (updateCurrStatus()):
        print(f"\n\n---------------{datetime.datetime.now()}\n")
        for key, val in gDict.items():
            sym = gDict[key]["symbol"]
            now = gDict[key]["current_price"]
            l24hHi = gDict[key]["high_24h"]
            ah = gDict[key]["ath"]
            ch1h = gDict[key]["price_change_percentage_1h_in_currency"]

            ahTimeDel = datetime.datetime.fromisoformat(
                gDict[key]["ath_date"].replace('Z', ''))

            delT = datetime.datetime.now() - ahTimeDel

            pickPer = ((l24hHi/now) - 1)*100

            if((now) and (l24hHi) and (ah) and (ch1h)):

                if(((ah > (now*1.06)) and (pickPer > 6)) or (ch1h > 6)):
                    rply = rply + \
                        f"{'{0:<8}'.format(sym)}{'{0:<30}'.format(key)}{'{0:<8}'.format(round(pickPer, 1))}{'{0:<8}'.format(round(ch1h, 1))}{'{0:<8}'.format(round(((ah/now - 1)*100), 2))}\n"
                    # print(f"{'{0:<8}'.format(sym)}{'{0:<30}'.format(key)}{'{0:<8}'.format(round(pickPer, 1))}{'{0:<8}'.format(round(ch1h, 1))}{'{0:<8}'.format(round(((ah/now - 1)*100), 2))}")
        return rply
    return False


def prepareReply():
    if(preSupportedWzCurr()):
        rply = Analyze()
        if(rply):
            return rply
        else:
            "Error"