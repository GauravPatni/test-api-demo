import requests
import datetime
from pycoingecko import CoinGeckoAPI
import time

cg = CoinGeckoAPI()

gDict = {}
gIdList = []
currNow = None


def updateCurrStatus():
    global gIdList
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
    # try:
    #     mkDataList = []
    #     gDict.clear()
    #     for pNo in range(1, 6, 1):
    #         mkLen = 0
    #         mkDataList = cg.get_coins_markets(
    #             vs_currency='usd', ids=gIdList, per_page=50, page=pNo, price_change_percentage='1h,24h')

    #         for mkData in mkDataList:
    #             gDict[curr] = mkData
    #         if (mkLen < 50):
    #             break

    #     print(f"Global Id   {len(gIdList)}")
    #     print(f"Global Dict {len(gDict)}")
    
    #     return True
    # except:
    #     print("Error: updateCurrStatus")
    #     return False


def preSupportedWzCurr():
    global gIdList

    cSymbolList = cg.get_coins_list()
    cgLen = len(cSymbolList)
    para = {"WZ": 1}
    resp = requests.post("https://test-wz-app.herokuapp.com/api", json=para,)
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
    # try:
    #     cSymbolList = cg.get_coins_list()
    #     cgLen = len(cSymbolList)
    #     para = {"WZ": 1}
    #     resp = requests.post("https://test-wz-app.herokuapp.com/api", json=para,)
    #     wData = resp.json()
    #     if wData:
    #         for key, val in wData.items():
    #             if(key[-4:] == "usdt"):
    #                 for cIndex in range(cgLen):
    #                     if (key[:-4] == cSymbolList[cIndex]["symbol"]):
    #                         gIdList.append(cSymbolList[cIndex]["id"])

    #         # print(gIdList)
    #         # print("\n\n")
    #         # stat = updateCurrStatus()
    #         # return stat
    #         return True
    #     return False
    # except :
    #     print("Error: preSupportedWzCurr")
    #     False



    


def getCurrNow():
    global currNow
    currNow = cg.get_price(vs_currencies='usd', ids=gIdList,
                           include_24hr_change='true', include_24hr_vol='true')
    # print(currNow)


def Analyze():
    
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
                    print(
                        f"{'{0:<8}'.format(sym)}{'{0:<30}'.format(key)}{'{0:<8}'.format(round(pickPer, 1))}{'{0:<8}'.format(round(ch1h, 1))}{'{0:<8}'.format(round(((ah/now - 1)*100), 2))}")


# def Analyze():
#     print(f"\n\n---------------{datetime.datetime.now()}\n")
#     for key, val in gDict.items():

#         now = val["usd"]
#         l24hCh = currNow[key]["usd_24h_change"]
#         l24hVol = currNow[key]["usd_24h_vol"]
#         ah = gDict[key]["ath"]
#         ahTimeDel = datetime.datetime.fromisoformat(
#             gDict[key]["ath_date"].replace('Z', ''))

#         delT = datetime.datetime.now() - ahTimeDel


#         if(l24hCh == None):
#             l24hCh = 0

#         if(l24hCh < 0):
#             l24hCh= l24hCh*-1

#         minChange =0
#         if(l24hVol):
#             minChange = l24hVol*now

#         if(((now*1.1) <= ah) and (l24hVol!= None) and (minChange > 1000000) and (l24hCh > 5)):

#             print(
#             f"{'{0:<30}'.format(key)}\t {'{0:<5} %'.format(round(((ah/now -1)*100),2))}\t{'{0:<20}'.format(round(l24hVol,1))}\t{round(ah,3)} \t{delT}")


preSupportedWzCurr()

while(1):
    Analyze()
    time.sleep(30)
