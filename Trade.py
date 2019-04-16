from NvestoAPI import NvestoAPI

class UserAlgorithm():

    def __init__(self):
        '''
        Attributes:
            api -- handle to the Nvesto Stock Exchange private API
            userId, password -- account information of a registered user
            token -- temporary user authentication string
            portfolio -- placeholder for a user's portfolio
        '''
        self.api = NvestoAPI()
        self.userId = "" # put your user ID here
        self.password = "" # put your password here
        self.token = ""
        self.portfolio = {}
        self.authenticate() # do not remove: always start with authentication
        self.updatePortfolio()

    def authenticate(self):
        '''
        No arguments: uses the userId and password class attributes
        No returns: sets the token class attribute
        '''
        self.token = self.api.getAuthentication(self.userId, self.password)

    def updatePortfolio(self):
        '''
        No arguments: uses the userId class attribute
        No returns: sets the portfolio class attribute
        '''
        self.portfolio = self.api.getPortfolio(self.userId, self.token)

    def getStockPrice(self, stock):
        '''
        Arguments:
            stock --  string, a valid stock ticker.
        Returns:
            price -- float
        '''
        bid = self.api.getStocksData()[stock]["bid"]
        ask = self.api.getStocksData()[stock]["ask"]
        return int(100 * (bid + ask) / 200)

    def getStockSentiment(self, stock):
        '''
        Arguments:
            stock --  string, a valid stock ticker
        Returns:
            sentiment -- string, valued "positive", "negative", or "neutral"
        '''
        return self.api.getStocksData()[stock]["sentiment"]

    def getPriceAttays(self, stock, interval):
        '''
        Arguments:
            stock --  string, a valid stock ticker
            interval -- string, either of "hour", "day", "week", "month", "year"
        Returns:
            prices -- array of price objects,
            price objects are {UTC UNIX time: int, price: float}
        '''
        return self.api.getPriceArrays()[stock][interval]

    def submitOrder(self, stock, side, price, size):
        '''
        Arguments:
            stock --  string, a valid stock ticker
            side -- char, either 'B' (for buy) or 'S' for (sell)
            price -- float, with up to two decimal digits
            size -- int
        Returns:
            orderId -- ID number of the submitted order, or -1 if submission failed
        '''
        return self.api.submitOrder(self.userId, self.token, stock, side, price, size)

    def cancelOrder(self, stock, orderId):
        '''
        Arguments:
            stock --  string, a valid stock ticker
            orderId -- order ID to be cancelled
        Returns:
            object -- cancellation report, object {success: True/False, errorMEssage: ''}
        '''
        return self.api.cancelOrder(self.userId, self.token, stock, orderId)

    def findPending(self):
        '''
        Returns:
            object -- pending orders of the user, objects: {stock: array of order IDs}
        '''
        return self.api.findPending(self.userId, self.token)

    def cancelAllOrders(self):
        '''
        No returns: cancels all the pending orders
        '''
        pending = self.findPending()
        for stock in pending.keys():
            for orderId in pending[stock]:
                self.cancelOrder(stock, orderId)


userAlgorithm = UserAlgorithm()

orderId = userAlgorithm.submitOrder("BANK", 'B', 1, 1)
print userAlgorithm.findPending()
userAlgorithm.cancelAllOrders()
print userAlgorithm.findPending()
