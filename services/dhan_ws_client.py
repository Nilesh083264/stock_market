import websocket
import threading
import json
import struct
import time
from utils.helpers import ATM,get_instrument, get_instruments_list
from constants.constant import index_ids
import asyncio
from services.ws_manager import manager


dict_instruments = {}

class DhanTickerClient:

    def __init__(self, token: str, client_id: str ,loop):
        self.url = (
            f"wss://api-feed.dhan.co?"
            f"version=2&token={token}&clientId={client_id}&authType=2"
        )
        self.ws = None
        self.connected = False
        self.loop = loop   # store main event loop

    # -------------------------
    # Binary Packet Parser
    # -------------------------
    def parse_ticker_packet(self, packet: bytes):

        if len(packet) < 16:
            return None

        response_code = packet[0]

        security_id = struct.unpack("<I", packet[4:8])[0]
        ltp = struct.unpack("<f", packet[8:12])[0]
        ltt_epoch = struct.unpack("<I", packet[12:16])[0]

        return {
            "response_code": response_code,
            "security_id": security_id,
            "ltp": round(ltp, 2),
            "ltt_epoch": ltt_epoch
        }

    # -------------------------
    # WebSocket Callbacks
    # -------------------------
    def on_open(self, ws):
        print("Connected to Dhan Feed")
        self.connected = True

    # def on_message(self, ws, message):
    #
    #     if isinstance(message, bytes):
    #         tick = self.parse_ticker_packet(message)
    #         tick_index = (index_ids.get(tick["security_id"]))
    #         if(tick_index != None ):
    #             tick_index = tick_index.get("index")
    #             last_atm = (index_ids.get(tick["security_id"])).get("last_atm")
    #             atm = ATM(tick_index,tick["ltp"])
    #             if(last_atm != atm):
    #                 if(last_atm != None):
    #                     lst = get_instruments_list(tick_index,last_atm)
    #                     self.unsubscribe_ticker(lst)
    #                     lst = get_instruments_list(tick_index,atm)
    #                     # time.sleep(0.1)
    #                     self.subscribe_ticker(lst)
    #                 index_ids[tick["security_id"]]["last_atm"] = atm
    #         if tick:
    #             print("Tick : ", tick)
    #     else:
    #         print("Text:", message)

    def on_message(self, ws, message):

        # Ignore non-binary messages
        if not isinstance(message, bytes):
            # print("Text:", message)
            return
        # print("Message :" ,message)
        tick = self.parse_ticker_packet(message)
        if not tick:
            return

        # Ignore response_code == 6
        if tick.get("response_code") == 6:
            return

        security_id = tick.get("security_id")
        ltp = tick.get("ltp")

        if not security_id or ltp is None:
            return

        index_data = index_ids.get(security_id)
        if not index_data:
            return

        tick_index = index_data.get("index")
        last_atm = index_data.get("last_atm")

        if not tick_index:
            return

        current_atm = ATM(tick_index, ltp)

        if last_atm != current_atm:

            if last_atm is not None:
                # print("Last ATM:", get_instruments_list(tick_index, last_atm))
                self.unsubscribe_ticker(get_instruments_list(tick_index, last_atm))

            # print("NEW ATM:", get_instruments_list(tick_index, current_atm))
            self.subscribe_ticker(get_instruments_list(tick_index, current_atm))

            index_data["last_atm"] = current_atm

        # print("Tick:", tick)
        # print("Tick:", tick)

        # Broadcast to all connected WebSocket clients
        if manager.active_connections:
            asyncio.run_coroutine_threadsafe(
                manager.broadcast(tick),
                self.loop
            )

    def on_error(self, ws, error):
        print("Error :", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Disconnected from Dhan Feed")
        self.connected = False

    # -------------------------
    # Connect
    # -------------------------
    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        thread = threading.Thread(target=self.ws.run_forever)
        thread.daemon = True
        thread.start()

        timeout = 5
        start = time.time()

        while not self.connected:
            if time.time() - start > timeout:
                raise TimeoutError("Connection timeout")
            time.sleep(0.1)

    # -------------------------
    # Subscribe Ticker
    # -------------------------
    def subscribe_ticker(self, instruments: list):

        payload = {
            "RequestCode": 15,
            "InstrumentCount": len(instruments),
            "InstrumentList": instruments
        }

        self.ws.send(json.dumps(payload))
        # print("Ticker subscription sent",instruments)

    # -------------------------
    # Unsubscribe Ticker
    # -------------------------
    def unsubscribe_ticker(self, instruments: list):

        payload = {
            "RequestCode": 16,
            "InstrumentCount": len(instruments),
            "InstrumentList": instruments
        }

        self.ws.send(json.dumps(payload))
        print("Ticker unsubscription sent")

    # -------------------------
    # Disconnect
    # -------------------------
    def disconnect(self):

        if self.ws and self.connected:
            payload = {
                "RequestCode": 12
            }

            self.ws.send(json.dumps(payload))
            print("Disconnect request sent")

            time.sleep(1)
            self.ws.close()



