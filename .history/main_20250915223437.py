from datetime import datetime
import random, time, traceback

from app.market_parser import MarketDataParser, SplitMarketDataParser
from app.logger import setup_logger
from app.utils import Helper
from app.config import CONFIG

config = CONFIG
# df  = Helper.read_file(r"docs\nse.txt")

logger = setup_logger(name="market_data", log_dir="logs")

def generate_fake_entry(exchange, symbol):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_price = round(random.uniform(100, 1500), 2)
    ask_price = round(last_price + random.uniform(0.1, 5), 2)
    bid_price = round(last_price - random.uniform(0.1, 5), 2)
    prev_close = round(last_price - random.uniform(1, 10), 2)
    volume = random.randint(100, 100000)
    ask_qty = random.randint(1, 500)
    bid_qty = random.randint(1, 500)
    trades = random.randint(1, 100)
    wap = round((ask_price + bid_price) / 2, 2)

    entry = (
        f"T||0||{exchange}||1||{symbol}||"
        f"302={last_price}~300={ask_price}~301={bid_price}~304={prev_close}~"
        f"3={trades}~5939=TRADING~100={volume}~2={bid_price}~10={timestamp}~"
        f"6={ask_qty}~7={bid_qty}~118={wap}"
    )
    return entry

nse_symbols = [
    "SYMBIOX$.NS", "CCLPROD.NS", "MARKPHAR.NS", "SIGMSOLV.NS", "OMAXAUTO.BEN.NS",
    "ATISHAY$.NS", "MORATEXT.BZN.NS", "SILKPOLY.SMN.NS", "INFY.NS", "RELIANCE.NS"
]

bse_symbols = [
    "BRAISOLU.BS", "INDRMEDI.BS", "WHIRINDI.BS", "ASTEDM.BS", "CESC.BS",
    "TCS.BS", "HDFCBANK.BS", "MARUTI.BS", "ITC.BS", "SBIN.BS"
]


parser = MarketDataParser(config)

try:
    logger.notice("Program Has Started.")
    # parser = MarketDataParser(config)
    parser = SplitMarketDataParser(config) 
    while True:
        symbol = random.choice(nse_symbols)
        fake_entry = generate_fake_entry("NS", symbol)
        logger.trace(fake_entry)
        parser.process_ticker(fake_entry)
        time.sleep(0.05)
except Exception as e:
    logger.error(f"{type(e)}:{e}")
except KeyboardInterrupt:
    logger.warning("\nSimulation stopped.")