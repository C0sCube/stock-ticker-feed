import os, re, traceback
from datetime import datetime
from app.logger import get_logger
from app.sql_connector import fetch_symbol_mapping
from app.constants import CONFIG, OUTPUT_DIR
        
class SplitMarketDataParser:
    def __init__(
        self,
        # logger,
        output_path = "",
        exchange="NSE",
        bin_size = 30,
        add_extension = True,
    ):
        
        self.exchange = exchange
        
        self.ports = CONFIG["NSE_PORTS"] if exchange == "NSE" else CONFIG["BSE_PORTS"]
        self.header = CONFIG.get("CSV_HEADER","Ticker,Date,Time,Ltp,BuyPrice,BuyQty,SellPrice,SellQty,Ltq,OpenInterest")
        self.header_count = len(self.header.split(","))
        self.logger = get_logger()
        self.output_path = output_path
        
        if not output_path:
            self.logger.warning(f"SplitMarketDataParser.__init__ -> Output Path not passed. Defaulting..")
            self.output_path = OUTPUT_DIR
        self.logger.info(f"Files Being Saved to: {self.output_path}")

        
        # self.symbol_set = set()
        self.tick_bin = dict()
        self.bin_size = bin_size
        
        # self.thread_id = thread_id
        self.tick_content_size = 6
        self.symbol_index = 4
        # self.fill_null = "Nil"
        
        if add_extension:self.ext = CONFIG["INDEX_EXTENSIONS"].get(exchange, "")
        
        try:            
            symbol_map = fetch_symbol_mapping()
            if not symbol_map:
                self.logger.warning("SplitMarketDataParser.__init__ -> No symbol mapping found. Using default mapping.")
            self.symbol_mapper = symbol_map if symbol_map else CONFIG.get("NSE_SYMBOL_MAPPER", {})
            
        except KeyError as ke:
            self.logger.error(f"KeyError in SplitMarketDataParser.__init__: {ke}. Check CONFIG keys.")
            self.symbol_mapper = {}
            
        except Exception as e:
            self.logger.exception(f"Unexpected error in SplitMarketDataParser.__init__: {e}")
            self.symbol_mapper = {}
            
            
    # def extract_nfo_ports(self,ticker:str):
    #     other,ticker_sections = ticker.strip().split(";",1)
        
    #     _time,symbol = other.split("CPR")
        
    #     date = datetime.now().strftime("%y-%m-%d")
        
    #     kv_pairs = [kv.split("=",1) for kv in ticker_sections.split(";") if ";" in kv]
    #     field_map = {k: v.strip() for k, v in kv_pairs}
        
    #     data_set = [date,_time.strip()]
    #     for port_name,port_val in self.ports.items():
    #         value = field_map.get(port_val, "0") or "0"
    #         data_set.append(value)
        
    #     if all(i == "0" for i in data_set):
    #         self.logger.debug(f"Function: SplitMarketDataParser.export_ports -> Empty tick skipped: {ticker}")
    #         return None,[]
        
    #     return symbol.strip(), data_set
            
        
    def extract_ports(self, ticker: str):
       
        if self.exchange == "NSE":
            ticker_sections = ticker.strip().split("||")
            if len(ticker_sections) < self.tick_content_size: # self.tick_content_size = 6
                self.logger.debug(f"Function: SplitMarketDataParser.export_ports -> Malformed tick skipped: {ticker}")
                return None, []

            symbol, field_values = ticker_sections[self.symbol_index], ticker_sections[-1] # self.symbol_index = 4
            kv_pairs = [kv.split("=", 1) for kv in field_values.split("~") if "=" in kv]
            field_map = {k: v.strip() for k, v in kv_pairs}

            data_set = []
            for port_name, port_val in self.ports.items():
                if port_name == "DATETIME":
                    value = field_map.get(port_val, "")
                    if value and " " in value:
                        date, time_ = value.split(" ", 1)
                        # value = f"{date},{time_}"
                        
                    else:
                        date,time_ = "0","0" #value = "0,0"  # date,time fallback
                    
                    data_set.extend([date,time_])
                else:
                    value = field_map.get(port_val, "0") or "0"
                    # value = float(value)
                    data_set.append(value)
        
        if self.exchange == "NFO":
            other,ticker_sections = ticker.strip().split(";",1)
            _time,symbol = other.split("CPR") 
            date = datetime.now().strftime("%y-%m-%d")
            
            kv_pairs = [kv.split("=",1) for kv in ticker_sections.split(";") if ";" in kv]
            field_map = {k: v.strip() for k, v in kv_pairs}
            
            data_set = [date,_time.strip()]
            for port_name,port_val in self.ports.items():
                value = field_map.get(port_val, "0") or "0"
                data_set.append(value)  
        
        
        #Check if the tick is completely empty or not
        if all(i == "0" for i in data_set):
            self.logger.debug(f"Function: SplitMarketDataParser.export_ports -> Empty tick skipped: {ticker}")
            return None,[]
        
        return symbol.strip(), data_set

    def symbol_operations(self, _symbol):
        try:
            mapped = self.symbol_mapper.get(_symbol, "")
            if not mapped:
                self.logger.debug(f"Symbol mapping not found for {_symbol} ,using original.")
                return _symbol.strip()

            if isinstance(self.ext, str) and self.ext:
                mapped = f"{mapped}.{self.ext}"

            self.logger.debug(f"Symbol mapped: {_symbol} -> {mapped}")
            return mapped.strip()

        except Exception as e:
            self.logger.warning(f"symbol_operations error: {type(e).__name__}: {e}")
            self.logger.debug(traceback.format_exc())
            return _symbol.strip()
    
    def process_ticker(self, ticker: str):
        symbol, data = self.extract_ports(ticker)
        if not symbol or not data:
            return

        _symbol = self.symbol_operations(symbol)
        # _symbol = symbol
            
        #checker for unique symbol
        if _symbol not in self.tick_bin:
            self.tick_bin[_symbol] = [self.header + "\n"] #header added
            
        data_row = ",".join(data)
        save_data = f"{_symbol},{data_row}\n"

        self.tick_bin[_symbol].append(save_data)
        # self.logger.trace(f"Added data for {symbol}: {save_data}")

        if len(self.tick_bin[_symbol]) >= self.bin_size:
            self.flush_tick_data(_symbol)
        
        
        # if symbol in ["RELINDUS.NS","TATASTEE.NS","AXISBANK.NS","INFO.NS","HDFCBANK.NS"]:
        #     if symbol not in self.tick_bin:
        #         self.tick_bin[symbol] = []

        #     self.tick_bin[symbol].append(save_data)
        #     self.logger.trace(f"Appended data for {symbol}: {save_data}")

        #     if len(self.tick_bin[symbol]) >= self.bin_size:
        #         self.flush_tick_data(symbol)

    def flush_tick_data(self, symbol):
        
        filename =f"{symbol}.csv" #f"{symbol}-worker{self.thread_id}.csv" if self.thread_id else f"{symbol}.csv"
        path = os.path.join(self.output_path,filename)
        flush_data = self.tick_bin.get(symbol, [])
        if flush_data:
            with open(path, mode="a", encoding="utf-8") as f:
                f.writelines(flush_data)
            self.tick_bin[symbol].clear()

    def flush_all_data(self):
        for symbol in list(self.tick_bin.keys()):
            self.flush_tick_data(symbol)    
        self.logger.info("Flushed all parsed data successfully.")
        
    # def map_symbol_data(self,):
    #     pass


