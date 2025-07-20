
import os
import requests

def fetch_trades():
    url = "https://api.dhan.co/trades"
    headers = {
        "access-token": os.getenv("DHAN_ACCESS_TOKEN"),
        "client-id": os.getenv("DHAN_CLIENT_ID")
    }

    try:
        resp = requests.get(url, headers=headers)
        print("Status Code:", resp.status_code)

        data = resp.json()
        print("Raw /trades response:", data)

        if not isinstance(data, list):
            raise Exception(f"Expected list of trades, got: {type(data)}")

        trades = []
        for t in data:
            if t.get("orderId") is None:
                continue
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
        print("Exception:", e)
        raise Exception(f"Error processing /trades response: {str(e)}")
