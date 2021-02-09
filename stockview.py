import csv
from datetime import datetime

PRICES = {
    "vfv": 8695,
    "nok": 470,
    "hero": 4090,
    "bb": 1531,
    "amc": 897,
    "xeg": 550
}
ISUSD = ["amc", "nok", "pltr", "bb"]
USDTOCAD = 12544

class Security:
    def __init__(self, ticker):
        self.net = 0
        self.trades = []
        self.ticker = ticker
        self.price = None

    def buy(self, price, count, rate=10000):
        self.trades.append(Share(price, count, rate))

    def sell(self, price, count, rate=10000):
        while count > 0:
            trade = self.trades.pop(0)
            
            if trade.count > count:
                trade.count -= count
                self.net += (price * (rate / 10000) - trade.price * (trade.rate / 10000)) * count
                self.trades.append(trade)
                break
                
            else:
                self.net += (price * (rate / 10000) - trade.price * (trade.rate / 10000)) * trade.count
                count -= trade.count

    def setPrice(self, val):
        if self.ticker in ISUSD:
            self.price =  (USDTOCAD/10000) * val * 100

        else:
            self.price = val * 100
        
    def value(self):
        return (self.net + sum([(self.price - t.price / (10000 / t.rate)) * t.count for t in self.trades])) / 100

    def __str__(self):
        return str(self.trades)

    def __repr__(self):
        return str(self)
    
class Share:
    def __init__(self, price, count, rate=10000):
        self.price = price
        self.count = count
        self.rate = rate

    def __str__(self):
        return f"{self.price} x {self.count}"

    def __repr__(self):
        return str(self)

def convertDate(raw):
    m, d, y = raw[0:2], raw[2:4], raw[4:6]
    return datetime(int("20"+y), int(m), int(d))

def datepp(date):
    return date.strftime("%d %B %Y")

def getActions():
    actions = {}
    with open("trades.csv") as csvfile:
        next(csvfile)
        
        for (date, action, stock, price, count, *rate) in csv.reader(csvfile):
            cDate = convertDate(date)
            if cDate not in actions:
                actions[cDate] = []

            actions[cDate].append([action, stock, price, count, *rate])

    return actions
            
def executeActions(actions, positions=None):
    if positions is None:
        positions = {}

    for (action, stock, price, count, *rate) in actions:
        if stock not in positions:
            positions[stock] = Security(stock)
            
        if action == "buy":
            print(f"buying {count} shares of {stock} for {price}")
            positions[stock].buy(int(price), int(count), int(rate[0]) if rate else 10000)

        elif action == "sell":
            print(f"selling {count} shares of {stock} for {price}")
            positions[stock].sell(int(price), int(count), int(rate[0]) if rate else 10000)

    return positions