# class MarketDataParser:
#     def __init__(self):
#         self.ports = CONFIG["NSE_PORTS"]
#         self.header = CONFIG.get("CSV_HEADER")
#         self.symbol_set = set()

#     def extract_symbol(self, ticker):
#         regex = CONFIG["NSE_REGEX"]["SYMBOL_REGEX"]
#         match = re.findall(regex, ticker, re.IGNORECASE)
#         if match:
#             symbol = match[0]
#             self.symbol_set.add(symbol)
#             return symbol
#         return None

#     def extract_ports(self, ticker):
#         data_set = []
#         for port_name, port_val in self.ports.items():
#             if port_name == "DATETIME":
#                 regex = fr"\b{port_val}=(\d{{4}}-\d{{2}}-\d{{2}})\s(\d{{2}}:\d{{2}}:\d{{2}})~"
#             else:
#                 regex = fr"\b{port_val}=(\d+\.?\d*)~"

#             match = re.findall(regex, ticker, re.IGNORECASE)
#             if match:
#                 value = match[0]
#                 value = ",".join(value) if isinstance(value, tuple) else value
#             else:
#                 value = "N/A,N/A" if port_name == "DATETIME" else "N/A"
#             data_set.append(value)

#         return data_set

#     def process_ticker(self, ticker):
#         symbol = self.extract_symbol(ticker)
#         if not symbol:
#             return

#         data = self.extract_ports(ticker)
#         data_csv = ",".join(data) + "\n"

#         symbol_path = os.path.join(OUTPUT_DIR, f"{symbol}.csv")
#         if not os.path.exists(symbol_path):
#             Helper.write_file(symbol_path, self.header, mode="a")
#         Helper.write_file(symbol_path, data_csv, "a")
        