import mysql.connector, traceback
from app.constants import DB_CONFIG, SP_CONFIG
from app.logger import get_logger

logger = get_logger()

def fetch_symbol_mapping(db_config = DB_CONFIG, sp_config = SP_CONFIG):
    
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.callproc(sp_config["name"], sp_config["params"])

        mapping = {}
        for result in cursor.stored_results():
            rows = result.fetchall()
            columns = result.column_names
            for row in rows:
                record = dict(zip(columns, row))
                cogencis = record.get("cogencis_symbol")
                exchange = record.get("exchange_symbol")
                if cogencis and exchange:
                    mapping[cogencis] = exchange

        cursor.close()
        conn.close()
    except Exception as e:
        logger.warning(f"fetch_symbol_mapping error: {type(e).__name__}: {e}")
        logger.info(f" SP didnt work returning empty mapper")
        logger.debug(traceback.format_exc())
        return {}

    return mapping