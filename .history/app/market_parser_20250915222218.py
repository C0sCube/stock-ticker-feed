import os, re
from app.utils import Helper
from app.config import CONFIG, OUTPUT_DIR

class MarketDataParser:
    def __init__(self):
        self.ports = CONFIG["NSE_PORTS"]
        self.header = CONFIG.get("CSV_HEADER")
        self.symbol_set = set()

    def extract_symbol(self, ticker):
        regex = CONFIG["NSE_REGEX"]["SYMBOL_REGEX"]
        match = re.findall(regex, ticker, re.IGNORECASE)
        if match:
            symbol = match[0]
            self.symbol_set.add(symbol)
            return symbol
        return None

    def extract_ports(self, ticker):
        data_set = []
        for port_name, port_val in self.ports.items():
            if port_name == "DATETIME":
                regex = fr"\b{port_val}=(\d{{4}}-\d{{2}}-\d{{2}})\s(\d{{2}}:\d{{2}}:\d{{2}})~"
            else:
                regex = fr"\b{port_val}=(\d+\.?\d*)~"

            match = re.findall(regex, ticker, re.IGNORECASE)
            if match:
                value = match[0]
                value = ",".join(value) if isinstance(value, tuple) else value
            else:
                value = "N/A,N/A" if port_name == "DATETIME" else "N/A"
            data_set.append(value)

        return data_set

    def process_ticker(self, ticker):
        symbol = self.extract_symbol(ticker)
        if not symbol:
            return

        data = self.extract_ports(ticker)
        data_csv = ",".join(data) + "\n"

        symbol_path = os.path.join(OUTPUT_DIR, f"{symbol}.csv")
        if not os.path.exists(symbol_path):
            Helper.write_file(symbol_path, self.header, mode="a")
        Helper.write_file(symbol_path, data_csv, "a")
        
        

class SplitMarketDataParser:
    def __init__(self, config):
        self.ports = config["NSE_PORTS"]
        self.header = config.get("CSV_HEADER")
        self.symbol_set = set()

    def extract_ports(self, ticker: str):
        
        parts = ticker.strip().split("||")
        if len(parts) < 6:
            return None, []

        symbol = parts[4]
        kv_string = parts[-1]

        kv_pairs = [kv.split("=", 1) for kv in kv_string.split("~") if "=" in kv]
        field_map = {k: v for k, v in kv_pairs}

        if "6840" in field_map:
            log().notice(f"Meta line → {symbol} group={field_map['6840']}")
            return None, []

        # port-data to extract
        data_set = []
        for port_name, port_val in self.ports.items():
            if port_name == "DATETIME":
                value = field_map.get(port_val, "N/A")
                if value != "N/A" and " " in value:
                    date, time_ = value.split(" ", 1)
                    value = f"{date},{time_}"
                else:
                    value = "N/A,N/A"
            else:
                value = field_map.get(port_val, "N/A")
            data_set.append(value)

        return symbol, data_set

    def process_ticker(self, ticker: str):
        symbol, data = self.extract_ports(ticker)
        if not symbol or not data:
            return

        row = ",".join(data) + "\n"
        symbol_path = os.path.join(OUTPUT_DIR, f"{symbol}.csv")

        if not os.path.exists(symbol_path):
            Helper.write_file(symbol_path, self.header, mode="a")

        Helper.write_file(symbol_path, row, "a")
        log().debug(f"Saved row for {symbol}: {row.strip()}")


