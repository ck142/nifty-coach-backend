from fastapi import APIRouter
from db import SessionLocal, Trade
import requests
from datetime import datetime, timedelta
import os

router = APIRouter()

DHAN_BASE = "https://api.dhan.co"
TOKEN = os.environ.get("DHAN_TOKEN")
CLIENT_ID = os.environ.get("DHAN_CLIENT_ID")

HEADERS = {
    "access-token": TOKEN,
    "client-id": CLIENT_ID
}

def fetch_trade_history_v1():
    session = SessionLocal()
    new_trades = 0
    total_pulled = 0
    today = datetime.now().date()
    from_date = today - timedelta(days=14)
    to_date = today

    for date_offset in range((to_date - from_date).days + 1):
        date = from_date + timedelta(days=date_offset)
        for page in range(1, 6):
            url = f"{DHAN_BASE}/history/tradeHistory/{date}/{date}/{page}"
            response = requests.get(url, headers=HEADERS)
            print(f"[DEBUG] {url} → {response.status_code}")
            print(f"[DEBUG] Response Text: {response.text}")

            if response.status_code == 404:
                print(f"[INFO] No more pages for {date} after page {page - 1}")
                break
            if response.status_code != 200:
                print(f"[ERROR] {url}: {response.status_code}")
                continue

            try:
                data = response.json()
                print(f"[{date}] Page {page}: {len(data)} trades")
                total_pulled += len(data)
            except Exception as e:
                print(f"[ERROR] JSON decode failed: {e}")
                continue

            for trade in data:
                try:
                    oid = f"{trade.get('orderId')}_v1"
                    if session.query(Trade).filter_by(order_id=oid).first():
                        continue
                    t = Trade(
                        order_id=oid,
                        symbol=trade.get("tradingSymbol"),
                        side=trade.get("transactionType"),
                        qty=int(trade.get("quantity", 0) or 0),
                        price=float(trade.get("price", 0) or 0.0),
                        timestamp=datetime.strptime(
                            trade.get("exchangeTime"),
                            "%Y-%m-%dT%H:%M:%S"
                        ) if trade.get("exchangeTime") else datetime.utcnow()
                    )
                    session.add(t)
                    new_trades += 1
                except Exception as e:
                    print(f"[ERROR] Skipping trade due to: {e}")

        session.commit()
    session.close()
    return new_trades, total_pulled

@router.post("/sync_trades")
def sync_trades():
    try:
        new_v1, pulled_v1 = fetch_trade_history_v1()
        return {"message": f"Pulled {pulled_v1} trades, synced {new_v1} new trades."}
    except Exception as e:
        return {"error": f"General error: {e}"}
