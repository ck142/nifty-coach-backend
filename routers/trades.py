from fastapi import APIRouter
from db import save_trade_to_db, get_all_trades
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
    # Get all trades using helper from db.py
    trades = get_all_trades(limit=500)
    return trades
