
import os
import requests
from datetime import datetime, timedelta

def fetch_trades():
    headers = {
        "access-token": os.getenv("DHAN_ACCESS_TOKEN"),
        "client-id": os.getenv("DHAN_CLIENT_ID")
    }

    all_trades = []
    today = datetime.today()

    for i in range(0, 60):  # Look back 60 days
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"https://api.dhan.co/trades?date={date_str}"

        try:
            resp = requests.get(url, headers=headers)
            print(f"Fetching trades for {date_str} - Status {resp.status_code}")
            data = resp.json()
            if not isinstance(data, list):
                continue

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
            print(f"Error on {date_str}: {e}")
            continue

    return all_trades
