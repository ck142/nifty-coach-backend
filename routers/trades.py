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

    today = datetime.now().date()
    all_trades = []

    for days_ago in range(0, 10):
        trade_date = today - timedelta(days=days_ago)
        trade_date_str = trade_date.strftime("%Y-%m-%d")
        page = 1

        while True:
            url = f"{DHAN_BASE_URL}/history/tradeHistory/{trade_date_str}/{trade_date_str}/{page}"
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 404:
                break
            if response.status_code != 200:
                return {"error": f"Failed to fetch trades: {response.status_code}", "details": response.text}
            trades = response.json()
            if not trades:
                break
            all_trades.extend(trades)
            page += 1

    return {"message": f"Fetched {len(all_trades)} trades", "trades": all_trades[:5]}  # Only preview first 5 for now
