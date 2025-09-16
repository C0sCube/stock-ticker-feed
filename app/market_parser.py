import os, re
from app.utils import Helper
from app.constants import CONFIG, OUTPUT_DIR

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
    def __init__(self, config, logger, exchange="NSE",bin_size = 60, thread_id = None):
        self.ports = config["NSE_PORTS"] if exchange == "NSE" else config["BSE_PORTS"]
        # self.header = config.get("CSV_HEADER")
        self.symbol_set = set()
        self.logger = logger
        self.tick_bin = dict()
        self.bin_size = bin_size
        
        self.thread_id = thread_id

    def extract_ports(self, ticker: str):
            ticker_sections = ticker.strip().split("||")
            if len(ticker_sections) < 6:
                return None, []

            symbol, field_values = ticker_sections[4], ticker_sections[-1]

            kv_pairs = [kv.split("=", 1) for kv in field_values.split("~") if "=" in kv]
            field_map = {k: v for k, v in kv_pairs}

            data_set = []
            for port_name, port_val in self.ports.items():
                if port_name == "DATETIME":
                    value = field_map.get(port_val, "")
                    if value and " " in value:
                        date, time_ = value.split(" ", 1)
                        value = f"{date},{time_}"
                    else:
                        value = "," #date,time
                else:
                    value = field_map.get(port_val, "")
                data_set.append(value)

            return symbol, data_set

    def process_ticker(self, ticker: str):
            symbol, data = self.extract_ports(ticker)
            if not symbol or not data:
                return

            data_row = ",".join(data)
            save_data = f"{symbol},{data_row}\n"

            if symbol not in self.tick_bin:
                self.tick_bin[symbol] = []

            self.tick_bin[symbol].append(save_data)

            if len(self.tick_bin[symbol]) >= self.bin_size:
                self.flush_tick_data(symbol)

    def flush_tick_data(self, symbol):
        
        filename =f"{symbol}-worker{self.thread_id}.csv" if self.thread_id else f"{symbol}.csv"
        path = os.path.join(OUTPUT_DIR,filename)
        flush_data = self.tick_bin.get(symbol, [])
        if flush_data:
            with open(path, mode="a", encoding="utf-8") as f:
                f.writelines(flush_data)
            self.tick_bin[symbol].clear()

    def flush_all_data(self):
        for symbol in list(self.tick_bin.keys()):
            self.flush_tick_data(symbol)
        
    def map_symbol_data(self,):
        pass


