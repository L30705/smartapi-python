from logzero import logger
from SmartApi.smartConnect import SmartConnect
import pyotp

api_key = 'Your Api Key'
username = 'Your client code'
pwd = 'Your pin'
smartApi = SmartConnect(api_key)
token = "Your QR value"
totp=pyotp.TOTP(token).now()
correlation_id = "abcde"
data = smartApi.generateSession(username, pwd, totp)
# print(data)
authToken = data['data']['jwtToken']
refreshToken = data['data']['refreshToken']
feedToken = smartApi.getfeedToken()
# print("Feed-Token :", feedToken)
res = smartApi.getProfile(refreshToken)
# print("Res:", res)
smartApi.generateToken(refreshToken)
res=res['data']['exchanges']


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
orderid = smartApi.placeOrder(orderparams)
print("PlaceOrder", orderid)

modifyparams = {
    "variety": "NORMAL",
    "orderid": orderid,
    "ordertype": "LIMIT",
    "producttype": "INTRADAY",
    "duration": "DAY",
    "price": "19500",
    "quantity": "1",
    "tradingsymbol": "SBIN-EQ",
    "symboltoken": "3045",
    "exchange": "NSE"
}
smartApi.modifyOrder(modifyparams)
print("Modify Orders:",modifyparams)

cancelOrder=smartApi.cancelOrder(orderid, "NORMAL")
print("cancelOrder",cancelOrder)

orderbook=smartApi.orderBook()
print("Order Book :", orderbook)

tradebook=smartApi.tradeBook()
print("Trade Book :",tradebook)

rmslimit=smartApi.rmsLimit()
print("RMS Limit :", rmslimit)

pos=smartApi.position()
print("Position :", pos)

holdings=smartApi.holding()
print("Holdings :", holdings)

exchange = "NSE"
tradingsymbol = "SBIN-EQ"
symboltoken = 3045
ltp=smartApi.ltpData("NSE", "SBIN-EQ", "3045")
print("Ltp Data :", ltp)


params = {
    "exchange": "NSE",
    "oldproducttype": "DELIVERY",
    "newproducttype": "MARGIN",
    "tradingsymbol": "SBIN-EQ",
    "transactiontype": "BUY",
    "quantity": 1,
    "type": "DAY"

}

convertposition=smartApi.convertPosition(params)

gttCreateParams = {
    "tradingsymbol": "SBIN-EQ",
    "symboltoken": "3045",
    "exchange": "NSE",
    "producttype": "MARGIN",
    "transactiontype": "BUY",
    "price": 100000,
    "qty": 10,
    "disclosedqty": 10,
    "triggerprice": 200000,
    "timeperiod": 365
}
rule_id = smartApi.gttCreateRule(gttCreateParams)
print("Gtt Rule :", rule_id)

gttModifyParams = {
    "id": rule_id,
    "symboltoken": "3045",
    "exchange": "NSE",
    "price": 19500,
    "quantity": 10,
    "triggerprice": 200000,
    "disclosedqty": 10,
    "timeperiod": 365
}
modified_id = smartApi.gttModifyRule(gttModifyParams)
print("Gtt Modified Rule :", modified_id)

cancelParams = {
    "id": rule_id,
    "symboltoken": "3045",
    "exchange": "NSE"
}

cancelled_id = smartApi.gttCancelRule(cancelParams)
print("gtt Cancel Rule :", cancelled_id)

gttdetails=smartApi.gttDetails(rule_id)
print("GTT Details",gttdetails)

smartApi.gttLists('List of status', '<page>', '<count>')

candleParams={
     "exchange": "NSE",
     "symboltoken": "3045",
     "interval": "ONE_MINUTE",
     "fromdate": "2021-02-10 09:15",
     "todate": "2021-02-10 09:16"
}
candledetails=smartApi.getCandleData(candleParams)
print("Historical Data",candledetails)

terminate=smartApi.terminateSession('Your client code')
print("Connection Close",terminate)

# # Websocket Programming

from SmartApi.smartWebSocketV2 import SmartWebSocketV2

AUTH_TOKEN = authToken
API_KEY = api_key
CLIENT_CODE = username
FEED_TOKEN = feedToken
# correlation_id = "abc123"
action = 1
mode = 1

token_list = [
    {
        "exchangeType": 1,
        "tokens": ["26009","1594"]
    }
]
token_list1 = [
    {
        "action": 0,
        "exchangeType": 1,
        "tokens": ["26009"]
    }
]

sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)

def on_data(wsapp, message):
    logger.info("Ticks: {}".format(message))
    close_connection()

def on_open(wsapp):
    logger.info("on open")
    sws.subscribe(correlation_id, mode, token_list)
    # sws.unsubscribe(correlation_id, mode, token_list1)


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
