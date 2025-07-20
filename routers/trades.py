
from fastapi import APIRouter
from db import SessionLocal, Trade
from datetime import datetime, timedelta
import os
from dhanhq import dhanhq

router = APIRouter()

ACCESS_TOKEN = os.environ.get("DHAN_TOKEN")
CLIENT_ID = os.environ.get("DHAN_CLIENT_ID")

dhan = dhanhq(ACCESS_TOKEN, CLIENT_ID)

def fetch_trade_history_from_sdk():
    session = SessionLocal()
    new_trades = 0
    total_fetched = 0

    today = datetime.now().date()
    from_date = today - timedelta(days=14)
    try:
        trades = dhan.get_trade_history(str(from_date), str(today))
    print(f"[INFO] Got trades raw type: {type(trades)}")
    print(f"[DEBUG] Raw trades response: {trades}")
        total_fetched = len(trades)
    except Exception as e:
        print(f"[ERROR] Failed to fetch from SDK: {e}")
        return 0, 0

    for trade in trades:
        try:
            oid = f"{trade.get('orderId')}_v12"
            if session.query(Trade).filter_by(order_id=oid).first():
                continue
            t = Trade(
                order_id=oid,
                symbol=trade.get("tradingSymbol"),
                side=trade.get("transactionType"),
                qty=int(trade.get("quantity", 0) or 0),
                price=float(trade.get("price", 0) or 0.0),
                timestamp=datetime.strptime(trade.get("exchangeTime"), "%Y-%m-%dT%H:%M:%S") if trade.get("exchangeTime") else datetime.utcnow()
            )
            session.add(t)
            new_trades += 1
        except Exception as e:
            print(f"[ERROR] Skipping trade due to: {e}")

    session.commit()
    session.close()
    return new_trades, total_fetched

@router.post("/sync_trades")
def sync_trades():
    try:
        new, total = fetch_trade_history_from_sdk()
        return {"message": f"Pulled {total} trades, synced {new} new trades."}
    except Exception as e:
        return {"error": f"General error: {e}"}
