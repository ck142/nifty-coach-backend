
import os
import requests

def fetch_trades():
    url = "https://api.dhan.co/orders/trade"
    headers = {
        "access-token": os.getenv("DHAN_ACCESS_TOKEN"),
        "client-id": os.getenv("DHAN_CLIENT_ID")
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        trades = []
        for t in data:
            trades.append({
                "order_id": t["orderId"],
                "symbol": t["securityId"],
                "side": t["transactionType"],
                "qty": t["filledQty"],
                "price": t["averagePrice"],
                "timestamp": t["orderTimestamp"]
            })
        return trades
    else:
        return []
