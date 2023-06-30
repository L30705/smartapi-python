# SMARTAPI-PYTHON

SMARTAPI-PYTHON is a Python library for interacting with Angel's Trading platform  ,that is a set of REST-like HTTP APIs that expose many capabilities required to build stock market investment and trading platforms. It lets you execute orders in real time..


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install smartapi-python.

```bash
pip install -r requirements_dev.txt       # for downloading the other required packages
pip install smartapi-python
pip install websocket-client
```

## Usage

```python
# package import statement
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp

api_key = 'Your Api Key'
clientId = 'Your Client Id'
pwd = 'Your Pin'
smartApi = SmartConnect(api_key)
token = "Your QR code value"
totp=pyotp.TOTP(token).now()
correlation_id = "abc123"

# login api call

data = smartApi.generateSession(clientId, pwd, totp)
# print(data)
authToken = data['data']['jwtToken']
refreshToken = data['data']['refreshToken']

# fetch the feedtoken
feedToken = smartApi.getfeedToken()

# fetch User Profile
res = smartApi.getProfile(refreshToken)
smartApi.generateToken(refreshToken)
res=res['data']['exchanges']

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
    orderId=smartApi.placeOrder(orderparams)
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
    rule_id=smartApi.gttCreateRule(gttCreateParams)
    print("The GTT rule id is: {}".format(rule_id))
except Exception as e:
    print("GTT Rule creation failed: {}".format(e.message))
    
#gtt rule list
try:
    status=["FORALL"] #should be a list
    page=1
    count=10
    lists=smartApi.gttLists(status,page,count)
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
    smartApi.getCandleData(historicParam)
except Exception as e:
    print("Historic Api failed: {}".format(e.message))
#logout
try:
    logout=smartApi.terminateSession('Your Client Id')
    print("Logout Successfull")
except Exception as e:
    print("Logout failed: {}".format(e.message))

```


## Getting started with SmartAPI Websocket's

```python

from SmartApi import SmartWebSocket

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


####### Websocket sample code ended here #######

####### Websocket V2 sample code #######

from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger

AUTH_TOKEN = "Your Auth_Token"
API_KEY = "Your Api_Key"
CLIENT_CODE = "Your Client Code"
FEED_TOKEN = "Your Feed_Token"
correlation_id = "abc123"
action = 1
mode = 1
token_list = [
    {
        "exchangeType": 1,
        "tokens": ["26009"]
    }
]
sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)

def on_data(wsapp, message):
    logger.info("Ticks: {}".format(message))
    # close_connection()

def on_open(wsapp):
    logger.info("on open")
    sws.subscribe(correlation_id, mode, token_list)

def on_error(wsapp, error):
    logger.error(error)

def on_close(wsapp):
    logger.info("Close")

def close_connection():
    sws.close_connection()


# Assign the callbacks.
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close

sws.connect()

```
