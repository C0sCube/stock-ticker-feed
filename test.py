import mysql.connector
import json
from app.constants import DB_CONFIG

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.callproc("WS_get_exchange_mapping_symbol", ("NS", None, None))

for result in cursor.stored_results():
    rows = result.fetchall()
    columns = result.column_names
    data = [dict(zip(columns, row)) for row in rows]
    json_output = json.dumps(data, indent=2)

    # Save to file
    with open('exchange_mapping.json', 'w') as f:
        f.write(json_output)

cursor.close()
conn.close()