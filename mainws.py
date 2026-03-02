from services.dhan_ws_client import DhanTickerClient
import time
from constants.token_service import token


TOKEN = token.get("access_token")
CLIENT_ID = token.get("client_id")



client = DhanTickerClient(TOKEN, CLIENT_ID)

client.connect()

instruments = [
        # {"ExchangeSegment": "NSE_EQ", "SecurityId": "1333"},
        # {"ExchangeSegment": "IDX_I", "SecurityId": "13"},
        {"ExchangeSegment": "IDX_I", "SecurityId": "442"},
        # {"ExchangeSegment": "IDX_I", "SecurityId": "27"},
        # {"ExchangeSegment": "IDX_I", "SecurityId": "51"},
        # {"ExchangeSegment": "IDX_I", "SecurityId": "69"},
        # {"ExchangeSegment": "IDX_I", "SecurityId": "25"}
        # {'ExchangeSegment': 'NSE_FNO', 'SecurityId': '54903'},
        # {'ExchangeSegment': 'NSE_FNO', 'SecurityId': '54964'}

]

client.subscribe_ticker(instruments)


try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    client.disconnect()
print("Program exited cleanly")
client.disconnect()
print("Program exited cleanly")