
import os
import requests
from datetime import datetime, timedelta

def fetch_trades_combined():
    headers = {
        "access-token": os.getenv("DHAN_ACCESS_TOKEN")
    }
    all_trades = []
    today = datetime.today()

    # === Pull last 30 days from /trades?date=
    for i in range(0, 30):
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"https://api.dhan.co/trades?date={date_str}"
        try:
            resp = requests.get(url, headers=headers)
            print(f"[v2] {date_str} /trades: {resp.status_code}")
            data = resp.json()
            if isinstance(data, list):
                for t in data:
                    if t.get("orderId") is None:
                        continue
                    all_trades.append({
                        "order_id": t.get("orderId"),
                        "symbol": t.get("securityId"),
                        "side": t.get("transactionType"),
                        "qty": t.get("tradedQuantity"),
                        "price": t.get("tradedPrice"),
                        "timestamp": t.get("exchangeTime") or t.get("createTime")
                    })
        except Exception as e:
            print(f"Error on v2 {date_str}: {e}")

    # === Pull from /tradeHistory using v1 (loop pages)
    for i in range(0, 60):  # last 60 days
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for page in range(1, 6):  # max 5 pages/day
            url = f"https://api.dhan.co/tradeHistory/{date_str}/{date_str}/{page}"
            try:
                resp = requests.get(url, headers=headers)
                print(f"[v1] {date_str} page {page} /tradeHistory: {resp.status_code}")
                data = resp.json()
                if isinstance(data, list) and len(data) > 0:
                    for t in data:
                        if t.get("orderId") is None or t.get("exchangeSegment") != "NSE_FNO":
                            continue
                        all_trades.append({
                            "order_id": t.get("orderId") + "_v1",  # avoid collision
                            "symbol": t.get("securityId"),
                            "side": t.get("transactionType"),
                            "qty": t.get("tradedQuantity"),
                            "price": t.get("tradedPrice"),
                            "timestamp": t.get("exchangeTime") or t.get("createTime")
                        })
                else:
                    break
            except Exception as e:
                print(f"Error on v1 {date_str} page {page}: {e}")
                break

    return all_trades
