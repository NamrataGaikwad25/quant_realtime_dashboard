import json
import threading
import websocket
import time
from database import get_connection, create_table
from utils.config import BINANCE_WS

create_table()

def on_message(ws, message):
    data = json.loads(message)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO ticks VALUES (?, ?, ?, ?)",
        (
            int(data["E"]),
            data["s"],
            float(data["p"]),
            float(data["q"])
        )
    )
    conn.commit()
    conn.close()

def start_stream(symbol):
    stream = f"{symbol}@trade"
    ws = websocket.WebSocketApp(
        f"{BINANCE_WS}/{stream}",
        on_message=on_message
    )
    ws.run_forever()

def run_ingestion(symbols):
    for sym in symbols:
        t = threading.Thread(target=start_stream, args=(sym,))
        t.daemon = True
        t.start()
