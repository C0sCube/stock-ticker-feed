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
        
        
    
    def parse_ticker(self,tick):
        parts = tick.strip().split("||")
        if len(parts) < 6:
            return None, {}

        # T||0||NS||1||CCLPROD.NS||4=905.00~6=66~5=906.20~7=5~2=905.00~~3=1~100=348~5620=A~302=905.00~300=905.00~301=905.00~304=902.55~5939=TRADING~118=905.00~18=314940.000000
        symbol = parts[4]    
        kv_string = parts[-1] 

        kv_pairs = [kv.split("=", 1) for kv in kv_string.split("~") if "=" in kv]
        field_map = {k: v for k, v in kv_pairs}

        return symbol, field_map
    
    def extract_ports(self, ticker):
        symbol, field_map = parse_ticker_line(ticker)
        if not symbol:
            return []

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

        return data_set


