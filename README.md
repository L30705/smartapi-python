# SMARTAPI-PYTHON

SMARTAPI-PYTHON is a Python library for dealing AMX,that is a set of REST-like HTTP APIs that expose many capabilities required to build stock market investment and trading platforms. It lets you execute orders in real time.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install smartapi-python.

```bash
pip install smartapi-python
pip install websocket-client
```

## Usage

```python
# package import statement
from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
#import smartapi.smartExceptions(for smartExceptions)

#create object of call
obj=SmartConnect(api_key="your api key",
                #optional
                #access_token = "your access token",
                #refresh_token = "your refresh_token")

#login api call

data = obj.generateSession("Your Client ID","Your Password")
refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()

#fetch User Profile
userProfile= obj.getProfile(refreshToken)
#place order
try:
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045",
        "transactiontype": "BUY",
        "exchange": "NSE",
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": "19500",
        "squareoff": "0",
        "stoploss": "0",
        "quantity": "1"
        }
    orderId=obj.placeOrder(orderparams)
    print("The order id is: {}".format(orderId))
except Exception as e:
    print("Order placement failed: {}".format(e.message))
#gtt rule creation
try:
    gttCreateParams={
            "tradingsymbol" : "SBIN-EQ",
            "symboltoken" : "3045",
            "exchange" : "NSE", 
            "producttype" : "MARGIN",
            "transactiontype" : "BUY",
            "price" : 100000,
            "qty" : 10,
            "disclosedqty": 10,
            "triggerprice" : 200000,
            "timeperiod" : 365
        }
    rule_id=obj.gttCreateRule(gttCreateParams)
    print("The GTT rule id is: {}".format(rule_id))
except Exception as e:
    print("GTT Rule creation failed: {}".format(e.message))
    
#gtt rule list
try:
    status=["FORALL"] #should be a list
    page=1
    count=10
    lists=obj.gttLists(status,page,count)
except Exception as e:
    print("GTT Rule List failed: {}".format(e.message))

#Historic api
try:
    historicParam={
    "exchange": "NSE",
    "symboltoken": "3045",
    "interval": "ONE_MINUTE",
    "fromdate": "2021-02-08 09:00", 
    "todate": "2021-02-08 09:16"
    }
    obj.getCandleData(historicParam)
except Exception as e:
    print("Historic Api failed: {}".format(e.message))
#logout
try:
    logout=obj.terminateSession('Your Client Id')
    print("Logout Successfull")
except Exception as e:
    print("Logout failed: {}".format(e.message))
```


## Getting started with SmartAPI Websocket's
```python

from smartapi import SmartWebSocket

# feed_token=092017047
FEED_TOKEN="YOUR_FEED_TOKEN"
CLIENT_CODE="YOUR_CLIENT_CODE"
# token="mcx_fo|224395"
token="EXCHANGE|TOKEN_SYMBOL"    #SAMPLE: nse_cm|2885&nse_cm|1594&nse_cm|11536&nse_cm|3045
# token="mcx_fo|226745&mcx_fo|220822&mcx_fo|227182&mcx_fo|221599"
task="mw"   # mw|sfi|dp

ss = SmartWebSocket(FEED_TOKEN, CLIENT_CODE)

def on_message(ws, message):
    print("Ticks: {}".format(message))
    
def on_open(ws):
    print("on open")
    ss.subscribe(task,token)
    
def on_error(ws, error):
    print(error)
    
def on_close(ws):
    print("Close")

# Assign the callbacks.
ss._on_open = on_open
ss._on_message = on_message
ss._on_error = on_error
ss._on_close = on_close

ss.connect()
```




