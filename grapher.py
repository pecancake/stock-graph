import matplotlib.pyplot as plt
import stockview
import yfinance as yf
from datetime import datetime, timedelta


def getCloseData(ticker, force=False):
    if ticker not in history or force:
        data = yf.Ticker(ticker).history(period="1d", start=STARTDATE, end=ENDDATE)
        history[ticker] = data['Close']

    return history[ticker]


def showGraph(plots):
    ax = plt.subplot(111)
    
    for ticker, values in sorted(plots.items(), key = lambda x: x[1][-1] if x[1][-1] != "DONE" else x[1][-2], reverse=True):
        if ticker != "all":
            coor = [(i, values[i]) for i in range(len(values)) if values[i] is not None and values[i] !="DONE"]
            xCoor = [i[0] for i in coor]
            yCoor = [i[1] for i in coor]
            ax.plot(xCoor, yCoor, label=f"{ticker} :: {round(yCoor[-1], 2)}")
        
    # ax.plot(plots["all"], label="ALL", color="black")     UNCOMMENT THIS LINE TO DRAW "ALL" LINE
    
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()


TRANSLATE = {"vfv": "vfv.to", "xeg": "xeg.to", "hero": "hero.to", "apha": "apha.to", "weed": "weed.to", "ac": "ac.to", "at": "at.to"}

history = {}
actions = stockview.getActions()
STARTDATE = min(actions.keys())
ENDDATE = datetime(2021, 2, 9)

print(STARTDATE, ENDDATE)
curr = STARTDATE
plots = {"all":[]}
BUFFER = 0
positions = None

while curr < ENDDATE:
    positions = stockview.executeActions(actions.get(curr, []), positions)
    allPlot = 0
    error = False
    
    for k,v in positions.items():
        price = getCloseData(TRANSLATE[k] if k in TRANSLATE else k).get(curr)
        
        if price is not None:
            v.setPrice(price)
            allPlot += v.value()

            if len(v.trades) > 0 or "DONE" not in plots[k]:
                if k not in plots:
                    plots[k] = [None] * BUFFER

                plots[k].append(v.value())

                if len(v.trades) == 0:
                    plots[k].append("DONE")
            
            error = False

        else:
            error = True

    if not error:
        print(stockview.datepp(curr), allPlot)
        plots['all'].append(allPlot)
        BUFFER += 1
        
    curr += timedelta(days=1)
    
showGraph(plots)
