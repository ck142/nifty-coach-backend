import os
import requests

def fetch_trades():
    url = "https://api.dhan.co/trades"
    headers = {
        "access-token": os.getenv("DHAN_ACCESS_TOKEN"),
        "client-id": os.getenv("DHAN_CLIENT_ID")
    }

    try:
        response = requests.get(url, headers=headers)
        print("Status Code:", response.status_code)

        data = response.json()
        print("Raw /trades response:", data)

        if not isinstance(data, list):
            raise ValueError(f"Expected list of trades but got: {type(data)}")

        trades = []
        for t in data:
            trades.append({
                "order_id": t.get("orderId"),
                "symbol": t.get("securityId"),
                "side": t.get("transactionType"),
                "qty": t.get("tradedQuantity"),
                "price": t.get("tradedPrice"),
                "timestamp": t.get("exchangeTime") or t.get("createTime")
            })
        return trades

    except Exception as e:
        raise Exception(f"Error processing /trades response: {str(e)}")
