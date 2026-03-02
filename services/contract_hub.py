import pandas as pd
from urllib.request import urlopen
from collections import defaultdict
from datetime import date
import os
import json
from constants.constant import BASE_DIR, HUB_FILE_PATH, CSV_URL , INDEX_SYMBOLS

FILE_PATH = HUB_FILE_PATH
print(FILE_PATH)
print(BASE_DIR)



# THis is for frtch --> read --> store JSON --> return dict
class contract_hub:

    CSV_URL = CSV_URL
    INDEX_SYMBOLS = list(INDEX_SYMBOLS.keys())

    def __init__(self):
        self.df = None
        self.index_data = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(dict)
            )
        )

    # -----------------------------------------
    # Step 1: Load CSV
    # -----------------------------------------
    def load_csv(self):
        with urlopen(self.CSV_URL, timeout=20) as response:
            self.df = pd.read_csv(response, low_memory=False)

    # -----------------------------------------
    # Step 2: Build Structure (Only Min Expiry)
    # -----------------------------------------
    def build_structure(self):

        if self.df is None:
            raise ValueError("Load CSV first")

        # Store minimum expiry per index
        min_expiry = {}

        # ---------- First Pass ----------
        for _, row in self.df.iterrows():

            if row["SEM_INSTRUMENT_NAME"] != "OPTIDX":
                continue

            trading_symbol = str(row["SEM_TRADING_SYMBOL"]).upper()
            index_name = trading_symbol.split("-")[0]

            if index_name not in self.INDEX_SYMBOLS:
                continue

            expiry = pd.to_datetime(row["SEM_EXPIRY_DATE"]).date()

            if index_name not in min_expiry:
                min_expiry[index_name] = expiry
            else:
                if expiry < min_expiry[index_name]:
                    min_expiry[index_name] = expiry

        # ---------- Second Pass ----------
        for _, row in self.df.iterrows():

            if row["SEM_INSTRUMENT_NAME"] != "OPTIDX":
                continue

            trading_symbol = str(row["SEM_TRADING_SYMBOL"]).upper()
            index_name = trading_symbol.split("-")[0]

            if index_name not in self.INDEX_SYMBOLS:
                continue

            expiry = pd.to_datetime(row["SEM_EXPIRY_DATE"]).date()

            # Only include nearest expiry
            if expiry != min_expiry[index_name]:
                continue

            strike = int(float(row["SEM_STRIKE_PRICE"]))
            option_type = row["SEM_OPTION_TYPE"]
            security_id = row["SEM_SMST_SECURITY_ID"]

            self.index_data[index_name][str(expiry)][strike][option_type] = str(security_id)
        print("INDEX",self.index_data)
        return self.index_data




def load_or_build():

    today = str(date.today())

    # If file exists → try loading
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            payload = json.load(f)

        if payload.get("date") == today:
            print("Loaded etc/hub.json structure from JOSN FILE")
            return payload["data"]

        else:
            print("File outdated. Rebuilding...")

    # Otherwise build fresh
    builder = contract_hub()
    builder.load_csv()
    data = builder.build_structure()

    # Convert defaultdict → normal dict
    def convert(obj):
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        return obj

    payload = {
        "date": today,
        "data": convert(data)
    }

    # Save file
    with open(FILE_PATH, "w") as f:
        json.dump(payload, f, indent=4)

    print("Built and saved new etc/hub.json structure")

    return payload["data"]

hub_dict = load_or_build()
