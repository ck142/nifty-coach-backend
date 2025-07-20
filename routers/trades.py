from fastapi import APIRouter
import os
import requests
from datetime import datetime, timedelta

router = APIRouter()

DHAN_BASE_URL = "https://api.dhan.co"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")

HEADERS = {
    "accept": "application/json",
    "access-token": ACCESS_TOKEN,
    "client-id": CLIENT_ID
}

@router.post("/sync_trades")
def sync_trades():
    if not ACCESS_TOKEN or not CLIENT_ID:
        return {"error": "Missing ACCESS_TOKEN or CLIENT_ID in environment"}

    url = f"{DHAN_BASE_URL}/orders"
    print(f"[DEBUG] Fetching: {url}")
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return {
            "error": f"Failed to fetch orders: {response.status_code}",
            "details": response.text
        }

    try:
        trades = response.json()
    except Exception as e:
        return {"error": f"Failed to parse response: {e}"}

    filtered = []
    for trade in trades:
        try:
            if trade.get("orderStatus") == "EXECUTED" and "OPTIDX" in trade.get("tradingSymbol", ""):
                filtered.append({
                    "order_id": trade.get("orderId"),
                    "symbol": trade.get("tradingSymbol"),
                    "side": trade.get("transactionType"),
                    "qty": trade.get("quantity"),
                    "price": trade.get("price"),
                    "timestamp": trade.get("exchangeTime")
                })
        except Exception as e:
            print(f"[ERROR] Skipping trade due to: {e}")

    return {
        "message": f"Fetched {len(filtered)} option trades",
        "trades": filtered[:5]  # Preview
    }
