
import os
import requests

def fetch_trades():
    url = "https://api.dhan.co/orders/trade"
    headers = {
        "access-token": os.getenv("DHAN_ACCESS_TOKEN"),
        "client-id": os.getenv("DHAN_CLIENT_ID")
    }

    print("Fetching trades with headers:", headers)

    response = requests.get(url, headers=headers)
    print("Response Code:", response.status_code)
    print("Response Body:", response.text)

    if response.ok:
        try:
            data = response.json()
            if not isinstance(data, list):
                raise ValueError("Expected list of trades but got:", data)
            trades = []
            for t in data:
                trades.append({
                    "order_id": t.get("orderId"),
                    "symbol": t.get("securityId"),
                    "side": t.get("transactionType"),
                    "qty": t.get("filledQty"),
                    "price": t.get("averagePrice"),
                    "timestamp": t.get("orderTimestamp")
                })
            return trades
        except Exception as e:
            raise Exception(f"Invalid JSON format from Dhan: {e}")
    else:
        raise Exception(f"Dhan API error: {response.status_code} {response.text}")