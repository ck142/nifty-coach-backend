from fastapi import APIRouter
from datetime import datetime, timedelta
import requests
import os
from db import save_trade_to_db

router = APIRouter()

DHAN_BASE_URL = "https://api.dhan.co"
ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
CLIENT_ID = os.getenv("DHAN_CLIENT_ID")

HEADERS = {
    "access-token": ACCESS_TOKEN,
    "client-id": CLIENT_ID,
}

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.post("/sync_trades")
def sync_trades():
    today = datetime.today()
    days_back = 10  # You can adjust this
    trades_saved = 0
    all_trades = []

    for i in range(days_back):
        day = today - timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        page = 0
        segment = 3  # NSE FO

        while True:
            url = f"{DHAN_BASE_URL}/history/tradeHistory/{date_str}/{date_str}/{segment}?page={page}"
            print(f"[DEBUG] Fetching: {url}")

            try:
                response = requests.get(url, headers=HEADERS)
                if response.status_code == 404:
                    print(f"[INFO] No more pages for {date_str} after page {page - 1}")
                    break
                elif not response.ok:
                    print(f"[ERROR] {url}: {response.status_code}")
                    print(f"[DEBUG] Response Text: {response.text}")
                    break

                data = response.json()
                trades = data.get("trades", [])

                if not trades:
                    print(f"[INFO] No trades for {date_str} on page {page}")
                    break

                for trade in trades:
                    print(f"[DEBUG] Processing trade: {trade}")
                    try:
                        trade_obj = {
                            "order_id": trade.get("orderId"),
                            "symbol": trade.get("tradingSymbol"),
                            "side": trade.get("transactionType"),
                            "qty": trade.get("quantity"),
                            "price": trade.get("price"),
                            "timestamp": trade.get("exchangeTime"),
                        }
                        if save_trade_to_db(trade_obj):
                            trades_saved += 1
                    except Exception as e:
                        print(f"[ERROR] Skipping trade due to: {e}")
                        continue

                all_trades.extend(trades)
                page += 1
            except Exception as e:
                print(f"[ERROR] Exception occurred while fetching trades: {e}")
                break

    return {"message": f"Synced {trades_saved} new trades.", "trades": all_trades}
