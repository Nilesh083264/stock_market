from dhanhq import MarketFeed
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
HUB_FILE_PATH = os.path.join(BASE_DIR, "etc/hub.json")
TOKEN_PATH = os.path.join(BASE_DIR, "etc/tokens.json")



# print("HUB_FILE_PATH : ",HUB_FILE_PATH)
# print("Base_dir : ",BASE_DIR)
# HUB_FILE_PATH :  /home/nilesh/Desktop/standred_Dhan_Project/etc/hub.json
# Base_dir :  /home/nilesh/Desktop/standred_Dhan_Project














CSV_URL = "https://images.dhan.co/api-data/api-scrip-master.csv"

INSTRUMENTS = [
        {"ExchangeSegment": "NSE_EQ", "SecurityId": "1333"},
        {"ExchangeSegment": "IDX_I", "SecurityId": "13"},
        {"ExchangeSegment": "IDX_I", "SecurityId": "442"},
        {"ExchangeSegment": "IDX_I", "SecurityId": "27"},
        {"ExchangeSegment": "IDX_I", "SecurityId": "51"},
        {"ExchangeSegment": "IDX_I", "SecurityId": "69"},
        {"ExchangeSegment": "IDX_I", "SecurityId": "25"}
        # {'ExchangeSegment': 'NSE_FNO', 'SecurityId': '54903'},
        # {'ExchangeSegment': 'NSE_FNO', 'SecurityId': '54964'}

]

strike_ABS = {
    "NIFTY":{"step":50,"ExchangeSegment":"IDX_I","SecurityId":13,"Exchange":"NSE_FNO"},
    "MIDCPNIFTY": {"step":25,"ExchangeSegment":"IDX_I","SecurityId":442,"Exchange":"NSE_FNO"},
    "BANKNIFTY": {"step":100,"ExchangeSegment":"IDX_I","SecurityId":25,"Exchange":"NSE_FNO"},
    "SENSEX":{"step":100,"ExchangeSegment":"IDX_I","SecurityId":51,"Exchange":"BSE_FNO"},
    "BANKEX":{"step":100,"ExchangeSegment":"IDX_I","SecurityId":69,"Exchange":"BSE_FNO"},
    "FINNIFTY":{"step":50,"ExchangeSegment":"IDX_I","SecurityId":27,"Exchange":"NSE_FNO"}
}
index_ids = {
    13:{"index":"NIFTY","last_atm":None,"CE":None,"PE":None},
    442:{"index":"MIDCPNIFTY","last_atm":None,"CE":None,"PE":None},
    25:{"index":"BANKNIFTY","last_atm":None,"CE":None,"PE":None},
    51:{"index":"SENSEX","last_atm":None,"CE":None,"PE":None},
    69:{"index":"BANKEX","last_atm":None,"CE":None,"PE":None},
    27:{"index":"FINNIFTY","last_atm":None,"CE":None,"PE":None}
}

INDEX_SYMBOLS ={
    "NIFTY":{"step":50,"ExchangeSegment":"IDX_I","SecurityId":13,"Exchange":"NSE_FNO"},
    "MIDCPNIFTY": {"step":25,"ExchangeSegment":"IDX_I","SecurityId":442,"Exchange":"NSE_FNO"},
    "BANKNIFTY": {"step":100,"ExchangeSegment":"IDX_I","SecurityId":25,"Exchange":"NSE_FNO"},
    "SENSEX":{"step":100,"ExchangeSegment":"IDX_I","SecurityId":51,"Exchange":"BSE_FNO"},
    "BANKEX":{"step":100,"ExchangeSegment":"IDX_I","SecurityId":69,"Exchange":"BSE_FNO"},
    "FINNIFTY":{"step":50,"ExchangeSegment":"IDX_I","SecurityId":27,"Exchange":"NSE_FNO"}
}

subscribed_ATMS = []










