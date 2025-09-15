import re,os, time
from datetime import datetime
from app.utils import Helper

class MarketDataParser:
    def __init__(self, config):
        self.ports = config["NSE_PORTS"]
        self.header = config.get("CSV_HEADER")
        self.nse_regex = config.get("NSE_REGEX")
        self.symbol_set = set()
        self.today = datetime.now().strftime("%Y%m%d")
        self.save_path = self.today
        Helper.create_dir(self.save_path)

    def extract_symbol(self, ticker):
        match = re.findall("\\|\\|([0-9A-Z$\\.]+\\.NS)\\b", ticker, re.IGNORECASE)
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
            
            print(f"{port_name}:{value}")
            data_set.append(value)
                
        return data_set

    def process_ticker(self, ticker):
        symbol = self.extract_symbol(ticker)
        # mapping of symbol ...
        
        if not symbol:
            return
        data = self.extract_ports(ticker)
        data_csv = ",".join(data) + "\n"
        
        symbol_path = os.path.join(self.save_path, f"{symbol}.csv")
        if not os.path.exists(symbol_path):
            Helper.write_file(symbol_path, self.header,mode="a")
        Helper.write_file(symbol_path, data_csv,"a")