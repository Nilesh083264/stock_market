import requests
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from constants.token_service import token


# ==========================================================
# UI → DHAN PAYLOAD MAPPING
# ==========================================================

CATEGORY_MAP = {
    "equity": "NSE_FNO",
}

INDEX_MAP = {
    "nifty": 13,
    "banknifty": 25,
    "finnifty": 27,
    "sensex": 51,
    "midcapnifty": 442,
    "bankex": 69
}


def resolve_expiry(expiry_date: str | None):
    """
    Basic expiry resolver.
    If expiry_date is None → current weekly expiry.
    You can improve this later for monthly logic.
    """
    if not expiry_date:
        return "WEEK", 1

    return "WEEK", 1


# ==========================================================
# CONFIG
# ==========================================================

class DhanConfig:
    BASE_URL = "https://api.dhan.co/v2/charts/rollingoption"

    def __init__(self):
        self.access_token = token.get("access_token")

    @property
    def headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "access-token": self.access_token
        }


# ==========================================================
# PAYLOAD BUILDER
# ==========================================================

class OptionPayloadBuilder:

    def __init__(self):
        self.payload = {
            "interval": "1",
            "instrument": "OPTIDX",
            "strike": "ATM",
            "requiredData": ["open", "high", "low", "close", "volume"]
        }

    def set_category(self, category: str):
        if category.lower() not in CATEGORY_MAP:
            raise ValueError("Invalid category")

        self.payload["exchangeSegment"] = CATEGORY_MAP[category.lower()]
        return self

    def set_index(self, index: str):
        if index.lower() not in INDEX_MAP:
            raise ValueError("Invalid index")

        self.payload["securityId"] = INDEX_MAP[index.lower()]
        if(self.payload["securityId"] in [51,69]):
            self.payload["exchangeSegment"] = "BSE_FNO"
        return self

    def set_expiry(self, expiry_date: str | None):
        expiry_flag, expiry_code = resolve_expiry(expiry_date)
        self.payload["expiryFlag"] = expiry_flag
        self.payload["expiryCode"] = expiry_code
        return self

    def set_option_type(self, option_type: str):
        self.payload["drvOptionType"] = option_type
        return self

    def set_dates(self, from_date: str, to_date: str):
        self.payload["fromDate"] = from_date
        self.payload["toDate"] = to_date
        return self

    def build(self):
        print(self.payload)
        return self.payload


# ==========================================================
# API CLIENT
# ==========================================================

class DhanApiClient:

    def __init__(self, config: DhanConfig):
        self.config = config

    def post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(
            DhanConfig.BASE_URL,
            headers=self.config.headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"Dhan API Error: {response.text}")
        print("response.json() --> len : ", len(str(response.json())))
        return response.json()


# ==========================================================
# STRATEGY PATTERN
# ==========================================================

class OptionStrategy(ABC):

    def __init__(self, client: DhanApiClient):
        self.client = client

    @abstractmethod
    def fetch(
        self,
        category: str,
        index: str,
        expiry: str | None,
        from_date: str,
        to_date: str
    ) -> Dict[str, Any]:
        pass


class CallStrategy(OptionStrategy):

    def fetch(self, category, index, expiry, from_date, to_date):

        payload = (
            OptionPayloadBuilder()
            .set_category(category)
            .set_index(index)
            .set_expiry(expiry)
            .set_dates(from_date, to_date)
            .set_option_type("CALL")
            .build()
        )

        result = self.client.post(payload)
        return result["data"]["ce"]


class PutStrategy(OptionStrategy):

    def fetch(self, category, index, expiry, from_date, to_date):

        payload = (
            OptionPayloadBuilder()
            .set_category(category)
            .set_index(index)
            .set_expiry(expiry)
            .set_dates(from_date, to_date)
            .set_option_type("PUT")
            .build()
        )

        result = self.client.post(payload)
        return result["data"]["pe"]


# ==========================================================
# STRADDLE SERVICE
# ==========================================================

class StraddleService:

    def __init__(self, call_strategy: OptionStrategy, put_strategy: OptionStrategy):
        self.call_strategy = call_strategy
        self.put_strategy = put_strategy

    def fetch_straddle(
        self,
        category: str,
        index: str,
        expiry: str | None,
        from_date: str,
        to_date: str
    ) -> List[Dict]:

        ce_data = self.call_strategy.fetch(
            category, index, expiry, from_date, to_date
        )

        pe_data = self.put_strategy.fetch(
            category, index, expiry, from_date, to_date
        )

        ce_ts_map = {ts: idx for idx, ts in enumerate(ce_data["timestamp"])}
        pe_ts_map = {ts: idx for idx, ts in enumerate(pe_data["timestamp"])}

        common_timestamps = sorted(set(ce_ts_map.keys()) & set(pe_ts_map.keys()))

        candles = []

        for ts in common_timestamps:
            ci = ce_ts_map[ts]
            pi = pe_ts_map[ts]

            candles.append({
                "time": ts,

                "call": {
                    "open": ce_data["open"][ci],
                    "high": ce_data["high"][ci],
                    "low": ce_data["low"][ci],
                    "close": ce_data["close"][ci],
                    "volume": ce_data["volume"][ci]
                },

                "put": {
                    "open": pe_data["open"][pi],
                    "high": pe_data["high"][pi],
                    "low": pe_data["low"][pi],
                    "close": pe_data["close"][pi],
                    "volume": pe_data["volume"][pi]
                },

                "straddle": {
                    "open": ce_data["open"][ci] + pe_data["open"][pi],
                    "high": ce_data["high"][ci] + pe_data["high"][pi],
                    "low": ce_data["low"][ci] + pe_data["low"][pi],
                    "close": ce_data["close"][ci] + pe_data["close"][pi],
                    "volume": ce_data["volume"][ci] + pe_data["volume"][pi]
                }
            })

        return candles

# ==========================================================
# STRATEGY FACTORY
# ==========================================================

class StrategyFactory:

    @staticmethod
    def create(option_type: str, client: DhanApiClient) -> OptionStrategy:

        if option_type.upper() == "CALL":
            return CallStrategy(client)

        elif option_type.upper() == "PUT":
            return PutStrategy(client)

        else:
            raise ValueError("Invalid option type")