
from fastapi import APIRouter
from db import save_trade_to_db
from datetime import datetime
import random

router = APIRouter()

@router.post("/sync_trades")
def sync_trades():
    # Dummy trade data for simulation
    dummy_trades = [
        {
            "order_id": f"{random.randint(10000, 99999)}",
            "symbol": "NIFTY25JUL18400CE",
            "side": "BUY",
            "qty": 75,
            "price": round(random.uniform(20, 300), 2),
            "timestamp": datetime.now()
        }
        for _ in range(3)
    ]

    new_count = 0
    for trade in dummy_trades:
        if save_trade_to_db(trade):
            new_count += 1

    return {"message": f"Synced {new_count} new trades.", "trades": dummy_trades}

@router.get("/get_trades")
def get_trades():
    from db import get_db_connection
    from psycopg2.extras import RealDictCursor

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM trades ORDER BY timestamp DESC LIMIT 500;")
    trades = cursor.fetchall()
    conn.close()
    return trades
