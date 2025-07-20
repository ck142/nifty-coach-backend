
from fastapi import APIRouter
from db import SessionLocal, Trade
import requests
from datetime import datetime
import os

router = APIRouter()

DHAN_BASE = "https://api.dhan.co"
TOKEN = os.environ.get("DHAN_TOKEN")
CLIENT_ID = os.environ.get("DHAN_CLIENT_ID")

HEADERS = {
    "access-token": TOKEN,
    "client-id": CLIENT_ID
}

def fetch_trade_history_from_orders():
    session = SessionLocal()
    new_trades = 0
    total_orders = 0

    url = f"{DHAN_BASE}/orders"
    
    response = requests.get(url, headers=HEADERS)
    print(f"[DEBUG] access-token: {HEADERS.get('access-token')}")
    print(f"[DEBUG] client-id: {HEADERS.get('client-id')}")
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch /orders: {response.status_code}")
        print(response.text)
        return new_trades, total_orders

    try:
        orders = response.json()
    except Exception as e:
        print(f"[ERROR] Could not decode /orders JSON: {e}")
        return new_trades, total_orders

    print(f"[INFO] Pulled {len(orders)} orders")
    total_orders = len(orders)

    for order in orders:
        try:
            status = order.get("orderStatus")
            if status not in ["TRADED", "EXECUTED", "COMPLETED"]:
                continue

            oid = f"{order.get('orderId')}_vOrders"
            if session.query(Trade).filter_by(order_id=oid).first():
                continue

            t = Trade(
                order_id=oid,
                symbol=order.get("tradingSymbol"),
                side=order.get("transactionType"),
                qty=int(order.get("quantity", 0) or 0),
                price=float(order.get("price", 0) or 0.0),
                timestamp=datetime.strptime(order.get("exchangeTime"), "%Y-%m-%dT%H:%M:%S") if order.get("exchangeTime") else datetime.utcnow()
            )
            session.add(t)
            new_trades += 1
        except Exception as e:
            print(f"[ERROR] Skipping order due to: {e}")

    session.commit()
    session.close()
    return new_trades, total_orders

@router.post("/sync_trades")
def sync_trades():
    try:
        new, total = fetch_trade_history_from_orders()
        return {"message": f"Pulled {total} orders, synced {new} new trades."}
    except Exception as e:
        return {"error": f"General error: {e}"}
