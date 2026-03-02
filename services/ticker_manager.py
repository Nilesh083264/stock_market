import threading
from services.dhan_ws_client import DhanTickerClient
from constants.token_service import token
from constants.constant import INSTRUMENTS


class TickerManager:

    def __init__(self):
        self.client = None
        self.thread = None
        self.running = False

    def _run(self, loop):
        TOKEN = token.get("access_token")
        CLIENT_ID = token.get("client_id")

        self.client = DhanTickerClient(TOKEN, CLIENT_ID, loop)
        self.client.connect()
        self.client.subscribe_ticker(INSTRUMENTS)
        self.running = True

    def start(self, loop):
        if self.running:
            return

        self.thread = threading.Thread(target=self._run,args=(loop,),daemon=True)
        self.thread.start()

    def stop(self):
        if self.client:
            self.client.disconnect()
        self.running = False


ticker_manager = TickerManager()