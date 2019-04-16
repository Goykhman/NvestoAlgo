import requests
import json
import warnings

warnings.filterwarnings("ignore")

apiKey = "JBibi78689gbkugt87TRbiut365gkJGiyf75878ugbkvfjyfkjvjyf" # public API
url0 = "https://nvestoapi.herokuapp.com/api/" + apiKey + "/"

allStocks = ["BANK", "PORK", "GOLD", "POTT", "KERR", "CASS"]

class NvestoAPI():

    def __init__(self):
        self.NvestoAPI = "NvestoAPI"

    def getAuthentication(self, userId, password):
        requestURL = url0 + "authenticate"
        credentials = {"userId": userId, "password": password}
        requestAuthenticate = requests.post(requestURL, data = credentials)
        token = json.loads(requestAuthenticate.text)
        return token["token"]

    def getPortfolio(self, userId, token):
        requestURL = url0 + "userData" + "/" + str(userId)
        requestPortfolio = requests.post(requestURL, data = {"token": token})
        portfolio = json.loads(requestPortfolio.text)
        portfolio["cash"] = float(portfolio["cash"])
        for stock in allStocks:
            portfolio[stock] = int(portfolio[stock])
        return portfolio

    def getStocksData(self):
        return json.loads(requests.get(url0 + "stockData").text)

    def getPriceArrays(self):
        priceArrays = json.loads(requests.get(url0 + "priceArrays").text)
        return priceArrays

    def submitOrder(self, userId, token, stock, side, price, size):
        order = {"userId": userId, "token": token, "stock": stock, "side": side, "price": price, "size": size}
        requestOrder = requests.post(url0 + "order", data = order)
        requestOrder = requestOrder or ""
        report = json.loads(requestOrder.text)
        if "orderId" in report:
            return report["orderId"]
        else:
            return -1

    def cancelOrder(self, userId, token, stock, orderId):
        cancel = {"stock": stock, "orderId": orderId, "token": token}
        return json.loads(requests.post(url0 + "cancel", data = cancel).text)

    def findPending(self, userId, token):
        pending = json.loads(requests.post(url0 + "userData" + "/" + str(userId), data = {"token": token}).text)["pending"]
        ret = {}
        for stock in pending.keys():
            ret[stock] = [x["orderId"] for x in pending[stock]]
        return ret
