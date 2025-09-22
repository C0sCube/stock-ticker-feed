import random
import time
import traceback
from datetime import datetime

from app.market_parser import SplitMarketDataParser
from app.logger import setup_logger
from app.constants import CONFIG, LOG_DIR


# --- Fake data generator ---
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
    turnover = round(last_price * volume, 6)

    if exchange == "BS":
        return (
            f"T||0||{exchange}||1||{symbol}||"
            f"302={last_price}~300={ask_price}~301={bid_price}~304={prev_close}~"
            f"3={trades}~5939=TRADING~100={volume}~2={bid_price}~10={timestamp}~"
            f"6={ask_qty}~7={bid_qty}~118={wap}~18={turnover}"
        )
    elif exchange == "NS":
        return (
            f"T||0||{exchange}||1||{symbol}||"
            f"4={last_price}~6={ask_qty}~5={ask_price}~7={bid_qty}~"
            f"2={bid_price}~10={timestamp}~3={trades}~100={volume}~"
            f"304={prev_close}~5939=TRADING~118={wap}~18={turnover}"
        )
    else:
        raise ValueError(f"Unknown exchange: {exchange}")


# --- Demo symbols ---
NSE_SYMBOLS = [
    "SYMBIOX$.NS", "CCLPROD.NS", "MARKPHAR.NS", "SIGMSOLV.NS", "OMAXAUTO.BEN.NS",
    "ATISHAY$.NS", "MORATEXT.BZN.NS", "SILKPOLY.SMN.NS", "INFY.NS", "RELIANCE.NS"
]

BSE_SYMBOLS = [
    "BRAISOLU.BS", "INDRMEDI.BS", "WHIRINDI.BS", "ASTEDM.BS", "CESC.BS",
    "TCS.BS", "HDFCBANK.BS", "MARUTI.BS", "ITC.BS", "SBIN.BS"
]


# --- Main simulation loop ---
def main():
    logger = setup_logger(name="market_data", log_dir=LOG_DIR)
    logger.notice("Program Started (Fake Tick Simulator)")

    parser = SplitMarketDataParser(CONFIG, logger, exchange="NSE")

    try:
        while True:
            symbol = random.choice(NSE_SYMBOLS)
            fake_entry = generate_fake_entry("NS", symbol)

            parser.process_ticker(fake_entry)
            time.sleep(0.02)  # 50 ticks/sec

    except KeyboardInterrupt:
        logger.warning("Simulation stopped by user")

    except Exception as e:
        logger.exception(f"Unhandled error: {type(e).__name__}: {e}")

    finally:
        parser.flush_all_data()
        logger.notice("Program Ended, buffered data flushed.")


if __name__ == "__main__":
    main()
